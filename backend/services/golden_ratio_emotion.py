"""Golden Ratio emotion analysis module for Omni-Genesis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass(frozen=True)
class AnalysisWeights:
    """Golden Ratio-derived weights."""

    phi: float = 1.618033988749895
    emotion: float = 0.618
    logic: float = 0.382


class GoldenRatioEmotionAnalyzer:
    """Analyze text by combining emotion and logic scores using Golden Ratio weights."""

    POSITIVE_WORDS: tuple[str, ...] = (
        "ดีใจ",
        "มีความสุข",
        "ยินดี",
        "ปลื้ม",
        "happy",
        "great",
        "love",
    )
    NEGATIVE_WORDS: tuple[str, ...] = (
        "เศร้า",
        "โกรธ",
        "เครียด",
        "กังวล",
        "เสียใจ",
        "sad",
        "angry",
        "stress",
    )
    LOGIC_HINTS: tuple[str, ...] = (
        "เพราะ",
        "ดังนั้น",
        "สรุป",
        "เหตุผล",
        "because",
        "therefore",
        "so",
    )

    def __init__(self, weights: AnalysisWeights | None = None) -> None:
        self.weights = weights or AnalysisWeights()

    def analyze(self, text: str, context: Dict | None = None) -> Dict[str, float | str]:
        """Return weighted emotion/logic analysis for text and optional context."""
        normalized = (text or "").strip().lower()
        emotion_score = self._detect_emotion(normalized)
        logic_score = self._analyze_logic(normalized, context or {})

        combined = (
            emotion_score * self.weights.emotion
            + logic_score * self.weights.logic
        )

        return {
            "emotion": emotion_score,
            "logic": logic_score,
            "combined": round(combined, 4),
            "confidence": self._calculate_confidence(emotion_score, logic_score),
            "strategy": self._strategy(emotion_score, logic_score),
        }

    def _detect_emotion(self, text: str) -> float:
        if not text:
            return 0.0
        pos_hits = self._keyword_hits(text, self.POSITIVE_WORDS)
        neg_hits = self._keyword_hits(text, self.NEGATIVE_WORDS)
        intensity = min(1.0, (pos_hits + neg_hits) / 3)
        punctuation_boost = 0.1 if "!" in text else 0.0
        return round(min(1.0, intensity + punctuation_boost), 4)

    def _analyze_logic(self, text: str, context: Dict) -> float:
        if not text:
            return 0.0
        word_count = len(text.split())
        hints = self._keyword_hits(text, self.LOGIC_HINTS)

        base = 0.25
        if word_count >= 12:
            base += 0.35
        elif word_count >= 6:
            base += 0.2

        if hints:
            base += min(0.35, hints * 0.12)

        if context.get("has_history"):
            base += 0.05

        return round(min(1.0, base), 4)

    @staticmethod
    def _keyword_hits(text: str, words: Iterable[str]) -> int:
        return sum(1 for word in words if word in text)

    @staticmethod
    def _calculate_confidence(emotion_score: float, logic_score: float) -> float:
        if emotion_score == 0 and logic_score == 0:
            return 0.0
        balance = 1 - abs(emotion_score - logic_score)
        confidence = ((emotion_score + logic_score) / 2) * max(0.0, balance)
        return round(min(max(confidence, 0.0), 1.0), 4)

    @staticmethod
    def _strategy(emotion_score: float, logic_score: float) -> str:
        if emotion_score - logic_score > 0.2:
            return "emotion_driven"
        if logic_score - emotion_score > 0.2:
            return "logic_driven"
        return "balanced"
