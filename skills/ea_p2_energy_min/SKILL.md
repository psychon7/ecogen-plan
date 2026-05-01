---
name: leed-ea-p2-energy-min
description: Generate LEED v5 EAp2 Minimum Energy Efficiency compliance documentation package from energy model outputs provided by a consultant or energy modeler.
version: 1.0.0
author: LEED Automation Platform
---

## Metadata
- **Credit Code:** EAp2
- **Credit Name:** Minimum Energy Efficiency
- **Points:** Required (Prerequisite)
- **Automation Level:** 85.7% (documentation automation only — energy modeling itself is NOT automated)
- **Complexity:** Medium
- **Primary Data Source:** Energy model output files (.eso, .csv, .htm, .xml) provided by energy modeler + ASHRAE 90.1-2022 static reference
- **HITL Required:** Yes

---

## Purpose
Automate the generation of the complete LEED v5 EAp2 Minimum Energy Efficiency compliance documentation package—including ASHRAE 90.1-2022 Appendix G performance rating method reports, energy performance summaries, and end-use breakdown comparisons—from raw energy model outputs provided by the project's energy modeler or MEP consultant.

> **CRITICAL BOUNDARY:** This skill does **NOT** perform energy modeling, simulation, or baseline/proposed model creation. It strictly parses, validates, calculates, and documents results from energy model outputs that must be created separately by a qualified energy modeler using EnergyPlus, eQuest, TRACE 700, IES VE, or equivalent software.

---

## Inputs (Required)

| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `proposed_model_eso` | File (`.eso`) | Energy modeler | File exists, size > 1 KB, valid EnergyPlus output format |
| `proposed_model_csv` | File (`.csv`) | Energy modeler | Contains `Date/Time` and at least 5 end-use columns |
| `proposed_model_htm` | File (`.htm`/`.html`) | Energy modeler | Contains "Annual Building Utility Performance Summary" table |
| `baseline_model_eso` | File (`.eso`) | Energy modeler | File exists, size > 1 KB, valid EnergyPlus output format |
| `baseline_model_csv` | File (`.csv`) | Energy modeler | Contains `Date/Time` and at least 5 end-use columns |
| `baseline_model_htm` | File (`.htm`/`.html`) | Energy modeler | Contains "Annual Building Utility Performance Summary" table |
| `building_gross_floor_area_sqft` | Float | Project team | > 0, matches model reported GSA within ±2% |
| `climate_zone` | String | Project team | Valid ASHRAE 90.1-2022 climate zone (e.g., "4A", "5B", "7") |
| `building_type` | String | Project team | Valid ASHRAE 90.1-2022 Appendix G building prototype (e.g., "SmallOffice", "LargeHotel", "MidriseApartment") |
| `energy_modeler_name` | String | Project team | Non-empty, < 100 chars |
| `energy_modeler_email` | String | Project team | Valid email format |
| `modeling_software` | String | Energy modeler | One of: `EnergyPlus`, `eQuest`, `TRACE_700`, `IES_VE`, `HAP`, `OpenStudio`, `Other` |
| `ashrae_90_1_version` | String | Project team | Default `"90.1-2022"`; must be `"90.1-2022"` or `"90.1-2019"` for v5 |
| `utility_rate_tariff` | File (`.json`/`.csv`) | Project team | Valid tariff structure with `$/kWh`, `$/kW`, `$/therm` rates; required for cost-based PRM |

---

## Inputs (Optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `proposed_model_xml` | File (`.xml`) | `null` | EnergyPlus XML output (for detailed HVAC component data) |
| `baseline_model_xml` | File (`.xml`) | `null` | EnergyPlus XML output (for detailed HVAC component data) |
| `ies_ve_results` | File (`.csv`/`.db`) | `null` | IES VE ApacheSim results export (if `modeling_software` = `IES_VE`) |
| `trace_700_report` | File (`.pdf`/`.xlsx`) | `null` | TRACE 700 export file (if `modeling_software` = `TRACE_700`) |
| `equest_lv` | File (`.lv`/`.sim`) | `null` | eQuest LV/SIM output file (if `modeling_software` = `eQuest`) |
| `on_site_renewable_kwh` | Float | `0.0` | Annual on-site renewable energy generation (kWh); subtracted from proposed cost per ASHRAE 90.1-2022 G2.4 |
| `purchased_renewable_kwh` | Float | `0.0` | Annual purchased renewable energy (kWh); used for cost calculations only |
| `unregulated_energy_included` | Boolean | `false` | Whether model includes unregulated loads (parking, exterior) per 90.1-2022 G3.1.1 |
| `exceptional_calculation_method` | File (`.pdf`/`.docx`) | `null` | Documentation for any exceptional calculation methods used per 90.1-2022 Appendix G |
| `recurring_mandates` | Array[String] | `[]` | List of project-specific recurring mandates (e.g., `["G3.1.2.8 Elevator Exception", "G3.1.2.11 Process Load Exception"]`) |
| `designed_vs_baseline_hvac_table` | File (`.csv`/`.xlsx`) | `null` | Manual override table for HVAC system mapping if auto-mapping fails |
| `project_timezone` | String | `"UTC"` | Timezone for timestamp alignment (e.g., `"America/New_York"`) |
| `currency_code` | String | `"USD"` | Currency for cost calculations (`USD`, `CAD`, `EUR`, etc.) |
| `demand_cost_explanation` | String | `""` | Narrative explaining demand charge methodology if non-standard |
| `project_name` | String | `""` | Project name for report headers |
| `project_address` | String | `""` | Project address for report headers |
| `leed_review_comments` | File (`.pdf`/`.docx`) | `null` | Previous GBCI review comments to address in narrative |
| `hitl_sla_hours` | Integer | `72` | SLA for HITL checkpoint turnaround (hours) |

---

## Workflow Steps (Durable)

### Step 1: Input Validation
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. Verify all required input files exist and are non-empty.
  2. Validate file extensions match declared `modeling_software`.
  3. Check `building_gross_floor_area_sqft` is numeric and > 0.
  4. Validate `climate_zone` against ASHRAE 90.1-2022 climate zone enum: `"0A"`–`"0B"`, `"1A"`–`"1B"`, `"2A"`–`"2B"`, `"3A"`–`"3C"`, `"4A"`–`"4C"`, `"5A"`–`"5C"`, `"6A"`–`"6B"`, `"7"`, `"8"`.
  5. Validate `building_type` against 90.1-2022 Appendix G prototype enum.
  6. Verify `.htm` files contain expected EnergyPlus report section anchors (e.g., `Annual Building Utility Performance Summary`, `End Uses`).
  7. Verify `.eso` files contain valid EnergyPlus output variable headers.
  8. Parse `.csv` files and confirm presence of minimum required columns: `Date/Time`, `Heating:Electricity`, `Cooling:Electricity`, `InteriorLights:Electricity`, `InteriorEquipment:Electricity`, `Fans:Electricity`, `Pumps:Electricity`, `HeatRejection:Electricity`, `Humidification:Electricity`, `HeatRecovery:Electricity`, `WaterSystems:Electricity`, `ExteriorLights:Electricity`, `ExteriorEquipment:Electricity` (or equivalent end-use labels).
  9. Validate `utility_rate_tariff` JSON/CSV contains at least one rate schedule with `energy_rate`, `demand_rate`, and `fuel_rates`.
  10. Cross-check proposed vs. baseline model reported building area; flag if difference > 2%.
- **Output:** `validation_report` (JSON) with `valid: bool`, `errors: List[str]`, `warnings: List[str]`, `file_checksums: Dict[str, str]`.
- **On Failure:** Halt workflow, return `validation_report` to caller. Do not proceed to Step 2.

---

### Step 2: Energy Model Output Parsing
- **Type:** API Call / File Processing
- **Automated:** Yes
- **Description:**
  1. **EnergyPlus branch** (if `modeling_software` in `[EnergyPlus, OpenStudio]`):
     - Use `eppy` (`readhtml.readhtml`) or custom parser to extract tables from `.htm`:
       - `Site and Source Energy`
       - `End Uses`
       - `End Uses By Subcategory`
       - `Utility Use Per Conditioned Floor Area`
       - `Energy Cost Summary`
     - Use `esoreader` or custom ESO parser to read `.eso` into pandas DataFrames keyed by report variable name.
     - Read `.csv` with `pandas.read_csv`; parse `Date/Time` into `DatetimeIndex` using `project_timezone`.
     - Extract annual sums for each end-use fuel type (Electricity, Natural Gas, District Heating, District Cooling, Water, Fuel Oil, Propane, Coal, Steam).
     - Extract peak demand values (kW) per utility type.
  2. **eQuest branch** (if `modeling_software == eQuest`):
     - Parse `.lv` or `.sim` file using `equest-parser` or custom regex-based parser.
     - Extract `BEPU` (Building Energy Performance Summary) table data.
     - Map eQuest end-use categories to ASHRAE 90.1 Appendix G end-use categories.
  3. **TRACE 700 branch** (if `modeling_software == TRACE_700`):
     - Parse PDF report using `pdfplumber` or `camelot` to extract `Energy Cost Budget` and `Design Energy Cost` tables.
     - Or read `.xlsx` export directly if provided in `trace_700_report`.
  4. **IES VE branch** (if `modeling_software == IES_VE`):
     - Read `ies_ve_results` CSV/DB and map ApacheSim output variables to 90.1 end-use categories.
  5. Normalize all energy values to common units: **kWh** for electricity, **therms** for natural gas, **kWh** for district energy.
  6. Compute site energy totals and source energy totals using ASHRAE 90.1-2022 Table D.2.1 source energy factors (Electricity: 2.05, Natural Gas: 1.01, District Heating: 1.20, District Cooling: 1.19, etc.).
  7. Apply `on_site_renewable_kwh` deduction from proposed model electricity per 90.1-2022 Section G2.4.
- **Output:** `parsed_model_data` (JSON) containing:
  - `proposed`: `{annual_end_uses: Dict, peak_demands: Dict, total_site_energy_kbtu: float, total_source_energy_kbtu: float, total_energy_cost_usd: float, model_reported_gross_floor_area: float}`
  - `baseline`: Same structure as `proposed`
  - `unit_conversions_applied: Dict[str, str]`
  - `source_energy_factors_used: Dict[str, float]`
- **On Failure:** Log parser error, attempt fallback parser. If both fail, raise `ModelParseError` and notify project team.

---

### Step 3: Energy Cost Calculation
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Load `utility_rate_tariff`.
  2. For each fuel type in parsed data, apply the appropriate energy rate ($/kWh, $/therm, $/gal, etc.) to annual consumption.
  3. For each fuel type with demand charges, apply demand rate ($/kW or $/kVA) to monthly or annual peak demand.
  4. If tariff has time-of-use (TOU) or seasonal blocks, aggregate hourly or monthly consumption from `.csv` time series to match tariff periods.
  5. Sum across all fuels to get:
     - `Baseline Energy Cost` = sum(baseline fuel costs + baseline demand charges)
     - `Proposed Energy Cost` = sum(proposed fuel costs + proposed demand charges) – `on_site_renewable_kwh` × applicable energy rate
  6. If `currency_code != "USD"`, convert using ECB or OANDA daily rates API (store rate used and timestamp).
  7. Round to 2 decimal places.
- **Output:** `energy_cost_summary` (JSON) with:
  - `baseline_total_usd: float`
  - `proposed_total_usd: float`
  - `cost_savings_usd: float`
  - `percent_better_than_baseline: float`
  - `fuel_cost_breakdown: Dict[str, Dict]`
  - `demand_cost_breakdown: Dict[str, Dict]`
  - `currency: str`
  - `exchange_rate: float | null`
- **On Failure:** If tariff is malformed or missing a fuel type, flag for HITL review with specific missing rate.

---

### Step 4: Compliance Calculation
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Calculate **Percent Better Than Baseline**:
     ```
     pct_better = ((baseline_energy_cost - proposed_energy_cost) / baseline_energy_cost) × 100
     ```
  2. For EAp2 (prerequisite), verify:
     - `pct_better >= 0.0` (proposed cost ≤ baseline cost)
  3. Compute end-use breakdown comparison table:
     - For each end-use category (Heating, Cooling, Lighting, Fans, Pumps, Heat Rejection, Humidification, Heat Recovery, Water Systems, Exterior Lighting, Exterior Equipment, Refrigeration, Cooking, Process), calculate:
       - Proposed annual energy (kWh or kBtu)
       - Baseline annual energy (kWh or kBtu)
       - Difference (Proposed – Baseline)
       - Percent difference from baseline
  4. Flag any end-use where proposed > baseline by > 10% as a potential modeling error or exception.
  5. Verify `model_reported_gross_floor_area` for both models matches `building_gross_floor_area_sqft` within ±2%; flag discrepancy.
  6. Check for mandatory minimums per 90.1-2022 Section G1.2.2 (e.g., baseline HVAC auto-size vs. proposed).
  7. Generate `compliance_status`: `"COMPLIANT"` if `pct_better >= 0`, else `"NON_COMPLIANT"`.
- **Output:** `compliance_calculation` (JSON) with:
  - `pct_better_than_baseline: float`
  - `compliance_status: str`
  - `end_use_comparison: List[Dict]`
  - `area_discrepancy_flag: bool`
  - `end_use_anomaly_flags: List[str]`
  - `minimum_requirements_check: Dict[str, bool]`
- **On Failure:** If baseline cost is 0 or negative, raise `CalculationError` and notify energy modeler.

---

### Step 5: HITL Checkpoint 1 — Energy Modeler Verification
- **Type:** Human Review
- **Automated:** No
- **Description:**
  Present the parsed energy model data and preliminary calculations to the **energy modeler** for verification:
  - Show summary of parsed values from `.eso`/`.csv`/`.htm`.
  - Display `Baseline Energy Cost`, `Proposed Energy Cost`, `Percent Better Than Baseline`.
  - Show end-use comparison table.
  - Flag any parser warnings or area discrepancies.
  - Ask modeler to confirm:
    1. Parsed values match their original model outputs.
    2. Baseline/proposed HVAC system mappings are correct.
    3. Any exceptional calculation methods are properly documented.
    4. On-site renewable energy deduction is applied correctly.
- **Reviewer Role:** Energy Modeler / MEP Consultant
- **SLA:** `hitl_sla_hours` (default 72 hours)
- **Instructions for Reviewer:**
  > "Please verify that the parsed energy values, cost calculations, and end-use breakdowns accurately reflect your EnergyPlus/eQuest/TRACE/IES model outputs. Confirm that baseline and proposed models are correctly mapped per ASHRAE 90.1-2022 Appendix G. If you approve, the workflow will proceed to narrative generation. If you reject, please provide corrected files or explanation."
- **Output:** `hitl_1_approval` (`approved` | `rejected` | `pending`) + `reviewer_notes: str`.
- **On Failure (rejected):** Return to Step 2 with corrected files or to Step 3 with modeler-provided overrides.

---

### Step 6: Compliance Narrative Generation
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Generate a comprehensive ASHRAE 90.1-2022 Appendix G compliance narrative including:
     - Project overview (`project_name`, `project_address`, climate zone, building type, GSA).
     - Modeling software and version statement.
     - Baseline building description (system type per 90.1-2022 Table G3.1.1-3, envelope, lighting, HVAC efficiencies).
     - Proposed building description (as-designed systems, envelope, lighting, controls, on-site renewables).
     - Energy performance comparison (site energy, source energy, energy cost).
     - Explanation of % better than baseline calculation.
     - End-use analysis with any anomalies explained.
     - On-site renewable energy accounting per G2.4.
     - Exceptional calculation methods (if any).
     - Statement of compliance: "The proposed building energy cost does not exceed the baseline building energy cost, meeting the requirements of ASHRAE 90.1-2022 Section G1.2.2 and LEED v5 EAp2."
  2. If `leed_review_comments` is provided, incorporate responses to prior GBCI comments.
  3. Generate in structured markdown; render to PDF via `weasyprint` or `pypandoc` + LaTeX.
- **Output:** `compliance_narrative_md: str`, `compliance_narrative_pdf: File`.
- **On Failure:** If PDF generation fails, output markdown and flag for manual conversion.

---

### Step 7: Energy Performance Summary Generation
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Generate a visual summary document (PDF) containing:
     - Cover page with project metadata.
     - Executive summary box: Baseline Cost, Proposed Cost, Savings, % Better.
     - Bar chart: Baseline vs. Proposed annual energy cost by fuel type (matplotlib / plotly).
     - Bar chart: Site energy vs. Source energy comparison.
     - Pie chart or stacked bar: End-use energy distribution for baseline and proposed.
     - Table: Key performance metrics (EUI site, EUI source, EUI cost per sq ft).
     - Climate zone and building type reference.
  2. Embed all charts as vector or high-resolution raster.
- **Output:** `energy_performance_summary_pdf: File`.
- **On Failure:** If chart rendering fails, generate tabular-only PDF and flag.

---

### Step 8: End-Use Comparison Table Generation
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Generate a detailed end-use comparison table in Excel (`.xlsx`) with the following sheets:
     - **Summary**: Annual totals, % better, EUI metrics.
     - **End-Use Breakdown**: Rows = end-use categories; Columns = Proposed (kWh, kBtu, % of total), Baseline (kWh, kBtu, % of total), Difference (kWh, kBtu, % change).
     - **Monthly Profile**: 12 rows (Jan–Dec); columns for baseline and proposed monthly energy cost and consumption.
     - **Peak Demand**: Monthly peak demand comparison (kW) by utility type.
     - **Cost Breakdown**: Rows = fuel types; Columns = Baseline cost, Proposed cost, Savings.
     - **Input Files**: Hyperlinks or checksums of uploaded model files for traceability.
  2. Apply conditional formatting: green if proposed < baseline, red if proposed > baseline by > 10%.
  3. Freeze panes on header rows.
- **Output:** `end_use_comparison_xlsx: File`.
- **On Failure:** If `openpyxl` fails, generate `.csv` sheets and flag.

---

### Step 9: HITL Checkpoint 2 — LEED Consultant Review
- **Type:** Human Review
- **Automated:** No
- **Description:**
  Present the complete documentation package to the **LEED consultant** or **project sustainability lead** for final review:
  - `compliance_narrative_pdf`
  - `energy_performance_summary_pdf`
  - `end_use_comparison_xlsx`
  - `compliance_calculation` JSON (inline summary)
  - Ask reviewer to confirm:
    1. Narrative accurately describes the project and modeling approach.
    2. All ASHRAE 90.1-2022 Appendix G requirements are addressed.
    3. End-use anomalies have acceptable explanations.
    4. Documents are ready for LEED Online upload.
- **Reviewer Role:** LEED Consultant / Sustainability Project Manager
- **SLA:** `hitl_sla_hours` (default 72 hours)
- **Instructions for Reviewer:**
  > "Please review the complete EAp2 documentation package. Confirm that the ASHRAE 90.1-2022 Appendix G compliance narrative, energy performance summary, and end-use comparison table are accurate and complete for LEED Online submission. Approve to finalize, or reject with corrections needed."
- **Output:** `hitl_2_approval` (`approved` | `rejected` | `pending`) + `reviewer_notes: str`.
- **On Failure (rejected):** Return to Step 6 with narrative edits or Step 8 with table corrections.

---

### Step 10: Final Package Assembly & Delivery
- **Type:** Document Generation / API Call
- **Automated:** Yes
- **Description:**
  1. Assemble final deliverables into a zip package:
     - `EAp2_Compliance_Narrative.pdf`
     - `EAp2_Energy_Performance_Summary.pdf`
     - `EAp2_End_Use_Comparison.xlsx`
     - `EAp2_Calculation_Workbook.json` (machine-readable compliance data)
     - `EAp2_Input_Files_Manifest.json` (checksums, file names, upload timestamps)
  2. Upload to project document management system (if DMS API configured).
  3. Generate LEED Online upload guidance:
     - Narrative → "EAp2: Minimum Energy Performance" → "Form" → "Narrative" section.
     - Energy model files → "EAp2: Minimum Energy Performance" → "Supporting Documentation" → Upload `.eso`, `.csv`, `.htm`.
     - Performance summary → "Supporting Documentation".
  4. Write audit log: every step executed, HITL decisions, file checksums, calculation inputs/outputs.
- **Output:** `final_package_zip: File`, `leed_online_guidance_md: str`, `audit_log_json: JSON`.
- **On Failure:** If zip assembly fails, deliver individual files. Log error.

---

## HITL Checkpoints

| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 5: Modeler Verification | Energy Modeler / MEP Consultant | 72 hours (configurable via `hitl_sla_hours`) | Verify parsed model outputs match original EnergyPlus/eQuest/TRACE/IES files. Confirm HVAC mappings, baseline system selections, exceptional calculations, and renewable energy deductions are correct. |
| Step 9: LEED Consultant Review | LEED Consultant / Sustainability PM | 72 hours (configurable via `hitl_sla_hours`) | Review compliance narrative for technical accuracy and completeness. Confirm end-use comparison table is correct. Verify all ASHRAE 90.1-2022 Appendix G requirements are addressed. Approve for LEED Online upload. |

---

## API Dependencies

| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| **EnergyPlus / Eppy** (`eppy`, `esoreader`, custom ESO parser) | Parse `.eso`, `.idf`, `.htm` files; extract report variables and summary tables. | Global (open source) | Custom regex-based parser for `.eso`; `BeautifulSoup` for `.htm` | N/A (local processing) |
| **eQuest Parser** (`equest-parser` or custom `.lv`/`.sim` parser) | Parse eQuest simulation output files. | Global (open source) | Manual `.lv` text extraction + mapping table | N/A (local processing) |
| **TRACE 700 Export Parser** (`pdfplumber`, `camelot`, `openpyxl`) | Extract tables from TRACE PDF or XLSX exports. | Global (license required for TRACE software, but parser is open) | Manual table extraction | N/A (local processing) |
| **IES VE API / ApacheSim Export Parser** | Parse IES VE CSV/DB simulation results. | Global (license required for IES software) | Manual CSV mapping to 90.1 end-use categories | N/A (local processing) |
| **ECB / OANDA Exchange Rates** | Currency conversion for non-USD projects. | Global | Hardcode last-known rate with timestamp | 1000 requests/day (OANDA free tier) |
| **ASHRAE 90.1-2022 Standard (static)** | Reference tables for climate zones, building prototypes, source energy factors, HVAC system types (Table G3.1.1-3), envelope requirements. | Global (published standard; US-centric jurisdiction) | Hardcoded JSON copy of relevant tables | N/A (static data) |
| **Pandoc / WeasyPrint / LaTeX** | Markdown-to-PDF rendering for narrative and summary documents. | Global | Raw markdown output if PDF engine fails | N/A (local processing) |
| **OpenPyXL / XlsxWriter** | Excel `.xlsx` generation for end-use comparison table. | Global | CSV output if Excel engine fails | N/A (local processing) |

---

## Regional Availability

| Region | Status | Notes |
|--------|--------|-------|
| **United States & Canada** | Available | ASHRAE 90.1 is the primary standard. Full parser support for EnergyPlus, eQuest, TRACE 700, IES VE. |
| **Europe (EU/UK)** | Available | ASHRAE 90.1 may be used for LEED; IECC/ASHRAE equivalence may require additional regional mapping. Currency conversion supported. |
| **Middle East & North Africa** | Available | Climate zones 0A–0B, 1A–1B supported. ASHRAE 90.1 applicable for LEED projects. |
| **Asia-Pacific** | Available | ASHRAE 90.1 used for LEED. Timezone handling required. Currency conversion supported. |
| **Latin America & Caribbean** | Available | ASHRAE 90.1 used for LEED. Currency conversion supported. |
| **Sub-Saharan Africa** | Limited | Few LEED projects; ASHRAE 90.1 climate zone mapping may require manual verification for non-standard locations. |

---

## Error Handling

| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| `InputValidationError` — missing/invalid required file | Halt; return detailed error message listing missing fields | Yes (email to `energy_modeler_email`) | No — requires human to upload correct file |
| `ModelParseError` — `.eso`/`.csv`/`.htm` parser failure | Attempt fallback parser; if both fail, halt and flag for modeler review | Yes (email to `energy_modeler_email`) | 1x with fallback parser |
| `AreaMismatchWarning` — model GSA differs from input GSA by > 2% | Continue with warning; flag in HITL Step 5 | No (flag in HITL review) | N/A |
| `TariffMissingFuelError` — utility rate missing rate for fuel in model | Halt Step 3; flag specific missing fuel and rate needed | Yes (email to project team) | No — requires tariff update |
| `ZeroBaselineCostError` — baseline energy cost is zero or negative | Halt Step 4; flag for modeler review | Yes (email to `energy_modeler_email`) | No — indicates model error |
| `EndUseAnomalyWarning` — proposed end-use > baseline by > 10% | Continue with warning; list in `end_use_anomaly_flags` | No (flag in HITL Step 5) | N/A |
| `HITLTimeoutError` — reviewer does not respond within SLA | Escalate to project manager; auto-reminder at 50% SLA, 75% SLA, 100% SLA | Yes (escalation email) | N/A — requires human action |
| `PDFRenderError` — WeasyPrint / LaTeX failure | Output raw markdown; flag for manual conversion | Yes (email to project team) | 1x with alternative engine |
| `ExcelGenerationError` — OpenPyXL failure | Output CSV sheets; flag for manual Excel assembly | Yes (email to project team) | 1x with XlsxWriter |
| `CurrencyConversionError` — exchange rate API failure | Use last cached rate; flag timestamp and source | No (log warning) | 1x with secondary API |

---

## Output Documents

| Document | Format | Description |
|----------|--------|-------------|
| `EAp2_Compliance_Narrative.pdf` | PDF | ASHRAE 90.1-2022 Appendix G compliance narrative: project description, baseline/proposed building descriptions, modeling methodology, energy performance results, compliance statement, and responses to prior review comments (if any). |
| `EAp2_Energy_Performance_Summary.pdf` | PDF | Visual executive summary with charts (cost by fuel, site/source energy, end-use distribution, EUI metrics) and key performance indicator tables. |
| `EAp2_End_Use_Comparison.xlsx` | XLSX | Multi-sheet Excel workbook: Summary, End-Use Breakdown, Monthly Profile, Peak Demand, Cost Breakdown, Input Files Manifest. Includes conditional formatting. |
| `EAp2_Calculation_Workbook.json` | JSON | Machine-readable record of all inputs, parsed values, unit conversions, cost calculations, end-use comparisons, and compliance status. |
| `EAp2_Input_Files_Manifest.json` | JSON | Checksums (SHA-256), filenames, upload timestamps, and parser versions for all input model files. |
| `EAp2_Final_Package.zip` | ZIP | Consolidated package of all above documents for LEED Online upload and project records. |
| `EAp2_LEED_Online_Guidance.md` | Markdown | Step-by-step instructions for uploading each document to the correct LEED Online credit form and supporting documentation sections. |
| `EAp2_Audit_Log.json` | JSON | Complete audit trail of workflow execution: step timestamps, HITL decisions, reviewer identities, calculation parameters, and any errors or warnings. |

---

## Testing

```bash
# Run all unit and integration tests for EAp2 skill
python -m pytest skills/leed-ea-p2-energy-min/tests/ -v --tb=short

# Test subsets
python -m pytest skills/leed-ea-p2-energy-min/tests/test_parsers.py -v
python -m pytest skills/leed-ea-p2-energy-min/tests/test_calculations.py -v
python -m pytest skills/leed-ea-p2-energy-min/tests/test_document_generation.py -v
python -m pytest skills/leed-ea-p2-energy-min/tests/test_hitl_workflow.py -v
python -m pytest skills/leed-ea-p2-energy-min/tests/test_end_to_end.py -v
```

### Test Data Requirements
- `tests/fixtures/sample_proposed.eso` — EnergyPlus output file (≥ 1 year, small office)
- `tests/fixtures/sample_baseline.eso` — Matching baseline model
- `tests/fixtures/sample_proposed.htm` — EnergyPlus table output
- `tests/fixtures/sample_baseline.htm` — Matching baseline table output
- `tests/fixtures/sample_proposed.csv` — Time-series end-use CSV
- `tests/fixtures/sample_baseline.csv` — Matching baseline CSV
- `tests/fixtures/sample_utility_rate.json` — Multi-fuel tariff with TOU
- `tests/fixtures/sample_ies_ve.csv` — IES VE ApacheSim export (optional)
- `tests/fixtures/sample_equest.lv` — eQuest LV output (optional)
- `tests/fixtures/sample_trace700.xlsx` — TRACE 700 export (optional)

---

## Example Usage (Deer-Flow)

```python
from deerflow.skills import EAp2MinimumEnergyEfficiency

skill = EAp2MinimumEnergyEfficiency(
    project_id="LEED-2024-56789",
    inputs={
        "proposed_model_eso": "/uploads/proposed_model.eso",
        "proposed_model_csv": "/uploads/proposed_model_enduses.csv",
        "proposed_model_htm": "/uploads/proposed_model_table.htm",
        "baseline_model_eso": "/uploads/baseline_model.eso",
        "baseline_model_csv": "/uploads/baseline_model_enduses.csv",
        "baseline_model_htm": "/uploads/baseline_model_table.htm",
        "building_gross_floor_area_sqft": 125000.0,
        "climate_zone": "4A",
        "building_type": "MediumOffice",
        "energy_modeler_name": "Jane Doe, PE",
        "energy_modeler_email": "jane.doe@meconsulting.com",
        "modeling_software": "EnergyPlus",
        "ashrae_90_1_version": "90.1-2022",
        "utility_rate_tariff": "/uploads/local_utility_tariff.json",
        "on_site_renewable_kwh": 45000.0,
        "project_name": "Green Tower Office Building",
        "project_address": "123 Main St, New York, NY 10001",
        "project_timezone": "America/New_York",
        "currency_code": "USD",
        "hitl_sla_hours": 72,
    }
)

result = await skill.execute()

# result structure:
# {
#   "status": "completed" | "hitl_pending" | "failed",
#   "current_step": str,
#   "validation_report": dict,
#   "compliance_calculation": dict,
#   "documents": {
#       "compliance_narrative_pdf": "/output/EAp2_Compliance_Narrative.pdf",
#       "energy_performance_summary_pdf": "/output/EAp2_Energy_Performance_Summary.pdf",
#       "end_use_comparison_xlsx": "/output/EAp2_End_Use_Comparison.xlsx",
#       "final_package_zip": "/output/EAp2_Final_Package.zip",
#   },
#   "hitl_status": {
#       "checkpoint_1": {"status": "approved", "reviewer": "Jane Doe", "timestamp": "2024-06-15T14:30:00Z"},
#       "checkpoint_2": {"status": "approved", "reviewer": "John Smith, LEED AP BD+C", "timestamp": "2024-06-18T09:15:00Z"},
#   },
#   "audit_log": "/output/EAp2_Audit_Log.json",
# }
```

---

## Deer-Flow Workflow (LangGraph)

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import operator


class EAp2State(TypedDict):
    project_id: str
    inputs: dict
    validation_report: dict | None
    parsed_model_data: dict | None
    energy_cost_summary: dict | None
    compliance_calculation: dict | None
    hitl_1_status: dict | None
    hitl_2_status: dict | None
    documents: dict | None
    errors: Annotated[list, operator.add]
    current_step: str
    audit_log: list


def validate_inputs(state: EAp2State):
    """Step 1: Validate all required inputs and files."""
    report = run_validation(state["inputs"])
    if not report["valid"]:
        return {
            "validation_report": report,
            "errors": [f"InputValidationError: {e}" for e in report["errors"]],
            "current_step": "FAILED_AT_VALIDATION",
        }
    return {
        "validation_report": report,
        "current_step": "INPUT_VALIDATION_COMPLETE",
        "audit_log": [{"step": "validate_inputs", "timestamp": utcnow(), "status": "ok"}],
    }


def parse_model_outputs(state: EAp2State):
    """Step 2: Parse energy model output files (.eso, .csv, .htm)."""
    parsed = run_parser(
        software=state["inputs"]["modeling_software"],
        proposed_files={
            "eso": state["inputs"]["proposed_model_eso"],
            "csv": state["inputs"]["proposed_model_csv"],
            "htm": state["inputs"]["proposed_model_htm"],
        },
        baseline_files={
            "eso": state["inputs"]["baseline_model_eso"],
            "csv": state["inputs"]["baseline_model_csv"],
            "htm": state["inputs"]["baseline_model_htm"],
        },
    )
    return {
        "parsed_model_data": parsed,
        "current_step": "MODEL_PARSING_COMPLETE",
        "audit_log": [{"step": "parse_model_outputs", "timestamp": utcnow(), "status": "ok"}],
    }


def calculate_energy_costs(state: EAp2State):
    """Step 3: Apply utility tariff to parsed consumption and demand data."""
    cost_summary = run_cost_calculator(
        parsed_data=state["parsed_model_data"],
        tariff=state["inputs"]["utility_rate_tariff"],
        renewable_kwh=state["inputs"].get("on_site_renewable_kwh", 0.0),
        currency=state["inputs"].get("currency_code", "USD"),
    )
    return {
        "energy_cost_summary": cost_summary,
        "current_step": "ENERGY_COST_CALCULATION_COMPLETE",
        "audit_log": [{"step": "calculate_energy_costs", "timestamp": utcnow(), "status": "ok"}],
    }


def perform_compliance_calculations(state: EAp2State):
    """Step 4: Calculate % better than baseline and end-use comparisons."""
    compliance = run_compliance_calculator(
        cost_summary=state["energy_cost_summary"],
        parsed_data=state["parsed_model_data"],
        input_gfa=state["inputs"]["building_gross_floor_area_sqft"],
    )
    return {
        "compliance_calculation": compliance,
        "current_step": "COMPLIANCE_CALCULATION_COMPLETE",
        "audit_log": [{"step": "perform_compliance_calculations", "timestamp": utcnow(), "status": "ok"}],
    }


def hitl_checkpoint_1(state: EAp2State):
    """Step 5: Human-in-the-loop — Energy Modeler Verification."""
    # Trigger async notification to energy modeler
    send_hitl_notification(
        recipient_email=state["inputs"]["energy_modeler_email"],
        subject=f"[LEED EAp2] Energy Model Verification Required — {state['inputs'].get('project_name', 'Unnamed')}",
        review_url=generate_review_url(state["project_id"], checkpoint=1),
        context={
            "parsed_summary": state["parsed_model_data"],
            "cost_summary": state["energy_cost_summary"],
            "compliance": state["compliance_calculation"],
        },
        sla_hours=state["inputs"].get("hitl_sla_hours", 72),
    )
    return {
        "current_step": "HITL_1_PENDING",
        "audit_log": [{"step": "hitl_checkpoint_1", "timestamp": utcnow(), "status": "pending"}],
    }


def generate_compliance_narrative(state: EAp2State):
    """Step 6: Generate ASHRAE 90.1-2022 Appendix G compliance narrative PDF."""
    narrative_md = render_narrative_markdown(
        inputs=state["inputs"],
        parsed_data=state["parsed_model_data"],
        cost_summary=state["energy_cost_summary"],
        compliance=state["compliance_calculation"],
    )
    pdf_path = render_pdf(narrative_md, filename="EAp2_Compliance_Narrative.pdf")
    return {
        "documents": {**(state.get("documents") or {}), "compliance_narrative_pdf": pdf_path},
        "current_step": "NARRATIVE_GENERATION_COMPLETE",
        "audit_log": [{"step": "generate_compliance_narrative", "timestamp": utcnow(), "status": "ok"}],
    }


def generate_energy_performance_summary(state: EAp2State):
    """Step 7: Generate visual energy performance summary PDF."""
    summary_pdf = render_performance_summary_pdf(
        inputs=state["inputs"],
        cost_summary=state["energy_cost_summary"],
        compliance=state["compliance_calculation"],
        parsed_data=state["parsed_model_data"],
    )
    return {
        "documents": {**(state.get("documents") or {}), "energy_performance_summary_pdf": summary_pdf},
        "current_step": "PERFORMANCE_SUMMARY_COMPLETE",
        "audit_log": [{"step": "generate_energy_performance_summary", "timestamp": utcnow(), "status": "ok"}],
    }


def generate_end_use_comparison(state: EAp2State):
    """Step 8: Generate detailed end-use comparison Excel workbook."""
    xlsx_path = render_end_use_xlsx(
        parsed_data=state["parsed_model_data"],
        cost_summary=state["energy_cost_summary"],
        compliance=state["compliance_calculation"],
        inputs=state["inputs"],
    )
    return {
        "documents": {**(state.get("documents") or {}), "end_use_comparison_xlsx": xlsx_path},
        "current_step": "END_USE_TABLE_COMPLETE",
        "audit_log": [{"step": "generate_end_use_comparison", "timestamp": utcnow(), "status": "ok"}],
    }


def hitl_checkpoint_2(state: EAp2State):
    """Step 9: Human-in-the-loop — LEED Consultant Final Review."""
    # Trigger async notification to LEED consultant
    send_hitl_notification(
        recipient_email=state["inputs"].get("leed_consultant_email", state["inputs"]["energy_modeler_email"]),
        subject=f"[LEED EAp2] Final Documentation Review — {state['inputs'].get('project_name', 'Unnamed')}",
        review_url=generate_review_url(state["project_id"], checkpoint=2),
        context={
            "documents": state["documents"],
            "compliance": state["compliance_calculation"],
        },
        sla_hours=state["inputs"].get("hitl_sla_hours", 72),
    )
    return {
        "current_step": "HITL_2_PENDING",
        "audit_log": [{"step": "hitl_checkpoint_2", "timestamp": utcnow(), "status": "pending"}],
    }


def assemble_final_package(state: EAp2State):
    """Step 10: Zip all outputs, generate LEED Online guidance, write audit log."""
    zip_path = assemble_zip_package(state["documents"], prefix="EAp2")
    guidance_md = generate_leed_online_guidance("EAp2", state["documents"])
    audit_path = write_audit_log(state["audit_log"], state["project_id"])
    return {
        "documents": {
            **state["documents"],
            "final_package_zip": zip_path,
            "leed_online_guidance_md": guidance_md,
            "audit_log_json": audit_path,
        },
        "current_step": "FINAL_PACKAGE_ASSEMBLED",
        "audit_log": [{"step": "assemble_final_package", "timestamp": utcnow(), "status": "ok"}],
    }


# --- Conditional routing ---

def route_after_validation(state: EAp2State):
    if state.get("errors"):
        return END
    return "parse_model_outputs"


def route_after_hitl_1(state: EAp2State):
    status = (state.get("hitl_1_status") or {}).get("status", "pending")
    if status == "approved":
        return "generate_compliance_narrative"
    if status == "rejected":
        return "parse_model_outputs"  # loop back with corrections
    return END  # still pending, exit and wait for external trigger


def route_after_hitl_2(state: EAp2State):
    status = (state.get("hitl_2_status") or {}).get("status", "pending")
    if status == "approved":
        return "assemble_final_package"
    if status == "rejected":
        return "generate_compliance_narrative"  # loop back with narrative edits
    return END


# --- Build graph ---
workflow = StateGraph(EAp2State)

workflow.add_node("validate", validate_inputs)
workflow.add_node("parse_model_outputs", parse_model_outputs)
workflow.add_node("calculate_costs", calculate_energy_costs)
workflow.add_node("calculate_compliance", perform_compliance_calculations)
workflow.add_node("hitl_1", hitl_checkpoint_1)
workflow.add_node("generate_narrative", generate_compliance_narrative)
workflow.add_node("generate_summary", generate_energy_performance_summary)
workflow.add_node("generate_end_use", generate_end_use_comparison)
workflow.add_node("hitl_2", hitl_checkpoint_2)
workflow.add_node("assemble", assemble_final_package)

workflow.set_entry_point("validate")
workflow.add_conditional_edges("validate", route_after_validation)
workflow.add_edge("parse_model_outputs", "calculate_costs")
workflow.add_edge("calculate_costs", "calculate_compliance")
workflow.add_edge("calculate_compliance", "hitl_1")
workflow.add_conditional_edges("hitl_1", route_after_hitl_1)
workflow.add_edge("generate_narrative", "generate_summary")
workflow.add_edge("generate_summary", "generate_end_use")
workflow.add_edge("generate_end_use", "hitl_2")
workflow.add_conditional_edges("hitl_2", route_after_hitl_2)
workflow.add_edge("assemble", END)

# Persistent checkpointing for HITL resume
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Execution
# result = app.invoke(initial_state, config={"thread_id": "EAp2-LEED-2024-56789"})
```

---

## Implementation Notes

### Energy Modeling Boundary (Critical)
This skill **strictly automates documentation** based on energy model outputs. The following activities **must** be performed by a qualified energy modeler **before** invoking this skill:

1. **Building energy model creation** in EnergyPlus, eQuest, TRACE 700, IES VE, HAP, or equivalent.
2. **Baseline model development** per ASHRAE 90.1-2022 Appendix G (envelope, lighting, HVAC system type from Table G3.1.1-3, equipment efficiencies).
3. **Proposed model development** with as-designed systems, controls, and on-site renewables.
4. **Simulation execution** and convergence verification.
5. **Quality assurance** of model outputs (e.g., check for unreasonably high heating loads, missing schedules, incorrect weather files).

This skill does **not**:
- Create `.idf`, `.osm`, `.inp`, `.gbxml`, or any model input files.
- Run EnergyPlus or any simulation engine.
- Auto-generate baseline HVAC system assignments.
- Perform geometric or thermal zoning analysis.
- Validate model thermodynamic correctness (only output file format correctness).

### File Format Support Matrix

| Software | `.eso` | `.csv` | `.htm` | `.xml` | Native Format | Parser Status |
|----------|--------|--------|--------|--------|---------------|---------------|
| EnergyPlus | Yes | Yes | Yes | Yes | — | Production-ready |
| OpenStudio | Yes | Yes | Yes | Yes | `.osm` | Production-ready (EnergyPlus backend) |
| eQuest | No | No | No | No | `.lv`, `.sim`, `.srp` | Beta (regex-based) |
| TRACE 700 | No | No | No | No | `.pdf`, `.xlsx` export | Beta (PDF table extraction) |
| IES VE | No | No | No | No | `.csv`, `.db` export | Beta (manual mapping) |
| HAP | No | No | No | No | `.pdf`, `.xlsx` export | Alpha (planned) |

### ASHRAE 90.1-2022 Reference Data (Static)
The skill bundles a JSON file (`data/ashrae_90_1_2022_reference.json`) containing:
- Climate zone definitions and geographic mappings.
- Appendix G building prototype enumerations (17 prototypes).
- Source energy factors (Table D.2.1).
- HVAC system type mapping (Table G3.1.1-3).
- Minimum equipment efficiency tables (for narrative reference only).

This static data is loaded at skill initialization and does not require an external API call.

### Security & Data Handling
- All uploaded model files are stored with SHA-256 checksums in the audit log.
- Files are retained for the duration of the LEED review cycle (configurable, default 24 months) then purged.
- No model files are transmitted to external APIs; all parsing is local.
- Currency conversion API calls include only the currency pair and amount, not project details.

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-15 | Initial release. EnergyPlus primary support. eQuest, TRACE 700, IES VE in beta. Two HITL checkpoints. Full PDF + XLSX output. ASHRAE 90.1-2022 Appendix G compliance. |

---

## License & Compliance
- **ASHRAE 90.1-2022**: Referenced standard. Users must possess a licensed copy of the standard for full verification. The skill includes only summary tables necessary for automation.
- **EnergyPlus**: Open-source under US DOE. Parser uses `eppy` (MIT license) and `esoreader` (MIT license).
- **LEED v5**: Trademark of U.S. Green Building Council. This skill is an independent automation tool and is not endorsed by USGBC or GBCI.
