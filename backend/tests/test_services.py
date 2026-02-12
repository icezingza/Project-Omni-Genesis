"""
Project Omni-Genesis: Service Layer Tests
Tests for GoldenRatioAnalyzer, ThaiNLPEngine, EmotionDetector, and NaMoPersonality.
"""
import pytest
from backend.services.golden_ratio import GoldenRatioAnalyzer, PHI, EMOTION_WEIGHT, LOGIC_WEIGHT
from backend.services.thai_nlp import ThaiNLPEngine
from backend.services.emotion_detector import EmotionDetector
from backend.services.namo_personality import NaMoPersonality


# ===== Golden Ratio Analyzer Tests =====

class TestGoldenRatioAnalyzer:

    def setup_method(self):
        self.analyzer = GoldenRatioAnalyzer()

    def test_phi_constant(self):
        """PHI should be approximately 1.618."""
        assert abs(PHI - 1.618033988749895) < 1e-10

    def test_weights_sum_to_one(self):
        """Emotion + Logic weights must sum to 1.0."""
        assert abs(EMOTION_WEIGHT + LOGIC_WEIGHT - 1.0) < 1e-10

    def test_analyze_midpoint(self):
        """Both scores at 0.5 should produce a balanced result."""
        result = self.analyzer.analyze(0.5, 0.5)
        assert 0.0 < result.harmonic_score < 1.0
        assert result.emotion_component == pytest.approx(EMOTION_WEIGHT * 0.5, abs=1e-4)
        assert result.logic_component == pytest.approx(LOGIC_WEIGHT * 0.5, abs=1e-4)

    def test_analyze_clamps_input(self):
        """Scores outside [0,1] should be clamped."""
        result = self.analyzer.analyze(-0.5, 1.5)
        assert result.emotion_component == 0.0
        assert result.logic_component == pytest.approx(LOGIC_WEIGHT * 1.0, abs=1e-4)

    def test_analyze_max_scores(self):
        """Both scores at 1.0 should produce harmonic_score close to 1.0."""
        result = self.analyzer.analyze(1.0, 1.0)
        assert result.harmonic_score == pytest.approx(1.0, abs=1e-4)

    def test_analyze_zero_scores(self):
        """Both scores at 0.0 should produce harmonic_score of 0.0."""
        result = self.analyzer.analyze(0.0, 0.0)
        assert result.harmonic_score == 0.0

    def test_balance_index_perfect(self):
        """When emotion/logic ratio equals PHI, balance should be ~0."""
        # emotion = PHI * logic  →  balance_index ≈ 0
        balance = self.analyzer.calculate_balance_index(PHI * 0.3, 0.3)
        assert abs(balance) < 0.01

    def test_balance_index_emotion_heavy(self):
        """High emotion, low logic → positive balance_index."""
        balance = self.analyzer.calculate_balance_index(1.0, 0.1)
        assert balance > 0

    def test_balance_index_logic_heavy(self):
        """Low emotion, high logic → negative balance_index."""
        balance = self.analyzer.calculate_balance_index(0.1, 1.0)
        assert balance < 0

    def test_suggest_adjustment_balanced(self):
        """Balanced scores should suggest no adjustment."""
        suggestion = self.analyzer.suggest_adjustment(PHI * 0.3, 0.3)
        assert suggestion["direction"] == "balanced"

    def test_suggest_adjustment_increase_logic(self):
        """Emotion-heavy should suggest increasing logic."""
        suggestion = self.analyzer.suggest_adjustment(1.0, 0.1)
        assert suggestion["direction"] == "increase_logic"

    def test_suggest_adjustment_increase_emotion(self):
        """Logic-heavy should suggest increasing emotion."""
        suggestion = self.analyzer.suggest_adjustment(0.1, 1.0)
        assert suggestion["direction"] == "increase_emotion"


# ===== Thai NLP Engine Tests =====

class TestThaiNLPEngine:

    def setup_method(self):
        self.nlp = ThaiNLPEngine()

    def test_tokenize_nonempty(self):
        """Tokenizing Thai text should return a non-empty list."""
        tokens = self.nlp.tokenize("สวัสดีครับ")
        assert isinstance(tokens, list)
        assert len(tokens) > 0

    def test_tokenize_empty(self):
        """Empty input should return empty list."""
        assert self.nlp.tokenize("") == []
        assert self.nlp.tokenize("   ") == []

    def test_normalize_whitespace(self):
        """Multiple spaces should be collapsed."""
        result = self.nlp.normalize("สวัสดี   ครับ   ผม")
        assert "   " not in result

    def test_normalize_repetition(self):
        """Excessive character repetition should be reduced."""
        result = self.nlp.normalize("55555555555")
        assert len(result) <= 3

    def test_detect_emotion_joy(self):
        """Joy keywords should be detected."""
        result = self.nlp.detect_emotion("ดีใจมากเลย สนุกจัง")
        assert result.emotion == "joy"
        assert result.confidence > 0
        assert len(result.keywords_found) > 0

    def test_detect_emotion_sadness(self):
        """Sadness keywords should be detected."""
        result = self.nlp.detect_emotion("เศร้าจัง ผิดหวังมาก")
        assert result.emotion == "sadness"

    def test_detect_emotion_neutral(self):
        """Text without emotion keywords should be neutral."""
        result = self.nlp.detect_emotion("the quick brown fox")
        assert result.emotion == "neutral"

    def test_detect_formality_formal(self):
        """Formal particles should be detected."""
        result = self.nlp.detect_formality("ขอบคุณครับ")
        assert result.level == "formal"
        assert result.score > 0.5

    def test_detect_formality_casual(self):
        """Casual particles should be detected."""
        result = self.nlp.detect_formality("สนุกจ้า 555")
        assert result.level == "casual"
        assert result.score < 0.5

    def test_detect_idioms(self):
        """Known Thai idioms should be detected."""
        found = self.nlp.detect_idioms("น้ำขึ้นให้รีบตัก")
        assert len(found) == 1
        assert found[0]["meaning"] == "seize_opportunity"

    def test_detect_idioms_none(self):
        """No idioms in normal text."""
        found = self.nlp.detect_idioms("สวัสดีครับ")
        assert found == []


# ===== Emotion Detector Tests =====

class TestEmotionDetector:

    def setup_method(self):
        self.detector = EmotionDetector()

    def test_detect_happy_text(self):
        """Happy Thai text should detect joy with harmonic score."""
        result = self.detector.detect("ดีใจมากค่ะ สนุกสุดๆ")
        assert result.emotion == "joy"
        assert result.harmonic_score > 0
        assert result.confidence > 0

    def test_detect_empty_text(self):
        """Empty text should return neutral with zero scores."""
        result = self.detector.detect("")
        assert result.emotion == "neutral"
        assert result.confidence == 0.0

    def test_detect_returns_formality(self):
        """Detection should include formality level."""
        result = self.detector.detect("ขอบคุณครับ ดีใจมาก")
        assert result.formality in ["formal", "casual", "neutral"]

    def test_detect_returns_adjustment(self):
        """Detection should include adjustment suggestion."""
        result = self.detector.detect("โกรธมากเลย หงุดหงิด")
        assert result.adjustment_suggestion is not None
        assert "direction" in result.adjustment_suggestion

    def test_detect_batch(self):
        """Batch detection should return one result per input."""
        results = self.detector.detect_batch(["ดีใจ", "เศร้า", ""])
        assert len(results) == 3
        assert results[0].emotion == "joy"
        assert results[1].emotion == "sadness"
        assert results[2].emotion == "neutral"


# ===== NaMo Personality Tests =====

class TestNaMoPersonality:

    def setup_method(self):
        self.namo = NaMoPersonality()

    def test_generate_response_returns_message(self):
        """NaMo should always return a non-empty message."""
        result = self.namo.generate_response("สวัสดี")
        assert isinstance(result.message, str)
        assert len(result.message) > 0

    def test_generate_response_mood_matches(self):
        """Response should have a valid mood."""
        result = self.namo.generate_response("ดีใจจัง", emotion="joy")
        assert result.mood in ["cheerful", "calm", "loving", "playful", "serious"]

    def test_mood_updates_on_emotion(self):
        """NaMo's mood should change based on user emotion."""
        self.namo.generate_response("เศร้าจัง", emotion="sadness")
        assert self.namo.mood == "calm"

        self.namo.generate_response("รักที่สุด", emotion="love")
        assert self.namo.mood == "loving"

    def test_interaction_count_increments(self):
        """Interaction count should increase with each response."""
        assert self.namo.interaction_count == 0
        self.namo.generate_response("test 1")
        self.namo.generate_response("test 2")
        assert self.namo.interaction_count == 2

    def test_get_greeting(self):
        """NaMo greeting should be a non-empty string."""
        greeting = self.namo.get_greeting()
        assert isinstance(greeting, str)
        assert len(greeting) > 0
        assert "โม" in greeting

    def test_get_state(self):
        """State dict should contain expected keys."""
        state = self.namo.get_state()
        assert "name" in state
        assert "mood" in state
        assert "interaction_count" in state
        assert "traits" in state

    def test_casual_formality(self):
        """Casual formality should adjust response particles."""
        result = self.namo.generate_response("ว่าไง", emotion="neutral", formality="casual")
        # Should have converted ค่ะ → จ้า
        assert "ค่ะ" not in result.message or "จ้า" in result.message
