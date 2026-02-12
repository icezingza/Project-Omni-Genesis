"""
Project Omni-Genesis: Thai NLP Engine
Provides Thai language processing — tokenization, emotion detection,
formality analysis, and text normalization.

Falls back gracefully when PyThaiNLP is not installed.
"""

import logging
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger("omni_genesis.thai_nlp")

# --- Try importing PyThaiNLP ---
try:
    from pythainlp.tokenize import word_tokenize as _thai_tokenize
    from pythainlp.util import normalize as _thai_normalize

    PYTHAINLP_AVAILABLE = True
    logger.info("PyThaiNLP loaded successfully")
except ImportError:
    PYTHAINLP_AVAILABLE = False
    logger.warning("PyThaiNLP not installed — using fallback tokenizer")


# --- Thai Emotion Vocabulary ---
THAI_EMOTION_KEYWORDS: Dict[str, List[str]] = {
    "joy": [
        "ดีใจ", "สนุก", "มีความสุข", "ยินดี", "เฮ", "สุขใจ",
        "ตื่นเต้น", "ปลื้ม", "หัวเราะ", "555", "ขอบคุณ",
    ],
    "sadness": [
        "เศร้า", "เสียใจ", "ร้องไห้", "ผิดหวัง", "โศก",
        "หดหู่", "เหงา", "คิดถึง", "ทุกข์", "ใจสลาย",
    ],
    "anger": [
        "โกรธ", "หงุดหงิด", "โมโห", "บ้า", "เกลียด",
        "รำคาญ", "ฉุนเฉียว", "อารมณ์เสีย",
    ],
    "fear": [
        "กลัว", "หวาดกลัว", "ตกใจ", "ระแวง", "วิตก",
        "กังวล", "เครียด", "หวาดผวา",
    ],
    "love": [
        "รัก", "คิดถึง", "ที่รัก", "หัวใจ", "กอด",
        "จูบ", "ดูแล", "ห่วงใย", "แฟน",
    ],
    "neutral": [
        "สวัสดี", "ครับ", "ค่ะ", "อะไร", "ทำไม",
        "ยังไง", "ได้", "ไม่", "ใช่",
    ],
}

# --- Formality Markers ---
FORMAL_PARTICLES = ["ครับ", "ค่ะ", "คะ", "ขอรับ", "เจ้าค่ะ"]
CASUAL_PARTICLES = ["จ้า", "จ้ะ", "นะ", "อ่ะ", "ว่ะ", "เว้ย", "โว้ย", "555"]

# --- Thai Idioms ---
THAI_IDIOMS: Dict[str, str] = {
    "น้ำขึ้นให้รีบตัก": "seize_opportunity",
    "ช้าๆ ได้พร้าเล่มงาม": "patience_rewarded",
    "กว่าถั่วจะสุก งาก็ไหม้": "trade_off",
    "ปากหวาน ก้นเปรี้ยว": "deception",
    "รักวัวให้ผูก รักลูกให้ตี": "tough_love",
}


@dataclass
class EmotionResult:
    """Result of Thai emotion detection."""
    emotion: str
    confidence: float
    keywords_found: List[str] = field(default_factory=list)


@dataclass
class FormalityResult:
    """Result of formality detection."""
    level: str  # "formal", "casual", "neutral"
    score: float  # 0.0 (very casual) to 1.0 (very formal)
    markers_found: List[str] = field(default_factory=list)


class ThaiNLPEngine:
    """
    Thai language NLP engine with tokenization, emotion detection,
    formality analysis, and text normalization.
    """

    def __init__(self):
        self.emotion_keywords = THAI_EMOTION_KEYWORDS
        self.idioms = THAI_IDIOMS

    # ------------------------------------------------------------------
    # Tokenization
    # ------------------------------------------------------------------
    def tokenize(self, text: str) -> List[str]:
        """
        Segment Thai text into words.
        Uses PyThaiNLP if available, otherwise falls back to character-level split.
        """
        if not text or not text.strip():
            return []

        if PYTHAINLP_AVAILABLE:
            return _thai_tokenize(text, engine="newmm")

        # Fallback: split on whitespace and common punctuation
        return [tok for tok in re.split(r"[\s,;!?。、]+", text) if tok]

    # ------------------------------------------------------------------
    # Text Normalization
    # ------------------------------------------------------------------
    def normalize(self, text: str) -> str:
        """
        Normalize Thai text — collapse whitespace, normalize Unicode forms,
        and reduce repeated characters (e.g. 5555555 → 555).
        """
        if not text:
            return ""

        if PYTHAINLP_AVAILABLE:
            text = _thai_normalize(text)

        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text).strip()

        # Reduce excessive repetition (e.g. "555555" → "555")
        text = re.sub(r"(.)\1{4,}", r"\1\1\1", text)

        return text

    # ------------------------------------------------------------------
    # Emotion Detection
    # ------------------------------------------------------------------
    def detect_emotion(self, text: str) -> EmotionResult:
        """
        Detect the dominant emotion in Thai text using keyword matching.

        Returns:
            EmotionResult with emotion label, confidence, and matched keywords.
        """
        if not text:
            return EmotionResult(emotion="neutral", confidence=0.0)

        normalized = self.normalize(text)
        tokens = self.tokenize(normalized)
        tokens_lower = [t.lower() for t in tokens]

        scores: Dict[str, Tuple[float, List[str]]] = {}

        for emotion, keywords in self.emotion_keywords.items():
            matched = [kw for kw in keywords if kw in normalized or kw in tokens_lower]
            if matched:
                # Confidence = proportion of keywords matched, capped at 1.0
                confidence = min(len(matched) / max(len(tokens), 1) * 2.0, 1.0)
                scores[emotion] = (confidence, matched)

        if not scores:
            return EmotionResult(emotion="neutral", confidence=0.3)

        # Pick highest-scoring emotion
        best_emotion = max(scores, key=lambda e: scores[e][0])
        best_conf, best_kws = scores[best_emotion]

        return EmotionResult(
            emotion=best_emotion,
            confidence=round(best_conf, 4),
            keywords_found=best_kws,
        )

    # ------------------------------------------------------------------
    # Formality Detection
    # ------------------------------------------------------------------
    def detect_formality(self, text: str) -> FormalityResult:
        """
        Determine the formality level of Thai text based on particles
        and sentence markers.

        Returns:
            FormalityResult with level, score (0-1), and matched markers.
        """
        if not text:
            return FormalityResult(level="neutral", score=0.5)

        formal_found = [p for p in FORMAL_PARTICLES if p in text]
        casual_found = [p for p in CASUAL_PARTICLES if p in text]

        formal_count = len(formal_found)
        casual_count = len(casual_found)
        total = formal_count + casual_count

        if total == 0:
            return FormalityResult(level="neutral", score=0.5)

        formality_score = formal_count / total

        if formality_score >= 0.6:
            level = "formal"
        elif formality_score <= 0.4:
            level = "casual"
        else:
            level = "neutral"

        return FormalityResult(
            level=level,
            score=round(formality_score, 4),
            markers_found=formal_found + casual_found,
        )

    # ------------------------------------------------------------------
    # Idiom Recognition
    # ------------------------------------------------------------------
    def detect_idioms(self, text: str) -> List[Dict[str, str]]:
        """
        Detect known Thai idioms (สำนวนไทย) in the text.

        Returns:
            List of dicts with 'idiom' and 'meaning' keys.
        """
        found = []
        for idiom, meaning in self.idioms.items():
            if idiom in text:
                found.append({"idiom": idiom, "meaning": meaning})
        return found
