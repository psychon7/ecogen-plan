name: leed-ea-c3-energy-enhanced
version: 1.0.0
author: LEED Automation Platform
description: Automates LEED v5 EAc3 Enhanced Energy Efficiency documentation from energy model outputs, including points calculation, narrative generation, and supporting summary reports.

## Metadata
- **Credit Code:** EAc3
- **Credit Name:** Enhanced Energy Efficiency
- **Points:** Up to 10 points (New Construction) / 7 points (Core and Shell)
- **Automation Level:** 87.7%
- **Complexity:** Medium-High
- **Primary Data Source:** EnergyPlus/Eppy model output parser, ASHRAE 90.1-2022 Appendix G static reference tables
- **HITL Required:** Yes

## Purpose
Automates the generation of LEED v5 EAc3 Enhanced Energy Efficiency documentation—including points calculation, narrative reports, and supporting energy model summaries—from externally-produced energy model output files, while requiring human verification of the improvement percentage and points award.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| project_id | string | Project database | UUIDv4 format, exists in LEED project registry |
| building_type | enum | User input | One of: "new_construction", "core_and_shell" |
| climate_zone | string | User input | ASHRAE 90.1-2022 climate zone (e.g., "4A", "5B") |
| baseline_model_path | path | Energy modeler upload | Valid .idf or .osm file; EnergyPlus-compatible |
| proposed_model_path | path | Energy modeler upload | Valid .idf or .osm file; EnergyPlus-compatible |
| baseline_results_dir | path | Energy modeler upload | Directory containing .eso, .mtr, .htm output files |
| proposed_results_dir | path | Energy modeler upload | Directory containing .eso, .mtr, .htm output files |
| modeler_improvement_pct | float | Energy modeler input | Range 0.0–100.0; baseline vs. proposed annual energy |
| total_building_area_m2 | float | Project database | > 0 |
| simulation_software | enum | User input | One of: "energyplus", "equest", "trace", "iesve", "carmel" |
| points_target | int | User input | 1–10 for NC, 1–7 for C&S; optional optimization flag |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| baseline_fuel_mix | dict | {} | Mapping of fuel type to annual consumption (kWh or therm) for custom baseline |
| electricity_rate | float | 0.12 | $/kWh for cost savings estimate |
| gas_rate | float | 1.20 | $/therm for cost savings estimate |
| water_heating_included | bool | true | Whether water heating energy is included in model outputs |
| renewable_energy_offset | float | 0.0 | On-site renewable energy production (MWh/yr) to subtract from proposed |
| include_cost_savings | bool | true | Whether to generate cost savings estimate in narrative |
| narrative_template | string | "default" | Template variant for narrative document |
| hitl_modeler_email | string | project.lead@example.com | Email for HITL Checkpoint 1 |
| hitl_leed_consultant_email | string | leed.consultant@example.com | Email for HITL Checkpoint 2 |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:** Validate all required input fields against schema. Check file existence and format for model result directories. Verify building_type matches supported NC/C&S. Confirm climate_zone against ASHRAE 90.1-2022 valid zones. Validate simulation_software against supported parser backends. Check that baseline and proposed results directories contain expected EnergyPlus output file extensions (.eso, .mtr, .htm, .csv, .err). Compute MD5 hashes of input directories for audit trail.
- **Output:** `ValidationReport` object with `valid: bool`, `errors: list[str]`, `checksums: dict`
- **On Failure:** Halt workflow; return validation errors to caller; notify project administrator via email.

### Step 2: Parse Energy Model Outputs
- **Type:** API Call
- **Automated:** Yes
- **Description:** Use Eppy (EnergyPlus Python interface) or vendor-specific parser to extract annual site energy consumption from baseline and proposed model outputs. Parse `.eso` (Output:Variable), `.mtr` (meter data), and `eplusout.htm` (HTML summary) files. Extract total annual energy (kWh/yr) by fuel type (electricity, natural gas, district heating, district cooling). Aggregate into total annual site energy. For eQuest/TRACE/IES-VE, use adapter layer (`equest_parser.py`, `trace_parser.py`, `iesve_parser.py`) to normalize into common schema: `{annual_electricity_kwh, annual_gas_therms, annual_district_heating_kwh, annual_district_cooling_kwh, total_site_energy_kwh, source_energy_kwh, peak_demand_kw}`.
- **Output:** `NormalizedEnergyData` object for both baseline and proposed
- **On Failure:** Log parser error details; fallback to manual upload form for CSV energy summary; trigger HITL Checkpoint 1 early.

### Step 3: Compute Improvement Percentage
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Calculate percentage energy improvement using ASHRAE 90.1-2022 Appendix G methodology: `% Improvement = (Baseline_Energy_kWh - Proposed_Energy_kWh) / Baseline_Energy_kWh * 100`. If `renewable_energy_offset > 0`, subtract from proposed before calculation. Apply ASHRAE 90.1-2022 mandatory adjustments if present (e.g., baseline unregulated load adjustment per Table G3.1 #17). Round to 2 decimal places. Cross-check against `modeler_improvement_pct` provided by energy modeler; flag if discrepancy > 0.5 percentage points.
- **Output:** `ImprovementResult` object with `pct_improvement`, `baseline_kwh`, `proposed_kwh`, `delta_kwh`, `modeler_discrepancy_flag`
- **On Failure:** Log calculation error; trigger HITL Checkpoint 1 with discrepancy alert.

### Step 4: Determine Points Award
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Map computed `% Improvement` to LEED v5 points using the published EAc3 points table (New Construction vs. Core and Shell). NC scale: 1 pt @ 5%, 2 @ 10%, 3 @ 15%, 4 @ 20%, 5 @ 25%, 6 @ 30%, 7 @ 35%, 8 @ 40%, 9 @ 45%, 10 @ 50%. C&S scale: 1 pt @ 3%, 2 @ 6%, 3 @ 9%, 4 @ 12%, 5 @ 15%, 6 @ 20%, 7 @ 25%. Interpolate linearly between thresholds (LEED v5 allows fractional thresholds; round down to nearest whole point). Compare against `points_target`; generate optimization gap analysis if target not met.
- **Output:** `PointsAward` object with `points_achieved`, `points_target`, `gap_to_next_point`, `pct_for_next_point`
- **On Failure:** Log mapping error; trigger HITL Checkpoint 2 with raw data.

### Step 5: HITL Checkpoint 1 — Energy Modeler Verification
- **Type:** Human Review
- **Automated:** No
- **Description:** Present computed `pct_improvement`, parsed energy breakdowns (baseline vs. proposed by end use: HVAC, lighting, water heating, plug loads, fans, pumps), and discrepancy flag to energy modeler. Modeler reviews parsed data for accuracy, confirms or corrects the improvement percentage, and approves proceeding. Modeler may upload corrected CSV summary if parser output is incorrect.
- **Output:** `ModelerApproval` object with `approved: bool`, `corrected_pct_improvement: float | null`, `notes: str`
- **On Failure:** Workflow paused; reminder sent at 24h and 48h; auto-escalate to project lead at 72h.

### Step 6: Compute Cost Savings Estimate (Optional)
- **Type:** Calculation
- **Automated:** Yes
- **Description:** If `include_cost_savings=True`, estimate annual cost savings: `Savings = (Baseline_kWh - Proposed_kWh) * blended_rate`. Blended rate computed from fuel mix and provided `electricity_rate`/`gas_rate`. Convert gas from therms to kWh equivalent (1 therm = 29.3071 kWh) for unified calculation. Compute simple payback if project cost data available via `project_id` lookup. Include 10-year NPV at 3% discount rate.
- **Output:** `CostSavingsEstimate` object with `annual_savings_usd`, `ten_year_npv_usd`, `payback_years`
- **On Failure:** Log error; skip cost section in narrative; continue workflow.

### Step 7: Generate Supporting Energy Model Summary
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generate PDF report containing: (a) project metadata, (b) simulation software and version, (c) climate zone and weather file, (d) baseline vs. proposed annual energy by fuel type and end use, (e) improvement percentage calculation with formula, (f) ASHRAE 90.1-2022 Appendix G compliance statement, (g) modeler sign-off block. Use WeasyPrint or ReportLab for PDF generation from Jinja2 HTML template. Embed parsed data tables and bar chart visualizations (matplotlib generated, embedded as base64 PNG).
- **Output:** `energy_model_summary.pdf` file path
- **On Failure:** Retry once with simplified template (no charts); if still failing, trigger HITL Checkpoint 2 with raw data payload.

### Step 8: Generate Points Calculation Table
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generate Excel (.xlsx) workbook with: Sheet 1 — Points calculation with building type, climate zone, baseline/proposed energy, improvement %, points achieved, points target, gap analysis; Sheet 2 — LEED v5 EAc3 points lookup table for reference; Sheet 3 — End-use energy breakdown (if available from parser); Sheet 4 — Fuel-type comparison. Format with conditional formatting (green for achieved, yellow for within 2% of next threshold, red for gap > 10%). Include data validation dropdowns and formula references.
- **Output:** `points_calculation.xlsx` file path
- **On Failure:** Retry once; if failing, generate CSV fallback and trigger HITL Checkpoint 2.

### Step 9: Generate Enhanced Energy Efficiency Narrative
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generate PDF narrative document for LEED submission including: executive summary, project description, energy modeling approach summary, ASHRAE 90.1-2022 baseline description, proposed design energy features summary, improvement percentage with calculation methodology, points achieved with reference to LEED v5 table, cost savings estimate (optional), supporting documentation index, and modeler/LEED consultant attestation placeholders. Use Jinja2 HTML template → WeasyPrint PDF pipeline. Include project logo, formatted tables, and chart embeds.
- **Output:** `enhanced_energy_efficiency_narrative.pdf` file path
- **On Failure:** Retry once with simplified template; if still failing, trigger HITL Checkpoint 2 with draft Markdown.

### Step 10: HITL Checkpoint 2 — LEED Consultant Confirmation
- **Type:** Human Review
- **Automated:** No
- **Description:** Present all three output documents (narrative PDF, points table XLSX, model summary PDF) to LEED consultant. Consultant reviews points calculation accuracy, verifies narrative completeness against LEED v5 EAc3 documentation requirements, confirms all required supporting data is included, and approves final submission package. Consultant may request revisions with inline comments.
- **Output:** `ConsultantApproval` object with `approved: bool`, `revision_requests: list[str]`, `notes: str`
- **On Failure:** Workflow paused; if revision requests provided, route back to Step 7/8/9 with requested changes; if no response in 48h, escalate.

### Step 11: Finalize and Package Deliverables
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Upon HITL Checkpoint 2 approval, apply consultant revisions if any. Finalize all PDFs with version numbers, timestamps, and digital checksums. Bundle into ZIP archive with manifest.json listing all files, their MD5 hashes, and generation timestamps. Upload to project document store with metadata tags: `leed_v5`, `eac3`, `energy_efficiency`, `submission_package`. Generate cover sheet with project info, credit code, and submission date.
- **Output:** `eac3_submission_package.zip` containing all final documents + manifest
- **On Failure:** Log packaging error; return individual file paths to caller.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 5: Modeler Verification | Energy Modeler (MEP Engineer) | 48 hours | Verify parsed energy consumption values match your simulation results. Confirm or correct the calculated improvement percentage. Check that baseline/proposed fuel breakdowns are accurate. Approve or request parser correction. |
| Step 10: LEED Consultant Confirmation | LEED Consultant / Project Lead | 48 hours | Review final narrative for completeness against LEED v5 EAc3 requirements. Verify points calculation matches LEED v5 points table. Confirm all supporting model summary data is present. Check narrative formatting and project-specific accuracy. Approve for submission or request revisions. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| EnergyPlus / Eppy | Parse .eso, .mtr, .htm output files | Global | Manual CSV upload form | N/A (local execution) |
| eQuest Parser (custom) | Parse eQuest simulation reports | Global | Manual CSV upload form | N/A (local execution) |
| TRACE Parser (custom) | Parse TRACE 700/3D Plus outputs | Global | Manual CSV upload form | N/A (local execution) |
| IES-VE Parser (custom) | Parse ApacheSim/VE results | Global | Manual CSV upload form | N/A (local execution) |
| ASHRAE 90.1-2022 Reference | Static lookup tables for baseline rules, climate zones, points methodology | Global | Local cached JSON copy | N/A (static data) |
| WeasyPrint / ReportLab | PDF document generation | Global | wkhtmltopdf / PDFKit | N/A (local execution) |
| OpenPyXL | Excel (.xlsx) generation | Global | CSV export | N/A (local execution) |
| Matplotlib | Chart generation for PDF embeds | Global | Skip charts, table-only output | N/A (local execution) |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| North America | Available | Full support; ASHRAE 90.1-2022 is regional standard |
| Europe | Available | Works with CEN/ISO energy models; may require climate zone mapping |
| Asia-Pacific | Available | Works with local simulation tools (e.g., DeST, EnergyPlus); climate zone mapping provided |
| Middle East | Available | Works with EnergyPlus/IES-VE; hot-arid climate zones supported |
| Latin America | Available | Works with EnergyPlus/eQuest; climate zone mapping provided |
| Africa | Available | Works with EnergyPlus; limited eQuest/TRACE support due to climate data |
| Global | Available | EnergyPlus is open-source and global; vendor-specific parsers may need local validation |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Invalid input schema | Halt workflow; return error details | Yes (project admin) | No |
| Missing model result files | Halt workflow; request file upload | Yes (energy modeler) | No |
| EnergyPlus parser failure | Switch to manual CSV upload; trigger HITL 1 | Yes (energy modeler) | 1x with fallback parser |
| eQuest/TRACE/IES parser failure | Switch to manual CSV upload; trigger HITL 1 | Yes (energy modeler) | 1x with simplified parser |
| % improvement discrepancy > 0.5% | Flag in HITL 1; require modeler resolution | Yes (energy modeler) | No |
| Points calculation out of range | Log warning; cap at max points; flag in HITL 2 | Yes (LEED consultant) | No |
| PDF generation failure | Retry with simplified template | Yes (project admin) | 1x |
| Excel generation failure | Fallback to CSV | Yes (project admin) | 1x |
| HITL 1 timeout (>48h) | Escalate to project lead; reminder at 24h/48h | Yes (project lead) | N/A |
| HITL 2 timeout (>48h) | Escalate to project lead; reminder at 24h/48h | Yes (project lead) | N/A |
| Cost savings calculation failure | Skip section; log warning; continue | No | 1x |
| ASHRAE 90.1 reference data missing | Use local cached JSON fallback | No | N/A |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Enhanced Energy Efficiency Narrative | PDF | Primary LEED submission narrative with project description, modeling approach, improvement calculation, points achieved, cost savings (optional), and attestation placeholders |
| Points Calculation Table | XLSX | Detailed points calculation workbook with lookup tables, end-use breakdowns, fuel comparisons, and conditional formatting |
| Supporting Energy Model Summary | PDF | Technical summary of baseline vs. proposed model results with energy breakdowns, charts, and modeler sign-off block |
| Submission Package Manifest | JSON | Machine-readable manifest with file list, checksums, timestamps, and metadata |
| Submission Package Archive | ZIP | Final bundled package containing all documents, manifest, and cover sheet |

## Testing
```bash
# Run all unit and integration tests for EAc3 skill
python -m pytest skills/leed-ea-c3-energy-enhanced/tests/ -v --tb=short

# Specific test suites
python -m pytest skills/leed-ea-c3-energy-enhanced/tests/test_input_validation.py
python -m pytest skills/leed-ea-c3-energy-enhanced/tests/test_energyplus_parser.py
python -m pytest skills/leed-ea-c3-energy-enhanced/tests/test_improvement_calculation.py
python -m pytest skills/leed-ea-c3-energy-enhanced/tests/test_points_mapping.py
python -m pytest skills/leed-ea-c3-energy-enhanced/tests/test_document_generation.py
python -m pytest skills/leed-ea-c3-energy-enhanced/tests/test_hitl_workflow.py
python -m pytest skills/leed-ea-c3-energy-enhanced/tests/test_end_to_end.py
```

## Example Usage (Deer-Flow)
```python
from deerflow.skills import EAc3EnergyEnhancedSkill

skill = EAc3EnergyEnhancedSkill(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    inputs={
        "building_type": "new_construction",
        "climate_zone": "4A",
        "baseline_model_path": "/uploads/proj_baseline.idf",
        "proposed_model_path": "/uploads/proj_proposed.idf",
        "baseline_results_dir": "/uploads/baseline_results/",
        "proposed_results_dir": "/uploads/proposed_results/",
        "modeler_improvement_pct": 32.5,
        "total_building_area_m2": 15000.0,
        "simulation_software": "energyplus",
        "points_target": 7,
        "electricity_rate": 0.14,
        "gas_rate": 1.35,
        "include_cost_savings": True,
        "renewable_energy_offset": 120.0,
        "hitl_modeler_email": "mep.engineer@designfirm.com",
        "hitl_leed_consultant_email": "leed.ap@consultingfirm.com"
    }
)

# Execute the full workflow (includes HITL checkpoints via state graph)
result = await skill.execute()

# Access outputs
print(f"Points Achieved: {result.points_achieved}")
print(f"Improvement: {result.pct_improvement}%")
print(f"Narrative PDF: {result.documents.narrative_pdf}")
print(f"Points Table: {result.documents.points_xlsx}")
print(f"Model Summary: {result.documents.model_summary_pdf}")
print(f"Submission Package: {result.documents.submission_zip}")
```

## Deer-Flow Workflow (LangGraph)
```python
from langgraph.graph import StateGraph, END
from deerflow.skills.leed_ea_c3.states import EAc3State
from deerflow.skills.leed_ea_c3.nodes import (
    validate_inputs,
    parse_energy_model_outputs,
    compute_improvement_percentage,
    determine_points_award,
    hitl_modeler_verification,
    compute_cost_savings,
    generate_model_summary_pdf,
    generate_points_table_xlsx,
    generate_narrative_pdf,
    hitl_leed_consultant_confirmation,
    finalize_submission_package
)
from deerflow.skills.leed_ea_c3.conditional_edges import (
    route_after_validation,
    route_after_parser,
    route_after_improvement,
    route_after_points,
    route_after_hitl1,
    route_after_cost,
    route_after_docs,
    route_after_hitl2
)

# Define the LangGraph workflow
workflow = StateGraph(EAc3State)

# Add all nodes
workflow.add_node("validate", validate_inputs)
workflow.add_node("parse_baseline", parse_energy_model_outputs)
workflow.add_node("parse_proposed", parse_energy_model_outputs)
workflow.add_node("compute_improvement", compute_improvement_percentage)
workflow.add_node("determine_points", determine_points_award)
workflow.add_node("hitl_modeler", hitl_modeler_verification)
workflow.add_node("cost_savings", compute_cost_savings)
workflow.add_node("gen_model_summary", generate_model_summary_pdf)
workflow.add_node("gen_points_table", generate_points_table_xlsx)
workflow.add_node("gen_narrative", generate_narrative_pdf)
workflow.add_node("hitl_consultant", hitl_leed_consultant_confirmation)
workflow.add_node("finalize", finalize_submission_package)

# Define edges
workflow.set_entry_point("validate")
workflow.add_conditional_edges("validate", route_after_validation)
workflow.add_conditional_edges("parse_baseline", route_after_parser)
workflow.add_conditional_edges("parse_proposed", route_after_parser)
workflow.add_conditional_edges("compute_improvement", route_after_improvement)
workflow.add_conditional_edges("determine_points", route_after_points)
workflow.add_conditional_edges("hitl_modeler", route_after_hitl1)
workflow.add_conditional_edges("cost_savings", route_after_cost)
workflow.add_conditional_edges("gen_model_summary", route_after_docs)
workflow.add_conditional_edges("gen_points_table", route_after_docs)
workflow.add_conditional_edges("gen_narrative", route_after_docs)
workflow.add_conditional_edges("hitl_consultant", route_after_hitl2)
workflow.add_edge("finalize", END)

# Compile the graph
app = workflow.compile()

# Execute with streaming (for HITL checkpoint visibility)
async for event in app.astream(initial_state, stream_mode="values"):
    if event.get("hitl_checkpoint"):
        print(f"HITL Checkpoint reached: {event['hitl_checkpoint']}")
        print(f"Pending reviewer: {event['pending_reviewer']}")
        print(f"SLA deadline: {event['sla_deadline']}")
```

## Additional Implementation Notes

### Parser Architecture
The skill uses a pluggable parser architecture:
- `BaseEnergyParser` abstract class defining `parse_results_dir(dir_path: Path) -> NormalizedEnergyData`
- `EnergyPlusParser` — uses `eppy` + `pyenergibridge` for .eso/.mtr parsing
- `EQuestParser` — reads `.psr` (parametric summary report) and `.sim` files
- `TraceParser` — reads TRACE 700 `.pdf` exports or `.csv` exports via `camelot-py`
- `IESVEParser` — reads ApacheSim tabular report XML exports

All parsers normalize to a common `NormalizedEnergyData` Pydantic model with fields:
- `annual_site_energy_kwh: float`
- `annual_source_energy_kwh: float`
- `fuel_breakdown: dict[FuelType, float]`
- `end_use_breakdown: dict[EndUse, float] | None`
- `peak_demand_kw: float | None`
- `simulation_software: str`
- `software_version: str | None`

### Points Mapping (LEED v5 EAc3)
```python
POINTS_TABLE_NC = {
    5.0: 1, 10.0: 2, 15.0: 3, 20.0: 4, 25.0: 5,
    30.0: 6, 35.0: 7, 40.0: 8, 45.0: 9, 50.0: 10
}
POINTS_TABLE_CS = {
    3.0: 1, 6.0: 2, 9.0: 3, 12.0: 4, 15.0: 5,
    20.0: 6, 25.0: 7
}

def map_points(pct_improvement: float, building_type: str) -> int:
    table = POINTS_TABLE_NC if building_type == "new_construction" else POINTS_TABLE_CS
    points = 0
    for threshold, pt in sorted(table.items()):
        if pct_improvement >= threshold:
            points = pt
    return points
```

### HITL Integration Pattern
HITL checkpoints use Deer-Flow's `HumanReviewNode`:
- State persists in PostgreSQL with `checkpoint_id` (UUID)
- Email notification sent via SendGrid / AWS SES with secure review link
- Reviewer interface renders parsed data + computed results inline
- Approval/rejection writes back to state graph via callback webhook
- SLA monitoring via Celery beat scheduler; escalation rules configurable per project

### Cost Savings Formula
```python
def compute_cost_savings(baseline: NormalizedEnergyData, proposed: NormalizedEnergyData, 
                         electricity_rate: float, gas_rate: float) -> CostSavingsEstimate:
    elec_delta = baseline.fuel_breakdown.get("electricity", 0) - proposed.fuel_breakdown.get("electricity", 0)
    gas_delta = baseline.fuel_breakdown.get("natural_gas", 0) - proposed.fuel_breakdown.get("natural_gas", 0)
    annual_savings = (elec_delta * electricity_rate) + (gas_delta * gas_rate)
    ten_year_npv = sum([annual_savings / (1.03 ** year) for year in range(1, 11)])
    return CostSavingsEstimate(annual_savings_usd=annual_savings, ten_year_npv_usd=ten_year_npv)
```

### File Structure
```
skills/leed-ea-c3-energy-enhanced/
├── SKILL.md                          # This file
├── __init__.py
├── state.py                          # EAc3State Pydantic model
├── nodes/
│   ├── __init__.py
│   ├── validate_inputs.py
│   ├── parse_outputs.py
│   ├── compute_improvement.py
│   ├── determine_points.py
│   ├── compute_cost_savings.py
│   ├── generate_documents.py
│   └── finalize_package.py
├── parsers/
│   ├── __init__.py
│   ├── base.py
│   ├── energyplus.py
│   ├── equest.py
│   ├── trace.py
│   └── iesve.py
├── templates/
│   ├── narrative_default.html
│   ├── narrative_cs_variant.html
│   ├── model_summary.html
│   └── styles.css
├── tests/
│   ├── __init__.py
│   ├── test_input_validation.py
│   ├── test_energyplus_parser.py
│   ├── test_improvement_calculation.py
│   ├── test_points_mapping.py
│   ├── test_document_generation.py
│   ├── test_hitl_workflow.py
│   ├── test_end_to_end.py
│   └── fixtures/
│       ├── baseline_results/
│       ├── proposed_results/
│       └── expected_outputs/
├── data/
│   └── ashrae_90_1_2022_reference.json
└── config.yaml
```
