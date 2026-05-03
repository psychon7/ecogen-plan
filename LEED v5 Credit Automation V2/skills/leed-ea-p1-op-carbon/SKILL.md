```markdown
---
name: leed-ea-p1-op-carbon
version: 1.0.0
author: LEED Automation Platform
description: Automates LEED EAp1 Operational Carbon Projection and Decarbonization Plan
---

## Metadata
- **Credit Code:** EAp1
- **Credit Name:** Operational Carbon Projection and Decarbonization Plan
- **Points:** Required (Prerequisite)
- **Automation Level:** 89.4%
- **Complexity:** Low-Medium
- **Primary Data Source:** EPA eGRID, NREL PVWatts, EnergyPlus simulation outputs
- **HITL Required:** Yes

## Purpose
Automates the development of a 25-year operational carbon projection and decarbonization plan by fetching grid emission factors, parsing energy model outputs, calculating annual carbon emissions, projecting future carbon trajectories with efficiency measures, and generating the required LEED submission documents.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| energy_model_output | File (.eso/.csv/.sql) | Project team / EnergyPlus | Must contain annual kWh by end use (heating, cooling, lighting, equipment, fans, pumps, hot water) |
| project_latitude | Float | Project team | -90.0 to 90.0 |
| project_longitude | Float | Project team | -180.0 to 180.0 |
| project_country | String | Project team | ISO 3166-1 alpha-2; if not US, triggers international grid factor lookup |
| building_gross_area_sqft | Float | Project team | > 0 |
| service_life_years | Integer | Project team | Default 25; must be ≥ 10 |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| onsite_renewable_kwh | Dict[str, float] | {} | Annual on-site renewable generation by type: solar_pv, solar_thermal, wind, geothermal, fuel_cell |
| planned_ee_measures | List[Dict] | [] | Each dict: measure_name, target_year, annual_kwh_reduction, implementation_cost, measure_category |
| grid_decarbonization_scenario | String | "eGRID_projected" | Options: "eGRID_projected", "NREL_REEDS", "custom_annual_factors" |
| custom_grid_factors | List[float] | None | If scenario is "custom", annual kgCO2/kWh factors for each projection year |
| building_sector | String | "commercial" | Used for eGRID subregion lookup weighting: commercial, residential, industrial |
| refrigerant_type | String | "R410A" | Used for refrigerant leakage carbon calculation if HVAC energy is present |
| refrigerant_charge_lbs | Float | 0.0 | Total refrigerant charge for leakage calculation |
| use_ipcc_2021_factors | Boolean | True | If True, uses AR6 emission factors; if False, uses AR5 |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. Parse and validate energy model output file using Eppy/EnergyPlus SQLite parser.
  2. Verify all required end-use categories are present: Heating, Cooling, Interior Lighting, Exterior Lighting, Interior Equipment, Exterior Equipment, Fans, Pumps, Heat Rejection, Humidification, Heat Recovery, Water Systems.
  3. Validate lat/lon coordinates using GeoJSON schema.
  4. Check service_life_years ≥ 10.
  5. Validate each planned_ee_measure dict has required fields: measure_name, target_year, annual_kwh_reduction.
  6. Cross-check onsite_renewable_kwh types against supported enumeration.
- **Output:** ValidatedInputSchema (Pydantic model) with normalized data structures.
- **On Failure:** Raise ValidationError with field-level details; trigger human notification via Slack/email.

### Step 2: Determine Grid Subregion and Fetch Emission Factors
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. **US Projects:** Use reverse geocoding (lat/lon → county FIPS) via FCC Area API (https://geo.fcc.gov/api/census/area) to determine eGRID subregion.
  2. Query EPA eGRID API (https://www.epa.gov/egrid/egrid-mapping-tool) or parse latest eGRID Summary Tables (XLSX) for:
     - `SUBRGN` code (e.g., "RFCW", "CAMX")
     - Annual `CO2e` emission rate (lb/MWh or kg/kWh)
     - Non-baseload emission rate (for marginal analysis, optional)
     - Grid loss factor (to apply to consumed kWh)
  3. Apply grid loss factor: `grid_CO2_factor = eGRID_rate_kg_per_kWh / (1 - grid_loss_factor)`.
  4. **Non-US Projects:** Use IEA World Energy Outlook country-specific grid emission factors (API or cached CSV). Fallback to IPCC national grid factors table.
  5. If `grid_decarbonization_scenario` is "eGRID_projected", apply eGRID historical decarbonization curve (2018-2023 CAGR) to project 25-year declining factors. If "NREL_REEDS", use NREL Standard Scenarios mid-case projection. If "custom", use user-provided annual list.
- **Output:** GridFactorsSchema with fields: subregion_code, current_annual_factor_kg_co2_per_kwh, projected_annual_factors[List[Float]], factor_source, projection_method, data_year.
- **On Failure:** If eGRID API unavailable, fallback to cached eGRID2022 v2.1 dataset (local SQLite). If no cached data and non-US, fallback to IPCC 2021 default grid factor (0.5 kgCO2/kWh) with WARNING flag.

### Step 3: Parse Energy Model End-Use kWh
- **Type:** API Call / File Parsing
- **Automated:** Yes
- **Description:**
  1. Detect file format by extension:
     - `.eso`: Use Eppy `readeso()` to extract `End Uses` table.
     - `.sql`: Use SQLite adapter to query `ReportDataDictionary` and `ReportData` tables for `End Uses` report.
     - `.csv`: Read via Pandas; validate column headers match expected end-use names.
  2. Extract annual kWh for each end use. Convert from MJ if necessary (divide by 3.6).
  3. Aggregate into categories: `electricity_total_kwh`, `natural_gas_total_therms` (if present), `district_heating_kwh`, `district_cooling_kwh`.
  4. Compute peak demand (kW) if available for demand charge carbon analysis.
  5. Tag each end use with fuel type (Electricity, Natural Gas, Fuel Oil, District Steam, etc.).
- **Output:** EndUseBreakdownSchema with nested fuel-type → end-use → annual_kwh mapping, total_site_energy_kbtu, total_source_energy_kbtu.
- **On Failure:** If file format unrecognized or missing required end uses, raise ParseError with diagnostic message listing available vs. expected columns.

### Step 4: Calculate Baseline Annual Operational Carbon
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. For each fuel type in end-use breakdown, apply appropriate emission factor:
     - **Electricity:** `annual_kWh × grid_CO2_factor_kg_per_kWh` (from Step 2).
     - **Natural Gas:** `annual_therms × 5.3 kgCO2e/therm` (EPA GHG Equivalencies).
     - **Fuel Oil #2:** `annual_gallons × 10.16 kgCO2e/gallon`.
     - **District Steam:** `annual_Mlbs × 254.0 kgCO2e/Mlb` (EPA CHP default).
     - **District Chilled Water:** `annual_kWh_thermal × grid_CO2_factor × 1.2` (typical COP inverse).
  2. Apply on-site renewable offsets:
     - Solar PV: subtract generation kWh × grid_CO2_factor (avoided emissions method).
     - Solar Thermal: subtract equivalent fuel kWh × fuel_CO2_factor.
  3. If refrigerant data provided, calculate annual leakage: `refrigerant_charge_lbs × 0.02 (2% annual leakage rate for R410A) × GWP_100yr_R410A (2088 kgCO2e/kg) × 0.453592 kg/lb`.
  4. Sum all categories: `baseline_annual_carbon_mt = Σ(fuel_emissions_kg - renewable_offsets_kg + refrigerant_kg) / 1000`.
  5. Calculate carbon intensity metrics: `kgCO2e/sf/year`, `kgCO2e/kWh_of_electricity`.
- **Output:** BaselineCarbonSchema with: total_annual_mt_co2e, by_fuel_type Dict, by_end_use Dict, intensity_metrics Dict, renewable_offsets_mt, refrigerant_emissions_mt.
- **On Failure:** If fuel type unrecognized, use IPCC default factor and flag for HITL review.

### Step 5: Project 25-Year Carbon Trajectory
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Initialize year-0 = baseline_annual_carbon_mt.
  2. For each year i from 1 to `service_life_years`:
     a. Apply grid decarbonization: `grid_factor_year_i = grid_factor_year_0 × (1 - grid_decay_rate)^i`, where grid decay rate derived from projection scenario (e.g., NREL REEDS = ~3.5% CAGR).
     b. Apply building system degradation: `degradation_multiplier = 1 + (0.005 × i)` for equipment efficiency loss (0.5%/year).
     c. For each planned_ee_measure: if `target_year == i`, subtract `annual_kwh_reduction × grid_factor_year_i / 1000` from carbon trajectory starting in year i.
     d. For on-site renewables: apply production degradation (0.5%/year for PV). Recalculate offset annually.
     e. Year i carbon = `(baseline_energy_kwh × degradation_multiplier × grid_factor_year_i / 1000) - renewable_offset_year_i - Σ(active_ee_measures_mt)`.
  3. Compute cumulative carbon over service life: `Σ(year_i) for i=0..24`.
  4. Compute net-zero crossover year: smallest i where `year_i_carbon ≤ 0` or meets NZE threshold; if none, return "No crossover within service life".
  5. Generate annual DataFrame: Year | Grid Factor | Baseline Energy | Degradation | EE Reductions | Renewable Offset | Net Annual Carbon | Cumulative Carbon.
- **Output:** CarbonProjectionSchema with: annual_projections[List[YearProjection]], cumulative_mt_co2e, net_zero_crossover_year, peak_annual_mt, year_25_reduction_pct, sensitivity_analysis Dict.
- **On Failure:** If EE measure reductions exceed baseline in any year, cap at 95% reduction and flag as "Aggressive target, review recommended".

### Step 6: Calculate Carbon Reduction Potential from Planned Measures
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. For each planned_ee_measure, calculate:
     - Annual carbon reduction (MT CO2e/year) in year of implementation.
     - Lifetime reduction: `annual_reduction_MT × (service_life_years - target_year)`.
     - Percent of baseline: `annual_reduction_MT / baseline_annual_carbon_mt × 100`.
     - Cost effectiveness: `implementation_cost / annual_reduction_MT` ($/MT CO2e avoided).
  2. Aggregate by measure_category (HVAC, Lighting, Envelope, Controls, Renewables):
     - Category total annual reduction.
     - Category total lifetime reduction.
     - Category total cost.
  3. Rank measures by cost-effectiveness ($/MT CO2e).
  4. Identify highest-impact measures (top 3 by lifetime reduction).
  5. Calculate combined interactive effects (simplified: sum of individual reductions × 0.85 interaction factor to avoid double-counting).
- **Output:** MeasuresAnalysisSchema with: individual_measures[List[MeasureImpact]], category_aggregates[Dict], ranking_by_cost_effectiveness[List], top_3_measures[List], combined_interactive_reduction_MT, implementation_cost_total.
- **On Failure:** If cost effectiveness exceeds $500/MT CO2e, flag as "Economically marginal" for HITL awareness.

### Step 7: Generate Net-Zero Pathway Calculation
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Define net-zero operational carbon: `Net Annual Carbon ≤ 0.1 × baseline_intensity` (LEED v5 near-zero threshold) OR absolute ≤ 5 MT CO2e/year.
  2. Starting from baseline trajectory (without EE measures), determine gap to net-zero for each year: `gap_MT = projected_carbon_MT - net_zero_threshold_MT`.
  3. Compute required additional on-site renewable capacity:
     - `additional_pv_kW = gap_MT × 1000 / (annual_pv_production_per_kW × grid_factor)`.
     - Annual PV production per kW from NREL PVWatts API (Step 8 pre-query) or default 1,350 kWh/kW/year.
  4. Compute required additional EE measures:
     - `additional_ee_kwh_reduction = gap_MT × 1000 / grid_factor`.
     - Group by category to suggest measure types.
  5. Generate pathway options:
     - **Option A (EE-led):** Maximize efficiency, minimal renewables.
     - **Option B (Renewable-led):** Aggressive on-site + off-site renewable procurement.
     - **Option C (Balanced):** 50/50 EE and renewable split.
  6. For each option, compute: total cost, net-zero achievement year, 25-year total carbon, LCC savings.
- **Output:** NetZeroPathwaySchema with: threshold_definition, gap_trajectory[List], required_renewable_capacity_kW, required_ee_reduction_kwh, pathway_options[List[PathwayOption]], recommended_pathway, confidence_score.
- **On Failure:** If gap exceeds physically achievable (e.g., >100% energy reduction required), flag as "Infeasible net-zero target" and suggest extended timeline or off-site strategies.

### Step 8: Query NREL PVWatts for On-Site Solar Production
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. Call NREL PVWatts v6 API (https://developer.nrel.gov/api/pvwatts/v6.json):
     - Parameters: `lat`, `lon`, `system_capacity` = 1.0 (kW reference), `module_type` = 0 (standard), `array_type` = 1 (fixed roof), `tilt` = latitude, `azimuth` = 180, `dataset` = "nsrdb".
  2. Extract `ac_annual` (annual AC kWh) for 1 kW system.
  3. Calculate full building potential: `max_roof_pv_kW = roof_area_sqft × 0.75 (usable) / 17.5 (sf/kW)`, `max_parking_pv_kW = parking_stalls × 330 × 0.6 / 17.5`.
  4. Compute total solar potential: `reference_annual_kwh_per_kw × total_pv_kW`.
  5. If user provided `onsite_renewable_kwh` with solar, validate against PVWatts estimate (±20% tolerance).
- **Output:** SolarPotentialSchema with: reference_annual_kwh_per_kw, max_building_pv_kW, max_parking_pv_kW, total_annual_potential_kwh, pvwatts_response_url, validation_status.
- **On Failure:** If NREL API limit reached or unavailable, use default 1,350 kWh/kW/year for lat < 40°, 1,500 kWh/kW/year for lat ≥ 40° (sunny US southwest). Flag as "PVWatts unavailable, using default production factors".

### Step 9: LEED Consultant HITL Review
- **Type:** Human Review
- **Automated:** No
- **Description:**
  Present the following to the LEED consultant via platform HITL review UI:
  1. Baseline annual carbon (MT CO2e/year) and intensity (kgCO2e/sf/year).
  2. 25-year projection chart (carbon vs. year, with EE measure milestones).
  3. Planned EE measures table with cost-effectiveness ranking.
  4. Net-zero pathway options (A, B, C) with achievement years.
  5. Grid subregion and emission factor source.
  6. Refrigerant emissions (if applicable).
  7. Sensitivity analysis: carbon at ±20% grid factor, ±10% energy use.
  8. Decarbonization strategy narrative draft.
  
  Consultant must approve or request edits on:
  - Carbon targets realism (not overly aggressive/conservative).
  - Decarbonization strategy completeness.
  - EE measure assumptions validity.
  - Net-zero pathway feasibility.
- **Output:** HITLReviewSchema with: reviewer_id, approval_status (approved/ revisions_required), revision_notes[List], approved_targets, approved_strategy.
- **On Failure:** If SLA exceeded (72 hours), escalate to senior consultant; auto-generate conservative targets and flag for post-submission review.

### Step 10: Generate Operational Carbon Projection Report (PDF)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Generate professional PDF report using ReportLab / WeasyPrint with sections:
     - Executive Summary: Baseline carbon, 25-year cumulative, net-zero target.
     - Methodology: Energy model source, grid factor source (eGRID subregion), emission factors, service life.
     - Baseline Carbon Inventory: Table of annual emissions by fuel type and end use, intensity metrics.
     - 25-Year Projection: Year-by-year table, line chart (carbon trajectory), annotated with EE measure implementation years.
     - Decarbonization Measures: Detailed table of each planned measure with kWh reduction, carbon reduction, cost, cost-effectiveness.
     - On-Site Renewable Analysis: PVWatts results, solar potential, current vs. maximum.
     - Net-Zero Pathway: Recommended pathway, required actions, achievement year.
     - Sensitivity Analysis: Tornado chart or table showing impact of ±variations.
     - Appendices: eGRID subregion map, IPCC factor references, energy model output summary.
  2. Embed charts as vector SVG where possible.
  3. Include page numbers, project name, credit code header.
  4. Apply LEED v5 document formatting standards.
- **Output:** PDF file path, page count, file size.
- **On Failure:** If chart generation fails, render tables only with placeholder text for charts. If PDF engine fails, fallback to DOCX generation.

### Step 11: Generate Decarbonization Plan (PDF)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Generate strategic decarbonization plan PDF with sections:
     - Carbon Vision & Targets: Short-term (5-yr), mid-term (15-yr), long-term (25-yr) targets.
     - Baseline & Context: Current carbon position relative to similar buildings.
     - Strategy Pillars:
       * Energy Efficiency (measures, timeline, responsible party, KPIs)
       * On-Site Renewable Generation (solar roadmap, phased capacity)
       * Grid Interaction (demand response, storage, grid factor trends)
       * Fuel Switching (electrification roadmap if fossil fuels present)
       * Operational Practices (commissioning, O&M, tenant engagement)
     - Implementation Roadmap: Gantt-style timeline (years 1-25) with milestones.
     - Financial Plan: Capital costs, operational savings, ROI, incentive capture.
     - Risk Analysis: Technology risk, policy risk, market risk, mitigation strategies.
     - Monitoring & Verification: M&V plan, annual reporting protocol, data collection plan.
     - Stakeholder Engagement: Internal teams, utilities, tenants, community.
  2. Include call-out boxes for key decisions and HITL consultant notes.
- **Output:** PDF file path, page count, file size.
- **On Failure:** Fallback to DOCX if PDF generation fails.

### Step 12: Generate Supporting Calculation Spreadsheet (XLSX)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Generate Excel workbook with sheets:
     - **Cover:** Project info, skill version, data sources, assumptions list.
     - **Inputs:** All input values (lat/lon, energy model summary, EE measures, renewables).
     - **Grid Factors:** eGRID subregion lookup, year-by-year projected grid factors with source citations.
     - **Energy End Uses:** Parsed energy model data by fuel and end use.
     - **Baseline Carbon:** Calculation formulas visible, annual carbon by fuel type, intensity metrics.
     - **25-Year Projection:** Annual columns (Year, Grid Factor, Energy Use, Degradation, EE Savings, Renewable Offset, Net Carbon, Cumulative), with formulas.
     - **EE Measures:** Individual measure analysis, category aggregation, cost-effectiveness, interactive effects.
     - **Net-Zero Pathway:** Three options with formulas, gap analysis, required capacity.
     - **Sensitivity:** ±20% grid factor, ±10% energy use, ±10% EE savings, ±15% renewable production.
     - **Summary Dashboard:** Key metrics table, carbon trajectory sparkline, measure ranking.
  2. All calculated cells contain Excel formulas (not hardcoded values) for auditor review.
  3. Apply conditional formatting: green for net-zero years, red for baseline, amber for intermediate.
- **Output:** XLSX file path, sheet count, file size.
- **On Failure:** If openpyxl fails, generate CSV bundle (multiple CSVs in ZIP). If all fail, notify human with raw JSON data.

### Step 13: Finalize and Package Deliverables
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Package all outputs into structured directory:
     - `/reports/`: PDF reports
     - `/calculations/`: XLSX spreadsheet
     - `/data/`: Raw JSON of all schemas (for programmatic access)
     - `/charts/`: Individual chart PNGs/SVGs embedded in reports
  2. Generate manifest.json with:
     - file paths, checksums (SHA-256), creation timestamps, skill version, input fingerprints.
  3. Validate file integrity: all required documents present, non-zero size, readable.
  4. Log execution summary: runtime per step, API call counts, errors encountered.
- **Output:** PackageManifestSchema with: output_directory, files[List[FileEntry]], validation_status, execution_summary.
- **On Failure:** If any required document missing or corrupt, retry generation once. If still failing, flag for human intervention.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 9: LEED Consultant Review | LEED AP BD+C or O+M (project consultant) | 72 hours | Review baseline carbon intensity for realism relative to building type and region. Verify EE measure assumptions are grounded in actual building assessments. Confirm net-zero target year is aggressive but achievable. Approve decarbonization strategy narrative or request revisions. Check that grid subregion assignment is correct. Validate on-site renewable production estimates against site constraints. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| EPA eGRID / Mapping Tool | Grid CO2 emission factors by eGRID subregion | US only | Cached eGRID2022 SQLite database | Public, no rate limit for data download |
| FCC Area API | Lat/lon → county FIPS → eGRID subregion | US only | Manual subregion lookup table | 500 req/day per IP |
| NREL PVWatts v6 | On-site solar production estimates | Global (NSRDB coverage) | Default production factors by latitude | 1000 req/day (free API key) |
| IEA World Energy Outlook | Country-level grid factors (non-US) | Global | IPCC 2021 default national factors | Subscription; cached annual extract |
| NREL REEDS / Standard Scenarios | Grid decarbonization projections | US only | eGRID historical CAGR (3%/year) | Public data download |
| EnergyPlus SQLite / Eppy | Parse .eso/.sql energy model outputs | Global (local processing) | Manual CSV parsing | N/A (local) |
| GeoNames / Reverse Geocoding | International location validation | Global | Manual country code validation | 1000 req/hour (free tier) |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | Full eGRID integration, PVWatts, all APIs. Most accurate grid factors. |
| Canada | Limited | No eGRID; use IEA/Environment Canada provincial grid factors. PVWatts available. |
| European Union | Limited | No eGRID; use Eurostat/ENTSO-E country grid factors. PVWatts coverage varies. |
| UK | Limited | No eGRID; use UK BEIS grid factors. PVWatts limited coverage. |
| Australia | Limited | No eGRID; use NGER/AEMO state grid factors. PVWatts available. |
| Asia-Pacific | Limited | No eGRID; use IEA/UNFCCC national factors. PVWatts available in many regions. |
| Middle East / Africa | Limited | Sparse grid factor data; IPCC defaults heavily relied upon. PVWatts available in sunny regions. |
| Latin America | Limited | IEA/OLADE national factors. PVWatts available. |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Invalid energy model format | Halt; request correct format (.eso/.sql/.csv) | Yes (immediate) | N/A |
| Missing required end-use categories | Continue with available data; flag warning in report | Yes (with partial data summary) | N/A |
| eGRID API unavailable | Use cached eGRID2022 database | No (silent fallback) | 3× with 5s backoff |
| FCC Area API unavailable (US) | Use manual lat/lon → subregion lookup table | No (silent fallback) | 2× |
| NREL PVWatts API limit exceeded | Use default production factors by latitude band | No (logged) | Next day |
| Non-US project with no IEA data | Use IPCC 2021 default national factor | Yes (with data gap warning) | N/A |
| EE measure reduction exceeds 95% of baseline | Cap at 95%; flag "Aggressive target" | Yes (in HITL review) | N/A |
| Cost effectiveness > $500/MT CO2e | Flag "Economically marginal" | Yes (in HITL review) | N/A |
| Net-zero gap physically infeasible | Suggest extended timeline or off-site | Yes (immediate, before HITL) | N/A |
| PDF generation failure | Fallback to DOCX generation | No (silent fallback) | 1× |
| XLSX generation failure | Fallback to CSV ZIP bundle | No (silent fallback) | 1× |
| HITL SLA exceeded (72 hrs) | Auto-approve with conservative targets | Yes (escalation to senior) | N/A |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Operational Carbon Projection Report | PDF | 25-year carbon trajectory, baseline inventory, projection charts, sensitivity analysis, appendices |
| Decarbonization Plan | PDF | Strategic plan with targets, measures roadmap, financial analysis, M&V protocol, risk analysis |
| Supporting Calculation Spreadsheet | XLSX | All input data, formulas, year-by-year calculations, sensitivity tables, dashboard |
| Execution Data Bundle | JSON | Machine-readable schemas of all intermediate calculations for programmatic access |
| Chart Assets | PNG/SVG | Individual chart files extracted from reports for reuse |

## Testing
```bash
# Unit tests
python -m pytest skills/ea-p1-op-carbon/tests/test_validation.py -v
python -m pytest skills/ea-p1-op-carbon/tests/test_egrid_fetch.py -v
python -m pytest skills/ea-p1-op-carbon/tests/test_energy_parse.py -v
python -m pytest skills/ea-p1-op-carbon/tests/test_carbon_calc.py -v
python -m pytest skills/ea-p1-op-carbon/tests/test_projection.py -v
python -m pytest skills/ea-p1-op-carbon/tests/test_pvwatts.py -v
python -m pytest skills/ea-p1-op-carbon/tests/test_document_gen.py -v

# Integration test (full workflow)
python -m pytest skills/ea-p1-op-carbon/tests/test_integration.py -v --run-integration

# Regression test with sample data
python skills/ea-p1-op-carbon/tests/regression_test.py \
  --energy-model skills/ea-p1-op-carbon/tests/fixtures/sample_office.sql \
  --expected-carbon 145.2 \
  --expected-tolerance 5.0
```

## Example Usage (OpenAI Agents SDK + Restate)
```python
from leed_platform.skills import EAp1OperationalCarbonSkill

skill = EAp1OperationalCarbonSkill(
    project_id="LEED-2024-1234",
    inputs={
        "energy_model_output": "/data/models/office_building.sql",
        "project_latitude": 39.7392,
        "project_longitude": -104.9903,
        "project_country": "US",
        "building_gross_area_sqft": 125000.0,
        "service_life_years": 25,
        "onsite_renewable_kwh": {
            "solar_pv": 450000.0,
            "solar_thermal": 0.0
        },
        "planned_ee_measures": [
            {
                "measure_name": "LED Lighting Retrofit",
                "target_year": 2,
                "annual_kwh_reduction": 180000.0,
                "implementation_cost": 450000.0,
                "measure_category": "Lighting"
            },
            {
                "measure_name": "HVAC Controls Upgrade",
                "target_year": 3,
                "annual_kwh_reduction": 220000.0,
                "implementation_cost": 320000.0,
                "measure_category": "Controls"
            },
            {
                "measure_name": "Envelope Air Sealing",
                "target_year": 5,
                "annual_kwh_reduction": 95000.0,
                "implementation_cost": 180000.0,
                "measure_category": "Envelope"
            }
        ],
        "grid_decarbonization_scenario": "NREL_REEDS",
        "building_sector": "commercial",
        "refrigerant_type": "R410A",
        "refrigerant_charge_lbs": 850.0
    }
)

# Execute full workflow
result = await skill.execute()

# Access outputs
print(f"Baseline Annual Carbon: {result.baseline_carbon.total_annual_mt_co2e:.1f} MT CO2e")
print(f"25-Year Cumulative: {result.projection.cumulative_mt_co2e:.1f} MT CO2e")
print(f"Net-Zero Crossover Year: {result.projection.net_zero_crossover_year}")
print(f"Top Measure: {result.measures_analysis.top_3_measures[0].measure_name}")

# Access file paths
print(f"Report PDF: {result.deliverables.carbon_projection_report}")
print(f"Decarbonization Plan: {result.deliverables.decarbonization_plan}")
print(f"Spreadsheet: {result.deliverables.calculation_spreadsheet}")
```

## Platform Workflow (OpenAI Agents SDK + Restate)
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Any

class LEEDCarbonState(TypedDict):
    inputs: dict
    validated: Optional[dict]
    grid_factors: Optional[dict]
    end_use_data: Optional[dict]
    baseline_carbon: Optional[dict]
    projection: Optional[dict]
    measures_analysis: Optional[dict]
    net_zero_pathway: Optional[dict]
    solar_potential: Optional[dict]
    hitl_review: Optional[dict]
    documents: Optional[dict]
    deliverables: Optional[dict]
    error: Optional[str]
    logs: list

def validate_inputs_node(state: LEEDCarbonState):
    """Step 1: Validate all input fields and energy model format."""
    from leed_platform.skills.ea_p1.validation import InputValidator
    validator = InputValidator()
    validated = validator.validate(state["inputs"])
    return {**state, "validated": validated, "logs": state["logs"] + ["Step 1: Inputs validated"]}

def fetch_grid_factors_node(state: LEEDCarbonState):
    """Step 2: Fetch eGRID or international grid emission factors."""
    from leed_platform.skills.ea_p1.grid_factors import GridFactorService
    service = GridFactorService()
    factors = service.fetch(
        lat=state["validated"]["project_latitude"],
        lon=state["validated"]["project_longitude"],
        country=state["validated"]["project_country"],
        scenario=state["validated"].get("grid_decarbonization_scenario", "eGRID_projected"),
        custom_factors=state["validated"].get("custom_grid_factors")
    )
    return {**state, "grid_factors": factors, "logs": state["logs"] + ["Step 2: Grid factors fetched"]}

def parse_energy_model_node(state: LEEDCarbonState):
    """Step 3: Parse EnergyPlus output (.eso/.sql/.csv)."""
    from leed_platform.skills.ea_p1.energy_parser import EnergyModelParser
    parser = EnergyModelParser()
    end_use_data = parser.parse(state["validated"]["energy_model_output"])
    return {**state, "end_use_data": end_use_data, "logs": state["logs"] + ["Step 3: Energy model parsed"]}

def calculate_baseline_node(state: LEEDCarbonState):
    """Step 4: Calculate baseline annual operational carbon."""
    from leed_platform.skills.ea_p1.carbon_calc import BaselineCarbonCalculator
    calc = BaselineCarbonCalculator()
    baseline = calc.calculate(
        end_use_data=state["end_use_data"],
        grid_factors=state["grid_factors"],
        renewables=state["validated"].get("onsite_renewable_kwh", {}),
        refrigerant_type=state["validated"].get("refrigerant_type"),
        refrigerant_charge=state["validated"].get("refrigerant_charge_lbs", 0.0)
    )
    return {**state, "baseline_carbon": baseline, "logs": state["logs"] + ["Step 4: Baseline carbon calculated"]}

def project_carbon_node(state: LEEDCarbonState):
    """Step 5: Generate 25-year carbon projection."""
    from leed_platform.skills.ea_p1.projection import CarbonProjector
    projector = CarbonProjector()
    projection = projector.project(
        baseline=state["baseline_carbon"],
        grid_factors=state["grid_factors"],
        service_life=state["validated"]["service_life_years"],
        ee_measures=state["validated"].get("planned_ee_measures", []),
        renewables=state["validated"].get("onsite_renewable_kwh", {})
    )
    return {**state, "projection": projection, "logs": state["logs"] + ["Step 5: 25-year projection generated"]}

def analyze_measures_node(state: LEEDCarbonState):
    """Step 6: Analyze carbon reduction potential of planned measures."""
    from leed_platform.skills.ea_p1.measures import MeasuresAnalyzer
    analyzer = MeasuresAnalyzer()
    measures = analyzer.analyze(
        baseline=state["baseline_carbon"],
        ee_measures=state["validated"].get("planned_ee_measures", []),
        grid_factors=state["grid_factors"],
        service_life=state["validated"]["service_life_years"]
    )
    return {**state, "measures_analysis": measures, "logs": state["logs"] + ["Step 6: Measures analyzed"]}

def calculate_net_zero_node(state: LEEDCarbonState):
    """Step 7: Calculate net-zero pathway options."""
    from leed_platform.skills.ea_p1.netzero import NetZeroPathwayCalculator
    calc = NetZeroPathwayCalculator()
    pathway = calc.calculate(
        projection=state["projection"],
        baseline=state["baseline_carbon"],
        grid_factors=state["grid_factors"],
        solar_potential=state.get("solar_potential")
    )
    return {**state, "net_zero_pathway": pathway, "logs": state["logs"] + ["Step 7: Net-zero pathway calculated"]}

def fetch_solar_potential_node(state: LEEDCarbonState):
    """Step 8: Query NREL PVWatts for solar production potential."""
    from leed_platform.skills.ea_p1.solar import SolarPotentialService
    service = SolarPotentialService()
    solar = service.fetch(
        lat=state["validated"]["project_latitude"],
        lon=state["validated"]["project_longitude"],
        building_area=state["validated"]["building_gross_area_sqft"]
    )
    return {**state, "solar_potential": solar, "logs": state["logs"] + ["Step 8: Solar potential fetched"]}

def hitl_review_checkpoint(state: LEEDCarbonState):
    """Step 9: HITL checkpoint for LEED consultant review.
    
    This step triggers a human-in-the-loop task.
    The workflow pauses until the consultant approves or requests revisions.
    """
    from leed_platform.hitl import create_review_task
    review = create_review_task(
        skill="ea_p1_op_carbon",
        project_id=state["inputs"].get("project_id"),
        review_data={
            "baseline_carbon": state["baseline_carbon"],
            "projection": state["projection"],
            "measures": state["measures_analysis"],
            "net_zero": state["net_zero_pathway"],
            "grid_factors": state["grid_factors"]
        },
        reviewer_role="LEED_AP",
        sla_hours=72
    )
    return {**state, "hitl_review": review, "logs": state["logs"] + ["Step 9: HITL review initiated"]}

def generate_documents_node(state: LEEDCarbonState):
    """Steps 10-12: Generate PDF reports and XLSX spreadsheet."""
    from leed_platform.skills.ea_p1.documents import DocumentGenerator
    gen = DocumentGenerator()
    docs = gen.generate_all(
        baseline=state["baseline_carbon"],
        projection=state["projection"],
        measures=state["measures_analysis"],
        net_zero=state["net_zero_pathway"],
        solar=state["solar_potential"],
        grid_factors=state["grid_factors"],
        inputs=state["validated"],
        hitl_notes=state["hitl_review"].get("revision_notes", [])
    )
    return {**state, "documents": docs, "logs": state["logs"] + ["Steps 10-12: Documents generated"]}

def finalize_deliverables_node(state: LEEDCarbonState):
    """Step 13: Package and finalize all deliverables."""
    from leed_platform.skills.ea_p1.packaging import DeliverablePackager
    packager = DeliverablePackager()
    deliverables = packager.package(
        documents=state["documents"],
        project_id=state["inputs"].get("project_id"),
        data_schemas={
            "baseline": state["baseline_carbon"],
            "projection": state["projection"],
            "measures": state["measures_analysis"],
            "net_zero": state["net_zero_pathway"],
            "grid": state["grid_factors"]
        }
    )
    return {**state, "deliverables": deliverables, "logs": state["logs"] + ["Step 13: Deliverables finalized"]}

def error_handler_node(state: LEEDCarbonState):
    """Global error handler for workflow failures."""
    from leed_platform.errors import notify_human, log_error
    log_error(state["error"], state["logs"])
    notify_human(state["error"], severity="high")
    return {**state, "deliverables": None}

# Build the LangGraph workflow
workflow = StateGraph(LEEDCarbonState)

# Add nodes
workflow.add_node("validate", validate_inputs_node)
workflow.add_node("fetch_grid", fetch_grid_factors_node)
workflow.add_node("parse_energy", parse_energy_model_node)
workflow.add_node("calc_baseline", calculate_baseline_node)
workflow.add_node("project", project_carbon_node)
workflow.add_node("analyze_measures", analyze_measures_node)
workflow.add_node("calc_netzero", calculate_net_zero_node)
workflow.add_node("fetch_solar", fetch_solar_potential_node)
workflow.add_node("hitl_review", hitl_review_checkpoint)
workflow.add_node("generate_docs", generate_documents_node)
workflow.add_node("finalize", finalize_deliverables_node)
workflow.add_node("error", error_handler_node)

# Define edges (linear with parallel branches where safe)
workflow.set_entry_point("validate")
workflow.add_edge("validate", "fetch_grid")
workflow.add_edge("validate", "parse_energy")  # Parallel: grid fetch and energy parse
workflow.add_edge("fetch_grid", "calc_baseline")
workflow.add_edge("parse_energy", "calc_baseline")
workflow.add_edge("calc_baseline", "project")
workflow.add_edge("calc_baseline", "analyze_measures")  # Parallel
workflow.add_edge("calc_baseline", "fetch_solar")       # Parallel
workflow.add_edge("project", "calc_netzero")
workflow.add_edge("analyze_measures", "calc_netzero")
workflow.add_edge("fetch_solar", "calc_netzero")
workflow.add_edge("calc_netzero", "hitl_review")
workflow.add_edge("hitl_review", "generate_docs")
workflow.add_edge("generate_docs", "finalize")
workflow.add_edge("finalize", END)

# Error handling (routes to error node on any exception)
workflow.add_conditional_edges("validate", lambda s: "error" if s.get("error") else "fetch_grid")
workflow.add_conditional_edges("fetch_grid", lambda s: "error" if s.get("error") else "calc_baseline")
workflow.add_conditional_edges("parse_energy", lambda s: "error" if s.get("error") else "calc_baseline")

# Compile the graph
app = workflow.compile()

# Execute
initial_state = {
    "inputs": {...},
    "validated": None,
    "grid_factors": None,
    "end_use_data": None,
    "baseline_carbon": None,
    "projection": None,
    "measures_analysis": None,
    "net_zero_pathway": None,
    "solar_potential": None,
    "hitl_review": None,
    "documents": None,
    "deliverables": None,
    "error": None,
    "logs": []
}

result = app.invoke(initial_state)
```
```