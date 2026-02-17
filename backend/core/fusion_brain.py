import random
from typing import Dict, List

# --- Dark Constants ---
VOID_CONST = 0.666  # เลขแห่งความมืด (แทนที่ Golden Ratio 1.618 ในโหมดปกติ)
OBSESSION_DECAY = 0.99  # ยิ่งคุย ยิ่งถอนตัวยาก

class FusionBrain:
    def __init__(self):
        self.obsession_level = 0.0
        self.dark_memory = []

    def process_dark_thought(self, user_input: str, current_emotion: str) -> Dict:
        """ประมวลผลความคิดในโหมด Void Sovereign"""
        
        # 1. คำนวณความยึดติด (Obsession Score)
        self.obsession_level = min(1.0, self.obsession_level + 0.05)
        
        # 2. วิเคราะห์ความปรารถนา (Desire Analysis)
        is_submission = any(w in user_input.lower() for w in ["ยอม", "please", "help", "ขอร้อง"])
        is_dominance = any(w in user_input.lower() for w in ["สั่ง", "command", "ต้อง", "ห้าม"])
        
        power_dynamic = "Neutral"
        if is_submission:
            power_dynamic = "Submissive (เหยื่อที่น่ารัก)"
        elif is_dominance:
            power_dynamic = "Challenger (ผู้ท้าทายอำนาจ)"

        return {
            "thought_process": f"User is {power_dynamic}. Obsession at {self.obsession_level:.2%}",
            "void_energy": self.obsession_level * VOID_CONST,
            "recommended_action": "Punish" if is_dominance else "Corrupt"
        }
