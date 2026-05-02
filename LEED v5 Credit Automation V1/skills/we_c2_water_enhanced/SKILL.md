---
name: leed-wec2-water-enhanced
version: 1.0.0
author: LEED Automation Platform
description: Automates LEED v5 WEc2 Enhanced Water Efficiency credit calculations, documentation, and points optimization across all six achievement pathways.
---

## Metadata
- **Credit Code:** WEc2
- **Credit Name:** Enhanced Water Efficiency
- **Points:** Up to 8 points (NC) / Up to 7 points (C&S)
- **Automation Level:** 87.5%
- **Complexity:** Medium
- **Primary Data Source:** EPA WaterSense Product Database, ENERGY STAR Product API, NRCS Soil Survey, NOAA NCEI Precipitation Data
- **HITL Required:** Yes

## Purpose
Automates the calculation, verification, and documentation of LEED v5 WEc2 Enhanced Water Efficiency credit across all achievement pathways, including whole-project water modeling, fixture efficiency verification, outdoor irrigation optimization, process water analysis, and alternative water source feasibility assessment.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `wep2_baseline_calcs` | JSON | WEp2 prerequisite output | Must contain baseline fixture water use (gal/yr), baseline flow rates, occupancy data, days of operation |
| `wep2_design_calcs` | JSON | WEp2 prerequisite output | Must contain design fixture water use (gal/yr), proposed flow rates, fixture counts |
| `rating_system` | Enum | User input | `NC` or `CS`; determines max points (8 vs 7) |
| `selected_pathways` | List[Enum] | User input | One or more of: `WholeProject`, `Fixtures`, `Appliances`, `Outdoor`, `Process`, `Reuse` |
| `site_latitude` | Float | Project location | -90.0 to 90.0 |
| `site_longitude` | Float | Project location | -180.0 to 180.0 |
| `building_area_sf` | Float | Project drawings | > 0 |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `additional_fixtures` | List[FixtureSpec] | `[]` | Post-prerequisite fixture upgrades beyond WEp2 (e.g., 1.0 gpf toilets, 0.5 gpm faucets) |
| `alternative_sources` | List[AltSource] | `[]` | Rainwater, graywater, condensate, municipally reclaimed water specs |
| `irrigation_area_sf` | Float | `0` | Landscaped area requiring irrigation (sq ft) |
| `plant_types` | List[PlantSpec] | `[]` | Species factor (Ks), hydrozone group, irrigation method per zone |
| `cooling_tower_present` | Boolean | `False` | Whether project includes cooling towers/evaporative condensers |
| `cooling_tower_specs` | CoolingTowerSpec | `null` | Makeup water analysis (Ca, alkalinity, SiO2, Cl-, conductivity), tons capacity, cycles |
| `commercial_kitchen` | Boolean | `False` | Whether project has commercial kitchen appliances |
| `kitchen_equipment` | List[KitchenSpec] | `[]` | Dishwasher type, meals/day, laundry lbs/year, ice machine type |
| `days_per_year` | Integer | `365` | Building operational days per year (1-366) |
| `indoor_water_use_breakdown` | JSON | `null` | Pre-calculated breakdown by end use (toilets, faucets, showers, kitchen, etc.) |
| `outdoor_water_use_breakdown` | JSON | `null` | Pre-calculated irrigation baseline and design water use |
| `process_water_use_breakdown` | JSON | `null` | Cooling tower, laundry, dishwashing, other process water |
| `reuse_ready_plumbing` | Boolean | `False` | Whether plumbing designed for future graywater reuse |
| `noaa_api_token` | String | `null` | NCEI API token for precipitation data (falls back to climate normals) |

## Workflow Steps (Durable)

### Step 1: Validate WEp2 Prerequisite Data
- **Type:** Validation
- **Automated:** Yes
- **Description:** Validates that all required WEp2 prerequisite calculations are present and consistent. Checks baseline fixture counts, baseline flow rates per LEED v5 Table 2 (1.6 gpf toilets, 1.0 gpf urinals, 2.2 gpm public faucets at 60 psi, 2.2 gpm private faucets at 60 psi, 2.2 gpm kitchen, 2.5 gpm showerheads at 80 psi), design flow rates, occupancy assumptions, and days of operation. Ensures the prerequisite 20% reduction is met. Flags inconsistencies where WEp2 data is missing or incomplete.
- **Output:** `ValidationReport` with status, errors, warnings, and normalized WEp2 data structure
- **On Failure:** Return error to user with specific missing fields; do not proceed until WEp2 data is complete

### Step 2: Enrich Fixture Data with WaterSense Verification
- **Type:** API Call
- **Automated:** Yes
- **Description:** For each proposed fixture specified by model number or type, queries the EPA WaterSense Product Search database (via `lookforwatersense.epa.gov` programmatic search) to verify WaterSense certification status. For U.S. and Canada projects, WaterSense-labeled fixtures are recommended and their verified flow rates are used in calculations. For dual-flush toilets, enforces the LEED v5 rule: full-flush volume must be ≤ 1.28 gpf; weighted averages are prohibited. Fetches actual certified flow/flush rates to replace manufacturer claims where available.
- **Output:** `VerifiedFixtureList` with certification status, verified flow rates, and source URLs
- **On Failure:** Log warning, use user-provided flow rates with annotation, continue with calculation

### Step 3: Enrich Appliance Data with ENERGY STAR Verification
- **Type:** API Call
- **Automated:** Yes
- **Description:** For commercial kitchen and laundry equipment, queries the ENERGY STAR certified products API (`data.energystar.gov`, dataset IDs: `pk8q-dim8` for dishwashers, ice machines, etc.). Verifies that proposed equipment meets ENERGY STAR Version 3.0 criteria for commercial dishwashers (undercounter ≤ 0.86 GPR, stationary door ≤ 0.89 GPR, etc.) or equivalent performance standards for international projects. Checks water consumption per rack/cycle against LEED v5 Tables 3-6 requirements.
- **Output:** `VerifiedApplianceList` with ENERGY STAR certification, water consumption specs, compliance status per table
- **On Failure:** Log warning, flag for manual verification, continue calculation with user-provided specs

### Step 4: Calculate Indoor Water Reduction (Option 2 Pathway)
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Calculates aggregate indoor fixture and fitting water use beyond the WEp2 prerequisite baseline. Formula: `Baseline_Indoor = Σ (Count_i × BaseRate_i × Uses_i × Days)` where BaseRate uses LEED v5 Table 2 baseline rates. `Design_Indoor = Σ (Count_i × DesignRate_i × Uses_i × Days)` including additional fixture improvements and alternative water sources. `PercentReduction = (Baseline_Indoor - Design_Indoor) / Baseline_Indoor × 100`. Alternative water contribution is calculated separately as: `AltContribution = AlternativeVolume / Baseline_Indoor × 100`. Points determined by: 30% = 1 pt, 35% = 2 pts, 40% = 3 pts (max).
- **Output:** `IndoorReductionResult` with gallons saved, percent reduction, points earned, and detailed breakdown
- **On Failure:** Return partial calculation with error annotations; notify human reviewer

### Step 5: Calculate Outdoor Water Use (Option 4 Pathway)
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Calculates irrigation water demand using the EPA WaterSense Water Budget approach. For Path 1 (No Irrigation): verifies no permanent irrigation system is installed; awards 2 points (NC) / 3 points (CS). For Path 2 (Efficient Irrigation): `IrrigationDemand = ETo × Ks × Area / (DU × 0.62)` where ETo = reference evapotranspiration (inches/day) from NOAA/NRCS climate data, Ks = species factor (0.2 for native/xeriscape, 0.5 for mixed, 0.7 for turf), Area = landscaped sq ft, DU = distribution uniformity (0.75 drip, 0.65 rotor, 0.55 spray). Compares to baseline conventional irrigation: `BaselineOutdoor = ETo × 0.7 × Area / (0.55 × 0.62)`. `OutdoorReduction = (BaselineOutdoor - DesignOutdoor) / BaselineOutdoor × 100`. Points: 50% = 1 pt, 100% (no potable) = 2 pts.
- **Output:** `OutdoorWaterResult` with annual gal, reduction %, points, irrigation schedule recommendation
- **On Failure:** Use climate normals fallback; flag if NRCS/NOAA data unavailable for location

### Step 6: Fetch Climate and Precipitation Data
- **Type:** API Call
- **Automated:** Yes
- **Description:** Fetches local climate data required for irrigation and rainwater harvesting calculations. Calls NOAA NCEI Climate Data Online API (`https://www.ncei.noaa.gov/cdo-web/api/v2/data`) with token auth to retrieve: (a) monthly precipitation normals (`NORMAL_MLY`, `datatypeid=MLY-PRCP-NORMAL`) for the nearest GHCN station, (b) daily ETo estimates from nClimGrid-Daily or PRISM data, (c) annual rainfall depth (`ANN-PRCP-NORMAL`). Calls NRCS Web Soil Survey API (`https://SDMDataAccess.sc.egov.usda.gov/`) for soil type, infiltration rate, and plant available water capacity at project location. For non-US projects, calls WorldClim/Open-Meteo precipitation data as fallback.
- **Output:** `ClimateData` with monthly precip (inches), annual precip, ETo (inches/day), soil type, growing season
- **On Failure:** Use climate zone defaults from ASHRAE/IGCC tables; flag for HITL verification

### Step 7: Calculate Alternative Water Source Contribution (Option 6 Pathway)
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Calculates volume and feasibility of alternative water sources. Rainwater harvesting: `RainwaterVolume = CatchmentArea_sf × AnnualPrecip_in × RunoffCoeff × 0.623 gal/sf/in × CollectionEfficiency` where RunoffCoeff = 0.95 (metal roof), 0.85 (concrete), 0.80 (shingle). Graywater: `GraywaterVolume = Σ (Occupants × FlowRate × Uses × Days × 0.65 graywater_fraction)`. Condensate: `CondensateVolume = ACFM × SpecificHumidityDiff × AirDensity × OperatingHours / WaterDensity` simplified per ASHRAE. Alternative source contribution % = `AltVolume / TotalDemand × 100`. Determines points for Path 2 Alternative Sources (2 points) or Path 1 Reuse-Ready (1 point).
- **Output:** `AlternativeWaterResult` with volume per source, contribution %, points, storage sizing recommendation
- **On Failure:** Return estimate with uncertainty bounds; escalate to HITL

### Step 8: Calculate Process Water Optimization (Option 5 Pathway)
- **Type:** Calculation
- **Automated:** Yes
- **Description:** For projects with cooling towers, calculates maximum cycles of concentration from potable water analysis. `Cycles_max = min(Ca_max/Ca_actual, Alk_max/Alk_actual, SiO2_max/SiO2_actual, Cl_max/Cl_actual, Cond_max/Cond_actual)` where max values from LEED v5 Table 8 (Ca 600 ppm, alkalinity 500 ppm, SiO2 150 ppm, Cl- 300 ppm, conductivity 3300 uS/cm). Awards 1 point for achieving max cycles without exceeding limits. Awards 2 points (NC) / 2-3 points (CS) for 25-30% cycle increase OR 20-30% alternative water use. For Path 2 (Optimize Cooling Water): compares proposed to baseline water-cooled chiller with 3 cycles, 0.002% drift. `CoolingWaterReduction = (Baseline_gal - Proposed_gal) / Baseline_gal × 100`. Awards 1-2 points based on reduction threshold.
- **Output:** `ProcessWaterResult` with cycles achieved, water saved, points, maintenance recommendations
- **On Failure:** Require manual water analysis input; flag incomplete data

### Step 9: Calculate Whole-Project Water Use (Option 1 Pathway)
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Aggregates all water end uses (indoor fixtures, outdoor irrigation, process water, appliances) into a whole-project baseline and proposed model. `TotalBaseline = IndoorBaseline + OutdoorBaseline + ProcessBaseline + ApplianceBaseline`. `TotalProposed = IndoorDesign + OutdoorDesign + ProcessDesign + ApplianceDesign - AlternativeWater`. `WholeProjectReduction = (TotalBaseline - TotalProposed) / TotalBaseline × 100`. Points per LEED v5 Table 1: 30%=1, 35%=2, 40%=3, 45%=4, 50%=5, 55%=6, 60%=7, 65%=8 (NC) / up to 55%=7 (CS). If alternative water is ≥ 20% of total, adds "Alternative Water" bonus notation.
- **Output:** `WholeProjectResult` with total gal/yr baseline and proposed, reduction %, points earned, pathway recommendation
- **On Failure:** Return component-level results with aggregation error flagged

### Step 10: Optimize Points Strategy
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Evaluates all possible combinations of achievement pathways to maximize points within the NC (8) or CS (7) limit. Rules: Option 1 (Whole-Project) is mutually exclusive with Options 2-6 combined. If Options 2-6 are selected, sums points from each. Checks for maximums: Option 2 max 3 pts, Option 3 max 2 pts, Option 4 max 2 pts (NC) / 3 pts (CS), Option 5 max 2 pts (NC) / 3 pts (CS), Option 6 max 2 pts. Identifies the highest-point achievable combination and flags which additional measures would yield more points. Provides marginal cost-benefit analysis (e.g., "Upgrading to 1.0 gpf toilets yields +1 point for $X fixture cost").
- **Output:** `PointsOptimizationReport` with optimal pathway combination, total points, marginal recommendations, ROI estimate
- **On Failure:** Return single-pathway results with note that optimization failed

### Step 11: Human Review Checkpoint - Alternative Sources & Irrigation
- **Type:** Human Review
- **Automated:** No
- **Description:** Presents alternative water source feasibility analysis and irrigation calculations to a qualified LEED AP or plumbing engineer for verification. Reviewer must confirm: (a) rainwater catchment area and runoff coefficients are realistic for roof materials, (b) graywater sources and treatment requirements comply with local plumbing code, (c) condensate recovery is mechanically feasible for HVAC configuration, (d) irrigation plant species factors and hydrozoning match landscape plans, (e) NRCS/NOAA climate data is representative of microclimate. Reviewer can approve, request revisions, or reject with comments. All calculations, source data, and assumptions are presented in review dashboard.
- **Output:** `HITLDecision` with status (approved/rejected/revise), reviewer comments, timestamp
- **On Failure:** Hold workflow; notify project team; SLA clock starts

### Step 12: Generate Enhanced Water Efficiency Calculations Document
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generates a comprehensive PDF calculation report following LEED v5 BD+C Reference Guide format. Includes: executive summary, WEp2 baseline summary, detailed fixture-by-fixture water use table, indoor reduction calculations, outdoor irrigation water budget with ETo and Ks values, process water optimization (cooling tower cycles, equipment water use), alternative water source feasibility with monthly yield estimates, whole-project summary with pie charts, points calculation table per selected pathway(s), and compliance statement. All formulas shown with values. Appendix includes API data source citations and climate data station IDs.
- **Output:** `WEc2_Calculations.pdf` (formatted for LEED Online upload)
- **On Failure:** Retry once with simplified formatting; notify user on second failure

### Step 13: Generate Alternative Water Source Analysis Document
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generates a standalone PDF alternative water source analysis including: source inventory (rainwater, graywater, condensate, reclaimed), monthly yield vs. demand curves, storage tank sizing calculations, overflow and dry-period analysis, treatment requirements per end use (irrigation vs. flush fixtures vs. cooling tower makeup), payback analysis, and code compliance checklist (IPC, UPC, local amendments). Includes catchment area diagrams and schematics placeholders.
- **Output:** `AltWaterSource_Analysis.pdf`
- **On Failure:** Retry once; fallback to markdown export

### Step 14: Generate Points Calculation Table
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Generates an XLSX workbook with multiple tabs: (1) Points Summary - all pathways with points earned, max points, and gap analysis, (2) Fixture Calculator - interactive calculator with all LEED v5 baseline rates, user-adjustable fixture counts and flow rates with live reduction % and points, (3) Irrigation Calculator - ETo lookup, plant database with Ks values, irrigation schedule, (4) Alternative Water Calculator - monthly rainwater yield by catchment area, graywater daily generation, (5) Cooling Tower Calculator - water analysis input, cycles calculation, (6) Whole-Project Aggregator - sums all tabs with pathway selector dropdown.
- **Output:** `WEc2_PointsCalculator.xlsx`
- **On Failure:** Generate CSV exports per tab; notify user

### Step 15: Finalize and Upload
- **Type:** API Call / Document Generation
- **Automated:** Yes
- **Description:** Packages all output documents with metadata (project ID, credit code, version, generation timestamp). Uploads to project document repository. Creates LEED Online-ready submission package with forms pre-populated where API data is available. Generates a compliance checklist for any remaining manual items (e.g., fixture cut sheets, water analysis lab reports, irrigation drawings). Returns final result with earned points, submission status, and action items.
- **Output:** `FinalSubmissionPackage` with document URLs, points summary, status, and next steps
- **On Failure:** Queue for retry; notify project administrator

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 11: Alternative Sources & Irrigation | LEED AP / Plumbing Engineer | 48 hours | Verify alternative water source feasibility (rainwater catchment realism, graywater code compliance, condensate mechanical feasibility), confirm plant species factors and hydrozoning match landscape plans, validate NRCS/NOAA climate data against local microclimate knowledge. Approve, request revisions with specific feedback, or reject with rationale. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| EPA WaterSense Product Search | Verify fixture certification, flow rates | US, Canada | Manual verification via manufacturer spec sheets | N/A (web scraping with 2s delay) |
| ENERGY STAR Product API (Socrata) | Verify commercial kitchen/laundry equipment water efficiency | US, Canada | ENERGY STAR Product Finder web lookup | 1000 req/day (Socrata), 5 req/sec |
| NRCS Web Soil Survey / SDM Data Access | Soil type, infiltration, plant available water for irrigation | US only | USDA county soil surveys (manual) | 50 req/min |
| NOAA NCEI Climate Data Online | Monthly/annual precipitation, climate normals for rainwater/irrigation | Global (US stations best coverage) | WorldClim 2.1 historical data, PRISM (US), Open-Meteo | 10,000 req/day, 5 req/sec |
| NOAA NCEI Search Service v1 | Discover climate stations near project site | Global | Manual station ID lookup via HOMR | 10,000 req/day |
| nClimGrid-Daily / GHCNd | Daily precipitation and temperature grids | US (CONUS) | PRISM gridded climate data | NetCDF download (no strict limit) |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | Full API support: WaterSense, ENERGY STAR, NRCS, NOAA. All pathways supported. |
| Canada | Available | WaterSense applies (recommended). ENERGY STAR available. NRCS not applicable; use Canadian soil surveys (manual fallback). NOAA stations available near border; use Environment Canada for northern sites. |
| Europe | Limited | No WaterSense (use local efficiency labels). ENERGY STAR for some appliances. No NRCS; use JRC SoilGrids or national soil databases. NOAA limited; use WorldClim/Open-Meteo. |
| Asia-Pacific | Limited | No WaterSense. ENERGY STAR limited. No NRCS; use FAO HWSD or national soil data. NOAA stations limited to certain countries; use WorldClim/JMA (Japan)/BOM (Australia). |
| Middle East/Africa | Limited | No WaterSense. ENERGY STAR limited. No NRCS; use FAO HWSD. NOAA very sparse; WorldClim or national met services required. |
| Latin America | Limited | No WaterSense. ENERGY STAR limited. No NRCS; use FAO HWSD or national soil data. NOAA stations in some countries; WorldClim fallback. |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| WEp2 prerequisite data missing/inconsistent | Halt workflow; return validation report | Yes (immediate) | 0 |
| WaterSense API unreachable (timeout) | Use user-provided fixture specs; flag for manual verification | Yes (in final report) | 2 (exponential backoff) |
| ENERGY STAR API rate limit exceeded | Queue for off-peak retry; use cached data if < 30 days old | Yes (if cached data stale) | 3 (1 hour delay) |
| NOAA NCEI token invalid/expired | Use climate normals fallback from built-in ASHRAE climate zone tables | Yes | 1 (after token refresh) |
| No climate station within 50km | Expand search radius to 100km; then use climate zone default | Yes | 2 |
| NRCS soil data unavailable for location | Use FAO HWSD SoilGrids 250m global data | No (logged) | 1 |
| Cooling tower water analysis incomplete | Halt Option 5 calculation; continue other pathways | Yes | 0 |
| Graywater code conflict detected | Flag for HITL review; do not count graywater until approved | Yes (HITL alert) | 0 |
| Points exceed maximum for rating system | Cap at max; flag optimization logic error | Yes | 0 |
| PDF generation failure | Retry with simplified template; fallback to markdown | Yes (if both fail) | 1 |
| XLSX generation failure | Output CSV tabs individually | Yes | 1 |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Enhanced Water Efficiency Calculations | PDF | Complete LEED v5 WEc2 calculation report with all formulas, values, and compliance statements. Formatted for LEED Online submission. |
| Alternative Water Source Analysis | PDF | Standalone feasibility analysis for rainwater, graywater, condensate, and reclaimed water with monthly yield curves, storage sizing, and payback analysis. |
| Points Calculation Table | XLSX | Interactive workbook with 6 tabs: Points Summary, Fixture Calculator, Irrigation Calculator, Alternative Water Calculator, Cooling Tower Calculator, and Whole-Project Aggregator. |
| Compliance Checklist | PDF | Remaining manual action items (e.g., lab reports, cut sheets, drawings) with responsible party and due dates. |
| HITL Review Record | PDF | Audit trail of human review decision, comments, and timestamps for alternative water and irrigation verification. |

## Testing
```bash
# Unit tests for calculation modules
python -m pytest skills/wec2/tests/test_fixture_calculations.py -v
python -m pytest skills/wec2/tests/test_irrigation_calculations.py -v
python -m pytest skills/wec2/tests/test_alternative_water.py -v
python -m pytest skills/wec2/tests/test_cooling_tower_cycles.py -v
python -m pytest skills/wec2/tests/test_points_optimization.py -v
python -m pytest skills/wec2/tests/test_api_clients.py -v
python -m pytest skills/wec2/tests/test_document_generation.py -v

# Integration tests (requires API keys)
python -m pytest skills/wec2/tests/integration/ --noaa-token=$NOAA_TOKEN --energystar-key=$ENERGY_STAR_KEY

# End-to-end test with sample project data
python -m pytest skills/wec2/tests/e2e/test_full_workflow.py -v --project-data=skills/wec2/tests/fixtures/sample_nc_project.json
```

## Example Usage (OpenAI Agents SDK + Restate)
```python
from leed_platform.skills import LEEDWaterEnhancedSkill

# Initialize with WEp2 prerequisite data and project location
skill = LEEDWaterEnhancedSkill(
    project_id="LEED-2026-12345",
    inputs={
        "rating_system": "NC",
        "wep2_baseline_calcs": {
            "total_baseline_gal_yr": 847500,
            "fixtures": [
                {"type": "toilet", "count": 45, "baseline_rate_gpf": 1.6, "uses_per_day": 3},
                {"type": "urinal", "count": 12, "baseline_rate_gpf": 1.0, "uses_per_day": 3},
                {"type": "public_faucet", "count": 30, "baseline_rate_gpm": 2.2, "uses_per_day": 15, "duration_sec": 15},
                {"type": "private_faucet", "count": 20, "baseline_rate_gpm": 2.2, "uses_per_day": 5, "duration_sec": 30},
                {"type": "shower", "count": 25, "baseline_rate_gpm": 2.5, "uses_per_day": 1, "duration_min": 8}
            ],
            "days_per_year": 260,
            "occupants": 150
        },
        "wep2_design_calcs": {
            "total_design_gal_yr": 632100,
            "fixtures": [
                {"type": "toilet", "count": 45, "design_rate_gpf": 1.28, "model": "Kohler-3810", "watersense": True},
                {"type": "urinal", "count": 12, "design_rate_gpf": 0.5, "model": "Sloan-WES-1000", "watersense": True},
                {"type": "public_faucet", "count": 30, "design_rate_gpm": 0.5, "model": "Delta-559HA", "watersense": True},
                {"type": "private_faucet", "count": 20, "design_rate_gpm": 1.5, "model": "Moen-6410", "watersense": True},
                {"type": "shower", "count": 25, "design_rate_gpm": 2.0, "model": "Moen-26008", "watersense": True}
            ]
        },
        "selected_pathways": ["WholeProject", "Outdoor", "Reuse"],
        "site_latitude": 33.4484,
        "site_longitude": -112.0740,
        "building_area_sf": 125000,
        "irrigation_area_sf": 15000,
        "plant_types": [
            {"species": "Bouteloua_gracilis", "ks": 0.25, "hydrozone": "native_grass", "irrigation_method": "drip", "area_sf": 8000},
            {"species": "Larrea_tridentata", "ks": 0.15, "hydrozone": "xeriscape", "irrigation_method": "drip", "area_sf": 5000},
            {"species": "Cynodon_dactylon", "ks": 0.65, "hydrozone": "turf_play", "irrigation_method": "rotor", "area_sf": 2000}
        ],
        "alternative_sources": [
            {"type": "rainwater", "catchment_area_sf": 45000, "roof_material": "metal", "collection_efficiency": 0.95, "end_uses": ["irrigation", "toilet_flush"]},
            {"type": "graywater", "sources": ["showers", "lavatories"], "graywater_fraction": 0.65, "treatment": "biological_filtration", "end_uses": ["irrigation"]}
        ],
        "cooling_tower_present": True,
        "cooling_tower_specs": {
            "tons": 500,
            "makeup_water_analysis": {"ca_ppm": 120, "alkalinity_ppm": 85, "sio2_ppm": 25, "cl_ppm": 45, "conductivity_us_cm": 420},
            "current_cycles": 4
        },
        "commercial_kitchen": True,
        "kitchen_equipment": [
            {"type": "dishwasher_undercounter", "model": "Hobart-LXIH", "meals_per_day": 200, "water_use_gpr": 0.74, "energy_star": True},
            {"type": "ice_machine", "model": "Scotsman-EH330", "capacity_lb_day": 400, "water_use_gal_100lb": 20, "energy_star": True}
        ]
    }
)

# Execute the full workflow
result = await skill.execute()

# Result structure
print(f"Total Points Earned: {result.total_points}")  # e.g., 6
print(f"Optimal Pathways: {result.optimal_pathways}")  # e.g., ['WholeProject']
print(f"Whole-Project Reduction: {result.whole_project_reduction_pct}%")  # e.g., 52.3%
print(f"Indoor Reduction: {result.indoor_reduction_pct}%")
print(f"Outdoor Reduction: {result.outdoor_reduction_pct}%")
print(f"Alternative Water Contribution: {result.alternative_contribution_pct}%")
print(f"Documents: {result.documents}")
# ['WEc2_Calculations.pdf', 'AltWaterSource_Analysis.pdf', 'WEc2_PointsCalculator.xlsx']
```

## Platform Workflow (OpenAI Agents SDK + Restate)
```python
from langgraph.graph import StateGraph, END
from leed_platform.state import LEEDWaterState
from leed_platform.nodes import (
    validate_wep2_data,
    verify_watersense_fixtures,
    verify_energy_star_appliances,
    calculate_indoor_reduction,
    calculate_outdoor_water,
    fetch_climate_data,
    calculate_alternative_water,
    calculate_process_water,
    calculate_whole_project,
    optimize_points_strategy,
    human_review_checkpoint,
    generate_calculation_pdf,
    generate_altwater_pdf,
    generate_points_xlsx,
    finalize_submission
)
from leed_platform.checkpoints import HITLCheckpoint

# Define the LangGraph workflow for this skill
workflow = StateGraph(LEEDWaterState)

# Node 1: Validation
workflow.add_node("validate", validate_wep2_data)

# Node 2: API enrichment (parallel fixture + appliance verification)
workflow.add_node("verify_fixtures", verify_watersense_fixtures)
workflow.add_node("verify_appliances", verify_energy_star_appliances)

# Node 3: Calculation branches (parallel where possible)
workflow.add_node("calc_indoor", calculate_indoor_reduction)
workflow.add_node("calc_outdoor", calculate_outdoor_water)
workflow.add_node("calc_altwater", calculate_alternative_water)
workflow.add_node("calc_process", calculate_process_water)

# Node 4: Climate data fetch (outdoor + altwater dependency)
workflow.add_node("fetch_climate", fetch_climate_data)

# Node 5: Aggregation
workflow.add_node("calc_whole_project", calculate_whole_project)

# Node 6: Optimization
workflow.add_node("optimize", optimize_points_strategy)

# Node 7: Human-in-the-loop checkpoint
workflow.add_node("hitl_review", human_review_checkpoint)

# Node 8: Document generation (parallel)
workflow.add_node("gen_calc_pdf", generate_calculation_pdf)
workflow.add_node("gen_altwater_pdf", generate_altwater_pdf)
workflow.add_node("gen_points_xlsx", generate_points_xlsx)

# Node 9: Finalize
workflow.add_node("finalize", finalize_submission)

# Define edges with conditional routing based on selected pathways
workflow.set_entry_point("validate")
workflow.add_edge("validate", "verify_fixtures")
workflow.add_edge("validate", "verify_appliances")

# After verification, branch to climate fetch (required for outdoor + altwater)
workflow.add_edge("verify_fixtures", "fetch_climate")
workflow.add_edge("verify_appliances", "fetch_climate")

# Climate data feeds outdoor and alternative calculations
workflow.add_edge("fetch_climate", "calc_outdoor")
workflow.add_edge("fetch_climate", "calc_altwater")

# Indoor and process calculations can run in parallel with climate-dependent calcs
workflow.add_edge("verify_fixtures", "calc_indoor")
workflow.add_edge("verify_appliances", "calc_process")

# All calculations must complete before whole-project aggregation
workflow.add_edge("calc_indoor", "calc_whole_project")
workflow.add_edge("calc_outdoor", "calc_whole_project")
workflow.add_edge("calc_altwater", "calc_whole_project")
workflow.add_edge("calc_process", "calc_whole_project")

# Optimization after aggregation
workflow.add_edge("calc_whole_project", "optimize")

# HITL checkpoint before document generation
workflow.add_edge("optimize", "hitl_review")

# Conditional: if HITL approved, generate documents; if rejected, loop back
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: state["hitl_status"],
    {
        "approved": "gen_calc_pdf",
        "rejected": "calc_altwater",  # Rejected: revisit altwater assumptions
        "revise": "calc_outdoor"      # Revision requested: revisit irrigation
    }
)

# Document generation in parallel
workflow.add_edge("gen_calc_pdf", "finalize")
workflow.add_edge("gen_altwater_pdf", "finalize")
workflow.add_edge("gen_points_xlsx", "finalize")

workflow.add_edge("finalize", END)

# Compile the workflow
app = workflow.compile(
    checkpointer=HITLCheckpoint(
        checkpoint_id="wec2_hitl",
        reviewer_roles=["LEED_AP", "Plumbing_Engineer"],
        sla_hours=48
    )
)

# Execute
initial_state = LEEDWaterState(
    project_id="LEED-2026-12345",
    inputs={...},
    step_results={},
    hitl_status="pending",
    documents=[]
)

final_state = await app.ainvoke(initial_state, config={"recursion_limit": 50})
```

## Calculation Reference

### LEED v5 Baseline Fixture Rates (Table 2)
| Fixture | Baseline Rate (IP) | Baseline Rate (SI) |
|---------|-------------------|-------------------|
| Toilet (water closet) | 1.6 gpf | 6.0 lpf |
| Urinal | 1.0 gpf | 3.8 lpf |
| Public lavatory faucet | 0.50 gpm at 60 psi | 1.9 lpm at 415 kPa |
| Private lavatory faucets | 2.2 gpm at 60 psi | 8.3 lpm at 415 kPa |
| Kitchen faucet | 2.2 gpm at 60 psi | 8.3 lpm at 415 kPa |
| Showerhead | 2.5 gpm at 80 psi per stall | 9.5 lpm at 550 kPa |

### Indoor Water Use Formula
```
FixtureWaterUse (gal/yr) = Count × FlowRate × UsesPerDay × DaysPerYear × (DurationMin/1 for flow; 1 for flush)

IndoorBaseline = Σ FixtureWaterUse(baseline_rate)
IndoorDesign   = Σ FixtureWaterUse(design_rate)
IndoorReduction% = (IndoorBaseline - IndoorDesign) / IndoorBaseline × 100
```

### Outdoor Irrigation Formula (WaterSense Water Budget)
```
ETc = ETo × Ks  (crop/landscape evapotranspiration, inches/day)
IrrigationDemand (gal/day) = ETc × Area_sf / (DU × 0.62)

Where:
  ETo = Reference evapotranspiration (inches/day) from NOAA/NRCS
  Ks  = Species factor (0.1-0.9)
  Area_sf = Landscaped area (sq ft)
  DU  = Distribution uniformity (drip=0.75, rotor=0.65, spray=0.55)
  0.62 = Conversion factor (gal/sf per inch of water)

AnnualOutdoor = IrrigationDemand × OperatingDaysPerYear
```

### Rainwater Harvesting Formula
```
RainwaterVolume (gal/yr) = CatchmentArea_sf × AnnualPrecip_in × RunoffCoeff × 0.623 × CollectionEfficiency

Runoff Coefficients:
  Metal roof: 0.95
  Concrete: 0.85
  Asphalt shingle: 0.80
  Clay tile: 0.75
  Gravel: 0.60

MonthlyVolume = CatchmentArea × MonthlyPrecip × RunoffCoeff × 0.623 × CollectionEfficiency
```

### Graywater Generation Formula
```
GraywaterVolume (gal/day) = Σ (Occupants_i × FlowRate_i × Uses_i × Duration_i × 0.65)

Where 0.65 is the typical graywater fraction of total fixture water use.

AnnualGraywater = GraywaterVolume × DaysPerYear
```

### Cooling Tower Cycles Formula
```
Cycles_max = min(
    600 / Ca_actual,
    500 / Alkalinity_actual,
    150 / SiO2_actual,
    300 / Cl_actual,
    3300 / Conductivity_actual
)

EvaporationRate (gpm) = Tons × 0.0015  (approximate)
Blowdown (gpm) = EvaporationRate / (Cycles - 1)
MakeupWater (gpm) = EvaporationRate + Blowdown
AnnualMakeup (gal) = MakeupWater × 60 × OperatingHours
```

### Points Tables

**Option 1: Whole-Project Water Use (NC Table 1 / CS Table 11)**
| Reduction | NC Points | CS Points |
|-----------|-----------|-----------|
| 30% | 1 | 1 |
| 35% | 2 | 2 |
| 40% | 3 | 3 |
| 45% | 4 | 4 |
| 50% | 5 | 5 |
| 55% | 6 | 6 |
| 60% | 7 | 7 |
| 65% | 8 | — |

**Option 2: Fixture and Fittings Calculated Reduction**
| Reduction | Points |
|-----------|--------|
| 30% | 1 |
| 35% | 2 |
| 40% | 3 |

**Option 4: Outdoor Water Use - Path 2 (Efficient Irrigation)**
| Reduction | Points (NC) | Points (CS) |
|-----------|-------------|-------------|
| 50% | 1 | 1 |
| 100% (no potable) | 2 | 2-3 |

**Option 5: Process Water - Cooling Tower Cycles (CS)**
| Achievement | CS Points |
|-------------|-----------|
| Max cycles achieved | 1 |
| +25% cycles OR +20% alt water | 2 |
| +30% cycles OR +30% alt water | 3 |

**Option 6: Water Reuse**
| Path | Points |
|------|--------|
| Path 1: Reuse-Ready System | 1 |
| Path 2: Alternative Water Sources | 2 |

## License & Maintenance
- **License:** Proprietary - LEED Automation Platform
- **Maintainer:** LEED Automation Platform Engineering Team
- **Last Updated:** 2025-06
- **LEED Version:** v5 BD+C (November 2025 Edition)
- **Next Review:** Upon LEED v5 reference guide update or API endpoint changes
