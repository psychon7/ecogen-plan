---
name: leed-we-p2-water-min
version: 1.0.0
author: LEED Automation Platform
description: Automates LEED v5 WEp2 Minimum Water Efficiency prerequisite documentation, validation, and submission.
---

## Metadata
- **Credit Code:** WEp2
- **Credit Name:** Minimum Water Efficiency
- **Points:** Required (Prerequisite)
- **Automation Level:** 89.3%
- **Complexity:** Low
- **Primary Data Source:** EPA WaterSense Product Database, ENERGY STAR Product API, USGBC Arc Platform API
- **HITL Required:** Yes

## Purpose
Automates the baseline-vs-design indoor water use calculation for LEED v5 WEp2, validates fixture specifications against EPA WaterSense and ENERGY STAR databases, verifies the ≥20% reduction requirement, and generates all submission-ready documents.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| fixture_schedule | List[Fixture] | Consultant upload | Must contain ≥1 fixture per type; all fields populated |
| project_occupancy | Object | Consultant input | FTE ≥ 0, transient ≥ 0, resident ≥ 0 (at least one > 0) |
| building_type | Enum | Consultant input | One of: office, retail, residential, healthcare, education, hospitality, warehouse, other |
| gender_ratio | Float | Consultant input | 0.0–1.0 (male proportion), used for toilet/urinal split |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| usage_frequency_override | Dict | None | Override default uses per occupant per day per fixture type |
| include_residential_units | Bool | False | Whether project has residential dwelling units with residential fixtures |
| residential_unit_count | Int | 0 | Number of dwelling units; required if include_residential_units=True |
| outdoor_water_separation | Bool | True | Whether outdoor water is metered separately (recommended for accuracy) |
| custom_baseline_flow_rates | Dict | None | Override standard LEED baseline flow rates (gpm/gpf) per fixture type |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:** Parse the uploaded fixture schedule CSV/JSON and validate schema integrity. Ensure all required fields are present (fixture_type, flow_rate, manufacturer, model, quantity). Cross-check building_type against supported enum values. Validate gender_ratio is within [0, 1]. Verify at least one occupancy category has a positive count.
- **Output:** Validated `FixtureSchedule` object with typed fields, or `ValidationError` with field-level details.
- **On Failure:** Return 400-style error to caller with specific field failures; do not proceed.

### Step 2: Fetch EPA WaterSense Certification
- **Type:** API Call
- **Automated:** Yes
- **Description:** For each fixture with manufacturer and model, query the EPA WaterSense Product Database (public REST API, no auth required). Retrieve certified flow rate, flush volume, and product category. Flag discrepancies if the specified flow_rate deviates > ±5% from the certified value. For uncertified products, flag as "non-WaterSense" and continue (product does not need to be WaterSense-certified to meet WEp2, but certification aids credibility).
- **Output:** `WaterSenseMatchResult` per fixture: `{fixture_id, certified_flow_rate, deviation_pct, certification_status}`.
- **On Failure:** If API timeout or 5xx, retry up to 3x with exponential backoff. If still failing, mark fixtures as "unverified" and continue; log warning for HITL review.

### Step 3: Fetch ENERGY STAR Appliance Data
- **Type:** API Call
- **Automated:** Yes
- **Description:** For ENERGY STAR–eligible fixture categories (dishwashers, clothes washers), query the ENERGY STAR Product API (https://data.energystar.gov/resource/). Retrieve rated water factor (WF) or water consumption per cycle. Compare to LEED baseline values. Validate that specified appliance water use is consistent with ENERGY STAR data.
- **Output:** `EnergyStarMatchResult` per appliance: `{fixture_id, rated_wf, rated_gallons_per_cycle, baseline_comparison}`.
- **On Failure:** Retry 3x. On persistent failure, mark as "unverified" and continue; flag in HITL checkpoint.

### Step 4: Calculate Baseline Water Use
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Compute total daily baseline water use using LEED v5 default fixture baseline flow rates and default usage frequencies per Appendix 2 (Table 1). Formula per fixture type: `baseline_use = fixture_count × baseline_flow_rate × uses_per_person_per_day × effective_occupancy`. Sum across all fixture types. Effective occupancy applies gender split for toilets/urinals (male count vs. female count derived from gender_ratio). Standard baseline flow rates: toilet=1.6 gpf, urinal=1.0 gpf, lavatory faucet=2.2 gpm, kitchen faucet=2.2 gpm, showerhead=2.5 gpm. Default usage frequencies depend on building_type (office: 3 toilet uses, 3 faucet uses, 1 shower per FTE who showers; residential: 5 toilet, 5 faucet, 1 shower per resident daily, etc.).
- **Output:** `BaselineWaterUse` object with daily, monthly, and annual gallons; breakdown by fixture type.
- **On Failure:** If invalid data (e.g., missing flow_rate), raise `CalculationError` and abort to HITL.

### Step 5: Calculate Design Water Use
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Compute total daily design water use using consultant-provided fixture flow rates and the same occupancy/usage frequencies. Formula: `design_use = fixture_count × design_flow_rate × uses_per_person_per_day × effective_occupancy`. Sum across all fixture types. If usage_frequency_override provided, use those values instead of defaults.
- **Output:** `DesignWaterUse` object with daily, monthly, and annual gallons; breakdown by fixture type.
- **On Failure:** If design_flow_rate > baseline_flow_rate for any fixture type, flag as "reduction impossible for this fixture" but continue calculation.

### Step 6: Compute Water Reduction Percentage
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Calculate percentage reduction: `water_reduction_pct = (baseline_annual_gal − design_annual_gal) / baseline_annual_gal × 100`. Round to one decimal place. Verify `water_reduction_pct ≥ 20.0%`. If threshold not met, compute the additional flow rate reduction needed per fixture type to reach 20% and include in diagnostic output.
- **Output:** `ReductionResult`: `{water_reduction_pct, baseline_annual_gal, design_annual_gal, meets_threshold: bool, gap_analysis}`.
- **On Failure:** If threshold not met, proceed to HITL checkpoint with gap analysis; do not auto-reject.

### Step 7: HITL Checkpoint — Verify Fixture Schedule & Occupancy
- **Type:** Human Review
- **Automated:** No
- **Description:** Present the reviewer (LEED consultant or project manager) with: (a) the uploaded fixture schedule rendered as a sortable table, (b) EPA WaterSense/ENERGY STAR match results with deviation flags, (c) occupancy assumptions with building-type defaults exposed, (d) baseline vs. design water use breakdown by fixture type, and (e) the computed reduction percentage. Reviewer must confirm fixture types, quantities, flow rates, and occupancy counts are accurate. Reviewer may adjust flow rates or occupancy inline; recalculation triggers automatically upon save.
- **Output:** `HITLReviewResult`: `{approved: bool, reviewer_id, timestamp, adjustments_made: []}`.
- **On Failure:** If rejected, return to consultant with annotated feedback; if approved, proceed to document generation.

### Step 8: Generate Compliance Table (XLSX)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generate a formatted Excel workbook with three sheets: (1) Fixture Compliance — each fixture with type, manufacturer, model, quantity, baseline flow rate, design flow rate, WaterSense/ENERGY STAR status, deviation; (2) Water Use Calculation — daily/annual baseline and design use by fixture type with reduction %; (3) Occupancy & Usage — FTE, transient, resident counts, gender split, uses per person per day per fixture type, and effective occupancy per fixture type.
- **Output:** `/tmp/we_p2_fixture_compliance_{project_id}.xlsx`
- **On Failure:** If generation fails, retry once; if still failing, alert engineering team via Slack/email and pause.

### Step 9: Generate Calculation Narrative (PDF)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generate a professional PDF report containing: cover page with project info and credit code, executive summary showing baseline vs. design and % reduction, methodology section citing LEED v5 Appendix 2 baseline values and usage frequencies, detailed calculation tables, fixture schedule summary, EPA WaterSense/ENERGY STAR verification evidence, and a compliance statement. Embed formulas so reviewer can trace calculations.
- **Output:** `/tmp/we_p2_water_calculations_{project_id}.pdf`
- **On Failure:** Retry once; on persistent failure, alert engineering and pause.

### Step 10: Generate Narrative Document (DOCX)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generate a Word document with the formal LEED narrative: introduction describing project water use goals, description of water-conserving fixtures and fittings installed, summary of baseline and design water use calculations, demonstration that ≥20% reduction is achieved, and references to supporting evidence (fixture cut sheets, WaterSense certifications). The document is ready for minor human editing before final upload.
- **Output:** `/tmp/we_p2_narrative_{project_id}.docx`
- **On Failure:** Retry once; on persistent failure, alert engineering and pause.

### Step 11: Upload to USGBC Arc Platform
- **Type:** API Call
- **Automated:** Yes
- **Description:** Authenticate with USGBC Arc Platform API via OAuth 2.0 client credentials flow. Upload the three generated documents to the project's WEp2 credit folder. Submit the calculated baseline, design, and reduction percentage as performance data JSON per Arc's WEp2 data schema. Update credit status to "Ready for Review" if all validations pass and HITL approved.
- **Output:** `ArcUploadResult`: `{credit_id, upload_urls, submission_status, arc_submission_id}`.
- **On Failure:** If OAuth token expired, refresh and retry. If Arc API returns 4xx with schema error, log details and return to HITL for data correction. If 5xx, retry 3x with backoff; on persistent failure, queue for manual upload and notify project manager.

### Step 12: Finalize and Notify
- **Type:** Validation
- **Automated:** Yes
- **Description:** Compile a summary JSON with all results, document paths, Arc submission IDs, and HITL reviewer info. Send notification email to project team with links to generated documents and Arc platform. Mark skill execution as complete in the workflow state.
- **Output:** `FinalResult` JSON.
- **On Failure:** Log error; notification delivery is non-blocking.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 7: Verify Fixture Schedule & Occupancy | LEED Consultant / Project Manager | 48 hours | Review fixture schedule for accuracy: confirm fixture types, manufacturer/model, quantities, and flow rates match construction documents. Verify occupancy counts (FTE, transient, resident) and gender ratio are realistic for building type and operational program. Check flagged WaterSense/ENERGY STAR deviations. Adjust any values inline if needed; recalculation auto-triggers on save. Approve only when confident data is accurate. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| EPA WaterSense Product Search API | Verify fixture flow rates against certified products | US (primary); global product coverage | Manual lookup via watersense-product-search.epa.gov web search | No rate limit documented; use 1 req/sec to be safe |
| ENERGY STAR Product API (Socrata) | Verify appliance water efficiency ratings | US | Manual lookup via energystar.gov product finder | 1000 req/day per API key |
| USGBC Arc Platform API | Submit performance data and documents | Global (requires USGBC project) | Manual upload via Arc web UI | 100 req/min per OAuth token |
| USGBC Arc OAuth 2.0 | Authentication for Arc API | Global | Manual token refresh | Standard OAuth limits |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | Full EPA WaterSense and ENERGY STAR API access |
| Canada | Available | WaterSense product data applicable; ENERGY STAR Canada overlap |
| European Union | Available | Fixture standards universal (flow rate verification independent of EPA); may need manual cross-reference to local certifications |
| Asia-Pacific | Available | Same as EU; flow rate data universal; WaterSense lookup useful for imported products |
| Middle East / Africa | Available | Same as above; baseline flow rates are LEED global standards |
| Latin America | Available | WaterSense-certified products common; full automation supported |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Fixture schedule schema invalid | Abort; return detailed validation error | Yes (consultant) | No |
| EPA WaterSense API timeout/unavailable | Mark fixtures as "unverified"; continue | No (flag in HITL) | 3x with backoff |
| ENERGY STAR API timeout/unavailable | Mark appliances as "unverified"; continue | No (flag in HITL) | 3x with backoff |
| Flow rate deviation > ±5% from WaterSense certified | Flag fixture; highlight in HITL | No (HITL review) | No |
| Design flow rate exceeds baseline for a fixture type | Flag as "negative reduction"; include in gap analysis | No (HITL review) | No |
| Water reduction < 20% | Continue to HITL with gap analysis | Yes (consultant + gap suggestions) | No |
| USGBC Arc OAuth failure | Refresh token; retry once | Yes (PM) if persistent | 1x refresh |
| USGBC Arc 5xx error | Queue for retry; hold submission | Yes (PM) | 3x with backoff |
| Document generation failure | Alert engineering; pause workflow | Yes (engineering team) | 1x |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Water Use Baseline and Design Calculations | PDF | Comprehensive calculation report with methodology, tables, formulas, and compliance statement |
| Fixture Compliance Table | XLSX | Three-sheet workbook with fixture inventory, water use calculations, and occupancy/usage data |
| LEED Narrative — 20% Water Reduction | DOCX | Formal narrative document demonstrating prerequisite compliance, ready for final editing |

## Testing
```bash
# Unit tests for validation, calculation, and API mocking
python -m pytest skills/leed-we-p2-water-min/tests/

# Key test suites:
# - test_validation.py: Fixture schedule schema validation, occupancy checks
# - test_calculations.py: Baseline/design math, reduction %, edge cases (zero occupancy, all-male/all-female)
# - test_api_clients.py: Mocked EPA WaterSense and ENERGY STAR API responses
# - test_document_generation.py: XLSX, PDF, DOCX output verification
# - test_hitl_workflow.py: HITL checkpoint state transitions
# - test_arc_upload.py: Mocked USGBC Arc OAuth and submission flows
```

## Example Usage (Deer-Flow)
```python
from deerflow.skills import LEEDWaterMinEfficiencySkill

skill = LEEDWaterMinEfficiencySkill(
    project_id="proj-12345",
    inputs={
        "fixture_schedule": [
            {
                "fixture_type": "toilet",
                "flow_rate": 1.28,
                "flow_rate_unit": "gpf",
                "manufacturer": "TOTO",
                "model": "Drake II CST454CEFG",
                "quantity": 24
            },
            {
                "fixture_type": "lavatory_faucet",
                "flow_rate": 1.5,
                "flow_rate_unit": "gpm",
                "manufacturer": "Delta",
                "model": "Lahara 2538-MPU-DST",
                "quantity": 24
            },
            {
                "fixture_type": "showerhead",
                "flow_rate": 1.75,
                "flow_rate_unit": "gpm",
                "manufacturer": "Moen",
                "model": "Velocity S6320",
                "quantity": 8
            }
        ],
        "project_occupancy": {
            "fte": 120,
            "transient": 30,
            "resident": 0
        },
        "building_type": "office",
        "gender_ratio": 0.55
    }
)

result = await skill.execute()

# result contains:
# - water_reduction_pct: 24.7
# - meets_threshold: True
# - baseline_annual_gal: 1_847_520
# - design_annual_gal: 1_391_304
# - documents: [pdf_path, xlsx_path, docx_path]
# - arc_submission_id: "arc-sub-98765"
```

## Deer-Flow Workflow (LangGraph)
```python
from langgraph.graph import StateGraph, END
from deerflow.state import LEEDState
from deerflow.nodes import (
    validate_inputs,
    fetch_watersense_data,
    fetch_energystar_data,
    calculate_baseline_use,
    calculate_design_use,
    compute_reduction,
    hitl_review_checkpoint,
    generate_xlsx_compliance_table,
    generate_pdf_calculations,
    generate_docx_narrative,
    upload_to_arc_platform,
    finalize_and_notify
)

workflow = StateGraph(LEEDState)

# Add nodes
workflow.add_node("validate", validate_inputs)
workflow.add_node("fetch_watersense", fetch_watersense_data)
workflow.add_node("fetch_energystar", fetch_energystar_data)
workflow.add_node("calc_baseline", calculate_baseline_use)
workflow.add_node("calc_design", calculate_design_use)
workflow.add_node("calc_reduction", compute_reduction)
workflow.add_node("hitl_review", hitl_review_checkpoint)
workflow.add_node("gen_xlsx", generate_xlsx_compliance_table)
workflow.add_node("gen_pdf", generate_pdf_calculations)
workflow.add_node("gen_docx", generate_docx_narrative)
workflow.add_node("arc_upload", upload_to_arc_platform)
workflow.add_node("finalize", finalize_and_notify)

# Define edges
workflow.set_entry_point("validate")
workflow.add_edge("validate", "fetch_watersense")
workflow.add_edge("validate", "fetch_energystar")
workflow.add_edge("fetch_watersense", "calc_baseline")
workflow.add_edge("fetch_energystar", "calc_baseline")
workflow.add_edge("calc_baseline", "calc_design")
workflow.add_edge("calc_design", "calc_reduction")
workflow.add_edge("calc_reduction", "hitl_review")
workflow.add_edge("hitl_review", "gen_xlsx")
workflow.add_edge("hitl_review", "gen_pdf")
workflow.add_edge("hitl_review", "gen_docx")
workflow.add_edge("gen_xlsx", "arc_upload")
workflow.add_edge("gen_pdf", "arc_upload")
workflow.add_edge("gen_docx", "arc_upload")
workflow.add_edge("arc_upload", "finalize")
workflow.add_edge("finalize", END)

# Conditional: if HITL rejects, loop back to validate with reviewer annotations
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: "validate" if state.hITL_result.approved is False else "gen_xlsx",
    {"validate": "validate", "gen_xlsx": "gen_xlsx"}
)

app = workflow.compile()

# Execute
initial_state = LEEDState(
    project_id="proj-12345",
    inputs={...},
    documents=[],
    hitl_result=None,
    arc_submission_id=None
)
final_state = await app.ainvoke(initial_state)
```

## Appendix A: LEED v5 Baseline Flow Rates & Usage Frequencies (Default)
| Fixture Type | Baseline Flow Rate | Unit | Default Uses/Person/Day (Office) | Default Uses/Person/Day (Residential) |
|--------------|-------------------|------|----------------------------------|---------------------------------------|
| Toilet (water closet) | 1.6 | gpf | 3 (FTE) | 5 (resident) |
| Urinal | 1.0 | gpf | 2 (male FTE only) | N/A |
| Lavatory faucet (public) | 2.2 | gpm | 3 | 5 |
| Lavatory faucet (private) | 2.2 | gpm | N/A | 5 |
| Kitchen faucet | 2.2 | gpm | 1 (if kitchen present) | 4 |
| Showerhead | 2.5 | gpm | 0.1 (if gym/showers) | 1 |
| Dishwasher (ENERGY STAR) | 6.5 | gal/cycle | 0.1 (if kitchen) | 1 |
| Clothes washer (ENERGY STAR) | 24.5 | gal/cycle | N/A | 1 per 2 residents |

> Note: Exact usage frequencies should be drawn from LEED v5 Reference Guide Appendix 2, Table 1, adjusted for building type. The table above shows representative defaults; the skill should embed the full LEED-v5-specified table.

## Appendix B: Arc Platform WEp2 Data Schema (Performance Data JSON)
```json
{
  "credit_code": "WEp2",
  "baseline_annual_water_use_gal": 1847520,
  "design_annual_water_use_gal": 1391304,
  "water_reduction_percentage": 24.7,
  "fixture_summary": [
    {
      "fixture_type": "toilet",
      "quantity": 24,
      "baseline_flow_rate": 1.6,
      "design_flow_rate": 1.28,
      "baseline_annual_gal": 562176,
      "design_annual_gal": 449741
    }
  ],
  "occupancy": {
    "fte": 120,
    "transient": 30,
    "resident": 0,
    "gender_ratio": 0.55
  },
  "building_type": "office",
  "watersense_verified": true,
  "energystar_verified": false,
  "documents": [
    {"type": "calculations_pdf", "arc_file_id": "file-abc123"},
    {"type": "compliance_xlsx", "arc_file_id": "file-def456"},
    {"type": "narrative_docx", "arc_file_id": "file-ghi789"}
  ]
}
```

## Appendix C: State Schema (LEEDState for LangGraph)
```python
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class Fixture:
    fixture_type: str  # "toilet", "urinal", "lavatory_faucet", "kitchen_faucet", "showerhead", "dishwasher", "clothes_washer"
    flow_rate: float
    flow_rate_unit: str  # "gpf", "gpm", "gal/cycle"
    manufacturer: str
    model: str
    quantity: int

@dataclass
class Occupancy:
    fte: int
    transient: int
    resident: int

@dataclass
class HITLResult:
    approved: bool
    reviewer_id: str
    timestamp: str
    adjustments_made: List[Dict[str, Any]]
    comments: Optional[str]

@dataclass
class LEEDState:
    project_id: str
    inputs: Dict[str, Any]
    validated_fixtures: Optional[List[Fixture]] = None
    occupancy: Optional[Occupancy] = None
    watersense_results: Optional[List[Dict]] = None
    energystar_results: Optional[List[Dict]] = None
    baseline_use: Optional[float] = None
    design_use: Optional[float] = None
    reduction_pct: Optional[float] = None
    meets_threshold: Optional[bool] = None
    hitl_result: Optional[HITLResult] = None
    documents: List[str] = None
    arc_submission_id: Optional[str] = None
    errors: List[str] = None
```
