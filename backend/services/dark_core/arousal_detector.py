"""Arousal detection module for analyzing user input keywords."""


class ArousalDetector:
    """Detect arousal levels in user input based on keywords."""

    def __init__(self) -> None:
        """Initialize keyword lists for arousal detection."""
        self.keywords = {
            "high": ["เสียว", "อยาก", "wet", "hard", "touch", "kiss", "จูบ", "กอด", "lick", "เลีย"],
            "medium": ["love", "รัก", "ชอบ", "miss", "คิดถึง", "hot", "ร้อน"],
            "low": ["hello", "hi", "สวัสดี", "talk", "คุย"],
        }

    def analyze(self, text: str) -> float:
        """Analyze text and return an arousal score between 0.0 and 1.0."""
        text = text.lower()
        score = 0.0

        for word in self.keywords["high"]:
            if word in text:
                score += 0.4
        for word in self.keywords["medium"]:
            if word in text:
                score += 0.2

        return min(score, 1.0)
