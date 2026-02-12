"""
Project Omni-Genesis: Golden Ratio Analyzer
Applies the Golden Ratio (φ ≈ 1.618) to balance emotion and logic scores,
producing a harmonic weighting used throughout the AI pipeline.
"""

import math
from dataclasses import dataclass
from typing import Optional


# The Golden Ratio constant
PHI: float = 1.618033988749895

# Derived weights: emotion = 1/φ ≈ 0.618, logic = 1 - 1/φ ≈ 0.382
EMOTION_WEIGHT: float = 1.0 / PHI
LOGIC_WEIGHT: float = 1.0 - EMOTION_WEIGHT


@dataclass
class GoldenRatioResult:
    """Result of a Golden Ratio analysis."""
    harmonic_score: float
    emotion_component: float
    logic_component: float
    balance_index: float
    is_balanced: bool


class GoldenRatioAnalyzer:
    """
    Analyzes and balances emotion vs logic scores using the Golden Ratio.
    
    Core Formula:
        harmonic_score = (EMOTION_WEIGHT × emotion) + (LOGIC_WEIGHT × logic)
        
    Where:
        EMOTION_WEIGHT = 1/φ ≈ 0.618
        LOGIC_WEIGHT   = 1 - 1/φ ≈ 0.382
    """

    def __init__(
        self,
        phi: float = PHI,
        balance_threshold: float = 0.15,
    ):
        """
        Args:
            phi: The Golden Ratio constant (default: φ ≈ 1.618).
            balance_threshold: How close to perfect balance (0.0) the 
                balance_index must be to count as "balanced".
        """
        self.phi = phi
        self.emotion_weight = 1.0 / phi
        self.logic_weight = 1.0 - self.emotion_weight
        self.balance_threshold = balance_threshold

    def analyze(
        self,
        emotion_score: float,
        logic_score: float,
    ) -> GoldenRatioResult:
        """
        Compute the PHI-weighted harmonic score for a pair of scores.

        Args:
            emotion_score: Emotion/voice intensity in [0, 1].
            logic_score: Logic/text coherence in [0, 1].

        Returns:
            GoldenRatioResult with harmonic_score, components, and balance info.
        """
        emotion_score = max(0.0, min(1.0, emotion_score))
        logic_score = max(0.0, min(1.0, logic_score))

        emotion_component = self.emotion_weight * emotion_score
        logic_component = self.logic_weight * logic_score
        harmonic_score = emotion_component + logic_component

        balance_index = self.calculate_balance_index(emotion_score, logic_score)
        is_balanced = abs(balance_index) <= self.balance_threshold

        return GoldenRatioResult(
            harmonic_score=round(harmonic_score, 6),
            emotion_component=round(emotion_component, 6),
            logic_component=round(logic_component, 6),
            balance_index=round(balance_index, 6),
            is_balanced=is_balanced,
        )

    def calculate_balance_index(
        self,
        emotion_score: float,
        logic_score: float,
    ) -> float:
        """
        Measure how far the emotion/logic ratio is from the ideal φ ratio.

        A balance_index of 0.0 means perfect Golden Ratio balance.
        Positive = emotion-heavy, Negative = logic-heavy.

        Args:
            emotion_score: Emotion intensity in [0, 1].
            logic_score: Logic coherence in [0, 1].

        Returns:
            Float in roughly [-1, 1] indicating directional imbalance.
        """
        if logic_score == 0:
            return 1.0 if emotion_score > 0 else 0.0

        actual_ratio = emotion_score / logic_score
        ideal_ratio = self.phi
        return (actual_ratio - ideal_ratio) / ideal_ratio

    def suggest_adjustment(
        self,
        emotion_score: float,
        logic_score: float,
    ) -> dict:
        """
        Suggest how to adjust scores toward Golden Ratio balance.

        Returns:
            Dict with 'direction' ('increase_logic' | 'increase_emotion' | 'balanced')
            and 'magnitude' (how much adjustment is needed, 0-1 scale).
        """
        balance = self.calculate_balance_index(emotion_score, logic_score)

        if abs(balance) <= self.balance_threshold:
            return {"direction": "balanced", "magnitude": 0.0}
        elif balance > 0:
            return {
                "direction": "increase_logic",
                "magnitude": round(min(abs(balance), 1.0), 4),
            }
        else:
            return {
                "direction": "increase_emotion",
                "magnitude": round(min(abs(balance), 1.0), 4),
            }
