import psutil
import platform
import datetime
import os
import socket
import time

class StatsManager:
    def __init__(self):
        pass

    def get_boot_time(self):
        boot_timestamp = psutil.boot_time()
        bt = datetime.datetime.fromtimestamp(boot_timestamp)
        return bt.strftime("%Y-%m-%d %H:%M:%S")

    def get_uptime(self):
        boot_timestamp = psutil.boot_time()
        now_timestamp = time.time()
        uptime_seconds = now_timestamp - boot_timestamp
        
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

    def get_system_info(self):
        uname = platform.uname()
        return {
            "System": uname.system,
            "Node Name": uname.node,
            "Release": uname.release,
            "Version": uname.version,
            "Machine": uname.machine,
            "Processor": uname.processor,
            "Architecture": platform.architecture()[0],
        }

    def get_cpu_info(self):
        freq = psutil.cpu_freq()
        return {
            "Physical Cores": psutil.cpu_count(logical=False),
            "Total Cores": psutil.cpu_count(logical=True),
            "Max Frequency": f"{freq.max:.2f}Mhz" if freq else "N/A",
            "Current Frequency": f"{freq.current:.2f}Mhz" if freq else "N/A",
            "CPU Usage": f"{psutil.cpu_percent(interval=0.1)}%"
        }

    def get_memory_info(self):
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        def get_size(bytes, suffix="B"):
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor
        return {
            "Total RAM": get_size(svmem.total),
            "Available RAM": get_size(svmem.available),
            "Used RAM": get_size(svmem.used),
            "RAM Percentage": f"{svmem.percent}%",
            "Total Swap": get_size(swap.total),
            "Used Swap": get_size(swap.used),
            "Swap Percentage": f"{swap.percent}%"
        }

    def get_disk_info(self):
        partitions = []
        try:
            for part in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    partitions.append({
                        "Device": part.device,
                        "Mountpoint": part.mountpoint,
                        "File System": part.fstype,
                        "Total Size": f"{usage.total / (1024**3):.2f} GB",
                        "Used": f"{usage.used / (1024**3):.2f} GB",
                        "Free": f"{usage.free / (1024**3):.2f} GB",
                        "Percentage": f"{usage.percent}%"
                    })
                except PermissionError:
                    continue
        except Exception:
            pass
        return partitions
        
    def get_disk_io(self):
        try:
            io = psutil.disk_io_counters()
            if io:
                return {
                    "Read Count": io.read_count,
                    "Write Count": io.write_count,
                    "Read Bytes": io.read_bytes,
                    "Write Bytes": io.write_bytes
                }
        except:
            pass
        return {}

    def get_network_info(self):
        net_io = psutil.net_io_counters()
        def get_size(bytes, suffix="B"):
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor
        return {
            "Total Bytes Sent": get_size(net_io.bytes_sent),
            "Total Bytes Received": get_size(net_io.bytes_recv),
            "Hostname": socket.gethostname(),
            "IP Address": socket.gethostbyname(socket.gethostname())
        }

    def get_battery_info(self):
        if not hasattr(psutil, "sensors_battery"):
            return "N/A"
        battery = psutil.sensors_battery()
        if battery:
            return {
                "Percentage": f"{battery.percent}%",
                "Power Plugged": "Yes" if battery.power_plugged else "No",
                "Time Left": f"{battery.secsleft / 60:.2f} min" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
            }
        return "Battery not detected"

    def get_running_processes_summary(self):
        # Count total processes
        total_procs = len(psutil.pids())
        
        # Get top resource hogs
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                procs.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Top CPU
        top_cpu = sorted(procs, key=lambda p: p['cpu_percent'], reverse=True)[:3]
        # Top Memory
        top_mem = sorted(procs, key=lambda p: p['memory_percent'], reverse=True)[:3]
        
        return {
            "Total Processes": total_procs,
            "Top CPU Processes": top_cpu,
            "Top Memory Processes": top_mem
        }
