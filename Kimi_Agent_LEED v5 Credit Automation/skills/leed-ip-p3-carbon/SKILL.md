---
name: leed-ip-p3-carbon
version: 1.0.0
author: LEED Automation Platform
description: Automates IPp3 Carbon Assessment 25-year emissions projection from operational, refrigerant, and embodied carbon sources.
---

## Metadata
- **Credit Code:** IPp3
- **Credit Name:** Carbon Assessment
- **Points:** Required (Prerequisite)
- **Automation Level:** 92.5%
- **Complexity:** Low
- **Primary Data Source:** EPA eGRID, EC3 Database API, IPCC emission factors
- **HITL Required:** Yes

## Purpose
This skill automates the generation of a 25-year carbon emissions projection for a LEED project by aggregating operational carbon (electricity/fuel), refrigerant emissions (leakage), and embodied carbon (materials), then producing submission-ready documents for the IPp3 prerequisite.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `project_id` | string | USGBC Arc Platform | UUID v4 format, must be active project |
| `eap1_energy_model` | dict | EAp1 skill output | Must contain `annual_kwh` (number ≥ 0) and `fuel_breakdown` (array) |
| `eap5_refrigerant_inventory` | array | EAp5 skill output | Each item must have `refrigerant_type` (string), `charge_kg` (number ≥ 0), `annual_leak_rate_pct` (number 0–100) |
| `mrp2_material_quantities` | array | MRp2 skill output | Each item must have `material_id` (string), `quantity` (number > 0), `unit` (string), `epd_id` (string, optional) |
| `project_location` | dict | Project registration | Must contain `zip_code` (string, US 5-digit) or `latitude`/`longitude` (float), `country` (ISO 3166-1 alpha-2) |
| `building_service_life_years` | integer | Project brief | Range 25–100, default 25 for IPp3 projection |
| `ltc4_transportation_data` | dict | LTc4 skill output (optional but recommended) | `annual_vmt_reduction` (number), `commuter_co2_per_mile` (number) |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `projection_horizon_years` | integer | 25 | Number of years for carbon projection (IPp3 requires 25) |
| `grid_emission_factor_override` | float | null | kg CO₂/kWh; used instead of eGRID lookup for international projects |
| `embodied_carbon_method` | string | "ec3" | Source for GWP factors: `"ec3"`, `"oneclicklca"`, `"static_ipcc"` |
| `discount_rate_pct` | float | 0.0 | Social cost of carbon discount rate for NPV-style analysis |
| `include_transportation` | boolean | true | Whether to include LTc4 transportation emissions in total |
| `decarbonization_scenario` | string | "bau" | `"bau"` (business-as-usual), `"moderate"`, or `"aggressive"` for pathway doc |
| `report_template_id` | string | "ip-p3-default" | USGBC report template identifier |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:** Validates all required fields, checks cross-references to EAp1/EAp5/MRp2/LTc4 data, confirms `project_location` resolves to a known grid region (US via ZIP or lat/lon), and ensures `building_service_life_years` ≥ `projection_horizon_years`. For non-US projects, requires `grid_emission_factor_override`.
- **Output:** `ValidatedInput` object with normalized units (kWh, kg, metric tons).
- **On Failure:** Raise `InputValidationError` with detailed field-level messages; retry not possible (fix input and re-trigger).

### Step 2: Fetch Grid Emission Factor (eGRID)
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. If `project_location.country == "US"` and `grid_emission_factor_override` is null:
     - Map ZIP code or lat/lon to eGRID subregion using EPA eGRID lookup service: `GET https://www.epa.gov/egrid/egrid-mapping` (or local cached mapping table updated annually).
     - Retrieve `CO2e emission rate (lb/MWh)` for the subregion from EPA eGRID summary file (latest year, e.g., 2022).
     - Convert to kg CO₂/kWh: `grid_factor = (lb/MWh × 0.453592) / 1000`.
  2. If international or override provided: use `grid_emission_factor_override` directly.
- **Output:** `grid_factor_kg_co2_per_kwh` (float), `egrid_subregion` (string or null), `data_year` (int).
- **On Failure:** If EPA mapping fails, fallback to US average eGRID factor (0.417 kg CO₂/kWh per 2022 national average) and flag for HITL review.

### Step 3: Fetch Embodied Carbon Factors (EC3 / One Click LCA / IPCC)
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  - If `embodied_carbon_method == "ec3"`:
    - Authenticate to EC3 Database API: `POST https://api.buildingtransparency.org/api/auth/token` with API key.
    - For each material in `mrp2_material_quantities`, query: `GET https://api.buildingtransparency.org/api/materials?search={material_id}&epd_id={epd_id}`.
    - Extract `gwp_per_unit` (kg CO₂e per declared unit) and `unit` from the best-matched EPD.
  - If `embodied_carbon_method == "oneclicklca"`:
    - Authenticate to One Click LCA API: `POST https://api.oneclicklca.com/v1/auth/token` with license credentials.
    - Batch query materials via `POST https://api.oneclicklca.com/v1/materials/search` with material list.
    - Extract `gwp_total_a1_a3` (kg CO₂e per unit) for each material.
  - If `embodied_carbon_method == "static_ipcc"`:
    - Use bundled IPCC 2019 Refinement/AR6 GWP100 factors for common construction materials (concrete, steel, timber, aluminum, glass, insulation).
- **Output:** Array of `EmbodiedCarbonFactor` objects: `{ material_id, gwp_kg_co2e_per_unit, matched_epd_id, confidence_score }`.
- **On Failure:** If EC3/One Click LCA API fails for a material, fallback to static IPCC factor if available; if unavailable, mark material for HITL resolution.

### Step 4: Calculate Operational Carbon
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  - From `eap1_energy_model.annual_kwh`, compute annual operational CO₂:
    ```
    annual_operational_co2_tons = (annual_kwh × grid_factor_kg_co2_per_kwh) / 1000
    ```
  - Multiply by `projection_horizon_years`:
    ```
    total_operational_co2_tons = annual_operational_co2_tons × projection_horizon_years
    ```
  - If fuel breakdown includes on-site fossil fuels (natural gas, fuel oil, propane), add:
    ```
    annual_fuel_co2_tons = Σ( fuel_annual_therms_or_gallons × fuel_emission_factor_kg_per_unit ) / 1000
    ```
    using EPA GHG emission factors for stationary combustion (e.g., natural gas: 53.07 kg CO₂/MMBtu = 0.00531 kg CO₂/therm).
- **Output:** `OperationalCarbonResult` with `annual_tons`, `total_25yr_tons`, `fuel_breakdown_tons`.
- **On Failure:** Calculation errors raise `CalculationError`; retry with sanitized inputs once.

### Step 5: Calculate Refrigerant Carbon
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  - For each refrigerant in `eap5_refrigerant_inventory`:
    - Look up GWP100 from IPCC AR6 Table 7.SM.7 (or ASHRAE Standard 34 addendum) by `refrigerant_type`.
    - Compute annual leakage:
      ```
      annual_leak_kg = charge_kg × (annual_leak_rate_pct / 100)
      ```
    - Compute annual CO₂e:
      ```
      annual_refrigerant_co2e_tons = (annual_leak_kg × gwp100) / 1000
      ```
  - Sum across all refrigerants and multiply by `projection_horizon_years`:
    ```
    total_refrigerant_co2e_tons = Σ(annual_refrigerant_co2e_tons) × projection_horizon_years
    ```
- **Output:** `RefrigerantCarbonResult` with `annual_tons`, `total_25yr_tons`, `by_refrigerant` array.
- **On Failure:** Unknown refrigerant type raises `RefrigerantLookupError`; flag for HITL.

### Step 6: Calculate Embodied Carbon
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  - For each material in `mrp2_material_quantities`:
    ```
    material_embodied_co2_tons = (quantity × gwp_kg_co2e_per_unit) / 1000
    ```
  - Sum across all materials:
    ```
    total_embodied_co2_tons = Σ(material_embodied_co2_tons)
    ```
  - Note: Embodied carbon is typically assessed once (at construction), not annualized. For the 25-year projection, embodied carbon is reported as a single upfront value, not multiplied by 25. This is consistent with USGBC IPp3 guidance.
- **Output:** `EmbodiedCarbonResult` with `total_tons`, `by_material` array, `data_source`.
- **On Failure:** Mismatched units raise `UnitConversionError`; attempt automatic unit conversion via `pint`; if impossible, flag for HITL.

### Step 7: Aggregate Total 25-Year Projection
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  - Sum the three emission streams:
    ```
    total_25yr_co2_tons = total_operational_co2_tons + total_refrigerant_co2e_tons + total_embodied_co2_tons
    ```
  - If `include_transportation == true` and LTc4 data present:
    ```
    transportation_annual_tons = (annual_vmt_reduction × commuter_co2_per_mile) / 1000 × -1   # negative = reduction
    transportation_25yr_tons = transportation_annual_tons × projection_horizon_years
    total_25yr_co2_tons += transportation_25yr_tons
    ```
  - Compute percentage contributions:
    ```
    pct_operational = total_operational_co2_tons / total_25yr_co2_tons × 100
    pct_refrigerant = total_refrigerant_co2e_tons / total_25yr_co2_tons × 100
    pct_embodied = total_embodied_co2_tons / total_25yr_co2_tons × 100
    ```
- **Output:** `CarbonProjectionSummary` object with totals, percentages, and per-year breakdown array.
- **On Failure:** Division by zero (all zeros) returns zeroed summary with warning flag.

### Step 8: HITL Review Checkpoint — LEED Consultant Verification
- **Type:** Human Review
- **Automated:** No
- **Description:** Pause workflow and present a structured review package to the assigned LEED consultant. Package includes: (a) energy model input summary and grid factor used, (b) refrigerant inventory with GWP values and leak rates, (c) material quantities with matched EPDs and GWP factors, (d) calculated totals with pie-chart visualization, (e) flagged items (fallback factors, unit mismatches, missing EPDs). Consultant approves, requests edits, or rejects with comments.
- **Output:** `HITLReviewResult` with `status` ∈ {`approved`, `revisions_requested`, `rejected`}, `reviewer_id`, `timestamp`, `comments`.
- **On Failure:** If SLA exceeded (72 hours), auto-escalate to senior reviewer and send reminder. If rejected, return to Step 4/5/6 depending on comment scope.

### Step 9: Generate Decarbonization Pathway Document
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  - Based on `decarbonization_scenario`, generate strategies:
    - **BAU:** No interventions; projection flat.
    - **Moderate:** 2% annual grid decarbonization (eGRID trend), 20% refrigerant leak reduction, 10% embodied carbon offset via material substitution.
    - **Aggressive:** 5% annual grid decarbonization, 50% leak reduction + low-GWP refrigerant retrofit, 30% embodied carbon reduction via mass timber/lower-carbon concrete.
  - Compute revised 25-year totals for each scenario.
  - Render PDF using Jinja2 template + WeasyPrint / ReportLab. Template ID: `decarbonization-pathway-v1`.
- **Output:** `decarbonization_pathway.pdf` (file path), `pathway_summary` dict.
- **On Failure:** If PDF generation fails, output Markdown intermediate and retry generation once.

### Step 10: Generate 25-Year Carbon Projection Report
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  - Compile all results into USGBC-formatted report:
    - Cover page with project ID, date, consultant name.
    - Section 1: Executive summary with total 25-year CO₂e (metric tons).
    - Section 2: Operational carbon methodology and annual breakdown table.
    - Section 3: Refrigerant carbon methodology and equipment-level table.
    - Section 4: Embodied carbon methodology with material-level EPD references.
    - Section 5: Transportation carbon (if included).
    - Section 6: Total projection graph (stacked bar per year).
    - Appendix: Raw data tables and API source citations.
  - Render PDF using Jinja2 template + WeasyPrint. Template ID from `report_template_id`.
- **Output:** `carbon_projection_report.pdf` (file path), `report_metadata` dict.
- **On Failure:** If template missing, fallback to base template and log warning.

### Step 11: Generate Calculation Spreadsheet
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  - Create XLSX with multiple worksheets:
    - `Inputs`: All raw inputs (energy model, refrigerants, materials, location).
    - `Grid Factor`: eGRID subregion, conversion math, source URL.
    - `Operational`: Year-by-year electricity and fuel CO₂.
    - `Refrigerant`: Per-system charge, leak rate, GWP, annual and total CO₂e.
    - `Embodied`: Material quantities, units, GWP per unit, total CO₂e, EPD IDs, EC3/One Click LCA URLs.
    - `Transportation`: VMT reduction, CO₂ per mile, annual and total.
    - `Summary`: Totals, percentages, chart data.
  - Use `openpyxl` with formulas (not static values) so reviewers can audit.
- **Output:** `carbon_calculation.xlsx` (file path).
- **On Failure:** If `openpyxl` fails, fallback to CSV bundle (zip of CSVs).

### Step 12: Submit to USGBC Arc Platform
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  - Authenticate: `POST https://api.usgbc.org/v3/auth/token` (OAuth 2.0 client credentials flow).
  - Upload documents: `POST https://api.usgbc.org/v3/projects/{project_id}/credits/IPp3/documents` with multipart/form-data for PDFs and XLSX.
  - Submit credit narrative: `POST https://api.usgbc.org/v3/projects/{project_id}/credits/IPp3/submission` with JSON body:
    ```json
    {
      "credit_code": "IPp3",
      "status": "submitted",
      "narrative": "Automated 25-year carbon projection...",
      "total_25yr_co2_tons": <value>,
      "operational_tons": <value>,
      "refrigerant_tons": <value>,
      "embodied_tons": <value>,
      "document_ids": [<ids>]
    }
    ```
- **Output:** `ArcSubmissionResult` with `submission_id`, `status`, `document_ids`.
- **On Failure:** If Arc API returns 4xx/5xx, queue for retry with exponential backoff (max 3 retries); notify project admin on final failure.

### Step 13: Finalize and Notify
- **Type:** API Call / Notification
- **Automated:** Yes
- **Description:**
  - Log completion to audit trail.
  - Send notification to project team: email + Slack/Teams webhook with summary:
    - Total 25-year CO₂e (tons)
    - Breakdown percentages
    - Link to Arc platform submission
    - HITL reviewer name and approval timestamp
  - Persist all intermediate artifacts to project data store (S3 / GCS / Azure Blob) with 7-year retention.
- **Output:** `CompletionSummary` object.
- **On Failure:** Notification failures are logged but non-blocking; retry once after 5 minutes.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 8: LEED Consultant Verification | LEED AP BD+C or O+M (consultant role) | 72 hours | (1) Confirm energy model `annual_kwh` matches design-intent or as-built energy model. (2) Verify refrigerant types, charges, and leak rates against mechanical schedules or commissioning reports. (3) Confirm material quantities and EPD matches reflect actual construction (not just design estimates). (4) Validate grid emission factor — check eGRID subregion matches project ZIP/lat-lon. (5) Review any fallback/static factors flagged by automation and approve or replace with project-specific data. (6) Confirm 25-year horizon and service life assumptions. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| EPA eGRID | Grid emission factors by US subregion | US only | US national average factor (0.417 kg CO₂/kWh, 2022) | Public CSV download (no rate limit); mapping service: 100 req/min |
| EC3 Database API | Embodied carbon EPD data for materials | Global (EPD coverage varies by region) | Static IPCC AR6 material factors bundled in skill | 1,000 req/day (free tier); 10,000 req/day (paid tier) |
| One Click LCA API | LCA calculations and material GWP | Global | EC3 API or static IPCC factors | License-dependent; typically 5,000 req/month |
| USGBC Arc Platform API | Project data submission and document upload | Global (all LEED-registered projects) | Manual upload via Arc web UI | 100 req/min per OAuth client |
| IPCC AR6 Static Factors | Refrigerant GWP100, combustion emission factors | Global (reference data) | N/A — bundled locally | N/A (local lookup table) |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | Full eGRID integration; all APIs operational. |
| Canada | Available | eGRID fallback to Canadian grid factors (Environment Canada National Pollutant Release Inventory or provincial utilities); EC3 EPD coverage good for North American products. |
| European Union | Available | No eGRID; use `grid_emission_factor_override` with EU EEA/ENTSO-E factors or national TSO data. EC3 and One Click LCA have strong EU EPD coverage. |
| United Kingdom | Available | No eGRID; use UK BEIS/Defra grid factors. EC3/One Click LCA coverage strong. |
| Australia / New Zealand | Available | No eGRID; use NGER/NZEI grid factors. EC3 coverage limited; One Click LCA preferred. |
| Asia-Pacific (excl. AU/NZ) | Limited | Grid factors must be overridden. EC3 EPD coverage limited; One Click LCA or static IPCC recommended. |
| Middle East / Africa | Limited | Grid factors must be overridden. EC3/One Click LCA coverage sparse; static IPCC fallback heavily relied upon. |
| Latin America | Limited | Grid factors must be overridden. EPD databases growing; static IPCC fallback common. |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Input validation failure | Halt workflow; return detailed error object to caller | Yes (project admin email) | No (fix input) |
| EPA eGRID mapping unavailable | Use US national average; flag for HITL | No (logged only) | 3× with 5-min backoff |
| EC3 API authentication failure | Switch to One Click LCA if configured; else static IPCC | Yes (if both APIs fail) | 2× then fallback |
| One Click LCA API failure | Switch to EC3 if configured; else static IPCC | Yes (if both APIs fail) | 2× then fallback |
| Unknown refrigerant type | Use closest ASHRAE match; flag for HITL | No (flag in review package) | No |
| Unit conversion failure (materials) | Flag material for HITL; skip in sum | No (flag in review package) | No |
| HITL SLA exceeded (72h) | Escalate to senior reviewer; auto-reminder | Yes (escalation email) | N/A |
| PDF generation failure | Output Markdown intermediate; retry generation once | No | 1× |
| Arc Platform API 5xx | Queue submission; exponential backoff | Yes (on final failure) | 3× |
| Arc Platform API 401/403 | Refresh OAuth token; retry once; else notify admin | Yes | 1× then HITL |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| 25-Year Carbon Projection Report | PDF | USGBC-formatted narrative report with methodology, calculations, tables, and year-by-year stacked bar chart. Submitted to Arc. |
| Decarbonization Pathway Document | PDF | Scenario-based report showing BAU, moderate, and aggressive decarbonization interventions with revised 25-year totals. |
| Calculation Spreadsheet | XLSX | Multi-worksheet audit file with all inputs, formulas, EPD references, and summary. Enables third-party verification. |

## Testing
```bash
# Run all unit and integration tests for the IPp3 skill
python -m pytest skills/ip-p3-carbon/tests/ -v --tb=short

# Specific test suites
python -m pytest skills/ip-p3-carbon/tests/test_validation.py
python -m pytest skills/ip-p3-carbon/tests/test_egrid_lookup.py
python -m pytest skills/ip-p3-carbon/tests/test_ec3_api.py
python -m pytest skills/ip-p3-carbon/tests/test_calculations.py
python -m pytest skills/ip-p3-carbon/tests/test_document_generation.py
python -m pytest skills/ip-p3-carbon/tests/test_arc_submission.py
python -m pytest skills/ip-p3-carbon/tests/test_hitl_checkpoint.py
```

## Example Usage (Deer-Flow)
```python
from deerflow.skills import IPp3CarbonSkill

skill = IPp3CarbonSkill(
    project_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    inputs={
        "eap1_energy_model": {
            "annual_kwh": 450000,
            "fuel_breakdown": [
                {"fuel": "natural_gas", "annual_therms": 12000},
                {"fuel": "fuel_oil_2", "annual_gallons": 0}
            ]
        },
        "eap5_refrigerant_inventory": [
            {"refrigerant_type": "R-410A", "charge_kg": 85.0, "annual_leak_rate_pct": 3.5},
            {"refrigerant_type": "R-134a", "charge_kg": 12.0, "annual_leak_rate_pct": 2.0}
        ],
        "mrp2_material_quantities": [
            {"material_id": "ready_mix_concrete_3000psi", "quantity": 850.0, "unit": "m3", "epd_id": "EPD-CON-2023-001"},
            {"material_id": "structural_steel_w_section", "quantity": 42000.0, "unit": "kg", "epd_id": "EPD-STL-2022-044"},
            {"material_id": "softwood_lumber_dimensional", "quantity": 18000.0, "unit": "kg", "epd_id": None}
        ],
        "project_location": {"zip_code": "90210", "country": "US"},
        "building_service_life_years": 50,
        "ltc4_transportation_data": {
            "annual_vmt_reduction": 45000,
            "commuter_co2_per_mile": 0.404
        },
        "projection_horizon_years": 25,
        "embodied_carbon_method": "ec3",
        "decarbonization_scenario": "moderate",
        "include_transportation": True
    }
)

result = await skill.execute()

# result structure:
# {
#   "total_25yr_co2_tons": 2847.3,
#   "operational_tons": 2341.5,
#   "refrigerant_tons": 185.2,
#   "embodied_tons": 320.6,
#   "transportation_tons": 0.0,  # reduction, may be negative
#   "documents": {
#       "projection_report": "/path/to/carbon_projection_report.pdf",
#       "pathway_document": "/path/to/decarbonization_pathway.pdf",
#       "calculation_spreadsheet": "/path/to/carbon_calculation.xlsx"
#   },
#   "arc_submission_id": "sub_987654321",
#   "hitl_approved_by": "reviewer_id_42",
#   "hitl_approved_at": "2025-01-15T09:30:00Z"
# }
```

## Deer-Flow Workflow (LangGraph)
```python
from langgraph.graph import StateGraph, END
from deerflow.skills.ip_p3_carbon.state import IPp3State
from deerflow.skills.ip_p3_carbon.nodes import (
    validate_inputs,
    fetch_egrid_factor,
    fetch_embodied_factors,
    calculate_operational_carbon,
    calculate_refrigerant_carbon,
    calculate_embodied_carbon,
    aggregate_projection,
    hitl_leed_consultant_review,
    generate_decarbonization_pathway,
    generate_projection_report,
    generate_calculation_spreadsheet,
    submit_to_arc_platform,
    finalize_and_notify
)

workflow = StateGraph(IPp3State)

# Add nodes
workflow.add_node("validate", validate_inputs)
workflow.add_node("fetch_grid", fetch_egrid_factor)
workflow.add_node("fetch_embodied", fetch_embodied_factors)
workflow.add_node("calc_operational", calculate_operational_carbon)
workflow.add_node("calc_refrigerant", calculate_refrigerant_carbon)
workflow.add_node("calc_embodied", calculate_embodied_carbon)
workflow.add_node("aggregate", aggregate_projection)
workflow.add_node("hitl_review", hitl_leed_consultant_review)
workflow.add_node("gen_pathway", generate_decarbonization_pathway)
workflow.add_node("gen_report", generate_projection_report)
workflow.add_node("gen_spreadsheet", generate_calculation_spreadsheet)
workflow.add_node("arc_submit", submit_to_arc_platform)
workflow.add_node("finalize", finalize_and_notify)

# Define edges
workflow.set_entry_point("validate")
workflow.add_edge("validate", "fetch_grid")
workflow.add_edge("fetch_grid", "fetch_embodied")

# Parallel calculation branches after data fetching
workflow.add_edge("fetch_embodied", "calc_operational")
workflow.add_edge("fetch_embodied", "calc_refrigerant")
workflow.add_edge("fetch_embodied", "calc_embodied")

# Join calculations
workflow.add_edge("calc_operational", "aggregate")
workflow.add_edge("calc_refrigerant", "aggregate")
workflow.add_edge("calc_embodied", "aggregate")

# HITL checkpoint
workflow.add_edge("aggregate", "hitl_review")

# Conditional routing from HITL
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: state["hitl_status"],
    {
        "approved": "gen_pathway",
        "revisions_requested": "validate",   # loop back to re-calculate
        "rejected": END                      # terminate with failure
    }
)

# Document generation (parallelizable)
workflow.add_edge("gen_pathway", "gen_report")
workflow.add_edge("gen_report", "gen_spreadsheet")
workflow.add_edge("gen_spreadsheet", "arc_submit")
workflow.add_edge("arc_submit", "finalize")
workflow.add_edge("finalize", END)

# Compile
app = workflow.compile()

# Execution
# final_state = await app.ainvoke(initial_state)
```

## Implementation Notes

### Bundled Static Data
The skill ships with the following local lookup tables (updated annually via CI/CD):
- `data/egrid_subregion_map.json`: ZIP code → eGRID subregion mapping (US Census ZCTA to eGRID 2022).
- `data/ipcc_ar6_refrigerant_gwp.json`: Refrigerant type → GWP100 (IPCC AR6 Table 7.SM.7).
- `data/ipcc_2019_combustion_factors.json`: Fuel type → kg CO₂ per unit (therm, gallon, liter, MMBtu).
- `data/ipcc_material_gwp_fallback.json`: Material category → kg CO₂e per kg (IPCC AR6/2019 refinement for concrete, steel, timber, aluminum, glass, insulation).

### Versioning & Data Freshness
- eGRID data: refreshed annually each January after EPA publication. Skill version bumped if schema changes.
- EC3/One Click LCA: dynamic via API; no local caching beyond 24-hour TTL for identical queries.
- IPCC factors: updated only when IPCC publishes new assessment report.

### Security & Compliance
- API keys (EC3, One Click LCA, USGBC Arc) are injected via environment variables / secrets manager. Never committed to repository.
- All PII (project location) is encrypted at rest and in transit.
- Audit logs retain all calculation inputs, API responses, and HITL decisions for 7 years per LEED documentation retention requirements.

### Performance Targets
- End-to-end automated execution (excluding HITL): < 90 seconds for typical projects (< 100 materials, < 20 refrigerant systems).
- HITL checkpoint: 72-hour SLA with auto-escalation.
- Document generation: < 30 seconds for all three output files.
