---
name: leed-ea-c7-refrigerant-enhanced
version: 1.0.0
author: LEED Automation Platform
description: Automate LEED EAc7 Enhanced Refrigerant Management compliance via GWP-weighted calculations and refrigerant-free system verification.
---

## Metadata
| Property | Value |
|----------|-------|
| **Credit Code** | EAc7 |
| **Credit Name** | Enhanced Refrigerant Management |
| **Points** | 2 |
| **Automation Level** | 89.3% |
| **Complexity** | Low |
| **Primary Data Sources** | EPA SNAP, IPCC AR6, Equipment schedules |
| **HITL Required** | Yes |
| **Data Availability Score** | 90/100 |
| **Real-time** | Yes |
| **Regional** | Global |

## Purpose
This skill automates LEED v5 EAc7 compliance by calculating the weighted average GWP of refrigerants in the project’s HVAC&R equipment, validating against the 675 GWP threshold, or confirming refrigerant-free system eligibility.

## LEED v5 Requirements
**Option 1 — Low-GWP Refrigerants**
- Do not install or maintain any refrigeration, HVAC, or fire suppression systems containing refrigerants with a GWP greater than 675.
- For HVAC&R systems containing a mixture of refrigerants, the weighted average GWP must not exceed 675.

**Option 2 — No Refrigerants**
- Do not use refrigerants in any refrigeration, HVAC, or fire suppression systems.
- Acceptable alternatives include: evaporative cooling, absorption chillers, desiccant dehumidification, natural ventilation, direct/indirect evaporative cooling, and systems using water or air as the working fluid.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `project_id` | String | User/DB | Non-empty, exists in project registry |
| `hvac_equipment_schedule` | JSON / CSV | Upload / CMMS | Must contain equipment_id, refrigerant_type, charge_kg |
| `credit_pathway` | Enum | User | `"low_gwp"` or `"no_refrigerant"` |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `equipment_count` | Integer | Auto-count | Number of HVAC&R units; used for sanity check |
| `snap_version` | String | `"2024"` | EPA SNAP program version for approved list |
| `ipcc_version` | String | `"AR6"` | IPCC assessment report for GWP values |
| `time_horizon` | Enum | `"100yr"` | GWP time horizon (`"20yr"` or `"100yr"`) |
| `building_area_sqft` | Float | 0 | For normalizing refrigerant charge per area |
| `include_fire_suppression` | Boolean | `false` | Whether fire suppression refrigerants are included |
| `gwp_tolerance` | Float | `0.01` | Numerical tolerance for ≤ 675 check |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. Verify `credit_pathway` is one of `"low_gwp"` or `"no_refrigerant"`.
  2. Parse `hvac_equipment_schedule`; ensure every row has `equipment_id`, `refrigerant_type`, and `charge_kg` (≥ 0).
  3. Check `refrigerant_type` is non-empty and contains at least one alphabetic character.
  4. If `credit_pathway` is `"no_refrigerant"`, skip refrigerant fields and validate documentation fields.
  5. Cross-check `equipment_count` against parsed rows if provided.
- **Output:** `ValidatedInput` dataclass with typed fields.
- **On Failure:** Return `InputValidationError` with missing / malformed field details; abort workflow.

### Step 2: Load GWP Reference Data
- **Type:** API Call / Static
- **Automated:** Yes
- **Description:**
  1. Load the bundled IPCC AR6 100-year GWP lookup table (`ipcc_ar6_gwp.json`).
  2. Map each `refrigerant_type` in the equipment schedule to its GWP value.
  3. For refrigerants not found in the bundled table, query the EPA SNAP approved-substitutes API (`https://www.epa.gov/snap/approved-substitutes`) to confirm low-GWP status and retrieve any supplemental GWP.
  4. Cache successful lookups for the session.
- **Output:** `List[RefrigerantGWP]` with fields: `refrigerant_type`, `gwp_value`, `source`.
- **On Failure:**
  - If bundled table is corrupt → retry once from backup mirror.
  - If EPA SNAP API times out → mark refrigerant as `UNKNOWN_GWP` and escalate to HITL.

### Step 3: Calculate Weighted Average GWP (Option 1)
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. For each equipment row, multiply `charge_kg` by `gwp_value`.
  2. Sum all charge-weighted GWP values: `Σ(Charge_i × GWP_i)`.
  3. Sum all charges: `Σ(Charge_i)`.
  4. Compute weighted average GWP:
     ```
     Weighted_Average_GWP = Σ(Charge_i × GWP_i) / Σ(Charge_i)
     ```
  5. Compare against threshold 675 with tolerance `gwp_tolerance`:
     ```python
     is_compliant = Weighted_Average_GWP <= (675 + gwp_tolerance)
     ```
  6. If `include_fire_suppression` is true, include fire suppression systems in the same calculation.
- **Output:** `CalculationResult` with `weighted_avg_gwp`, `total_charge_kg`, `unit_count`, `is_compliant`.
- **On Failure:** Division by zero (no charge data) → return `CalculationError`; abort workflow.

### Step 4: Verify Refrigerant-Free Systems (Option 2)
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. If `credit_pathway == "no_refrigerant"`, scan the equipment schedule for any refrigerant-containing entries.
  2. Confirm all HVAC&R systems use refrigerant-free technologies (evaporative, absorption, desiccant, natural ventilation, water/air-based).
  3. Flag any equipment that lists a refrigerant type or non-zero charge as a violation.
  4. Generate a summary of refrigerant-free system types found.
- **Output:** `NoRefrigerantVerification` with `systems_found`, `violation_count`, `is_compliant`.
- **On Failure:** If violations detected → mark non-compliant, append to compliance report, but continue to HITL checkpoint.

### Step 5: HITL Checkpoint — Refrigerant Compliance Verification
- **Type:** Human Review
- **Automated:** No
- **Description:**
  1. Present the reviewer with:
     - Selected credit pathway (Option 1 or Option 2)
     - For Option 1: weighted average GWP, per-equipment breakdown, and ≤ 675 compliance flag
     - For Option 2: list of refrigerant-free systems, any flagged violations
     - Raw equipment schedule for cross-reference
  2. Reviewer must confirm:
     - Equipment schedule accuracy and completeness
     - Refrigerant types and charges match manufacturer specifications
     - For Option 1: weighted average GWP ≤ 675 is correct
     - For Option 2: no refrigerants are used
  3. Reviewer approves, rejects, or requests clarification.
- **Output:** `HITLDecision` enum: `APPROVED`, `REJECTED`, or `CLARIFICATION`.
- **On Failure:** If reviewer requests clarification → return to Step 1 with comment annotations.

### Step 6: Generate Compliance Report
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Populate the Enhanced Refrigerant Compliance Report template (`templates/eac7_compliance_report.html`) with:
     - Project metadata and credit pathway
     - Complete equipment schedule with GWP values
     - Calculation steps and formulas
     - Weighted average GWP result and compliance determination
     - EPA SNAP and IPCC AR6 data sources cited
     - HITL approval timestamp and reviewer ID
  2. Render to PDF using `weasyprint` or `pdfkit`.
- **Output:** `eac7_compliance_report.pdf` (absolute path).
- **On Failure:** If template engine fails → fallback to raw Markdown → PDF via `pandoc`; log incident.

### Step 7: Generate Alternative System Documentation (Optional)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. If `credit_pathway == "no_refrigerant"`, generate a supplementary PDF:
     - List of all refrigerant-free systems
     - System types (evaporative, absorption, etc.)
     - Equipment IDs and capacities
     - Statement of no refrigerant use
  2. Format as `eac7_alternative_systems.pdf`.
- **Output:** `eac7_alternative_systems.pdf` (absolute path) or `None`.
- **On Failure:** Log warning; primary compliance report still delivered.

### Step 8: Persist & Return
- **Type:** Persistence
- **Automated:** Yes
- **Description:**
  1. Store the `CalculationResult` and generated PDF paths in the project database under `leed_credits.eac7`.
  2. Update the project’s LEED automation dashboard with compliance status.
  3. Return a JSON result object.
- **Output:**
  ```json
  {
    "credit_code": "EAc7",
    "compliant": true,
    "pathway": "low_gwp",
    "weighted_avg_gwp": 412.5,
    "total_charge_kg": 156.0,
    "unit_count": 12,
    "report_path": "/mnt/agents/output/eac7_compliance_report.pdf",
    "alt_doc_path": null,
    "hitl_status": "APPROVED",
    "data_sources": ["IPCC AR6", "EPA SNAP 2024"],
    "timestamp": "2024-06-15T09:34:12Z"
  }
  ```
- **On Failure:** If database write fails → retry up to 3× with exponential backoff; alert admin if all retries fail.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 5 | LEED AP / Mechanical Engineer | 48 hours | Verify equipment schedule accuracy. Confirm refrigerant types and charges match manufacturer cut-sheets. For Option 1, validate weighted average GWP ≤ 675. For Option 2, confirm zero refrigerant use. Approve or request clarification. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| EPA SNAP Approved Substitutes | Confirm low-GWP refrigerant approval status; retrieve supplemental GWP data | US primary, global reference | Bundled IPCC AR6 table (static) | Not published; use 1 req/sec |
| AHRI Directory | Cross-reference equipment efficiency and factory-charged refrigerant type | North America primary | Manufacturer spec sheets (manual upload) | 100 req/min |
| IPCC AR6 (static) | Primary GWP reference values | Global | IPCC AR5 fallback table | N/A (local file) |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | Full EPA SNAP integration; AHRI Directory active |
| Canada | Available | SNAP list applicable; AHRI covers most equipment |
| Europe | Available | IPCC AR6 primary; no EPA SNAP; use EU F-Gas registry as supplemental |
| Asia-Pacific | Available | IPCC AR6 primary; AHRI limited; manufacturer data recommended |
| Middle East / Africa | Available | IPCC AR6 primary; local manufacturer data may be required |
| Latin America | Available | IPCC AR6 primary; AHRI limited |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Input validation failure (missing fields) | Abort; return detailed error | Yes — immediate | 0 |
| Unknown refrigerant type (not in IPCC AR6 or EPA SNAP) | Flag for HITL review; set GWP to `null` | Yes — immediate | 0 |
| EPA SNAP API timeout | Use bundled IPCC AR6 table; log missing data | Yes — after 3 attempts | 3 |
| AHRI Directory timeout | Skip cross-reference; use uploaded schedule | No | 2 |
| Division by zero (zero total charge) | Abort; require charge data or switch to Option 2 | Yes — immediate | 0 |
| Weighted average GWP > 675 | Mark non-compliant; still generate report for review | Yes — immediate | 0 |
| PDF generation failure | Fallback to Markdown → pandoc; log incident | Yes — if fallback also fails | 1 |
| Database write failure | Retry with exponential backoff | Yes — after 3 retries | 3 |
| HITL rejection | Return to Step 1 with reviewer comments | Yes — immediate | 0 |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Enhanced Refrigerant Compliance Report | PDF | Full calculation, equipment breakdown, GWP sources, HITL approval, LEED v5 compliance statement |
| Alternative System Documentation | PDF | Refrigerant-free system inventory and certification (generated only for Option 2) |

## Testing
```bash
# Unit tests
python -m pytest skills/eac7/tests/test_validation.py
python -m pytest skills/eac7/tests/test_gwp_lookup.py
python -m pytest skills/eac7/tests/test_calculation.py
python -m pytest skills/eac7/tests/test_report_generation.py

# Integration tests
python -m pytest skills/eac7/tests/test_full_workflow.py

# HITL simulation tests
python -m pytest skills/eac7/tests/test_hitl_checkpoint.py
```

## Example Usage (Deer-Flow)
```python
from deerflow.skills import EnhancedRefrigerantManagementSkill

skill = EnhancedRefrigerantManagementSkill(
    project_id="LEED-2024-0892",
    inputs={
        "credit_pathway": "low_gwp",
        "hvac_equipment_schedule": [
            {"equipment_id": "AHU-01", "refrigerant_type": "R-410A", "charge_kg": 12.5},
            {"equipment_id": "AHU-02", "refrigerant_type": "R-32", "charge_kg": 8.0},
            {"equipment_id": "CHLR-01", "refrigerant_type": "R-134a", "charge_kg": 135.0},
        ],
        "ipcc_version": "AR6",
        "time_horizon": "100yr",
        "gwp_tolerance": 0.01,
    }
)
result = await skill.execute()
print(f"Compliant: {result['compliant']}, Weighted Avg GWP: {result['weighted_avg_gwp']}")
```

## Deer-Flow Workflow (LangGraph)
```python
from langgraph.graph import StateGraph, END
from deerflow.state import LEEDState
from deerflow.nodes import (
    validate_inputs,
    load_gwp_reference,
    calculate_weighted_gwp,
    verify_no_refrigerant,
    human_review_checkpoint,
    generate_compliance_report,
    generate_alt_system_doc,
    persist_results,
)

# Initialize the state graph
workflow = StateGraph(LEEDState)

# Add nodes
workflow.add_node("validate", validate_inputs)
workflow.add_node("load_gwp", load_gwp_reference)
workflow.add_node("calculate_gwp", calculate_weighted_gwp)
workflow.add_node("verify_no_ref", verify_no_refrigerant)
workflow.add_node("hitl_review", human_review_checkpoint)
workflow.add_node("generate_report", generate_compliance_report)
workflow.add_node("generate_alt_doc", generate_alt_system_doc)
workflow.add_node("persist", persist_results)

# Define edges
workflow.set_entry_point("validate")
workflow.add_edge("validate", "load_gwp")

# Branch based on credit pathway
workflow.add_conditional_edges(
    "load_gwp",
    lambda state: state.credit_pathway,
    {
        "low_gwp": "calculate_gwp",
        "no_refrigerant": "verify_no_ref",
    },
)

# Both pathways converge at HITL review
workflow.add_edge("calculate_gwp", "hitl_review")
workflow.add_edge("verify_no_ref", "hitl_review")

# HITL decision routing
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: state.hitl_status,
    {
        "APPROVED": "generate_report",
        "REJECTED": "validate",       # Loop back to validation with comments
        "CLARIFICATION": "validate",  # Loop back to validation with comments
    },
)

# Report generation, then optional alt doc
workflow.add_edge("generate_report", "generate_alt_doc")
workflow.add_edge("generate_alt_doc", "persist")
workflow.add_edge("persist", END)

# Compile
app = workflow.compile()
```

## Calculation Reference

### Weighted Average GWP (Option 1)
```
Weighted_Average_GWP = Σ(Charge_i × GWP_i) / Σ(Charge_i)
```
Where:
- `Charge_i` = refrigerant charge of equipment *i* (kg)
- `GWP_i` = 100-year GWP of refrigerant *i* per IPCC AR6
- `Σ(Charge_i)` = total refrigerant charge across all project HVAC&R equipment

**Compliance condition:**
```
Weighted_Average_GWP ≤ 675
```

### Example Calculation
| Equipment | Refrigerant | Charge (kg) | GWP (AR6 100-yr) | Charge × GWP |
|-----------|-------------|-------------|-------------------|--------------|
| AHU-01 | R-410A | 12.5 | 2,088 | 26,100 |
| AHU-02 | R-32 | 8.0 | 771 | 6,168 |
| CHLR-01 | R-1234ze | 135.0 | 7 | 945 |
| **Total** | | **155.5** | | **33,213** |

```
Weighted_Average_GWP = 33,213 / 155.5 = 213.6
Compliance: 213.6 ≤ 675 → PASS
```

### No-Refrigerant Verification (Option 2)
All entries in `hvac_equipment_schedule` must satisfy:
```
refrigerant_type in [None, "", "N/A", "none"]
AND charge_kg == 0
```
Any violation flags the project as non-compliant under Option 2.

## Data Model
```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class CreditPathway(Enum):
    LOW_GWP = "low_gwp"
    NO_REFRIGERANT = "no_refrigerant"

class HITLStatus(Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CLARIFICATION = "CLARIFICATION"
    PENDING = "PENDING"

@dataclass
class EquipmentRow:
    equipment_id: str
    refrigerant_type: str
    charge_kg: float
    system_type: Optional[str] = None  # e.g., "packaged_unit", "chiller"

@dataclass
class RefrigerantGWP:
    refrigerant_type: str
    gwp_value: float
    source: str  # "IPCC_AR6", "EPA_SNAP", "AHRI"
    time_horizon: str = "100yr"

@dataclass
class CalculationResult:
    weighted_avg_gwp: float
    total_charge_kg: float
    unit_count: int
    is_compliant: bool
    threshold: float = 675.0
    tolerance: float = 0.01

@dataclass
class NoRefrigerantVerification:
    systems_found: List[str]
    violation_count: int
    is_compliant: bool

@dataclass
class HITLDecision:
    status: HITLStatus
    reviewer_id: str
    timestamp: str
    comments: Optional[str] = None

@dataclass
class SkillOutput:
    credit_code: str
    compliant: bool
    pathway: str
    weighted_avg_gwp: Optional[float]
    total_charge_kg: Optional[float]
    unit_count: int
    report_path: str
    alt_doc_path: Optional[str]
    hitl_status: str
    data_sources: List[str]
    timestamp: str
```

## Appendix A: Common Refrigerant GWP Values (IPCC AR6, 100-yr)
| Refrigerant | GWP |
|-------------|-----|
| R-11 | 4,750 |
| R-12 | 10,200 |
| R-22 | 1,810 |
| R-32 | 771 |
| R-123 | 93 |
| R-134a | 1,530 |
| R-410A | 2,088 |
| R-404A | 3,943 |
| R-407C | 1,774 |
| R-448A | 1,386 |
| R-449A | 1,397 |
| R-452B | 676 |
| R-454B | 509 |
| R-513A | 631 |
| R-1234yf | < 1 |
| R-1234ze | 7 |
| R-744 (CO₂) | 1 |
| R-717 (Ammonia) | 0 |
| R-718 (Water) | 0 |
| R-290 (Propane) | 3 |

> **Note:** The full IPCC AR6 lookup table is bundled at `skills/eac7/data/ipcc_ar6_gwp.json`. Update annually or when a new IPCC assessment report is released.
