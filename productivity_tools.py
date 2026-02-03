import time
import os
import threading
from plyer import notification

class ProductivityTools:
    def __init__(self):
        self.timer_running = False
        self.stop_timer_flag = False

    def start_pomodoro(self, minutes=25, callback=None):
        self.timer_running = True
        self.stop_timer_flag = False
        seconds = minutes * 60
        
        try:
            while seconds > 0 and not self.stop_timer_flag:
                mins, secs = divmod(seconds, 60)
                timer_str = f"{mins:02d}:{secs:02d}"
                if callback:
                    callback(timer_str)
                time.sleep(1)
                seconds -= 1
            
            if not self.stop_timer_flag:
                # Timer completed naturally
                notification.notify(
                    title="Pomodoro Complete",
                    message="Time for a break! Good job.",
                    app_name="SystemStats App",
                    timeout=10
                )
        except Exception:
            pass
        finally:
            self.timer_running = False

    def stop_timer(self):
        self.stop_timer_flag = True

    def save_note(self, note_content):
        filename = "quick_notes.txt"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(filename, "a", encoding='utf-8') as f:
                f.write(f"[{timestamp}] {note_content}\n")
            return True
        except:
            return False

    def get_notes(self):
        filename = "quick_notes.txt"
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding='utf-8') as f:
                    return f.readlines()
            except:
                return []
        return []
        
    def clear_notes(self):
        filename = "quick_notes.txt"
        if os.path.exists(filename):
             os.remove(filename)
             return True
        return False
