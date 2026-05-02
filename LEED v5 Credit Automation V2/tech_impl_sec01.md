# Master Technical Implementation Document
## Deer-Flow LEED v5 Credit Automation Platform

---

# Section 1: Executive Summary

## 1.1 Platform Purpose and Scope

The Deer-Flow LEED v5 Credit Automation Platform is an enterprise-grade AI orchestration system designed to automate the data collection, calculation, and documentation workflows required for Leadership in Energy and Environmental Design (LEED) v5 Building Design and Construction (BD+C) certification. Built on the Deer-Flow agent orchestration framework, the platform decomposes each LEED credit into discrete, executable skills that leverage 261 verified external data sources to eliminate manual data gathering, reduce calculation errors, and compress certification timelines from months to weeks.

LEED v5 represents the most significant revision to the rating system in over a decade, introducing mandatory prerequisites across all credit categories and increasing the granularity of performance thresholds. The platform addresses the critical bottleneck in LEED certification: the project team's dependency on fragmented, manually-sourced data from government databases, commercial registries, manufacturer documentation, and proprietary energy models. By establishing machine-readable API integrations across the entire data ecosystem, the platform enables continuous compliance monitoring rather than the traditional batch-and-review model.

## 1.2 Tier 1 Skill Architecture: 16 Skills Covering 40+ Points

The platform implements 16 Tier 1 automation skills, each mapped directly to one or more LEED v5 credits with automation scores of 90 or above. These skills represent the highest-confidence, highest-value automation opportunities and collectively cover over 40 certification points.

| Tier 1 Skill | LEED Credit(s) | Points | Automation Score |
|-------------|----------------|--------|-----------------|
| Carbon Assessment Engine | IPp3, EAp1 | 3 | 95 |
| Sensitive Land Protector | LTc1 | 2 | 95 |
| Light Pollution Calculator | SSc6 | 1 | 95 |
| Embodied Carbon Quantifier | MRp2, MRc2 | 4 | 95 |
| LEED AP Verifier | PRc2 | 1 | 95 |
| Human Impact Assessor | IPp2 | 2 | 90 |
| Compact Development Analyzer | LTc3 | 2 | 90 |
| Rainwater Manager | SSc3 | 2 | 90 |
| Water Efficiency Validator | WEp2 | 2 | 90 |
| Decarbonization Planner | EAp1 | 3 | 90 |
| Refrigerant Compliance Checker | EAp5, EAc7 | 2 | 90 |
| Renewable Energy Estimator | EAc4 | 3 | 90 |
| Low-Emitting Materials Scanner | MRc3 | 2 | 90 |
| Product Procurement Validator | MRc4 | 2 | 90 |
| Heat Island Reducer | SSc5 | 2 | 95 |
| Transit Access Analyzer | LTc3, LTc4 | 2 | 90 |

Each Tier 1 skill is implemented as a Deer-Flow workflow composed of data ingestion nodes, validation gates, calculation engines, and human-in-the-loop (HITL) checkpoints. Skills are triggered by project milestones (design development, construction documents, final completion) and produce USGBC-ready documentation packages in PDF and XML formats.

## 1.3 Data Source Ecosystem: 261 Verified Sources

The platform integrates with 261 distinct data sources across four categories:

| Category | Count | Primary Providers | Access Model |
|----------|-------|-------------------|-------------|
| Government APIs & Databases | 89 | NOAA, EPA, FEMA, USGS, Census, NREL, USFWS, NRCS | Free with registration |
| Commercial Databases & Tools | 67 | EC3, Tally, One Click LCA, EPD Registry, HPD Collaborative | License / Subscription |
| Industry Registries & Certifications | 58 | GREENGUARD, FloorScore, ENERGY STAR, Green-e, CRRC, AHRI | Mixed free / paid |
| GIS, Transit & Software APIs | 47 | USGS National Map, GTFS, Walk Score, Autodesk, ArcGIS, Google Maps | API key / subscription |

Each source has been evaluated for API availability, data quality, update frequency, and licensing terms. The platform maintains a source health monitoring dashboard that tracks API uptime, rate limit consumption, and data freshness. When a source becomes unavailable, the fallback chain automatically promotes secondary sources or triggers HITL escalation.

## 1.4 Time-to-Value: 10-Week Delivery Advantage

Building a LEED automation platform from scratch requires approximately 40-48 weeks of engineering effort distributed across API discovery and integration (16 weeks), calculation engine development (12 weeks), document generation (8 weeks), and testing / compliance validation (8 weeks). The Deer-Flow reference architecture reduces this to 10 weeks through:

1. **Pre-built API Connectors**: 40+ API connectors with OAuth, API key, and certificate-based authentication patterns are pre-implemented. Each connector includes retry logic, rate limit management, and data transformation pipelines.

2. **Calculation Template Library**: 28 pre-validated calculation templates covering carbon summation, percentage reduction, area-weighted averages, ASHRAE formula implementations, and runoff volume modeling. Templates are parameterized by climate zone, building type, and project phase.

3. **Document Generation Pipeline**: USGBC-compliant documentation templates with automated data population, signature workflows, and submission-ready formatting. Supports both PDF and the USGBC Arc platform XML schema.

4. **Compliance Validation Engine**: Automated cross-checks against LEED v5 reference guides, including threshold validation, prerequisite sequencing, and credit interdependency verification.

| Milestone | From-Scratch Timeline | Deer-Flow Timeline | Savings |
|-----------|----------------------|-------------------|---------|
| API Integration Complete | Week 16 | Week 3 | 13 weeks |
| Calculation Engine Ready | Week 28 | Week 5 | 23 weeks |
| Document Pipeline Operational | Week 36 | Week 7 | 29 weeks |
| Full Platform in Production | Week 48 | Week 10 | 38 weeks |

## 1.5 Three-Tier Automation Classification

The platform classifies every LEED credit into one of three automation tiers based on data availability, calculation complexity, and the need for human judgment.

**Tier 1: Fully Automated (16 credits, 31%)**
Credits where all required data is available via API, calculations are deterministic, and outputs can be generated without human review. Examples: IPp3 Carbon Assessment (EPA eGRID + EC3), LTc1 Sensitive Land Protection (FEMA NFHL + USFWS), SSc6 Light Pollution Reduction (IES TM-15-11 static data + manufacturer specs).

**Tier 2: Semi-Automated with HITL (22 credits, 43%)**
Credits where data ingestion and preliminary calculations are automated, but a human reviewer must confirm outputs, adjust assumptions, or interpret qualitative criteria. Examples: IPc1 Integrative Design Process (data gathering automated, but charrette documentation requires team review), EQc2 Thermal Comfort (model inputs automated, but comfort zone selection requires designer judgment).

**Tier 3: Human-Led with Data Support (13 credits, 25%)**
Credits where the platform serves as a data aggregator and calculation assistant, but the core certification work remains human-driven. Examples: PRc1 Innovation (creative solutions cannot be automated), IPc2 Legal Review (contractual language requires attorney review).

| Tier | Credits | Points Covered | Automation Strategy |
|------|---------|----------------|---------------------|
| 1 - Fully Automated | 16 | 40+ | Unattended execution, exception-only HITL |
| 2 - Semi-Automated | 22 | 35+ | Automated ingestion + human confirmation gates |
| 3 - Human-Led | 13 | 15+ | Data aggregation, template generation, validation |

---

# Section 2: Expanded Data Availability Analysis

## 2.1 Government API Catalog

The following table catalogs the primary government APIs integrated into the Deer-Flow platform. Each entry includes authentication requirements, rate limits, supported credits, regional applicability, and integration complexity rating. All government APIs listed provide free public access with registration.

| API Name | Provider | URL | Auth | Rate Limit | Credits Supported | Regional | Complexity |
|----------|----------|-----|------|-----------|-------------------|----------|------------|
| NOAA Climate Data Online | National Oceanic and Atmospheric Administration | https://www.ncdc.noaa.gov/cdo-web/webservices | API Key (free registration) | 1,000 requests/day | IPp1, SSc3, SSp1 | US territories | Low |
| NOAA Precipitation Frequency Data Server | NOAA / NWS | https://hdsc.nws.noaa.gov/hdsc/pfds/ | None (web services) | No limits | SSc3 | US territories | Low |
| FEMA Flood Map Service Center | Federal Emergency Management Agency | https://msc.fema.gov/portal/advanceSearch | None (basic), API key (advanced) | Reasonable use policy | IPp1, LTc1 | US only | Low |
| FEMA NFHL Web Services | FEMA | https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer | Public access | No limits (WMS/WFS) | LTc1, LTc2 | US only | Low |
| EPA eGRID | Environmental Protection Agency | https://www.epa.gov/egrid | Public access | No limits | IPp3, EAp1, EAc4 | US only | Low |
| EPA EJScreen | EPA | https://www.epa.gov/ejscreen | Public access | No limits | IPp2 | US only | Low |
| EPA AQI API (AirNow) | EPA | https://www.airnowapi.org/aqforecast | API Key (free) | 500 requests/day | EQp2 | US only | Low |
| EPA SNAP Program Database | EPA | https://www.epa.gov/snap | Public access | No limits | EAp5, EAc7 | US + international (Montreal Protocol) | Low |
| EPA Brownfields API | EPA | https://www.epa.gov/brownfields | Public access | No limits | LTc2 | US only | Low |
| EPA Envirofacts | EPA | https://www.epa.gov/enviro | Public access | No limits | Multiple (facility-level) | US only | Low |
| US Census Bureau API | US Census Bureau | https://www.census.gov/data/developers.html | API Key (free) | Variable by endpoint | IPp2, LTc2, LTc3 | US only | Medium |
| USGS National Map API | US Geological Survey | https://nationalmap.gov/ | None | Reasonable use | LTc1, SSp1 | US territories | Medium |
| USGS 3DEP Elevation Service | USGS | https://apps.nationalmap.gov/epqs/ | None | No limits | LTc1, SSc5 | US territories | Low |
| NREL PVWatts API | National Renewable Energy Laboratory | https://developer.nrel.gov/docs/solar/pvwatts/ | API Key (free registration) | 1,000 requests/day | EAc4 | US territories + international (limited) | Low |
| NREL NSRDB | NREL | https://nsrdb.nrel.gov/ | API Key (free) | Bulk download + API | EAc4 | Americas + limited global | Low |
| USFWS Critical Habitat API | US Fish & Wildlife Service | https://ecos.fws.gov/ecp/ | None | No limits | LTc1 | US only | Low |
| NRCS Soil Survey API | USDA Natural Resources Conservation Service | https://sdmdataaccess.sc.egov.usda.gov/ | None | Reasonable use | SSc3, SSp1 | US territories | Medium |
| USDA PLANTS Database | USDA | https://plants.usda.gov/ | None | No limits | SSc2, SSc4 | US territories | Low |
| NWS API | National Weather Service | https://api.weather.gov | None | Public access | IPp1, SSc3 | US territories | Low |
| National Wetlands Inventory | USFWS | https://www.fws.gov/program/national-wetlands-inventory | None (GIS layers) | No limits | LTc1 | US only | Low |

### Authentication and Rate Limit Management

All government API connectors implement a unified authentication handler supporting four patterns: API key header (`X-API-Key`), OAuth 2.0 bearer tokens, certificate-based mutual TLS (for BAS protocols), and unauthenticated public access. Rate limit handling uses a token bucket algorithm with exponential backoff. The connector configuration schema is:

```json
{
  "api_name": "epa_egrid",
  "auth_type": "none",
  "rate_limit": {
    "requests_per_day": null,
    "requests_per_minute": null,
    "concurrent_limit": 10,
    "backoff_strategy": "exponential"
  },
  "fallback_chain": ["epa_egrid_static_annual", "eia_grid_emissions"],
  "data_freshness_hours": 8760,
  "region": "US",
  "health_check_endpoint": "/status"
}
```

### Regional Limitations

Government APIs listed above are **US-only** unless explicitly noted. The FEMA flood map services, USFWS habitat data, and EPA EJScreen are tied to US federal jurisdiction and have no equivalent coverage in Canada, EU, or other regions. The NOAA climate APIs provide limited coverage for US territories (Puerto Rico, Guam, USVI). NREL PVWatts includes select international locations but with reduced solar resource data accuracy. For international deployments, the platform substitutes equivalent regional data sources (e.g., EU Copernicus for climate data, EEA for air quality, Eurostat for demographics) via a region-aware source router.

## 2.2 Industry & Commercial API Catalog

The following table catalogs commercial and industry-specific APIs integrated into the platform. These sources typically require licenses, subscriptions, or commercial agreements. Cost estimates are provided where publicly available.

| API Name | Provider | Auth | Cost | Credits Supported | Regional | Complexity |
|----------|----------|------|------|-------------------|----------|------------|
| EC3 Database API | Building Transparency | API Key (free registration) | Free for research; commercial licensing available | IPp3, MRp2, MRc2 | Global (materials-focused) | Medium |
| Tally API | Building Transparency / Autodesk | License + API Key | License-dependent (Revit plugin + cloud API) | IPp3, MRp2, MRc2 | Global | Medium |
| One Click LCA API | One Click LCA Ltd | API Token (license required) | License-dependent (contact provider) | MRp2, MRc2 | Global (region-specific databases) | Medium |
| EPD Registry | EPD International / ECO Platform | API available on request | Free search; API pricing on request | MRc4 | Global | Low |
| HPD Repository API | Health Product Declaration Collaborative | Registration required | API for data partners (contact provider) | MRc4 | Primarily US/EU | Medium |
| GREENGUARD Certification Database | UL Environment | Public access | Free | MRc3 | Global | Low |
| FloorScore Certification Database | RFCI | Public access | Free | MRc3 | Global | Low |
| Walk Score API | Walk Score / Redfin | API Key (paid) | By subscription tier ($2,000+/year for commercial) | LTc3 | US/Canada primary; limited global | Low |
| ENERGY STAR Product API | EPA | Public access | Free | WEp2, LTc5 | US territories | Low |
| ENERGY STAR Portfolio Manager API | EPA | API Key (free) | Free | EAp4, EAc5 | US only | Medium |
| GBCI Credential Directory | Green Business Certification Inc | API access on request | Contact GBCI | PRc2 | Global | Low |
| Cool Roof Rating Council | CRRC | Public access | Free (product search); API on request | SSc5 | US primary; international products | Low |
| Green-e Registry | Center for Resource Solutions | Public access | Free | EAc4 | North America primary | Low |
| AHRI Directory | Air-Conditioning, Heating, and Refrigeration Institute | Public access | Free | EAp5, EAc7, EAc3 | US/Canada | Low |
| USGBC Arc Platform API | US Green Building Council | OAuth 2.0 | Contact USGBC | All reporting credits | Global | Medium |

### Cost and Licensing Architecture

The platform implements a tiered licensing module that tracks API usage against project budgets. Commercial APIs are classified into four cost tiers:

| Tier | Annual Cost Range | Examples | Billing Model |
|------|-------------------|----------|--------------|
| Free / Open Access | $0 | EPA eGRID, NOAA, USGS, ENERGY STAR | N/A |
| Registration-Based | $0-$500 | NREL, EC3 (research tier), Census | API key required |
| Subscription | $1,000-$10,000 | Walk Score, One Click LCA, Tally | Monthly/annual license |
| Enterprise Negotiated | $10,000+ | USGBC Arc, Autodesk Forge, IES VE | Custom agreement |

The platform's API gateway module enforces per-project budget caps and provides cost attribution by credit, enabling project managers to understand data acquisition costs at the credit level.

## 2.3 Calculation Engine Data Sources

The calculation engine maps each LEED v5 calculation type to verified data sources and establishes transformation pipelines from raw API output to credit-compliant inputs.

### 2.3.1 Calculation-to-Source Mapping Matrix

| Calculation Type | Occurrences | Primary Data Sources | Secondary Sources | Formula Complexity | Validation Rule |
|-----------------|-------------|---------------------|-------------------|-------------------|-----------------|
| Carbon / GWP Calculations | 19 | EPA eGRID (grid EF), EC3 (embodied carbon), IPCC AR6 (GWP values), Tally/One Click LCA (building LCA) | EPA GHGRP, DEFRA (UK), IEA emission factors | Medium-High | Cross-check against IPCC AR6 Table 7.15; verify EC3 data vintage matches reporting year |
| Database / Verification | 18 | EPD Registry, HPD Repository, GREENGUARD, FloorScore, FSC Certificate DB, Green-e Registry | UL SPOT, SCS Global, Cradle to Cradle | Low | Certification expiry date within project construction period; verify certificate scope matches product category |
| Area / Volume / Quantity | 17 | Autodesk Revit API (BIM extraction), Autodesk Forge (geometry), Procore (quantity tracking), Building specs | Manual take-offs, 2D drawings, spreadsheet uploads | Low-Medium | BIM-to-spec reconciliation: ±5% tolerance; flag discrepancies for HITL review |
| Percentage / Reduction | 16 | EnergyPlus outputs (energy %), EPA WaterSense (water %), EC3 (carbon %), ENERGY STAR (efficiency %) | ASHRAE 90.1 baseline models, local utility incentives | Low | Baseline must match ASHRAE 90.1-2022 Appendix G for BD+C; percentage rounded to nearest whole number per LEED guidance |
| Water Calculations | 7 | EPA WaterSense Product DB (fixture flow rates), NOAA Atlas 14 (precipitation), NRCS Soil Survey (infiltration), SWMM (runoff modeling) | Local stormwater manuals, manufacturer cut sheets | Medium | Fixture flow rates ≤ WaterSense labeled values; runoff volume matches 95th percentile storm (NOAA Atlas 14) |
| Ventilation / IAQ | 7 | ASHRAE 62.1-2022 (ventilation rates), CBE Thermal Comfort Tool, IAQ sensor APIs (PM2.5, CO2, TVOC) | EPA Indoor airPLUS, OSHA standards, manufacturer specs | Medium | Ventilation rate compliance: outdoor air per person and per area; CO2 ≤ 1,000 ppm continuous |
| Daylight / Lighting | 5 | Radiance/DIVA/ClimateStudio (sDA/ASE), IES TM-15-11 (BUG ratings), DIALux/Relux (LPD calculations) | Manufacturer photometric files, site photos | Medium-High | sDA ≥ 50%, ASE ≤ 10% (LEED v5 thresholds); LPD ≤ ASHRAE 90.1-2022 by space type |
| SRI / Reflectance | 3 | CRRC Rated Products Database (SRI values), manufacturer test data (ASTM E1980), Tree Equity Score (shade area) | ASTM E903 (solar reflectance), ASTM E408 (emittance) | Low | SRI ≥ 29 (non-roof), SRI ≥ 82 (low-slope roof) per LEED v5; CRRC rating within 3 years |
| Transit / Density | 4 | Walk Score API, GTFS feeds (2000+ agencies), US Census API (population density), Google Maps (distance matrix) | Local transit authority data, OpenStreetMap, parcel databases | Low-Medium | Transit service frequency ≥ 72 trips/weekday; density calculation uses Census block group or parcel data |
| Energy Production | 3 | NREL PVWatts (solar production), NREL NSRDB (solar resource), Green-e Registry (REC verification) | SAM (System Advisor Model), local utility net metering rules | Medium | PVWatts simulation must use NSRDB TMY data for project location; production estimates ±10% of measured for existing buildings |
| Grid Emission Factors | 4 | EPA eGRID (annual), EPA GHGRP (facility-level), EIA Electric Power Monthly (state-level) | IPCC default factors, IEA electricity data (international) | Low | Use eGRID subregion for project location; if location unknown, use national average with documentation |
| Refrigerant GWP | 2 | EPA SNAP Program (approved refrigerants), IPCC AR6 (GWP values), AHRI Directory (equipment data) | UNEP Ozone Secretariat, ASHRAE 34 safety classifications | Low | Refrigerant must be on EPA SNAP approved list for application type; GWP from IPCC AR6 Table 7.15 |
| Demographic / EJ | 3 | US Census API (ACS 5-Year), EPA EJScreen (12 environmental + 6 demographic indicators), HUD Housing Data | State-level health department data, local equity assessments | Low | ACS data vintage must be within 5 years of project registration; block group level minimum |
| Flood / Hazard | 3 | FEMA NFHL (flood zones), USGS 3DEP (elevation/slope), NOAA Storm Events Database | State geological surveys, local floodplain administrators | Low | Flood zone determination from NFHL, not FIRMette sketches; 100-year floodplain buffer ≥ 100 feet |
| Soil / Infiltration | 2 | NRCS Soil Survey (hydrologic group, infiltration rate), OpenTopography (3DEP lidar) | Local soil conservation districts, geotechnical reports | Low-Medium | Soil group from SSURGO; infiltration rate for design storm per local stormwater manual |

### 2.3.2 Calculation Pipeline Architecture

Each calculation type follows a standardized pipeline with five stages:

1. **Data Ingestion**: API calls to primary sources with automatic retry and fallback
2. **Validation Gate**: Schema validation, range checks, and freshness verification
3. **Transformation**: Raw API response → normalized calculation inputs via mapping tables
4. **Execution**: Deterministic calculation using pre-validated formula templates
5. **Output Formatting**: LEED-compliant output with units, precision, and reference citations

Example pipeline for Embodied Carbon (MRp2 / MRc2):

```python
# Stage 1: Data Ingestion
ec3_response = ec3_api.query(material_category="concrete", region="US-Northeast")
epd_response = epd_registry.query(product_type="ready_mix_concrete", valid=True)

# Stage 2: Validation Gate
assert ec3_response.gwp_unit == "kgCO2e"  # Unit consistency check
assert epd_response.validity_date > project_start_date  # Freshness check
assert 0 < ec3_response.gwp_value < 1000  # Range check (sanity)

# Stage 3: Transformation
normalized_inputs = {
    "material_quantities": revit_api.get_material_takeoff(),
    "gwp_factors": ec3_response.get_factors_by_material(),
    "epd_verifications": epd_response.get_certification_status()
}

# Stage 4: Execution
total_embodied_carbon = sum(
    qty * gwp for qty, gwp in normalized_inputs["material_quantities"].items()
)
reduction_percentage = (baseline_carbon - total_embodied_carbon) / baseline_carbon * 100

# Stage 5: Output Formatting
output = {
    "total_embodied_carbon_kgco2e": round(total_embodied_carbon, 0),
    "reduction_percentage": round(reduction_percentage, 1),
    "baseline_source": "EC3 2024 Material Baselines",
    "data_vintage": "2024-Q2",
    "epd_coverage_percent": epd_coverage,
    "compliance_status": "Pass" if reduction_percentage >= 10 else "Fail"
}
```

## 2.4 Regional Availability Matrix

The following matrix assesses data availability by region and LEED credit category. Status definitions: **Full** = all required data sources available with equivalent coverage to US; **Limited** = partial coverage or lower data quality; **Unavailable** = no equivalent regional source identified.

| Region | IP - Integrative Process | LT - Location & Transportation | SS - Sustainable Sites | WE - Water Efficiency | EA - Energy & Atmosphere | MR - Materials & Resources | EQ - Indoor Environmental Quality | PR - Project Priorities |
|--------|-------------------------|--------------------------------|----------------------|----------------------|-------------------------|---------------------------|-----------------------------------|------------------------|
| **United States** | Full (Census, EJScreen, eGRID, NOAA) | Full (FEMA, USFWS, Census, Walk Score, GTFS) | Full (NOAA, NRCS, USGS, CRRC) | Full (WaterSense, ENERGY STAR, fixture DBs) | Full (eGRID, PVWatts, ENERGY STAR, SNAP) | Full (EC3, EPD, HPD, GREENGUARD, Green-e) | Full (AirNow, ASHRAE, AHRI) | Full (GBCI Directory) |
| **Canada** | Limited (No EJScreen; StatsCan replaces Census; limited grid emission detail) | Limited (No FEMA equivalent; provincial flood maps; limited Walk Score) | Limited (Environment Canada climate data; NRCS equivalent varies by province) | Full (CSA standards, Natural Resources Canada fixture ratings) | Limited (No eGRID; provincial grid data fragmented; no PVWatts TMY for all locations) | Full (EC3 global, EPD Registry, FSC Canada) | Full (CSA F280, AHRI Canada, GREENGUARD) | Full (GBCI Canada) |
| **EU / UK** | Limited (Eurostat replaces Census; no EJ screening equivalent; EEA air quality) | Limited (No FEMA; JRC flood data partial; Google Maps / OSM transit) | Limited (Copernicus climate; no NRCS; EEA soil data coarse) | Limited (No WaterSense; national fixture standards vary) | Limited (No eGRID; ENTSO-E grid data complex; limited solar resource APIs) | Full (ECO Platform EPDs, EC3 EU, HPD Collaborative) | Full (EN 16798, CEN standards, GREENGUARD EU) | Full (GBCI Europe) |
| **Australia / NZ** | Limited (ABS data; no EJ screening; limited grid emission detail) | Limited (Geoscience Australia flood; no FEMA; transit data via GTFS AU) | Limited (BOM climate; no NRCS; CSIRO soil data partial) | Limited (WELS ratings; no WaterSense; WaterMark certification) | Limited (AEMO grid data; no PVWatts; limited solar APIs) | Full (EC3 ANZ, EPD Australasia, GECA) | Full (NCC Section J, GREENGUARD AU) | Full (GBCI APAC) |
| **Asia-Pacific (excl. AU/NZ)** | Unavailable (No unified census API; limited EJ data) | Limited (Local transit APIs; no unified flood data; limited Walk Score) | Limited (Local meteorological agencies; no unified soil data) | Limited (National standards vary widely; no unified fixture DB) | Limited (National grid data only; limited renewable energy APIs) | Limited (Local EPD programs; EC3 limited Asia coverage) | Limited (ASHRAE adopted; local IAQ standards vary) | Full (GBCI APAC) |
| **Middle East** | Unavailable (Limited demographic APIs; no EJ screening) | Unavailable (No unified flood or habitat data; limited transit) | Limited (Local climate data; no regional soil survey API) | Limited (No unified fixture DB; local water standards) | Limited (No grid emission API; limited solar resource data) | Limited (EC3 limited ME coverage; local certification programs) | Limited (ASHRAE 55 adopted; limited product cert DBs) | Full (GBCI Middle East) |
| **Latin America** | Unavailable (Limited census APIs; no EJ screening) | Limited (Local hazard maps; no unified flood API; limited GTFS) | Limited (Local meteorological data; no unified soil survey) | Limited (No unified fixture DB; local water standards vary) | Limited (National grid data only; limited renewable APIs) | Limited (EC3 limited LATAM; local EPD programs emerging) | Limited (ASHRAE adopted; limited local product certs) | Full (GBCI Latin America) |

### Regional Fallback Strategies

When operating in regions with **Limited** or **Unavailable** data coverage, the platform applies the following fallback hierarchy:

1. **Source Substitution**: Replace US-specific APIs with regional equivalents (e.g., Eurostat for Census, EEA for air quality, Copernicus for climate). The source router module maintains a mapping of equivalent sources by region.

2. **Static Data Ingestion**: For sources with no API equivalent, the platform ingests published static datasets (e.g., ENTSO-E annual grid emission reports, IPCC default emission factors) and applies them as baseline values.

3. **HITL Escalation**: When automated data coverage falls below 60% for a given credit, the workflow escalates to a human analyst who manually sources the required data through the platform's data entry interface. The analyst's inputs are validated against range rules and stored for future reuse.

4. **Third-Party Data Procurement**: For enterprise clients, the platform supports integration with commercial data providers (e.g., Moody's ESG, S&P Global) that offer international coverage for environmental and demographic indicators.

| Region | Fallback Data Procurement Cost (per project) | Manual Data Entry Hours | HITL Trigger Rate |
|--------|---------------------------------------------|------------------------|-------------------|
| US | $0 | 0-4 hours | <5% |
| Canada | $500-$2,000 | 4-12 hours | 10-15% |
| EU/UK | $2,000-$5,000 | 8-20 hours | 15-25% |
| Australia/NZ | $1,000-$3,000 | 6-16 hours | 15-20% |
| Asia-Pacific | $5,000-$15,000 | 20-40 hours | 30-50% |
| Middle East | $5,000-$15,000 | 20-40 hours | 30-50% |
| Latin America | $3,000-$10,000 | 16-32 hours | 25-40% |

## 2.5 Real-Time vs. Batch Data Classification

The platform classifies each credit's data requirements by temporal access pattern: **Real-Time** (API calls at time of credit execution), **Batch** (pre-loaded static datasets updated periodically), or **Mixed** (combination of both).

| Credit | Credit Name | Real-Time Data Sources | Batch Data Sources | Classification |
|--------|------------|----------------------|-------------------|----------------|
| IPp1 | Climate Resilience | NOAA Climate Data API, NWS API, AirNow | IPCC climate projections, ASHRAE climate zones | Mixed |
| IPp2 | Human Impact Assessment | Census API, EPA EJScreen | HUD housing data, local health data | Mixed |
| IPp3 | Carbon Assessment | EPA eGRID, EC3 API | IPCC AR6 GWP values, EC3 annual baselines | Mixed |
| IPc1 | Integrative Design Process | NREL energy target data | ASHRAE standards, benchmark databases | Mixed |
| IPc2 | Legal Review | -- | Contract templates, legal precedent databases | Batch |
| LTp1 | Construction Activity Pollution Prevention | AirNow, local air quality monitors | EPA stormwater regulations, state SWPPP templates | Mixed |
| LTc1 | Sensitive Land Protection | FEMA NFHL, USFWS Critical Habitat, USGS 3DEP | National Wetlands Inventory (static layers), state critical areas | Mixed |
| LTc2 | Priority Considerations | EPA Brownfields, FEMA NFHL | State brownfield registries, local redevelopment plans | Mixed |
| LTc3 | Compact and Connected Development | Walk Score API, GTFS feeds, Census API | Local zoning maps, parcel databases, transit ridership | Mixed |
| LTc4 | Low-Carbon Transportation | GTFS Realtime, Walk Score | EPA fuel economy ratings, local EV incentive programs | Mixed |
| LTc5 | EV Infrastructure | ENERGY STAR EVSE registry | Local building codes, utility EV programs | Mixed |
| SSp1 | Site Assessment | USGS National Map, NRCS Soil Survey | Local ecological surveys, state natural heritage programs | Mixed |
| SSc2 | Habitat Conservation | USFWS, USDA PLANTS | Local native plant lists, state wildlife action plans | Mixed |
| SSc3 | Rainwater Management | NOAA Atlas 14, NRCS Soil Survey | Local stormwater manuals, state design rainfall tables | Mixed |
| SSc4 | Heat Resilience | NOAA Climate Data, NWS | Tree Equity Score (annual), urban heat island studies | Mixed |
| SSc5 | Heat Island Reduction | CRRC (real-time search) | IES TM-15-11 (static), manufacturer photometric data | Mixed |
| SSc6 | Light Pollution Reduction | -- | IES TM-15-11 BUG ratings (static), manufacturer cut sheets | Batch |
| SSc7 | Site Outdoor Lighting | -- | IES RP-8 (static), manufacturer photometric files | Batch |
| WEp1 | Water Use Reduction | Smart water meter APIs | EPA WaterSense product DB, fixture manufacturer specs | Mixed |
| WEp2 | Minimum Water Efficiency | ENERGY STAR Product API | EPA WaterSense Product DB, ASHRAE 189.1 | Mixed |
| WEc1 | Water Use Reduction | Smart water meter APIs, Green Button (interval data) | EPA WaterSense, SWMM model parameters | Mixed |
| EAp1 | Operational Carbon Projection | EPA eGRID, NREL PVWatts | EnergyPlus baseline models, ASHRAE 90.1-2022 | Mixed |
| EAp2 | Minimum Energy Performance | EnergyPlus / Eppy | ASHRAE 90.1-2022 Appendix G, CBECS benchmark data | Mixed |
| EAp3 | Fundamental Commissioning | Procore API (project status) | ASHRAE standards, commissioning templates | Mixed |
| EAp4 | Energy Performance | Green Button API, smart meter APIs | ENERGY STAR Portfolio Manager, utility rate schedules | Mixed |
| EAp5 | Fundamental Refrigerant Management | EPA SNAP, AHRI Directory | Montreal Protocol schedules (static), IPCC GWP values | Mixed |
| EAc2 | Optimize Energy Performance | EnergyPlus / Eppy | ASHRAE 90.1-2022, local utility incentive databases | Mixed |
| EAc3 | Advanced Energy Metering | BAS/BMS protocols (BACnet) | ASHRAE 202 metering guidelines, utility data access protocols | Mixed |
| EAc4 | Renewable Energy | NREL PVWatts, Green-e Registry | NSRDB solar resource data (annual), REC verification databases | Mixed |
| EAc5 | Enhanced Commissioning | Procore API, IES VE | Commissioning report templates, ASHRAE 202 | Mixed |
| EAc6 | Demand Response | OpenADR API | Utility DR program data, grid operator signals | Mixed |
| EAc7 | Enhanced Refrigerant Management | EPA SNAP, AHRI Directory | IPCC AR6 GWP values, refrigerant charge calculators | Mixed |
| MRp1 | Building Life-Cycle Impact Reduction | EC3 API, EPD Registry | Building longevity databases, adaptive reuse case studies | Mixed |
| MRp2 | Quantify Embodied Carbon | EC3 API, Tally API | EC3 annual baselines, material take-off templates | Mixed |
| MRc1 | Building Life-Cycle Impact Reduction | EC3 API, EPD Registry | Historic preservation databases, structural assessment standards | Mixed |
| MRc2 | Reduce Embodied Carbon | EC3 API, Tally API, One Click LCA | EC3 baselines, EPD validation databases | Mixed |
| MRc3 | Low-Emitting Materials | GREENGUARD DB, FloorScore DB | CDPH Standard Method (static), manufacturer VOC test reports | Mixed |
| MRc4 | Product Selection & Procurement | EPD Registry, HPD API, FSC DB | Green-e, SCS Global, Cradle to Cradle certifications | Mixed |
| MRc5 | Construction Waste Management | Procore API | Local waste diversion facility databases, EPA WARM model | Mixed |
| EQp1 | Minimum IAQ Performance | AirNow, IAQ sensor APIs | ASHRAE 62.1-2022, manufacturer filtration data | Mixed |
| EQp2 | Environmental Tobacco Smoke | AirNow (outdoor air quality) | Local smoking ordinances, building code requirements | Mixed |
| EQp3 | Construction IAQ Management | IAQ sensor APIs | SMACNA IAQ guidelines, manufacturer low-emitting product data | Mixed |
| EQc1 | Outdoor Air Delivery | BAS/BMS protocols | ASHRAE 62.1 ventilation tables, airflow measurement standards | Mixed |
| EQc2 | Thermal Comfort | IAQ sensor APIs (temp, humidity) | CBE Thermal Comfort Tool, ASHRAE 55-2023 | Mixed |
| EQc3 | Daylight | -- | Radiance/DIVA simulation outputs, IES LM-83-12 | Batch |
| EQc4 | Glare Control | -- | DGP simulation outputs, manufacturer shading data | Batch |
| EQc5 | IAQ Assessment | IAQ sensor APIs (PM2.5, CO2, TVOC) | EPA Indoor airPLUS, manufacturer sensor calibration data | Mixed |
| EQc6 | Interior Lighting | -- | IES RP-1 (static), manufacturer photometric data | Batch |
| EQc7 | Daylighting Controls | -- | Daylight autonomy simulation outputs | Batch |
| PRp1 | LEED Accredited Professional | GBCI Credential Directory | -- | Real-Time |
| PRc1 | Innovation | -- | -- | Human-Led |
| PRc2 | LEED AP | GBCI Credential Directory | LEED AP specialty requirements (static) | Real-Time |

### Data Freshness Requirements

| Data Category | Update Frequency | Source Examples | Staleness Threshold | Action on Stale Data |
|--------------|-----------------|-----------------|-------------------|---------------------|
| Weather / Climate | Hourly to daily | NOAA, NWS, AirNow | 24 hours | Re-fetch; if unavailable, use last-known-good with warning |
| Grid Emission Factors | Annual | EPA eGRID, EIA | 18 months | Use most recent available; flag if >2 years old |
| Product Certifications | Weekly to monthly | GREENGUARD, FloorScore, EPD Registry | 90 days | Re-verify; if expired, flag for HITL review |
| Census / Demographic | Annual (ACS 5-year) | US Census, Eurostat | 5 years | Use most recent vintage; flag if data vintage predates project registration |
| Solar Resource Data | Annual (TMY updates) | NREL NSRDB | 10 years | Use available TMY; note data vintage in documentation |
| Soil / Geotechnical | Static (survey updates) | NRCS SSURGO | 10 years | Use available; note survey vintage |
| Transit / Walkability | Real-time (GTFS) / Quarterly (Walk Score) | GTFS feeds, Walk Score | 30 days for Walk Score; real-time for GTFS | Re-fetch; if unavailable, use last-known-good |
| Energy Model Outputs | Per-simulation | EnergyPlus, IES VE, eQUEST | N/A (project-specific) | Archive with timestamp; reuse for related credits |

### Batch Data Ingestion Schedule

The platform maintains a nightly batch ingestion pipeline that updates static reference datasets. The schedule is:

| Dataset | Frequency | Ingestion Window | Storage Backend |
|---------|-----------|-----------------|-----------------|
| EPA eGRID | Annual | January (post-release) | PostgreSQL + S3 |
| NOAA Climate Normals | Decadal + interim | Monthly check | PostgreSQL |
| NREL NSRDB TMY | Annual | Quarterly check | S3 (Parquet) |
| EC3 Baselines | Quarterly | Week 1 of quarter | PostgreSQL |
| EPD Registry | Weekly | Sunday 02:00 UTC | PostgreSQL + Elasticsearch |
| GREENGUARD / FloorScore | Weekly | Sunday 03:00 UTC | PostgreSQL |
| Green-e Registry | Monthly | 1st of month | PostgreSQL |
| GBCI Credential Directory | Daily | 04:00 UTC | PostgreSQL (cached) |
| ASHRAE Standards (static) | As published | On release | Document store |
| IPCC GWP Values | Per assessment report | On AR release | PostgreSQL |

---

*End of Sections 1-2. Document continues in subsequent files with Sections 3-7 covering Architecture Overview, Detailed System Design, Implementation Specifications, Integration Details, Testing & Deployment, and Appendices.*
