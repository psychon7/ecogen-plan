"""Unit tests for confidence scoring."""

from backend.services.calculation_service import compute_confidence_tier


def test_tier_a_high_confidence():
    """All components ≥ 0.85 should yield Tier A."""
    scores = {"extraction": 0.92, "certification": 0.88, "calculation": 0.95}
    result = compute_confidence_tier(scores)

    assert result["tier"] == "A"
    assert result["floor_triggered"] is False
    assert result["overall"] >= 0.85


def test_tier_c_floor_triggered():
    """Any component < 0.70 should force Tier C."""
    scores = {"extraction": 0.95, "certification": 0.65, "calculation": 0.90}
    result = compute_confidence_tier(scores)

    assert result["tier"] == "C"
    assert result["floor_triggered"] is True


def test_tier_b_medium():
    """All above floor but below A threshold."""
    scores = {"extraction": 0.78, "certification": 0.75, "calculation": 0.80}
    result = compute_confidence_tier(scores)

    assert result["tier"] == "B"
    assert result["floor_triggered"] is False


def test_empty_scores():
    """Empty scores should return Tier C."""
    result = compute_confidence_tier({})

    assert result["tier"] == "C"
    assert result["floor_triggered"] is True
