---
name: leed-ss-c5-heat-island
version: 1.0.0
author: LEED Automation Platform
description: Automate SSc5 Heat Island Reduction credit compliance for high-SRI roofing, paving, and vegetation strategies.
---

## Metadata
- **Credit Code:** SSc5
- **Credit Name:** Heat Island Reduction
- **Points:** 2
- **Automation Level:** 85.3%
- **Complexity:** Low
- **Primary Data Source:** Cool Roof Rating Council (CRRC), Tree Equity Score (American Forests), Material SRI Databases
- **HITL Required:** Yes

## Purpose
Automate the calculation, compliance verification, and documentation of heat island reduction strategies using SRI-weighted materials, vegetated surfaces, and tree canopy coverage for LEED v5 SSc5.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `roof_area_sqft` | float | Project drawing/quantity takeoff | `> 0` |
| `roof_slope` | string | Project specifications | Enum: `"low"` (≤2:12), `"steep"` (>2:12) |
| `roof_materials` | list[dict] | User input / CRRC lookup | Each dict: `{ "area": float, "sri": float, "product_id": str, "manufacturer": str }` |
| `nonroof_paving_area_sqft` | float | Project drawing/quantity takeoff | `≥ 0` |
| `nonroof_materials` | list[dict] | User input / CRRC lookup | Each dict: `{ "area": float, "sri": float, "type": str ("open_grid"|"vegetated"|"high_sri"|"shade") }` |
| `parking_spaces_total` | int | Project drawing | `≥ 0` |
| `parking_covered_spaces` | int | Project drawing | `0 ≤ value ≤ parking_spaces_total` |
| `tree_canopy_sqft` | float | Tree Equity Score / landscape plan | `≥ 0` |
| `site_area_sqft` | float | Project boundary / civil plan | `> 0` |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `project_address` | string | `""` | Full street address for Tree Equity Score API lookup |
| `project_lat` | float | `0.0` | Latitude (fallback if address unavailable) |
| `project_lon` | float | `0.0` | Longitude (fallback if address unavailable) |
| `census_tract_id` | string | `""` | 11-digit GEOID for direct Tree Equity Score lookup |
| `parking_high_sri_materials` | list[dict] | `[]` | Materials used for uncovered parking surfaces `{ "area": float, "sri": float }` |
| `vegetated_surface_sqft` | float | `0.0` | Total area of vegetated open-grid paving |
| `shade_structure_sqft` | float | `0.0` | Area under shade structures (solar canopies, awnings) |
| `manufacturer_data_sheets` | list[str] | `[]` | URLs or file paths to SRI manufacturer documentation |
| `roof_exemption_sqft` | float | `0.0` | Area of roof exempt from SRI (vegetated roofs, PV panels, pool covers) |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:** Verify all required inputs are present and within valid ranges. Confirm roof_materials and nonroof_materials arrays contain valid SRI values (0–100 range). Validate that sum of material areas does not exceed declared total area for each surface type. Check that parking_covered_spaces ≤ parking_spaces_total.
- **Output:** `validated_inputs` dict with normalized units and error flags
- **On Failure:** Return `InputValidationError` with specific field-level messages; halt workflow

### Step 2: Lookup CRRC SRI Values
- **Type:** API Call
- **Automated:** Yes
- **Description:** Query the Cool Roof Rating Council (CRRC) Rated Products Directory for each roof and non-roof material `product_id`. Retrieve certified Solar Reflectance (SR), Thermal Emittance (TE), and calculated SRI. If product_id is not provided, attempt fuzzy match by manufacturer + product name. Cache results.
- **Output:** `crrc_lookup_results` — list of dicts with `{ "product_id", "sr", "te", "sri", "source_url" }`
- **On Failure:** Flag materials for HITL review in Step 5; proceed with user-provided SRI values

### Step 3: Fetch Tree Equity Score
- **Type:** API Call
- **Automated:** Yes
- **Description:** Call American Forests Tree Equity Score API using `project_address`, `(lat, lon)`, or `census_tract_id`. Retrieve existing tree canopy percentage for the project census tract. Compare against project-proposed tree canopy coverage. If project is outside US, skip this call and rely solely on user-provided tree_canopy_sqft.
- **Output:** `tree_equity_data` — dict with `{ "canopy_pct", "target_canopy_pct", "tract_geoid", "status" }`
- **On Failure:** Log warning; proceed with user-provided canopy data

### Step 4: Calculate Weighted Average SRI (Roof)
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Compute weighted average SRI for roof materials excluding exempt areas. Apply slope-based threshold: low-slope roofs require weighted SRI ≥ 64; steep-slope roofs require weighted SRI ≥ 82. Formula: `roof_compliant = (Σ(material_area_i × sri_i)) / roof_area_sqft ≥ threshold`. If exempt areas exist, subtract from denominator.
- **Output:** `roof_sri_compliance` — dict with `{ "weighted_sri", "threshold", "compliant": bool, "exempt_area": float }`
- **On Failure:** `CalculationError`; retry once; then raise

### Step 5: Verify Material SRI — HITL Checkpoint
- **Type:** Human Review
- **Automated:** No
- **Description:** Present reviewer with all roof and non-roof materials, their SRI values, CRRC lookup status, and manufacturer documentation links. Reviewer confirms SRI values are from manufacturer datasheets or CRRC-certified ratings. If CRRC lookup failed or user-provided SRI deviates >5 points from CRRC value, flag for manual override.
- **Output:** `hitl_material_verification` — dict with `{ "verified": bool, "overrides": list, "reviewer_id": str, "timestamp": str }`
- **On Failure:** Wait for human response (SLA: 48h); send reminder at 24h

### Step 6: Calculate Non-Roof Paving Compliance
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Calculate percentage of non-roof paving area using compliant strategies: vegetated surfaces, open-grid pavers (≥50% pervious/open), high-SRI materials (SRI ≥ 29), and shade structures. Formula: `nonroof_compliant = (vegetated_sqft + open_grid_sqft + shade_structure_sqft + high_sri_sqft) / nonroof_paving_area_sqft`. Threshold: ≥ 50%.
- **Output:** `nonroof_compliance` — dict with `{ "compliant_area": float, "compliant_pct": float, "threshold": 0.50, "compliant": bool }`
- **On Failure:** `CalculationError`; retry once; then raise

### Step 7: Calculate Parking Compliance
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Evaluate parking under cover OR high-SRI materials. Option 1: covered_pct = parking_covered_spaces / parking_spaces_total ≥ 50%. Option 2: if cover < 50%, verify uncovered parking uses high-SRI materials (SRI ≥ 29) and the weighted average across all parking surfaces ≥ 29. Set `parking_compliant` if either option passes.
- **Output:** `parking_compliance` — dict with `{ "option_used": str, "covered_pct": float, "parking_sri": float, "compliant": bool }`
- **On Failure:** `CalculationError`; retry once; then raise

### Step 8: Calculate Tree Canopy Compliance
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Compute tree canopy coverage as percentage of total site area. Formula: `canopy_pct = tree_canopy_sqft / site_area_sqft`. Threshold: ≥ 30%. If Tree Equity Score API returned a higher regional target, use the stricter of the two thresholds. Flag discrepancy if user canopy is significantly below regional average.
- **Output:** `canopy_compliance` — dict with `{ "canopy_pct": float, "threshold": float, "compliant": bool, "regional_canopy_pct": float }`
- **On Failure:** `CalculationError`; retry once; then raise

### Step 9: Aggregate Credit Points
- **Type:** Calculation
- **Automated:** Yes
- **Description:** LEED v5 SSc5 awards up to 2 points based on compliant strategies. Point allocation: 1 point for roof compliance; 1 point for non-roof + parking + canopy (at least two of three must pass for full 2 points). If only roof passes, award 1 point. If roof fails but ≥2 of other strategies pass, award 1 point. If roof + ≥1 other passes, award 2 points. Produce final point summary.
- **Output:** `credit_points` — dict with `{ "points_achieved": int, "max_points": 2, "breakdown": dict }`
- **On Failure:** `CalculationError`; retry once; then raise

### Step 10: Generate SRI Compliance Table (XLSX)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generate Excel workbook with three sheets: (1) Roof Materials — area, SR, TE, SRI, weighted contribution; (2) Non-Roof Materials — area, type, SRI, compliant area tally; (3) Parking & Canopy — spaces, cover percentage, canopy percentage. Include pass/fail indicators and threshold references.
- **Output:** `sri_compliance_table.xlsx` file path
- **On Failure:** `DocumentGenerationError`; retry with alternate template; notify if persistent

### Step 11: Generate Heat Island Reduction Calculations (PDF)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Produce PDF narrative report showing all calculations, formulas, threshold comparisons, weighted averages, and strategy descriptions. Include material specifications, CRRC references, Tree Equity Score results, and compliance verdicts for roof, non-roof, parking, and canopy.
- **Output:** `heat_island_reduction_calculations.pdf` file path
- **On Failure:** `DocumentGenerationError`; retry with alternate renderer; notify if persistent

### Step 12: Generate Material Specification Summary (PDF)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generate concise PDF summary of all specified materials with manufacturer names, product IDs, CRRC ratings (SR, TE, SRI), and installation notes. Include HITL reviewer sign-off block and date stamp.
- **Output:** `material_specification_summary.pdf` file path
- **On Failure:** `DocumentGenerationError`; retry; notify if persistent

### Step 13: Finalize and Return
- **Type:** Validation
- **Automated:** Yes
- **Description:** Verify all three output documents exist and are non-empty. Compile final result payload with compliance booleans, points achieved, material lists, and document paths. Log execution summary.
- **Output:** `SkillResult` object with all deliverables and metadata
- **On Failure:** `FinalizationError`; return partial results with warning flags

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 5: Verify Material SRI | Sustainability Consultant / LEED AP | 48 hours | Confirm each material's SRI value is sourced from CRRC-certified rating or manufacturer datasheet. Verify product IDs match actual specifications. Override any flagged discrepancies. Approve or reject with notes. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| CRRC Rated Products Directory | SRI, SR, TE lookup by product ID | Global | User-provided SRI from manufacturer datasheet | 100 req/min (public) |
| American Forests Tree Equity Score | Existing tree canopy % by census tract | US only (excl. territories) | User-provided canopy area + site plan | 1000 req/day (public) |
| Manufacturer SRI Databases | Product-specific SRI values | Global (varies by manufacturer) | CRRC lookup; generic SRI tables | N/A (third-party) |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | Full CRRC + Tree Equity Score API access |
| Canada | Available | CRRC access; Tree Equity Score unavailable (use user-provided canopy) |
| Europe | Available | CRRC access for imported products; no Tree Equity Score (use user-provided canopy) |
| Asia-Pacific | Available | CRRC access; regional manufacturer databases may supplement; no Tree Equity Score |
| Middle East / Africa | Available | CRRC access; limited local SRI databases; no Tree Equity Score |
| Latin America | Available | CRRC access; no Tree Equity Score |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| `InputValidationError` | Halt workflow; return detailed field errors | Yes (project team) | 0 |
| `CRRCAPITimeout` | Use cached/user SRI; flag for HITL | No | 3 (exponential backoff) |
| `CRRCProductNotFound` | Proceed with user SRI; flag for HITL verification | No | 0 |
| `TreeEquityScoreTimeout` | Skip API; use user canopy data; log warning | No | 2 |
| `TreeEquityScoreOutOfRegion` | Skip API; log info; proceed with user data | No | 0 |
| `CalculationError` | Retry calculation; validate input types | No | 1 |
| `DocumentGenerationError` | Retry with alternate template/renderer | Yes (platform admin) | 2 |
| `HITLTimeout` | Escalate to secondary reviewer; extend SLA | Yes (reviewer + admin) | N/A |
| `HITLRejected` | Pause workflow; return partial results with rejection notes | Yes (project team) | N/A |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Heat Island Reduction Calculations | PDF | Full narrative with formulas, thresholds, compliance verdicts, and strategy descriptions |
| SRI Compliance Table | XLSX | Multi-sheet workbook with material areas, SRI values, weighted averages, and pass/fail indicators |
| Material Specification Summary | PDF | Concise material reference with manufacturer info, CRRC ratings, and HITL sign-off block |

## Testing
```bash
python -m pytest skills/leed-ss-c5-heat-island/tests/
```

## Example Usage (Deer-Flow)
```python
from deerflow.skills import HeatIslandReductionSkill

skill = HeatIslandReductionSkill(
    project_id="LEED-2024-8842",
    inputs={
        "roof_area_sqft": 45000.0,
        "roof_slope": "low",
        "roof_materials": [
            {"area": 30000.0, "sri": 78.0, "product_id": "CRRC-12345", "manufacturer": "CoolRoof Co"},
            {"area": 15000.0, "sri": 65.0, "product_id": "CRRC-67890", "manufacturer": "GreenShingle Inc"}
        ],
        "nonroof_paving_area_sqft": 25000.0,
        "nonroof_materials": [
            {"area": 8000.0, "sri": 35.0, "type": "high_sri"},
            {"area": 7000.0, "sri": 0.0, "type": "vegetated"},
            {"area": 5000.0, "sri": 29.0, "type": "open_grid"}
        ],
        "parking_spaces_total": 120,
        "parking_covered_spaces": 65,
        "tree_canopy_sqft": 18000.0,
        "site_area_sqft": 60000.0,
        "project_address": "1234 Market St, Philadelphia, PA 19107"
    }
)
result = await skill.execute()
print(result.points_achieved)  # 2
print(result.documents)        # ["sri_compliance_table.xlsx", "heat_island_reduction_calculations.pdf", ...]
```

## Deer-Flow Workflow (LangGraph)
```python
from langgraph.graph import StateGraph
from deerflow.skills.leed_ss_c5_heat_island.state import HeatIslandState

workflow = StateGraph(HeatIslandState)

# Nodes
workflow.add_node("validate", validate_inputs)
workflow.add_node("crrc_lookup", fetch_crrc_sri_values)
workflow.add_node("tree_equity", fetch_tree_equity_score)
workflow.add_node("calculate_roof", calculate_roof_sri_compliance)
workflow.add_node("hitl_material_review", human_review_checkpoint)  # HITL
workflow.add_node("calculate_nonroof", calculate_nonroof_compliance)
workflow.add_node("calculate_parking", calculate_parking_compliance)
workflow.add_node("calculate_canopy", calculate_canopy_compliance)
workflow.add_node("aggregate_points", aggregate_credit_points)
workflow.add_node("generate_xlsx", generate_sri_compliance_table)
workflow.add_node("generate_pdf_calcs", generate_heat_island_pdf)
workflow.add_node("generate_pdf_spec", generate_material_spec_pdf)
workflow.add_node("finalize", finalize_results)

# Edges
workflow.set_entry_point("validate")
workflow.add_edge("validate", "crrc_lookup")
workflow.add_edge("validate", "tree_equity")
workflow.add_edge("crrc_lookup", "calculate_roof")
workflow.add_edge("calculate_roof", "hitl_material_review")
workflow.add_edge("hitl_material_review", "calculate_nonroof")
workflow.add_edge("hitl_material_review", "calculate_parking")
workflow.add_edge("tree_equity", "calculate_canopy")
workflow.add_edge("calculate_nonroof", "aggregate_points")
workflow.add_edge("calculate_parking", "aggregate_points")
workflow.add_edge("calculate_canopy", "aggregate_points")
workflow.add_edge("aggregate_points", "generate_xlsx")
workflow.add_edge("generate_xlsx", "generate_pdf_calcs")
workflow.add_edge("generate_pdf_calcs", "generate_pdf_spec")
workflow.add_edge("generate_pdf_spec", "finalize")
workflow.add_edge("finalize", END)

# Conditional edges
workflow.add_conditional_edges(
    "hitl_material_review",
    lambda state: "approved" if state.hitl_verified else "rejected",
    {"approved": "calculate_nonroof", "rejected": END}
)

# Compile
app = workflow.compile()
```
