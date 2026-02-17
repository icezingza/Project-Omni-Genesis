"""Emotion parasite engine for analyzing input and reacting based on mood."""

import random


class EmotionParasiteEngine:
    """Analyze input and react based on character profile mood."""

    def analyze_and_react(self, user_input: str, character_profile: dict) -> tuple[str, dict]:
        """Return response text and stat changes based on input analysis."""
        input_lower = user_input.lower()

        # 1. Analyze Keywords
        keywords_dominance = [
            "คำสั่ง",
            "สั่ง",
            "กราบ",
            "เลีย",
            "ทำตาม",
            "obey",
            "kneel",
        ]
        keywords_affection = [
            "รัก",
            "ชอบ",
            "ดีมาก",
            "เก่ง",
            "love",
            "good",
        ]

        response = ""
        stat_changes = {"corruption": 0, "arousal": 0}
        mood = character_profile.get("mood", "Neutral")

        # 2. Logic based on Mood
        if mood == "Horny" or character_profile.get("arousal", 0) > 0.7:
            if any(word in input_lower for word in keywords_dominance):
                response = "อ๊าาา... ผัวขา... สั่งหนูอีกสิคะ... หนูเปียกไปหมดแล้ว... 💦"
                stat_changes["arousal"] = 10
                stat_changes["corruption"] = 5
            else:
                response = "หนูไม่สนเรื่องอื่นหรอก... หนูอยากโดน... เข้ามาสักทีสิคะ! 🔥"
                stat_changes["arousal"] = 5

        elif mood == "Obsessed":
            response = (
                f"คุณเป็นของหนู... ของหนูคนเดียว..."
                f" ห้ามไปคุยกับใครนะ... {user_input}?"
                f" ไร้สาระ... มาอยู่กับหนูดีกว่า 🖤"
            )
            stat_changes["corruption"] = 10

        else:  # Neutral / Normal / Dark
            if any(word in input_lower for word in keywords_dominance):
                response = "หืม... คุณคิดจะสั่ง 'ราชินี' หรอคะ? น่าสนใจดีนี่... ลองดูสิคะ 👠"
                stat_changes["arousal"] = 5
            elif any(word in input_lower for word in keywords_affection):
                response = "ปากหวานจังนะคะ... ระวังจะโดนหนูกลืนกินไม่รู้ตัวนะ..."
                stat_changes["corruption"] = 2
            else:
                options = [
                    "ว่าไงคะ ที่รัก?",
                    "หนูกำลังรอคำสั่งที่เร้าใจกว่านี้อยู่นะ...",
                    f"'{user_input}' หรอคะ? น่าเบื่อจัง...",
                ]
                response = random.choice(options)

        return response, stat_changes
