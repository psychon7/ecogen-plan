## 5. Recommended MVP Scope

### 5.1 MVP Credit Selection Criteria

#### 5.1.1 Selection framework

MVP credit selection applies a weighted four-dimension framework: **Automation Suitability** (1–5), **Commercial Value** (1–5), **Risk Level** (Low/Medium/High), and **Cross-Credit Synergy** (binary). Credits must score 4+ on both automation and commercial value to qualify for Phase 1. Automation Suitability measures the degree to which AI agents can execute core workflows — data retrieval, calculation, narrative generation, and document compilation. Commercial Value combines consultant time saved per project, applicability across the LEED project portfolio, and role in achieving higher certification levels. Risk Level captures reviewer rejection probability, liability exposure, and third-party data dependency. Cross-Credit Synergy elevates credits whose outputs become inputs for others, creating compounding automation value.[^1^]

Analysis of 43 credits across seven LEED v5 BD+C categories yielded a shortlist of 8 credit specifications (grouped into 5 functional suites) that meet the MVP threshold. These credits cover prerequisites applying to 100% of projects, address up to 28 points of available credit value, and rely primarily on deterministic calculations, public data APIs, and templatable narrative generation — all domains where contemporary AI systems demonstrate high reliability.[^2^]

#### 5.1.2 Final MVP shortlist: 5 suites for Phase 1 launch

The MVP launches five integrated credit suites, each pairing prerequisites with associated credits to exploit natural data dependencies:

**Table 5.1: MVP Credit Suite Summary**

| Suite | Credits | Auto Score | Value | Risk | Est. Time Saved/Project |
|-------|---------|-----------:|------:|------:|------------------------:|
| Water Efficiency | WEp2 + WEc2 | 5 / 5 | 5 / 5 | Low | 17–27 hrs |
| Integrative Process | IPp1 + IPp2 | 4 / 5 | 5 / 5 | Medium | 20–28 hrs |
| Low-Emitting Materials | MRc3 | 5 / 5 | 4 / 5 | Low | 37–59 hrs |
| Indoor Environmental Quality | EQp1 + EQp2 | 4 / 5 | 4–5 / 5 | Low-Med | 12–22 hrs |
| Refrigerant Management | EAp5 + EAc7 | 4–5 / 5 | 4 / 5 | Low | 8–16 hrs |

Total addressable time savings across all five suites ranges from **94 to 152 consultant-hours per project**. At a blended consulting rate of \$150 per hour, a single platform subscription pays for itself within the first one to two projects.[^3^] The selection prioritizes prerequisites (WEp2, EQp1, EQp2, EAp5) because they apply to every project — no consultant can opt out. Credits scoring 5/5 on automation (WEc2, MRc3, EAc7) require minimal human review and deliver predictable, auditable outputs.[^4^]

### 5.2 MVP Credit 1: WEp2 + WEc2 Water Efficiency Suite

#### 5.2.1 User input form

The Water Efficiency Suite uses a structured intake designed to minimize friction while capturing all variables for the calculation engine.[^5^]

**Table 5.2: WEp2/WEc2 User Input Form**

| Field | Type | Required | Source |
|-------|------|----------|--------|
| Project address | Geocoded text | Yes | Auto-climate zone detect |
| Building type | Dropdown (12 types) | Yes | User selection |
| Occupancy — FTE count | Integer | Yes | User entry or import |
| Occupancy — transient count | Integer | Yes | User entry or import |
| Gender ratio | Slider (0–100%) | Yes | Default 50% |
| Operating days/year | Integer | Yes | Default 260 |
| Fixture schedule upload | CSV / Excel / PDF | Yes | Uploaded schedule |
| Cut sheet upload (optional) | PDF bundle | No | Manufacturer docs |
| Irrigation area (sq ft) | Float | If applicable | User entry |
| Cooling tower present | Boolean | Yes | User toggle |
| Alternative water sources | Multi-select | No | Rainwater / greywater / reclaimed |

The fixture schedule parser accepts three modalities: structured CSV/Excel with columns for fixture type, manufacturer, model, quantity, and flow rate; PDF plumbing schedules via OCR table extraction; or manual web form entry with auto-suggest for common models. All inputs normalize into a unified fixture database keyed by type.[^6^]

#### 5.2.2 AI agents

**Agent 1 — Fixture Parser.** Extracts fixture data from schedules, performs OCR on cut sheets for certified flow/flush rates, and cross-references against the EPA WaterSense database. Outputs a normalized fixture database.[^7^]

**Agent 2 — Occupancy Profiler.** Applies LEED-default usage patterns by building type (toilets at 1 flush/FTE/day, urinals at 2 uses/male/day, lavatories at 3 minutes/use) and generates an annual usage matrix.[^8^]

**Agent 3 — Baseline Calculator.** Applies LEED v5 Table 2 baseline rates (toilet 1.6 GPF, urinal 1.0 GPF, public lavatory 0.50 GPM, private lavatory 2.2 GPM, kitchen faucet 2.2 GPM, showerhead 2.5 GPM) and computes total annual baseline consumption.[^9^]

**Agent 4 — Proposed Calculator.** Applies actual fixture flow rates and computes percentage reduction: $\text{\% Reduction} = (\text{Baseline} - \text{Proposed}) / \text{Baseline} \times 100\%$.[^10^]

**Agent 5 — Multi-Option Optimizer (WEc2).** Evaluates all six WEc2 options simultaneously — whole-project reduction (1–8 points), fixture reduction (1–3 points), appliance compliance (1–2 points), outdoor water use (1–2 points), cooling tower optimization (1–2 points), and water reuse (1–2 points) — recommending the optimal combination.[^11^]

**Agent 6 — Document Compiler.** Populates LEED Online forms, generates fixture compliance tables with flags, compiles cut sheet indices, and produces irrigation pathway narratives.[^12^]

#### 5.2.3 Generated outputs and QA

The suite produces six deliverables: (1) a complete WEp2 submission package; (2) a WEc2 multi-option analysis with point recommendations; (3) auto-populated LEED Online forms; (4) a fixture compliance matrix; (5) a cross-credit data feed to WEc1; and (6) an upgrade recommendations report showing the cheapest fixture substitutions per point gained.[^13^]

QA operates at three levels. Level 1 (automated) validates calculations against LEED v5 reference examples, checks unit consistency, and flags flow rates outside expected ranges. Level 2 (AI-assisted) identifies low-confidence OCR extractions and ambiguous classifications for human review. Level 3 (professional) requires licensed engineer or LEED AP sign-off before USGBC submission.[^14^]

#### 5.2.4 Time saved and pricing

Manual WEp2 requires 8–12 hours; WEc2 adds 12–20 hours. The automated pipeline reduces combined effort to 3–5 hours of review — savings of 17–27 hours per project.[^15^]

**Table 5.3: WEp2 + WEc2 Commercial Model**

| Metric | Value |
|--------|-------|
| Consultant time saved | 17–27 hrs/project |
| Value at \$150/hr | \$2,550–\$4,050 |
| Platform price point (annual) | \$4,800–\$7,200 |
| Payback period | 1.2–2.8 projects |
| Applicability | 100% of LEED projects |
| Credit points covered | Prerequisite + up to 8 pts |

The suite justifies a premium tier because WEp2 is mandatory — no LEED project can proceed without compliance. The WEc2 optimizer provides a clear ROI narrative: every point gained represents avoided design changes downstream.[^16^]

### 5.3 MVP Credit 2: IPp1 + IPp2 Assessment Suite

#### 5.3.1 User input form

The Integrative Process Suite generates two prerequisite reports — Climate Resilience (IPp1) and Human Impact (IPp2) — from a unified intake where most data is retrieved automatically by web research agents.[^17^]

**Table 5.4: IPp1/IPp2 User Input Form**

| Field | Type | Required | Used By |
|-------|------|----------|---------|
| Project address | Geocoded text | Yes | Both |
| Building type and function | Dropdown + text | Yes | Both |
| Projected service life | Integer (years) | Yes | IPp1 |
| Design strategies under consideration | Multi-select + text | Yes | Both |
| Site-specific observations | Text area (500 words) | No | Both |
| Known community issues | Text area | No | IPp2 |
| Sustainability goals | Multi-select | No | Both |

#### 5.3.2 AI agents

**Agent 1 — Climate Data Researcher (IPp1).** Executes parallel queries across FEMA flood zones, NOAA climate projections, USGS seismic/landslide data, state resilience plans, and IPCC AR6 scenarios. Populates hazard tables covering 13+ categories with exposure, sensitivity, adaptive capacity, and risk ratings.[^18^]

**Agent 2 — Demographics Researcher (IPp2).** Queries U.S. Census ACS data, EPA EJScreen environmental justice indicators, CDC Social Vulnerability Index, and local comprehensive plans. Generates four-category demographic profiles.[^19^]

**Agent 3 — Priority Hazard Selector.** Analyzes risk ratings and recommends the top 2–3 priority hazards for detailed analysis; consultant confirms or overrides.[^20^]

**Agent 4 — Narrative Generator.** Drafts all assessment narratives — hazard descriptions, impact analyses, design strategy integration — using structured templates grounded in project-specific data to minimize hallucination.[^21^]

**Agent 5 — Report Compiler.** Assembles the full assessment with executive summary, data tables, priority hazard deep-dives, design integration narrative, and source URL appendices.[^22^]

#### 5.3.3 Generated outputs and QA

IPp1 produces a Climate Resilience Assessment (15–25 pages) with hazard data tables, two priority hazard risk matrices, and design strategy integration. IPp2 produces a Human Impact Assessment (12–20 pages) covering demographics, infrastructure, human use/health, and occupant experience. Both reports include .gov/.edu source citations for reviewer verification.[^23^]

QA emphasizes data provenance: every climate data point carries a source URL, demographic data is tagged with ACS vintage, and consultant review (3–4 hours) is mandatory before submission.[^24^]

#### 5.3.4 Time saved and pricing

IPp1 manually requires 10–20 hours; IPp2 requires 8–16 hours. The automated suite delivers draft reports in under 30 minutes, reducing total effort to 3–4 hours per assessment — a 70–80% reduction for IPp1 and 65–75% for IPp2.[^25^]

**Table 5.5: IPp1 + IPp2 Commercial Model**

| Metric | Value |
|--------|-------|
| Consultant time saved | 20–28 hrs/project |
| Value at \$150/hr | \$3,000–\$4,200 |
| Platform price point (annual) | \$3,600–\$6,000 |
| Payback period | 0.9–2.0 projects |
| Applicability | 100% of NC and C+S projects |
| Credit points covered | 2 prerequisites (required) |

These prerequisites are required for all New Construction and Core & Shell projects. Firms report spending more staff time on IPp1/IPp2 than on any other prerequisites except energy modeling, making this a high-willingness-to-pay feature.[^26^]

### 5.4 MVP Credit 3: MRc3 Low-emitting Materials

#### 5.4.1 User input form

MRc3 evaluates products across nine interior material categories for VOC emissions and content compliance. The input accepts bulk product data via specification document parsing.[^27^]

**Table 5.6: MRc3 User Input Form**

| Field | Type | Required |
|-------|------|----------|
| Specification document upload | PDF / DOCX | Yes (primary) |
| Material schedule upload | CSV / Excel | Yes (alternative) |
| Product submittal upload | PDF bundle | Optional |
| Procurement cost data | CSV | For cost-based calculation |
| Project type | NC / C+S / School / Healthcare | Yes |
| Target path | Path 1 / 2 / 3 / Auto | Yes |

The specification parser scans CSI-formatted documents to extract product names, manufacturers, model numbers, and quantities — then classifies each into LEED categories (paints, adhesives, flooring, walls, ceilings, insulation, furniture, composite wood).[^28^]

#### 5.4.2 AI agents

**Agent 1 — Product Inventory Parser.** Extracts and deduplicates product data from specs, schedules, and submittals. Assigns each product to one of nine LEED categories.[^29^]

**Agent 2 — Certification Database Query Engine.** Queries 10+ databases in parallel per product: UL SPOT (GREENGUARD), SCS Global (FloorScore, Indoor Advantage), CRI (Green Label Plus), Declare (ILFI), Cradle to Cradle, BIFMA level, and CARB/EPA certifier databases. Returns certification status, validity date, and testing protocol version.[^30^]

**Agent 3 — Rule-based Compliance Screener.** Applies three criteria: (1) VOC Emissions — third-party certification against CDPH Standard Method v1.2-2017, lab report verification, or inherently non-emitting classification; (2) Furniture Emissions — BIFMA M7.1-2011(R2021) and e3 compliance; (3) Formaldehyde Emissions — ULEF/NAF certification or structural wood exemptions. Outputs COMPLIANT / NON-COMPLIANT / PENDING per product.[^31^]

**Agent 4 — Percentage Calculator.** Computes category-level compliance by cost, area, volume, or count. Applies path logic: paints ≥90% AND flooring ≥90% AND ceilings ≥90% earns Path 1 (1 point); adding any two of adhesives, walls, insulation, or composite wood at ≥80% earns Path 2 (2 points); adding furniture ≥80% earns Path 3 (2 points).[^32^]

**Agent 5 — Exception Reporter.** Identifies products lacking documentation, flags expired certifications, and recommends specific substitutions to close compliance gaps.[^33^]

#### 5.4.3 Generated outputs and QA

The module produces: (1) a color-coded master compliance table; (2) a category-level percentage summary with points determination; (3) an exception report with actionable recommendations; and (4) a compiled LEED Online submission package with indexed certification evidence.[^34^]

QA employs dual-parser validation for certification data, confidence scoring for product classification with human override for low-confidence assignments, and version tracking for CDPH Standard Method updates.[^35^]

#### 5.4.4 Time saved and pricing

Manual MRc3 documentation requires 44–66 hours per project: 8–12 hours for inventory, 16–24 hours for certification lookups (2–3 minutes × 200–400 products), 8–12 hours for compliance screening, 2–3 hours for calculations, and 4–6 hours each for table creation and document assembly. Automation reduces this to 3–7 hours of review — a **92% time reduction**, the highest in the MVP scope.[^36^]

**Table 5.7: MRc3 Commercial Model**

| Metric | Value |
|--------|-------|
| Consultant time saved | 37–59 hrs/project |
| Value at \$150/hr | \$5,550–\$8,850 |
| Platform price point (annual) | \$6,000–\$9,600 |
| Payback period | 0.7–1.7 projects |
| Applicability | ~90% of LEED projects |
| Credit points covered | 1–2 points |

MRc3 commands the highest per-credit price point because the manual certification lookup process is universally identified by sustainability consultants as the most tedious, repetitive, and error-prone workflow in LEED documentation. Automating it is the single most compelling value proposition for material-heavy projects.[^37^]

### 5.5 MVP Credit 4: EQp1 + EQp2 Quality Plans Suite

#### 5.5.1 User input form

The Indoor Environmental Quality Suite automates the Construction Management Plan (EQp1) and Fundamental Air Quality compliance (EQp2).[^38^]

**Table 5.8: EQp1/EQp2 User Input Form**

| Field | Type | Required | Used By |
|-------|------|----------|---------|
| Project type | Dropdown | Yes | Both |
| Construction duration (months) | Integer | Yes | EQp1 |
| Contractor information | Text | Yes | EQp1 |
| Building footprint (sq ft) | Float | Yes | EQp1 |
| HVAC system type | Dropdown | Yes | Both |
| Filtration specifications | Text + MERV rating | Yes | EQp2 |
| Space schedule upload | CSV / Excel | Yes | EQp2 |
| Zone CFM values | CSV / Excel | Yes | EQp2 |
| Outdoor air quality location | Auto-detected | Yes | EQp2 |
| Absorptive material list | Text area | Yes | EQp1 |
| Smoking area location | Coordinates | Yes | EQp1 |

#### 5.5.2 AI agents

**Agent 1 — Construction Management Plan Generator (EQp1).** Drafts an 8–12 page plan covering all seven required areas: no-smoking policy with 25-foot setback verification, extreme heat protection, HVAC protection with MERV filter sequences, source control for absorptive materials, pathway interruption with barrier specs, housekeeping with HEPA requirements, and construction sequencing. Generates a 50–100 item implementation checklist.[^39^]

**Agent 2 — Outdoor Air Quality Investigator (EQp2).** Queries EPA AirNow for attainment status, identifies local pollutant sources, and drafts the investigation narrative referencing ASHRAE 62.1-2022 Sections 4.1–4.3.[^40^]

**Agent 3 — ASHRAE 62.1 Calculator (EQp2).** Performs the Ventilation Rate Procedure: $V_{bz} = R_p \times P_z + R_a \times A_z$ per zone, applies zone air distribution effectiveness $E_z$ from Table 6-2, and sums to system-level outdoor air intake rates. Verifies filtration compliance against MERV 13 / ePM1 50% thresholds.[^41^]

**Agent 4 — Package Assembler.** Compiles the management plan, VRP spreadsheet, filtration compliance table, air quality narrative, and entryway system spec into unified submission packages.[^42^]

#### 5.5.3 Generated outputs and QA

EQp1 outputs include the complete construction management plan, smoking area distance verification with graphic annotation, and field documentation templates. EQp2 outputs include the VRP calculation spreadsheet, filtration compliance table, outdoor air quality investigation narrative, and OA measurement device compliance list.[^43^]

QA verifies EQp1 plan completeness across all seven required sections with cross-referencing to EQp2 for filtration consistency. The EQp2 calculation engine is unit-tested against all ASHRAE 62.1-2022 reference examples. Healthcare and residential projects trigger automatic addenda for ASHRAE 170-2021 and ASHRAE 62.2-2022 respectively.[^44^]

#### 5.5.4 Time saved and pricing

EQp1 manually requires 6–10 hours; EQp2 requires 10–16 hours. Automation reduces combined effort to 3–4 hours of review — savings of 12–22 hours per project.[^45^]

**Table 5.9: EQp1 + EQp2 Commercial Model**

| Metric | Value |
|--------|-------|
| Consultant time saved | 12–22 hrs/project |
| Value at \$150/hr | \$1,800–\$3,300 |
| Platform price point (annual) | \$3,600–\$5,400 |
| Payback period | 1.1–3.0 projects |
| Applicability | 100% of LEED projects |
| Credit points covered | 2 prerequisites (required) |

The ASHRAE 62.1 calculation engine represents significant differentiation — no existing LEED automation tool offers automated VRP computation with live ASHRAE table lookups. The construction management plan generator also serves general contractor coordination, extending value beyond the sustainability team.[^46^]

### 5.6 MVP Credit 5: EAp5 + EAc7 Refrigerant Management

#### 5.6.1 User input form

The Refrigerant Management Suite combines the Fundamental Refrigerant Management prerequisite (EAp5) with Enhanced Refrigerant Management (EAc7) through a shared refrigerant inventory database.[^47^]

**Table 5.10: EAp5/EAc7 User Input Form**

| Field | Type | Required |
|-------|------|----------|
| Equipment schedule upload | CSV / Excel / PDF | Yes |
| Refrigerant equipment list | CSV (alternative) | If no schedule |
| Building type | Dropdown | Yes |
| Food retailing area (% of gross) | Float | Yes (for GreenChill) |
| Self-contained vs. field-piped status | Boolean per unit | Yes (EAc7) |
| Equipment location per unit | Text | Yes (for tCO₂e) |

The equipment schedule parser extracts refrigerant type, charge per unit, quantity, and equipment category from standard MEP schedules.[^48^]

#### 5.6.2 AI agents

**Agent 1 — Equipment Schedule Parser.** Ingests PDF, Excel, or Revit exports; extracts equipment ID, type, manufacturer, model, refrigerant type, charge per unit, quantity, and installation type.[^49^]

**Agent 2 — GWP Database Engine.** Matches refrigerant types against a version-controlled database of 200+ entries with IPCC AR6 values: R-410A (2,088), R-134a (1,430), R-32 (675), R-513A (573), R-454B (466), R-1234yf (<1). Flags HCFC refrigerants as banned in new equipment.[^50^]

**Agent 3 — Inventory Calculator (EAp5).** Computes per-equipment and project total GWP, average GWP per pound, and generates the HCFC-free certification statement. Flags equipment requiring alternative evaluation (GWP >700).[^51^]

**Agent 4 — Weighted GWP Analyzer (EAc7).** Calculates $\text{Weighted GWP} = \sum(\text{GWP}_i \times \text{Charge}_i) / \sum(\text{Charge}_i)$ per category and compares against benchmarks: HVAC (1,400), Data Centers (700), Process Refrigeration (300). Points: ≤80% = 1 point; ≤50% = 2 points.[^52^]

**Agent 5 — Leakage Plan Generator (EAc7).** Computes tCO₂e per space, verifies ≥80% of total GWP is in self-contained equipment, and generates the complete leakage minimization plan with pressure check intervals by tCO₂e tier.[^53^]

**Agent 6 — GreenChill Assessor.** Eligibility triggers at >20% food retailing area; generates certification pathway documentation.[^54^]

#### 5.6.3 Generated outputs and QA

EAp5 outputs include the refrigerant inventory table, HCFC compliance report, and alternative evaluation template. EAc7 outputs include the weighted GWP report, benchmark comparison, leakage minimization plan, and GreenChill pathway. All GWP values carry IPCC AR6 source attribution; weighted calculations display full formulas. Cross-credit consistency is enforced through automatic EAp5-to-EAc7 data import.[^55^]

#### 5.6.4 Time saved and pricing

EAp5 manually requires 4–8 hours; EAc7 requires 6–12 hours. The integrated suite reduces both to 30–60 minutes of review — a **90% time reduction** each, plus elimination of manual data transfer between the two credits.[^56^]

**Table 5.11: EAp5 + EAc7 Commercial Model**

| Metric | Value |
|--------|-------|
| Consultant time saved | 8–16 hrs/project |
| Value at \$150/hr | \$1,200–\$2,400 |
| Platform price point (annual) | \$2,400–\$4,800 |
| Payback period | 1.0–4.0 projects |
| Applicability | 100% of projects with refrigeration |
| Credit points covered | Prerequisite + up to 2 pts |

The GWP calculation engine is foundational infrastructure enabling future refrigerant-related features — SNAP program compliance tracking and EPA Section 608 reporting — creating a natural expansion path despite the lower standalone price point.[^57^]

### 5.7 MVP Implementation Roadmap

#### 5.7.1 Phase 1 (Months 1–3)

Phase 1 targets the three prerequisite-heavy suites applying to 100% of projects: Water Efficiency (WEp2/WEc2), Refrigerant Management (EAp5/EAc7), and Indoor Environmental Quality (EQp1/EQp2). Development begins with shared infrastructure — document parsing engines, calculation frameworks, and the GWP/refrigerant databases — that all subsequent credits depend upon. A team of 4–5 engineers (2 backend, 1 ML, 1 frontend, 1 QA) can deliver this scope within 12 weeks.[^58^]

#### 5.7.2 Phase 2 (Months 3–5)

Phase 2 introduces the assessment-heavy suites: Integrative Process (IPp1/IPp2) and Low-Emitting Materials (MRc3). These require more sophisticated NLP — web research agents querying 10+ government databases for IPp1/IPp2, and a multi-database certification query engine for MRc3. The team expands to 5–6 engineers with an NLP specialist and data engineer.[^59^]

Key milestones include: (1) parallel web research agents for FEMA, NOAA, USGS, Census, EPA EJScreen, and CDC SVI; (2) MRc3 certification database engine with cached fallback for rate-limited APIs; and (3) inherently non-emitting classification with conservative decision rules.[^60^]

#### 5.7.3 Phase 3 (Months 5–8)

Phase 3 focuses on integration. The cross-credit data pipeline enables WEp2 outputs to flow into WEc2 and WEc1, and EAp5 inventory data into EAc7 calculations. The professional review workflow adds mandatory sign-off gates tracking reviewer identity, timestamp, and approval status. Beta testing with 5–10 design firms begins in Month 6; feedback drives UI refinements and edge-case handling.[^61^]

**Table 5.12: MVP Implementation Roadmap**

| Phase | Timeline | Deliverables | Team | Key Dependencies |
|-------|----------|-------------|------|-----------------|
| Phase 1 | Months 1–3 | WEp2/WEc2 calc engine + UI; EAp5/EAc7 GWP DB + parser; EQp1 plan gen + EQp2 ASHRAE 62.1 calc | 4–5 engineers | GREENGUARD/SCS APIs; EPA AirNow; NOAA/FEMA |
| Phase 2 | Months 3–5 | IPp1/IPp2 web research + narrative gen; MRc3 product parser + compliance engine | 5–6 engineers | Census API; EC3/CLF APIs; cert DB rate limits |
| Phase 3 | Months 5–8 | Cross-credit data pipeline; review workflow; LEED Online export; beta testing | 4 engineers | USGBC API; customer beta feedback |
| Launch | Month 8+ | 5 suites live; tiered pricing; onboarding; support | 3–4 + success | 3–5 paying beta customers |

#### 5.7.4 Commercial model

The platform uses a **per-suite subscription** with three tiers. Starter includes any one suite at \$3,600–\$4,800 annually for boutique consultancies (5–15 projects/year). Professional includes all five suites at \$9,600–\$14,400 for mid-size firms (20–50 projects). Enterprise adds custom integrations, API access, and volume pricing for 50+ projects.[^62^]

At 50 paying customers (blend of tiers), annual recurring revenue ranges from \$480,000 to \$720,000. The addressable market — approximately 2,500 LEED consultancies in North America — supports a path to \$2–4 million ARR at 15–25% market penetration within three years.[^63^]

