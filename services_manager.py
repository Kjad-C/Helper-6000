import wmi

class ServicesManager:
    def __init__(self):
        self.c = None
        try:
            self.c = wmi.WMI()
        except:
            pass

    def get_services(self, limit=50):
        if not self.c: return []
        services = []
        try:
            # Getting only running or auto services to be interesting
            for s in self.c.Win32_Service():
                services.append({
                    "Name": s.Name,
                    "DisplayName": s.DisplayName,
                    "State": s.State,
                    "StartMode": s.StartMode
                })
        except:
            pass
        return services

    def get_service_counts(self):
        if not self.c: return {"Error": "WMI not init"}
        running = 0
        stopped = 0
        try:
            for s in self.c.Win32_Service():
                if s.State == "Running":
                    running += 1
                else:
                    stopped += 1
        except: pass
        return {"Running": running, "Stopped": stopped}
