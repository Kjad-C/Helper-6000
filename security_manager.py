import psutil
import os
import subprocess
import json

class SecurityManager:
    def __init__(self):
        pass

    def check_suspicious_processes(self):
        # Very basic heuristic: check for processes running from temp or strange locations
        suspicious = []
        try:
            for p in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
                try:
                    exe = p.info['exe']
                    if exe:
                        exe_lower = exe.lower()
                        if 'appdata\\local\\temp' in exe_lower:
                            suspicious.append({
                                "pid": p.info['pid'],
                                "name": p.info['name'],
                                "reason": "Running from TEMP folder"
                            })
                        # Check for miners (naive check)
                        if 'xmrig' in exe_lower or 'minerd' in exe_lower:
                            suspicious.append({
                                "pid": p.info['pid'],
                                "name": p.info['name'],
                                "reason": "Known miner name"
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception:
            pass
        return suspicious

    def list_pip_packages(self):
        try:
            result = subprocess.check_output("pip list --format=json", shell=True)
            return json.loads(result.decode())
        except:
            return []

    def check_firewall_status(self):
        # PowerShell command to check Windows Firewall
        cmd = "Get-NetFirewallProfile | Format-Table Name, Enabled -AutoSize"
        try:
            output = subprocess.check_output(["powershell", "-Command", cmd], creationflags=subprocess.CREATE_NO_WINDOW).decode()
            return output.strip()
        except:
            return "Could not determine firewall status."

    def list_startup_apps(self):
        # Checking startup folder (basic)
        startup_items = []
        user_startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        if os.path.exists(user_startup):
            for f in os.listdir(user_startup):
                startup_items.append(f)
        return startup_items

    def check_listening_ports(self):
         # Returns list of connections that are LISTENING from non-loopback
         listening = []
         try:
             conns = psutil.net_connections(kind='inet')
             for c in conns:
                 if c.status == 'LISTEN':
                     if c.laddr.ip not in ('127.0.0.1', '::1', '0.0.0.0'):
                         listening.append({
                             "ip": c.laddr.ip,
                             "port": c.laddr.port,
                             "pid": c.pid
                         })
         except:
             pass
         return listening
