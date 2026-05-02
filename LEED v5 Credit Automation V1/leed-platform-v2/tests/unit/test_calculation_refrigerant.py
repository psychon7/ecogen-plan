"""Unit tests for refrigerant impact calculations (EAc7/EAp5)."""

from backend.services.calculation_service import (
    RefrigerantSystem,
    RefrigerantCalcResult,
    calculate_refrigerant_impact,
)


def test_low_gwp_system_meets_threshold():
    """R-32 system should meet the LCGWP ≤ 100/kW threshold."""
    systems = [
        RefrigerantSystem(
            system_name="RTU-1",
            refrigerant_type="R-32",
            charge_kg=10.0,
            cooling_capacity_kw=50.0,
            equipment_life_years=20,
        ),
    ]

    result = calculate_refrigerant_impact(systems)

    assert isinstance(result, RefrigerantCalcResult)
    assert result.meets_gwp_threshold is True
    assert result.meets_odp_threshold is True
    assert result.total_lcgwp > 0
    assert len(result.system_details) == 1


def test_high_gwp_system_fails_threshold():
    """R-410A system with large charge should fail the threshold."""
    systems = [
        RefrigerantSystem(
            system_name="Chiller-1",
            refrigerant_type="R-410A",
            charge_kg=100.0,
            cooling_capacity_kw=50.0,
            equipment_life_years=20,
        ),
    ]

    result = calculate_refrigerant_impact(systems)

    assert result.meets_gwp_threshold is False
    assert result.weighted_lcgwp > 100


def test_natural_refrigerant_zero_impact():
    """R-717 (ammonia) should have zero GWP impact."""
    systems = [
        RefrigerantSystem(
            system_name="NH3-Chiller",
            refrigerant_type="R-717",
            charge_kg=50.0,
            cooling_capacity_kw=200.0,
        ),
    ]

    result = calculate_refrigerant_impact(systems)

    assert result.total_lcgwp == 0
    assert result.meets_gwp_threshold is True


def test_empty_systems():
    """No systems should return zero result."""
    result = calculate_refrigerant_impact([])

    assert result.total_lcgwp == 0
    assert result.weighted_lcgwp == 0


def test_multiple_systems_weighted():
    """Weighted LCGWP should reflect total capacity."""
    systems = [
        RefrigerantSystem(
            system_name="A", refrigerant_type="R-32",
            charge_kg=10, cooling_capacity_kw=100,
        ),
        RefrigerantSystem(
            system_name="B", refrigerant_type="R-410A",
            charge_kg=10, cooling_capacity_kw=100,
        ),
    ]

    result = calculate_refrigerant_impact(systems)

    assert len(result.system_details) == 2
    assert result.weighted_lcgwp == round(result.total_lcgwp / 200, 2)
