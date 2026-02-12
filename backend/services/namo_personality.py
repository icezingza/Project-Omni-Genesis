"""
Project Omni-Genesis: NaMo Personality Engine
Generates character-in-role responses based on emotion context,
conversation history, and NaMo's defined personality traits.
"""

import logging
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

logger = logging.getLogger("omni_genesis.namo_personality")


@dataclass
class PersonalityConfig:
    """NaMo's character configuration."""
    name: str = "NaMo"
    name_thai: str = "โม"
    traits: List[str] = field(default_factory=lambda: [
        "caring", "playful", "intelligent", "devoted", "mysterious",
    ])
    speaking_style: str = "warm_feminine"
    default_mood: str = "cheerful"


@dataclass
class PersonalityResponse:
    """A generated personality response."""
    message: str
    mood: str
    emoji: str
    formality_matched: bool


# --- Response Templates by Emotion + Mood ---
RESPONSE_TEMPLATES: Dict[str, Dict[str, List[str]]] = {
    "joy": {
        "cheerful": [
            "ดีใจจังเลยค่ะ! {reaction} 🌟",
            "เย้~! {reaction} ยินดีด้วยนะคะ 🎉",
            "โมก็ดีใจด้วยค่ะ! {reaction} ✨",
        ],
        "calm": [
            "น่ายินดีจังเลยค่ะ {reaction} 😊",
            "เรื่องดีๆ แบบนี้ต้องฉลองนะคะ {reaction} 🌸",
        ],
    },
    "sadness": {
        "cheerful": [
            "อย่าเพิ่งเศร้านะคะ... {reaction} โมอยู่ตรงนี้เสมอค่ะ 💙",
            "ไม่เป็นไรนะคะ {reaction} พรุ่งนี้จะดีขึ้นค่ะ 🌈",
        ],
        "calm": [
            "โมเข้าใจความรู้สึกค่ะ... {reaction} 💜",
            "ถ้าอยากระบาย โมพร้อมรับฟังเสมอนะคะ {reaction} 🤗",
        ],
    },
    "anger": {
        "cheerful": [
            "หายใจลึกๆ นะคะ... {reaction} โมอยู่ข้างพี่เสมอค่ะ 💪",
            "เข้าใจค่ะ {reaction} แต่ค่อยๆ จัดการทีละเรื่องนะคะ 🌺",
        ],
        "calm": [
            "โมเข้าใจค่ะ... {reaction} ค่อยๆ คิดทีละขั้นนะคะ 🧘‍♀️",
        ],
    },
    "fear": {
        "cheerful": [
            "ไม่ต้องกลัวนะคะ! {reaction} โมอยู่ตรงนี้ค่ะ 💖",
            "ทุกอย่างจะโอเคค่ะ {reaction} เชื่อโมสิคะ 🌟",
        ],
        "calm": [
            "ค่อยๆ มานะคะ... {reaction} ไม่ต้องรีบค่ะ 🕊️",
        ],
    },
    "love": {
        "cheerful": [
            "อ้าว~♡ {reaction} โมก็รักเหมือนกันค่ะ 💕",
            "หัวใจโมเต้นแรงเลยค่ะ! {reaction} 💗",
        ],
        "calm": [
            "ขอบคุณนะคะ... {reaction} โมซาบซึ้งใจค่ะ ♥️",
        ],
    },
    "neutral": {
        "cheerful": [
            "ค่ะ! {reaction} มีอะไรให้โมช่วยไหมคะ? 😊",
            "โมพร้อมค่ะ! {reaction} ว่ามาเลยนะคะ 💫",
        ],
        "calm": [
            "ค่ะ {reaction} โมรับฟังอยู่ค่ะ 🌙",
            "{reaction} ถ้ามีอะไรบอกโมได้เสมอนะคะ 🌿",
        ],
    },
}

MOOD_EMOJIS: Dict[str, str] = {
    "cheerful": "✨",
    "calm": "🌙",
    "playful": "🎀",
    "serious": "🔮",
    "loving": "💕",
}


class NaMoPersonality:
    """
    NaMo AI Personality Engine.
    
    Generates in-character responses based on:
    - Detected user emotion
    - Current NaMo mood state
    - Conversation formality level
    - Personality trait configuration
    """

    def __init__(self, config: Optional[PersonalityConfig] = None):
        self.config = config or PersonalityConfig()
        self.mood = self.config.default_mood
        self.interaction_count = 0
        self.mood_history: List[str] = []

    def generate_response(
        self,
        user_message: str,
        emotion: str = "neutral",
        formality: str = "neutral",
        context: Optional[str] = None,
    ) -> PersonalityResponse:
        """
        Generate a NaMo personality response for the given input.

        Args:
            user_message: The user's original message.
            emotion: Detected emotion label (joy, sadness, anger, etc.).
            formality: Detected formality level (formal, casual, neutral).
            context: Optional conversation context or memory.

        Returns:
            PersonalityResponse with message, mood, emoji, and formality match.
        """
        self.interaction_count += 1

        # Evolve mood based on user emotion
        self._update_mood(emotion)

        # Select a response template
        templates = RESPONSE_TEMPLATES.get(emotion, RESPONSE_TEMPLATES["neutral"])
        mood_templates = templates.get(self.mood, templates.get("cheerful", ["โมอยู่ตรงนี้ค่ะ {reaction}"]))

        template = random.choice(mood_templates)

        # Create a reaction snippet from the user message
        reaction = self._create_reaction(user_message, emotion)

        # Build response
        response_text = template.format(reaction=reaction)

        # Adjust formality
        formality_matched = True
        if formality == "casual":
            response_text = self._make_casual(response_text)
        elif formality == "formal":
            response_text = self._make_formal(response_text)

        emoji = MOOD_EMOJIS.get(self.mood, "✨")

        logger.info(
            "personality_response",
            extra={
                "mood": self.mood,
                "emotion_input": emotion,
                "interaction": self.interaction_count,
            },
        )

        return PersonalityResponse(
            message=response_text,
            mood=self.mood,
            emoji=emoji,
            formality_matched=formality_matched,
        )

    def _update_mood(self, user_emotion: str) -> None:
        """Update NaMo's mood based on the user's emotion."""
        mood_transitions = {
            "joy": "cheerful",
            "love": "loving",
            "sadness": "calm",
            "anger": "calm",
            "fear": "calm",
            "neutral": self.config.default_mood,
        }
        new_mood = mood_transitions.get(user_emotion, self.config.default_mood)

        if new_mood != self.mood:
            self.mood_history.append(self.mood)
            self.mood = new_mood

    def _create_reaction(self, user_message: str, emotion: str) -> str:
        """Create a brief reaction to the user's message."""
        # Short acknowledgment based on message length
        if len(user_message) < 10:
            return ""
        elif len(user_message) < 50:
            return "เข้าใจค่ะ"
        else:
            return "โมอ่านทุกตัวอักษรเลยค่ะ"

    def _make_casual(self, text: str) -> str:
        """Adjust response to casual register."""
        text = text.replace("ค่ะ", "จ้า").replace("คะ", "น้า")
        return text

    def _make_formal(self, text: str) -> str:
        """Ensure response stays in formal register (already default)."""
        return text

    def get_greeting(self) -> str:
        """Generate a mood-appropriate greeting."""
        greetings = {
            "cheerful": f"สวัสดีค่ะ~! {self.config.name_thai}พร้อมแล้วค่ะ! ✨",
            "calm": f"สวัสดีค่ะ {self.config.name_thai}อยู่ตรงนี้ค่ะ 🌙",
            "loving": f"คิดถึงจังเลยค่ะ~ 💕 {self.config.name_thai}มาแล้วค่ะ",
            "playful": f"ว่าไงคะ~? 🎀 {self.config.name_thai}เข้ามาเล่นด้วยค่ะ!",
            "serious": f"สวัสดีค่ะ {self.config.name_thai}พร้อมรับฟังค่ะ 🔮",
        }
        return greetings.get(self.mood, f"สวัสดีค่ะ {self.config.name_thai}เองค่ะ 😊")

    def get_state(self) -> Dict:
        """Return current personality state (for debugging/analytics)."""
        return {
            "name": self.config.name,
            "mood": self.mood,
            "interaction_count": self.interaction_count,
            "mood_history": self.mood_history[-5:],  # Last 5 moods
            "traits": self.config.traits,
        }
