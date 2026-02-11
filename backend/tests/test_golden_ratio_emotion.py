from backend.services.golden_ratio_emotion import GoldenRatioEmotionAnalyzer


def test_analyze_returns_weighted_scores():
    analyzer = GoldenRatioEmotionAnalyzer()
    result = analyzer.analyze("ฉันเศร้ามาก เพราะวันนี้งานพัง!", {"has_history": True})

    assert set(result.keys()) == {"emotion", "logic", "combined", "confidence", "strategy"}
    assert 0.0 <= result["combined"] <= 1.0
    assert result["strategy"] in {"emotion_driven", "logic_driven", "balanced"}


def test_analyze_empty_text_is_safe():
    analyzer = GoldenRatioEmotionAnalyzer()
    result = analyzer.analyze("", None)

    assert result["emotion"] == 0.0
    assert result["logic"] == 0.0
    assert result["combined"] == 0.0
    assert result["confidence"] == 0.0
