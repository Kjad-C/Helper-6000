
import os
import shutil
import subprocess
import glob
import ctypes
import platform
import sys

class MaintenanceManager:
    def __init__(self):
        pass

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def get_temp_size(self):
        temp_path = os.environ.get('TEMP')
        total_size = 0
        file_count = 0
        try:
            for dirpath, dirnames, filenames in os.walk(temp_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        try:
                            total_size += os.path.getsize(fp)
                            file_count += 1
                        except OSError:
                            pass
        except Exception:
            pass
        
        return total_size, file_count

    def clear_temp_files(self):
        temp_path = os.environ.get('TEMP')
        deleted_size = 0
        deleted_files = 0
        errors = 0
        
        for dirpath, dirnames, filenames in os.walk(temp_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    size = os.path.getsize(fp)
                    os.remove(fp)
                    deleted_size += size
                    deleted_files += 1
                except Exception:
                    errors += 1
                    
        return deleted_files, deleted_size, errors

    def run_disk_cleanup(self):
        try:
            # Try launching with shell=True for better path resolution
            subprocess.Popen("cleanmgr", shell=True)
            return True
        except Exception as e:
            return False

    def run_drive_optimization(self):
        try:
            # dfrgui is strictly a Windows utility. 
            # Using 'start' via shell often helps resolve it correctly if simple Popen fails.
            subprocess.Popen('start dfrgui', shell=True)
            return True
        except Exception as e:
            # Fallback to direct path if needed, though 'start' usually works
            try:
                subprocess.Popen(r"C:\Windows\System32\dfrgui.exe", shell=True)
                return True
            except:
                return False

    def flush_dns(self):
        try:
            subprocess.run(["ipconfig", "/flushdns"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False

    def network_connectivity_test(self, host="8.8.8.8"):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '4', host]
        try:
            # Hide console window for the subprocess
            startupinfo = None
            if platform.system().lower() == 'windows':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
            output = subprocess.check_output(command, startupinfo=startupinfo).decode()
            if "TTL=" in output:
                for line in output.split('\n'):
                    if "Average" in line:
                         # Extract proper timing
                         return line.strip().split(',')[-1].strip()
                return "Online (Latency Unknown)"
            else:
                return "Unreachable"
        except Exception:
            return "Failed to ping"
            
    def open_task_manager(self):
        try:
            subprocess.Popen("taskmgr", shell=True)
            return True
        except:
            return False
            
    def open_control_panel(self):
         try:
            subprocess.Popen("control", shell=True)
            return True
         except:
            return False
