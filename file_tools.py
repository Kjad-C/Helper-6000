import os
import hashlib
from concurrent.futures import ThreadPoolExecutor
import subprocess

class FileDoctor:
    def __init__(self):
        pass

    def scan_large_files(self, directory, min_size_mb=100, limit=20):
        large_files = []
        min_size_bytes = min_size_mb * 1024 * 1024
        
        try:
            for root, dirs, files in os.walk(directory):
                for name in files:
                    try:
                        filepath = os.path.join(root, name)
                        # Skip system paths to be safe/fast if scanning absolute root
                        if "Windows" in filepath: continue
                        
                        size = os.path.getsize(filepath)
                        if size > min_size_bytes:
                            large_files.append((filepath, size))
                    except:
                        pass
        except:
            pass
            
        # Sort by size desc
        large_files.sort(key=lambda x: x[1], reverse=True)
        return large_files[:limit]

    def _hash_file(self, filepath, block_size=65536):
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                buf = f.read(block_size)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(block_size)
            return hasher.hexdigest()
        except:
            return None

    def find_duplicates(self, directory):
        # Heavy operation, finding dupes by size first then hash
        size_map = {}
        duplicates = []
        
        # Phase 1: Group by size
        for root, dirs, files in os.walk(directory):
            for name in files:
                try:
                    filepath = os.path.join(root, name)
                    if "Windows" in filepath or "Program Files" in filepath: continue # safety skip
                    
                    size = os.path.getsize(filepath)
                    if size < 1024 * 1024: continue # Skip small files for speed demo
                    
                    if size in size_map:
                        size_map[size].append(filepath)
                    else:
                        size_map[size] = [filepath]
                except:
                    pass
        
        # Phase 2: Check Hash for collisions
        for size, paths in size_map.items():
            if len(paths) > 1:
                hash_map = {}
                for p in paths:
                    h = self._hash_file(p)
                    if h:
                        if h in hash_map:
                            hash_map[h].append(p)
                        else:
                            hash_map[h] = [p]
                
                for h, p_list in hash_map.items():
                    if len(p_list) > 1:
                        duplicates.append((size, p_list))
                        
        return duplicates

    def get_directory_tree_stats(self, directory):
        # Return stricture suitable for tree view + simple size
        tree_counts = {"files": 0, "dirs": 0, "size": 0}
        try:
            for root, dirs, files in os.walk(directory):
                tree_counts["dirs"] += len(dirs)
                tree_counts["files"] += len(files)
                for f in files:
                    try:
                        tree_counts["size"] += os.path.getsize(os.path.join(root, f))
                    except: pass
        except:
            pass
        return tree_counts
