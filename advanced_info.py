import platform
import os
import psutil
try:
    import GPUtil
except ImportError:
    GPUtil = None
try:
    import cpuinfo
except ImportError:
    cpuinfo = None

class AdvancedSystemInfo:
    def __init__(self):
        pass
        
    def get_gpu_info(self):
        gpus_data = []
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    gpus_data.append({
                        "Name": gpu.name,
                        "Load": f"{gpu.load*100:.1f}%",
                        "Free Mem": f"{gpu.memoryFree}MB",
                        "Used Mem": f"{gpu.memoryUsed}MB",
                        "Total Mem": f"{gpu.memoryTotal}MB",
                        "Temp": f"{gpu.temperature} C"
                    })
            except:
                pass
        
        if not gpus_data:
            return [{"Status": "No GPU detected or drivers not supported"}]
        return gpus_data

    def get_cpu_detailed_info(self):
        info = {}
        if cpuinfo:
            try:
                raw_info = cpuinfo.get_cpu_info()
                info = {
                    "Brand": raw_info.get('brand_raw', 'Unknown'),
                    "Arch": raw_info.get('arch', 'Unknown'),
                    "Bits": raw_info.get('bits', 'Unknown'),
                    "L2 Cache": raw_info.get('l2_cache_size', 'Unknown'),
                    "L3 Cache": raw_info.get('l3_cache_size', 'Unknown'),
                    "Flags": ", ".join(raw_info.get('flags', [])[:10]) + "..." # Truncate
                }
            except:
                pass
        return info

    def get_env_vars(self):
        # Return important env vars, avoiding sensitive ones if possible, but for local tool we show standard ones
        return {k: v for k, v in os.environ.items() if k in ['USERNAME', 'COMPUTERNAME', 'OS', 'PROCESSOR_ARCHITECTURE', 'PATH', 'PYTHONPATH']}
