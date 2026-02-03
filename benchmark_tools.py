import time
import os
import random
import psutil

class SystemBenchmark:
    def __init__(self):
        pass

    def cpu_stress_test(self, duration_sec=5):
        # Calculate primes to stress CPU
        start = time.time()
        count = 0
        while time.time() - start < duration_sec:
            # simple sieve or just division check
            n = 10000 + count
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    break
            count += 1
        return count # Score based on operations

    def disk_write_speed(self):
        # Create 100MB file
        filename = "bench_test.tmp"
        size_mb = 100
        data = os.urandom(1024 * 1024) # 1MB junk
        
        start = time.time()
        try:
            with open(filename, "wb") as f:
                for _ in range(size_mb):
                    f.write(data)
            end = time.time()
            duration = end - start
            speed = size_mb / duration
            
            # Clean up
            os.remove(filename)
            return f"{speed:.2f} MB/s"
        except:
            return "Error"

    def memory_check(self):
        # Allocate a large list and check
        try:
            # 100MB alloc
            big_list = [random.random() for _ in range(10**7)]
            # Sort it
            big_list.sort()
            del big_list
            return "Pass (Allocation & Sort OK)"
        except Exception as e:
            return f"Fail: {e}"
