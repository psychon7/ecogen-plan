# LEED v5 BD+C: LT + SS Credit Automation Analysis

**Prepared:** 2025-06-10  
**Scope:** Location & Transportation (LTc1-LTc5) + Sustainable Sites (SSp1, SSc1-SSc6)  
**Total Credits Analyzed:** 12  
**Methodology:** Each credit scored on Automation Score (1-5), Commercial Value (1-5), and Risk Level. Detailed blueprints provided for credits scoring 3+ on automation.

---

## EXECUTIVE SUMMARY

| Metric | Value |
|--------|-------|
| Credits Scoring 4-5 (High Automation) | 5 credits |
| Credits Scoring 3 (Moderate Automation) | 3 credits |
| Credits Scoring 1-2 (Low Automation) | 4 credits |
| **Total Points Available in Automated Credits** | **LT 11 pts + SS 8 pts = 19 pts** |
| **Top MVP Candidates** | LTc3, SSc4, LTc1, SSc3, SSc5 |
| **Recommended for MVP** | 5 credits |
| **Recommended for Later** | 4 credits |
| **Recommended Assist Only** | 3 credits |

---

## SUMMARY TABLE: All 12 Credits

| # | Credit | Name | Auto Score | Comm. Value | Risk | Doc Type | Inputs (Public / Upload) | Recommendation |
|---|--------|------|------------|-------------|------|----------|--------------------------|----------------|
| 1 | LTc1 | Sensitive Land Protection | **4** | 3 | Medium | Site analysis, GIS layers, narrative | NRCS soils, FEMA flood, NatureServe, USGS DEM, NHDPlus, NWI / Site plan with footprint | **Automate in MVP** |
| 2 | LTc2 | Equitable Development | 2 | 2 | Medium | Policy docs, records, narrative | HUD AMI (API), Census demographics / Brownfield letters, employment records, lease agreements, apprenticeship docs | **Assist Only** |
| 3 | LTc3 | Compact & Connected Development | **5** | **5** | Low | GIS analysis, calculation, data report | Census density, Walk Score API, GTFS/transit APIs, Google Maps/Places API, parcel GIS / Project address only | **Automate in MVP** |
| 4 | LTc4 | Transport Demand Mgmt | 3 | 4 | Medium | Calculation, site analysis, narrative | OpenStreetMap bike data, Google Maps Distance API, transit APIs / Occupancy counts, parking study, VMT analysis | **Automate Later** |
| 5 | LTc5 | Electric Vehicles | 2 | 2 | Low | Drawing markup, calculation | None significant / EVSE cut sheets, electrical plans, parking plan | **Assist Only** |
| 6 | SSp1 | Minimized Site Disturbance | 2 | 3 | Medium | Policy, checklist, photo evidence | EPA CGP reference / Erosion control plan, site assessment, inspection records | **Assist Only** |
| 7 | SSc1 | Biodiverse Habitat | 3 | 3 | Medium | Calculation, site analysis, species list | EPA ecoregion API, USDA PLANTS, ABC Threat Factor DB / Site plan, soil test, glass schedule | **Automate Later** |
| 8 | SSc2 | Accessible Outdoor Space | 2 | 2 | Low | Drawing markup, calculation | None / Site plan, landscape plan, occupancy count | **Assist Only** |
| 9 | SSc3 | Rainwater Management | **4** | **4** | Medium | Calculation, hydrology model | NOAA PFDS precipitation data, NRCS curve numbers, EPA stormwater data / Site plan with impervious surfaces | **Automate in MVP** |
| 10 | SSc4 | Enhanced Resilient Site Design | **4** | **5** | Medium | Site analysis, hazard assessment, checklist | FEMA flood maps, NOAA climate data, IPCC projections, USGS hazards, NIFC wildfire, NOAA SLR / IPp1 assessment reference | **Automate in MVP** |
| 11 | SSc5 | Heat Island Reduction | **4** | **4** | Low | Calculation, drawing markup | American Forests Tree Equity Score API, CRRC rated products DB / Site plan, roof plan, product cut sheets | **Automate in MVP** |
| 12 | SSc6 | Light Pollution Reduction | 3 | 3 | Low | Template checklist, drawing markup | MLO lighting zone lookup, IES TM-15-11 reference / Lighting fixture schedule, site lighting plan | **Automate Later** |

---

## DETAILED CREDIT ANALYSES

---

### LTc1: SENSITIVE LAND PROTECTION

**Scorecard:** Automation: 4 | Commercial Value: 3 | Risk: **Medium**

**Overview:** This credit requires the project to avoid developing on sensitive land — including prime farmland, floodplains, notable habitat, water bodies, wetlands, and steep slopes. Two options exist: (1) build on previously developed land (simpler), or (2) avoid all sensitive land categories on previously undeveloped sites.

#### Documentation Type
Site analysis, GIS overlay analysis, narrative report, uploaded site plan

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - NRCS Soil Survey** | Web Soil Survey (WSS) via Soil Data Access API | Query soil map units for prime farmland classification |
| **Public - FEMA Flood Data** | FEMA National Flood Hazard Layer (NFHL) REST API | Overlay project polygon to check 100-year floodplain intersection |
| **Public - NatureServe** | NatureServe Explorer Web Services | Query species/habitat status for G1/G2/GH rankings within buffer |
| **Public - USGS Topography** | USGS 3D Elevation Program (3DEP) | DEM raster analysis for slope calculation (% grade) |
| **Public - National Wetland Inventory** | USGS NWI WMS/WFS services | Wetland polygon proximity within 50 ft setback |
| **Public - NHDPlus** | EPA/USGS National Hydrography Dataset | Water body proximity within 100 ft setback |
| **Public - Protected Areas** | USGS Protected Areas Database (PAD-US) | Conservation land overlaps |
| **Upload - Site Plan** | Project CAD/GIS file with development footprint | Define analysis boundary |

#### AI Techniques Applicable
1. **GIS/data integration** (PRIMARY): Auto-query all 7 public data layers and overlay against project polygon
2. **Web research agents**: Fetch current NatureServe data, verify NRCS classifications
3. **LLM narrative generation**: Generate sensitive land assessment narrative from GIS results
4. **Calculation engines**: Slope analysis from DEM, setback distance calculations, area percentage for steep slope protection

#### Automation Blueprint (Score: 4)

```
STEP 1: Project Boundary Input
- User uploads site boundary polygon (GeoJSON, KML, or Shapefile)
- OR enters project address and AI geocodes to parcel boundary

STEP 2: Automated GIS Data Fetching (Parallel API Calls)
- NRCS Soil Data Access API → Prime farmland status (yes/no + map units)
- FEMA NFHL API → Flood zone classification (AE, A, V, X) + floodplain intersection
- NatureServe Web Services → Species/habitat with G1/G2/GH rankings within 1-mile buffer
- USGS NWI WFS → Wetland polygons within 100ft buffer
- NHDPlus → Water body features within 200ft buffer
- USGS 3DEP DEM → Slope raster extraction for project area
- PAD-US → Protected area overlap check

STEP 3: Automated Analysis
- Floodplain: Boolean intersection check against 100-year floodplain
- Habitat: Buffer analysis for NatureServe polygons
- Wetlands: 50ft setback distance calculation from delineated wetlands
- Water bodies: 100ft setback distance calculation
- Slopes: DEM analysis → slope raster → classify 15-25% and >25% zones
  → Calculate protection percentages required (40% / 60%)
- Prime farmland: Soil map unit overlay → classification check

STEP 4: Compliance Report Generation
- LLM generates narrative report with findings for each sensitive land category
- Auto-generated compliance checklist (pass/fail per category)
- Map visualization with all data layers overlaid on project boundary

STEP 5: Consultant Review
- Review auto-generated report and maps
- Upload site plan showing development footprint (required for submission)
- Confirm or override any findings
- Wetland delineation still requires licensed professional (upload)

OUTPUT: Sensitive Land Assessment Report + compliance maps + checklist
```

**Estimated Time Savings:** 6-10 hours of manual GIS analysis → 30 minutes of review

**Risk Factors:**
- Wetland delineation requires licensed professional survey (cannot be fully automated)
- NatureServe data completeness varies by region
- Slope analysis accuracy depends on DEM resolution
- FEMA flood maps may not be digitized in all jurisdictions

**Final Recommendation:** **Automate in MVP** — Strong ROI from GIS automation, high repeatability

---

### LTc2: EQUITABLE DEVELOPMENT

**Scorecard:** Automation: 2 | Commercial Value: 2 | Risk: **Medium**

**Overview:** Multiple pathways including brownfield remediation, historic location, local economy support, affordable housing, and equitable construction. Options are document-heavy and authority-dependent.

#### Documentation Type
Policy documents, employment records, narrative, uploaded certifications

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - HUD AMI** | HUD Fair Market Rents & Income Limits API | AMI lookup by county/MFAs |
| **Public - Census demographics** | US Census Bureau ACS API | Jobs-to-housing ratio, demographic data |
| **Upload - Brownfield letter** | From EPA or state environmental authority | PDF document |
| **Upload - Employment records** | Payroll data with worker addresses | Confidential data |
| **Upload - Lease/sale agreements** | Legal documents with affordability covenants | Legal documents |
| **Upload - Apprenticeship records** | DOL registered apprenticeship documentation | Government records |
| **Upload - Training records** | Attendance logs for life-skills training | Internal records |

#### AI Techniques Applicable
1. **LLM document analysis**: Extract key data from uploaded brownfield letters, lease agreements
2. **Web research agents**: Verify AMI calculations against HUD data
3. **Template-based document generation**: Generate local employment percentage reports
4. **GIS integration**: Calculate sensitive receptor distances for DC/WD/DC projects

#### Automation Assessment
This credit is primarily document-driven. Most pathways require:
- Letters from government authorities (cannot be auto-generated)
- Confidential employment/payroll data (cannot be publicly sourced)
- Legal agreements with affordability covenants
- Construction hours tracking data (project-specific)

The only fully automatable component is the HUD AMI data lookup and demographic analysis for the jobs-to-housing ratio pathway.

**Final Recommendation:** **Assist Only** — Provide AMI lookup tools and document templates, but automation ROI is low due to document-heavy nature

---

### LTc3: COMPACT AND CONNECTED DEVELOPMENT

**Scorecard:** Automation: 5 | Commercial Value: 5 | Risk: **Low**

**Overview:** The highest-point credit in the LT category (up to 6 points). Three main options: surrounding density, access to transit, and walkable location. Almost entirely driven by publicly available location data.

#### Documentation Type
GIS analysis, data report, calculation, proximity inventory

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - Address/Coordinates** | Project geocoded address | Entry point for all analyses |
| **Public - Walk Score** | Walk Score API (walkscore.com) | Direct API call with lat/lon |
| **Public - Census/ACS** | US Census Bureau TIGER/ACS API | Housing units, population, density within 0.25 mi |
| **Public - Transit GTFS** | TransitLand, Mobility Database | Schedule data for trip counting |
| **Public - Google Maps/Places** | Google Maps API, Places API | Walking distance calculations, nearby uses inventory |
| **Public - Local GIS Parcels** | City/county open data portals | Parcel-level density calculations |
| **Public - OpenStreetMap** | OSM Overpass API | Building footprints, land use tags |
| **Upload** | None required for data gathering | Only final report format preference |

#### AI Techniques Applicable
1. **GIS/data integration** (PRIMARY): Density calculation within 0.25-mile buffer using census + parcel data
2. **Transit API integration** (PRIMARY): Automated GTFS parsing for weekday/weekend trip counting
3. **Walk Score API**: Direct integration for instant score retrieval
4. **Google Maps/Places API**: Walking distance matrix + nearby use type categorization
5. **LLM narrative generation**: Auto-generate density analysis narrative, transit proximity report
6. **Web research agents**: Verify transit schedules, find local GIS portals
7. **Calculation engines**: Density formulas (DU/acre, FAR, combined SF/acre), trip counting logic

#### Automation Blueprint (Score: 5)

```
STEP 1: Project Location Input
- User enters project address
- AI geocodes to lat/lon coordinates
- Auto-detects project type (NC, CS, School, Healthcare, DC/WD/DC)

STEP 2: Option 1 - Surrounding Density Analysis (Parallel)
  2a: Census Data Query
    - Download ACS block group data within 0.25-mile radius
    - Extract housing units, population, building square footage estimates
    - Calculate residential density (DU/acre), nonresidential FAR, combined density
    - Compare against thresholds: 22,000 SF/acre (1pt), 35,000 SF/acre (2pt)
  2b: Local Parcel Data (if available)
    - Query municipal open data portal for parcel data
    - Cross-reference with building permits/assessor data
    - Refine density calculations with actual building areas
  2c: OpenStreetMap Buildings
    - Extract building footprints and inferred land use
    - Supplement density data where parcel data is unavailable

STEP 3: Option 2 - Access to Transit Analysis (Parallel)
  3a: Transit Stop Discovery
    - Google Maps Nearby Search for bus stops, rail stations within 0.25/0.5 mi
    - GTFS feed matching for discovered stops
  3b: Trip Counting Engine
    - Parse GTFS: trips.txt + stop_times.txt + calendar.txt
    - Count trips per route per direction
    - Apply counting rules:
      * Weekday: use day with LOWEST trips
      * Weekend: use day with HIGHEST trips
      * One direction per route only
      * One stop per route (if multiple qualifying stops)
    - Compare against thresholds: 72/30 (1pt) → 360/216 (4pt)
  3c: Walking Distance Verification
    - Google Maps Distance Matrix API: walking distances to each qualifying stop
    - Verify within 0.25 mi (bus) or 0.5 mi (rail/BRT/ferry)

STEP 4: Option 3 - Walkable Location Analysis (Parallel)
  4a: Walk Score API
    - Direct API call → instant score (0-100)
    - Map to points: 60-69 (1pt), 70-79 (2pt), 80+ (3pt)
  4b: Proximity Uses Inventory (fallback/alternative)
    - Google Maps Places API: search all 40+ use categories within 0.5 mi
    - Apply counting rules: max 2 per type, must cover 3+ of 5 categories
    - Tally qualifying use types → map to points

STEP 5: Points Optimization Report
- LLM generates comprehensive report showing:
  * All three option analyses with point estimates
  * Recommended pathway for maximum points
  * Data sources cited for each finding
  * Walking distance maps for transit
  * Density visualization map

STEP 6: Project-Type Variations (Auto-Detect)
- Schools: Connected site analysis (adjacent/infill parcel check)
- DC/WD/DC: Transportation resources proximity (highway, rail, logistics hub)
- Healthcare: Surrounding density + rural campus provisions

OUTPUT: Complete LTc3 credit package with all analyses, maps, and point optimization
```

**Estimated Time Savings:** 15-25 hours of manual data gathering and GIS analysis → 15 minutes of review

**Risk Factors:**
- GTFS data availability varies by transit agency
- Parcel data may not be openly available in all jurisdictions
- "Buildable land area" requires consultant judgment to exclude roads/water
- Walking distance API results may not match actual pedestrian routes exactly

**Data API Costs:**
- Walk Score API: ~$0.05/call
- Google Maps API: ~$5-10 for full analysis
- Census/ACS: Free
- TransitLand: Free tier available
- GTFS: Free from transit agencies

**Final Recommendation:** **Automate in MVP** — Highest commercial value credit, almost entirely public data-driven, massive time savings

---

### LTc4: TRANSPORTATION DEMAND MANAGEMENT

**Scorecard:** Automation: 3 | Commercial Value: 4 | Risk: **Medium**

**Overview:** Requires a Transportation Demand Assessment (TDA) before earning points. Options include parking reduction, parking fees, and active travel facilities (bike network, storage, showers, maintenance).

#### Documentation Type
Calculation, site analysis, narrative report, drawing markup

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - ITE Parking Generation** | ITE Parking Generation Manual (subscription) | Reference data for base parking ratios |
| **Public - Bike network** | OpenStreetMap cycling tags, city bike maps | Network analysis for 3-mile contiguous network |
| **Public - Transit** | Google Maps API, GTFS | TDA exemption verification |
| **Public - Local zoning** | Municipal zoning code search | Parking minimum requirements |
| **Upload - Occupancy counts** | Project FTE/visitor counts | Required for all calculations |
| **Upload - Parking study** | By qualified transportation professional | Required for Option 1 |
| **Upload - Site plan** | Showing parking layout, bike storage locations | Drawing |

#### AI Techniques Applicable
1. **Calculation engines**: Bicycle storage count formulas, shower scaling formula, parking reduction %
2. **GIS/data integration**: Bike network proximity analysis via OpenStreetMap
3. **LLM narrative generation**: TDA narrative, VMT analysis report structure
4. **Web research agents**: Find local bike network maps, verify transit access for exemption
5. **Template-based document generation**: TDA report template, parking study template

#### Automation Blueprint (Score: 3)

```
STEP 1: TDA Exemption Check
- AI checks if project qualifies for exemption:
  * Within 0.5 mi of major transit → query Google Maps walking distance
  * In transit priority area → query local transit authority maps
  * Residential affordable housing in infill → requires consultant input
  * Local TDM program → web research for local programs
- If exempt: generate exemption documentation path

STEP 2: Occupancy-Based Calculations
- User inputs FTE count, visitor count, dwelling units (if residential)
- AI calculates:
  * Bicycle short-term storage: 2.5% of peak visitors (min 4)
  * Bicycle long-term storage: 5% FTE commercial (min 4), 15% FTE residential
  * Showers: scaling formula (1 per 100, then 1 per 150, then 1 per 500, etc.)
  * Shared micromobility: up to 50% credit calculation

STEP 3: Bike Network Analysis
- OpenStreetMap Overpass query: bicycle lanes/paths within 600ft of project
- Network analysis: trace 3-mile contiguous network from project
- Speed limit verification for adjacent streets (OSM maxspeed tags)
- Generate bike network proximity map

STEP 4: Parking Reduction Calculation
- User inputs total parking spaces
- AI calculates ITE base ratio (requires ITE manual data or consultant input)
- Reduction percentage = (ITE base - provided) / ITE base
- Points mapping: 30% (1pt), 60% (2pt), 100% (3pt)

STEP 5: Document Generation
- Auto-populate TDA report template with calculated values
- Generate bicycle storage plan template
- Create parking reduction calculation table
- LLM drafts VMT analysis structure (emissions data requires professional input)

OUTPUT: TDA report template + storage calculations + bike network map + parking analysis
```

**Estimated Time Savings:** 4-8 hours of calculation and documentation → 1 hour of review and professional input

**Risk Factors:**
- VMT analysis requires professional transportation engineer judgment
- ITE Parking Generation Manual is copyrighted (subscription required)
- Bike network quality assessment requires professional judgment
- Parking reduction strategies may trigger zoning code conflicts

**Final Recommendation:** **Automate Later** — Strong calculation engine value, but requires professional engineering input for VMT and parking studies

---

### LTc5: ELECTRIC VEHICLES

**Scorecard:** Automation: 2 | Commercial Value: 2 | Risk: **Low**

**Overview:** Requires installing EVSE or making parking spaces EV-ready. Simple percentage-based calculations from total parking count.

#### Documentation Type
Drawing markup, calculation, product specification

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - ENERGY STAR EVSE** | ENERGY STAR Product Finder | Verify certified products |
| **Upload - Total parking count** | From parking plan or project data | Number input |
| **Upload - EVSE cut sheets** | Manufacturer specifications | PDF product data |
| **Upload - Electrical plans** | Showing conduit, panel, voltage | Drawing |
| **Upload - Accessible EV space plan** | Dimensioned drawings | Drawing |

#### AI Techniques Applicable
1. **Calculation engines**: EVSE count = max(5% total parking, 2 spaces), EV-ready count percentages
2. **LLM document analysis**: Extract voltage/ampacity from EVSE cut sheets
3. **Template-based document generation**: Parking count calculation table

#### Automation Assessment
This credit is straightforward calculation once parking count is known. The complexity is in:
- Verifying EVSE meets ENERGY STAR connected functionality (from cut sheets)
- Accessible space dimensions (9ft wide + 5ft access aisle) — requires drawing review
- Electrical load calculations — requires electrical engineer review

**Final Recommendation:** **Assist Only** — Simple calculator tool, but documentation is almost entirely uploaded design documents

---

### SSp1: MINIMIZED SITE DISTURBANCE (Prerequisite)

**Scorecard:** Automation: 2 | Commercial Value: 3 | Risk: **Medium**

**Overview:** Required prerequisite. Two parts: (1) erosion and sedimentation control plan per EPA CGP, and (2) preconstruction site assessment for vegetation conservation.

#### Documentation Type
Policy document, checklist, photo evidence

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - EPA 2022 CGP** | EPA website (free PDF) | Reference standard |
| **Upload - Erosion control plan** | Project-specific document | Consultant prepared |
| **Upload - Site assessment** | Vegetation survey, habitat assessment | Field survey required |
| **Upload - Inspection records** | Weekly/14-day inspection logs | Field verification |
| **Upload - Exclusion zone plans** | Physical barrier documentation | Drawing |

#### AI Techniques Applicable
1. **LLM narrative generation**: Draft erosion control plan from project parameters
2. **Template-based document generation**: Inspection log templates, exclusion zone documentation templates
3. **Computer vision**: Analyze site photos for vegetation coverage (preliminary)
4. **Web research agents**: Verify EPA CGP requirements for project location

#### Automation Assessment
This is a field-verification-heavy prerequisite. Key limitation: preconstruction survey requires physical site visit by qualified professional to identify special-status vegetation, healthy habitat, and invasive species. No public database can substitute for this field work.

The automatable components are:
- EPA CGP compliance checklist generation
- Inspection schedule/log templates
- Erosion control plan template (LLM-generated from project type/size)
- Construction-exclusion zone documentation templates

**Final Recommendation:** **Assist Only** — Generate templates and checklists, but the core requirement demands physical site verification

---

### SSc1: BIODIVERSE HABITAT

**Scorecard:** Automation: 3 | Commercial Value: 3 | Risk: **Medium**

**Overview:** Preserve greenfield areas (40%) and restore previously disturbed areas (20-40%). Requires native species selection, soil restoration, pollinator habitat, and optionally bird-friendly glass.

#### Documentation Type
Calculation, site analysis, species list, drawing markup

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - EPA Ecoregions** | EPA Level III Ecoregion GIS data | Determine project ecoregion for species selection |
| **Public - USDA PLANTS** | USDA PLANTS Database API | Native/adapted species lookup by state/ecoregion |
| **Public - NRCS Soil Survey** | Web Soil Survey API | Soil restoration requirements, prime farmland check for imports |
| **Public - ABC Threat Factor DB** | American Bird Conservancy (web search) | Glass threat factor verification |
| **Upload - Site plan** | Greenfield/disturbed area delineation | Area measurement source |
| **Upload - Soil test** | Imported soil analysis | Verify no prime farmland soils |
| **Upload - Glass schedule** | Product specifications for bird-friendly compliance | Drawing/specification |

#### AI Techniques Applicable
1. **GIS/data integration**: EPA ecoregion identification, area calculations from site plan
2. **LLM narrative generation**: Native species recommendations for ecoregion, vegetation restoration plan
3. **Web research agents**: USDA PLANTS database queries, state native plant society resources, bird-friendly glass product research
4. **Calculation engines**: Greenfield preservation %, disturbed area restoration %, pollinator habitat sq ft
5. **Computer vision**: Analyze site photos for vegetation cover estimation

#### Automation Blueprint (Score: 3)

```
STEP 1: Ecoregion & Species Research
- GIS overlay: project location → EPA Level III ecoregion
- Web agent queries USDA PLANTS Database for:
  * Native species list for ecoregion/state (minimum 10 species)
  * Trees, shrubs, ground cover categories
  * Pollinator-friendly flowering plants
- Web agent searches state extension/native plant society resources

STEP 2: Area Calculations (from uploaded site plan)
- User uploads site plan with area annotations OR
- AI extracts area measurements from PDF/drawing
- Calculate: protected greenfield / total greenfield >= 40%
- Calculate: restored area / total disturbed area >= 20% (1pt) or 40% (2pt)
- Calculate: pollinator habitat >= 110 sq ft in groupings >= 10 sq ft each

STEP 3: Soil Restoration Check
- NRCS soil survey API: verify on-site soils classification
- Flag if imported soils from prime farmland sources (prohibited)
- Generate soil restoration documentation

STEP 4: Bird-Friendly Glass (Option 2)
- Web agent searches ABC Threat Factor Database for specified glass products
- Verify threat factor <= 30 for all glass below 50ft
- Cross-reference glass schedule with height thresholds

OUTPUT: Species recommendation report + area calculation table + soil analysis + bird-friendly compliance check
```

**Estimated Time Savings:** 3-5 hours of research and calculation → 1 hour of review

**Risk Factors:**
- Species selection requires ecological expertise — AI recommendations need expert review
- Bird-friendly glass threat factors may not be available for all products
- Soil restoration requires physical soil testing
- Area measurements from uploaded drawings may need verification

**Final Recommendation:** **Automate Later** — Species research engine is valuable but requires expert review; area calculator is useful

---

### SSc2: ACCESSIBLE OUTDOOR SPACE

**Scorecard:** Automation: 2 | Commercial Value: 2 | Risk: **Low**

**Overview:** Requires outdoor space >= 30% of site, with vegetated portion >= 25% of outdoor space, plus urban and community elements.

#### Documentation Type
Drawing markup, calculation

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Upload - Site plan** | With area measurements | Total site area, outdoor space area |
| **Upload - Landscape plan** | Vegetation types and areas | Vegetated portion calculation |
| **Upload - Occupancy count** | For seating calculation (if social area) | 5% of occupants |

#### AI Techniques Applicable
1. **Calculation engines**: Outdoor space %, vegetated %, seating count
2. **LLM narrative generation**: Outdoor space narrative description

#### Automation Assessment
This is a straightforward calculation credit with design document requirements:
- (Outdoor space / Total site) >= 30%
- (Vegetated area / Outdoor space) >= 25%
- Seating count >= 5% of occupants (if social area selected)
- Simple calculator tool can verify compliance
- Most documentation is design drawings that must be uploaded

**Final Recommendation:** **Assist Only** — Simple compliance calculator, but documentation is entirely design drawings

---

### SSc3: RAINWATER MANAGEMENT

**Scorecard:** Automation: 4 | Commercial Value: 4 | Risk: **Medium**

**Overview:** Retain runoff from percentile rainfall events (80th-90th) using LID/GI practices. Option 2 uses natural land cover condition modeling. Critical for site sustainability and flood risk reduction.

#### Documentation Type
Calculation, hydrology model, site analysis

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - NOAA Precipitation** | NOAA Precipitation Frequency Data Server (PFDS) | Regional rainfall depth for target percentile events |
| **Public - NRCS Curve Numbers** | Web Soil Survey + NRCS TR-55 | Hydrologic soil group → Curve Number for runoff calculation |
| **Public - NRCS Soil Survey** | Soil Data Access API | Soil hydrologic group classification |
| **Public - EPA Stormwater** | EPA Stormwater Calculator (SWC) | Simplified runoff modeling tool |
| **Public - Climate Data** | NOAA Climate Data Online | Historical precipitation records |
| **Upload - Site plan** | Impervious surface delineation | Runoff calculation input |
| **Upload - LID/GI design** | Bioretention, permeable pavement, green roof specs | Strategy documentation |

#### AI Techniques Applicable
1. **Calculation engines** (PRIMARY): Runoff volume = Rainfall depth x Area x Runoff Coefficient, NRCS Curve Number method
2. **GIS/data integration**: Soil hydrologic group overlay, impervious area calculation
3. **Web research agents**: NOAA PFDS data retrieval, regional rainfall statistics
4. **LLM narrative generation**: Rainwater management plan narrative, LID strategy documentation
5. **Template-based document generation**: Hydrology calculation report

#### Automation Blueprint (Score: 4)

```
STEP 1: Project Location & Site Data Input
- User enters project address
- AI determines NOAA PFDS station ID
- User uploads site plan with impervious surface areas
- User inputs project type (standard or zero lot line)

STEP 2: Rainfall Data Retrieval
- NOAA PFDS API query:
  * 80th, 85th, 90th percentile rainfall depths (24-hour)
  * Duration: typically 24-hour event
  * Return periods: mapped to percentile events
- For zero lot line: 70th, 75th, 80th percentile

STEP 3: Soil & Hydrology Analysis
- NRCS Soil Data Access API:
  * Query soil map units within project boundary
  * Extract hydrologic soil group (A, B, C, D)
  * Calculate weighted average Curve Number
- Area inputs from site plan:
  * Impervious area → CN = 98
  * Pervious area → CN based on soil group and land use
  * Weighted CN = (CN1 x Area1 + CN2 x Area2) / Total Area

STEP 4: Runoff Volume Calculations
- Option 1 (Percentile Events):
  * Runoff depth = f(Rainfall depth, Weighted CN) per NRCS TR-55
  * Runoff volume = Runoff depth x Total site area
  * Retention requirement = Total runoff volume (100% retention)
  * Points: 80th (1pt), 85th (2pt), 90th (3pt)

- Option 2 (Natural Land Cover):
  * Model pre-development CN (meadow/woods condition)
  * Model post-development CN (proposed conditions)
  * Volume to retain = Post-dev runoff - Pre-dev runoff

STEP 5: LID/GI Strategy Calculator
- User inputs proposed GI strategies with areas:
  * Green roof area → retention credit
  * Permeable pavement area → infiltration credit
  * Bioretention/rain garden area → retention + infiltration
  * Rainwater harvesting volume → collection credit
- AI calculates total retention capacity vs. required
- Compliance check: total retention >= required retention

STEP 6: Water Reuse Bonus Point Check
- If rainwater harvesting included:
  * Verify end uses: irrigation, flush fixtures, makeup water
  * Calculate annual reuse volume
  * Additional point if reuse system is designed

STEP 7: Report Generation
- LLM generates rainwater management plan narrative
- Auto-generated calculation tables with all inputs and formulas
- Hydrology summary: rainfall depth, CN, runoff volume, retention capacity
- Compliance summary: pass/fail per point threshold
- LID/GI strategy summary with retention credits

OUTPUT: Rainwater management calculation report + hydrology analysis + compliance summary
```

**Estimated Time Savings:** 8-12 hours of manual data lookup and calculation → 1-2 hours of review and input

**Risk Factors:**
- Hydrology modeling simplified vs. full SWMM modeling — accuracy depends on site complexity
- NRCS CN method is approximate; complex sites may need professional hydrologist
- Impervious area measurements from uploaded drawings require verification
- LID/GI retention rates are conservative estimates
- Professional engineer stamp may be required for submission in some jurisdictions

**Data Sources:**
- NOAA PFDS: Free (https://hdsc.nws.noaa.gov/hdsc/pfds/)
- NRCS Soil Data Access: Free
- EPA Stormwater Calculator: Free desktop tool

**Final Recommendation:** **Automate in MVP** — Strong engineering calculation engine with robust public data integration, high commercial value

---

### SSc4: ENHANCED RESILIENT SITE DESIGN

**Scorecard:** Automation: 4 | Commercial Value: 5 | Risk: **Medium**

**Overview:** Address two highest-priority hazards from IPp1 Climate Resilience Assessment. Covers 10 hazard types: drought, extreme heat, flooding, hail, hurricanes, sea level rise, tsunamis, wildfires, winter storms.

#### Documentation Type
Site analysis, hazard assessment, checklist, narrative

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - FEMA Flood Maps** | FEMA NFHL API, Flood Insurance Rate Maps | Flood zone, base flood elevation |
| **Public - NOAA Climate Data** | NOAA Climate Explorer, NCEI | Temperature trends, precipitation patterns |
| **Public - IPCC Projections** | IPCC AR6 Interactive Atlas | Regional climate projections |
| **Public - USGS Hazards** | USGS Earthquake, Landslide, Volcano hazards | Multi-hazard mapping |
| **Public - NIFC Wildfire** | National Interagency Fire Center | Wildfire risk assessment |
| **Public - NOAA Sea Level Rise** | NOAA Sea Level Rise Viewer | SLR projections for coastal sites |
| **Public - IBHS/FORTIFIED** | Insurance Institute for Business & Home Safety | Hail/high wind standards reference |
| **Public - ASCE Standards** | ASCE 24, ASCE/SEI 7 | Flood/wind design references |
| **Public - Tsunami Data** | NOAA TsunamiReady, state tsunami maps | Tsunami evacuation zones |
| **Upload - IPp1 Assessment** | Climate resilience assessment (prerequisite) | Identify top 2 hazards |
| **Upload - Site plans** | Showing resilient design strategies | Drawing markup |

#### AI Techniques Applicable
1. **Web research agents** (PRIMARY): Multi-source hazard data retrieval — the most complex web research task in all LT+SS credits
2. **GIS/data integration**: FEMA flood overlay, wildfire risk mapping, sea level rise projection
3. **LLM narrative generation**: Hazard-specific strategy narratives, resilience plan documentation
4. **Template-based document generation**: Strategy checklists per hazard type, compliance documentation
5. **Computer vision**: Analyze site photos for existing resilience features

#### Automation Blueprint (Score: 4)

```
STEP 1: Hazard Identification from IPp1
- User uploads IPp1 Climate Resilience Assessment
- AI extracts two highest-priority hazards (LLM document parsing)
- OR: User selects two hazards from list of 10

STEP 2: Automated Hazard Data Retrieval (Parallel by Hazard)

  For each selected hazard:

  DROUGHT:
    - NOAA Climate Explorer: historical drought index (PDSI/SPI) for project region
    - US Drought Monitor: current and projected drought conditions
    - Generate: drought risk summary + native plant recommendation list

  EXTREME HEAT:
    - NOAA Climate Data: historical heat wave frequency and duration trends
    - EPA EJSCREEN: heat vulnerability indices for project census tract
    - Generate: heat risk assessment + strategy checklist (7 strategies)

  FLOODING:
    - FEMA NFHL: flood zone classification + base flood elevation
    - NOAA PFDS: rainfall intensity trends
    - USGS stream gauges: nearby flood stage data
    - Generate: flood risk assessment + ASCE 24/FEMA 543 strategy checklist

  HAIL:
    - NOAA Storm Events Database: historical hail frequency/severity for county
    - IBHS: FORTIFIED Commercial Hail requirements summary
    - Generate: hail risk assessment + design requirement checklist

  HURRICANES/HIGH WINDS:
    - ASCE/SEI 7-10: wind speed map for project location
    - NOAA HURDAT2: historical hurricane tracks near project
    - FEMA wind zones: project classification
    - Generate: wind risk assessment + FORTIFIED design checklist

  SEA LEVEL RISE:
    - NOAA Sea Level Rise Viewer: projections for project coastal location
    - IPCC AR6: regional SLR projections for design service life
    - Generate: SLR risk assessment + 9-strategy checklist

  TSUNAMIS:
    - NOAA/NWS TsunamiReady: project proximity to tsunami evacuation zones
    - State tsunami inundation maps: overlay check
    - Generate: tsunami risk assessment + signage/communication checklist

  WILDFIRES:
    - NIFC/MTBS: historical wildfire burn area near project
    - State wildfire risk assessment: project zone classification
    - NWCG Standards: compliance checklist
    - Generate: wildfire risk assessment + Safer from the Start zone checklist

  WINTER STORMS:
    - NOAA Climate Data: historical snowfall/ice storm frequency
    - ASCE 7: snow load requirements for project location
    - Generate: winter storm risk assessment + 4-strategy checklist

STEP 3: Strategy Compliance Checklist
- For each hazard: auto-generate checklist of required strategies
- Track: minimum count of strategies (typically 2+)
- Cross-reference with uploaded site plans (if available)

STEP 4: Narrative Report Generation
- LLM generates comprehensive resilient site design narrative:
  * Hazard context and regional risk profile
  * Selected strategies with design rationale
  * Compliance with referenced standards
  * Integration with overall site design

STEP 5: Documentation Package Assembly
- Auto-generate compliance tables per hazard
- Strategy implementation checklist
- Reference standard summaries (ASCE 24, FEMA 543, FORTIFIED, NWCG)
- Map visualizations: hazard overlays on project site

OUTPUT: Resilient site design assessment + hazard-specific strategy checklists + compliance documentation
```

**Estimated Time Savings:** 10-15 hours of multi-source research and documentation → 2 hours of review

**Risk Factors:**
- Hazard data quality varies significantly by region
- IPp1 prerequisite assessment must be completed first
- Strategy selection requires engineering/architectural judgment
- Some referenced standards require purchase/subscription (FORTIFIED, ASCE)
- Climate projection uncertainty ranges are wide

**Final Recommendation:** **Automate in MVP** — Highest commercial value in SS category, complex multi-source web research is exactly where AI excels, strong risk-reduction value for projects

---

### SSc5: HEAT ISLAND REDUCTION

**Scorecard:** Automation: 4 | Commercial Value: 4 | Risk: **Low**

**Overview:** Three independent options: (1) weighted nonroof/roof calculation, (2) 100% parking under cover, (3) Tree Equity Score. Uses SRI/SR values and area-based calculations.

#### Documentation Type
Calculation, drawing markup, data report

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - CRRC Rated Products** | Cool Roof Rating Council database | SRI/SR values for roofing products |
| **Public - American Forests Tree Equity** | Tree Equity Score API | Score for project location |
| **Public - ANSI/CRRC S100** | CRRC website | Standard reference |
| **Upload - Site plan** | Paving areas, roof areas | Area measurement |
| **Upload - Roof plan** | Roof types and slopes | Area + slope classification |
| **Upload - Product cut sheets** | SRI/SR values for paving and roofing materials | Compliance verification |
| **Upload - Parking plan** | Space count and cover type | Option 2 compliance |

#### AI Techniques Applicable
1. **Calculation engines** (PRIMARY): Weighted area calculation — the core compliance equation
2. **Web research agents**: CRRC product database queries, Tree Equity Score lookup
3. **LLM document analysis**: Extract SRI/SR values from product cut sheets
4. **LLM narrative generation**: Heat island reduction narrative, shade plan description
5. **Computer vision**: Identify roof types and paving materials from drawings (preliminary)

#### Automation Blueprint (Score: 4)

```
STEP 1: Area Data Collection
- User uploads site plan and roof plan
- AI extracts or user inputs:
  * Total paving area (nonroof)
  * Total roof area (by slope: low <= 2:12, steep > 2:12)
  * Area of each mitigation strategy

STEP 2: Product Data Lookup (Parallel)
  Option A - CRRC Database:
    - Web agent queries CRRC rated products database for specified products
    - Extract: initial SRI, aged SRI, initial SR, product name
    - Verify aged SRI >= 64 (low-slope) or >= 32 (steep-slope)
    - Verify initial SR >= 0.33 for paving

  Option B - Cut Sheet Analysis:
    - User uploads product cut sheets (PDF)
    - LLM extracts SRI/SR values from each document
    - Verify compliance with threshold values

STEP 3: Weighted Calculation Engine
Equation:
[(Area_nonroof_measures / 0.5) + (Area_high_ref_roof / 0.75) + (Area_veg_roof / 0.75)] 
>= Total_paving_area + Total_roof_area

Input form:
| Strategy | Area (SF) | Weight | Weighted Area |
|----------|-----------|--------|---------------|
| Nonroof: Shade | [input] | /0.5 | auto-calc |
| Nonroof: SR>=0.33 | [input] | /0.5 | auto-calc |
| Nonroof: Open-grid | [input] | /0.5 | auto-calc |
| High-reflectance roof (low-slope) | [input] | /0.75 | auto-calc |
| High-reflectance roof (steep-slope) | [input] | /0.75 | auto-calc |
| Vegetated roof | [input] | /0.75 | auto-calc |
| TOTAL | | | auto-sum |
| Required (paving + roof) | | | auto-calc |
| PASS/FAIL | | | auto-check |

STEP 4: Option 2 - Parking Under Cover
- User inputs: total parking spaces, spaces covered
- Check: covered / total = 100%
- Verify cover type: high-reflectance (SRI>=32) OR vegetated OR energy generation

STEP 5: Option 3 - Tree Equity Score
- API call to American Forests Tree Equity Score:
  * Input: project address/lat/lon
  * Output: priority ranking (high priority / highest priority / not priority)
- If high/highest priority: generate canopy cover improvement plan
- If not priority: flag that Option 3 is not available

STEP 6: Points Optimization
- Calculate points achievable per option:
  * Option 1: 1 point if equation passes
  * Option 2: 1 point if 100% covered
  * Option 3: 1 point if in priority area + canopy increase
- Recommend combination for maximum points (max 2)

STEP 7: Report Generation
- Auto-generated calculation table with all inputs
- Compliance pass/fail per option
- Product data summary table
- Shade plan template (10-year canopy widths)
- LLM-generated heat island reduction narrative

OUTPUT: Weighted calculation report + product compliance summary + Tree Equity Score + points optimization
```

**Estimated Time Savings:** 4-6 hours of calculation and product research → 30 minutes of data input and review

**Risk Factors:**
- CRRC database may not include all products
- Aged SRI values may not be available for all products
- Tree Equity Score API availability and terms of use
- Area measurements from drawings need verification
- Shade plan requires landscape architect input for 10-year canopy projections

**Data API Costs:**
- Tree Equity Score API: Free for basic lookups
- CRRC Database: Free web search
- Google Maps: Minimal for geocoding

**Final Recommendation:** **Automate in MVP** — Excellent calculation engine candidate, clear thresholds, multiple public data sources, low risk

---

### SSc6: LIGHT POLLUTION REDUCTION

**Scorecard:** Automation: 3 | Commercial Value: 3 | Risk: **Low**

**Overview:** Three requirements: uplight control, light trespass control, and signage luminance limits. All based on BUG (Backlight, Uplight, Glare) ratings from IES TM-15-11 and MLO lighting zones.

#### Documentation Type
Template checklist, drawing markup, compliance table

#### Required Inputs

| Input Category | Specific Source | Method |
|----------------|----------------|--------|
| **Public - MLO Lighting Zones** | Model Lighting Ordinance (IES/IDA) | Zone determination (LZ0-LZ4) |
| **Public - IES TM-15-11** | IES standard (purchase required) | BUG rating reference |
| **Upload - Lighting fixture schedule** | With BUG ratings from manufacturer | U, B, G ratings per luminaire |
| **Upload - Site lighting plan** | Luminaire locations and mounting heights | Distance to lighting boundary |
| **Upload - Signage schedule** | Internally illuminated signs with luminance | cd/m2 values |

#### AI Techniques Applicable
1. **Template-based document generation** (PRIMARY): Auto-generate BUG compliance tables per MLO zone
2. **LLM document analysis**: Extract BUG ratings from fixture schedules
3. **Web research agents**: Determine MLO lighting zone for project location (municipal ordinance lookup)
4. **Calculation engines**: Mounting height distance ratios (distance/MH), uplight/backlight/glare compliance verification
5. **Computer vision**: Analyze site lighting plans for luminaire count and boundary distances (preliminary)

#### Automation Blueprint (Score: 3)

```
STEP 1: Lighting Zone Determination
- Web agent researches project location's MLO lighting zone:
  * Search municipal lighting ordinance
  * Default zones: rural (LZ0), residential (LZ1), mixed (LZ2), 
    commercial (LZ3), high-activity (LZ4)
  * Confirm zone classification with consultant

STEP 2: Fixture Data Input
- User uploads lighting fixture schedule
- AI (LLM) extracts per luminaire:
  * BUG ratings: Uplight (U0-U5), Backlight (B0-B5), Glare (G0-G5)
  * Mounting height
  * Mounting location (ground, building, pole)
- OR: User manually inputs data in structured form

STEP 3: Site Layout Input
- User uploads site lighting plan
- AI identifies (or user inputs):
  * Lighting boundary location
  * Distance from each luminaire to lighting boundary
  * Mounting height for each luminaire

STEP 4: Automated Compliance Verification

  Uplight Check:
  | Zone | Max U | Each luminaire U rating | Pass/Fail |
  |------|-------|------------------------|-----------|
  | LZ0  | U0    | [from schedule]        | auto      |
  | LZ1  | U0    | [from schedule]        | auto      |
  | LZ2  | U2    | [from schedule]        | auto      |
  | LZ3  | U3    | [from schedule]        | auto      |
  | LZ4  | U4    | [from schedule]        | auto      |

  Backlight Check (distance/mounting height ratio):
  For each luminaire:
  - Calculate ratio = distance_to_boundary / mounting_height
  - Determine applicable B rating limit from table
  - Compare actual B rating vs. limit
  - Pass/Fail per luminaire

  Glare Check (similar to backlight):
  - Determine G rating limit from table
  - Compare actual G rating vs. limit
  - Pass/Fail per luminaire

STEP 5: Signage Luminance Check
- User inputs signage luminance values (cd/m2)
- Compare against zone limits:
  | Zone | Max cd/m2 | Actual | Pass/Fail |
  |------|-----------|--------|-----------|
  | LZ0  | 50        | [input]| auto      |
  | LZ1  | 50        | [input]| auto      |
  | LZ2  | 100       | [input]| auto      |
  | LZ3  | 200       | [input]| auto      |
  | LZ4  | 350       | [input]| auto      |

STEP 6: Exemption Processing
- User flags exempt fixtures (specialized signal, theatrical, etc.)
- Verify exemption conditions met
- Document separate controls for exempt fixtures

STEP 7: Compliance Report
- Auto-generated BUG compliance table
- Luminaire-by-luminaire pass/fail summary
- Signage luminance compliance table
- MLO zone determination documentation
- Exemption documentation (if applicable)

OUTPUT: Complete BUG compliance report + MLO zone documentation + pass/fail summary
```

**Estimated Time Savings:** 3-5 hours of manual table lookup and verification → 1 hour of data input

**Risk Factors:**
- IES TM-15-11 is a copyrighted standard (purchase required for full reference)
- BUG ratings from manufacturers may not be on all fixture schedules
- Distance measurements from lighting plan require careful interpretation
- Exemption determinations require professional judgment

**Final Recommendation:** **Automate Later** — Template generation and compliance checker are valuable, but lower priority than GIS-heavy credits

---

## PRIORITY RANKING & MVP RECOMMENDATION

### Top 5: Automate in MVP

| Rank | Credit | Auto | Value | Why MVP? | Est. Dev Effort |
|------|--------|------|-------|----------|-----------------|
| 1 | LTc3 | 5 | 5 | Highest points, 100% public data, instant ROI | Medium |
| 2 | SSc4 | 4 | 5 | Multi-hazard data fusion, huge time saver | High |
| 3 | SSc3 | 4 | 4 | Engineering calculation engine, reusable | Medium |
| 4 | SSc5 | 4 | 4 | Clear calculation logic, Tree Equity API | Low |
| 5 | LTc1 | 4 | 3 | GIS pipeline template reusable for other credits | Medium |

### Tier 2: Automate Later

| Rank | Credit | Auto | Value | Why Later? |
|------|--------|------|-------|-----------|
| 6 | LTc4 | 3 | 4 | Requires professional engineer input for VMT |
| 7 | SSc1 | 3 | 3 | Species research engine needs expert review |
| 8 | SSc6 | 3 | 3 | Template-based, lower commercial value |

### Tier 3: Assist Only

| Rank | Credit | Auto | Value | Why Assist Only? |
|------|--------|------|-------|-----------------|
| 9 | LTc2 | 2 | 2 | Document-heavy, authority letters |
| 10 | LTc5 | 2 | 2 | Simple calc, mostly uploaded drawings |
| 11 | SSp1 | 2 | 3 | Physical field verification required |
| 12 | SSc2 | 2 | 2 | Simple calc, uploaded design drawings |

---

## SHARED INFRASTRUCTURE RECOMMENDATIONS

### Core AI Components to Build

1. **GIS Data Pipeline** (reusable across LTc1, LTc3, LTc1, SSc3, SSc4, SSc5)
   - Unified interface for NRCS, FEMA, USGS, NOAA, EPA data APIs
   - Polygon-based overlay analysis engine
   - Buffer/setback distance calculation
   - Map visualization generation

2. **Transit Data Engine** (LTc3, LTc4)
   - GTFS feed parser with trip counting logic
   - Google Maps/Places API wrapper for proximity analysis
   - Walk Score API integration
   - Distance matrix calculation

3. **Calculation Engine** (LTc4, LTc5, SSc1, SSc3, SSc5, SSc6)
   - Formula execution with unit conversion
   - Threshold compliance checking
   - Points optimization logic
   - Report table generation

4. **Web Research Agent** (LTc1, LTc3, SSc1, SSc4, SSc5, SSc6)
   - Multi-source data retrieval
   - Standard/ordinance lookup
   - Product database queries
   - Climate/hazard data compilation

5. **Document Parser** (LTc2, LTc4, LTc5, SSc5, SSc6)
   - PDF extraction for product cut sheets
   - Fixture schedule parsing
   - Address/geocoding extraction
   - Value extraction from forms

6. **LLM Narrative Generator** (all credits scoring 3+)
   - Site assessment narratives
   - Compliance report generation
   - Strategy documentation
   - Plan template population

### Public API Integration Map

| API | Used By | Cost | Integration Complexity |
|-----|---------|------|----------------------|
| NRCS Soil Data Access | LTc1, SSc1, SSc3 | Free | Medium |
| FEMA NFHL | LTc1, SSc4 | Free | Medium |
| USGS 3DEP/NHDPlus/NWI | LTc1 | Free | Medium |
| NatureServe Web Services | LTc1 | Free | High (complex queries) |
| USGS PAD-US | LTc1 | Free | Low |
| Census/ACS API | LTc3, LTc2 | Free | Medium |
| Walk Score API | LTc3 | ~$0.05/call | Low |
| Google Maps API | LTc3, LTc4 | ~$5-20/analysis | Low |
| TransitLand/GTFS | LTc3, LTc4 | Free tier | Medium |
| OpenStreetMap Overpass | LTc3, LTc4 | Free | Medium |
| NOAA PFDS | SSc3 | Free | Low |
| NOAA Climate Data | SSc4 | Free | Medium |
| NOAA Sea Level Rise | SSc4 | Free | Low |
| EPA EJSCREEN | SSc4 | Free | Low |
| American Forests Tree Equity | SSc5 | Free | Low |
| CRRC Database | SSc5 | Free | Low |
| USDA PLANTS | SSc1 | Free | Medium |
| ABC Threat Factor DB | SSc1 | Free (web search) | High (no API) |
| NIFC Wildfire | SSc4 | Free | Medium |
| HUD AMI | LTc2 | Free | Low |

---

## RISK MITIGATION STRATEGIES

| Risk Category | Mitigation |
|--------------|------------|
| **Data accuracy** | Always flag "AI-generated, requires professional review" disclaimer |
| **Regulatory changes** | Cache data with timestamp; flag when data > 12 months old |
| **Jurisdiction variations** | Build modular pipelines that adapt to local data availability |
| **Professional liability** | Never claim to replace licensed professionals; position as "draft generator" |
| **USGBC review rejection** | Include all source citations; generate standard-format documentation |
| **Data API failures** | Graceful degradation with manual input fallback for each data source |
| **GIS coordinate errors** | Validate geocoded addresses against parcel boundaries |
| **Calculation errors** | Show all formulas and inputs; allow manual override of any value |

---

## IMPLEMENTATION ROADMAP

### Phase 1: MVP (Months 1-3) — 5 Credits
- **LTc3** (Compact & Connected): GIS + transit + Walk Score pipeline
- **SSc5** (Heat Island): Calculation engine + Tree Equity API
- **LTc1** (Sensitive Land): GIS multi-layer overlay pipeline
- **SSc3** (Rainwater): NOAA + NRCS calculation engine
- **SSc4** (Resilient Site): Multi-hazard web research agent

**MVP Points Coverage:** 12-16 LT points + 8-10 SS points = ~20-26 of 26 total points

### Phase 2: Enhancement (Months 4-6) — 3 Credits
- **LTc4** (TDM): Calculation engine + bike network analysis
- **SSc1** (Biodiverse Habitat): Species research engine + area calculator
- **SSc6** (Light Pollution): BUG compliance checker + template generator

### Phase 3: Assist Tools (Months 7-9) — 4 Credits
- **LTc2**: AMI lookup tool, document templates
- **LTc5**: EVSE/EV-ready calculator
- **SSp1**: Erosion control plan template, inspection log generator
- **SSc2**: Outdoor space compliance calculator

---

*Analysis complete. Total credits analyzed: 12. Recommended for MVP: 5. Total potential points automated: 20-26 of 26.*
