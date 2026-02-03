import speedtest
import socket
import requests
import json
import concurrent.futures

class NetworkToolkit:
    def __init__(self):
        pass
        
    def get_public_ip(self):
        try:
            return requests.get('https://api.ipify.org').text
        except:
            return "Unknown"

    def get_geoip_info(self):
        try:
            response = requests.get('http://ip-api.com/json/')
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}

    def run_speedtest(self):
        # This can be slow, needs to be run with a status spinner
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000      # Convert to Mbps
            ping = st.results.ping
            return {
                "download": f"{download_speed:.2f} Mbps",
                "upload": f"{upload_speed:.2f} Mbps",
                "ping": f"{ping:.2f} ms"
            }
        except Exception as e:
            return {"error": str(e)}

    def scan_common_ports(self, host="127.0.0.1"):
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 
            443: "HTTPS", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Proxy"
        }
        
        open_ports = []
        
        def check_port(port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                return (port, common_ports[port])
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_port = {executor.submit(check_port, port): port for port in common_ports}
            for future in concurrent.futures.as_completed(future_to_port):
                res = future.result()
                if res:
                    open_ports.append(res)
                    
        return sorted(open_ports)
