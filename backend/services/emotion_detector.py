"""
Project Omni-Genesis: Emotion Detector
Combines Thai NLP keyword analysis with Golden Ratio weighting
to produce a comprehensive emotion analysis result.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .golden_ratio import GoldenRatioAnalyzer, GoldenRatioResult
from .thai_nlp import ThaiNLPEngine, EmotionResult

logger = logging.getLogger("omni_genesis.emotion_detector")


# Emotion → base logic/emotion score mapping
# These represent the "typical" intensities for each detected emotion
EMOTION_PROFILES: Dict[str, Dict[str, float]] = {
    "joy":     {"emotion_intensity": 0.85, "logic_clarity": 0.65},
    "sadness": {"emotion_intensity": 0.80, "logic_clarity": 0.40},
    "anger":   {"emotion_intensity": 0.90, "logic_clarity": 0.30},
    "fear":    {"emotion_intensity": 0.75, "logic_clarity": 0.45},
    "love":    {"emotion_intensity": 0.95, "logic_clarity": 0.55},
    "neutral": {"emotion_intensity": 0.40, "logic_clarity": 0.70},
}


@dataclass
class DetectionResult:
    """Full emotion detection result combining NLP and Golden Ratio."""
    emotion: str
    confidence: float
    harmonic_score: float
    balance_index: float
    is_balanced: bool
    keywords_found: List[str] = field(default_factory=list)
    formality: str = "neutral"
    adjustment_suggestion: Optional[Dict] = None


class EmotionDetector:
    """
    End-to-end emotion detector that:
    1. Uses ThaiNLPEngine for keyword-based emotion detection
    2. Maps emotion → intensity profiles
    3. Applies GoldenRatioAnalyzer for PHI-weighted scoring
    """

    def __init__(
        self,
        nlp_engine: Optional[ThaiNLPEngine] = None,
        ratio_analyzer: Optional[GoldenRatioAnalyzer] = None,
    ):
        self.nlp = nlp_engine or ThaiNLPEngine()
        self.ratio = ratio_analyzer or GoldenRatioAnalyzer()

    def detect(self, text: str) -> DetectionResult:
        """
        Run full emotion detection pipeline on input text.

        Args:
            text: User message (Thai or English).

        Returns:
            DetectionResult with emotion, confidence, harmonic analysis.
        """
        if not text or not text.strip():
            return DetectionResult(
                emotion="neutral",
                confidence=0.0,
                harmonic_score=0.0,
                balance_index=0.0,
                is_balanced=True,
            )

        # Step 1: Thai NLP emotion detection
        nlp_result: EmotionResult = self.nlp.detect_emotion(text)

        # Step 2: Get emotion profile for Golden Ratio analysis
        profile = EMOTION_PROFILES.get(
            nlp_result.emotion,
            EMOTION_PROFILES["neutral"],
        )

        # Scale intensities by confidence
        emotion_score = profile["emotion_intensity"] * nlp_result.confidence
        logic_score = profile["logic_clarity"] * nlp_result.confidence

        # Ensure minimum scores for meaningful analysis
        emotion_score = max(emotion_score, 0.1)
        logic_score = max(logic_score, 0.1)

        # Step 3: Golden Ratio analysis
        ratio_result: GoldenRatioResult = self.ratio.analyze(
            emotion_score=emotion_score,
            logic_score=logic_score,
        )

        # Step 4: Get adjustment suggestion
        suggestion = self.ratio.suggest_adjustment(emotion_score, logic_score)

        # Step 5: Formality analysis
        formality = self.nlp.detect_formality(text)

        logger.info(
            "emotion_detected",
            extra={
                "emotion": nlp_result.emotion,
                "confidence": nlp_result.confidence,
                "harmonic_score": ratio_result.harmonic_score,
            },
        )

        return DetectionResult(
            emotion=nlp_result.emotion,
            confidence=nlp_result.confidence,
            harmonic_score=ratio_result.harmonic_score,
            balance_index=ratio_result.balance_index,
            is_balanced=ratio_result.is_balanced,
            keywords_found=nlp_result.keywords_found,
            formality=formality.level,
            adjustment_suggestion=suggestion,
        )

    def detect_batch(self, texts: List[str]) -> List[DetectionResult]:
        """
        Run emotion detection on multiple texts.

        Args:
            texts: List of user messages.

        Returns:
            List of DetectionResult objects.
        """
        return [self.detect(t) for t in texts]
