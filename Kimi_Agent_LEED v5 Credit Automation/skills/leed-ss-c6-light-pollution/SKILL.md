---
name: leed-ss-c6-light-pollution
version: 1.0.0
author: LEED Automation Platform
description: Automates SSc6 Light Pollution Reduction compliance via BUG rating validation, IDA zone classification, and luminaire control verification.
---

## Metadata
- **Credit Code:** SSc6
- **Credit Name:** Light Pollution Reduction
- **Points:** 1
- **Automation Level:** 90.6%
- **Complexity:** Low
- **Primary Data Source:** IES TM-15-11 BUG Rating Matrix (static), IDA Dark Sky Places Database, Manufacturer cut sheets
- **HITL Required:** Yes

## Purpose
Automatically validates luminaire BUG (Backlight-Uplight-Glare) ratings against IES TM-15-11 zone thresholds, verifies automatic lighting controls, and generates the complete SSc6 compliance documentation package.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `luminaire_schedule` | CSV / XLSX | Uploaded by user | Must contain columns: fixture_id, fixture_type, mounting_location, manufacturer, model_number, bug_backlight, bug_uplight, bug_glare, lumens, control_type, mounting_height_ft, wattage, quantity |
| `project_lat` | float | User input or project geocoding | -90.0 to 90.0 |
| `project_lon` | float | User input or project geocoding | -180.0 to 180.0 |
| `project_address` | string | User input | Non-empty, used for geocoding fallback |
| `exterior_total_watts` | float | Uploaded lighting power summary | >= 0 |
| `site_area_sqft` | float | Uploaded site plan / BIM | > 0 |
| `operational_hours` | string | User input | Format "HH:MM-HH:MM" or "24h" |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `lighting_zone_override` | string | auto-detected | Override IES LZ classification (LZ0, LZ1, LZ2, LZ3, LZ4) |
| `ida_dark_sky_proximity_miles` | float | auto-calculated | Distance to nearest IDA Dark Sky Place; used for LZ0 override |
| `interior_to_exterior_fixture_ids` | list[str] | [] | Fixture IDs for interior luminaires that emit light to exterior (must have U=0) |
| `curfew_time` | string | "22:00" | Local time when automatic reduction/shutoff must engage |
| `emergency_fixture_ids` | list[str] | [] | Fixtures exempt from automatic shutoff (code-required emergency lighting) |
| `shielding_description` | string | "" | Description of custom shielding for non-standard fixtures |
| `bim_luminaire_export` | JSON | null | Revit / BIM 360 luminaire export for automated schedule population |

## Workflow Steps (Durable)

### Step 1: Validate Inputs & Ingest Luminaire Schedule
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. Parse the uploaded luminaire schedule (CSV/XLSX) into a typed DataFrame.
  2. Validate required columns are present. If `bim_luminaire_export` is provided, merge/augment the schedule.
  3. Validate numeric fields: `bug_backlight`, `bug_uplight`, `bug_glare` must be integers 0-5 per IES TM-15-11; `lumens`, `wattage`, `quantity` must be > 0.
  4. Validate `mounting_location` values ∈ {interior, exterior, site}.
  5. Validate `control_type` values ∈ {motion_sensor, timer, photocell, manual, none}.
  6. Geocode `project_address` if `project_lat`/`project_lon` are missing.
- **Output:** `validated_schedule` (DataFrame), `project_coords` (lat, lon), `validation_report` (dict)
- **On Failure:** Return `ValidationError` with specific field-level messages. No retry; user must re-upload corrected schedule.

### Step 2: Determine IES Lighting Zone (LZ)
- **Type:** API Call + Calculation
- **Automated:** Yes
- **Description:**
  1. If `lighting_zone_override` is provided, use it directly.
  2. Otherwise, query the IDA Dark Sky Places database (https://www.darksky.org/our-work/conservation/international-dark-sky-places/) via API or web scrape to find the nearest Dark Sky Park, Reserve, Sanctuary, or Community.
  3. Calculate distance from project coordinates to nearest IDA place.
  4. Classify zone using the following rules:
     - **LZ0**: Within 5 miles of an IDA Dark Sky Sanctuary OR within 10 miles of an IDA Dark Sky Park/Reserve with no major urban centers between.
     - **LZ1**: Rural areas with intrinsically dark landscapes; no IDA proximity but population density < 100/sq mi and no significant sky glow.
     - **LZ2**: Suburban / low-density residential; population density 100-1,000/sq mi.
     - **LZ3**: Moderate brightness / commercial-industrial; population density 1,000-5,000/sq mi.
     - **LZ4**: High ambient brightness / urban core; population density > 5,000/sq mi.
  5. Cross-check with US Census Bureau population density API (US only) or WorldPop global population density raster (global) for density-based classification.
  6. If IDA proximity indicates LZ0 but density suggests LZ3+, flag for HITL review (edge case: urban area near a Dark Sky Community boundary).
- **Output:** `lighting_zone` (string LZ0-LZ4), `ida_nearest_place` (dict with name, distance, type), `zone_confidence` (float 0-1)
- **On Failure:** If IDA API is unavailable, fallback to population-density-only classification. If both fail, default to LZ2 and flag low-confidence for HITL.

### Step 3: Apply IES TM-15-11 BUG Threshold Matrix
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Load the static IES TM-15-11 BUG rating threshold matrix:

     | Zone | Max Backlight (B) | Max Uplight (U) | Max Glare (G) |
     |------|-------------------|-----------------|---------------|
     | LZ0  | B0                | U0              | G0            |
     | LZ1  | B1                | U1              | G1            |
     | LZ2  | B2                | U2              | G2            |
     | LZ3  | B3                | U2              | G3            |
     | LZ4  | B4                | U2              | G4            |

  2. For each luminaire in `validated_schedule`:
     - **Interior + emitting to exterior** (`fixture_id` in `interior_to_exterior_fixture_ids`): require `bug_uplight == 0` regardless of zone. Backlight and Glare are not evaluated for interior fixtures.
     - **Exterior**: require `bug_backlight <= zone_max_backlight` AND `bug_uplight <= zone_max_uplight` AND `bug_glare <= zone_max_glare`.
     - **Site** (parking lots, walkways, landscape): same thresholds as Exterior.
     - **Interior (not emitting to exterior)**: exempt from BUG evaluation.
  3. Flag each luminaire as `COMPLIANT`, `NON_COMPLIANT`, or `EXEMPT`.
  4. Compute compliance ratio: `%_compliant = compliant_count / (total - exempt_count)`.
- **Output:** `bug_evaluation_results` (DataFrame with per-fixture compliance status and failure reasons), `compliance_ratio` (float), `zone_thresholds` (dict)
- **On Failure:** If BUG values are missing for any non-exempt luminaire, mark as `NEEDS_DATA` and flag for HITL.

### Step 4: Verify Lighting Controls
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. For every exterior and site luminaire (excluding `emergency_fixture_ids`), verify `control_type` is NOT `manual` and NOT `none`.
  2. Acceptable controls: `motion_sensor`, `timer`, `photocell`, or any combination thereof.
  3. Validate control logic requirements:
     - **Motion sensor**: must reduce light output by ≥ 50% OR shut off within 15 minutes of no occupancy.
     - **Timer / curfew**: must shut off or reduce by ≥ 50% during non-operational hours (after `curfew_time` if provided).
     - **Photocell**: must automatically reduce output at dawn/dusk transition.
  4. If `control_type == "none"` or `"manual"` for any non-emergency exterior/site fixture, flag as `CONTROL_DEFICIENT`.
  5. Compute `control_compliance_rate`.
- **Output:** `control_evaluation_results` (DataFrame), `control_compliance_rate` (float), `deficient_fixtures` (list)
- **On Failure:** If control information is missing for >20% of exterior/site fixtures, flag for HITL data collection.

### Step 5: Calculate Exterior Lighting Power Density (ELPD)
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Sum total wattage of all exterior and site luminaires: `exterior_total_watts`.
  2. Calculate ELPD = `exterior_total_watts / site_area_sqft` (W/ft²).
  3. Compare against ASHRAE 90.1 baseline for the building type (optional sanity check; not a credit requirement but good practice for integrated design).
  4. Document the calculated value for the compliance report.
- **Output:** `elpd` (float W/ft²), `exterior_wattage_by_area` (dict)
- **On Failure:** If `site_area_sqft` is missing or `exterior_total_watts` mismatch with schedule sum, flag for HITL reconciliation.

### Step 6: HITL Checkpoint — Verify Manufacturer BUG Ratings
- **Type:** Human Review
- **Automated:** No
- **Description:**
  1. Present the reviewer with:
     - The per-fixture BUG rating summary table.
     - Hyperlinks to manufacturer cut sheets (if URLs provided in schedule; otherwise request upload).
     - List of fixtures with `NEEDS_DATA` or `NON_COMPLIANT` status.
     - The calculated lighting zone and IDA proximity results.
  2. Reviewer must:
     - Confirm BUG ratings (B/U/G) match manufacturer cut sheets for every non-exempt luminaire.
     - Approve or override the lighting zone classification.
     - Confirm control types match actual installed (or specified) systems.
     - Upload missing manufacturer cut sheets for any fixtures with unverified BUG data.
  3. Reviewer actions: `APPROVE`, `REJECT_WITH_COMMENTS`, `REQUEST_DATA`.
- **Output:** `hitl_decision` (approved / rejected / data_requested), `hitl_comments` (string), `verified_bug_data` (DataFrame with reviewer_attested flag)
- **On Failure:** If rejected, workflow pauses; user must update inputs and restart from Step 3. If data requested, workflow pauses pending upload.

### Step 7: Generate Compliance Documents
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. **Light Pollution Compliance Report (PDF)**:
     - Executive summary with project info, lighting zone, IDA proximity.
     - Detailed per-fixture compliance table (fixture ID, type, location, BUG values, zone threshold, status, control type).
     - Narrative explaining control strategy and curfew compliance.
     - ELPD calculation summary.
     - LEED v5 SSc6 requirement checklist with pass/fail per criterion.
  2. **BUG Rating Summary Table (XLSX)**:
     - Structured workbook with tabs: All Fixtures, Non-Compliant Only, Interior-Exterior, Controls Summary.
     - Conditional formatting: green = compliant, red = non-compliant, gray = exempt.
     - Includes formulas for auto-counting compliant ratios.
  3. **Luminaire Specification Compliance (PDF)**:
     - Manufacturer-level summary showing each model number, its BUG rating, and whether it meets project zone requirements.
     - Cut sheet cross-reference table with file names/URLs.
  4. All documents embed the lighting zone, IDA nearest place info, and reviewer attestation timestamp.
- **Output:** `compliance_report_pdf` (path), `bug_summary_xlsx` (path), `luminaire_spec_pdf` (path), `document_metadata` (dict)
- **On Failure:** If document generation engine fails, retry once; if persistent, queue for background generation and notify user.

### Step 8: Final Validation & Submission Packaging
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. Re-run Steps 3-5 using HITL-verified BUG data to confirm all fixtures are compliant.
  2. Compute final credit eligibility: `eligible = (compliance_ratio == 1.0) AND (control_compliance_rate == 1.0)`.
  3. If `lighting_zone == "LZ0"` and any non-exempt fixture has non-zero uplight, override to `NOT_ELIGIBLE` (zero tolerance for LZ0).
  4. Package all documents, calculation logs, and HITL attestation into a ZIP bundle formatted for LEED Online upload.
  5. Generate `submission_manifest.json` with file checksums.
- **Output:** `final_eligibility` (bool), `submission_bundle_zip` (path), `submission_manifest` (JSON)
- **On Failure:** If final compliance check fails after HITL approval (data inconsistency), raise `CriticalComplianceError` and escalate to senior reviewer.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 6: Verify Manufacturer BUG Ratings | LEED AP / Lighting Designer | 48 hours | 1. Cross-check every non-exempt luminaire's B/U/G rating against the manufacturer-provided cut sheet or LM-63/IES file. 2. Confirm lighting zone (LZ0-LZ4) is appropriate for project location and adjacent IDA Dark Sky status. 3. Verify control types (motion sensor, timer, photocell) are correctly specified and will be installed. 4. For any fixture marked NEEDS_DATA, upload cut sheet or manually enter BUG values. 5. Reject if >10% of BUG ratings cannot be verified. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| IDA Dark Sky Places | Find nearest Dark Sky Park/Reserve/Sanctuary/Community | Global | Manual web lookup at darksky.org | No rate limit (static scrape or cached API) |
| US Census Bureau TIGER/Geocoder | Population density for US projects | US only | WorldPop raster API | 100 requests/min |
| WorldPop (University of Southampton) | Global population density raster | Global | Manual classification via project description | 50 requests/min |
| Nominatim (OpenStreetMap) | Geocode project address to lat/lon | Global | Google Maps Geocoding API (if API key configured) | 1 request/sec |
| Manufacturer APIs (e.g., Acuity Brands, Signify, Cooper Lighting) | Fetch BUG ratings by model number | Global (varies by manufacturer) | Manual cut sheet upload | Varies |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | Full IDA + Census density + all manufacturer APIs |
| Canada | Available | IDA + Nominatim geocoding; Census fallback to Statistics Canada |
| Europe | Available | IDA + WorldPop density; manufacturer APIs active |
| Australia / New Zealand | Available | IDA + WorldPop; strong local dark sky advocacy data |
| Asia-Pacific | Available | IDA + WorldPop; some manufacturer API latency |
| Middle East / Africa | Limited | IDA coverage sparse; WorldPop density available; rely on manual LZ classification |
| South America | Available | IDA + WorldPop; growing Dark Sky Place network |
| Global Remote / Off-Grid | Limited | No density data; manual LZ0-LZ1 classification recommended |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Invalid luminaire schedule format | Reject upload, return specific column error | Yes (immediate) | N/A — user must re-upload |
| Missing BUG rating for non-exempt fixture | Mark fixture as NEEDS_DATA, flag HITL | Yes (via HITL queue) | N/A — requires human data entry |
| IDA API unreachable | Fallback to population density classification | No (silent fallback) | 3 retries with 5s backoff |
| Population density API failure | Default to LZ2, flag low-confidence | Yes (digest) | 2 retries |
| Geocoding failure | Request manual lat/lon entry | Yes (immediate) | 2 retries with alternate provider |
| Manufacturer API timeout for BUG data | Queue for background fetch | No | 3 retries with 10s backoff |
| HITL rejection | Pause workflow, notify project team | Yes (immediate) | N/A — requires resubmission |
| Document generation failure | Retry once, then background queue | Yes (if persistent) | 1 immediate retry |
| LZ0 proximity conflict (urban near IDA boundary) | Flag for mandatory HITL review | Yes (immediate) | N/A |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Light Pollution Compliance Report | PDF | Executive narrative + per-fixture compliance table + control strategy summary + LEED v5 SSc6 checklist |
| BUG Rating Summary Table | XLSX | Multi-tab workbook with all fixtures, non-compliant subset, interior-exterior breakdown, and control summary with conditional formatting |
| Luminaire Specification Compliance | PDF | Manufacturer-level BUG rating verification with cut sheet cross-references and model number compliance matrix |
| Submission Bundle | ZIP | Combined package of all PDFs/XLSX + `submission_manifest.json` + calculation audit log, ready for LEED Online upload |

## Testing
```bash
# Run unit tests for SSc6 skill
python -m pytest skills/ss-c6/tests/

# Key test modules:
# - test_input_validation.py     : Validates schedule parsing and geocoding
# - test_zone_classification.py  : Tests IDA proximity + density-based LZ logic
# - test_bug_thresholds.py       : Tests IES TM-15-11 matrix application per zone
# - test_control_verification.py : Tests motion sensor / timer / photocell compliance
# - test_document_generation.py : Tests PDF/XLSX output correctness
# - test_hitl_integration.py     : Tests checkpoint state persistence and resume
```

## Example Usage (Deer-Flow)
```python
from deerflow.skills import LEEDSsC6LightPollutionSkill

skill = LEEDSsC6LightPollutionSkill(
    project_id="proj-12345",
    inputs={
        "luminaire_schedule": "/uploads/fixture_schedule.xlsx",
        "project_lat": 34.0522,
        "project_lon": -118.2437,
        "project_address": "Los Angeles, CA",
        "exterior_total_watts": 12500.0,
        "site_area_sqft": 150000.0,
        "operational_hours": "06:00-22:00",
        "curfew_time": "22:00",
        "emergency_fixture_ids": ["EM-01", "EM-02"],
        "interior_to_exterior_fixture_ids": ["IF-LOBBY-01", "IF-ATRIUM-03"]
    }
)

result = await skill.execute()

# result contains:
# {
#   "final_eligibility": True,
#   "lighting_zone": "LZ3",
#   "ida_nearest_place": {"name": "Joshua Tree National Park", "distance_miles": 125.4, "type": "Dark Sky Park"},
#   "compliance_ratio": 1.0,
#   "control_compliance_rate": 1.0,
#   "elpd_w_per_sqft": 0.083,
#   "documents": {
#       "compliance_report_pdf": "/output/ss-c6/proj-12345_compliance_report.pdf",
#       "bug_summary_xlsx": "/output/ss-c6/proj-12345_bug_summary.xlsx",
#       "luminaire_spec_pdf": "/output/ss-c6/proj-12345_luminaire_spec.pdf",
#       "submission_bundle_zip": "/output/ss-c6/proj-12345_submission.zip"
#   },
#   "hitl_status": "approved",
#   "submission_manifest": {...}
# }
```

## Deer-Flow Workflow (LangGraph)
```python
from langgraph.graph import StateGraph, END
from deerflow.skills.leed_ss_c6.types import SSc6State

# Define nodes
workflow = StateGraph(SSc6State)

workflow.add_node("validate_inputs", validate_luminaire_schedule)
workflow.add_node("determine_zone", classify_lighting_zone)
workflow.add_node("apply_bug_matrix", evaluate_bug_thresholds)
workflow.add_node("verify_controls", evaluate_lighting_controls)
workflow.add_node("calculate_elpd", compute_exterior_power_density)
workflow.add_node("hitl_review", human_review_checkpoint)   # HITL gate
workflow.add_node("generate_docs", generate_compliance_documents)
workflow.add_node("final_check", final_compliance_validation)

# Define edges
workflow.set_entry_point("validate_inputs")
workflow.add_edge("validate_inputs", "determine_zone")
workflow.add_edge("determine_zone", "apply_bug_matrix")
workflow.add_edge("apply_bug_matrix", "verify_controls")
workflow.add_edge("verify_controls", "calculate_elpd")
workflow.add_edge("calculate_elpd", "hitl_review")

# HITL branching
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: state["hitl_decision"],
    {
        "approved": "generate_docs",
        "rejected": END,          # Workflow halts; user restarts
        "data_requested": END       # Workflow pauses pending data upload
    }
)

workflow.add_edge("generate_docs", "final_check")
workflow.add_conditional_edges(
    "final_check",
    lambda state: "pass" if state["final_eligibility"] else "fail",
    {
        "pass": END,
        "fail": END               # Returns failure report with remediation actions
    }
)

# Compile
app = workflow.compile()

# Execute
final_state = app.invoke({
    "project_id": "proj-12345",
    "inputs": {...},
    "validated_schedule": None,
    "lighting_zone": None,
    "bug_results": None,
    "control_results": None,
    "elpd": None,
    "hitl_decision": None,
    "hitl_comments": None,
    "documents": None,
    "final_eligibility": None,
    "submission_manifest": None
})
```

---

### Appendix A: IES TM-15-11 BUG Rating Quick Reference

The Backlight-Uplight-Glare (BUG) rating system assigns each luminaire an integer rating from 0 (best) to 5 (worst) for each of the three components. The rating depends on the luminaire's luminous intensity distribution, mounting height, and light output.

**BUG Rating Sources:**
- Manufacturer-provided BUG ratings (preferred).
- `.ies` photometric file analysis via lighting software (e.g., AGi32, Dialux, Relux).
- IES TM-15-11 calculation methodology (internal tool).

**Zone Threshold Summary for SSc6:**

| Zone | Typical Setting | Max Backlight | Max Uplight | Max Glare | Use Case |
|------|----------------|---------------|-------------|-----------|----------|
| LZ0 | IDA Dark Sky Sanctuary core | B0 | U0 | G0 | Astronomy sites, wilderness |
| LZ1 | Rural, intrinsically dark | B1 | U1 | G1 | Rural residential, parks |
| LZ2 | Suburban, low density | B2 | U2 | G2 | Residential, light commercial |
| LZ3 | Urban, moderate brightness | B3 | U2 | G3 | Commercial, industrial |
| LZ4 | Urban core, high brightness | B4 | U2 | G4 | Downtown, high-rise districts |

*Note: Glare (G) is evaluated but is typically a recommendation; the LEED v5 SSc6 hard requirements focus on Backlight and Uplight compliance.*

### Appendix B: Control Type Definitions

| Control Type | Requirement | LEED v5 SSc6 Compliance |
|--------------|-------------|------------------------|
| Motion sensor | ≥ 50% reduction or full shutoff within 15 min of vacancy | Compliant |
| Timer (curfew) | Automatic shutoff or ≥ 50% dimming after operational hours | Compliant |
| Photocell | Automatic output adjustment based on ambient light | Compliant (must supplement with timer or motion sensor) |
| Manual switch | No automatic reduction | **Non-compliant** |
| None | Always on at full output | **Non-compliant** |
| Combined (e.g., photocell + timer) | Meets most stringent individual requirement | Compliant |

### Appendix C: IDA Dark Sky Place Types

| Type | Description | LZ Implication |
|------|-------------|--------------|
| International Dark Sky Sanctuary | Most remote, darkest sites | Usually triggers LZ0 within 5 miles |
| International Dark Sky Park | Publicly accessible protected areas | May trigger LZ0 within 10 miles if no urban buffer |
| International Dark Sky Reserve | Large, dark core + buffer zone | Core = LZ0, buffer = LZ1 |
| Urban Night Sky Place | Dark sky area within/ adjacent to urban environment | Typically LZ2-LZ3; does not trigger LZ0 |
| Dark Sky Community | Municipality with outdoor lighting ordinance | Adjacent projects may be LZ1-LZ2 |
