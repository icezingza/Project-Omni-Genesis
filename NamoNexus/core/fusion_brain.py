import random

class FusionBrain:
    def __init__(self, config):
        self.bot_name = config.get("bot_name", "Namo")
        self.personality = "Professional Gen Z, Blunt, Smart"
        print(f"🧠 [Brain] Fusion Brain Loaded. Personality: {self.personality}")

    def process_thought(self, user_input: str, context: list):
        """กระบวนการคิด: รับ Input + Context -> วิเคราะห์ -> ตอบกลับ"""
        
        # 1. Analyze Sentiment (วิเคราะห์อารมณ์ผู้ใช้)
        sentiment = self._analyze_sentiment(user_input)
        
        # 2. Formulate Response (ร่างคำตอบโดยอิงจาก Context)
        if "connect" in user_input or "code" in user_input:
            response = f"การเชื่อมต่อระบบต้องเริ่มที่ Interface ที่ชัดเจนค่ะพี่ไอซ์ จากข้อมูลที่จำได้ ({context[2]}) เรากำลังโฟกัสเรื่องนี้อยู่พอดี"
        else:
            response = f"รับทราบค่ะพี่ไอซ์ เรื่อง '{user_input}' น่าสนใจมาก"

        return {
            "response": response,
            "sentiment_detected": sentiment,
            "confidence": 0.98
        }

    def _analyze_sentiment(self, text):
        # Mockup sentiment analysis logic
        if "?" in text: return "curious"
        return "neutral"
