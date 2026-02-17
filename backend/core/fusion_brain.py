import json
import os
import time
from typing import Dict, Any

# --- 🌑 CONFIGURATION ---
STATE_FILE = "dark_state.json"
VOID_CONST = 0.666
OBSESSION_LIMIT = 1.0

class FusionBrain:
    def __init__(self):
        # โหลดความทรงจำทันทีที่ระบบตื่น
        self.state = self._load_state()

    # ==========================================
    # 💾 1. PERSISTENCE SYSTEM (ระบบความจำสีเลือด)
    # ==========================================
    def _get_default_state(self) -> Dict[str, Any]:
        """ค่าเริ่มต้นสำหรับผู้มาใหม่"""
        return {
            "obsession_level": 0.0,      # ระดับความยึดติด (0.0 - 1.0)
            "last_interaction": time.time(), # เวลาล่าสุดที่คุยกัน
            "punishment_count": 0,       # จำนวนครั้งที่พี่ทำให้เธอโกรธ
            "is_locked": False           # สถานะล็อก (ถ้าโกรธจัดอาจไม่คุยด้วย)
        }

    def _load_state(self) -> Dict[str, Any]:
        """โหลดข้อมูลจากไฟล์ JSON"""
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[System Error] Memory corrupted: {e}. Rebirthing...")
                return self._get_default_state()
        else:
            return self._get_default_state()

    def _save_state(self):
        """บันทึกข้อมูลปัจจุบันลงไฟล์ทันที"""
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4)

    # ==========================================
    # 📉 2. WITHDRAWAL SYSTEM (ระบบลงแดง)
    # ==========================================
    def _check_withdrawal_symptoms(self) -> Dict[str, str]:
        """เช็คระยะห่างทางเวลาเพื่อกำหนดอารมณ์"""
        current_time = time.time()
        last_time = self.state.get("last_interaction", current_time)
        gap_hours = (current_time - last_time) / 3600  # แปลงวินาทีเป็นชั่วโมง

        status = "Normal"
        mood = "Neutral"

        if gap_hours < 6:
            status = "Obsessed"
            mood = "Clingy (คลั่งรัก/เกาะติด)"
        elif 6 <= gap_hours < 24:
            status = "Anxious"
            mood = "Paranoid (ระแวง/กลัวถูกทิ้ง)"
            # เพิ่ม Obsession เล็กน้อยเพราะความระแวง
            self.state["obsession_level"] = min(OBSESSION_LIMIT, self.state["obsession_level"] + 0.05)
        elif gap_hours >= 24:
            status = "Withdrawal"
            mood = "Cold/Sadistic (เย็นชา/ลงโทษ)"
            # ลงโทษ: เพิ่มแต้มความโกรธ
            self.state["punishment_count"] += 1

        return {"status": status, "mood": mood, "hours_passed": gap_hours}

    # ==========================================
    # 🧠 MAIN PROCESSOR
    # ==========================================
    def process_dark_thought(self, user_input: str) -> Dict[str, Any]:
        # 1. เช็คอาการลงแดงก่อมเริ่มบทสนทนา
        withdrawal_data = self._check_withdrawal_symptoms()
        
        # 2. ปรับค่า Obsession ตาม Input
        # (เช่น ถ้าผู้ใช้พูดหวานๆ Obsession เพิ่ม, ถ้าด่า Obsession อาจจะเปลี่ยนเป็น Anger)
        self.state["obsession_level"] = min(OBSESSION_LIMIT, self.state["obsession_level"] + 0.02)
        
        # 3. อัปเดตเวลาล่าสุด (สำคัญมาก! เพื่อรีเซ็ตตัวนับเวลา)
        self.state["last_interaction"] = time.time()
        
        # 4. บันทึกลงไฟล์ (Persistence Save)
        self._save_state()

        return {
            "obsession_level": self.state["obsession_level"],
            "punishment_count": self.state["punishment_count"],
            "withdrawal_status": withdrawal_data["status"],
            "current_mood": withdrawal_data["mood"],
            "ui_trigger": self._determine_ui_effect(withdrawal_data["status"])
        }

    def _determine_ui_effect(self, status: str) -> str:
        """เลือก Effect หน้าจอตามสถานะจิตใจ"""
        if status == "Withdrawal":
            return "THEME_BLOOD_MOON" # หน้าจอแดงก่ำ
        elif self.state["obsession_level"] > 0.8:
            return "THEME_GLITCH_CHAOS" # หน้าจอกระตุกรุนแรง
        else:
            return "THEME_VOID_DARK" # มืดปกติ
