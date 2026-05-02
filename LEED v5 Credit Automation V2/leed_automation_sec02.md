## 2. Top Credits For Full Automation

The automation matrix in Chapter 1 identified eight credits scoring 4 or 5 on automation potential, applicable to nearly all project types, and drawing primarily on structured data, public APIs, or templated documents. This chapter presents a detailed product blueprint for each, organized to answer what a product manager or engineering lead asks when building the feature: what goes in, what happens inside, what comes out, what must a human still review, and how complex the build is.

The eight credits span six LEED categories: Integrative Process (IPp1, IPp2, IPc2), Water Efficiency (WEp2, WEc2), Indoor Environmental Quality (EQp1, EQp2), Materials and Resources (MRc3), Location and Transportation (LTc3), and Energy and Atmosphere (EAc7, EAp5). Together they cover prerequisites required on every project and credits worth up to 28 points. The unifying pattern is deterministic logic: given a defined set of inputs, the compliance calculation or document structure is known in advance. There is no design creativity, site fieldwork, or stakeholder negotiation required to produce the core deliverable.

---

### 2.1 IPp1 Climate Resilience Assessment

**Automation rationale.** IPp1 requires a structured hazard assessment covering 13+ natural hazard categories, with deep-dive analysis on the two highest-priority hazards. Every data element—FEMA flood zones, USGS seismic ratings, NOAA climate projections, IPCC emission scenarios, wildfire risk maps, drought indices—resides in publicly accessible government databases with API or bulk-download interfaces. The consultant's traditional 10–20 hours per project are spent searching these sources, transcribing data into tables, and writing explanatory text. This workflow—structured data retrieval followed by narrative synthesis—is precisely what LLMs with web-research tool access automate most effectively.

**Required consultant inputs.** Project street address, building type and function (e.g., speculative office, acute-care hospital), projected service life (typically 50–100 years), design strategies under consideration, and any site-specific microclimate observations. These inputs require under 10 minutes of consultant time.

**Data sources and APIs.** FEMA National Flood Hazard Layer REST API for flood zone classification; USGS seismic hazard data and 3D Elevation Program DEM for slope/landslide analysis; NOAA Climate Explorer and Sea Level Rise Viewer for temperature, precipitation, and sea-level projections; NOAA Storm Events Database for historical hurricane, hail, and winter storm frequency; IPCC AR6 Interactive Atlas for regional emission scenarios (SSP1-2.6 through SSP5-8.5); National Interagency Fire Center data for wildfire probability; state and municipal climate resilience plans for jurisdiction-specific guidance.

**AI workflow.** *Step 1—Intake:* geocode address to lat/lon, identify county, census tract, and FEMA region. *Step 2—Parallel data retrieval:* four agent threads query flood/hurricane/sea-level (FEMA/NOAA), landslide/seismic/volcanic (USGS/state geological surveys), extreme heat/cold and IPCC scenarios (Climate.gov), and local adaptation plans. *Step 3—Table population:* fill structured compliance tables for each of 13+ hazard categories with level, risk rating, exposure score, sensitivity score, adaptive capacity, and vulnerability rating per the LEED v5 format. *Step 4—Priority selection:* AI ranks hazards by composite vulnerability score and recommends the top two for deep-dive analysis; consultant confirms or overrides. *Step 5—Deep-dive analysis:* for each selected hazard, generate IPCC scenario selection with justification, service-life projections, operational and construction-phase impact assessment, and mitigation strategy recommendations. *Step 6—Design integration:* AI connects assessment findings to each proposed strategy with specific performance references. *Step 7—Report compilation:* assemble full report with executive summary, tables, deep-dives, integration narrative, and appendices listing every source URL. *Step 8—Consultant review:* validate AI-sourced data against local knowledge.

**Generated outputs.** Complete Climate Resilience Assessment report (PDF/DOCX) with all required tables, priority-hazard deep-dive narratives, design integration section, and cited source URLs. Generation time: 5–8 minutes after data retrieval.

**Validation logic.** System uses only .gov and .edu sources; every claim carries a source URL. Risk ratings are computed through a standardized matrix, not LLM inference. Values outside expected regional ranges trigger human-review flags.

**Human review required.** Consultant confirmation of priority hazard selection; review of AI-sourced data against local knowledge; final sign-off. ~3–4 hours versus 15 hours manual research and writing.

**MVP complexity: Medium.** Primary engineering effort is the multi-source web-research agent layer and structured table population engine. LLM narrative generation is a commodity capability. No proprietary data licensing required.

**Productization notes.** Cache retrieved hazard data at the county level so subsequent projects in the same geography reuse baseline data, reducing API costs and generation time by an estimated 60% for multi-project portfolios.

---

### 2.2 IPp2 Human Impact Assessment

**Automation rationale.** IPp2 requires a four-category assessment: demographics, infrastructure and land use, human health and environmental impacts, and occupant experience. The first three categories draw entirely on public APIs—the U.S. Census American Community Survey, EPA EJScreen, CDC Social Vulnerability Index, HUD Fair Market Rents, and local comprehensive plans. Only the fourth category requires project-specific design information. The manual burden of 8–16 hours per project is spent on data lookup and narrative writing that an automated pipeline eliminates.

**Required consultant inputs.** Project address, building type and intended use, site-specific neighborhood context (optional), known community issues, and design strategies under consideration.

**Data sources and APIs.** U.S. Census Bureau ACS 5-year API for demographics (race, age, income, education, employment, housing density); EPA EJScreen API for environmental justice indicators; CDC SVI database for social vulnerability metrics; HUD Fair Market Rents API for housing affordability; Walk Score API for walkability; Google Maps/Places API for proximity to social services, healthcare, schools, and parks; Bureau of Labor Statistics for local employment data.

**AI workflow.** *Step 1—Intake:* address and building type entry. *Step 2—Demographics (parallel agents):* Census data for race/ethnicity, age, income, education, employment, and density within 0.5-mile radius; EJScreen environmental justice indicators; CDC SVI data. *Step 3—Infrastructure (parallel):* municipal comprehensive plan retrieval, transportation network analysis, zoning classification mapping. *Step 4—Health impacts (parallel):* HUD affordability data, social services proximity mapping, workforce statistics. *Step 5—Occupant experience:* daylight access, views, and air/water quality analysis via EPA AirNow and NOAA climate data. *Step 6—Narrative generation:* four category narratives with inline citations, constrained to retrieved data only—no speculative community characterization. *Step 7—Design integration:* connect assessment findings to proposed strategies. *Step 8—Compilation and review.*

**Generated outputs.** Complete Human Impact Assessment report with four category narratives, demographic data tables, infrastructure analysis, health impact evaluation, and full source citations.

**Validation logic.** All demographic data carries the ACS vintage year. Census data is flagged if the project area spans multiple block groups with divergent characteristics. EJScreen and SVI values include percentile rankings for context.

**Human review required.** Consultant review for local context nuance; confirmation that demographic data vintage is acceptable. ~3–4 hours versus 12 hours manual.

**MVP complexity: Medium.** Comparable to IPp1. Primary effort is Census API integration and ACS data parsing. Narrative templates are simpler than IPp1 because the four-category structure is more predictable.

**Productization notes.** Prefer direct Census API integration over web-scraping for reliability. Flag data age prominently—ACS data lags 2–3 years, which reviewers occasionally question.

---

### 2.3 IPc2 Green Leases

**Automation rationale.** IPc2 offers up to 6–7 points for Core and Shell projects and requires a legal document incorporating 18 best-practice lease clauses across energy, water, IAQ, and thermal comfort, plus compliance clauses for 9 required tenant prerequisites. Every clause maps to a specific LEED prerequisite or credit; scoring is deterministic based on the number of best practices selected. A consultant typically spends 20–30 hours drafting and negotiating this document; automation reduces this to 3–5 hours of selection and legal review.

**Required consultant inputs.** Base building LEED attempted credits list; tenant space types and square footages; owner requirements for specific clauses; building-specific energy and water metering details; ENERGY STAR score if applicable; project team contact information. Consultant may override AI-recommended selections.

**Data sources.** LEED v5 reference guide accessed via RAG pipeline for exact requirement text; Green Lease Leaders program requirements for Option 3; ENERGY STAR Portfolio Manager data for energy disclosure clauses.

**AI workflow.** *Step 1—Best practice selection:* AI presents all 18 best practices with plain-language descriptions; consultant selects or accepts AI recommendations based on building type; AI auto-calculates projected points. *Step 2—Required prerequisite clauses (auto-generated):* generate compliance clauses for all 9 required tenant prerequisites—IPp1 Climate Resilience, IPp2 Human Impact, IPp3 Carbon Assessment, WEp2 Minimum Water, EAp2 Minimum Energy, EAp3 Commissioning, EAp4 Metering, MRp1 Zero Waste, and EQp2 Air Quality—using RAG retrieval of exact LEED v5 language. *Step 3—Best practice clause generation:* for each selected practice (energy 1–11, water 12–15, IAQ 16, thermal comfort 17, innovation 18), generate an appropriate lease clause with project-specific placeholders. *Step 4—Owner-fit-out sections:* generate clauses for any owner-performed fit-out work. *Step 5—Document assembly:* compile full lease with cover, TOC, prerequisite section, best practices, fit-out, commitment language, and signatures. *Step 6—Supporting docs:* best-practice count summary, points calculation, commitment template. *Step 7—Legal review.*

**Generated outputs.** Standard green lease document (DOCX) with compliance checklist, scoring table, prerequisite clause index, and supporting commitment documentation.

**Validation logic.** RAG over the LEED v5 reference guide ensures every clause references correct requirement text. The scoring engine maps selected best practices to point values per the published table. A clause without a matching prerequisite triggers an error flag.

**Human review required.** Legal counsel review of all generated clauses (mandatory); consultant verification of project-specific parameters; owner approval of commitment language. ~3–5 hours versus 20–30 hours manual.

**MVP complexity: Medium.** The RAG pipeline over LEED reference material is the critical engineering investment. Lease clause generation requires careful prompt engineering. The scoring calculator is trivial.

**Productization notes.** Include a mandatory legal-review workflow gate. The AI generates draft language only; final legal liability rests with the project team's counsel. Build clause version control for iteration tracking during legal review.

---

### 2.4 WEp2 Minimum Water Efficiency and WEc2 Enhanced Water Efficiency

**Automation rationale.** WEp2 and WEc2 form a unified calculation pipeline. WEp2 is a prerequisite requiring ≥20% water use reduction below baseline; WEc2 offers up to 8 points for deeper reductions through six independent options. Both rely on the same core calculation: baseline consumption per LEED Table 2 versus proposed fixture flow/flush rates, multiplied by usage profiles derived from building occupancy. The entire calculation is arithmetic on structured data. Traditional workflow: 8–12 hours for WEp2, 12–20 hours for WEc2.

**Required consultant inputs.** Fixture schedule (uploaded Excel, CSV, or PDF) listing fixture type, manufacturer, model, quantity, and flow/flush rate; occupancy data (FTE count, transient count, gender ratio, operating days); building type; irrigation data if applicable; equipment schedules for WEc2 Options 3 and 5.

**Data sources.** EPA WaterSense product database for fixture certification; ENERGY STAR product database for appliance compliance; NOAA climate data for evapotranspiration calculations; local utility water quality data for cooling tower cycle calculations.

**AI workflow—unified nine-step pipeline.** *Step 1—Fixture extraction:* parse schedules via structured upload, OCR from PDF, or cut-sheet parsing into a normalized fixture database. *Step 2—Occupancy profile:* apply LEED-default usage patterns per fixture type to generate annual uses. *Step 3—Baseline calculation:* apply Table 2 rates (toilet 1.6 gpf, urinal 1.0 gpf, public lavatory 0.50 gpm, private lavatory 2.2 gpm, kitchen faucet 2.2 gpm, showerhead 2.5 gpm). *Step 4—Proposed calculation:* apply actual fixture rates from the schedule. *Step 5—Reduction check:* % Reduction = (Baseline − Proposed) / Baseline × 100; compare to thresholds (WEp2 ≥20%; WEc2 30%/35%/40% for 1/2/3 points). *Step 6—Equipment check:* parse against Tables 3–6 for ENERGY STAR labels, prerinse spray valves, commercial kitchen equipment, and cooling tower specifications. *Step 7—Irrigation:* generate no-irrigation narrative or calculate total irrigation requirement baseline per EPA methodology. *Step 8—WEc2 optimization:* evaluate all six options simultaneously, calculate achievable points, recommend optimal combination. *Step 9—Documentation:* populate LEED credit forms, generate fixture compliance matrix, equipment cut sheet index with flags, irrigation narrative, and submission package.

**Generated outputs.** Water use baseline table, reduction calculation worksheet, fixture and equipment compliance matrices, irrigation narrative, WEc2 option optimization report, and fully populated LEED credit forms.

**Validation logic.** Fixture rates cross-referenced against EPA WaterSense. Baseline rates version-locked to LEED v5 Table 2. Reduction percentages outside 0–80% trigger range flags. Formulas exposed and auditable.

**Human review required.** Verify fixture schedule completeness; confirm occupancy assumptions; review irrigation data if applicable. ~1–2 hours for WEp2, 2–3 hours for WEc2.

**MVP complexity: Medium.** Fixture extraction engine (OCR + structured parsing) is highest-engineering. Calculation engine is straightforward. Design WEp2→WEc2 as a shared pipeline from the start.

**Productization notes.** This is the highest-ROI Water Efficiency automation—100% project applicability with prerequisite status meaning failure is not an option. Build the calculation engine first; add OCR as Phase 2 with manual entry as MVP fallback.

---

### 2.5 EQp1 Construction Management and EQp2 Fundamental Air Quality

**Automation rationale.** Both credits produce templated plans with well-defined requirement sets. EQp1 requires a seven-section Construction Management Plan covering no-smoking policy, extreme heat protection, HVAC protection, source control, pathway interruption, housekeeping, and scheduling. EQp2 requires an IAQ Management Plan with outdoor air quality investigation, ASHRAE 62.1 ventilation design, filtration compliance, and entryway system documentation. Neither requires engineering creativity—only parameter substitution into established templates. Manual drafting: 6–10 hours for EQp1, 10–16 hours for EQp2.

**Required consultant inputs.** EQp1: project type, construction duration, contractor name, building footprint, absorptive material list, HVAC type, MERV filter specification. EQp2: HVAC zone schedule (room, type, area, occupant density, CFM), space schedule, filtration specs (MERV rating, ISO 16890 class), building location and type for ASHRAE table lookups.

**Data sources.** ASHRAE 62.1-2022 ventilation rate tables ($R_p$ and $R_a$); EPA AirNow API for local air quality; ASHRAE 52.2-2017 filtration standard; ASHRAE 62.2-2022 for residential; ASHRAE 170-2021 for healthcare.

**AI workflow—EQp1.** *Step 1—Intake:* project context entry. *Step 2—Plan generation (LLM with seven-section template):* Section 1 no-smoking policy with ≥25-ft distance verification; Section 2 extreme heat protection with rest/shade protocols; Section 3 HVAC protection with filter installation sequence; Section 4 source control for material storage; Section 5 pathway interruption with barrier specifications; Section 6 housekeeping with HEPA vacuum specs; Section 7 scheduling with construction sequencing. *Step 3—Checklist generation:* 50–100 implementation items with responsible parties and phase-based due dates. *Step 4—Assembly.*

**AI workflow—EQp2.** *Step 1—Intake.* *Step 2—Outdoor air quality:* query EPA AirNow, identify attainment status, draft narrative per ASHRAE 62.1 Sections 4.1–4.3. *Step 3—VRP calculation:* for each zone, look up $R_p$ and $R_a$ from Table 6-1, compute $V_{bz} = R_p \\times P_z + R_a \\times A_z$, apply $E_z$ from Table 6-2, sum to system $V_{oz}$. *Step 4—Filtration verification:* check MERV 13 / ePM1 50% / ASHRAE 241 compliance. *Step 5—Measurement device check:* flag systems >1,000 cfm OA. *Step 6—Entryway documentation.* *Step 7—Project-type overrides:* healthcare (ASHRAE 170), residential (ASHRAE 62.2). *Step 8—Assembly.*

**Generated outputs.** EQp1: 8–12 page Construction Management Plan, implementation checklist, photo log templates. EQp2: VRP calculation spreadsheet, filtration compliance table, outdoor air quality narrative, IAQ Management Plan.

**Validation logic.** EQp1: seven-section structure validated against LEED v5 checklist; smoking area distance verified numerically. EQp2: ASHRAE tables version-locked; VRP unit-tested against published examples; filtration checked against EPA-verified database.

**Human review required.** Contractor sign-off on EQp1; energy engineer review of VRP calculations; LEED AP final sign-off. ~1 hour EQp1, 2–3 hours EQp2.

**MVP complexity: Low (EQp1); High (EQp2).** EQp1 is almost entirely LLM template filling. EQp2 requires embedding full ASHRAE 62.1 tables and multi-standard cross-referencing. Build EQp1 first for quick ROI.

**Productization notes.** The ASHRAE 62.1 engine in EQp2 feeds directly into EQc1 and EQc2, making it shared infrastructure worth investing in early.

---

### 2.6 MRc3 Low-emitting Materials

**Automation rationale.** MRc3 is a pure rule-based compliance engine. Products in nine categories are screened against explicit thresholds: CDPH Standard Method v1.2-2017 Table 4-1 VOC limits, ANSI/BIFMA M7.1/e3 furniture standards, and CARB/EPA TSCA Title VI formaldehyde limits. A product either meets the threshold or it does not. Manual burden—44–66 hours for 200–400 products—comes from certification database lookups. Automation eliminates this entirely.

**Required consultant inputs.** Product list with manufacturer and model data (uploaded); submittal PDFs with certification evidence; cost, area, or count values per product; project type (NC or C+S) for path determination.

**Data sources.** UL SPOT database (GREENGUARD); SCS Global Services (FloorScore, Indoor Advantage); Carpet and Rug Institute (Green Label Plus); Declare database; Cradle to Cradle registry; EPA TSCA Title VI database; BIFMA level registry; manufacturer CDPH test reports.

**AI workflow.** *Phase 1—Import:* parse product data from specs, submittals, or schedules; classify into nine LEED categories; apply inherently non-emitting rules (ceramic tile, glass, metal, cured concrete). *Phase 2—Database query:* for each product, query all relevant certification databases; verify certification validity date, CDPH method version, and test scenario. For uploaded test reports, parse to extract test date, method version, and measured VOC values against Table 4-1. *Phase 3—Compliance screening:* apply three criteria—VOC emissions (certification, test report, or inherently non-emitting), furniture emissions (BIFMA M7.1/e3), formaldehyde (ULEF, NAF, or structural exemption). Calculate compliant percentage per category. *Phase 4—Path determination:* NC Path 1 (paints/flooring/ceilings >90%) = 1 point; Path 2 (+ two of adhesives/walls/insulation/composite wood >80%) = 2 points; Path 3 (+ furniture >80%) = 2 points. C+S: any three of seven categories >90% = 1 point. Generate compliance table, gap analysis, and optimization recommendations.

**Generated outputs.** Material compliance matrix (product × category × certification × status), VOC threshold comparison table, percentage calculations per category, path determination with points, exception report for non-compliant items, optimization recommendations.

**Validation logic.** Certification dates checked against purchase timeline. CDPH Standard Method version verified as v1.2-2017. Test report parsing uses dual-parser validation. Inherently non-emitting classification uses conservative rules—when in doubt, requires certification.

**Human review required.** Exception review for products with failed database queries; verification of edge-case category assignments. AI handles ~92% automatically; human focuses on ~8% exceptions. ~3–7 hours versus 44–66 hours manual.

**MVP complexity: Medium.** Certification database integration—seven certifiers with varying API availability—is the primary effort. Build incrementally, starting with UL SPOT, SCS, and CRI as the highest-volume databases.

**Productization notes.** This is the highest time-savings automation in MR. A single database query per product takes 2–3 minutes manually; at 300 products, that is 10–15 hours of data entry eliminated. Build as a shared module—MRc4 consumes the same product inventory.

---

### 2.7 LTc3 Compact and Connected Development

**Automation rationale.** LTc3 offers up to 6 points and is driven almost entirely by public geospatial data. Three independent options determine points: surrounding density (Census/parcel data), access to transit (GTFS schedule data), and walkable location (Walk Score API and proximity inventory). For density and transit, every data element comes from public APIs; only the walkable location option requires proximity construction from Google Places data. The credit is 100% calculation-based with deterministic thresholds.

**Required consultant inputs.** Project address only. All other data fetched automatically. Optional: consultant override of auto-detected project type.

**Data sources.** Walk Score API (~$0.05 per call); Google Maps Distance Matrix and Places (~$5–10 per analysis); U.S. Census TIGER/ACS API (free); TransitLand or Mobility Database for GTFS feeds (free); local municipal open data for parcel-level density; OpenStreetMap Overpass API for building footprints.

**AI workflow.** *Step 1—Geocode and type detection:* establish 0.25-mile and 0.5-mile analysis radii. *Step 2—Density analysis:* download ACS block group data within 0.25-mile radius; calculate DU/acre, FAR, and combined density; refine with parcel data if available. Thresholds: 22,000 SF/acre (1 point), 35,000 (2 points). *Step 3—Transit analysis:* discover stops within 0.25 mi (bus) and 0.5 mi (rail) via Google Maps Nearby; match to GTFS feeds; count trips applying LEED rules (lowest weekday, highest weekend, one direction, one stop per route). Thresholds: 72/30 trips (1 point) up to 360/216 (4 points). *Step 4—Walkability:* Walk Score API call (1–3 points) plus proximity uses inventory via Google Places across 40+ categories. *Step 5—Optimization report:* compare all options, recommend maximum-point pathway. *Step 6—Project variations:* schools receive connected site analysis; data centers receive transportation resources analysis.

**Generated outputs.** Connectivity analysis report, density calculations, transit documentation with trip counts and walking distances, Walk Score or proximity inventory, points optimization recommendation, density/transit access maps.

**Validation logic.** GTFS trip counts verified against agency schedules. Walking distances flagged if exceeding LEED radius. Census block group geometry verified for radius coverage.

**Human review required.** Confirm density calculations; verify transit distances reflect actual pedestrian access. ~15–30 minutes versus 15–25 hours manual.

**MVP complexity: Medium–High.** GTFS parsing and trip-counting logic is the primary challenge due to agency schedule variations. Walk Score and Census integrations are straightforward.

**Productization notes.** API costs are minimal (~$10/project). Cache Census and GTFS data at tract level for multi-project portfolios. Build the GTFS engine as a standalone microservice for reuse across projects.

---

### 2.8 EAc7 Enhanced Refrigerant Management and EAp5 Fundamental Refrigerant Management

**Automation rationale.** Both credits are pure database and calculation work. EAp5 (prerequisite) requires a complete refrigerant inventory with GWP lookup and HCFC-free verification. EAc7 (credit, up to 2 points) requires weighted average GWP calculations against category benchmarks, a leakage minimization plan, and GreenChill certification verification. Every GWP value is published by the IPCC or EPA; every benchmark is fixed in the LEED v5 reference guide. EAp5 data infrastructure feeds directly into EAc7, creating compounding automation value. Manual work: 4–8 hours (EAp5) plus 6–12 hours (EAc7).

**Required consultant inputs.** Equipment schedule with refrigerant type, charge per unit, quantity, new/existing designation (uploaded PDF, Excel, or Revit export). For EAc7: self-contained versus field-piped status per equipment item; food retailing percentage of gross area.

**Data sources.** EPA SNAP Program refrigerant database; IPCC AR6 GWP values (100-year); EPA GreenChill certification database; ASHRAE Standard 34 safety classifications.

**AI workflow—EAp5.** *Step 1—Parse schedule:* extract equipment ID, type, manufacturer, model, refrigerant type, charge, quantity, new/existing. *Step 2—GWP lookup:* match each refrigerant to database values (R-410A=2,088; R-32=675; R-134a=1,430; R-1234yf<1; 200+ entries). *Step 3—Calculate:* per equipment GWP = charge × GWP; project total and average. *Step 4—HCFC check:* flag R-22, R-123, etc.; flag GWP >700 for alternative evaluation. *Step 5—Generate:* inventory table, HCFC-free certification statement, alternative requirements list. *Step 6—Leak check templates.* *Step 7—Quality review.*

**AI workflow—EAc7.** *Step 1—Import EAp5 data.* *Step 2—Low GWP:* weighted average per category vs. benchmarks (HVAC 1,400; Data Centers/IT 700; Process Refrigeration 300). ≤80% of benchmark = 1 point; ≤50% = 2 points. *Step 3—Leakage plan:* verify ≥80% of total GWP in self-contained equipment; calculate tCO₂e per space (charge kg × GWP / 1,000); flag spaces >100 tCO₂e; generate plan with design specs, installation requirements, O&M procedures, and pressure-check intervals. *Step 4—GreenChill:* certification pathway if food retailing >20% of gross area. *Step 5—Documentation:* Low GWP report, leakage plan, detection specs, maintenance schedule. *Step 6—Quality review.*

**Generated outputs.** Complete refrigerant inventory, GWP analysis table with benchmark comparisons, HCFC-free certification, leakage minimization plan with maintenance schedules, compliance declaration.

**Validation logic.** GWP values version-locked to IPCC AR6. Benchmarks hardcoded from LEED v5. All calculations include full formula audit trails. GWP >700 triggers mandatory alternative evaluation.

**Human review required.** Verify all equipment captured; confirm self-contained/field-piped status. ~30 minutes–1 hour versus 10–20 hours manual.

**MVP complexity: Medium.** GWP database (200+ entries) is a one-time build. Equipment schedule parsing handles multiple MEP formats. Calculation engine and plan template are straightforward.

**Productization notes.** Build EAp5 engine first; EAc7 is a reporting layer on the same data. This compounding pattern—one input feeding multiple credits—is the architectural model to replicate across categories. Maintain the GWP database quarterly when IPCC/EPA publish updates.

---

### Cross-Credit Architecture Implications

These eight blueprints reveal a consistent pattern: the highest-value automation targets are credits where a single structured data input feeds multiple outputs. The WEp2 fixture database feeds WEc2. The EAp5 refrigerant inventory feeds EAc7. The MRc3 product inventory feeds MRc4. The IPp1 hazard data feeds SSc4. A platform that normalizes project data into a shared database—fixtures, equipment, products, hazards, demographics—and exposes it to multiple credit engines achieves compounding automation value that siloed credit tools cannot match.

The technology stack required across all eight blueprints is consistent: a multi-modal document parser for uploaded schedules and cut sheets, a web-research agent layer for public API queries, a calculation engine for deterministic compliance math, an LLM narrative generation module for templated documents, and a certification database integration layer for product lookups. These five components, built once and reused across credits, form the core infrastructure of a comprehensive LEED automation platform.
