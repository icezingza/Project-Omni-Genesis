"""Dark core engines for arousal detection, dialogue, and emotion analysis."""

from .arousal_detector import ArousalDetector
from .dark_dialogue_engine import DarkDialogueEngine
from .emotion_parasite_engine import EmotionParasiteEngine

__all__ = ["ArousalDetector", "DarkDialogueEngine", "EmotionParasiteEngine"]
