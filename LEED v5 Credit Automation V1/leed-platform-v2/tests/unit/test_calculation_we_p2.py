"""Unit tests for the WEp2 water calculation service."""

from backend.services.calculation_service import (
    Fixture,
    WaterCalcResult,
    calculate_we_p2,
)


def test_we_p2_basic_office_meets_threshold():
    """Office with low-flow fixtures should meet the 20% threshold."""
    fixtures = [
        Fixture(fixture_type="toilet", quantity=10, design_flow_rate=1.1),
        Fixture(fixture_type="urinal", quantity=4, design_flow_rate=0.5),
        Fixture(fixture_type="lavatory_faucet", quantity=10, design_flow_rate=0.5),
        Fixture(fixture_type="kitchen_faucet", quantity=2, design_flow_rate=1.5),
        Fixture(fixture_type="showerhead", quantity=2, design_flow_rate=1.5),
    ]

    result = calculate_we_p2(
        fixtures=fixtures,
        fte_occupants=100,
        gender_ratio=0.5,
        building_type="office",
    )

    assert isinstance(result, WaterCalcResult)
    assert result.baseline_annual_gallons > 0
    assert result.design_annual_gallons > 0
    assert result.design_annual_gallons < result.baseline_annual_gallons
    assert result.reduction_pct > 0
    assert result.meets_threshold is True
    assert result.gap_analysis is None


def test_we_p2_no_reduction_fails_threshold():
    """Fixtures at baseline rates should not meet the 20% threshold."""
    fixtures = [
        Fixture(fixture_type="toilet", quantity=10, design_flow_rate=1.6),
        Fixture(fixture_type="lavatory_faucet", quantity=10, design_flow_rate=2.2),
    ]

    result = calculate_we_p2(
        fixtures=fixtures,
        fte_occupants=50,
        gender_ratio=0.5,
    )

    assert result.reduction_pct == 0.0
    assert result.meets_threshold is False
    assert result.gap_analysis is not None
    assert result.gap_analysis["additional_savings_needed_gal"] > 0


def test_we_p2_zero_occupants():
    """Zero occupants should return zero values."""
    fixtures = [Fixture(fixture_type="toilet", quantity=5, design_flow_rate=1.0)]

    result = calculate_we_p2(fixtures=fixtures, fte_occupants=0)

    assert result.baseline_daily_gallons == 0
    assert result.design_daily_gallons == 0


def test_we_p2_fixture_breakdown_populated():
    """Breakdown should have one entry per fixture."""
    fixtures = [
        Fixture(fixture_type="toilet", quantity=5, design_flow_rate=1.0),
        Fixture(fixture_type="lavatory_faucet", quantity=5, design_flow_rate=0.5),
    ]

    result = calculate_we_p2(fixtures=fixtures, fte_occupants=20)

    assert len(result.fixture_breakdown) == 2
    assert result.fixture_breakdown[0]["fixture_type"] == "toilet"
    assert result.fixture_breakdown[1]["fixture_type"] == "lavatory_faucet"


def test_we_p2_gender_ratio_affects_urinals():
    """Higher male ratio should increase urinal baseline use."""
    fixtures = [
        Fixture(fixture_type="urinal", quantity=4, design_flow_rate=0.5),
    ]

    result_high_male = calculate_we_p2(
        fixtures=fixtures, fte_occupants=100, gender_ratio=0.8,
    )
    result_low_male = calculate_we_p2(
        fixtures=fixtures, fte_occupants=100, gender_ratio=0.2,
    )

    assert result_high_male.baseline_daily_gallons > result_low_male.baseline_daily_gallons
