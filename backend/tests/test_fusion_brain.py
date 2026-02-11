"""
Project Omni-Genesis: Fusion Brain Logic Tests
Tests the Golden Ratio calculations and Fusion Mode triggers.
"""
import pytest
from backend.core.fusion_brain import FusionBrain

@pytest.fixture
def brain():
    return FusionBrain()

def test_harmonic_score_calculation(brain):
    """
    Test Golden Ratio weighting formula:
    Harmonic Score = (0.618 * Emotion) + (0.382 * Logic)
    """
    # Case 1: Pure Emotion (1.0, 0.0) -> Should be ~0.618
    score = brain.calculate_harmonic_score(1.0, 0.0)
    assert abs(score - 0.618) < 0.001

    # Case 2: Pure Logic (0.0, 1.0) -> Should be ~0.382
    score = brain.calculate_harmonic_score(0.0, 1.0)
    assert abs(score - 0.382) < 0.001
    
    # Case 3: Balanced (0.5, 0.5) -> Should be 0.5
    score = brain.calculate_harmonic_score(0.5, 0.5)
    assert abs(score - 0.5) < 0.001

def test_process_fusion_unlock(brain):
    """Test the secret unlock trigger mechanism."""
    result = brain.process("UNLOCK_FUSION", "test_user")
    
    assert result["harmonic_score"] == 1.0
    assert "Fusion Mode Activated" in result["reply"]
    assert brain.config.flags["_UNLOCK_FUSION_NSFWRP_MODE"] is True

def test_process_normal_flow(brain):
    """Test normal processing flow without triggers."""
    result = brain.process("Hello NaMo", "test_user")
    
    assert "reply" in result
    assert "emotion" in result
    assert "harmonic_score" in result
    assert result["user_id"] == "test_user"