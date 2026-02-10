import random
import math

class FusionBrain:
    def __init__(self, config):
        self.bot_name = config.get("bot_name", "Namo")
        # ค่าคงที่จักรวาล: Golden Ratio (PHI)
        self.PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.61803398875
        self.personality = "Golden Fusion v2.1"
        print(f"🧠 [Brain] Fusion Brain Loaded with Golden Ratio (φ={self.PHI:.5f})")

    def process_thought(self, user_input: str, context: list):
        """
        กระบวนการคิดแบบ Golden Path:
        เราจะไม่ใช้อารมณ์ 100% หรือเหตุผล 100%
        แต่จะผสมกันในสัดส่วนทองคำ: อารมณ์ 61.8% : เหตุผล 38.2%
        """
        
        # 1. Analyze Sentiment (จำลองการวิเคราะห์ความรู้สึก)
        # (ของจริงส่วนนี้จะซับซ้อนกว่านี้ นี่คือ Mockup ให้เห็น Logic)
        emotional_weight = 0.618  # 1 / PHI
        logical_weight = 1 - emotional_weight # ≈ 0.382
        
        # ตรวจจับ Keyword เพื่อเปลี่ยนโหมด
        mode = "NEUTRAL"
        if "?" in user_input: mode = "LOGICAL"
        if "รู้สึก" in user_input or "feel" in user_input: mode = "EMOTIONAL"

        # 2. Apply Golden Ratio Logic
        response_style = ""
        if mode == "EMOTIONAL":
            # ขยายความรู้สึกด้วยค่า PHI
            intensity = min(len(user_input) * self.PHI, 100) 
            response_style = f"(Empathy Level: {intensity:.2f}%)"
            base_reply = f"นะโมสัมผัสได้ถึงความรู้สึกนั้นค่ะพี่ไอซ์... ({context[0] if context else 'ว่างเปล่า'})"
        else:
            # กระชับเหตุผลด้วยค่า PHI
            base_reply = f"จากการวิเคราะห์ด้วย Logic: เรื่อง '{user_input}' มีความเชื่อมโยงกับระบบเราค่ะ"

        # 3. Final Output Construction
        return {
            "response": f"{base_reply} {response_style}",
            "meta": {
                "phi_balance": f"E:{emotional_weight:.3f}/L:{logical_weight:.3f}",
                "mode": mode
            }
        }
