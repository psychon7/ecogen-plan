# LEED v5 WE + EQ Credit Automation Potential Analysis

**Analysis Date:** 2025  
**Analyst:** AI LEED Automation Strategist  
**Scope:** 12 Credits — 4 Water Efficiency (WE) + 8 Indoor Environmental Quality (EQ)  
**Framework:** Automation Score (1-5), Commercial Value (1-5), Risk (Low/Medium/High), AI Technique Mapping, Blueprint Design

---

## Executive Summary

| Category | Credits Analyzed | High Automation (4-5) | Medium Automation (3) | Low Automation (1-2) | Total Points Represented |
|----------|-----------------|----------------------|----------------------|---------------------|-------------------------|
| Water Efficiency (WE) | 4 | 4 | 0 | 0 | Prereqs + 9-15 pts |
| Indoor Environmental Quality (EQ) | 8 | 5 | 2 | 1 | Prereqs + 13-15 pts |
| **TOTAL** | **12** | **9** | **2** | **1** | **All WE/EQ Points** |

**Key Finding:** Water Efficiency credits are the highest-value automation targets — calculation-driven, data-rich, and universally applicable. EQ credits split into highly automatable narrative/plan credits (EQp1, EQp2, EQc3) and partially automatable calculation credits (EQc2 daylight, EQc4 thermal modeling). Only EQc5 (Air Quality Testing) has low automation potential due to mandatory physical laboratory testing.

---

## Table 1: Master Scoring Matrix — All 12 Credits

| Credit | Name | Auto Score | Comm. Value | Risk | Doc Type | Key Inputs | AI Techniques | Recommendation |
|--------|------|------------|-------------|------|----------|------------|---------------|----------------|
| **WEp1** | Water Metering & Reporting | 4 | 4 | Low | plan, commitment letter | spec sheets, meter locations | Template filling, LLM narrative, checklist generation | **MVP** |
| **WEp2** | Minimum Water Efficiency | 5 | 5 | Low | calculation, specification | fixture schedule, cut sheets | Spreadsheet extraction, calc engine, spec parsing, template filling | **MVP** |
| **WEc1** | Water Metering & Leak Detection | 4 | 4 | Low | plan, layout drawing | submeter specs, plumbing drawings | Template filling, drawing annotation, LLM narrative | **MVP** |
| **WEc2** | Enhanced Water Efficiency | 5 | 5 | Low-Med | calculation, specification | fixture schedule, equipment specs, water analysis | Spreadsheet extraction, calc engine, multi-option scoring, spec parsing | **MVP** |
| **EQp1** | Construction Management | 4 | 5 | Low | plan, checklist, narrative | project schedule, material list, site layout | LLM narrative generation, template filling, checklist auto-generation | **MVP** |
| **EQp2** | Fundamental Air Quality | 4 | 4 | Medium | calculation, specification, narrative | HVAC schedules, OA rates, filtration specs | Calculation engine, spec verification, LLM narrative, template filling | **MVP** |
| **EQp3** | No Smoking / Vehicle Idling | 3 | 3 | Low | plan, site plan | site layout, building footprint | Site plan analysis, template filling, distance calculation | **Later** |
| **EQc1** | Enhanced Air Quality | 3 | 3 | Medium | calculation, narrative | ventilation calcs from EQp2, IAQ model results | Calculation engine, template filling, results parsing | **Later** |
| **EQc2** | Occupant Experience | 4 | 4 | Medium | survey, calculation, narrative | floor plans, glazing specs, luminaire data | Survey generation, daylight simulation integration, spatial analysis, LLM narrative | **MVP** |
| **EQc3** | Accessibility & Inclusion | 4 | 4 | Low | checklist, narrative, drawing | local accessibility codes, floor plans | Standards cross-check, template filling, LLM narrative, checklist generation | **MVP** |
| **EQc4** | Resilient Spaces | 3 | 3 | Medium | calculation, narrative, specification | TMY weather data, building envelope specs, window schedule | Thermal simulation integration, template filling, LLM narrative | **Later** |
| **EQc5** | Air Quality Testing & Monitoring | 2 | 3 | High | test report, specification | laboratory test results, monitor specs | Document parsing, test plan generation, spec verification | **Assist Only** |

---

## Table 2: Scoring Legend & Definitions

### Automation Score (1-5)
| Score | Definition | Meaning |
|-------|-----------|---------|
| 5 | Fully Automated | AI can perform calculations, generate all documents, and produce submission-ready packages with minimal human review |
| 4 | Mostly Automated | AI handles 80%+ of work; human review for accuracy and sign-off only |
| 3 | Partially Automated | AI assists with 50-80%; significant human input on analysis and judgment |
| 2 | Low Automation | AI assists with 20-50%; mostly manual with AI tooling support |
| 1 | Not Practical | Requires physical testing, on-site verification, or regulatory sign-off that cannot be automated |

### Commercial Value (1-5)
| Score | Definition |
|-------|-----------|
| 5 | High-volume prerequisite applicable to 100% of projects; significant time savings; client-visible value |
| 4 | Applicable to most projects; meaningful time savings; supports multiple credit pathways |
| 3 | Moderate applicability; specialized project types; niche but valuable when applicable |
| 2 | Limited applicability; small time savings; low client visibility |
| 1 | Rarely applicable; minimal commercial impact |

### Risk Level
| Level | Meaning |
|-------|---------|
| Low | Well-defined calculations/tables; clear compliance thresholds; low liability |
| Medium | Some engineering judgment required; cross-referenced standards; moderate review needed |
| High | Physical testing required; laboratory accreditation; regulatory compliance; high liability |

---

## Part 1: Detailed Credit Analysis — Water Efficiency (WE)

---

### WEp1: Water Metering and Reporting

**Overview:** Prerequisite requiring permanent water meters, separate potable/alternative water metering, and a 5-year USGBC data sharing commitment.

#### Scoring
- **Automation Score:** 4/5
- **Commercial Value:** 4/5 (100% of projects; simple but mandatory)
- **Risk Level:** Low

#### Documentation Type
- Commitment letter (narrative)
- Meter specification compliance table
- Access protocol documentation
- Installation verification checklist

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **Specifications (human-provided)** | Meter manufacturer, model, flow range, communication protocol |
| **Drawings (human-provided)** | Meter locations on plumbing plans |
| **AI-Generated** | Commitment letter draft, access protocol narrative, compliance checklist |

#### AI Techniques Applicable
1. **Template Filling:** Auto-generate the 5-year commitment letter from project data (owner name, project ID, meter specifications)
2. **LLM Narrative Generation:** Draft access protocol narrative describing how facility manager accesses data (BMS, cloud, app)
3. **Checklist Generation:** Auto-create meter verification checklist from submittal requirements
4. **Specification Parsing:** Extract meter capabilities from manufacturer cut sheets (flow range, data recording interval, communication options)

#### Automation Blueprint

```
Step 1: PROJECT DATA INTAKE
├── Input: Project name, owner, address, LEED ID, project type (NC/C+S)
├── Input: Meter specifications (manufacturer, model, recording capability)
└── AI Action: Populate project metadata into template database

Step 2: COMMITMENT LETTER GENERATION (LLM)
├── Template: USGBC-standard 5-year water data sharing commitment
├── AI Action: Generate signed-ready commitment letter with project specifics
├── AI Action: Insert meter count, types, and reporting frequency
└── Output: Draft commitment letter for owner signature

Step 3: ACCESS PROTOCOL DOCUMENTATION (LLM)
├── Input: Meter communication method (BMS/local network/cloud/app)
├── AI Action: Generate narrative describing real-time data access pathway
├── AI Action: Document user roles (facility manager, tenant access)
└── Output: Access protocol narrative (1-2 pages)

Step 4: COMPLIANCE CHECKLIST GENERATION
├── AI Action: Generate project-specific checklist from WEp1 requirements
├── Items: [ ] Meter installed, [ ] Separate potable/alternative metering, 
│           [ ] Recording capability confirmed, [ ] Access verified,
│           [ ] Commitment letter signed
└── Output: Interactive compliance checklist

Step 5: PACKAGE ASSEMBLY
├── AI Action: Compile all documents into WEp1 submission package
├── AI Action: Cross-reference with WEp2/WEc1 for meter consistency
└── Output: Complete WEp1 documentation package

HUMAN REVIEW POINTS: Owner signature on commitment letter; visual 
verification of meter installation (photos); final approval of access protocol.
```

#### Final Recommendation: **Automate in MVP**

---

### WEp2: Minimum Water Efficiency

**Overview:** Prerequisite with three requirement areas: (1) fixture/fitting efficiency (prescriptive OR performance path), (2) equipment water efficiency, (3) outdoor water use efficiency. This is the **highest-value automation target** in the entire WE/EQ category.

#### Scoring
- **Automation Score:** 5/5
- **Commercial Value:** 5/5 (100% of projects; calculation-heavy; prerequisite = must-pass)
- **Risk Level:** Low

#### Documentation Type
- **Calculation** (fixture water reduction %, TIR reduction %)
- **Specification** (fixture cut sheets, appliance compliance tables)
- **Narrative** (irrigation approach justification)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **Fixture Schedule (human-provided)** | Fixture type, manufacturer, model, quantity, location, flow/flush rate |
| **Cut Sheets / Specs (human-provided)** | Manufacturer documentation with certified flow/flush rates |
| **Occupancy Data (human-provided)** | FTE count, transient count, gender ratio, operating days/year |
| **Irrigation Data (human-provided)** | Landscape area, plant types, irrigation system type, climate zone |
| **AI-Calculated** | Water reduction %, baseline vs. proposed consumption, compliance status per fixture, TIR calculation |

#### AI Techniques Applicable
1. **Spreadsheet/Calculation Engine:** Full water use reduction calculator — baseline vs. proposed
2. **Document Parsing (OCR):** Extract flow/flush rates from manufacturer cut sheets
3. **Template Filling:** Auto-populate LEED credit forms with calculated results
4. **Multi-Pathway Scoring:** Simultaneously evaluate Option 1 (prescriptive) and Option 2 (performance) to recommend optimal path
5. **Cross-Credit Integration:** Feed WEp2 calculations into WEc2 for enhanced efficiency points

#### Automation Blueprint — WATER CALCULATION ENGINE

```
STEP 1: FIXTURE DATA INTAKE & EXTRACTION
├── Input Method A: Manual fixture schedule upload (Excel/CSV)
├── Input Method B: OCR extraction from plumbing drawings/schedules
│   └── AI parses PDF/DWG fixture schedules → structured database
├── Input Method C: Spec parser extracts flow/flush rates from cut sheets
│   └── AI reads manufacturer PDFs → extracts gpf/gpm values by model
└── Output: Normalized fixture database (type, model, quantity, rate)

STEP 2: OCCUPANCY PROFILE GENERATION
├── Input: Building type, FTE count, transient count, gender ratio
├── AI Action: Apply LEED-default usage patterns per fixture type
│   ├── Toilets: 1 flush/occupant/day (FTE), 0.5 flush/visitor
│   ├── Urinals: 2 uses/male/day (based on gender ratio)
│   ├── Lavatory faucets: 3 min/use, X uses/day
│   ├── Kitchen faucets: apply per building type
│   └── Showerheads: 1 shower/occupant/day (residential/dorm only)
├── AI Action: Calculate total annual uses per fixture type
└── Output: Annual usage matrix (fixture x annual gallons)

STEP 3: BASELINE CALCULATION (Table 2)
├── AI Action: Apply LEED Table 2 baseline rates per fixture type
│   ├── Toilet baseline: 1.6 gpf
│   ├── Urinal baseline: 1.0 gpf
│   ├── Public lavatory: 0.50 gpm @ 60 psi
│   ├── Private lavatory: 2.2 gpm @ 60 psi
│   ├── Kitchen faucet: 2.2 gpm @ 60 psi
│   └── Showerhead: 2.5 gpm @ 80 psi
├── AI Action: Multiply baseline rate x annual uses = baseline consumption
└── Output: Total annual baseline water consumption (gallons/year)

STEP 4: PROPOSED CALCULATION
├── AI Action: Apply actual fixture flow/flush rates from Step 1
├── AI Action: Multiply proposed rate x annual uses = proposed consumption
├── AI Action: Calculate pressure adjustment if local supply differs from baseline
└── Output: Total annual proposed water consumption (gallons/year)

STEP 5: REDUCTION CALCULATION & COMPLIANCE CHECK
├── Formula: % Reduction = (Baseline - Proposed) / Baseline × 100%
├── AI Action: Compare result against thresholds
│   ├── WEp2 Option 2: ≥ 20% reduction → PASS/FAIL
│   ├── WEc2 Option 2: ≥ 30%/35%/40% → 1/2/3 points
│   └── Flag: Which fixtures contribute most to savings/shortfall
└── Output: Compliance report with reduction %, pass/fail status, improvement recommendations

STEP 6: EQUIPMENT EFFICIENCY COMPLIANCE CHECK
├── AI Action: Parse equipment schedule against WEp2 Tables 3-4
├── Check: ENERGY STAR labels on appliances (washer, dishwasher, ice machine)
├── Check: Prerinse spray valves ≤ 1.3 gpm
├── Check: Commercial kitchen equipment against flow rate thresholds
├── Check: Cooling tower specs (makeup meters, conductivity controllers, drift eliminators)
├── Check: No once-through cooling confirmation
└── Output: Equipment compliance matrix (PASS/FAIL per item)

STEP 7: IRRIGATION COMPLIANCE
├── Input: Landscape plan data, climate zone, plant palette, irrigation system
├── Path A (No Irrigation): AI generates narrative justifying no permanent irrigation
├── Path B (Efficient Irrigation):
│   ├── AI Action: Calculate TIR baseline per EPA methodology
│   │   └── ET₀ × Plant Factor × Area / Irrigation Efficiency
│   ├── AI Action: Calculate proposed irrigation with plant selection + system efficiency
│   └── Check: ≥ 30% reduction from TIR → PASS/FAIL
└── Output: Irrigation compliance documentation (narrative or calculation)

STEP 8: DOCUMENTATION GENERATION
├── AI Action: Populate LEED WEp2 credit form with all calculated values
├── AI Action: Generate fixture compliance table (spec vs. max allowed)
├── AI Action: Compile equipment cut sheet index with compliance flags
├── AI Action: Generate narrative for selected irrigation pathway
└── Output: Complete WEp2 submission package (calculation + specs + narrative)

STEP 9: WEc2 FEED-FORWARD (Cross-Credit)
├── AI Action: Forward WEp2 calculation as baseline for WEc2
├── AI Action: Identify gap to next WEc2 threshold (30%/35%/40%)
├── AI Action: Recommend strategies to achieve additional points
│   ├── More efficient fixtures (identify upgrade candidates)
│   ├── Alternative water sources (rainwater, greywater)
│   └── Cooling tower optimization
└── Output: WEc2 strategy report with points opportunity analysis
```

#### Data Model — Fixture Calculation Database

```json
{
  "project_id": "string",
  "building_type": "office|healthcare|residential|school|retail|hotel",
  "occupancy": {
    "fte_count": number,
    "transient_count": number,
    "gender_ratio_male": number,
    "operating_days_per_year": number,
    "hours_per_day": number
  },
  "fixtures": [
    {
      "fixture_type": "toilet|urinal|public_lavatory|private_lavatory|kitchen_faucet|showerhead",
      "manufacturer": "string",
      "model": "string",
      "quantity": number,
      "flow_rate_gpf": number,
      "flow_rate_gpm": number,
      "dual_flush": boolean,
      "full_flush_gpf": number,
      "half_flush_gpf": number,
      "watersense_labeled": boolean,
      "annual_uses": number,
      "baseline_gallons": number,
      "proposed_gallons": number
    }
  ],
  "baseline_total_gpy": number,
  "proposed_total_gpy": number,
  "reduction_percentage": number,
  "wep2_compliant": boolean,
  "wec2_points_available": number,
  "improvement_recommendations": ["string"]
}
```

#### Final Recommendation: **Automate in MVP — TOP PRIORITY**

---

### WEc1: Water Metering and Leak Detection

**Overview:** 1-point credit requiring submeters on major subsystems (Option 1) OR leak detection sensors on 50% of flush fixtures + action plan (Option 2).

#### Scoring
- **Automation Score:** 4/5
- **Commercial Value:** 4/5 (simple 1 point; applicable to most projects)
- **Risk Level:** Low

#### Documentation Type
- Plan (leak detection action plan)
- Specification (submeter/sensor specs)
- Layout drawing (submeter/sensor locations)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **Plumbing drawings** | Fixture counts, piping layouts, subsystem boundaries |
| **Submeter/sensor specs** | Manufacturer, model, recording capability, communication protocol |
| **Building type** | Determines additional requirements (healthcare, residential, C+S) |
| **AI-Generated** | Action plan narrative, subsystem coverage verification, spec compliance table |

#### AI Techniques Applicable
1. **Drawing Analysis:** Parse plumbing drawings to count fixtures and identify subsystem boundaries
2. **Coverage Calculator:** Verify 80% fixture coverage (Option 1) or 50% flush fixture coverage (Option 2)
3. **LLM Narrative Generation:** Generate leak detection action plan for Option 2
4. **Template Filling:** Populate submeter compliance table per subsystem

#### Automation Blueprint

```
STEP 1: PROJECT TYPE CLASSIFICATION
├── Input: Building type (office, healthcare, residential, C+S, etc.)
├── AI Action: Determine applicable subsystem requirements
│   ├── Base: Indoor fixtures (≥80%), irrigation, makeup water, commercial kitchen, laundry
│   ├── Healthcare: + 5 additional subsystem choices
│   ├── Residential: + individual dwelling unit meters
│   └── C+S: + tenant meter infrastructure (min. 1 per floor)
└── Output: Project-specific subsystem checklist

STEP 2: FIXTURE COVERAGE CALCULATION
├── Input: Fixture count from plumbing schedule
├── AI Action: Calculate coverage percentage per subsystem
│   ├── Option 1: % of indoor fixtures covered by submeters
│   └── Option 2: % of flush fixtures covered by leak sensors
├── AI Action: Flag gaps if coverage below threshold
└── Output: Coverage report with PASS/FAIL per subsystem

STEP 3: SPECIFICATION COMPLIANCE (Option 1 - Submeters)
├── Input: Submeter cut sheets/specs
├── AI Action: Verify hourly data recording capability
├── AI Action: Verify real-time data access (network/BMS/cloud/app)
└── Output: Submeter compliance table

STEP 4: LEAK DETECTION ACTION PLAN (Option 2 - LLM Generation)
├── Template: Standard leak detection action plan
├── AI Action: Generate customized action plan including:
│   ├── Data access method (describe BMS/cloud integration)
│   ├── Leak identification procedure (abnormal flow rate detection)
│   ├── Alarm notification protocol
│   └── Remediation procedures (contact, response time, repair)
└── Output: Complete leak detection action plan (2-3 pages)

STEP 5: PACKAGE ASSEMBLY
├── AI Action: Compile plumbing drawing excerpts with meter/sensor callouts
├── AI Action: Generate subsystem verification table
└── Output: Complete WEc1 submission package
```

#### Final Recommendation: **Automate in MVP**

---

### WEc2: Enhanced Water Efficiency

**Overview:** The highest-point-value credit in WE category — up to 8 points (NC) / 7 points (C+S) through 6 options: whole-project reduction, fixture reduction, appliance/process, outdoor, process optimization, and water reuse.

#### Scoring
- **Automation Score:** 5/5
- **Commercial Value:** 5/5 (up to 8 points; calculation-driven; multiple pathways)
- **Risk Level:** Low-Medium (multiple options increase complexity; cooling tower water analysis requires lab testing for Option 5)

#### Documentation Type
- **Calculation** (water reduction %, cooling tower cycles, TIR)
- **Specification** (equipment compliance tables)
- **Narrative** (alternative water source description)
- **Test Report** (potable water analysis for cooling tower cycles)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **WEp2 calculation output** | Baseline and proposed water consumption (auto-fed) |
| **Equipment schedule** | Appliances, kitchen equipment, lab equipment, steam systems |
| **Cooling tower data** | Makeup water analysis (Ca, alkalinity, SiO₂, Cl⁻, conductivity) |
| **Alternative water sources** | Rainwater, greywater, reclaimed water availability |
| **AI-Calculated** | Point-scoring optimization across all 6 options; whole-project reduction %; cooling tower max cycles |

#### AI Techniques Applicable
1. **Multi-Option Optimization Engine:** Calculate achievable points across all 6 options simultaneously and recommend optimal combination
2. **Spreadsheet Extraction:** Pull fixture/equipment data from schedules
3. **Calculation Engine:** All reduction calculations, cooling tower cycle calculations, TIR calculations
4. **Cross-Credit Integration:** Inherit WEp2 baseline; feed results to overall LEED score optimization
5. **Document Parsing:** Extract ENERGY STAR certifications from equipment specs

#### Automation Blueprint — MULTI-OPTION SCORING ENGINE

```
STEP 0: INHERIT WEp2 DATA
├── Auto-import: WEp2 baseline and proposed calculations
├── Auto-import: Fixture schedule with flow/flush rates
└── AI Action: Establish WEp2 baseline as starting point for WEc2

OPTION 1: WHOLE-PROJECT WATER USE (1-8 points)
├── AI Action: Build comprehensive water model including ALL end uses
│   ├── Indoor fixtures/fittings (from WEp2)
│   ├── Appliances and equipment (from equipment schedule)
│   ├── Process water (cooling towers, boilers)
│   ├── Irrigation (from TIR calculation)
│   └── Alternative water contributions
├── AI Action: Calculate total baseline consumption
├── AI Action: Calculate total proposed consumption with all strategies
├── Formula: % Reduction = (Baseline - Proposed) / Baseline × 100%
├── AI Action: Map reduction % to points (30%=1pt → 65%=8pts NC)
└── Output: Option 1 points analysis with strategy breakdown

OPTION 2: FIXTURE & FITTINGS REDUCTION (1-3 points)
├── Input: More efficient fixtures or alternative water for flushing
├── AI Action: Calculate additional reduction beyond WEp2 20%
├── AI Action: Map to points: 30%=1pt, 35%=2pts, 40%=3pts
├── AI Action: Identify cheapest upgrade path per fixture type
│   └── Marginal analysis: cost of fixture upgrade vs. water savings
└── Output: Option 2 points + upgrade recommendations

OPTION 3: APPLIANCE & PROCESS WATER (1-2 points)
├── AI Action: Parse equipment schedule against Tables 3-6 (NC) / 13-16 (C+S)
├── Check Table 3: Commercial washing machines ≤ 1.8 gal/lb
├── Check Table 4: Kitchen equipment ENERGY STAR or flow rate compliance
├── Check Table 5: Lab equipment (RO recovery ≥75%, sterilizer limits, etc.)
├── Check Table 6: Municipal steam condensate recovery
├── AI Action: Count compliant tables → 1 point per table (max 2)
└── Output: Option 3 compliance matrix

OPTION 4: OUTDOOR WATER USE (1-2 points NC / 1-3 points C+S)
├── Path A (No Irrigation): AI generates narrative → 2 pts NC / 3 pts C+S
├── Path B (Efficient Irrigation):
│   ├── AI Action: Calculate TIR baseline per EPA methodology
│   ├── AI Action: Calculate proposed with efficient plants + irrigation
│   ├── Check: 50% reduction = 1pt, 100% = 2pts (NC); 50%=1, 75%=2, 100%=3 (C+S)
│   └── Output: TIR calculation + points

OPTION 5: OPTIMIZE PROCESS WATER (1-2 points NC / 1-3 points C+S)
├── Path A: Cooling Tower Cycles
│   ├── Input: Potable water analysis (Ca=___, alkalinity=___, SiO₂=___, Cl⁻=___, conductivity=___)
│   ├── AI Action: Calculate max cycles per parameter:
│   │   Cycles_max = Limit_i / Actual_i for each parameter
│   │   System_max = MIN(all Cycles_max_i)
│   ├── AI Action: Evaluate points:
│   │   ├── Achieve max cycles = 1 point
│   │   ├── Max cycles + 25% increase OR 20% alt water = 2 points
│   │   └── (C+S only) Max cycles + 30% increase OR 30% alt water = 3 points
│   └── Output: Cycle calculation + points + treatment recommendations
│
├── Path B: Optimize Water Use for Cooling
│   ├── Input: Cooling system specifications
│   ├── AI Action: Establish baseline (water-cooled chiller, 0.002% drift, 3 cycles)
│   ├── AI Action: Calculate annual proposed water use
│   ├── Check: 25% reduction = 1pt, 50% = 2pts (NC); + 100% = 3pts (C+S)
│   └── Output: Cooling water optimization report
│
└── Path C: Alternative Process Water
    ├── AI Action: Calculate process water demand (excluding cooling)
    ├── AI Action: Calculate alternative water contribution
    ├── Check: Eligibility (process water ≥ 10% of total regulated use)
    └── Check: 20%=1pt, 30%=2pts (NC); 20%=1, 30%=2, 40%=3 (C+S)

OPTION 6: WATER REUSE (1-2 points)
├── Path A (Reuse-Ready): AI generates narrative describing reuse-ready plumbing
├── Path B (Alternative Sources): 
│   ├── Input: On-site reuse system specs OR municipal reclaimed water agreement
│   ├── AI Action: Document eligible end uses (irrigation, flush fixtures, makeup water)
│   └── Output: Reuse system documentation

STEP 7: OPTIMIZATION ENGINE — BEST COMBINATION
├── AI Action: Evaluate ALL option combinations for maximum points
├── Constraint: Option 1 OR combination of Options 2-6 (not both)
├── AI Action: Calculate points per cost/complexity ratio
├── AI Action: Recommend optimal strategy:
│   Example: "Pursue Options 2(3pts) + 4(2pts) + 5(2pts) = 7 points"
└── Output: Optimization report with recommended pathway

STEP 8: DOCUMENTATION GENERATION
├── AI Action: Generate comprehensive credit form with all selected options
├── AI Action: Compile all calculation worksheets
├── AI Action: Index equipment cut sheets with compliance flags
├── AI Action: Generate alternative water source narratives
└── Output: Complete WEc2 submission package
```

#### Data Model — Multi-Option Point Optimizer

```json
{
  "project_type": "NC|CS",
  "wec2_analysis": {
    "option_1_whole_project": {
      "baseline_gpy": number,
      "proposed_gpy": number,
      "reduction_pct": number,
      "points": "0-8",
      "applicable": boolean
    },
    "option_2_fixture_reduction": {
      "additional_reduction_pct": number,
      "points": "0-3",
      "upgrade_recommendations": ["string"]
    },
    "option_3_appliance": {
      "compliant_tables": ["table_3|table_4|table_5|table_6"],
      "points": "0-2"
    },
    "option_4_outdoor": {
      "tir_reduction_pct": number,
      "points": "0-2",
      "path": "no_irrigation|efficient_irrigation"
    },
    "option_5_process": {
      "cooling_tower_cycles": {
        "max_calculated_cycles": number,
        "actual_cycles": number,
        "points": "0-2"
      },
      "alternative_process_water_pct": number,
      "points": "0-2"
    },
    "option_6_reuse": {
      "path": "reuse_ready|alternative_sources",
      "points": "0-2"
    },
    "optimization_result": {
      "recommended_strategy": "option_1|options_2_6",
      "selected_options": ["string"],
      "total_points": number,
      "platinum_eligible": boolean
    }
  }
}
```

#### Final Recommendation: **Automate in MVP — TOP PRIORITY**

---

## Part 2: Detailed Credit Analysis — Indoor Environmental Quality (EQ)

---

### EQp1: Construction Management

**Overview:** Prerequisite requiring a construction management plan covering 7 areas: no smoking, extreme heat protection, HVAC protection, source control, pathway interruption, housekeeping, and scheduling.

#### Scoring
- **Automation Score:** 4/5
- **Commercial Value:** 5/5 (100% of projects; narrative-heavy; time-consuming to draft manually)
- **Risk Level:** Low

#### Documentation Type
- **Plan** (construction management plan — narrative)
- **Checklist** (implementation tracking)
- **Photo log** (signage, walk-off mats, barriers — requires field verification)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **Project data** | Project type, size, construction phase, contractor info |
| **Material list** | Absorptive materials on site (carpet, ceiling panels, insulation, furnishings) |
| **Site layout** | Building footprint, designated smoking area location |
| **HVAC schedule** | Filtration specifications, MERV rating, equipment protection plan |
| **AI-Generated** | Complete construction management plan, implementation checklist, smoking area distance verification |

#### AI Techniques Applicable
1. **LLM Narrative Generation:** Draft comprehensive construction management plan (8-12 pages) covering all 7 required areas
2. **Template Filling:** Populate project-specific details into standard plan template
3. **Checklist Auto-Generation:** Create implementation tracking checklist from plan requirements
4. **Distance Calculation:** Verify smoking area is ≥ 25 feet from building

#### Automation Blueprint

```
STEP 1: PROJECT CONTEXT INTAKE
├── Input: Project type, location, construction duration, contractor name
├── Input: Building footprint dimensions
├── Input: HVAC system type, filtration schedule
├── Input: List of absorptive materials to be stored on-site
└── AI Action: Store in project context database

STEP 2: CONSTRUCTION MANAGEMENT PLAN GENERATION (LLM)
├── Template: 7-section plan structure
├── Section 1 — No Smoking (AI-generated)
│   ├── Policy statement prohibiting smoking during construction
│   ├── Designated smoking area location (>25 ft from building)
│   ├── Signage plan (prohibition signs at entries, smoking area)
│   └── Enforcement procedures
├── Section 2 — Extreme Heat Protection (AI-generated)
│   ├── Heat stress prevention measures
│   ├── Worker rest/shade provisions
│   ├── Hydration protocols
│   └── Modified work schedules for high-heat days
├── Section 3 — HVAC Protection (AI-generated)
│   ├── Protection of ductwork during construction
│   ├── MERV filter installation sequence
│   ├── Equipment operation restrictions
│   └── Filtration media replacement schedule (post-construction, pre-occupancy)
├── Section 4 — Source Control (AI-generated)
│   ├── Material storage plan (moisture-protected area)
│   ├── VOC-emitting material handling procedures
│   ├── Inventory of absorptive materials and storage locations
│   └── Moisture damage prevention measures
├── Section 5 — Pathway Interruption (AI-generated)
│   ├── Isolation procedures for dusty/VOC-emitting activities
│   ├── Temporary barrier specifications
│   ├── Walk-off mat placement plan at entries
│   └── Dust collection on power tools
├── Section 6 — Housekeeping (AI-generated)
│   ├── Regular cleaning schedule
│   ├── HEPA vacuum specifications
│   ├── Dust control during sweeping
│   └── Waste management procedures
└── Section 7 — Scheduling (AI-generated)
    ├── Construction activity sequencing for IAQ protection
    ├── Wet work (concrete, paint) drying periods
    ├── Material installation sequencing (low-VOC first)
    └── Occupied area coordination (for renovation projects)

STEP 3: SMOKING AREA DISTANCE VERIFICATION
├── Input: Site plan coordinates (building, proposed smoking area)
├── AI Action: Calculate distance between building and smoking area
├── Check: ≥ 25 feet (7.5 meters) → PASS/FAIL
└── Output: Distance verification with graphic annotation

STEP 4: IMPLEMENTATION CHECKLIST GENERATION
├── AI Action: Generate detailed checklist from all 7 plan sections
├── Items: 50-100 implementation items with responsible party and due dates
├── Format: Sortable by phase, responsible party, priority
└── Output: Interactive implementation checklist

STEP 5: DOCUMENTATION TRACKING TEMPLATES
├── AI Action: Generate photo log templates for:
│   ├── No-smoking signage installation
│   ├── Walk-off mat placement
│   ├── Temporary barriers
│   ├── Material storage areas
│   └── HEPA vacuum use
├── AI Action: Generate filtration media replacement log
└── Output: Field documentation templates

STEP 6: PACKAGE ASSEMBLY
├── AI Action: Compile plan + checklist + templates into submission package
├── AI Action: Cross-reference with EQp2 for filtration consistency
└── Output: Complete EQp1 documentation package

HUMAN REVIEW POINTS: Contractor sign-off on plan; field verification 
photos; actual smoking area location confirmation; final implementation 
checklist sign-off by construction manager.
```

#### Final Recommendation: **Automate in MVP**

---

### EQp2: Fundamental Air Quality

**Overview:** Prerequisite with three requirements: (1) outdoor air quality investigation, (2) ventilation and filtration design per ASHRAE 62.1, (3) entryway system design. Heavily calculation-driven for ventilation rates.

#### Scoring
- **Automation Score:** 4/5
- **Commercial Value:** 4/5 (100% of projects; engineering-calculations; multiple standards)
- **Risk Level:** Medium (multiple ASHRAE standards; engineering judgment required)

#### Documentation Type
- **Calculation** (ventilation rates per ASHRAE 62.1 VRP/IAQP)
- **Specification** (filtration specs, OA measurement devices, entryway systems)
- **Narrative** (outdoor air quality investigation report)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **HVAC design** | Zone schedules, OA intake rates, system types, CFM values |
| **Space data** | Room types, areas, occupant densities, ceiling heights |
| **Filtration specs** | MERV rating, filter model, ASHRAE 52.2 compliance |
| **Local air quality** | Project location for outdoor air quality assessment |
| **AI-Calculated** | VRP rates per ASHRAE 62.1, filtration compliance verification, OA investigation report |

#### AI Techniques Applicable
1. **ASHRAE 62.1 Calculation Engine:** Automate ventilation rate procedure calculations
2. **Specification Verification:** Check filtration specs against MERV 13 / ePM1 50% requirements
3. **LLM Narrative Generation:** Draft outdoor air quality investigation report
4. **Template Filling:** Populate ASHRAE compliance tables
5. **Spatial Analysis:** Check OA measurement device placement (>1,000 cfm systems)

#### Automation Blueprint

```
STEP 1: PROJECT DATA INTAKE
├── Input: Building type, location (city/state), climate zone
├── Input: HVAC zone schedule (room name, type, area, occupants, CFM)
├── Input: Filtration specifications (MERV rating, standard)
└── AI Action: Normalize into calculation database

STEP 2: OUTDOOR AIR QUALITY INVESTIGATION (LLM)
├── AI Action: Generate location-specific air quality investigation
│   ├── Query EPA AirNow database for project location air quality
│   ├── Identify attainment vs. nonattainment status
│   ├── Document local pollutant sources
│   └── Reference ASHRAE 62.1-2022 Sections 4.1-4.3
├── AI Action: Draft investigation report (2-3 pages)
└── Output: Outdoor air quality investigation narrative

STEP 3: VENTILATION RATE CALCULATION (ASHRAE 62.1 VRP)
├── Input: Space schedule with room types and occupant counts
├── AI Action: Look up Rp (CFM/person) and Ra (CFM/ft²) per ASHRAE 62.1 Table 6-1
├── AI Action: Calculate breathing zone OA rate:
│   Vbz = Rp × Pz + Ra × Az
├── AI Action: Apply zone air distribution effectiveness (Ez) from Table 6-2
│   Voz = Vbz / Ez
├── AI Action: Sum to system-level OA intake rate
└── Output: Complete VRP calculation spreadsheet

STEP 4: FILTRATION COMPLIANCE VERIFICATION
├── Input: Filter specifications (MERV rating, ISO 16890 class, or in-room system)
├── AI Action: Verify compliance with EQp2 requirements
│   ├── MERV 13 per ASHRAE 52.2-2017 → PASS
│   ├── OR ePM1 50% per ISO 16890-2016 → PASS
│   ├── OR in-room system per ASHRAE 241-2023 → verify test documentation
│   └── Else → FAIL with recommendation
└── Output: Filtration compliance report per HVAC system

STEP 5: OUTDOOR AIRFLOW MEASUREMENT DEVICE CHECK
├── Input: System CFM schedule
├── AI Action: Flag systems with OA intake > 1,000 cfm
├── AI Action: Verify measurement device specs for flagged systems
└── Output: OA measurement device compliance list

STEP 6: ENTRYWAY SYSTEM DOCUMENTATION
├── AI Action: Generate entryway system specification requirements
├── Check: Permanent entryway systems at all primary exterior entrances
└── Output: Entryway system specification compliance note

STEP 7: HEALTHCARE/RESIDENTIAL OVERRIDES (if applicable)
├── Healthcare: Add ASHRAE 170-2021 Sections 6-10 requirements
├── Residential: Add ASHRAE 62.2-2022 calculations
│   ├── Dwelling unit ventilation rates
│   ├── Kitchen/bathroom exhaust sizing
│   ├── Makeup air for >400 cfm exhaust
│   └── ENERGY STAR exhaust fan verification
└── Output: Project-type-specific addendum

STEP 8: DOCUMENTATION PACKAGE
├── AI Action: Compile VRP calculation spreadsheet
├── AI Action: Generate filtration compliance table
├── AI Action: Draft outdoor air quality investigation narrative
├── AI Action: Generate entryway system spec sheet
└── Output: Complete EQp2 submission package
```

#### Final Recommendation: **Automate in MVP**

---

### EQp3: No Smoking or Vehicle Idling

**Overview:** Prerequisite prohibiting smoking and vehicle idling on-site, with residential compartmentalization requirements.

#### Scoring
- **Automation Score:** 3/5
- **Commercial Value:** 3/5 (100% of projects but relatively simple documentation)
- **Risk Level:** Low

#### Documentation Type
- **Plan** (no-smoking / no-idling policy)
- **Site plan** (designated smoking area locations)
- **Test report** (blower door test — for residential non-smoking projects)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **Site plan** | Building footprint, property lines, entries, outdoor air intakes |
| **Building type** | Standard or residential or school |
| **Blower door results** (residential) | Leakage rates per unit |
| **AI-Generated** | Policy document, site plan annotations, distance verification, blower door analysis |

#### AI Techniques Applicable
1. **Site Plan Analysis:** Identify minimum 25-ft setback zones from entries, intakes, operable windows
2. **Distance Calculation:** Verify smoking area placement
3. **LLM Narrative Generation:** Draft no-smoking / no-idling policy
4. **Blower Door Analysis:** (For residential) Process test results against Table 1 thresholds

#### Automation Blueprint

```
STEP 1: POLICY DOCUMENT GENERATION (LLM)
├── Input: Building type, owner name, project address
├── AI Action: Generate no-smoking and no-idling policy document
│   ├── Indoor prohibition
│   ├── Outdoor prohibition except designated areas
│   ├── Vehicle idling prohibition
│   ├── Communication and enforcement provisions
│   └── School-specific total prohibition (if applicable)
└── Output: Policy document (1-2 pages)

STEP 2: SITE PLAN SMOKING AREA ANALYSIS
├── Input: Site plan with building, entries, OA intakes, operable windows
├── AI Action: Identify 25-foot exclusion zones around all entries/intakes/windows
├── AI Action: Propose compliant designated smoking area location(s)
├── AI Action: Calculate distances from building to proposed smoking area
└── Output: Annotated site plan with smoking area recommendations

STEP 3: RESIDENTIAL COMPARTMENTALIZATION (if applicable)
├── Input: Blower door test results (CFM50, CFM75, enclosure area)
├── Input: Conditioned floor area per unit
├── AI Action: Calculate leakage per enclosure area
├── AI Action: Compare against Table 1 thresholds
│   ├── ≥ 5,000 sq ft: 0.13 cfm/sq ft @ 50 Pa (new) / 0.20 (renovation)
│   ├── < 5,000 sq ft: 1.0 ACH @ 50 Pa (new) / 1.5 (renovation)
├── AI Action: Calculate weighted average leakage
└── Output: Compartmentalization compliance report
```

#### Final Recommendation: **Automate Later** (lower priority — simple enough; residential blower door integration adds moderate value)

---

### EQc1: Enhanced Air Quality

**Overview:** 1-point credit for exceeding ASHRAE 62.1 — either increased ventilation (Option 1) or enhanced IAQ design with lower contaminant limits (Option 2).

#### Scoring
- **Automation Score:** 3/5
- **Commercial Value:** 3/5 (1 point only; requires building on EQp2 calculations)
- **Risk Level:** Medium (engineering judgment for IAQ modeling in Option 2)

#### Documentation Type
- **Calculation** (ventilation increase % or IAQ modeling results)
- **Narrative** (IAQ design documentation)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **EQp2 ventilation calculations** | Baseline VRP rates (auto-imported) |
| **Increased OA rates** | Target ventilation increase (15% or 30% EP) |
| **IAQ model results** (Option 2) | PM2.5, formaldehyde, ozone concentration predictions |
| **AI-Calculated** | Increased ventilation rates, % coverage of regularly occupied spaces |

#### AI Techniques Applicable
1. **Calculation Engine:** Increase VRP rates by 15% or 30%; verify 95% space coverage
2. **Template Filling:** Populate enhanced IAQ design limits table
3. **Results Parsing:** Parse IAQ modeling output for PM2.5, formaldehyde, ozone compliance

#### Automation Blueprint

```
OPTION 1: INCREASED VENTILATION
├── Step 1: Import EQp2 VRP calculations
├── Step 2: Multiply all Voz values by 1.15 (or 1.30 for EP)
├── Step 3: Identify regularly occupied spaces
├── Step 4: Verify increased OA reaches 95% of regularly occupied floor area
├── Step 5: Generate documentation showing increase calculation
└── Output: Option 1 compliance report

OPTION 2: ENHANCED IAQ DESIGN
├── Step 1: Import IAQ modeling results (PM2.5, formaldehyde, ozone)
├── Step 2: Verify against enhanced design limits:
│   ├── PM2.5 ≤ 10 µg/m³
│   ├── Formaldehyde ≤ 20 µg/m³
│   └── Ozone ≤ 10 ppb
├── Step 3: Generate IAQ design narrative
└── Output: Option 2 compliance report
```

#### Final Recommendation: **Automate Later** (builds on EQp2 automation; simple extension)

---

### EQc2: Occupant Experience

**Overview:** The most complex EQ credit — up to 7 points across 5 options: biophilic environment, adaptable environment, thermal environment, sound environment, and lighting environment (with daylight simulation). Combines calculations, surveys, narratives, and simulation.

#### Scoring
- **Automation Score:** 4/5
- **Commercial Value:** 4/5 (up to 7 points; highly visible to clients; occupant survey creates ongoing engagement)
- **Risk Level:** Medium (daylight simulation requires external software; acoustic modeling is specialized)

#### Documentation Type
- **Calculation** (view area %, daylight sDA/ASE, UGR, proximity %)
- **Narrative** (biophilic design, adaptable environment, thermal analysis)
- **Survey** (acoustic expectations mapping — can be AI-generated)
- **Simulation report** (daylight per IES LM-83-23)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **Floor plans** | Room types, areas, glazing locations, regularly occupied space boundaries |
| **Glazing specs** | VLT values, frit/pattern/tint information |
| **Luminaire schedule** | Manufacturer, model, photometric data, CRI, UGR values |
| **Building model** | For daylight simulation (Revit/Rhino/DXF export) |
| **AI-Calculated** | View area percentages, sDA/ASE, UGR compliance, proximity calculations |
| **AI-Generated** | Biophilic design narrative, occupant surveys, acoustic mapping templates |

#### AI Techniques Applicable
1. **Spatial Analysis:** Calculate view area %, daylight proximity % from floor plans
2. **Simulation Integration:** Interface with daylight simulation tools (Radiance, ClimateStudio, LightStanza)
3. **Survey Generation & Analysis:** Create and analyze occupant experience surveys
4. **LLM Narrative Generation:** Biophilic design narrative, adaptable environment description, thermal analysis
5. **Document Parsing:** Extract photometric data from luminaire cut sheets (CRI, UGR, luminance)
6. **Template Filling:** Acoustic expectations mapping table

#### Automation Blueprint

```
OPTION 1: BIOPHILIC ENVIRONMENT

Path 1: Integrated Biophilic Design (1 point)
├── AI Action (LLM): Generate biophilic design narrative addressing all 5 principles
│   ├── Principle 1: Repeated and sustained engagement with nature
│   ├── Principle 2: Human adaptations to natural world
│   ├── Principle 3: Emotional attachment to building/location
│   ├── Principle 4: Positive interactions between people and nature
│   └── Principle 5: Mutual reinforcing, interconnected solutions
├── Input: Project-specific biophilic design features
└── Output: Biophilic design narrative (3-5 pages)

Path 2: Quality Views (2-3 points)
├── Input: Floor plan with glazing locations and room areas
├── AI Action: Calculate regularly occupied floor area
├── AI Action: Identify glazing with VLT > 40%
├── AI Action: Calculate viewable area per room
├── AI Action: Determine qualifying view content (nature/urban/25+ ft distance)
├── AI Action: Apply 30% cap for interior atrium views
├── Calculation: % of regularly occupied floor area with compliant views
│   ├── ≥ 75% → 2 points
│   └── ≥ 90% → 3 points
└── Output: View area calculation with floor plan annotations

OPTION 2: ADAPTABLE ENVIRONMENT (NC only, 1 point)
├── AI Action (LLM): Generate adaptable environment narrative describing:
│   ├── Variable thermal/sound/lighting zones
│   ├── Accessible quiet space provision
│   └── At least one additional strategy (furniture variety, height adjustability, outdoor space)
├── Input: Project-specific adaptability features
└── Output: Adaptable environment narrative (2-3 pages)

OPTION 3: THERMAL ENVIRONMENT (NC only, 1 point)
├── AI Action: Generate ASHRAE 55-2023 compliance documentation
├── AI Action (LLM): Draft thermal condition analysis addressing:
│   ├── Seasonal thermal condition alignment
│   ├── Overcooling prevention strategies
│   ├── Solutions for newly arrived occupants
│   ├── Transition space comfort solutions
│   └── Task-specific thermal support
└── Output: Thermal environment narrative + ASHRAE 55 compliance summary

OPTION 4: SOUND ENVIRONMENT (1-2 points)

Path 1: Acoustic Expectations Mapping (1 point)
├── AI Action: Generate acoustic expectations mapping template
├── Categories for each space:
│   ├── Noise exposure zones (high/medium/low/no risk)
│   ├── Acoustic comfort (loud/quiet/mixed/circulation/sensitive)
│   ├── Acoustic privacy (high/confidential/normal/marginal/none)
│   ├── Communication zones (excellent/good/marginal/none)
│   └── Soundscape management (preserve/improve/restore/mitigate/specialize)
├── AI Action: Define acoustic criteria and design strategies per category
└── Output: Acoustic expectations mapping matrix (all primary spaces)

Path 2: Acoustic Criteria (2 points — requires specialized modeling)
├── Input: Acoustic modeling results or measurement data
├── AI Action: Verify 75% of occupied spaces + all classrooms meet criteria
├── Note: Acoustic modeling requires specialized software (ODEON, EASE)
└── Output: Acoustic criteria compliance report

OPTION 5: LIGHTING ENVIRONMENT (1-6 points)

Path 1: Solar Glare (1 point)
├── Input: Window schedule with orientation
├── AI Action: Identify regularly occupied spaces with direct sun penetration
├── AI Action: Verify glare control devices specified (manual or auto with override)
└── Output: Solar glare compliance table

Path 2: Quality Electric Lighting (1 point)
├── Input: Luminaire schedule with photometric data
├── AI Action: Verify ONE of:
│   ├── Luminance < 6,000 cd/m² between 45-90° from nadir
│   ├── UGR ≤ 19 (tabular method)
│   └── UGR ≤ 19 (software modeling)
├── AI Action: Verify color rendering:
│   ├── CRI ≥ 90; OR
│   ├── IES TM-30-20: Rf ≥ 78, Rg ≥ 95, Rcs,h1: -1% to 15%
└── Output: Electric lighting compliance report

Path 3: Proximity to Windows (1 point)
├── Input: Floor plan with glazing locations and regularly occupied areas
├── AI Action: Calculate area within 20 ft (6 m) of envelope glazing with VLT > 40%
├── Calculation: % of regularly occupied area within proximity threshold
│   └── ≥ 30% → 1 point
└── Output: Proximity calculation with floor plan annotations

Path 4: Daylight Simulation (1-4 points)
├── Input: Building 3D model (via BIM integration or upload)
├── Input: Climate data (auto-selected by location)
├── AI Action: Interface with daylight simulation engine (Radiance/ClimateStudio)
│   ├── Run sDA 300/50% calculation per IES LM-83-23
│   ├── Run ASE 1000,250 calculation
│   ├── Identify spaces with ASE > 20% → flag glare control needs
│   └── Calculate average sDA for total regularly occupied floor area
├── Scoring:
│   ├── sDA ≥ 40% → 1 point
│   ├── sDA ≥ 55% → 2 points
│   ├── sDA ≥ 65% → 3 points
│   └── sDA ≥ 75% → 4 points
└── Output: Daylight simulation report with sDA/ASE maps
```

#### Daylight Simulation Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EQc2 Daylight Module                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  BIM Import  │───▶│  Geometry    │───▶│  Radiance    │  │
│  │  (Revit/IFC) │    │  Processor   │    │  Model Gen   │  │
│  └──────────────┘    └──────────────┘    └──────┬───────┘  │
│                                                  │           │
│  ┌──────────────┐    ┌──────────────┐           │           │
│  │  Climate DB  │───▶│  Weather     │───────────┤           │
│  │  (TMY3/EPW)  │    │  File Sel.   │           │           │
│  └──────────────┘    └──────────────┘           ▼           │
│                                        ┌──────────────────┐  │
│                                        │  Simulation      │  │
│                                        │  Engine          │  │
│                                        │  (Radiance/Daysim│  │
│                                        │   or API call to │  │
│                                        │   ClimateStudio) │  │
│                                        └────────┬─────────┘  │
│                                                 │            │
│                                                 ▼            │
│                                        ┌──────────────────┐  │
│                                        │  Results Parser  │  │
│                                        │  • sDA 300/50%   │  │
│                                        │  • ASE 1000,250  │  │
│                                        │  • Space-by-space│  │
│                                        │  • Average sDA   │  │
│                                        └────────┬─────────┘  │
│                                                 │            │
│                                                 ▼            │
│                                        ┌──────────────────┐  │
│                                        │  LEED Report Gen │  │
│                                        │  • sDA maps      │  │
│                                        │  • ASE flags     │  │
│                                        │  • Points calc   │  │
│                                        │  • IES LM-83-23  │  │
│                                        │    format        │  │
│                                        └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### Occupant Survey Platform (for EQc2 + EQc3 Integration)

```
┌─────────────────────────────────────────────────────────────┐
│              AI Occupant Experience Survey Engine             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  SURVEY GENERATION (AI-powered)                               │
│  ├── Building-type-specific question templates                │
│  ├── Customizable per project goals                           │
│  └── Multilingual support                                     │
│                                                               │
│  SURVEY CATEGORIES:                                           │
│  ├── Thermal comfort (EQc2 Option 3 validation)               │
│  ├── Lighting quality (EQc2 Option 5 validation)              │
│  ├── Acoustic comfort (EQc2 Option 4 validation)              │
│  ├── Biophilic connection (EQc2 Option 1 validation)          │
│  ├── Spatial adaptability (EQc2 Option 2 validation)          │
│  ├── Accessibility satisfaction (EQc3 validation)             │
│  └── Overall well-being                                       │
│                                                               │
│  ANALYSIS MODULE:                                             │
│  ├── Sentiment analysis on open responses                     │
│  ├── Statistical analysis of Likert-scale responses           │
│  ├── Correlation with design features                         │
│  └── Gap analysis → improvement recommendations               │
│                                                               │
│  OUTPUT:                                                      │
│  ├── Survey results dashboard                                 │
│  ├── Automated narrative summary                              │
│  └── LEED credit documentation appendices                     │
└─────────────────────────────────────────────────────────────┘
```

#### Final Recommendation: **Automate in MVP** (daylight simulation integration is complex but high-value; survey platform is unique differentiator)

---

### EQc3: Accessibility and Inclusion

**Overview:** 1-point credit requiring local accessibility code compliance + 10 additional strategies from a menu of 21 options across 4 categories: physical diversity, safety/aging, social health, and navigation.

#### Scoring
- **Automation Score:** 4/5
- **Commercial Value:** 4/5 (1 point but 100% applicable; highly visible to clients; social impact)
- **Risk Level:** Low

#### Documentation Type
- **Checklist** (accessibility code compliance + strategy selection)
- **Narrative** (strategy descriptions)
- **Drawing** (strategy implementation on plans)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **Local accessibility codes** | Applicable code requirements (from IPp2) |
| **Floor plans** | Door widths, ramp locations, counter heights, restroom layouts |
| **Project type** | Determines which of 21 strategies are most relevant |
| **Demographic data** | Local language distribution (for >5% threshold) |
| **AI-Generated** | Strategy selection guide, compliance checklist, strategy narratives, code cross-reference |

#### AI Techniques Applicable
1. **Standards Cross-Check:** Compare design against local accessibility codes
2. **Checklist Generation:** Auto-generate 21-strategy evaluation checklist
3. **LLM Narrative Generation:** Draft strategy implementation descriptions
4. **Spatial Analysis:** Verify door widths, clearances, accessible routes from drawings
5. **Demographic Data Lookup:** Identify languages spoken by >5% of local population

#### Automation Blueprint

```
STEP 1: LOCAL ACCESSIBILITY CODE COMPLIANCE CHECK
├── Input: Applicable accessibility codes (from IPp2 output)
├── Input: Floor plan with door widths, ramp locations, accessible routes
├── AI Action: Cross-check design elements against code requirements
│   ├── Door clear width ≥ 32 inches
│   ├── Ramp slopes and landings
│   ├── Accessible route continuity
│   └── Counter/reception desk accessibility
├── AI Action: Flag non-compliant elements with recommendations
└── Output: Accessibility code compliance report

STEP 2: STRATEGY SELECTION GUIDE (AI-POWERED)
├── Input: Project type (office, healthcare, residential, school, retail)
├── Input: Project-specific features (fitness center, lactation needs, etc.)
├── AI Action: Rank 21 strategies by relevance and ease of implementation
│   ├── HIGH PRIORITY (easy wins):
│   │   #5 Nonslip flooring, #7 Visual indication at glazing, 
│   │   #10 Visual contrast, #17 Wayfinding signage, #18 Nontext diagrams
│   ├── MEDIUM PRIORITY (design-dependent):
│   │   #1 Wave-to-open operators, #4 Alternate accessible routes,
│   │   #9 Closed risers, #11 Visual/tactile warnings
│   └── SPECIALIZED (project-type-specific):
│       #12 Lactation rooms, #13 All-gender restrooms,
│       #14 Adult changing, #15 Multilingual signage
├── AI Action: Recommend optimal 10-strategy combination
└── Output: Strategy selection recommendation report

STEP 3: STRATEGY NARRATIVE GENERATION (LLM)
├── For each selected strategy, AI generates:
│   ├── Strategy description (what it is and why it matters)
│   ├── Implementation approach (how it's incorporated into design)
│   └── Compliance verification (how it exceeds code requirements)
├── Example for #5 Nonslip flooring:
│   "The project specifies flooring materials with a dynamic coefficient 
│    of friction ≥ 0.42 per ANSI A326.3 in all corridors, lobbies, 
│    restrooms, and other high-traffic areas. This exceeds minimum code 
│    requirements and supports safe navigation for occupants with mobility 
│    aids and those at risk of falls."
└── Output: Strategy narrative document (10 strategies, 1-2 paragraphs each)

STEP 4: QUANTITATIVE VERIFICATION
├── Strategy #2: Meeting spaces for 10% mobility device capacity
│   ├── Input: Meeting room schedule with capacities
│   ├── AI Action: Calculate 10% of capacity per room
│   └── Verify: Clear floor space for mobility device turnaround
├── Strategy #15: Languages spoken by >5% of local population
│   ├── AI Action: Query Census/demographic data for project location
│   ├── AI Action: Identify languages exceeding 5% threshold
│   └── Output: Language list with signage recommendations
└── Output: Quantitative compliance verification

STEP 5: DRAWING ANNOTATION GUIDE
├── AI Action: Generate drawing annotation instructions for each strategy
│   ├── Mark door operator locations on plans
│   ├── Highlight visual contrast locations
│   ├── Note wayfinding signage placements
│   └── Identify accessible route alternatives
└── Output: Drawing annotation guide for architect

STEP 6: PACKAGE ASSEMBLY
├── AI Action: Compile code compliance report + strategy narratives + 
│              quantitative verification + drawing annotations
└── Output: Complete EQc3 submission package
```

#### Final Recommendation: **Automate in MVP**

---

### EQc4: Resilient Spaces

**Overview:** 1-2 point credit for climate resilience features — episodic event management mode (NC only), infection risk management (NC only), thermal safety during power outages, and operable windows.

#### Scoring
- **Automation Score:** 3/5
- **Commercial Value:** 3/5 (up to 2 points; specialized; growing importance)
- **Risk Level:** Medium (thermal modeling requires specialized simulation; ASHRAE 241 compliance)

#### Documentation Type
- **Narrative** (management mode design documentation)
- **Calculation** (thermal modeling, operable window %)
- **Specification** (system capabilities for management modes)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **TMY weather data** | Peak summer/winter conditions for location |
| **Building envelope specs** | U-values, SHGC, thermal mass, infiltration rates |
| **Window schedule** | Operable window count, area, room locations, ASHRAE 62.1 Section 6.4 compliance |
| **HVAC specs** | System types, capacity, management mode capabilities |
| **AI-Calculated** | Operable window % of regularly occupied spaces; thermal modeling coordination |

#### AI Techniques Applicable
1. **Thermal Simulation Integration:** Interface with EnergyPlus/ThermalCalc for 48-hour power outage modeling
2. **Template Filling:** Management mode documentation per ASHRAE Guideline 44 / ASHRAE 241
3. **Spatial Analysis:** Calculate % of regularly occupied spaces with operable windows
4. **LLM Narrative Generation:** Management mode design narratives

#### Automation Blueprint

```
OPTION 1: EPISODIC OUTDOOR EVENT MANAGEMENT (NC only, 1 point)
├── AI Action: Generate ASHRAE Guideline 44 management mode documentation
├── Content:
│   ├── Trigger conditions (wildfire smoke AQI thresholds, etc.)
│   ├── System response (reduce OA, increase filtration, pressurization)
│   ├── Control sequences
│   └── Commissioning verification requirements
├── Input: Local environmental risks (wildfire, ozone, industrial)
└── Output: Management mode design documentation

OPTION 2: INFECTION RISK MANAGEMENT MODE (NC only, 1 point)
├── AI Action: Generate ASHRAE 241-2023 Section 5.1 compliance documentation
├── Content:
│   ├── Equivalent clean airflow rates per space type
│   ├── System operating modes (normal vs. risk management)
│   ├── Control sequences
│   └── B10.2 design documentation
├── Input: Space schedule with ASHRAE 241-2023 airflow requirements
└── Output: Infection risk management mode documentation

OPTION 3: THERMAL SAFETY DURING POWER OUTAGES (1-2 points)

Path 1: Extreme Heat (1 point)
├── Input: Building envelope specs, internal gains, TMY weather data
├── AI Action: Coordinate thermal modeling (48-hour power outage, peak summer)
│   ├── Target: Maintain habitable conditions (ASHRAE 55 adaptive comfort)
│   ├── Identify thermal safety zones
│   └── Note: Requires external simulation tool (EnergyPlus/ClimateStudio)
└── Output: Thermal modeling report coordination + safety zone identification

Path 2: Extreme Cold (1 point)
├── Input: Building envelope specs, Passive House certification (alternative)
├── AI Action: Coordinate thermal modeling (48-hour power outage, peak winter)
│   ├── Target: Maintain habitable conditions
│   └── Alternative: Passive House certification documentation
└── Output: Thermal modeling report + safety zone identification

OPTION 4: OPERABLE WINDOWS (1-2 points)
├── Input: Window schedule with operability flag
├── Input: Floor plan with regularly occupied areas
├── AI Action: Calculate total regularly occupied floor area
├── AI Action: Calculate area of regularly occupied spaces with operable windows
│   ├── Verify: Compliant with ASHRAE 62.1-2022 Section 6.4
├── Formula: % = Area with operable windows / Total regularly occupied area
│   ├── ≥ 50% → 1 point
│   └── ≥ 75% → 2 points
└── Output: Operable window compliance calculation
```

#### Final Recommendation: **Automate Later** (thermal modeling requires external simulation integration; operable window calc is simple but credit is specialized)

---

### EQc5: Air Quality Testing and Monitoring

**Overview:** 1-2 point credit (NC only) for preoccupancy air testing (PM/inorganic gases + VOCs) OR continuous IAQ monitoring. Requires physical laboratory testing.

#### Scoring
- **Automation Score:** 2/5
- **Commercial Value:** 3/5 (1-2 points but requires physical testing; NC only)
- **Risk Level:** High (laboratory accreditation requirements; physical sample collection; strict test protocols)

#### Documentation Type
- **Test report** (laboratory test results for CO, PM, ozone, VOCs)
- **Test plan** (preoccupancy testing protocol)
- **Specification** (monitor specs for Option 2)

#### Required Inputs
| Source | Data Elements |
|--------|--------------|
| **Laboratory test reports** | CO, PM2.5, PM10, ozone, VOC concentration results |
| **Test plan** | Number of measurements, locations, timing |
| **Monitor specs** (Option 2) | CO₂, PM2.5, TVOC, temperature, RH sensor specifications |
| **AI-Generated** | Test plan, measurement location recommendations, spec verification |
| **Human-Required** | Physical sample collection, laboratory analysis, field measurements |

#### AI Techniques Applicable
1. **Test Plan Generation:** Calculate number of measurements per floor area (Table 1); recommend representative locations
2. **Document Parsing:** Parse laboratory test reports; extract concentration values; compare against limits
3. **Specification Verification:** Verify monitor specs meet "building grade or better" requirement
4. **TVOC Calculation:** Compute TVOC per EN 16516:2017 or CDPH method

#### Limitations — Why This Cannot Score Higher

| Limitation | Impact on Automation |
|-----------|---------------------|
| Physical sample collection required | AI cannot collect air samples |
| ISO/IEC 17025 accredited laboratory required | AI cannot perform laboratory analysis |
| Specific test methods mandated (ISO 4224, ISO 16000-6, etc.) | Requires certified laboratory equipment |
| Direct reading instruments with minimum accuracy specs | Requires calibrated physical instruments |
| 4-hour minimum measurement period | Time-bound physical process |
| Field verification of monitor placement (3-6 ft above floor) | Requires on-site confirmation |

#### Automation Blueprint (What CAN Be Automated)

```
STEP 1: TEST PLAN GENERATION
├── Input: Total occupied floor area
├── AI Action: Calculate number of measurements per Table 1
│   ├── ≤ 5,000 sq ft → 1 measurement
│   ├── 5,000-15,000 → 2 measurements
│   ├── 15,000-25,000 → 3 measurements
│   ├── 25,000-200,000 → 4 + 1 per 25,000 above 25,000
│   └── > 200,000 → 10 + 1 per 50,000 above 200,000
├── AI Action: Recommend representative measurement locations
│   ├── High-occupancy areas
│   ├── Areas with potential contaminant sources
│   ├── Mix of space types
│   └── Avoid areas with unusual ventilation
└── Output: IAQ testing plan with measurement count and locations

STEP 2: LABORATORY RESULT PARSING (after testing)
├── Input: Laboratory test reports (PDF)
├── AI Action: Extract concentration values for each contaminant
│   ├── CO: ___ ppm
│   ├── PM2.5: ___ µg/m³
│   ├── PM10: ___ µg/m³
│   ├── Ozone: ___ ppm
│   ├── Formaldehyde: ___ µg/m³
│   └── [11 other VOCs]
├── AI Action: Compare against Table 2 and Table 3 limits
│   ├── CO ≤ 9 ppm (no more than 2 ppm above outdoor)
│   ├── PM2.5 ≤ 12 µg/m³ (attainment) or 35 µg/m³ (nonattainment)
│   ├── Ozone ≤ 0.07 ppm
│   └── Each VOC ≤ respective limit
├── AI Action: Flag any exceedances
└── Output: Contaminant compliance matrix

STEP 3: TVOC CALCULATION
├── Input: GC/MS analytical data
├── AI Action: Calculate TVOC per EN 16516:2017 or CDPH v1.2
├── AI Action: Compare against 500 µg/m³ screening level
├── If exceeded: Flag for individual VOC investigation
└── Output: TVOC calculation + screening result

STEP 4: MONITOR SPEC VERIFICATION (Option 2)
├── Input: Monitor specifications for CO₂, PM2.5, TVOC, T, RH
├── AI Action: Verify "building grade or better" status
├── AI Action: Verify placement height (3-6 ft above floor)
└── Output: Monitor compliance verification

STEP 5: DOCUMENTATION COORDINATION
├── AI Action: Generate test result summary table
├── AI Action: Compile lab accreditation certificates
├── AI Action: Organize direct reading instrument specs
└── Output: Coordinated EQc5 submission package
```

#### Final Recommendation: **Assist Only** (AI can generate test plans and parse results, but physical testing is mandatory and cannot be automated)

---

## Part 3: Cross-Cutting AI Architecture

---

### Unified Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PROJECT DATA INTAKE LAYER                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │   BIM/Revit │  │  Schedules │  │ Cut Sheets │  │   Drawings  │   │
│  │   Import    │  │ (Excel/CSV) │  │   (PDF)    │  │ (PDF/DWG)  │   │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘   │
│        │               │               │               │            │
│        ▼               ▼               ▼               ▼            │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │              MULTI-MODAL DOCUMENT PARSER                    │    │
│  │  • OCR/vision for drawings and cut sheets                   │    │
│  │  • Table extraction from schedules                          │    │
│  │  • Text extraction from specs                               │    │
│  │  • BIM geometry extraction                                  │    │
│  └─────────────────────────┬──────────────────────────────────┘    │
│                            │                                         │
│                            ▼                                         │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │              UNIFIED PROJECT DATABASE                        │    │
│  │  • Fixtures: type, qty, model, flow rate                     │    │
│  │  • Equipment: appliance, kitchen, lab specs                  │    │
│  │  • HVAC: zones, CFM, filtration, OA rates                    │    │
│  │  • Spaces: area, occupancy, glazing, room type               │    │
│  │  • Envelope: U-values, SHGC, window operability              │    │
│  └─────────────────────────┬──────────────────────────────────┘    │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     CALCULATION ENGINE LAYER                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────┐│
│  │  WATER CALCULATOR   │  │  VENTILATION CALC   │  │  SPATIAL       ││
│  │  • WEp2 baseline    │  │  • ASHRAE 62.1 VRP  │  │  ANALYZER      ││
│  │  • WEc2 options 1-6 │  │  • OA rate increase │  │  • View area % ││
│  │  • TIR calculator   │  │  • Filtration check │  │  • Daylight    ││
│  │  • Cooling cycles   │  │  • Residential 62.2 │  │    proximity   ││
│  └────────────────────┘  └────────────────────┘  └────────────────┘│
│                                                                      │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────┐│
│  │  POINT OPTIMIZER    │  │  COMPLIANCE         │  │  CROSS-CREDIT  ││
│  │  • Multi-option     │  │  CHECKER            │  │  INTEGRATOR    ││
│  │    scoring          │  │  • Standard lookup  │  │  • WEp2→WEc2   ││
│  │  • Points/cost      │  │  • Threshold        │  │  • EQp2→EQc1   ││
│  │    analysis         │  │    comparison       │  │  • EQp2→EQc2   ││
│  │  • Strategy         │  │  • Gap analysis     │  │  • IPp2→EQc3   ││
│  │    recommendations  │  │  • Risk flags       │  │  • Shared data ││
│  └────────────────────┘  └────────────────────┘  └────────────────┘│
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  DOCUMENT GENERATION LAYER                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              LLM NARRATIVE GENERATION MODULE                  │   │
│  │                                                              │   │
│  │  Templates:                                                  │   │
│  │  ├── Construction Management Plan     (EQp1)                 │   │
│  │  ├── Leak Detection Action Plan       (WEc1)                 │   │
│  │  ├── Outdoor Air Quality Investigation (EQp2)                │   │
│  │  ├── Biophilic Design Narrative       (EQc2)                 │   │
│  │  ├── Adaptable Environment Narrative  (EQc2)                 │   │
│  │  ├── Thermal Environment Analysis     (EQc2)                 │   │
│  │  ├── Accessibility Strategy Descriptions (EQc3)              │   │
│  │  ├── Management Mode Documentation    (EQc4)                 │   │
│  │  └── Water Reuse / Alternative Source Narratives (WEc2)      │   │
│  │                                                              │   │
│  │  Inputs: Project metadata + design features + compliance     │   │
│  │  Output: Submission-ready narrative documents                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              TEMPLATE FILLING MODULE                          │   │
│  │                                                              │   │
│  │  ├── LEED Credit Forms (auto-populated calculations)         │   │
│  │  ├── Compliance Tables (fixture, equipment, filtration)      │   │
│  │  ├── Equipment Schedules with compliance flags               │   │
│  │  ├── Specification Verification Matrices                     │   │
│  │  └── Cut Sheet Index with cross-references                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              CHECKLIST & SURVEY MODULE                        │   │
│  │                                                              │   │
│  │  ├── Implementation Checklists (EQp1 construction)           │   │
│  │  ├── Accessibility Strategy Evaluation (EQc3)                │   │
│  │  ├── Equipment Compliance Checklists                         │   │
│  │  ├── Occupant Experience Surveys (EQc2)                      │   │
│  │  └── Field Verification Photo Log Templates                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part 4: Implementation Prioritization Matrix

---

### Priority 1: MVP — Automate First (Highest ROI)

| Rank | Credit | Auto | Value | Effort | Why MVP? |
|------|--------|------|-------|--------|----------|
| 1 | **WEp2** | 5 | 5 | Medium | Prerequisite for ALL projects; pure calculation engine; feeds WEc2; highest time savings |
| 2 | **WEc2** | 5 | 5 | Medium | Up to 8 points; inherits WEp2 data; multi-option optimizer; biggest points impact |
| 3 | **EQp1** | 4 | 5 | Low | Prerequisite; pure LLM generation; 8-12 page plan from template; immediate time savings |
| 4 | **EQp2** | 4 | 4 | High | Prerequisite; ASHRAE 62.1 calc engine; complex but high-value; feeds EQc1 |
| 5 | **EQc3** | 4 | 4 | Low | 1 point; checklist-driven; LLM narratives; low effort, high success rate |
| 6 | **WEp1** | 4 | 4 | Low | Prerequisite; commitment letter + access protocol; template-driven |
| 7 | **WEc1** | 4 | 4 | Low | 1 point; action plan generation + coverage calc; simple extension of WEp1 |

### Priority 2: Phase 2 — Automate Later

| Rank | Credit | Auto | Value | Effort | Why Later? |
|------|--------|------|-------|--------|------------|
| 8 | **EQc2** | 4 | 4 | High | Up to 7 points; daylight simulation integration is complex; survey platform is unique; high effort but high reward |
| 9 | **EQc1** | 3 | 3 | Low | 1 point; simple extension of EQp2 calc engine; low hanging fruit after EQp2 |
| 10 | **EQc4** | 3 | 3 | High | 1-2 points; thermal modeling integration; specialized; growing climate importance |
| 11 | **EQp3** | 3 | 3 | Low | Prerequisite; relatively simple; site plan analysis adds moderate value |

### Priority 3: Assist Only

| Rank | Credit | Auto | Value | Reason |
|------|--------|------|-------|--------|
| 12 | **EQc5** | 2 | 3 | Physical laboratory testing is mandatory; AI can generate test plans and parse results only |

---

## Part 5: Technical Implementation Stack

---

### Recommended Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Document Parsing** | Python + PyPDF2/pdfplumber + OpenCV | Extract tables from schedules, parse cut sheets, OCR drawings |
| **Calculation Engine** | Python + Pandas + NumPy | Water calculations, ventilation rates, spatial analysis |
| **LLM Generation** | GPT-4/Claude + Structured Templates | Narrative document generation with project-specific context |
| **Drawing Analysis** | OpenCV + shapely + ifcopenshell | Floor plan parsing, area calculations, spatial queries |
| **Daylight Simulation** | Radiance/Daysim API or ClimateStudio integration | sDA/ASE calculations per IES LM-83-23 |
| **BIM Integration** | ifcopenshell / Revit API | Extract geometry, schedules, and properties from building models |
| **Database** | PostgreSQL + JSONB | Project data storage, queryable fixture/equipment database |
| **API Layer** | FastAPI | RESTful endpoints for credit calculations and document generation |
| **Frontend** | React/Vue | User interface for data input, results review, document export |

### Key APIs and External Data Sources

| Data Source | Credits Using | Data Provided |
|-------------|--------------|---------------|
| **EPA AirNow API** | EQp2, EQc5 | Local air quality, attainment status |
| **US Census API** | EQc3 | Local language demographics |
| **ENERGY STAR Product Finder** | WEp2, WEc2 | Appliance certification lookup |
| **EPA WaterSense Product Search** | WEp2, WEc2 | Fixture certification verification |
| **TMY3/EPW Weather Data** | EQc4 | Peak climate conditions for thermal modeling |
| **ASHRAE Standards Database** | EQp2, EQc1, EQc2 | Ventilation rates, thermal comfort criteria |

---

## Part 6: Risk Assessment & Mitigation

---

### Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Calculation errors** | Medium | High | Peer review workflow; unit test all formulas against LEED reference examples; engineer sign-off |
| **OCR/spec parsing errors** | Medium | Medium | Confidence scoring on extracted values; human review flag for low-confidence extractions; manual override |
| **LLM hallucination in narratives** | Low-Medium | Medium | Structured templates with constrained generation; factual grounding in project data; human review |
| **Incorrect standard reference** | Low | High | Version-locked standards database; update alerts when standards change; compliance team review |
| **Daylight simulation inaccuracy** | Medium | Medium | Benchmark against known simulation tools; validation against physical measurements; qualified analyst review |
| **Over-automation (missing project-specific factors)** | Medium | High | Gap analysis prompts; project-specific question flow; always allow human override; qualified professional review |

### Quality Assurance Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                    QA REVIEW WORKFLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LEVEL 1: AUTOMATED QA (Always Run)                              │
│  ├── Calculation unit tests (known test cases)                   │
│  ├── Range validation (flow rates, reduction %)                  │
│  ├── Cross-credit consistency checks                             │
│  ├── Unit conversion verification (IP ↔ SI)                      │
│  └── Completeness check (all required fields populated)          │
│                                                                  │
│  LEVEL 2: AI QA REVIEW (Flagged Items)                           │
│  ├── Low-confidence OCR extractions → human review               │
│  ├── Values outside expected ranges → human review               │
│  ├── First-time project types → enhanced review                  │
│  └── Complex multi-option credits → engineer review              │
│                                                                  │
│  LEVEL 3: PROFESSIONAL REVIEW (Required Before Submission)       │
│  ├── Licensed engineer sign-off on all calculations              │
│  ├── LEED AP review of narrative documents                       │
│  ├── Final completeness check against USGBC requirements         │
│  └── Project team approval of all generated documents            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 7: Commercial Impact Summary

---

### Time Savings Estimates (Per Project)

| Credit | Manual Hours | Automated Hours | Savings | Annual Savings (50 projects) |
|--------|-------------|----------------|---------|------------------------------|
| WEp2 | 8-12 hrs | 1-2 hrs | 7-10 hrs | 350-500 hrs |
| WEc2 | 12-20 hrs | 2-3 hrs | 10-17 hrs | 500-850 hrs |
| EQp1 | 6-10 hrs | 1 hr | 5-9 hrs | 250-450 hrs |
| EQp2 | 10-16 hrs | 2-3 hrs | 8-13 hrs | 400-650 hrs |
| EQc2 (daylight) | 16-24 hrs | 4-6 hrs | 12-18 hrs | 600-900 hrs |
| EQc3 | 4-8 hrs | 1 hr | 3-7 hrs | 150-350 hrs |
| WEp1 | 2-4 hrs | 0.5 hr | 1.5-3.5 hrs | 75-175 hrs |
| WEc1 | 3-6 hrs | 0.5 hr | 2.5-5.5 hrs | 125-275 hrs |
| **TOTAL MVP** | **61-100 hrs** | **12-17 hrs** | **49-83 hrs** | **2,450-4,150 hrs** |

### Points Coverage

| Category | Credits Automated | Points Covered | % of Category |
|----------|------------------|----------------|---------------|
| Water Efficiency | 4/4 | Prereqs + up to 15 pts | 100% |
| Indoor Environmental Quality | 7/8 | Prereqs + up to 13 pts | ~90% (EQc5 assist-only) |

### Competitive Differentiation

| Feature | Market Position |
|---------|----------------|
| **Water calculation engine** | Unique — no competitor offers automated fixture-to-submission pipeline |
| **Multi-option WEc2 optimizer** | Unique — real-time points optimization across 6 options |
| **LLM plan generation** | Emerging — few competitors, significant moat via template quality |
| **Occupant survey platform** | Unique — integrated survey + LEED documentation |
| **Cross-credit data flow** | Unique — WEp2→WEc2, EQp2→EQc1→EQc2 integration |
| **Daylight simulation integration** | Rare — only most expensive competitors offer this |

---

## Appendices

### Appendix A: Automation Score Distribution

```
Automation Score Distribution (12 credits):

Score 5 (Fully Automated):  ████████████  2 credits (WEp2, WEc2)
Score 4 (Mostly Automated): ██████████████████████  7 credits (WEp1, WEc1, EQp1, EQp2, EQc2, EQc3)
Score 3 (Partially Automated): ██████  2 credits (EQp3, EQc1, EQc4)
Score 2 (Low Automation):     █  1 credit (EQc5)
Score 1 (Not Practical):      0 credits

Mean Automation Score: 3.9/5
Median Automation Score: 4/5
```

### Appendix B: LEED Standard Reference Map

| Standard | Credits Using It | Automation Approach |
|----------|-----------------|---------------------|
| ASHRAE 62.1-2022 | EQp2, EQc1, EQc4 | Table lookups for rates; calculation engine for VRP |
| ASHRAE 55-2023 | EQc2 Option 3 | Compliance checklist; narrative generation |
| ASHRAE 241-2023 | EQp2, EQc4 Options 1-2 | Requirements database; documentation template |
| ASHRAE 62.2-2022 | EQp2 (residential) | Calculation engine for ventilation/exhaust |
| IES LM-83-23 | EQc2 Path 4 | Simulation integration; results parsing |
| IES TM-30-20 | EQc2 Path 2 | Specification verification |
| EPA TIR Methodology | WEp2, WEc2 Option 4 | Calculation engine |
| ENERGY STAR | WEp2, WEc2 Option 3 | API lookup for product certification |
| EPA WaterSense | WEp2 | Product database verification |

### Appendix C: Credit Dependency Graph

```
WEp2 (Minimum Water Efficiency)
  ├──► WEc2 Option 2 (Fixture Reduction) [inherits baseline]
  ├──► WEc1 (submeter 80% of WEp2 fixtures)
  └──► WEc2 Option 1 (Whole-Project) [uses WEp2 water model]

EQp2 (Fundamental Air Quality)
  ├──► EQc1 Option 1 (15% increased ventilation) [inherits VRP calc]
  └──► EQc1 Option 2 (enhanced IAQ design) [builds on EQp2 baseline]

EQp1 (Construction Management)
  └──► EQc2 Option 1 Path 1 (Biophilic) [#16 accessibility strategy]

IPp2 (Human Impact Assessment)
  └──► EQc3 (local accessibility code identification)

EQc2 Occupant Experience
  ├──► EQc3 (#16 neurodivergent strategy requires EQc2 Path 1)
  └──► EQc4 (thermal safety informed by thermal environment design)
```

---

*Analysis completed. 12 credits analyzed across 8 dimensions each = 96 individual assessments. 9 credits recommended for automation (4+ score), 2 for later automation (score 3), 1 for assist-only (score 2). Estimated time savings: 49-83 hours per project for MVP automation scope.*

*Document generated for orchestrator integration and product roadmap prioritization.*
