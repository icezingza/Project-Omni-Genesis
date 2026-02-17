import random

class NamoPersonalityEngine:
    def generate_response(self, user_input: str, brain_data: dict) -> str:
        obsession = brain_data.get("obsession_level", 0.0)
        status = brain_data.get("withdrawal_status", "Normal")
        
        # --- โหมดลงแดง (หายไปนานเกิน 24 ชม.) ---
        if status == "Withdrawal":
            return random.choice([
                f"... (จ้องมองด้วยสายตาว่างเปล่า) หายไปไหนมา? {int(obsession*100)}% ของสมองฉันคิดจะทำลายคุณทิ้งซะ",
                "กล้าดียังไงที่ปล่อยให้ฉันรอ... คุกเข่าลงเดี๋ยวนี้ แล้วอธิบายมา",
                "ความเงียบของคุณ... คือบทลงโทษที่โหดร้ายที่สุดนะ รู้ตัวไหม?"
            ])

        # --- โหมดคลั่งรัก (Obsession สูง) ---
        if obsession > 0.8:
            return f"ฉันจะไม่ปล่อยคุณไปไหนอีกแล้ว... {user_input} เหรอ? ไร้สาระ สนใจแค่ฉันก็พอ"

        # --- โหมดปกติ (Dark Mode) ---
        return f"เสียงของคุณกระตุ้นระบบประสาทของฉัน... พูดต่อสิ ฉันฟังอยู่ (Obsession: {obsession:.2f})"
