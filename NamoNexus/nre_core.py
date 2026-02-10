import time
import psutil
import os
from datetime import datetime
from dotenv import load_dotenv

# โหลดความลับจาก .env ทันทีที่ไฟล์ถูกเรียก
load_dotenv()

class NRECore:
    def __init__(self):
        self.start_time = time.time()
        self.status = "OFFLINE"
        self._verify_security() # <--- เรียกตรวจความปลอดภัยทันที

    def _verify_security(self):
        """ระบบรักษาความปลอดภัย: ตรวจสอบ Key ก่อนเริ่มทำงาน"""
        api_key = os.getenv("NRE_API_KEY")
        if not api_key:
            raise PermissionError("⛔ FATAL: NRE_API_KEY not found! System Locked.")

        # (ในอนาคตเพิ่ม Logic ตรวจ IP หรือ Token ตรงนี้)
        print("🛡️ [Security] Access Granted. Fortress is secure.")

    def boot_system(self):
        print("⚙️ [NRE] System Booting...")
        time.sleep(0.5)
        self.status = "ONLINE"
        print("✅ [NRE] System Online. All sensors active.")

    def check_health(self):
        return {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "uptime": time.time() - self.start_time
        }

    def log_activity(self, activity_type: str, details: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # ถ้าเป็น Error ร้ายแรง ให้แจ้งเตือนหนักๆ
        prefix = "🔴" if activity_type == "ERROR" else "📝"
        print(f"{prefix} [NRE Log] [{timestamp}] [{activity_type}] {details}")
