import json
import os

CONFIG_FILE = "app_config.json"

DEFAULT_CONFIG = {
    "theme_color": "cyan",
    "refresh_rate": 1.0,
    "enable_notifications": True,
    "keep_history_days": 7,
    "auto_launch_dashboard": False,
    "temperature_unit": "C",
    "show_splash_screen": True,
    "default_view": "Main Menu",
    "logging_level": "INFO",
    "warn_battery_percent": 20,
    "check_updates_on_start": True
}

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return {**DEFAULT_CONFIG, **json.load(f)} # Merge with defaults
            except:
                pass
        return DEFAULT_CONFIG.copy()

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=4)
            return True
        except:
            return False

    def get(self, key):
        return self.config.get(key, DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
