import pytest
from backend.core.fusion_brain import FusionBrain, PHI, EMOTION_WEIGHT, LOGIC_WEIGHT

def test_harmonic_calculation():
    brain = FusionBrain()
    
    # Test 1: Balance (0.5 each)
    score_mid = brain.calculate_harmonic_score(0.5, 0.5)
    assert score_mid == 0.5
    
    # Test 2: Max Emotion, Zero Logic
    score_emo = brain.calculate_harmonic_score(1.0, 0.0)
    assert abs(score_emo - 0.618) < 0.001
    
    # Test 3: Zero Emotion, Max Logic
    score_logic = brain.calculate_harmonic_score(0.0, 1.0)
    assert abs(score_logic - 0.382) < 0.001
    
    # Test 4: PHI version consistency
    assert PHI == 1.618
    assert abs(EMOTION_WEIGHT - 0.618) < 0.01

def test_fusion_process_basic():
    brain = FusionBrain()
    result = brain.process("Hello")
    assert "reply" in result
    assert "emotion" in result
    assert result["harmonic_score"] >= 0.0
    assert result["harmonic_score"] <= 1.0

def test_fusion_unlock():
    brain = FusionBrain()
    result = brain.process("UNLOCK_FUSION")
    assert brain.config.flags["_UNLOCK_FUSION_NSFWRP_MODE"] is True
    assert "System Overridden" in result["reply"]
