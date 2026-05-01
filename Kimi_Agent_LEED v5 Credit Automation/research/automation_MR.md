# LEED v5 MR Credits: AI Automation Potential Analysis

**Analysis Date:** Current Session
**Analyst:** AI Product Strategist / LEED Consultant / LCA Practitioner
**Source Document:** `/mnt/agents/output/research/leed_MR_extracted.md`
**Credits Analyzed:** 7 (MRp1, MRp2, MRc1, MRc2, MRc3, MRc4, MRc5)

---

## Executive Summary

The Materials and Resources (MR) category presents **exceptional automation potential** across all credits. Of the 7 credits analyzed, **5 are rated for MVP automation** (Automation Score 4+), **1 rated for Later automation**, and **1 rated as Assist Only**. The category is characterized by:

- **Data-heavy calculations** (GWP, diversion rates, compliance percentages)
- **Document-intensive workflows** (EPDs, certifications, hauler reports)
- **Rule-based compliance screening** (low-emitting thresholds, scoring matrices)
- **Repetitive data entry** (product lists, material quantities, manufacturer lookups)

### Top Automation Candidates

| Rank | Credit | Auto Score | Commercial Value | Key Automation Enabler |
|------|--------|-----------:|-----------------:|----------------------|
| 1 | MRc3: Low-emitting Materials | **5/5** | **4/5** | Rule-based compliance table — fully automatable |
| 2 | MRp2: Quantify Embodied Carbon | **4/5** | **5/5** | EPD parsing + EC3/CLF integration + calculation engine |
| 3 | MRc2: Reduce Embodied Carbon | **4/5** | **5/5** | Same pipeline as MRp2 with benchmarking + scenario comparison |
| 4 | MRc4: Building Product Selection | **4/5** | **5/5** | Multi-attribute scoring engine + certification database |
| 5 | MRc5: C&D Waste Diversion | **4/5** | **4/5** | Hauler report parsing + diversion calculation engine |
| 6 | MRp1: Zero Waste Operations | **3/5** | **3/5** | Template generation + plan drafting (physical verification needed) |
| 7 | MRc1: Building/Materials Reuse | **3/5** | **3/5** | Calculation engine + salvage assessment template |

### Total Addressable Market Value

- **MR category represents up to 21 points (NC) / 26 points (C&S)** — highest automation-value credit category in LEED
- **Platinum prerequisite:** 20% embodied carbon reduction ties directly to MRp2 + MRc2 automation
- **Repetitive project type work** makes MR credits ideal for automation (every project needs these calculations)
- **Document processing burden** is highest in MR category (EPDs, certifications, hauler tickets, test reports)

---

## Detailed Credit Analysis

---

# MRp1: Planning for Zero Waste Operations

## Scoring Summary

| Metric | Score |
|--------|-------|
| **Automation Score** | **3/5** |
| **Commercial Value** | **3/5** |
| **Risk Level** | **Low** |
| **Documentation Type** | Waste Management Plan (template), Site Plan Narrative, Maintenance Manual Excerpts |
| **Final Recommendation** | **Automate in MVP** — Plan Generation Module |

---

## Required Inputs vs. AI-Processable Elements

| Input Category | Source | AI Role |
|---------------|--------|---------|
| **Site plan / floor plans** | Architect/Designer | Parse CAD/PDF to identify areas for collection/storage zones |
| **Local recycling services availability** | Municipal sources | Research and auto-populate |
| **Building type / occupancy** | Project brief | Auto-configure plan template |
| **Local regulations** | Municipal code | Research and incorporate |
| **Waste stream characterization** | Project data | Template-generated with defaults |
| **Zero waste operations plan** | **AI GENERATED** | Full plan generation from template + project parameters |
| **Safe handling procedures** | Regulatory standards | Template-generated |
| **Tenant guidelines (C&S)** | **AI GENERATED** | Auto-generate from base plan |

---

## AI Techniques Applicable

| Technique | Application | Maturity |
|-----------|-------------|----------|
| **Document template generation** | Generate complete Zero Waste Operations Plan | High |
| **CAD/PDF plan parsing** | Identify suitable areas for collection/storage | Medium |
| **Regulatory research agent** | Auto-populate local recycling requirements | Medium |
| **Building type classification** | Select appropriate plan template variant | High |
| **Narrative generation** | Write plan narratives from project parameters | High |

---

## Automation Blueprint (Score: 3)

### Workflow: Zero Waste Operations Plan Generator

```
Step 1: PROJECT INTAKE
├── Input: Building type, square footage, occupancy count, location
├── Input: Floor plans (PDF/DWG) or space program
└── AI Action: Classify building type, select template variant

Step 2: AREA ANALYSIS (Semi-automated)
├── Input: Floor plans
├── AI Action: Parse plans to identify:
│   ├── Loading dock / service entrance locations
│   ├── Janitorial closet locations
│   ├── Common area / break room locations
│   ├── Parking area access points
│   └── Potential storage area candidates
├── Human Review: Confirm area selections (REQUIRED — physical verification)
└── Output: Annotated plan with proposed collection zones

Step 3: LOCAL SERVICE RESEARCH
├── AI Action: Research municipal recycling programs for project location
├── AI Action: Identify local organic waste collection services
├── AI Action: Identify e-waste recycling providers
├── AI Action: Identify battery recycling programs
├── AI Action: Identify mercury lamp disposal options
└── Output: Local service provider list with contact info

Step 4: PLAN GENERATION (Fully Automated)
├── AI Action: Assemble plan from template + project data
├── Sections auto-generated:
│   ├── Executive Summary
│   ├── Waste Stream Characterization
│   ├── Collection Infrastructure Design
│   ├── Storage Area Specifications
│   ├── Recyclable Materials Accepted (all 7 types)
│   ├── Hazardous Material Handling (batteries, lamps, e-waste)
│   ├── Occupant Education Program
│   ├── Janitorial Staff Protocols
│   ├── Vendor/Service Provider Specifications
│   ├── Monitoring and Reporting Procedures
│   └── Appendices (signage specs, training materials)
└── Output: Complete draft Zero Waste Operations Plan

Step 5: TENANT GUIDELINES (C&S Only)
├── AI Action: Extract building infrastructure info
├── AI Action: Generate tenant guideline section
└── Output: Draft tenant waste management guidelines

Step 6: REVIEW & EXPORT
├── Human Review: Technical review (1-2 hours vs. 8-12 manual)
├── Export: Word, PDF, or LEED Online format
└── Deliverable: Ready-to-submit Zero Waste Operations Plan
```

---

## Implementation Estimate

| Task | Manual Hours | Automated Hours | Savings |
|------|-------------|----------------|---------|
| Plan drafting | 8-12 | 1-2 (review) | **85%** |
| Area identification | 2-4 | 0.5 (review) | **75%** |
| Local service research | 2-3 | 0 (automated) | **100%** |
| Tenant guideline drafting | 2-3 | 0.5 (review) | **80%** |
| **TOTAL** | **14-22** | **2-3.5** | **~85%** |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Site plan interpretation errors | Human review gate for area identification |
| Changing local regulations | Quarterly database updates for municipal programs |
| Plan not specific enough | Template includes project-specific parameter injection |
| Signage specifications | Pre-approved signage library from USGBC examples |

---

# MRp2: Quantify and Assess Embodied Carbon

## Scoring Summary

| Metric | Score |
|--------|-------|
| **Automation Score** | **4/5** |
| **Commercial Value** | **5/5** |
| **Risk Level** | **Medium** |
| **Documentation Type** | Embodied Carbon Quantification Report, GWP Calculation Spreadsheet |
| **Final Recommendation** | **Automate in MVP** — Core Module (Required Prerequisite) |

---

## Required Inputs vs. AI-Processable Elements

| Input Category | Source | AI Role |
|---------------|--------|---------|
| **Material quantities (takeoff)** | Estimator / BIM / Specs | Parse from documents; manual entry fallback |
| **EPD PDFs for specified materials** | Manufacturers / EPD databases | **FULLY PARSE** — extract GWP/unit, declared unit, scope |
| **EC3/CLF industry average data** | Public API / database | **AUTO-INTEGRATE** — lookup benchmarks |
| **ILCD+EPD digital files** | EPD platforms (ECO Platform, IBU) | **FULLY PARSE** — structured data extraction |
| **Material classification** | Project data | Auto-map to EC3/CLF categories |
| **Top 3 hotspot identification** | **AI GENERATED** | Rank materials by total GWP contribution |
| **Reduction strategies narrative** | **AI GENERATED** | Draft from hotspot analysis + best practices DB |
| **Quantification report** | **AI GENERATED** | Full report generation |
| **Tenant guidelines (C&S)** | **AI GENERATED** | Auto-generate summary |

---

## AI Techniques Applicable

| Technique | Application | Maturity |
|-----------|-------------|----------|
| **EPD PDF parsing & data extraction** | Extract GWP (A1-A3), declared unit, material category from any PDF EPD | High — ISO 14025/EN 15804 structure is predictable |
| **ILCD+EPD digital format parsing** | Parse structured XML EPD data | High — standardized format |
| **EC3/CLF database integration** | Auto-lookup industry average GWP for material categories | High — EC3 has public API |
| **Material schedule parsing** | Extract material quantities from spec documents, BIM schedules | Medium-High |
| **Calculation engine** | GWP total = SUM(GWP/unit x Quantity) across all materials | High — straightforward math |
| **Hotspot ranking** | Rank materials by total GWP, identify top 3 | High |
| **Narrative generation** | Draft reduction strategies from hotspot analysis | Medium-High |
| **Report generation** | Generate full quantification report | High |
| **BIM/Revit data extraction** | Pull material quantities directly from model | Medium |

---

## Automation Blueprint (Score: 4)

### Workflow: Embodied Carbon Quantification Engine

```
PHASE 1: MATERIAL INTAKE
┌─────────────────────────────────────────────────────────────┐
│ Step 1.1: MATERIAL SCHEDULE IMPORT                          │
│ ├── Input: Material takeoff (Excel/CSV) from estimator       │
│ ├── Input: Spec section PDFs                                  │
│ ├── Input: BIM material schedule export                       │
│ ├── AI Action: Parse and normalize material list              │
│ ├── AI Action: Categorize materials into EC3/CLF categories   │
│ └── Output: Normalized material database with quantities      │
├─────────────────────────────────────────────────────────────┤
│ Step 1.2: EPD COLLECTION & PARSING                           │
│ ├── Input: EPD PDFs from manufacturers / reps                 │
│ ├── Input: EPD URLs (ECO Platform, EPD Norge, IBU, etc.)     │
│ ├── AI Action: Download EPDs from URLs                        │
│ ├── AI Action: Parse PDF EPDs — extract:                      │
│ │   ├── Product name / manufacturer                           │
│ │   ├── Declared unit (m2, kg, m3, etc.)                      │
│ │   ├── Reference service life                                │
│ │   ├── GWP A1-A3 (kg CO2e per declared unit)                 │
│ │   ├── EPD scope (cradle-to-gate confirmed)                  │
│ │   ├── EPD validity date                                     │
│ │   └── Third-party verifier                                  │
│ ├── AI Action: Match parsed EPDs to material schedule items   │
│ └── Output: EPD-matched material database with GWP values     │
├─────────────────────────────────────────────────────────────┤
│ Step 1.3: GAP FILLING (EC3/CLF Integration)                  │
│ ├── AI Action: For materials WITHOUT EPDs:                    │
│ │   ├── Query EC3 API for product-specific GWP                │
│ │   ├── Query CLF Material Baselines for industry average     │
│ │   └── Apply conservative default based on material category │
│ ├── AI Action: Flag confidence level per material             │
│ │   ├── High: Product-specific Type III EPD                   │
│ │   ├── Medium: EC3 product data                              │
│ │   └── Low: CLF industry average                             │
│ └── Output: Complete GWP dataset for all materials            │
└─────────────────────────────────────────────────────────────┘

PHASE 2: CALCULATION ENGINE
┌─────────────────────────────────────────────────────────────┐
│ Step 2.1: CRADLE-TO-GATE GWP CALCULATION                    │
│ ├── Formula: GWP_total = SUM(GWP_unit_i x Quantity_i)        │
│ ├── For each material:                                        │
│ │   ├── Convert quantity to declared unit if needed           │
│ │   ├── Calculate material-level GWP                          │
│ │   └── Roll up by category (concrete, steel, etc.)           │
│ ├── Calculate project total GWP                               │
│ ├── Calculate GWP per square foot (intensity metric)          │
│ └── Output: Detailed GWP calculation spreadsheet              │
├─────────────────────────────────────────────────────────────┤
│ Step 2.2: HOTSPOT ANALYSIS                                   │
│ ├── AI Action: Rank all materials by total GWP contribution   │
│ ├── AI Action: Rank by material category                      │
│ ├── AI Action: Calculate % contribution per material          │
│ ├── AI Action: Identify TOP 3 sources                         │
│ ├── AI Action: Generate hotspot visualization                 │
│ └── Output: Hotspot report with ranked materials              │
├─────────────────────────────────────────────────────────────┤
│ Step 2.3: REDUCTION STRATEGIES                               │
│ ├── AI Action: Query best practices database by material type │
│ ├── For each hotspot material, suggest:                       │
│ │   ├── Alternative materials with lower GWP                  │
│ │   ├── Mix optimization (e.g., SCM % in concrete)            │
│ │   ├── Supplier switching to lower-carbon producers          │
│ │   └── Design optimization (reduce quantity)                 │
│ ├── AI Action: Draft reduction strategies narrative           │
│ └── Output: Draft reduction strategies section                │
└─────────────────────────────────────────────────────────────┘

PHASE 3: REPORT GENERATION
┌─────────────────────────────────────────────────────────────┐
│ Step 3.1: REPORT ASSEMBLY                                    │
│ ├── Sections auto-generated:                                  │
│ │   ├── Executive Summary                                     │
│ │   ├── Project Description & Scope                           │
│ │   ├── Methodology (ISO 21930 / EN 15804)                    │
│ │   ├── System Boundary (A1-A3 Cradle-to-Gate)                │
│ │   ├── Material Inventory (complete list with quantities)    │
│ │   ├── EPD Summary (all EPDs used with references)           │
│ │   ├── GWP Calculations (detailed per material)              │
│ │   ├── Results by Material Category                          │
│ │   ├── Top 3 Hotspot Identification                          │
│ │   ├── Reduction Strategies Considered                       │
│ │   ├── Data Quality & Confidence Assessment                  │
│ │   ├── Limitations & Assumptions                             │
│ │   └── References & Appendices                               │
│ └── Output: Complete draft quantification report              │
├─────────────────────────────────────────────────────────────┤
│ Step 3.2: TENANT GUIDELINES (C&S)                            │
│ ├── AI Action: Extract key embodied carbon data               │
│ ├── AI Action: Summarize material suppliers                   │
│ └── Output: Draft tenant guideline section                    │
├─────────────────────────────────────────────────────────────┤
│ Step 3.3: EXPORT & SUBMISSION                                │
│ ├── Export: Word, PDF, Excel calculations                     │
│ ├── Format: LEED Online ready                                 │
│ └── Deliverable: Complete MRp2 submission package             │
└─────────────────────────────────────────────────────────────┘
```

---

## EPD Parsing Engine — Technical Architecture

```
EPD Input → Classification → Extraction → Validation → Output
     │            │              │             │           │
     ▼            ▼              ▼             ▼           ▼
  [PDF]    →  [Layout     →  [Field      →  [Cross-  →  [Structured
  [URL]       Analysis]      Extraction]    Check]       JSON]
  [ILCD       (detect EPD    (GWP, unit,    (unit      (ready for
   XML]        template)      validity)      sanity)     calculation)
```

### Supported EPD Formats & Sources

| Source | Format | Parser Method | Coverage |
|--------|--------|--------------|----------|
| **ECO Platform** (EU) | PDF + ILCD+EPD | PDF parser + XML parser | 4,000+ EPDs |
| **IBU (Germany)** | PDF | PDF parser | 2,000+ EPDs |
| **EPD Norge** | PDF | PDF parser | 1,000+ EPDs |
| **ASTM/NSF (US)** | PDF | PDF parser | 1,500+ EPDs |
| **UL Environment** | PDF | PDF parser | 800+ EPDs |
| **SCS Global** | PDF | PDF parser | 600+ EPDs |
| **Direct from Manufacturers** | PDF | PDF parser | Variable |

### EC3/CLF Integration Points

| Integration | API/Method | Data Retrieved |
|-------------|-----------|----------------|
| **Embodied Carbon in Construction (EC3)** | Public API + data export | Product-specific GWP, project benchmarking |
| **CLF Material Baselines** | Annual report (published) | Industry average GWP by material category |
| **US EPA Benchmarks** | Published reports | Industry averages for select materials |
| **EPD Registry (ILCD)** | API query | Digital EPD structured data |

---

## Implementation Estimate

| Task | Manual Hours | Automated Hours | Savings |
|------|-------------|----------------|---------|
| Material schedule compilation | 4-6 | 1 (review) | **80%** |
| EPD collection & manual data entry | 8-16 | 1-2 (review matching) | **85%** |
| GWP calculations (spreadsheet) | 4-6 | 0 (fully auto) | **100%** |
| Hotspot analysis | 2-3 | 0 (fully auto) | **100%** |
| Report writing | 6-10 | 1-2 (review/edit) | **85%** |
| **TOTAL** | **24-41** | **3-7** | **~85%** |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| EPD parsing errors (wrong GWP value) | Dual-parser validation: extract from PDF + cross-check with EC3 database |
| Unit conversion errors | Automated unit conversion with explicit declared unit tracking |
| EPD scope misalignment (not A1-A3) | Parser flags scope; human review for non-standard EPDs |
| Material matching errors (wrong EPD to material) | Confidence scoring + human review for low-confidence matches |
| Calculation accuracy | Open calculation formulas; auditable spreadsheet export |
| Data quality for CLF averages | Flag when industry averages used; suggest product-specific EPDs |

---

# MRc1: Building and Materials Reuse

## Scoring Summary

| Metric | Score |
|--------|-------|
| **Automation Score** | **3/5** |
| **Commercial Value** | **3/5** |
| **Risk Level** | **Medium** |
| **Documentation Type** | Reuse Calculation Spreadsheet, Salvage Assessment Report, Photographic Evidence Log |
| **Final Recommendation** | **Automate Later** — Calculation engine with field data input |

---

## Required Inputs vs. AI-Processable Elements

| Input Category | Source | AI Role |
|---------------|--------|---------|
| **Existing building survey** | Field measurement / As-builts | Parse as-builts; field verification REQUIRED |
| **Existing floor area** | Construction documents | Auto-extract from drawings |
| **Reused structure area** | Field verification / Photos | Calculation engine; photo organization |
| **Material inventory (existing)** | Salvage assessment | Template-guided data collection |
| **Material inventory (new)** | Material schedule | Parse from specs |
| **Salvage assessment report** | **AI GENERATED** (template) | Full report template with field data insertion |
| **Reuse percentage calculations** | **AI CALCULATED** | Full calculation per Equation 1 |
| **Source documentation** | Salvage yards / Reuse markets | Document organization |
| **Photographic evidence** | Field photos | Auto-organize by material type |

---

## AI Techniques Applicable

| Technique | Application | Maturity |
|-----------|-------------|----------|
| **Construction document parsing** | Extract existing building areas from as-builts | Medium |
| **Calculation engine** | Reuse % = Reused area / Total area; per material type | High |
| **Template generation** | Salvage assessment report template | High |
| **Photo organization** | Auto-sort field photos by material category | Medium |
| **Drawing comparison** | Compare existing vs. demolition drawings | Low-Medium |
| **Deconstruction plan drafting** | Generate deconstruction sequencing plan | Medium |

---

## Automation Blueprint (Score: 3)

### Workflow: Building & Materials Reuse Documentation Engine

```
PATH A: BUILDING REUSE (Option 1)
Step 1: EXISTING CONDITIONS IMPORT
├── Input: As-built drawings (PDF/DWG)
├── Input: Existing building area calculation
├── AI Action: Parse drawings to extract:
│   ├── Total building area
│   ├── Floor deck area
│   ├── Roof deck area
│   ├── Enclosure area (walls, windows)
│   └── Structural system type
├── Input: Demolition / renovation scope drawings
├── AI Action: Compare existing vs. scope to identify:
│   ├── Areas remaining (reused)
│   ├── Areas being demolished
│   └── Areas being modified
└── Output: Building reuse calculation spreadsheet

Step 2: BUILDING REUSE CALCULATION
├── AI Action: Calculate reuse percentage:
│   └── Reuse % = Reused structure area / Total project area
├── AI Action: Map to points table (20%/35%/50% for NC)
├── AI Action: Generate calculation narrative
└── Output: Building reuse compliance documentation

PATH B: MATERIALS REUSE (Option 2)
Step 1: SALVAGE ASSESSMENT SETUP
├── Input: Deconstruction scope (if applicable)
├── AI Action: Generate salvage assessment template
├── AI Action: Create material inventory checklist
│   ├── Targeted materials (carpet, ceilings, furniture, walls)
│   └── Other materials (lumber, doors, fixtures, hardware)
└── Output: Field-ready salvage assessment form

Step 2: MATERIAL DATA COLLECTION
├── Input: Field survey data (quantities, conditions, locations)
├── Input: Salvage source documentation
├── AI Action: Organize by material type per Table 4
├── AI Action: Calculate reuse % per Equation 1:
│   └── Reuse % = Amount reused / Total amount in scope
└── Output: Material reuse calculation spreadsheet

Step 3: POINTS CALCULATION
├── AI Action: Apply weighted average rules
├── AI Action: Map to points thresholds
│   ├── 1 point: 15% of 1 targeted, OR 15% of 2 other
│   └── 2 points: 30% of 1 targeted, OR 15% of 2 targeted, etc.
└── Output: Points determination with supporting calcs

Step 4: DOCUMENTATION ASSEMBLY
├── AI Action: Generate reuse documentation package:
│   ├── Calculation summary
│   ├── Material inventory with sources
│   ├── Photographic evidence log (auto-organized)
│   └── Salvage assessment report (if deconstruction)
└── Output: Complete MRc1 submission package
```

---

## Implementation Estimate

| Task | Manual Hours | Automated Hours | Savings |
|------|-------------|----------------|---------|
| Existing conditions documentation | 4-6 | 1-2 | **65%** |
| Area calculations | 2-3 | 0 (auto) | **100%** |
| Salvage assessment (field) | 4-8 | 2-4 (template-guided) | **40%** |
| Calculation spreadsheets | 2-3 | 0 (auto) | **100%** |
| Report assembly | 2-4 | 0.5-1 | **75%** |
| **TOTAL** | **14-24** | **4-8** | **~55%** |

> **Note:** Lower automation savings due to field verification requirements. Physical survey of existing conditions cannot be automated.

---

# MRc2: Reduce Embodied Carbon

## Scoring Summary

| Metric | Score |
|--------|-------|
| **Automation Score** | **4/5** (Option 2: EPD Analysis) / **2/5** (Option 1: WBLCA) |
| **Commercial Value** | **5/5** |
| **Risk Level** | **Medium** |
| **Documentation Type** | WBLCA Report OR EPD Analysis Report OR Construction Emissions Log |
| **Final Recommendation** | **Automate in MVP** — EPD Analysis Path (Option 2) as primary; WBLCA (Option 1) as Assist |

---

## Required Inputs vs. AI-Processable Elements

| Input Category | Source | AI Role |
|---------------|--------|---------|
| **Material quantities (as-designed + as-constructed)** | Estimator / BIM | Parse; reconcile if >10% change |
| **Product-specific Type III EPDs** | Manufacturers | **FULLY PARSE** — GWP/unit extraction |
| **Industry average benchmarks** (CLF/EPA) | Public database | **AUTO-INTEGRATE** |
| **Baseline building model** (WBLCA Option 1) | LCA Practitioner | **ASSIST** — template + data prep; requires specialized LCA software |
| **Construction fuel/utility data** (Option 3) | Contractor logs | Parse from logs, invoices |
| **WBLCA report** (Option 1) | **AI ASSISTED** | Data prep, formatting, template; core LCA in specialized software |
| **EPD Analysis report** (Option 2) | **AI GENERATED** | Full report from parsed EPDs + calculations |
| **Construction emissions report** (Option 3) | **AI GENERATED** | Full report from fuel/utility data |
| **Material quantity reconciliation** | **AI CALCULATED** | Auto-flag if >10% change |

---

## AI Techniques Applicable

| Technique | Application | Maturity | Option |
|-----------|-------------|----------|--------|
| **EPD parsing & data extraction** | Extract GWP for EPD analysis | High | Option 2 |
| **EC3/CLF database integration** | Industry average benchmarking | High | Option 2 |
| **WBLCA report templating** | Format and structure WBLCA results | High | Option 1 |
| **Baseline scenario modeling** | Generate baseline building parameters | Medium | Option 1 |
| **Material quantity reconciliation** | Compare design vs. as-built quantities | High | All |
| **Reduction percentage calculation** | (Baseline - Proposed) / Baseline | High | All |
| **Points optimization engine** | Calculate maximum points path | Medium | All |
| **Fuel/utility log parsing** | Extract A5 emissions data | Medium | Option 3 |
| **Multi-impact category tracking** | GWP, ozone, acidification, eutrophication, smog, energy | Medium | Option 1 |

---

## Automation Blueprint (Score: 4 — EPD Analysis Path)

### Option 2: EPD Analysis — Full Automation Workflow

```
┌──────────────────────────────────────────────────────────────────┐
│                 MRc2: EPD ANALYSIS AUTOMATION PIPELINE           │
│                    (Highest automation potential)                 │
└──────────────────────────────────────────────────────────────────┘

PHASE 1: DATA COLLECTION (Reuses MRp2 pipeline)
┌────────────────────────────────────────────────────────────────┐
│ 1.1 Import material schedule (as-constructed quantities)       │
│ 1.2 Parse EPDs (same parser as MRp2)                           │
│ 1.3 Extract GWP/unit for each material                         │
│ 1.4 Auto-lookup CLF/EPA industry averages by category          │
│ 1.5 Calculate project-average GWP/unit                         │
│     └── Proj Avg = SUM(GWP_i x Qty_i) / SUM(Qty_i)            │
└────────────────────────────────────────────────────────────────┘

PHASE 2: PATH SELECTION & CALCULATION
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  PATH 1: PROJECT-AVERAGE APPROACH                              │
│  ├── Calculate weighted average GWP for entire project        │
│  ├── Compare to CLF/EPA industry average for same scope       │
│  ├── Calculate % reduction:                                   │
│  │   Reduction % = (Industry Avg - Project Avg) / Industry Avg │
│  ├── Map to points:                                           │
│  │   0% (meet avg) = 1 point                                  │
│  │   20% reduction = 2 points                                 │
│  │   40%+ reduction = 3 points                                │
│  └── Output: Path 1 compliance report                         │
│                                                                │
│  PATH 2: MATERIALS-TYPE APPROACH                               │
│  ├── Group materials by type (concrete, steel, insulation...) │
│  ├── For each material type:                                  │
│  │   ├── Calculate weighted average GWP/unit                   │
│  │   ├── Compare to industry benchmark                        │
│  │   └── Determine if below benchmark                         │
│  ├── Count material categories below benchmark                │
│  ├── Map to points:                                           │
│  │   3 categories (NC) / 2 categories (C&S) = 1 point         │
│  │   5+ categories (NC) / 4+ categories (C&S) = 2 points      │
│  └── Output: Path 2 compliance report                         │
│                                                                │
│  AI ACTION: Auto-recommend optimal path based on data          │
│  └── "Path 1 yields 3 points; Path 2 yields 2 points"        │
│                                                                │
└────────────────────────────────────────────────────────────────┘

PHASE 3: RECONCILIATION ENGINE
┌────────────────────────────────────────────────────────────────┐
│ 3.1 Compare as-designed vs. as-constructed quantities          │
│ 3.2 Auto-flag materials with >10% quantity change             │
│ 3.3 If flagged:                                                │
│     ├── Recalculate with as-constructed quantities            │
│     ├── Identify impact on total GWP                          │
│     └── Flag for human review                                  │
│ 3.4 If material substitution occurred:                        │
│     ├── Identify substituted materials                        │
│     ├── Parse new EPDs if needed                               │
│     └── Recalculate with new GWP values                       │
└────────────────────────────────────────────────────────────────┘

PHASE 4: REPORT GENERATION
┌────────────────────────────────────────────────────────────────┐
│ Sections auto-generated:                                       │
│ ├── Executive Summary                                          │
│ ├── Option Selected (Path 1 or Path 2)                        │
│ ├── Methodology (ISO 21930 / EN 15804 / CLF Baselines)        │
│ ├── Material Inventory (all covered materials)                │
│ ├── EPD Summary (all product-specific EPDs used)              │
│ ├── Industry Average Benchmarks (CLF/EPA references)          │
│ ├── Calculations:                                              │
│ │   ├── Project-average GWP/unit (Path 1)                     │
│ │   ├── Per-material-type GWP comparison (Path 2)             │
│ │   └── Reduction percentage vs. baseline                     │
│ ├── Points Determination                                       │
│ ├── Material Quantity Reconciliation (if applicable)          │
│ ├── Data Quality & Confidence Assessment                      │
│ └── Appendices (EPD references, calculation detail)           │
└────────────────────────────────────────────────────────────────┘
```

### Option 1: WBLCA — Assist-Only Workflow

```
┌──────────────────────────────────────────────────────────────────┐
│  MRc2 Option 1 (WBLCA) requires specialized LCA software        │
│  (Tally, One Click LCA, Revit LCA tools, etc.)                  │
│  AI CANNOT replace the LCA calculation engine.                  │
│                                                                 │
│  WHAT AI CAN DO:                                                │
│  ├── Prepare material inventory in LCA software import format   │
│  ├── Generate baseline building parameters from design data     │
│  ├── Extract material quantities from BIM for LCA import        │
│  ├── Template the WBLCA report structure                        │
│  ├── Format LCA software output into LEED-compliant report      │
│  ├── Generate all 6 required impact category tables             │
│  ├── Calculate % reduction from baseline                        │
│  ├── Draft narrative sections                                   │
│  └── Prepare LEED Online submission formatting                  │
│                                                                 │
│  WHAT REQUIRES SPECIALIZED SOFTWARE:                            │
│  ├── Building model creation in LCA tool                        │
│  ├── Life cycle impact calculations                             │
│  ├── Baseline building modeling                                 │
│  ├── Module A-C boundary calculations                           │
│  └── EPD data import into LCA tool                              │
└──────────────────────────────────────────────────────────────────┘
```

### Option 3: Construction Activity Tracking — Automation Workflow

```
Step 1: FUEL & UTILITY DATA IMPORT
├── Input: Contractor fuel receipts/invoices
├── Input: Utility bills for construction site
├── Input: Equipment logs (if available)
├── AI Action: Parse invoices to extract:
│   ├── Fuel type and quantity (gallons diesel, gasoline, etc.)
│   ├── Electricity usage (kWh)
│   ├── Natural gas usage (therms)
│   └── Date ranges
└── Output: Structured fuel/utility database

Step 2: EMISSIONS CALCULATION
├── AI Action: Apply EPA emission factors:
│   ├── Diesel: 22.38 lbs CO2/gallon
│   ├── Gasoline: 19.60 lbs CO2/gallon
│   ├── Electricity: eGrid factor by region
│   └── Natural gas: 11.7 lbs CO2/therm
├── AI Action: Calculate total A5 emissions
└── Output: A5 emissions report

Step 3: PATH DETERMINATION
├── Path 1: Contractor only → 1 point
├── Path 2: Contractor + subcontractors → 2 points
└── Output: Points determination

Step 4: REPORT GENERATION
├── AI Action: Generate complete tracking report
└── Output: Option 3 submission package
```

---

## Points Optimization Engine

```
┌─────────────────────────────────────────────────────────────────┐
│                    POINTS OPTIMIZER LOGIC                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INPUT: Material schedule + EPD library                         │
│                                                                 │
│  AI evaluates ALL options simultaneously:                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Option 1:      │  │  Option 2 Path 1│  │  Option 2 Path 2│ │
│  │  WBLCA          │  │  Project-Avg    │  │  Materials-Type │ │
│  │                 │  │                 │  │                 │ │
│  │  Points: 1-6    │  │  Points: 1-3    │  │  Points: 1-2    │ │
│  │  Effort: High   │  │  Effort: Low    │  │  Effort: Medium │ │
│  │  Auto: Partial  │  │  Auto: Full     │  │  Auto: Full     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                 │
│  AI RECOMMENDATION ENGINE:                                      │
│  ├── If Platinum target (20% reduction required):              │
│  │   └── Recommend Option 1 (WBLCA) or Option 2 Path 1        │
│  ├── If maximum points with minimum effort:                    │
│  │   └── Recommend Option 2 Path 1 (EPD Analysis)             │
│  ├── If limited EPD availability:                              │
│  │   └── Recommend Option 2 Path 2 (Materials-Type)           │
│  └── If construction-phase data available:                     │
│      └── Recommend Option 3 (Activity Tracking) as supplement  │
│                                                                 │
│  OUTPUT: Recommended pathway with projected points              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Estimate

### Option 2 (EPD Analysis) — Primary Automation Target

| Task | Manual Hours | Automated Hours | Savings |
|------|-------------|----------------|---------|
| EPD collection & data extraction | 12-20 | 2-3 (review) | **85%** |
| Industry average lookup | 4-6 | 0 (auto) | **100%** |
| Calculation (project-average or materials-type) | 4-6 | 0 (auto) | **100%** |
| Reduction analysis & points determination | 2-3 | 0 (auto) | **100%** |
| Material quantity reconciliation | 2-4 | 0.5 (review flags) | **85%** |
| Report writing | 6-10 | 1-2 (review/edit) | **85%** |
| **TOTAL (Option 2)** | **30-49** | **4-6** | **~88%** |

### Option 1 (WBLCA) — Assist Mode

| Task | Manual Hours | AI-Assisted Hours | Savings |
|------|-------------|------------------|---------|
| Material prep for LCA tool | 4-6 | 1-2 | **65%** |
| LCA modeling (specialized software) | 16-24 | 16-24 (no reduction) | **0%** |
| Report templating & formatting | 6-10 | 1-2 | **80%** |
| Baseline comparison & narrative | 2-4 | 0.5-1 | **75%** |
| **TOTAL (Option 1)** | **28-44** | **19-29** | **~25%** |

---

# MRc3: Low-emitting Materials

## Scoring Summary

| Metric | Score |
|--------|-------|
| **Automation Score** | **5/5** |
| **Commercial Value** | **4/5** |
| **Risk Level** | **Low** |
| **Documentation Type** | Compliance Table, Product Inventory with Certifications, Percentage Calculations |
| **Final Recommendation** | **Automate in MVP** — Flagship automation module |

---

## Required Inputs vs. AI-Processable Elements

| Input Category | Source | AI Role |
|---------------|--------|---------|
| **Product list / material schedule** | Specs / Submittals | **FULLY PARSE** — extract all products by category |
| **Manufacturer product data** | Submittals / Cut sheets | Extract product names, manufacturers, model numbers |
| **Third-party certifications** | Manufacturer docs / Online DB | **AUTO-LOOKUP** — query certifier databases |
| **CDPH Standard Method compliance** | Lab reports / Certifications | **AUTO-VALIDATE** — check dates, scenarios, limits |
| **BIFMA compliance** (furniture) | Manufacturer docs | **AUTO-VALIDATE** — check M7.1 + e3 compliance |
| **CARB/EPA formaldehyde compliance** | Manufacturer docs | **AUTO-VALIDATE** — ULEF/NAF certification check |
| **Inherently non-emitting determination** | Product classification | **AUTO-CLASSIFY** — apply product type rules |
| **VOC emissions evaluation** | **AI SCREENED** — rule-based pass/fail | Full automation against CDPH Table 4-1 limits |
| **Percentage compliance calculations** | **AI CALCULATED** | By cost, area, volume, or count per category |
| **Compliance table** | **AI GENERATED** | Full compliance matrix |
| **LEED Online submission** | **AI FORMATTED** | Ready-to-upload format |

---

## AI Techniques Applicable

| Technique | Application | Maturity |
|-----------|-------------|----------|
| **Rule-based compliance engine** | Screen all products against CDPH/BIFMA/CARB thresholds | **Very High** — explicit thresholds make this ideal for automation |
| **Certification database lookup** | Query certifier APIs (GREENGUARD, SCS, CRI, FloorScore, etc.) | **High** — major certifiers have public databases |
| **Submittal document parsing** | Extract product info from submittal PDFs | **High** |
| **Material schedule parsing** | Extract product lists from specification documents | **High** |
| **Percentage calculator** | Calculate % compliance by cost/area/volume/count per category | **Very High** — straightforward math |
| **Compliance table generator** | Generate matrix of all products x categories x compliance status | **Very High** |
| **Exception flagging** | Identify products without sufficient documentation | **High** |
| **Narrative generator** | Write compliance narrative for LEED Online | **High** |
| **Document package assembler** | Compile all certifications, lab reports, compliance evidence | **High** |

---

## Automation Blueprint (Score: 5)

### Workflow: Low-Emitting Materials Compliance Engine

```
┌──────────────────────────────────────────────────────────────────┐
│          MRc3: FULLY AUTOMATED COMPLIANCE ENGINE                 │
│              (Highest automation score in MR category)            │
└──────────────────────────────────────────────────────────────────┘

PHASE 1: PRODUCT INVENTORY IMPORT
┌─────────────────────────────────────────────────────────────────┐
│ Step 1.1: MULTI-SOURCE PRODUCT DATA IMPORT                     │
│ ├── Source A: Specification documents (PDF/DOC)                │
│ │   └── AI Action: Parse sections to extract:                   │
│ │       ├── Product name, manufacturer, model number            │
│ │       ├── CSI division / product category                     │
│ │       └── Quantity (cost, area, volume, or count)             │
│ ├── Source B: Submittal documents (PDF)                        │
│ │   └── AI Action: Extract product data from submittal logs     │
│ ├── Source C: Material schedule (Excel)                        │
│ │   └── AI Action: Import and normalize                         │
│ ├── Source D: Procurement data / invoices                      │
│ │   └── AI Action: Extract product names and costs              │
│ ├── AI Action: DEDUPLICATE and MERGE all sources               │
│ ├── AI Action: CLASSIFY each product into LEED category:       │
│ │   ├── Paints and Coatings                                     │
│ │   ├── Adhesives and Sealants                                  │
│ │   ├── Flooring                                                │
│ │   ├── Walls                                                   │
│ │   ├── Ceilings                                                │
│ │   ├── Insulation                                              │
│ │   ├── Furniture                                               │
│ │   ├── Composite Wood                                          │
│ │   └── EXCLUDED (HVAC, electrical, structural, etc.)          │
│ └── Output: Complete product inventory with category assignments│
├─────────────────────────────────────────────────────────────────┤
│ Step 1.2: CERTIFICATION DATABASE QUERY                         │
│ For each product, AI queries certification databases:           │
│ ├── GREENGUARD Gold / GREENGUARD Certified                     │
│ ├── SCS Global Services (FloorScore, Indoor Advantage)         │
│ ├── Carpet and Rug Institute (CRI Green Label Plus)            │
│ ├── Declare (ILFI) — Red List Free status                      │
│ ├── Cradle to Cradle Certified                                  │
│ ├── BIFMA level (furniture)                                     │
│ ├── CARB/EPA Third-Party Certifier database (composite wood)   │
│ ├── Manufacturer-specific CDPH test reports                     │
│ └── AI Action: Store all certification evidence links           │
├─────────────────────────────────────────────────────────────────┤
│ Step 1.3: INHERENTLY NON-EMITTING CLASSIFICATION               │
│ AI Action: Auto-classify products as inherently non-emitting:  │
│ ├── Ceramic tile, porcelain, glass, stone, concrete (cured)    │
│ ├── Metals (steel, aluminum, copper)                           │
│ ├── Unfinished/untreated solid wood (case-by-case)             │
│ ├── Masonry, brick, plaster (cured)                            │
│ └── Output: Flag with "inherently non-emitting" status         │
└─────────────────────────────────────────────────────────────────┘

PHASE 2: RULE-BASED COMPLIANCE SCREENING
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  SCREENING ENGINE: For each product in each category, apply:    │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ CRITERION 1: VOC Emissions Evaluation                    │   │
│  │                                                          │   │
│  │ Check ONE of:                                            │   │
│  │ A. Third-party certification (GREENGUARD, FloorScore,    │   │
│  │    CRI Green Label Plus, SCS Indoor Advantage, etc.)     │   │
│  │    → VERIFY: Certification valid at purchase date        │   │
│  │    → VERIFY: Certification based on CDPH v1.2-2017       │   │
│  │    → VERIFY: Private office scenario (or school scenario)│   │
│  │                                                          │   │
│  │ B. Lab test report                                       │   │
│  │    → VERIFY: Tested within 3 years of purchase           │   │
│  │    → VERIFY: CDPH Standard Method v1.2-2017              │   │
│  │    → VERIFY: Meets Table 4-1 private office limits       │   │
│  │                                                          │   │
│  │ C. Inherently non-emitting / salvaged / reused           │   │
│  │    → VERIFY: Product classification matches              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ CRITERION 2: Furniture Emissions Evaluation              │   │
│  │                                                          │   │
│  │ Check ONE of:                                            │   │
│  │ A. Third-party certification                             │   │
│  │    → VERIFY: ANSI/BIFMA M7.1-2011(R2021) testing        │   │
│  │    → VERIFY: Complies with ANSI/BIFMA e3-2014 or e3-2024 │   │
│  │    → VERIFY: Correct scenario (seating/classroom/open)   │   │
│  │                                                          │   │
│  │ B. Inherently non-emitting / salvaged / reused           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ CRITERION 3: Formaldehyde Emissions (Composite Wood)     │   │
│  │                                                          │   │
│  │ Check ONE of:                                            │   │
│  │ A. ULEF certified under EPA TSCA Title VI or CARB ATCM   │   │
│  │ B. NAF certified under EPA TSCA Title VI or CARB ATCM    │   │
│  │ C. PS 1-09 or PS 2-10, labeled Exposure 1 or Exterior   │   │
│  │ D. Structural wood per ASTM D5456 / ANSI A190.1 /        │   │
│  │    ASTM D5055 / ANSI PRG 320 / PS 20-15                  │   │
│  │ E. Inherently non-emitting / salvaged / reused           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  OUTPUT per product: COMPLIANT / NON-COMPLIANT / PENDING        │
│  OUTPUT: Exception report for products requiring manual review   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

PHASE 3: PERCENTAGE CALCULATION ENGINE
┌─────────────────────────────────────────────────────────────────┐
│ For each product category, calculate:                           │
│                                                                 │
│ Compliant % = (Sum of compliant product values) /              │
│               (Sum of all product values in category)          │
│                                                                 │
│ Where "value" = cost OR area OR volume OR count (user selects) │
│                                                                 │
│ PATH DETERMINATION (New Construction):                          │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ Path 1 (1 point):                                        │    │
│ │   Paints >90% AND Flooring >90% AND Ceilings >90%        │    │
│ │                                                          │    │
│ │ Path 2 (2 points):                                       │    │
│ │   Path 1, PLUS any 2 of:                                 │    │
│ │   Adhesives >80%, Walls >80%, Insulation >80%,           │    │
│ │   Composite Wood >80%                                    │    │
│ │                                                          │    │
│ │ Path 3 (2 points):                                       │    │
│ │   Path 1, PLUS Furniture >80%                            │    │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                 │
│ PATH DETERMINATION (Core and Shell):                            │
│ ┌──────────────────────────────────────────────────────────┐    │
│ │ Any 3 of 7 categories at >90% = 1 point                  │    │
│ └──────────────────────────────────────────────────────────┘    │
│                                                                 │
│ AI OUTPUT:                                                     │
│ ├── Current compliance status per category                     │
│ ├── Path achievable with current products                      │
│ ├── GAP ANALYSIS: What additional compliance is needed         │
│ └── OPTIMIZATION: Which product changes would maximize points  │
└─────────────────────────────────────────────────────────────────┘

PHASE 4: COMPLIANCE TABLE & REPORT GENERATION
┌─────────────────────────────────────────────────────────────────┐
│ Step 4.1: MASTER COMPLIANCE TABLE                              │
│ ├── Columns: Product | Manufacturer | Category | Quantity |    │
│ │            Certification | Test Date | Compliant? | Evidence  │
│ ├── Color-coded: Green (compliant) / Red (non-compliant) /    │
│ │                  Yellow (pending review)                     │
│ ├── Sortable by category, manufacturer, compliance status      │
│ └── Export: Excel, PDF, or direct to LEED Online               │
│                                                                 │
│ Step 4.2: LEED ONLINE SUBMISSION PACKAGE                       │
│ ├── Product category compliance documentation                   │
│ ├── All third-party certifications (compiled)                   │
│ ├── Percentage compliance calculations per category             │
│ ├── Product list with manufacturer information                  │
│ └── Narrative describing compliance approach                    │
│                                                                 │
│ Step 4.3: EXCEPTION REPORT                                     │
│ ├── Products without sufficient documentation                   │
│ ├── Certifications that have expired                            │
│ ├── Products requiring manual review                            │
│ └── Recommended actions to achieve compliance                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Certification Database Integration Map

| Certifier / Program | Database URL / API | Coverage | Auto-Queryable |
|---------------------|---------------------|----------|---------------|
| **GREENGUARD** (UL) | UL SPOT database | Paints, coatings, furniture, flooring | Yes |
| **FloorScore** (SCS) | SCS Global database | Flooring | Yes |
| **Indoor Advantage** (SCS) | SCS Global database | Various interior products | Yes |
| **CRI Green Label Plus** | CRI website | Carpet | Yes |
| **Declare** (ILFI) | Declare database | Red List Free status | Yes |
| **Cradle to Cradle** | C2C Certified Product Registry | Multi-attribute | Yes |
| **BIFMA level** | BIFMA website | Furniture | Partial |
| **CARB/EPA TPC** | EPA TSCA Title VI database | Composite wood | Yes |
| **ECOLOGO** (UL) | UL database | Various | Yes |
| **Blue Angel** | German certifier | Various | Partial |
| **Nordic Swan Ecolabel** | Nordic database | Various | Partial |

---

## Implementation Estimate

| Task | Manual Hours | Automated Hours | Savings |
|------|-------------|----------------|---------|
| Product inventory compilation | 8-12 | 1-2 (review) | **85%** |
| Certification lookup per product | 16-24 (2-3 min x 200-400 products) | 1-2 (exception review) | **95%** |
| Compliance screening per product | 8-12 | 0 (fully auto) | **100%** |
| Percentage calculations | 2-3 | 0 (fully auto) | **100%** |
| Compliance table creation | 4-6 | 0 (fully auto) | **100%** |
| Narrative writing | 2-3 | 0.5 (review) | **80%** |
| Document package assembly | 4-6 | 0.5 (review) | **90%** |
| **TOTAL** | **44-66** | **3-7** | **~92%** |

> **This is the highest time-savings credit in the MR category.** Manual certification lookup for 200-400 products is extremely labor-intensive and the #1 target for automation.

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Certification database query failure | Fallback to manual entry with clear UI; flag for human review |
| Product misclassification | Explicit classification rules with human override; confidence scoring |
| Expired certifications | Date validation engine auto-flags expired certs at time of purchase |
| Inherently non-emitting misclassification | Conservative classification — when in doubt, require certification |
| Category boundary disputes (e.g., is this wall or furniture?) | Decision tree with manual override option |
| Changing CDPH Standard Method versions | Engine tracks version used; alerts when new version published |

---

# MRc4: Building Product Selection and Procurement

## Scoring Summary

| Metric | Score |
|--------|-------|
| **Automation Score** | **4/5** |
| **Commercial Value** | **5/5** |
| **Risk Level** | **Low-Medium** |
| **Documentation Type** | Product Inventory with MAS Scores, Product Category Adjusted Value Calculations, Certification Evidence |
| **Final Recommendation** | **Automate in MVP** — Multi-Attribute Scoring Engine |

---

## Required Inputs vs. AI-Processable Elements

| Input Category | Source | AI Role |
|---------------|--------|---------|
| **Product inventory** (same as MRc3) | Specs / Submittals / Procurement | **FULLY PARSE** — reuse MRc3 product data |
| **Product values** (cost, area, volume, count) | Procurement data | **AUTO-EXTRACT** from invoices/schedule |
| **Manufacturer sustainability documentation** | Manufacturer websites / Cert DBs | **AUTO-LOOKUP** — query 15+ certification databases |
| **EPD availability** | EPD databases | **AUTO-QUERY** — check if product has EPD |
| **Health Product Declaration (HPD)** | HPD Public Repository | **AUTO-QUERY** |
| **Cradle-to-Cradle certification** | C2C database | **AUTO-QUERY** |
| **Material ingredient screening** | Manufacturer docs / HPDs | **AUTO-PARSE** — extract ingredient disclosures |
| **Social responsibility documentation** | Manufacturer reports | **AUTO-EXTRACT** — CSR reports, supply chain disclosures |
| **Circular economy documentation** | Manufacturer docs | **AUTO-ASSESS** — take-back programs, recyclability |
| **MAS score per product** | **AI CALCULATED** | Sum achievement levels across criteria areas |
| **Product category adjusted value** | **AI CALCULATED** | Equation 1: 100 x SUM(MAS x Value) / Total Value |
| **Points determination** | **AI CALCULATED** | Count categories exceeding 100% |

---

## AI Techniques Applicable

| Technique | Application | Maturity |
|-----------|-------------|----------|
| **Multi-attribute scoring engine** | Calculate MAS (1-5) per product across 5 criteria areas | **High** — rule-based scoring |
| **Certification database lookup** | Query 15+ databases for product sustainability credentials | **High** |
| **EPD existence check** | Verify if product has published Type III EPD | **High** |
| **HPD parsing** | Extract ingredient disclosures from Health Product Declarations | **Medium-High** |
| **Material ingredient screening** | Screen against priority chemical lists | **Medium** |
| **CSR report parsing** | Extract social responsibility metrics from manufacturer reports | **Medium** |
| **Circular economy assessment** | Evaluate take-back programs, recyclability claims | **Medium** |
| **Product category calculation engine** | Equation 1: adjusted value per category | **Very High** — straightforward math |
| **Points optimization** | Recommend product swaps to maximize points | **Medium** |
| **Document package assembly** | Compile all evidence for LEED submission | **High** |

---

## Automation Blueprint (Score: 4)

### Workflow: Multi-Attribute Scoring Engine

```
┌──────────────────────────────────────────────────────────────────┐
│         MRc4: MULTI-ATTRIBUTE SCORING ENGINE                     │
│          (5 Criteria Areas x 3 Achievement Levels)               │
└──────────────────────────────────────────────────────────────────┘

PHASE 1: PRODUCT DATA IMPORT (Reuse MRc3 inventory)
┌─────────────────────────────────────────────────────────────────┐
│ Step 1.1: Import product inventory from MRc3 pipeline           │
│ ├── Product name, manufacturer, category, value                 │
│ └── Already classified into eligible categories                 │
│                                                                 │
│ Step 1.2: EXPANDED CERTIFICATION LOOKUP                         │
│ For each product, query for evidence in FIVE criteria areas:    │
│                                                                 │
│  CRITERIA AREA 1: CLIMATE HEALTH                               │
│  ├── Product has Type III EPD (ISO 14025 / EN 15804)           │
│  │   └── Level 1: EPD available                                │
│  │   └── Level 2: EPD with lower GWP than industry average     │
│  │   └── Level 3: EPD with significantly lower GWP (top 20%)   │
│  └── Product has carbon footprint disclosure                    │
│                                                                 │
│  CRITERIA AREA 2: HUMAN HEALTH                                 │
│  ├── Product has HPD (Health Product Declaration)              │
│  │   └── Level 1: HPD available (Basic)                        │
│  │   └── Level 2: HPD with full disclosure                     │
│  │   └── Level 3: HPD with no Red List chemicals                │
│  ├── Product meets CDPH low-emitting (MRc3 compliant)          │
│  │   └── Counts toward Level 1                                 │
│  └── Product has GREENGUARD Gold / Cradle to Cradle            │
│      └── Contributes to higher levels                          │
│                                                                 │
│  CRITERIA AREA 3: ECOSYSTEM HEALTH                             │
│  ├── Product has FSC certification (wood products)             │
│  ├── Product has certified sustainable sourcing                │
│  ├── Product avoids harmful substances in production           │
│  └── Product has aquatic toxicity assessment                   │
│                                                                 │
│  CRITERIA AREA 4: SOCIAL HEALTH & EQUITY                       │
│  ├── Manufacturer has CSR report / supply chain disclosure     │
│  ├── Product has fair labor certification (Fair Trade, etc.)   │
│  ├── Manufacturer SA8000 or equivalent                         │
│  └── Product has local/regional sourcing claim                 │
│                                                                 │
│  CRITERIA AREA 5: CIRCULAR ECONOMY                             │
│  ├── Product has take-back program                             │
│  ├── Product contains recycled content (post-consumer)         │
│  ├── Product is recyclable at end-of-life                      │
│  ├── Product has Cradle to Cradle certification (Silver+)      │
│  └── Product is reusable / designed for disassembly            │
│                                                                 │
│  OUTPUT: Certification evidence matrix per product              │
│  (Which criteria areas have evidence, at what level)            │
└─────────────────────────────────────────────────────────────────┘

PHASE 2: MAS CALCULATION ENGINE
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  For each product:                                               │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Product MAS = SUM of achievement levels across criteria   │ │
│  │                (max 5 per product)                         │ │
│  │                                                            │ │
│  │  Example:                                                  │ │
│  │  • Product: Interior Paint                                 │ │
│  │  • Climate Health: Level 1 (EPD available) = 1             │ │
│  │  • Human Health: Level 2 (GREENGUARD Gold + HPD Full) = 2  │ │
│  │  • Ecosystem Health: Level 0 (no evidence) = 0             │ │
│  │  • Social Health: Level 1 (CSR report) = 1                 │ │
│  │  • Circular Economy: Level 1 (recycled content) = 1         │ │
│  │  ─────────────────────────────────────────────────         │ │
│  │  • Product MAS = 5 (MAXED OUT — ideal product)             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Adjusted Product Value = Product Value x Product MAS            │
│                                                                  │
│  Example:                                                        │
│  • Product cost: $5,000                                          │
│  • Product MAS: 3                                                │
│  • Adjusted Product Value = $5,000 x 3 = $15,000                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

PHASE 3: PRODUCT CATEGORY CALCULATION
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Equation 1 (per category):                                      │
│                                                                  │
│  Category Adjusted Value = 100 x [SUM(Product MAS x Product    │
│                                          Value) /                 │
│                                    (Total Value of all products  │
│                                           in category)]           │
│                                                                  │
│  Example — PAINTS & COATINGS category:                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Product      │ Cost    │ MAS │ Adjusted Value              │ │
│  │──────────────│─────────│─────│─────────────────────────────│ │
│  │ Paint A      │ $3,000  │ 3   │ $9,000                      │ │
│  │ Paint B      │ $5,000  │ 2   │ $10,000                     │ │
│  │ Paint C      │ $2,000  │ 1   │ $2,000                      │ │
│  │──────────────│─────────│─────│─────────────────────────────│ │
│  │ TOTAL        │ $10,000 │     │ SUM = $21,000               │ │
│  │                                                         │ │
│  │ Category Adjusted Value = 100 x ($21,000 / $10,000)     │ │
│  │                         = 210%                          │ │
│  │                                                         │ │
│  │ RESULT: >100% → EARNS 1 POINT for this category        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  REPEAT for all eligible product categories.                    │
│                                                                  │
│  POINTS TABLE:                                                   │
│  1 category >100%  = 1 point                                    │
│  2 categories >100% = 2 points                                  │
│  3 categories >100% = 3 points                                  │
│  4 categories >100% = 4 points                                  │
│  5 categories >100% = 5 points                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

PHASE 4: OPTIMIZATION & REPORTING
┌─────────────────────────────────────────────────────────────────┐
│ Step 4.1: GAP ANALYSIS                                          │
│ ├── Current projected points based on specified products        │
│ ├── Which categories are close to 100% threshold                │
│ ├── Which products have lowest MAS scores                       │
│ └── RECOMMENDATION: Specific product swaps to increase points   │
│                                                                 │
│ Step 4.2: SCENARIO MODELING                                     │
│ ├── "If we switch Paint C to a Level 3 product..."             │
│ ├── "If we add HPDs for all flooring products..."              │
│ └── Calculate impact on total points                            │
│                                                                 │
│ Step 4.3: SUBMISSION PACKAGE                                    │
│ ├── Product inventory with MAS scores for all products          │
│ ├── Product category adjusted value calculations                │
│ ├── Evidence compilation (certifications, EPDs, HPDs)           │
│ ├── Points determination summary                                │
│ └── LEED Online formatted submission                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## MAS Scoring Rubric (AI-Implemented)

### Climate Health Scoring

| Level | Evidence Required | AI Verification Method |
|-------|------------------|----------------------|
| **1** | Product has Type III EPD | Query EPD databases; verify ISO 14025 / EN 15804 compliance |
| **2** | EPD demonstrates GWP below industry average | Compare EPD GWP to CLF baseline for same category |
| **3** | EPD demonstrates GWP in top 20% (lowest) of category | Compare to CLF percentile ranking |

### Human Health Scoring

| Level | Evidence Required | AI Verification Method |
|-------|------------------|----------------------|
| **1** | HPD (Basic) available OR meets CDPH low-emitting | Query HPD Repository OR verify MRc3 compliance |
| **2** | HPD with full disclosure (100% ingredients) | Parse HPD — verify "100%" disclosure level |
| **3** | HPD with no Red List chemicals + optimization | Parse HPD ingredient list against ILFI Red List |

### Ecosystem Health Scoring

| Level | Evidence Required | AI Verification Method |
|-------|------------------|----------------------|
| **1** | Sourcing disclosure or FSC certification | Query FSC database; parse manufacturer claims |
| **2** | Certified sustainable sourcing | Verify third-party sustainable sourcing cert |
| **3** | Comprehensive ecosystem impact assessment | EPD with full environmental impacts beyond GWP |

### Social Health & Equity Scoring

| Level | Evidence Required | AI Verification Method |
|-------|------------------|----------------------|
| **1** | Manufacturer CSR or supply chain disclosure | Parse manufacturer website / annual report |
| **2** | Third-party social responsibility certification | Query SA8000, B Corp, or equivalent databases |
| **3** | Comprehensive fair labor + community benefit | Multiple social certifications + local sourcing |

### Circular Economy Scoring

| Level | Evidence Required | AI Verification Method |
|-------|------------------|----------------------|
| **1** | Recycled content disclosure OR recyclability claim | Parse manufacturer documentation |
| **2** | Take-back program OR Cradle to Cradle Certified (Bronze/Silver) | Query C2C database; verify take-back program |
| **3** | Cradle to Cradle Certified (Gold/Platinum) OR comprehensive circular design | Query C2C database at Gold/Platinum level |

---

## Implementation Estimate

| Task | Manual Hours | Automated Hours | Savings |
|------|-------------|----------------|---------|
| Product inventory (reuse MRc3 data) | 0 (shared) | 0 (shared) | **100% reuse** |
| Expanded certification lookup | 20-30 (5-7 min x 200+ products x 5 criteria) | 2-4 (exception review) | **90%** |
| MAS score calculation per product | 8-12 | 0 (fully auto) | **100%** |
| Product category adjusted value calc | 2-4 | 0 (fully auto) | **100%** |
| Points determination | 1-2 | 0 (fully auto) | **100%** |
| Scenario modeling / optimization | 4-6 | 0.5 (review) | **90%** |
| Report writing & evidence assembly | 6-8 | 1-2 (review) | **80%** |
| **TOTAL** | **41-62** | **4-7** | **~90%** |

---

# MRc5: Construction and Demolition Waste Diversion

## Scoring Summary

| Metric | Score |
|--------|-------|
| **Automation Score** | **4/5** |
| **Commercial Value** | **4/5** |
| **Risk Level** | **Low-Medium** |
| **Documentation Type** | C&D Waste Management Plan (template), Final Waste Management Report, Diversion Calculation Spreadsheet, Hauler Documentation |
| **Final Recommendation** | **Automate in MVP** — Hauler Report Parser + Diversion Engine |

---

## Required Inputs vs. AI-Processable Elements

| Input Category | Source | AI Role |
|---------------|--------|---------|
| **Waste management plan** | **AI GENERATED** (template) | Full plan from template + project data |
| **Hauler tickets / weight tickets** | Waste hauler | **FULLY PARSE** — extract weight, material type, destination |
| **Recycler/salvage receipts** | Recycling facilities | **FULLY PARSE** — extract quantities, diversion claims |
| **Facility recycling rate documentation** | Processing facilities | **AUTO-VALIDATE** — check third-party verification |
| **Mixed C&D facility average rates** | Facilities | Lookup; flag if >35% claimed without third-party |
| **Total waste generated** | **AI CALCULATED** | Sum all waste streams |
| **Total diverted** | **AI CALCULATED** | Sum (quantity x diversion rate) per material |
| **Overall diversion %** | **AI CALCULATED** | Total Diverted / Total Generated |
| **Source-separated %** | **AI CALCULATED** | Meet 10% (1 pt) or 25% (2 pt) thresholds |
| **Final waste management report** | **AI GENERATED** | Complete report from parsed data |
| **Photographic evidence** | Site photos | Auto-organize by waste stream |

---

## AI Techniques Applicable

| Technique | Application | Maturity |
|-----------|-------------|----------|
| **Hauler ticket/weight ticket parsing** | Extract tonnage, material type, date, destination from standardized forms | **High** — standard form layouts |
| **Receipt/document parsing** | Extract quantities from recycler/salvage facility receipts | **High** |
| **Waste stream classification** | Auto-classify materials into LEED categories | **High** |
| **Diversion calculation engine** | Apply diversion rates: 100% source-separated, 200% salvage, 35% max unverified mixed | **Very High** — rule-based |
| **C&D waste management plan generation** | Generate plan template from project parameters | **High** |
| **Final report generation** | Compile all data into LEED submission report | **High** |
| **Photo organization** | Auto-sort site photos by waste stream type | **Medium** |
| **Threshold monitoring** | Track progress toward 50% / 75% diversion in real-time | **High** |
| **Exception flagging** | Flag missing hauler tickets, data gaps, threshold risks | **High** |

---

## Automation Blueprint (Score: 4)

### Workflow: C&D Waste Diversion Documentation Engine

```
┌──────────────────────────────────────────────────────────────────┐
│         MRc5: WASTE DIVERSION AUTOMATION PIPELINE                │
│           (Hauler Report Parser + Diversion Engine)              │
└──────────────────────────────────────────────────────────────────┘

PHASE 0: WASTE MANAGEMENT PLAN GENERATION (Pre-Construction)
┌─────────────────────────────────────────────────────────────────┐
│ Step 0.1: Plan Template Generation                             │
│ ├── Input: Project type, size, location, demolition scope      │
│ ├── Input: Estimated waste streams (from material schedule)    │
│ ├── AI Action: Generate complete C&D Waste Management Plan:    │
│ │   ├── Project Information & Waste Stream Characterization    │
│ │   ├── Waste Reduction Goals (target 50% or 75% diversion)    │
│ │   ├── Source Separation Strategy                              │
│ │   ├── Material Recovery & Recycling Procedures               │
│ │   ├── Salvage & Reuse Procedures                              │
│ │   ├── Hazardous Waste Handling                                │
│ │   ├── Roles & Responsibilities (GC, subs, haulers)           │
│ │   ├── Training Requirements                                   │
│ │   ├── Monitoring & Reporting Procedures                      │
│ │   ├── Target Diversion Rates by Material Type                │
│ │   ├── Hauler & Facility Selection Criteria                    │
│ │   └── Record-Keeping Requirements                             │
│ └── Output: Draft C&D Waste Management Plan                     │
│                                                                 │
│ Step 0.2: TARGET SETTING                                       │
│ ├── AI Action: Estimate waste quantities by type from BIM      │
│ ├── AI Action: Identify high-diversion-potential materials     │
│ └── Output: Realistic diversion targets by material            │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: HAULER DATA INTAKE (Construction Phase)
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  INPUT SOURCES (all parsed automatically):                      │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ SOURCE 1: Hauler Weight Tickets                            │  │
│  │ ├── Parse from: PDF scans, digital tickets, photos        │  │
│  │ ├── Extract:                                               │  │
│  │ │   ├── Date                                               │  │
│  │ │   ├── Hauler company name                                │  │
│  │ │   ├── Ticket / load number                               │  │
│  │ │   ├── Material type (concrete, wood, metal, mixed, etc.)│  │
│  │ │   ├── Gross weight / tare weight / net weight            │  │
│  │ │   ├── Destination facility                               │  │
│  │ │   └── Load type (source-separated vs. mixed)             │  │
│  │ └── Store in structured database                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ SOURCE 2: Recycler / Salvage Facility Receipts             │  │
│  │ ├── Parse from: PDF receipts, digital reports              │  │
│  │ ├── Extract:                                               │  │
│  │ │   ├── Facility name & location                           │  │
│  │ │   ├── Material type & quantity received                  │  │
│  │ │   ├── Processing method (recycling, salvage, reuse)      │  │
│  │ │   ├── Facility recycling rate (if mixed C&D)             │  │
│  │ │   └── Third-party verification status                    │  │
│  │ └── Store in structured database                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ SOURCE 3: Manufacturer Take-Back Documentation             │  │
│  │ ├── Parse from: Manufacturer reports, digital records      │  │
│  │ ├── Extract:                                               │  │
│  │ │   ├── Manufacturer name                                  │  │
│  │ │   ├── Material type & quantity                           │  │
│  │ │   └── Take-back program confirmation                     │  │
│  │ └── Store in structured database                            │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ SOURCE 4: Photo Log (Supplemental)                         │  │
│  │ ├── Site photos of waste streams, dumpster types           │  │
│  │ ├── AI Action: Auto-organize by date & waste stream        │  │
│  │ └── Used as supplemental evidence                           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

PHASE 2: DIVERSION RATE CALCULATION ENGINE
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  RULE-BASED DIVERSION RATE ASSIGNMENT:                          │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ DIVERSION TYPE          │ RATE    │ AI ASSIGNMENT LOGIC     ││
│  │─────────────────────────│─────────│─────────────────────────││
│  │ Source-separated →      │ 100%    │ Auto if destination is  ││
│  │ single-material recycler│         │ named recycler          ││
│  │                         │         │                         ││
│  │ Off-site salvage/reuse  │ 100%    │ Auto if receipt from    ││
│  │                         │         │ salvage yard            ││
│  │                         │         │                         ││
│  │ Salvaged materials      │ 200%    │ Auto-flag for special   ││
│  │ (off-site reuse)        │         │ handling; double value  ││
│  │                         │         │                         ││
│  │ Manufacturer take-back  │ 100%    │ Auto if manufacturer    ││
│  │ program                 │         │ program documented      ││
│  │                         │         │                         ││
│  │ Mixed C&D → processing  │ Facility│ Facility rate from      ││
│  │ facility                │ average │ database; if unknown,   ││
│  │                         │ or 35%  │ default to 35%          ││
│  │                         │         │                         ││
│  │ Alternative daily cover │ 0%      │ Auto-flag as disposal   ││
│  │ Incineration/energy     │ 0%      │ Auto-flag as disposal   ││
│  │ recovery                │         │                         ││
│  │                         │         │                         ││
│  │ Hazardous waste         │ EXCLUDE │ Auto-flag for exclusion ││
│  │ On-site reuse           │ EXCLUDE │ Directed to MRc1        ││
│  │ Excavated soil/land     │ EXCLUDE │ Auto-flag for exclusion ││
│  │ clearing                │         │                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  CALCULATIONS:                                                   │
│  ├── Total C&D Waste Generated = SUM(all waste by weight)        │
│  ├── Total Diverted = SUM(Quantity x Diversion Rate)             │
│  ├── Overall Diversion % = (Total Diverted / Total Generated) x 100│
│  ├── Source-Separated Quantity = SUM(source-separated + salvaged) │
│  ├── Source-Separated % of Diverted = Source-Sep / Total Diverted │
│  └── Source-Separated % of Total = Source-Sep / Total Generated   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

PHASE 3: REAL-TIME DASHBOARD & THRESHOLD MONITORING
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  LIVE PROJECT DASHBOARD:                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ OVERALL DIVERSION: 62% ████████████████░░░░░░░░░░  TARGET │ │
│  │                              50%      75%                    │ │
│  │                              [★1pt]  [★2pt]                  │ │
│  │                                                              │ │
│  │ SOURCE-SEPARATED: 18% of total ████░░░░░░░░░░░░░░░        │ │
│  │                              10%     25%                     │ │
│  │                              [★1pt]  [★2pt]                  │ │
│  │                                                              │ │
│  │ MATERIAL BREAKDOWN:                                          │ │
│  │ Concrete:  45 tons  → 95% diverted ████████████░            │ │
│  │ Wood:      32 tons  → 78% diverted ██████████░░░            │ │
│  │ Metal:     18 tons  → 100% diverted █████████████           │ │
│  │ Drywall:   12 tons  → 50% diverted ██████░░░░░░░            │ │
│  │ Mixed:     28 tons  → 35% diverted █████░░░░░░░░            │ │
│  │                                                              │ │
│  │ STATUS: ✅ 1 point achieved; 2 points within reach          │ │
│  │                                                              │ │
│  │ ALERTS:                                                      │ │
│  │ ⚠️ Mixed C&D at 35% (facility unverified) — risk of audit   │ │
│  │ 💡 Increase source separation to reach 2nd point            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  AI-GENERATED RECOMMENDATIONS:                                   │
│  ├── "If you source-separate 10 more tons of drywall, you      │
│  │    will achieve 2 points"                                    │
│  ├── "Consider switching mixed C&D hauler to [Verified Facility]│
│  │    with 65% average recycling rate"                          │
│  └── "Salvaged doors (2 tons) qualify for 200% diversion —     │
│       claim now to boost rate"                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

PHASE 4: FINAL REPORT GENERATION
┌─────────────────────────────────────────────────────────────────┐
│ Step 4.1: FINAL WASTE MANAGEMENT REPORT                        │
│ ├── Auto-generated sections:                                    │
│ │   ├── Project Information                                     │
│ │   ├── C&D Materials Management Plan Summary                   │
│ │   ├── Total Waste Generated (by weight)                       │
│ │   ├── Waste Diversion Summary                                 │
│ │   ├── Waste by Material Type (with diversion rates)           │
│ │   ├── Diversion Strategies Employed                            │
│ │   ├── Facility Documentation                                  │
│ │   ├── Source-Separated Materials Summary                      │
│ │   ├── Salvaged Materials Summary (200% rate)                  │
│ │   ├── Hazardous Waste Handling Summary                        │
│ │   ├── Overall Diversion Percentage Calculation                │
│ │   ├── Points Determination                                    │
│ │   └── Appendices (hauler tickets, receipts, photos)           │
│                                                                 │
│ Step 4.2: CALCULATION SPREADSHEET                              │
│ ├── Line-item waste log with diversion calculations             │
│ ├── Formulas visible and auditable                              │
│ ├── Export to Excel                                             │
│ └── Used as LEED submission evidence                            │
│                                                                 │
│ Step 4.3: DOCUMENT PACKAGE                                     │
│ ├── Compiled hauler tickets (indexed)                           │
│ ├── Recycler/salvage receipts (indexed)                         │
│ ├── Facility recycling rate documentation                       │
│ ├── Third-party verification letters (if applicable)            │
│ ├── Photographic evidence (organized)                           │
│ └── LEED Online formatted submission                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Supported Hauler Report Formats

| Hauler / Service | Report Format | Parser Method | Common Regions |
|-----------------|---------------|--------------|----------------|
| **Waste Management** | PDF weight tickets + portal export | PDF parser + CSV import | Nationwide US |
| **Republic Services** | PDF tickets + online reports | PDF parser + API query | Nationwide US |
| **Allied Waste** | PDF tickets | PDF parser | Regional US |
| **Local/independent haulers** | Various PDF formats | Template-matching + OCR | All regions |
| **LEED waste tracking spreadsheets** | Excel template | Direct import | All regions |
| **SmartWaste / similar tools** | CSV/Excel export | Direct import | UK/EU primarily |
| **Photo of scale tickets** | JPG/PNG | OCR extraction | All regions |

---

## Implementation Estimate

| Task | Manual Hours | Automated Hours | Savings |
|------|-------------|----------------|---------|
| Waste management plan drafting | 4-6 | 1 (review) | **80%** |
| Hauler ticket data entry | 8-16 (200+ tickets) | 1-2 (exception review) | **90%** |
| Diversion calculations | 4-6 | 0 (fully auto) | **100%** |
| Facility recycling rate verification | 2-4 | 0.5 (review) | **80%** |
| Progress tracking & threshold monitoring | 2-4 (ongoing) | 0 (real-time auto) | **100%** |
| Final report generation | 4-6 | 0.5-1 (review) | **85%** |
| Document package assembly | 3-4 | 0.5 (review) | **85%** |
| **TOTAL** | **27-46** | **4-6** | **~87%** |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Hauler ticket OCR errors | Confidence scoring + human review for low-confidence extractions |
| Facility recycling rate claims | Flag unverified rates; require documentation for >35% claims |
| Source-separated threshold tracking | Real-time dashboard alerts project team before project end |
| Missing tickets | Exception report flags gaps; require manual entry for missing data |
| Material misclassification | Standardized waste stream taxonomy with manual override |
| Weight unit inconsistency | Engine enforces consistent units (all weight or all volume) |
| Salvage 200% rate misapplication | Explicit flagging; requires receipt from salvage/reuse facility |

---

# Cross-Credit Integration Architecture

## Shared Data Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    SHARED INPUT LAYER                            │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Material   │  │  Product    │  │   BIM/Revit │             │
│  │  Schedule   │  │  Specs      │  │   Export    │             │
│  │  (Excel)    │  │  (PDF/DOC)  │  │  (IFC/CSV)  │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         └─────────────────┼─────────────────┘                    │
│                           ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │           MATERIAL / PRODUCT DATABASE (Normalized)          ││
│  │  ├── Product ID                                             ││
│  │  ├── Product Name / Manufacturer / Model                    ││
│  │  ├── CSI Division / Category                                ││
│  │  ├── Quantity (cost, weight, area, volume, count)           ││
│  │  ├── LEED MR Category (credits applicable)                  ││
│  │  └── Status (confirmed, pending, excluded)                  ││
│  └────────────────────────┬────────────────────────────────────┘│
│                           │                                      │
│         ┌─────────────────┼─────────────────┐                    │
│         ▼                 ▼                 ▼                    │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │  MRp2/MRc2 │  │    MRc3      │  │    MRc4      │            │
│  │  EPD Data  │  │  Low-Emitting │  │   MAS Scores │            │
│  │  Pipeline  │  │  Compliance   │  │   Engine     │            │
│  └──────┬─────┘  └──────┬───────┘  └──────┬───────┘            │
│         │               │                 │                      │
│         └───────────────┼─────────────────┘                      │
│                         ▼                                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              COMPLIANCE DASHBOARD & REPORTING                ││
│  │  ├── Per-credit status (complete, in-progress, not started) ││
│  │  ├── Points tracking across all MR credits                  ││
│  │  ├── Cross-credit optimization recommendations              ││
│  │  └── Unified submission package for LEED Online             ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Cross-Credit Optimization Opportunities

| Synergy | Credits | Description |
|---------|---------|-------------|
| **Product inventory sharing** | MRc3 + MRc4 | Same product list drives both credits; parse once, use twice |
| **EPD data reuse** | MRp2 + MRc2 + MRc4 | Parsed EPDs feed embodied carbon calcs AND product selection scoring |
| **Low-emitting + Product Selection** | MRc3 + MRc4 | Products meeting MRc3 criteria contribute to MRc4 Human Health scoring |
| **Reuse + Waste Diversion** | MRc1 + MRc5 | Materials reused on-site → MRc1; materials salvaged off-site → MRc5 (at 200%) |
| **Material schedule → All credits** | All MR | Single material takeoff feeds EPD lookup, compliance screening, scoring |
| **Waste plan → Operations plan** | MRc5 + MRp1 | C&D waste experience informs zero waste operations planning |

---

# Summary: Prioritized Implementation Roadmap

## MVP Phase (Immediate — High Impact, Low Risk)

| Priority | Credit | Effort | Impact | Key Deliverable |
|----------|--------|--------|--------|-----------------|
| **1** | **MRc3** (Low-emitting) | Medium | Very High | Compliance engine with certification DB lookup |
| **2** | **MRp2** (Embodied Carbon Quantification) | High | Very High | EPD parser + calculation engine + report generator |
| **3** | **MRc5** (Waste Diversion) | Medium | High | Hauler ticket parser + diversion calculator |
| **4** | **MRc2** (Reduce Embodied Carbon) | High | Very High | Extends MRp2 pipeline with benchmarking + scenario analysis |
| **5** | **MRc4** (Product Selection) | High | Very High | Multi-attribute scoring engine |

## Phase 2 (Later — Good Value, Higher Complexity)

| Priority | Credit | Effort | Impact | Key Deliverable |
|----------|--------|--------|--------|-----------------|
| **6** | **MRp1** (Zero Waste Operations) | Low | Medium | Plan template generator with project parameter injection |
| **7** | **MRc1** (Building/Materials Reuse) | Medium | Medium | Calculation engine + salvage assessment template |

## Phase 3 (Continuous — Enhancement)

| Initiative | Description |
|------------|-------------|
| **WBLCA integration** | API connectors to Tally, One Click LCA for Option 1 assistance |
| **Real-time waste tracking** | IoT scale integration for live diversion dashboard |
| **BIM direct integration** | Revit/ArchiCAD plugins for material data export |
| **Manufacturer API network** | Direct EPD/certification APIs from top 100 manufacturers |
| **Predictive optimization** | ML models to predict optimal material substitutions before procurement |

---

# Final Recommendations Matrix

| Credit | Auto Score | Value | Risk | Recommendation | Timeline | Key Investment |
|--------|-----------|-------|------|----------------|----------|----------------|
| **MRc3** | 5/5 | 4/5 | Low | **Automate in MVP** | Month 1-2 | Certification DB integration |
| **MRp2** | 4/5 | 5/5 | Medium | **Automate in MVP** | Month 1-3 | EPD parser engine |
| **MRc2** | 4/5 | 5/5 | Medium | **Automate in MVP** | Month 2-4 | Extends MRp2 + EC3/CLF APIs |
| **MRc5** | 4/5 | 4/5 | Low-Med | **Automate in MVP** | Month 2-3 | Hauler ticket OCR/parser |
| **MRc4** | 4/5 | 5/5 | Low-Med | **Automate in MVP** | Month 3-5 | Multi-attribute scoring engine |
| **MRp1** | 3/5 | 3/5 | Low | **Automate Later** | Month 4-5 | Plan template library |
| **MRc1** | 3/5 | 3/5 | Medium | **Automate Later** | Month 5-6 | Salvage assessment templates |

---

# ROI Projection

## Time Savings Summary

| Credit | Manual (hrs) | Automated (hrs) | Savings | Projects/Year | Hours Saved/Year |
|--------|-------------|-----------------|---------|---------------|-----------------|
| MRc3 | 44-66 | 3-7 | 92% | 50 | **2,050-2,950** |
| MRp2 | 24-41 | 3-7 | 85% | 50 | **1,050-1,700** |
| MRc2 | 30-49 | 4-6 | 88% | 50 | **1,300-2,150** |
| MRc5 | 27-46 | 4-6 | 87% | 50 | **1,150-2,000** |
| MRc4 | 41-62 | 4-7 | 90% | 50 | **1,850-2,750** |
| MRp1 | 14-22 | 2-3.5 | 85% | 50 | **600-925** |
| MRc1 | 14-24 | 4-8 | 55% | 50 | **500-800** |
| **TOTAL** | **194-310** | **24-44.5** | **~87%** | **50** | **~8,500-13,275** |

## At $150/hr consultant rate: **$1.27M - $1.99M annual value** for 50-project portfolio

---

*Analysis completed. All automation blueprints designed for immediate engineering implementation.*
