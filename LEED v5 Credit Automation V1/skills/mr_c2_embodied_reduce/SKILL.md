---
name: leed-mr-c2-embodied-reduce
version: 1.0.0
author: LEED Automation Platform
description: Automates LEED v5 MRc2 embodied carbon reduction documentation, baseline comparison, and points calculation from LCA tool outputs.
---

## Metadata
- **Credit Code:** MRc2
- **Credit Name:** Reduce Embodied Carbon
- **Points:** Up to 6 points
- **Automation Level:** 88.4%
- **Complexity:** Medium
- **Primary Data Source:** EC3 Database, EPD Registry, CLF Material Baselines, One Click LCA API
- **HITL Required:** Yes

## Purpose
Automates the documentation, baseline comparison, and points calculation for LEED v5 MRc2 (Reduce Embodied Carbon) based on LCA tool outputs, EPD data, and material baseline benchmarks — orchestrating EC3, EPD Registry, and CLF data without performing the WBLCA itself.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `project_id` | string | Deer-Flow project registry | UUID format, exists in project database |
| `baseline_embodied_carbon` | dict | MRp2 prerequisite output | Required keys: `total_kg_co2`, `structural_kg_co2`, `enclosure_kg_co2`, `building_area_m2`, `lca_tool`, `baseline_date` |
| `design_embodied_carbon` | dict | LCA tool export (One Click LCA/Tally) | Required keys: `total_kg_co2`, `structural_kg_co2`, `enclosure_kg_co2`, `lca_tool`, `export_date` |
| `material_changes` | list[dict] | Project team input / LCA diff | Each item: `{"material_category": "string", "original_spec": "string", "revised_spec": "string", "quantity": "number", "unit": "string", "gwp_reduction_kg_co2": "number"}` |
| `building_area` | number | Project metadata | > 0, units match baseline (`m2` or `ft2`) |
| `building_use_type` | string | LEED project registration | Enum: `office`, `multifamily`, `warehouse`, `retail`, `healthcare`, `education`, `hospitality`, `other` |
| `structural_systems` | list[string] | Project structural engineer | Must include at least one of: `concrete`, `steel`, `mass_timber`, `masonry` |
| `enclosure_systems` | list[string] | Project architect | Must include at least one of: `curtain_wall`, `precast`, `brick`, `metal_panel`, `roofing` |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `reduction_option` | string | `"percentage"` | `"percentage"` (Option 1) or `"gwp_threshold"` (Option 2) |
| `clf_benchmark_version` | string | `"2023"` | CLF baseline year: `"2021"`, `"2023"`, or `"latest"` |
| `epd_registry` | string | `"openEPD"` | Preferred EPD registry: `"openEPD"`, `"EC3"`, `"IBU"`, `"Environdec"` |
| `material_categories` | list[string] | `["concrete", "steel", "wood", "aluminum", "insulation", "glazing", "finishes"]` | Full list of material categories tracked |
| `include_mep` | bool | `false` | Whether MEP systems are included in LCA scope |
| `include_site` | bool | `false` | Whether site/landscape materials are included |
| `biogenic_carbon_method` | string | `"dynamic_LCA"` | Method for biogenic carbon accounting: `"dynamic_LCA"`, `"module_D"`, `"none"` |
| `reuse_materials` | list[dict] | `[]` | Salvaged/reused materials: `[{"material": "string", "quantity": "number", "unit": "string", "source": "string", "avoided_emissions_kg_co2": "number"}]` |
| `hitl_reviewer_email` | string | `None` | Email for HITL reviewer notification |
| `one_click_lca_api_key` | string | `None` | API key for One Click LCA integration (if using Option 2 or automated import) |
| `tally_export_path` | string | `None` | Path to Tally LCA JSON/CSV export file |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:** Validates that all required inputs are present, that structural and enclosure systems are included per LEED v5 requirements, that baseline and design carbon values are positive numbers, that building area units are consistent, and that material_changes list contains at least one entry. Checks that `baseline_embodied_carbon` contains MRp2 prerequisite data (or fetches it via project_id if available). Validates that reduction_option is one of the allowed values. If `tally_export_path` or One Click LCA API key is provided, pre-validates file format or API connectivity.
- **Output:** `ValidatedInput` dict with normalized units (converted to metric), confirmed material categories, and baseline reference linkage.
- **On Failure:** Returns `ValidationError` with specific field-level messages. Retries not applicable — project team must correct inputs.

### Step 2: Fetch CLF Baseline Benchmarks
- **Type:** API Call
- **Automated:** Yes
- **Description:** Queries CLF Material Baselines API (https://carbonleadershipforum.org/) for GWP benchmarks matching the building_use_type, structural_systems, and enclosure_systems. Fetches kgCO2e/m2 baselines for each material category. If `clf_benchmark_version` is `"latest"`, resolves to the most recent published version. Validates that structural and enclosure benchmarks exist (LEED v5 requirement). Handles regional baseline variants if available.
- **Output:** `CLFBaseline` dict with per-category and total benchmarks, metadata on version, and URL to source dataset.
- **On Failure:** If CLF API is unavailable, falls back to cached baseline dataset (last valid fetch within 30 days). If no cache exists, escalates to HITL with manual baseline entry instructions. Human notification: Yes.

### Step 3: Fetch Product EPD Data
- **Type:** API Call
- **Automated:** Yes
- **Description:** For each material in `material_changes`, queries the configured EPD registry (default: openEPD API) to fetch product-specific GWP values (A1-A3 declared unit). If openEPD is unavailable, falls back to EC3 Database API. Validates that EPDs are ISO 14025/EN 15804 or ISO 21930 compliant and not expired. Extracts GWP per declared unit, converts to project quantities, and computes revised material carbon totals. Cross-references with original specifications to calculate per-material reductions.
- **Output:** `EPDData` list with product GWP values, EPD validity status, compliance standard, and calculated per-material embodied carbon.
- **On Failure:** If EPD registry APIs fail, marks materials as "EPD lookup failed" and continues with user-provided GWP values. Flags these for HITL review. Human notification: Yes. Retry: 3 times with exponential backoff.

### Step 4: Validate Baseline vs. Design Consistency
- **Type:** Validation
- **Automated:** Yes
- **Description:** Compares baseline_embodied_carbon and design_embodied_carbon to ensure they use the same LCA tool, same system boundaries (structural + enclosure mandatory), same building area, and consistent units. Checks that the design carbon is lower than baseline (or flags if not). Verifies that biogenic carbon accounting method is consistent between both studies. If inconsistencies are detected, generates a detailed discrepancy report.
- **Output:** `ConsistencyReport` with pass/fail status, list of discrepancies (if any), and recommendations for resolution.
- **On Failure:** If critical inconsistencies found (e.g., different tools, different system boundaries), blocks automation and routes to HITL for manual reconciliation. Human notification: Yes.

### Step 5: Calculate Percentage Reduction (Option 1)
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Computes percentage reduction using the formula: `Reduction % = ((Baseline_Total_kgCO2 - Design_Total_kgCO2) / Baseline_Total_kgCO2) × 100`. Also calculates per-category reductions for structural and enclosure systems separately. Validates that structural + enclosure systems collectively represent at least the minimum required scope per LEED v5. Determines points earned based on LEED v5 MRc2 points table: 1 point for 10% reduction, 2 points for 20%, 3 points for 30%, 4 points for 40%, 5 points for 50%, 6 points for 60%+. If Option 2 is selected, skips this and proceeds to Step 6.
- **Output:** `ReductionResult` with total percentage, per-category breakdown, points earned, and LEED table reference.
- **On Failure:** If calculation produces negative reduction (i.e., design > baseline), flags as "increase in embodied carbon" and requires HITL review. Human notification: Yes.

### Step 6: Calculate GWP Threshold Achievement (Option 2)
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Only executes if `reduction_option` is `"gwp_threshold"`. For each material category, compares the design GWP against LEED v5 Option 2 specific material GWP thresholds (e.g., concrete ≤ X kgCO2e/m3, steel ≤ Y kgCO2e/kg, etc.). Uses EC3 Database API or One Click LCA API to fetch threshold values. Calculates number of categories meeting thresholds. Determines points based on number of categories achieving thresholds: 1-2 categories = 1 point, 3-4 = 2 points, 5-6 = 3 points, 7+ = 4 points (with bonus points for structural/enclosure achievement). For structural and enclosure systems specifically, checks if 50%+ of materials by mass meet their respective thresholds for bonus points.
- **Output:** `ThresholdResult` with per-material pass/fail status, categories achieved, bonus points, and total points.
- **On Failure:** If threshold data is unavailable for a material category, marks as "threshold unknown" and continues. Flags for HITL review. Human notification: No (logged only).

### Step 7: Process Reuse and Salvage Credits
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Processes `reuse_materials` list to calculate avoided emissions from salvaged/reused materials. For each reused material, validates that source documentation exists (deconstruction records, supplier certificates). Calculates avoided emissions as the difference between baseline new-material carbon and actual reused-material carbon (typically near-zero for direct reuse). Adds avoided emissions to the numerator of the reduction calculation. Checks LEED v5 requirements for documentation of reuse (chain of custody, prior use verification).
- **Output:** `ReuseCredit` with total avoided emissions, per-material breakdown, documentation status, and adjusted reduction percentage.
- **On Failure:** If documentation is missing for a reused material, flags for HITL review with specific documentation requirements. Human notification: Yes.

### Step 8: HITL Checkpoint — Verify Reduction Strategies and LCA Outputs
- **Type:** Human Review
- **Automated:** No
- **Description:** Presents the reviewer with: (a) side-by-side baseline vs. design comparison table, (b) material changes list with EPD-linked GWP values, (c) calculated reduction percentage and points, (d) any flagged discrepancies or EPD lookup failures, (e) reuse/salvage documentation status. Reviewer must confirm: (1) LCA tool outputs are accurate and from a qualified practitioner, (2) material changes were actually implemented in the design, (3) EPDs are valid and applicable to specified products, (4) baseline is appropriate (MRp2 prerequisite met), (5) structural and enclosure systems are fully represented. Reviewer can approve, request changes, or reject with comments.
- **Output:** `HITLDecision` with status (`approved`, `changes_requested`, `rejected`), reviewer comments, and timestamp.
- **On Failure:** If SLA exceeded (72 hours), auto-escalates to secondary reviewer and notifies project manager. If rejected, returns to project team with required corrections listed.

### Step 9: Generate Embodied Carbon Reduction Report (PDF)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generates a comprehensive PDF report including: executive summary with reduction percentage and points earned, methodology section describing LCA tools, baseline sources, and EPDs used, detailed baseline vs. design comparison tables (by material category), material optimization strategies narrative, EPD summary table with compliance verification, structural and enclosure system breakdown, reuse/salvage documentation section, and appendices with raw data exports. Formatted per LEED v5 documentation requirements with version control and page numbering.
- **Output:** `MRc2_Reduction_Report.pdf` — absolute file path.
- **On Failure:** If PDF generation fails (e.g., template error), retries once with fallback template. If still failing, generates markdown intermediate and queues for manual PDF conversion. Human notification: Yes.

### Step 10: Generate Baseline vs. Design Comparison (XLSX)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generates an Excel workbook with multiple sheets: (1) `Summary` — total baseline, design, reduction %, points; (2) `By_Material_Category` — per-category kgCO2, kgCO2/m2, % of total, reduction; (3) `Material_Details` — line-item materials with original spec, revised spec, quantity, unit, original GWP, revised GWP, delta; (4) `EPD_Summary` — EPD metadata (manufacturer, product, standard, validity, GWP value); (5) `Structural_Enclosure` — mandatory systems breakdown; (6) `Reuse_Salvage` — reused materials with avoided emissions; (7) `Points_Calculation` — LEED table with achieved thresholds/reductions. Includes data validation, conditional formatting for reductions >50%, and formulas intact.
- **Output:** `MRc2_Baseline_Design_Comparison.xlsx` — absolute file path.
- **On Failure:** If Excel generation fails, retries once. If still failing, outputs CSV sheets as fallback. Human notification: No (logged only).

### Step 11: Generate Points Calculation Workbook (XLSX)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generates a focused Excel workbook for LEED reviewer verification: Sheet 1 shows the LEED v5 MRc2 points table with the project's achieved row highlighted. Sheet 2 contains all calculation formulas with cell references to source data. Sheet 3 is a checklist of LEED requirements with pass/fail status (structural included, enclosure included, baseline valid, EPDs current, LCA boundaries consistent, etc.). Sheet 4 contains reviewer notes field (pre-filled with HITL comments). All formulas are transparent and auditable.
- **Output:** `MRc2_Points_Calculation.xlsx` — absolute file path.
- **On Failure:** If Excel generation fails, outputs formula documentation as markdown. Human notification: No (logged only).

### Step 12: Upload to LEED Documentation Portal
- **Type:** API Call
- **Automated:** Yes
- **Description:** If project has LEED documentation portal credentials configured, automatically uploads the three output documents to the correct MRc2 credit folder. Sets document metadata (credit code, revision, date, author). Returns upload confirmation with document IDs. If portal API is unavailable, queues for retry and provides manual upload instructions.
- **Output:** `UploadConfirmation` with document IDs, URLs, and status.
- **On Failure:** If portal API fails, queues for retry (3 attempts over 24 hours). If all retries fail, provides manual upload instructions to project team. Human notification: Yes.

### Step 13: Finalize and Notify
- **Type:** API Call
- **Automated:** Yes
- **Description:** Sends completion notification to project team with summary: reduction percentage, points earned, documents generated, and any outstanding items requiring attention. Updates Deer-Flow project registry with MRc2 completion status, points awarded, and document paths. Logs full execution trace for audit purposes.
- **Output:** `CompletionSummary` with status, points, document paths, and next steps.
- **On Failure:** If notification fails, logs error but does not block completion. Retries notification once.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 8 — Verify Reduction Strategies and LCA Outputs | LCA-qualified project team member (structural engineer, architect, or sustainability consultant with LCA training) | 72 hours | Verify: (1) LCA tool output accuracy and qualified practitioner authorship, (2) material specification changes were implemented in construction documents, (3) EPDs are valid, current, and product-applicable, (4) MRp2 baseline is complete and appropriate, (5) structural + enclosure systems are fully represented in scope, (6) reuse/salvage documentation is sufficient, (7) unit consistency across all inputs. Approve if all checks pass; request changes with specific corrections if not. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| **EC3 Database API** | Material GWP data, product benchmarks, manufacturer-specific EPDs | Global (US-centric data, expanding internationally) | Cached EC3 dataset (updated monthly); manual EPD entry | 1000 requests/minute |
| **openEPD API** | Product-specific EPD search and retrieval (ISO-compliant) | Global | EC3 Database API; direct EPD PDF parsing | 500 requests/minute |
| **CLF Material Baselines API** | Benchmark GWP values by building type and material category | Global (US/Canada primary; international baselines for select materials) | Cached CLF baselines (2021, 2023); project-specific baseline from MRp2 | 100 requests/minute |
| **One Click LCA API** | Optional LCA calculation import, GWP threshold validation, automated material data retrieval | Global (EU, US, CA, AU, Asia-Pacific) | Manual One Click LCA export import (JSON/CSV); Tally export | 300 requests/minute |
| **Tally** (file-based, not API) | LCA tool export import | N/A (file-based) | One Click LCA export; manual data entry | N/A |
| **LEED Documentation Portal API** | Automated document upload to USGBC project repository | Global | Manual upload via LEED Online web interface | 50 requests/minute |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| **United States** | Available | Full EC3, CLF baselines, EPD registry coverage. LEED v5 primary market. |
| **Canada** | Available | CLF baselines include Canadian variants. EC3 covers major Canadian manufacturers. |
| **European Union** | Available | openEPD/Environdec EPD registry strong. EC3 expanding EU coverage. One Click LCA fully operational. |
| **United Kingdom** | Available | EPD registry access via Environdec/IBU. CLF baselines usable with adjustments. |
| **Australia / New Zealand** | Available | One Click LCA regional data available. EPD access via regional registries. |
| **Asia-Pacific (excl. AU/NZ)** | Limited | One Click LCA available in select markets (Singapore, Japan). EC3 coverage limited. EPD registry access variable. |
| **Latin America** | Limited | EC3 minimal coverage. EPD registries growing (Brazil). CLF baselines may require regional adjustment factors. |
| **Middle East / Africa** | Limited | EPD registry access sparse. One Click LCA limited. Recommend project-specific baseline from MRp2. |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Invalid or missing required input | Block execution, return detailed validation error | Yes (project team) | N/A |
| CLF API unavailable | Use cached baselines; if no cache, escalate to HITL | Yes | 3× over 10 min |
| EPD registry API failure | Continue with user-provided GWP; flag for HITL review | Yes | 3× with backoff |
| EPD expired or non-compliant | Flag material, continue calculation, require HITL verification | Yes (HITL reviewer) | N/A |
| Baseline/Design inconsistency (critical) | Block calculation, route to HITL for reconciliation | Yes | N/A |
| Negative reduction (design > baseline) | Flag as increase, require HITL review and explanation | Yes | N/A |
| One Click LCA API failure | Use manual file import path; notify user to upload export | Yes | 3× over 15 min |
| PDF generation failure | Retry once with fallback template; if still failing, output markdown | Yes | 1× |
| LEED portal upload failure | Queue for retry; provide manual upload instructions | Yes | 3× over 24 hrs |
| HITL reviewer unresponsive (SLA breach) | Auto-escalate to secondary reviewer; notify project manager | Yes | Escalation after 72 hrs |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Embodied Carbon Reduction Report | PDF | Comprehensive LEED submission document with methodology, baseline vs. design comparison, material optimization narrative, EPD compliance summary, structural/enclosure breakdown, and appendices |
| Baseline vs. Design Comparison | XLSX | Detailed Excel workbook with per-material, per-category, and system-level embodied carbon data, EPD metadata, and reuse/salvage credits |
| Points Calculation | XLSX | LEED reviewer-focused workbook with transparent formulas, points table, requirement checklist, and calculation audit trail |

## Testing
```bash
# Unit tests
python -m pytest skills/leed-mr-c2-embodied-reduce/tests/

# Integration tests (requires API keys)
python -m pytest skills/leed-mr-c2-embodied-reduce/tests/integration/ -v --api-mode

# Key test scenarios:
# 1. Full Option 1 percentage reduction flow with valid inputs
# 2. Option 2 GWP threshold flow with multi-material compliance
# 3. CLF API fallback to cached baselines
# 4. EPD registry failure with user-provided GWP fallback
# 5. HITL approval and rejection paths
# 6. Negative reduction detection and escalation
# 7. Reuse/salvage material processing
# 8. Structural + enclosure scope validation
# 9. Unit conversion consistency (imperial to metric)
# 10. PDF and Excel document generation validation
# 11. LEED portal upload (mocked)
```

## Example Usage (Deer-Flow)
```python
from deerflow.skills import MRc2EmbodiedReduceSkill

skill = MRc2EmbodiedReduceSkill(
    project_id="proj-12345-abcde",
    inputs={
        "baseline_embodied_carbon": {
            "total_kg_co2": 4500000,
            "structural_kg_co2": 2100000,
            "enclosure_kg_co2": 1350000,
            "building_area_m2": 25000,
            "lca_tool": "One Click LCA",
            "baseline_date": "2024-01-15"
        },
        "design_embodied_carbon": {
            "total_kg_co2": 3150000,
            "structural_kg_co2": 1470000,
            "enclosure_kg_co2": 945000,
            "lca_tool": "One Click LCA",
            "export_date": "2024-06-20"
        },
        "material_changes": [
            {
                "material_category": "concrete",
                "original_spec": "Standard Portland Cement Concrete (30 MPa)",
                "revised_spec": "30% GGBFS Concrete Mix (30 MPa)",
                "quantity": 8500,
                "unit": "m3",
                "gwp_reduction_kg_co2": 425000
            },
            {
                "material_category": "steel",
                "original_spec": "Hot-rolled structural steel (A992)",
                "revised_spec": "EAF-produced structural steel with recycled content",
                "quantity": 420,
                "unit": "tonnes",
                "gwp_reduction_kg_co2": 336000
            },
            {
                "material_category": "glazing",
                "original_spec": "Standard double-pane IGU",
                "revised_spec": "Triple-pane low-carbon IGU with warm edge spacers",
                "quantity": 3200,
                "unit": "m2",
                "gwp_reduction_kg_co2": 128000
            }
        ],
        "building_area": 25000,
        "building_use_type": "office",
        "structural_systems": ["concrete", "steel"],
        "enclosure_systems": ["curtain_wall", "precast"],
        "reduction_option": "percentage",
        "clf_benchmark_version": "2023",
        "reuse_materials": [
            {
                "material": "Reclaimed dimensional lumber",
                "quantity": 45,
                "unit": "m3",
                "source": "Local deconstruction project (Building XYZ)",
                "avoided_emissions_kg_co2": 28000
            }
        ]
    }
)

result = await skill.execute()

# Expected result:
# {
#   "status": "completed",
#   "reduction_percentage": 30.0,
#   "points_earned": 3,
#   "option": "percentage",
#   "documents": {
#     "reduction_report_pdf": "/mnt/agents/output/skills/leed-mr-c2-embodied-reduce/reports/MRc2_Reduction_Report_proj-12345.pdf",
#     "comparison_xlsx": "/mnt/agents/output/skills/leed-mr-c2-embodied-reduce/reports/MRc2_Baseline_Design_Comparison_proj-12345.xlsx",
#     "points_calculation_xlsx": "/mnt/agents/output/skills/leed-mr-c2-embodied-reduce/reports/MRc2_Points_Calculation_proj-12345.xlsx"
#   },
#   "hitl_status": "approved",
#   "baseline_vs_clf": {
#     "baseline_total_kg_co2": 4500000,
#     "clf_benchmark_kg_co2": 4750000,
#     "baseline_variance_from_clf": -5.3
#   }
# }
```

## Deer-Flow Workflow (LangGraph)
```python
from langgraph.graph import StateGraph, END
from deerflow.skills.leed_mr_c2.states import MRc2State
from deerflow.skills.leed_mr_c2.nodes import (
    validate_inputs,
    fetch_clf_baselines,
    fetch_epd_data,
    validate_consistency,
    calculate_reduction,
    calculate_gwp_threshold,
    process_reuse_materials,
    human_review_checkpoint,
    generate_reduction_report,
    generate_comparison_xlsx,
    generate_points_calculation,
    upload_to_leed_portal,
    finalize_and_notify
)

# Define the LangGraph workflow for this skill
workflow = StateGraph(MRc2State)

# Add all processing nodes
workflow.add_node("validate", validate_inputs)
workflow.add_node("fetch_clf", fetch_clf_baselines)
workflow.add_node("fetch_epds", fetch_epd_data)
workflow.add_node("validate_consistency", validate_consistency)
workflow.add_node("calculate_reduction", calculate_reduction)
workflow.add_node("calculate_threshold", calculate_gwp_threshold)
workflow.add_node("process_reuse", process_reuse_materials)
workflow.add_node("hitl_review", human_review_checkpoint)
workflow.add_node("generate_report", generate_reduction_report)
workflow.add_node("generate_comparison", generate_comparison_xlsx)
workflow.add_node("generate_points", generate_points_calculation)
workflow.add_node("upload_portal", upload_to_leed_portal)
workflow.add_node("finalize", finalize_and_notify)

# Define the execution edges
workflow.set_entry_point("validate")
workflow.add_edge("validate", "fetch_clf")
workflow.add_edge("fetch_clf", "fetch_epds")
workflow.add_edge("fetch_epds", "validate_consistency")
workflow.add_edge("validate_consistency", "calculate_reduction")

# Conditional routing based on reduction_option
# "percentage" -> calculate_reduction -> process_reuse
# "gwp_threshold" -> calculate_threshold -> process_reuse
workflow.add_conditional_edges(
    "validate_consistency",
    lambda state: "calculate_threshold" if state["inputs"].get("reduction_option") == "gwp_threshold" else "calculate_reduction",
    {
        "calculate_reduction": "calculate_reduction",
        "calculate_threshold": "calculate_threshold"
    }
)

workflow.add_edge("calculate_reduction", "process_reuse")
workflow.add_edge("calculate_threshold", "process_reuse")

# Human-in-the-loop checkpoint (interrupts execution)
workflow.add_edge("process_reuse", "hitl_review")

# After HITL approval, proceed to document generation
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: "generate" if state["hitl_status"] == "approved" else "reject",
    {
        "generate": "generate_report",
        "reject": END  # Returns to project team with corrections needed
    }
)

# Parallel document generation
workflow.add_edge("generate_report", "generate_comparison")
workflow.add_edge("generate_comparison", "generate_points")
workflow.add_edge("generate_points", "upload_portal")
workflow.add_edge("upload_portal", "finalize")
workflow.add_edge("finalize", END)

# Compile the workflow
app = workflow.compile()

# Execute
# result = await app.ainvoke(initial_state)
```

---

## Implementation Notes

### WBLCA Boundary (CRITICAL)
This skill **does NOT perform Whole Building Life Cycle Assessment (WBLCA)**. The WBLCA must be completed by a qualified practitioner using Tally, One Click LCA, or equivalent tools prior to invoking this skill. This skill automates:
- Documentation of reduction strategies
- Baseline-to-design comparison
- Points calculation based on LCA tool outputs
- EPD validation and linking
- LEED submission document generation

### Baseline Requirements
- The baseline must come from MRp2 (Building Life-Cycle Assessment) prerequisite completion.
- If MRp2 baseline is unavailable, the skill can use CLF benchmarks as a provisional baseline with clear disclosure, but this requires HITL approval and may not be accepted by all LEED reviewers.
- Structural systems and enclosure systems must both be included in the baseline and design LCA scopes per LEED v5.

### Material Category Scope
LEED v5 MRc2 requires embodied carbon reduction across material categories. The skill tracks:
- Structural: concrete, steel, mass timber, masonry
- Enclosure: curtain wall, precast, brick, metal panel, roofing, glazing
- Additional: insulation, finishes, site materials (if included)

### Biogenic Carbon
- Must use consistent biogenic carbon accounting between baseline and design.
- Options: dynamic LCA (preferred by CLF), Module D (end-of-life recycling), or exclusion (if both studies exclude).
- Reuse materials receive credit for avoided emissions but require chain-of-custody documentation.

### Version History
- **v1.0.0** (2024): Initial release supporting LEED v5 MRc2 Option 1 (percentage reduction) and Option 2 (GWP thresholds).
