---
name: leed-mr-p2-embodied-carbon
version: 1.0.0
author: LEED Automation Platform
description: Automate EPD parsing, material matching, and LEED submission document generation for MRp2 embodied carbon prerequisite.
---

## Metadata
- **Credit Code:** MRp2
- **Credit Name:** Quantify and Assess Embodied Carbon
- **Points:** Required (Prerequisite)
- **Automation Level:** 87.0%
- **Complexity:** Medium
- **Primary Data Source:** EC3 Database, EPD Registry, CLF Material Baselines
- **HITL Required:** Yes

## Purpose
Automate EPD parsing, material-to-GWP matching, baseline comparison against CLF baselines, and LEED submission document generation for MRp2, while strictly operating outside the whole-building LCA calculation boundary and accepting outputs from tools such as Tally or One Click LCA.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `project_id` | string | platform project metadata | UUIDv4 format, non-null |
| `material_takeoff` | File (CSV/XLSX) | User upload | Required columns: `material_name`, `material_category`, `quantity`, `unit`, `location_in_building`. Non-empty file, >0 rows. |
| `building_area` | number | User input | >0; accepts sq ft or sq m; validated against project metadata |
| `service_life` | integer | User input or project defaults | >= 60 years (typical reference study period); range 30-100 |
| `lca_software` | enum | User selection | One of: `Tally`, `One_Click_LCA`, `Other` |
| `structural_systems_included` | boolean | User confirmation | Must be `true` for credit compliance |
| `enclosure_systems_included` | boolean | User confirmation | Must be `true` for credit compliance |
| `assessment_standard` | enum | User selection | One of: `ISO_21930`, `EN_15804`, `ISO_14040_14044` |
| `building_type` | enum | User input or project metadata | One of: `commercial`, `residential`, `healthcare`, `education`, `industrial`, `mixed_use` |
| `region_code` | string | User input or project metadata | ISO 3166-1 alpha-2 country code; determines CLF baseline region |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `lca_tool_output` | File (CSV/JSON/XLSX) | null | Whole-building LCA output from Tally/One Click LCA for cross-check validation. **Not required for primary calculation.** |
| `uploaded_epds` | File[] (PDF/XML) | [] | Project-specific EPDs already procured by the project team |
| `project_epd_registry_ids` | string[] | [] | EPD Registry UUIDs for materials with known registry entries |
| `clf_baseline_year` | integer | Current year - 1 | Year of CLF baseline to compare against (e.g., 2023) |
| `functional_unit_override` | string | `1 m2 of building area per year` | Overrides default functional unit for GWP intensity calculation |
| `system_boundary` | enum | `A-C (cradle-to-grave)` | One of: `A-C`, `A-D`, `A1-A3` (modules per ISO 21930/EN 15804) |
| `excluded_materials` | string[] | [] | Material categories explicitly excluded from takeoff (documented for transparency) |
| `include_mep` | boolean | false | Include mechanical/electrical/plumbing systems in assessment (not required by credit) |
| `include_interiors` | boolean | false | Include interior nonstructural systems in assessment (not required by credit) |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. Parse `material_takeoff` file and validate schema (required columns present, no nulls in key fields, numeric quantities).
  2. Validate `building_area` > 0 and normalize to metric (sq m) using conversion factor 0.092903 for sq ft inputs.
  3. Confirm `structural_systems_included` and `enclosure_systems_included` are both `true`; if either is `false`, abort with compliance error.
  4. Validate `assessment_standard` is one of permitted ISO/EN standards.
  5. Check `lca_software` is declared; if `Other`, flag for manual tool verification in HITL.
  6. Detect duplicate material entries and flag for consolidation.
  7. Verify `material_category` values map to a controlled vocabulary (Concrete, Steel, Wood, Masonry, Glass, Insulation, Roofing, Other). Unmapped categories trigger HITL.
- **Output:** `ValidationResult` object: `{ valid: bool, errors: [], warnings: [], normalized_takeoff: DataFrame }`
- **On Failure:** Return `ValidationError` to user with specific row-level issues; retry allowed after user correction.

### Step 2: Parse EPDs and Extract GWP Data
- **Type:** API Call / Document Parsing
- **Automated:** Yes
- **Description:**
  1. **Uploaded EPDs:** Iterate `uploaded_epds`. For each PDF, use PDF extraction pipeline (PyPDF2 + OCR fallback) to extract declared unit, GWP-A1A3 (kg CO2e per declared unit), GWP-total (A-C or A-D), product description, manufacturer, EPD validity date, and program operator.
  2. **XML EPDs (ILCD+EPD / EPDx):** If XML format detected, parse via `xml.etree.ElementTree` for structured extraction of `LCIAResult` elements for GWP (GWP-GWP100, GWP-GWP20 where available).
  3. **EPD Registry API:** For each material without uploaded EPD, call `GET https://api.theepdregistry.com/v1/epds/search?q={material_name}&region={region_code}&limit=10` to fetch matching EPDs. Extract `epd_id`, `product_name`, `manufacturer`, `gwp_a1a3`, `gwp_total`, `declared_unit`, `valid_from`, `valid_to`.
  4. **EC3 Database API:** For each material, call `GET https://buildingtransparency.org/api/v1/materials?name={material_name}&category={material_category}` to retrieve industry-average GWP values. Extract `ec3_gwp`, `ec3_unit`, `data_source`, `confidence_level`.
  5. Aggregate extracted EPD data into `EPDInventory` table keyed by `material_uuid`.
- **Output:** `EPDInventory` DataFrame with columns: `material_uuid`, `material_name`, `source_type` (Uploaded/Registry/EC3), `epd_id`, `gwp_a1a3`, `gwp_total`, `declared_unit`, `valid`, `confidence`.
- **On Failure:** If EPD Registry API unavailable, fallback to EC3 only with confidence downgrade. If EC3 unavailable, flag `HITL_REQUIRED` for manual EPD sourcing.

### Step 3: Material Matching and GWP Assignment
- **Type:** Calculation / AI Matching
- **Automated:** Yes
- **Description:**
  1. For each row in normalized takeoff, perform fuzzy string match (`fuzzywuzzy.process.extract` with threshold 80) against `EPDInventory.product_name` to identify candidate EPDs.
  2. Apply category filter: only match EPDs whose declared category aligns with takeoff `material_category`.
  3. Rank candidates by: (a) exact manufacturer match if known, (b) regional proximity, (c) EPD validity date (prefer current), (d) specificity (product-specific > product-group > industry-average).
  4. Select top candidate. Compute `total_gwp = quantity × gwp_per_declared_unit`. Handle unit conversion between takeoff unit and EPD declared unit using UCUM-based conversion table (kg, m3, m2, ton, piece).
  5. If multiple EPD candidates score equally, flag for HITL disambiguation.
  6. If no match found with confidence > 70%, flag `NO_MATCH` and assign EC3 industry-average as placeholder with HITL review.
  7. Store match rationale (`match_reason`) for audit trail.
- **Output:** `MaterialGWPTable` DataFrame: `material_uuid`, `material_name`, `quantity`, `unit`, `matched_epd_id`, `gwp_per_unit`, `total_gwp`, `match_confidence`, `match_reason`, `system_type`.
- **On Failure:** If >20% of materials are unassigned, escalate to HITL checkpoint immediately.

### Step 4: HITL Checkpoint 1 — Material Takeoff Accuracy
- **Type:** Human Review
- **Automated:** No
- **Description:**
  1. Pause workflow and present reviewer with:
     - Original `material_takeoff` file (download link)
     - Normalized takeoff summary (row count, total quantities per category, building area, service life)
     - Detected duplicate entries and auto-consolidation preview
     - Unmapped category flags
     - Missing structural/enclosure coverage alerts (if any material categories suggest gaps)
  2. Reviewer actions: `CONFIRM` (proceed), `EDIT` (upload corrected takeoff), `REJECT` (abort with notes).
  3. On `EDIT`, workflow returns to Step 1 with new file.
- **Output:** `HITLDecision` object: `{ decision: CONFIRM|EDIT|REJECT, reviewer_id, timestamp, notes }`
- **On Failure:** If SLA exceeded (72h), auto-escalate to project manager and default to `CONFIRM` with risk flag if no response.

### Step 5: System Classification and Scope Verification
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Classify each material into `system_type`: `Structural` (concrete, structural steel, rebar, timber framing, masonry structural), `Enclosure` (cladding, glazing, roofing, insulation, waterproofing, air barriers), `MEP` (if `include_mep=true`), `Interior` (if `include_interiors=true`), `Other`.
  2. Verify that `Structural` and `Enclosure` groups each contain at least one material with non-zero quantity. If either group is empty, trigger compliance error — credit requires at minimum structural + enclosure assessment.
  3. Compute group-level subtotals: `structural_gwp`, `enclosure_gwp`, `mep_gwp`, `interior_gwp`, `other_gwp`.
  4. Compute `total_embodied_carbon = sum(all_gwp)` for included modules (A-C or A-D per `system_boundary`).
  5. If `lca_tool_output` provided, parse and cross-check group totals against LCA tool output. Flag variance >10% for HITL review.
- **Output:** `SystemBreakdown` object with group totals and compliance flags.
- **On Failure:** Structural or enclosure missing → fatal compliance error, workflow stops.

### Step 6: HITL Checkpoint 2 — EPD Matching and GWP Values
- **Type:** Human Review
- **Automated:** No
- **Description:**
  1. Present reviewer with `MaterialGWPTable` including:
     - Material name, quantity, unit
     - Matched EPD name, manufacturer, EPD ID, validity status
     - GWP per unit and total GWP
     - Match confidence score and auto-match rationale
     - EC3 fallback indicators (highlighted in amber)
     - Cross-check variance with LCA tool output (if provided)
  2. For each low-confidence match (<80%) or EC3 fallback, require explicit reviewer confirmation or replacement with alternative EPD.
  3. Allow reviewer to reassign EPDs by searching EPD Registry inline or uploading new EPDs.
  4. Reviewer actions per row: `CONFIRM`, `REPLACE_EPD` (with new selection), `FLAG_FOR_REVIEW`.
  5. Global actions: `COMPLETE_REVIEW` (proceed), `RETURN_TO_STEP3` (trigger rematch with adjusted parameters), `ABORT`.
- **Output:** `ValidatedGWPTable` with all reviewer confirmations and reassignments logged.
- **On Failure:** SLA 72h. If exceeded, auto-proceed with flagged values marked `UNREVIEWED` and risk disclaimer appended to report.

### Step 7: CLF Baseline Comparison (Optional)
- **Type:** API Call / Calculation
- **Automated:** Yes
- **Description:**
  1. Call `GET https://clf-baselines.org/api/v1/baselines?building_type={building_type}&region={region_code}&year={clf_baseline_year}` to retrieve CLF material baseline GWP values by category.
  2. If API unavailable, use local CLF baseline dataset (cached JSON, updated quarterly) for US, Canada, UK, EU regions.
  3. Map material categories to CLF baseline categories (e.g., "Ready-mix concrete" → "Concrete", "Structural steel sections" → "Steel").
  4. For each category present in takeoff, compute:
     - `baseline_gwp = baseline_gwp_per_m2 × building_area` (or per-volume equivalent if baseline is volumetric)
     - `variance_pct = (project_gwp - baseline_gwp) / baseline_gwp × 100`
  5. Flag categories where project GWP deviates >30% from baseline (potential data quality issue or genuinely innovative material).
  6. If CLF baseline unavailable for region, mark comparison as `NOT_AVAILABLE` and proceed.
- **Output:** `BaselineComparison` DataFrame: `category`, `project_gwp`, `baseline_gwp`, `variance_pct`, `baseline_available`.
- **On Failure:** CLF data unavailable → soft failure; log warning and continue without baseline comparison.

### Step 8: GWP Intensity Calculation
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Compute total embodied carbon for included system boundary:
     - `gwp_total = sum(validated_gwp_total for all included materials)`
  2. Compute GWP intensity:
     - `gwp_intensity = gwp_total / building_area` → `kg CO2e/m2`
     - If input was sq ft, also compute `kg CO2e/sq ft` for US project convenience.
  3. If service life provided and `functional_unit_override` not set, compute annualized GWP:
     - `gwp_annualized = gwp_total / service_life` → `kg CO2e/year`
  4. Compute structural-only and enclosure-only intensities for submittal transparency.
- **Output:** `GWPMetrics` object: `{ gwp_total, gwp_intensity_m2, gwp_intensity_sf, gwp_annualized, structural_gwp, enclosure_gwp, mep_gwp, interior_gwp }`
- **On Failure:** Mathematical impossibility (zero building area) → caught in Step 1; else compute error aborts with stack trace.

### Step 9: Generate LEED Submission Documents
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. **Embodied Carbon Assessment Report (PDF):**
     - Cover page with project ID, credit code MRp2, date, LCA software used, assessment standard
     - Executive summary: total GWP, GWP intensity, scope (structural + enclosure), service life, system boundary
     - Methodology section: EPD sourcing (registry + EC3), matching algorithm, unit conversions
     - Material-GWP detailed table (from `ValidatedGWPTable`)
     - System breakdown chart (structural vs enclosure vs other)
     - Baseline comparison section (if available)
     - HITL review log (reviewer IDs, timestamps, notes)
     - Limitations and assumptions (LCA tool boundary statement)
     - Appendices: EPD summary table, CLF baseline source
     - Generated via `ReportLab`/`WeasyPrint` with custom LEED-compliant styling.
  2. **Material-GWP Table (XLSX):**
     - Full `ValidatedGWPTable` with all columns
     - Additional columns: `epd_download_link`, `validity_status`, `reviewer_notes`
     - Separate worksheets: `All Materials`, `Structural Only`, `Enclosure Only`, `EPD Inventory`, `Baseline Comparison`, `HITL Log`
     - Generated via `openpyxl` with data validation and conditional formatting.
  3. **EPD Summary (PDF):**
     - Condensed EPD information for each matched EPD: product name, manufacturer, program operator, EPD ID, validity period, declared unit, GWP-A1A3, GWP-total, source URL
     - One-page-per-EPD format for LEED reviewer convenience.
  4. **Baseline Comparison Report (PDF, conditional):**
     - Only generated if CLF baseline data available.
     - Side-by-side project vs baseline table, variance visualization, regional benchmark context.
- **Output:** File paths to four generated documents.
- **On Failure:** Template or data formatting error → retry once with simplified formatting; if persistent, HITL review of template data.

### Step 10: Final Validation and Delivery
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. Verify all required output documents exist and are non-empty.
  2. Verify `MaterialGWPTable` contains at least structural and enclosure rows (credit minimum).
  3. Cross-check PDF page count >3 (prevents empty report generation).
  4. Compute final automation score: `automated_steps / total_steps × 100`; for MRp2 this is 87% (2 HITL steps out of 10).
  5. Package outputs into project deliverables directory.
  6. Log execution metadata: runtime, API call counts, HITL durations, error flags, data quality score.
- **Output:** `SkillExecutionResult` object with document paths, metrics, and audit log.
- **On Failure:** Document generation incomplete → retry Step 9; if persistent, deliver partial outputs with error appendix.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 4: Material Takeoff Accuracy | Project Engineer / Sustainability Consultant | 72 hours | Verify that the material takeoff is complete and accurate. Confirm all structural and enclosure materials are included. Check for duplicate entries, correct units, and realistic quantities. Approve or upload corrected takeoff. |
| Step 6: EPD Matching and GWP Values | LCA Specialist / Sustainability Consultant | 72 hours | Verify that each material is matched to the correct EPD. Confirm GWP values (per declared unit) are reasonable for the material type and region. Re-assign EPDs where confidence is low or EC3 fallback was used. Cross-check against project-specific EPDs if available. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| **EC3 Database API** (`https://buildingtransparency.org/api/v1/materials`) | Retrieve industry-average embodied carbon GWP by material category and region | Global (primary: US, Canada, EU, UK, Australia) | Use cached quarterly EC3 snapshot JSON | 100 req/min with API key; 20 req/min anonymous |
| **EPD Registry API** (`https://api.theepdregistry.com/v1/epds/search`) | Search and retrieve product-specific EPD data including GWP, declared unit, validity | Global (strongest coverage: EU, North America, APAC) | Manual EPD upload; fallback to manufacturer EPD sourcing | 200 req/min with free registration; 50 req/min basic tier |
| **One Click LCA API** (`https://api.oneclicklca.com/v1/projects/{id}/results`) | Cross-check whole-building LCA results against calculated material GWP totals | Global (license-based; available in 150+ countries) | Skip cross-check; rely on material-by-material calculation | License-dependent; typically 100 req/min |
| **Tally API** (`https://api.tallylca.com/v1/revit-models/{id}/materials`) | Import material quantities and GWP from Revit-integrated Tally export | Global (license-based; primarily US and Canada) | Manual CSV export from Tally; user upload | License-dependent; no public rate limit published |
| **CLF Baseline API** (`https://clf-baselines.org/api/v1/baselines`) | Retrieve regional CLF material baselines for comparison | Limited (US, Canada, UK, EU, Australia, NZ; expanding) | Use locally cached CLF dataset (updated quarterly); skip comparison if unavailable | 50 req/min |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | Full EC3, EPD Registry, CLF baseline, One Click LCA, and Tally support. Optimal data coverage. |
| Canada | Available | EC3 includes Canadian data. CLF baselines available. EPD Registry strong coverage. |
| European Union | Available | EPD Registry (EN 15804 EPDs) very strong. EC3 expanding EU coverage. CLF baselines available for select countries. One Click LCA widely used. |
| United Kingdom | Available | EPD Registry strong. CLF baselines available. EC3 limited but growing. |
| Australia / New Zealand | Limited | EPD Registry coverage moderate. EC3 has basic data. CLF baselines available. One Click LCA supported. |
| Asia-Pacific (excl. AU/NZ) | Limited | EPD Registry growing. EC3 minimal. CLF baselines not available. One Click LCA supported in major markets (JP, SG, HK). |
| Middle East / Africa | Limited | EPD Registry limited. EC3 minimal. No CLF baselines. One Click LCA available in UAE, SA. |
| Latin America | Limited | EPD Registry minimal. EC3 minimal. No CLF baselines. One Click LCA expanding (BR, MX). |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Material takeoff schema invalid | Return validation error with row-level details | Yes (immediate) | User must re-upload; no auto-retry |
| EPD Registry API down | Switch to EC3 as primary; mark confidence downgrade | Yes (flag in HITL) | 3 retries with exponential backoff; then fallback |
| EC3 API down | Use cached EC3 snapshot; mark `CACHED_DATA` warning | Yes (flag in HITL) | 3 retries; then proceed with snapshot |
| One Click LCA API down (if cross-check enabled) | Skip cross-check step; continue with material calculation | Yes (notification that cross-check skipped) | 2 retries; then skip |
| Tally API down (if import enabled) | Request manual CSV export from user | Yes (email/notification) | N/A — requires user action |
| CLF Baseline API down | Use local cache; if cache stale (>90 days), skip comparison | No (soft failure, logged) | 2 retries; then cache or skip |
| >20% materials unassigned after matching | Immediate HITL escalation with unassigned list | Yes (urgent HITL flag) | 1 rematch attempt with relaxed thresholds; then HITL |
| Unit conversion failure (unknown unit) | Flag specific material; use HITL for manual conversion | Yes | User must specify conversion factor |
| HITL SLA exceeded (72h) | Auto-proceed with risk disclaimer; mark `UNREVIEWED` | Yes (escalation to PM) | N/A |
| PDF generation failure | Retry with simplified template; if fails, generate plain HTML | Yes | 1 retry |
| Structural or enclosure systems missing | Fatal compliance error; workflow stops; user must correct takeoff | Yes (immediate) | N/A |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Embodied Carbon Assessment Report | PDF | Full LEED submittal report for MRp2 including methodology, material-GWP table, system breakdown, HITL log, and limitations |
| Material-GWP Table | XLSX | Detailed material-by-material GWP data with multiple worksheets for filtering and analysis |
| EPD Summary | PDF | Condensed one-page-per-EPD reference document for LEED reviewer verification |
| Baseline Comparison Report | PDF (conditional) | Side-by-side comparison of project GWP vs CLF regional baselines with variance analysis |

## Testing
```bash
# Run unit tests for MRp2 skill
python -m pytest skills/leed-mr-p2-embodied/tests/

# Run integration tests (requires EC3 and EPD Registry API keys)
pytest skills/leed-mr-p2-embodied/tests/integration/ --api-keys-env

# Run E2E workflow test with mock HITL
pytest skills/leed-mr-p2-embodied/tests/e2e/ --mock-hitl
```

## Example Usage (OpenAI Agents SDK + Restate)
```python
from leed_platform.skills import MRp2EmbodiedCarbonSkill

skill = MRp2EmbodiedCarbonSkill(
    project_id="550e8400-e29b-41d4-a716-446655440000",
    inputs={
        "material_takeoff": "/uploads/project_123_takeoff.xlsx",
        "building_area": 45000,           # sq ft; auto-converted to sq m
        "service_life": 60,
        "lca_software": "Tally",
        "structural_systems_included": True,
        "enclosure_systems_included": True,
        "assessment_standard": "ISO_21930",
        "building_type": "commercial",
        "region_code": "US",
        "lca_tool_output": "/uploads/tally_export.csv",  # optional cross-check
        "uploaded_epds": ["/uploads/epd_concrete.pdf", "/uploads/epd_steel.xml"],
        "include_mep": False,
        "include_interiors": False,
        "system_boundary": "A-C"
    }
)

# Execute full workflow with HITL checkpoints
result = await skill.execute()

# Access outputs
print(result.documents["assessment_report"])     # /output/MRp2_assessment_report.pdf
print(result.documents["material_gwp_table"])      # /output/MRp2_material_gwp_table.xlsx
print(result.documents["epd_summary"])             # /output/MRp2_epd_summary.pdf
print(result.metrics.gwp_total)                    # e.g., 2847000.0 kg CO2e
print(result.metrics.gwp_intensity_m2)             # e.g., 678.5 kg CO2e/m2
```

## Platform Workflow (OpenAI Agents SDK + Restate)
```python
from langgraph.graph import StateGraph, END
from leed_platform.skills.leed_mr_p2.types import MRp2State, HITLAction
from leed_platform.skills.leed_mr_p2.nodes import (
    validate_inputs,
    parse_epds,
    match_materials,
    hitl_takeoff_review,
    classify_systems,
    hitl_epd_review,
    compare_baseline,
    calculate_gwp_metrics,
    generate_documents,
    final_validate
)

# Define the LangGraph workflow for MRp2
workflow = StateGraph(MRp2State)

# --- Nodes ---
workflow.add_node("validate", validate_inputs)
workflow.add_node("parse_epds", parse_epds)
workflow.add_node("match_materials", match_materials)
workflow.add_node("hitl_takeoff", hitl_takeoff_review)      # HITL Checkpoint 1
workflow.add_node("classify_systems", classify_systems)
workflow.add_node("hitl_epd", hitl_epd_review)              # HITL Checkpoint 2
workflow.add_node("compare_baseline", compare_baseline)
workflow.add_node("calculate_metrics", calculate_gwp_metrics)
workflow.add_node("generate_docs", generate_documents)
workflow.add_node("final_validate", final_validate)

# --- Edges ---
workflow.set_entry_point("validate")

workflow.add_conditional_edges(
    "validate",
    lambda state: "parse_epds" if state.validation.valid else "hitl_takeoff" if state.validation.needs_hitl else END,
    { "parse_epds": "parse_epds", "hitl_takeoff": "hitl_takeoff", "__end__": END }
)

workflow.add_edge("parse_epds", "match_materials")

workflow.add_conditional_edges(
    "match_materials",
    lambda state: "hitl_takeoff" if state.takeoff_review_pending else "classify_systems",
    { "hitl_takeoff": "hitl_takeoff", "classify_systems": "classify_systems" }
)

# HITL Checkpoint 1: Material Takeoff
workflow.add_conditional_edges(
    "hitl_takeoff",
    lambda state: state.hitl_decision.action,
    {
        HITLAction.CONFIRM: "classify_systems",
        HITLAction.EDIT: "validate",          # Loop back with corrected takeoff
        HITLAction.REJECT: END
    }
)

workflow.add_edge("classify_systems", "hitl_epd")

# HITL Checkpoint 2: EPD Matching
workflow.add_conditional_edges(
    "hitl_epd",
    lambda state: state.hitl_decision.action,
    {
        HITLAction.CONFIRM: "compare_baseline",
        HITLAction.REPLACE_EPD: "match_materials",   # Loop back for rematch
        HITLAction.RETURN_TO_STEP3: "match_materials",
        HITLAction.ABORT: END
    }
)

workflow.add_edge("compare_baseline", "calculate_metrics")
workflow.add_edge("calculate_metrics", "generate_docs")
workflow.add_edge("generate_docs", "final_validate")
workflow.add_edge("final_validate", END)

# Compile the workflow
app = workflow.compile()

# Execute with project state
initial_state = MRp2State(project_id="...", inputs={...})
result = app.invoke(initial_state)
```

## Skill Implementation Notes

### Boundary Statement (Critical)
This skill **does not** perform whole-building life cycle assessment (WBLCA) calculations. Whole-building LCA requires specialized software (Tally, One Click LCA, SimaPro, GaBi) that models building systems, operational energy, end-of-life scenarios, and complex system interactions per ISO 21930 / EN 15804. This skill operates **downstream** of those tools: it accepts LCA software outputs (optional cross-check), EPDs, and material takeoffs, then automates the labor-intensive tasks of EPD parsing, material matching, GWP aggregation, baseline comparison, and LEED document generation. The actual WBLCA remains the responsibility of the project LCA practitioner.

### EPD Matching Algorithm Detail
The material-to-EPD matching uses a multi-stage pipeline:
1. **Exact match** on EPD Registry UUID if `project_epd_registry_ids` provided.
2. **Fuzzy name match** (token sort ratio) on `material_name` vs EPD `product_name` with category constraint.
3. **Category fallback** to EC3 industry-average if no product-specific EPD available.
4. **Regional prioritization** — prefer EPDs from same country/region as project.
5. **Validity filter** — exclude expired EPDs unless explicitly overridden.

### Unit Conversion Engine
Built-in UCUM-compliant unit conversions:
- Mass: kg, ton (metric), lb, ton (US)
- Volume: m3, cu ft, L, gal (US)
- Area: m2, sq ft, sq yd
- Length: m, ft, in, mm
- Count: piece, each (no conversion needed)

### Data Quality Scoring
Each material row receives a `data_quality_score` (0-100):
- Product-specific EPD (current, same region): 95-100
- Product-group EPD (current, same region): 80-94
- Generic EPD (different region): 60-79
- EC3 industry-average: 40-59
- Unassigned / placeholder: 0-39

### Audit Trail
Every automated decision is logged:
- EPD match rationale (string explanation)
- API call timestamps and response codes
- Unit conversion factors applied
- HITL reviewer actions with timestamps
- Confidence scores at each decision point
