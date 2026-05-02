"""CalculationService — deterministic LEED formulas.

Pure Python functions, no LLM dependency.  Each credit's formulas
are isolated and unit-testable.  Called by Restate's CreditWorkflow.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# WEp2 — Minimum Water Efficiency (fixture-based)
# ---------------------------------------------------------------------------

# LEED v5 baseline flow rates (gallons per flush / gallons per minute)
WE_BASELINE_RATES: dict[str, float] = {
    "toilet": 1.6,             # gpf
    "urinal": 1.0,             # gpf
    "lavatory_faucet": 2.2,    # gpm
    "kitchen_faucet": 2.2,     # gpm
    "showerhead": 2.5,         # gpm
}

# Default daily uses per occupant (office building type)
WE_DEFAULT_USES_OFFICE: dict[str, float] = {
    "toilet": 3.0,
    "urinal": 3.0,
    "lavatory_faucet": 3.0,
    "kitchen_faucet": 1.0,
    "showerhead": 0.1,
}

# Duration assumptions (minutes per use, for gpm fixtures)
WE_DURATION_MINUTES: dict[str, float] = {
    "lavatory_faucet": 0.25,
    "kitchen_faucet": 0.25,
    "showerhead": 5.0,
}


@dataclass
class Fixture:
    """A single fixture in the schedule."""
    fixture_type: str
    quantity: int
    design_flow_rate: float     # gpf or gpm depending on type
    manufacturer: str | None = None
    model: str | None = None


@dataclass
class WaterCalcResult:
    """Result of WEp2 baseline vs design water calculation."""
    baseline_daily_gallons: float = 0.0
    design_daily_gallons: float = 0.0
    baseline_annual_gallons: float = 0.0
    design_annual_gallons: float = 0.0
    reduction_pct: float = 0.0
    meets_threshold: bool = False
    threshold_pct: float = 20.0
    fixture_breakdown: list[dict[str, Any]] = field(default_factory=list)
    gap_analysis: dict[str, Any] | None = None


def calculate_we_p2(
    fixtures: list[Fixture],
    fte_occupants: int,
    transient_occupants: int = 0,
    gender_ratio: float = 0.5,
    building_type: str = "office",
    uses_override: dict[str, float] | None = None,
) -> WaterCalcResult:
    """Compute WEp2 baseline vs design water use.

    Returns structured result with per-fixture breakdown.
    """
    uses = dict(WE_DEFAULT_USES_OFFICE)
    if uses_override:
        uses.update(uses_override)

    total_occupants = fte_occupants + transient_occupants
    if total_occupants <= 0:
        return WaterCalcResult()

    male_count = total_occupants * gender_ratio
    female_count = total_occupants * (1 - gender_ratio)

    baseline_daily = 0.0
    design_daily = 0.0
    breakdown = []

    for f in fixtures:
        ft = f.fixture_type.lower()
        baseline_rate = WE_BASELINE_RATES.get(ft, 0.0)
        daily_uses = uses.get(ft, 0.0)

        # gpf fixtures (toilet, urinal) — gallons = qty × rate × uses × occupants
        if ft in ("toilet", "urinal"):
            if ft == "urinal":
                effective_occ = male_count
            else:
                effective_occ = total_occupants
            b = f.quantity * baseline_rate * daily_uses * effective_occ / f.quantity if f.quantity else 0
            d = f.quantity * f.design_flow_rate * daily_uses * effective_occ / f.quantity if f.quantity else 0
            # Simplified: total for all fixtures of this type
            b = baseline_rate * daily_uses * effective_occ
            d = f.design_flow_rate * daily_uses * effective_occ
        else:
            # gpm fixtures — gallons = rate × duration × uses × occupants
            duration = WE_DURATION_MINUTES.get(ft, 0.25)
            b = baseline_rate * duration * daily_uses * total_occupants
            d = f.design_flow_rate * duration * daily_uses * total_occupants

        baseline_daily += b
        design_daily += d

        breakdown.append({
            "fixture_type": ft,
            "quantity": f.quantity,
            "baseline_rate": baseline_rate,
            "design_rate": f.design_flow_rate,
            "baseline_daily_gal": round(b, 2),
            "design_daily_gal": round(d, 2),
        })

    baseline_annual = baseline_daily * 365
    design_annual = design_daily * 365
    reduction = ((baseline_annual - design_annual) / baseline_annual * 100) if baseline_annual > 0 else 0.0

    result = WaterCalcResult(
        baseline_daily_gallons=round(baseline_daily, 2),
        design_daily_gallons=round(design_daily, 2),
        baseline_annual_gallons=round(baseline_annual, 2),
        design_annual_gallons=round(design_annual, 2),
        reduction_pct=round(reduction, 1),
        meets_threshold=reduction >= 20.0,
        fixture_breakdown=breakdown,
    )

    if not result.meets_threshold:
        result.gap_analysis = {
            "required_reduction_pct": 20.0,
            "current_reduction_pct": result.reduction_pct,
            "additional_savings_needed_gal": round(
                baseline_annual * 0.2 - (baseline_annual - design_annual), 2
            ),
        }

    return result


# ---------------------------------------------------------------------------
# EAc7 / EAp5 — Refrigerant Management (GWP / LCGWP)
# ---------------------------------------------------------------------------

@dataclass
class RefrigerantSystem:
    """A single HVAC system with refrigerant data."""
    system_name: str
    refrigerant_type: str
    charge_kg: float
    cooling_capacity_kw: float
    equipment_life_years: int = 20
    end_of_life_loss_pct: float = 10.0
    annual_leak_rate_pct: float = 2.0


# Common refrigerant GWP values (AR5)
REFRIGERANT_GWP: dict[str, int] = {
    "R-410A": 2088,
    "R-134a": 1430,
    "R-407C": 1774,
    "R-32": 675,
    "R-1234yf": 4,
    "R-1234ze": 7,
    "R-290": 3,
    "R-744": 1,    # CO2
    "R-717": 0,    # Ammonia
}

# Common refrigerant ODP values
REFRIGERANT_ODP: dict[str, float] = {
    "R-410A": 0.0,
    "R-134a": 0.0,
    "R-407C": 0.0,
    "R-32": 0.0,
    "R-1234yf": 0.0,
    "R-1234ze": 0.0,
    "R-290": 0.0,
    "R-744": 0.0,
    "R-717": 0.0,
}


@dataclass
class RefrigerantCalcResult:
    """Result of refrigerant impact calculation."""
    total_lcgwp: float = 0.0
    weighted_lcgwp: float = 0.0
    total_lcodp: float = 0.0
    meets_gwp_threshold: bool = False
    meets_odp_threshold: bool = True
    system_details: list[dict[str, Any]] = field(default_factory=list)


def calculate_refrigerant_impact(systems: list[RefrigerantSystem]) -> RefrigerantCalcResult:
    """Calculate lifecycle GWP and ODP for all refrigerant systems.

    LCGWP = GWP × (Lr × Life + Mr) × Rc / Life
    where Lr = annual leak rate, Mr = end-of-life loss, Rc = charge.
    """
    total_capacity = sum(s.cooling_capacity_kw for s in systems)
    if total_capacity <= 0:
        return RefrigerantCalcResult()

    total_lcgwp = 0.0
    total_lcodp = 0.0
    details = []

    for s in systems:
        gwp = REFRIGERANT_GWP.get(s.refrigerant_type, 0)
        odp = REFRIGERANT_ODP.get(s.refrigerant_type, 0.0)

        lr = s.annual_leak_rate_pct / 100
        mr = s.end_of_life_loss_pct / 100
        life = s.equipment_life_years

        lcgwp = gwp * (lr * life + mr) * s.charge_kg / life
        lcodp = odp * (lr * life + mr) * s.charge_kg / life

        total_lcgwp += lcgwp
        total_lcodp += lcodp

        details.append({
            "system_name": s.system_name,
            "refrigerant": s.refrigerant_type,
            "gwp": gwp,
            "charge_kg": s.charge_kg,
            "lcgwp": round(lcgwp, 2),
            "lcodp": round(lcodp, 6),
        })

    weighted = total_lcgwp / total_capacity if total_capacity > 0 else 0

    # LEED v5 threshold: LCGWP ≤ 100 per kW
    return RefrigerantCalcResult(
        total_lcgwp=round(total_lcgwp, 2),
        weighted_lcgwp=round(weighted, 2),
        total_lcodp=round(total_lcodp, 6),
        meets_gwp_threshold=weighted <= 100,
        meets_odp_threshold=total_lcodp == 0,
        system_details=details,
    )


# ---------------------------------------------------------------------------
# Confidence scoring (shared)
# ---------------------------------------------------------------------------

def compute_confidence_tier(
    component_scores: dict[str, float],
    floor_threshold: float = 0.70,
) -> dict[str, Any]:
    """Compute overall confidence tier from component scores.

    Floor Rule: if any critical component < floor_threshold → Tier C.
    """
    if not component_scores:
        return {"overall": 0.0, "tier": "C", "floor_triggered": True, "components": {}}

    overall = sum(component_scores.values()) / len(component_scores)
    floor_triggered = any(v < floor_threshold for v in component_scores.values())

    if floor_triggered:
        tier = "C"
    elif overall >= 0.85:
        tier = "A"
    else:
        tier = "B"

    return {
        "overall": round(overall, 3),
        "tier": tier,
        "floor_triggered": floor_triggered,
        "components": {k: round(v, 3) for k, v in component_scores.items()},
    }
