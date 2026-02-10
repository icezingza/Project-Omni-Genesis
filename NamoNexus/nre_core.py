import time
import psutil
from datetime import datetime

class NRECore:
    def __init__(self):
        self.start_time = time.time()
        self.status = "OFFLINE"

    def boot_system(self):
        print("⚙️ [NRE] System Booting...")
        time.sleep(1)
        self.status = "ONLINE"
        print("✅ [NRE] System Online. All sensors active.")

    def check_health(self):
        """ตรวจสอบสถานะระบบ (CPU, RAM)"""
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        return {"cpu": cpu_usage, "ram": memory_usage, "uptime": time.time() - self.start_time}

    def log_activity(self, activity_type: str, details: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"📝 [NRE Log] [{timestamp}] [{activity_type}] {details}")
