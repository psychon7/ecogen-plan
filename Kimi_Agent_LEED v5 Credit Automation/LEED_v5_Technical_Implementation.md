# Deer-Flow LEED v5 Credit Automation Platform
# Technical Implementation Document

**Version:** 1.0.0  
**Date:** May 2026  
**Classification:** Engineering Blueprint

---

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


---

# Master Technical Implementation Document

## Section 3: Deer-Flow Platform Architecture

### 3.1 System Overview

The LEED v5 Automation Platform is built on **Deer-Flow**, ByteDance's open-source "SuperAgent Harness" (60.2k GitHub stars, v2.0). Deer-Flow provides the foundational infrastructure for skill-based agent orchestration, durable workflow execution, and human-in-the-loop (HITL) coordination. Rather than building a custom workflow engine from scratch -- an estimated 12-week engineering effort -- the platform leverages Deer-Flow's proven architecture and extends it with LEED-specific skills, API integrations, and document templates.

**Core Architectural Principles:**

| Principle | Implementation | Rationale |
|-----------|---------------|-----------|
| Skill-based modularity | One skill per LEED credit/prerequisite | Isolated development, testing, and deployment per credit |
| Durable workflows | LangGraph with checkpoint persistence | Survives restarts, API failures, and multi-day HITL delays |
| Sandboxed execution | Docker containers per skill | Prevents cross-credit contamination; energy model parsing isolated |
| Memory persistence | PostgreSQL + Redis | Project state survives session termination; full audit trail |
| Human-in-the-Loop | Slack / Email / Web UI | Consultant review at critical checkpoints with SLA enforcement |

**Platform Foundation Provided by Deer-Flow:**

```
LEED v5 Automation Platform (Built on Deer-Flow)
================================================================
Included (70-80% of infrastructure):
  - Skill system and registry
  - Sub-agent orchestration (parallel/sequential)
  - LangGraph durable workflows with checkpointing
  - Docker sandbox execution
  - Memory / state persistence
  - HITL channels (Slack, Telegram, Email)
  - Web UI (React frontend)
  - API gateway (FastAPI)

Built on Top (LEED-specific layer):
  - 16 LEED credit skills
  - 36 API integration tools
  - Document templates (Jinja2)
  - Regional availability filter
  - HITL dashboard enhancements
```

**LangGraph Durable Workflows:**

Deer-Flow uses LangGraph as its workflow engine. Each skill defines a `StateGraph` where nodes represent workflow steps (validation, API calls, calculations, document generation) and edges define execution flow, including conditional routing based on HITL decisions. Checkpointing persists state to PostgreSQL after every node execution, enabling workflows to survive server restarts and resume from exact failure points.

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Workflow survives restarts; each node is checkpointed automatically
workflow = StateGraph(LEEDState)
workflow.add_node("validate", validate_inputs)
workflow.add_node("fetch_data", fetch_api_data)
workflow.add_node("calculate", perform_calculations)
workflow.add_node("hitl_review", human_review_checkpoint)
workflow.add_node("generate", generate_documents)

# Conditional edges based on HITL response
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: state["hitl_result"]["action"],
    {"approve": "generate", "reject": "validate", "request_changes": "calculate"}
)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

**Skill-Based Architecture:**

Each of the 16 LEED credits is implemented as a Deer-Flow skill -- a self-contained module with its own `SKILL.md` manifest, workflow graph, input/output schemas, templates, and test suite. Skills are mounted at `/mnt/skills/leed/` and discovered at runtime by the skill registry.

**Sandbox Execution:**

Each skill executes within an isolated Docker container provisioned by Deer-Flow's `AioSandboxProvider`. Energy model parsing, PDF generation, and Excel compilation occur in sandboxed environments with no access to other skills' data or the host system. Files are persisted across workflow steps at `/mnt/user-data/outputs/` and retained per the project's data retention policy (default: 24 months).

**Memory System:**

Deer-Flow's memory system stores project-specific facts and intermediate calculation results in PostgreSQL, keyed by `thread_id` (project identifier). This enables multi-session workflows where a consultant can start an energy analysis on Monday, receive a Slack HITL notification Tuesday, approve calculations Wednesday, and find the workflow resumed exactly where it left off.

---

### 3.2 Core Components Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LEED v5 AUTOMATION PLATFORM                           │
│                         (Built on Deer-Flow v2.0)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FRONTEND LAYER                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  React + TypeScript Dashboard                                       │   │
│  │  - Credit selection wizard    - HITL review interface              │   │
│  │  - Project dashboard          - Document preview                   │   │
│  │  - Regional availability map  - USGBC submission tracker           │   │
│  └────────────────────┬────────────────────────────────────────────────┘   │
│                       │ HTTPS / WebSocket                                   │
│  API GATEWAY          ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  FastAPI Gateway                                                    │   │
│  │  - JWT authentication         - Rate limiting (100 req/min)        │   │
│  │  - Request routing            - Webhook handling for HITL          │   │
│  │  - API key management (Vault)   - Request/response logging           │   │
│  └────────────────────┬────────────────────────────────────────────────┘   │
│                       │ gRPC / HTTP                                           │
│  WORKFLOW ENGINE      ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  LangGraph Server (Python)                                          │   │
│  │  - StateGraph compilation     - Checkpoint persistence (PostgreSQL)│   │
│  │  - Node execution scheduler   - Conditional edge routing             │   │
│  │  - Parallel sub-agent spawn   - Error recovery & retry logic         │   │
│  └────────────────────┬────────────────────────────────────────────────┘   │
│                       │ Docker socket API                                     │
│  SANDBOX LAYER        ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Docker Container Pool                                              │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        ┌──────────┐        │   │
│  │  │ IP-p3    │ │ EAp1     │ │ WEp2     │  ...   │ SSc6     │        │   │
│  │  │ Carbon   │ │ OpCarbon │ │ WaterMin │        │ Light    │        │
│  │  └──────────┘ └──────────┘ └──────────┘        └──────────┘        │   │
│  │  /mnt/skills/leed/       /mnt/user-data/outputs/                   │   │
│  └────────────────────┬────────────────────────────────────────────────┘   │
│                       │ API calls (HTTPS)                                     │
│  EXTERNAL APIs        ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  EPA eGRID │ EC3 Database │ USGBC Arc │ NREL PVWatts │ NOAA Atlas   │   │
│  │  EPA SNAP  │ EPD Registry │ AHRI Dir  │ Walk Score   │ CRRC         │   │
│  │  Google Maps│ US Census │ NRCS Soils│ IES TM-15    │ FEMA NFHL    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  PERSISTENCE LAYER                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ PostgreSQL   │  │ Redis        │  │ S3 / MinIO   │  │ Vault        │   │
│  │ (State,      │  │ (Cache,      │  │ (Documents,  │  │ (API Keys,   │   │
│  │  Audit Logs) │  │  Pub/Sub)    │  │  Artifacts)  │  │  Secrets)    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                             │
│  HITL CHANNELS                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                       │
│  │ Slack Bot    │  │ Email (SES)  │  │ Web UI       │                       │
│  │ (Primary)    │  │ (Fallback)   │  │ (Dashboard)  │                       │
│  └──────────────┘  └──────────────┘  └──────────────┘                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 3.3 Component Specifications Table

| Component | Technology | Purpose | Scaling Strategy | SLA Target |
|-----------|-----------|---------|------------------|------------|
| **Frontend** | React 18 + TypeScript + Vite | Consultant dashboard, HITL review UI, project tracking | CDN (CloudFront) + S3 static hosting | 99.9% uptime |
| **API Gateway** | FastAPI + Uvicorn | Auth (JWT), routing, rate limiting, request validation | Horizontal (Kubernetes HPA, 2-20 pods) | 200ms p99 latency |
| **LangGraph Server** | Python 3.11 + LangGraph 0.0.x | Workflow engine, checkpoint management, node scheduling | Stateful (1 pod per project partition) | Checkpoint < 500ms |
| **Skill Containers** | Docker + Python 3.11 | Credit-specific agent execution (parsing, calculation, docs) | Per-credit pool (warm standby containers) | Cold start < 5s |
| **Memory Store** | PostgreSQL 15 + pgvector | Project state, workflow checkpoints, audit logs | Master-replica (2 replicas, async) | RPO < 1min |
| **Cache / Pub-Sub** | Redis 7 (Cluster) | API response cache, HITL notification queue, rate limit counters | 3-master cluster with replicas | < 5ms read |
| **Document Store** | S3 / MinIO | Generated PDFs, XLSX, DOCX, ZIP packages, manifest JSON | Object storage (versioned, encrypted) | 99.99% durability |
| **Secrets Manager** | HashiCorp Vault | API keys, OAuth credentials, DB passwords | HA cluster (3 nodes, auto-unseal) | 99.99% availability |
| **Message Queue** | Redis Streams / RabbitMQ | HITL notification delivery, async document generation | Pub/sub with consumer groups | Delivery < 1s |
| **Monitoring** | Prometheus + Grafana | Metrics, alerting, SLA tracking | 2-replica Prometheus, shared Grafana | 15s scrape interval |

---

### 3.4 Data Flow

The following describes the complete data flow for a typical project executing multiple LEED credits from intake through submission:

**Step 1 — Project Intake**
The consultant creates a project via the React dashboard, entering building type, location (lat/lon or address), target certification level, and team roster. The API Gateway validates inputs and creates a project record in PostgreSQL with a unique `thread_id`. Project metadata is saved to Deer-Flow memory.

**Step 2 — Credit Selection**
The consultant selects credits to pursue from the 16-skill registry. The RegionalSkillFilter middleware evaluates each skill against project location, disabling skills whose required APIs are unavailable in that region (e.g., EPA eGRID for non-US projects triggers a warning and fallback data path).

**Step 3 — Skill Execution (Parallel Where Independent)**
The LangGraph Server spawns sub-agents for each selected credit. Independent prerequisites (EAp1, EAp2, EAp5, MRp2, WEp2) execute in parallel. Dependent credits (IPp3 requires EAp1 + EAp5 + MRp2 outputs) execute sequentially after prerequisites complete.

**Step 4 — API Data Fetching**
Each skill fetches required data from external APIs: EPA eGRID for grid factors, EC3 for embodied carbon EPDs, NREL PVWatts for solar potential, NOAA Atlas 14 for rainfall data. API responses are cached in Redis with TTL appropriate to data volatility (eGRID: 1 year; EC3: 24 hours).

**Step 5 — Calculations**
Skills perform credit-specific calculations using validated API data. All calculations use explicit formulas with unit conversion tracking. Results are stored in the workflow state and logged to the audit trail.

**Step 6 — HITL Review Checkpoints**
When a skill reaches a HITL checkpoint, the workflow pauses and persists state. A notification is dispatched via the primary channel (Slack) with fallback to email. The consultant reviews parsed data, calculations, and draft documents through the web UI, then approves, rejects, or requests changes. The workflow resumes based on the decision.

**Step 7 — Document Generation**
Upon HITL approval, skills generate submission documents using Jinja2 HTML templates rendered to PDF via WeasyPrint, Excel workbooks via OpenPyXL, and Word narratives via python-docx. Documents include embedded calculation formulas for auditor verification.

**Step 8 — Package Assembly**
The Package Assembly skill (a meta-skill) collects all approved credit documents, generates a project-level manifest.json with SHA-256 checksums, bundles into a ZIP archive, and uploads to the document store.

**Step 9 — USGBC Arc Submission**
For credits configured for direct submission, the platform authenticates to the USGBC Arc API via OAuth 2.0 and uploads documents to the appropriate credit folders. Submission IDs are stored in project state.

**Step 10 — Export & Archive**
The consultant downloads the complete submission package. All intermediate artifacts, API responses, and audit logs are archived to S3 with 7-year retention per LEED documentation requirements.

---

### 3.5 Security & Compliance

**API Key Management (HashiCorp Vault)**

All external API credentials are stored in HashiCorp Vault with the following access controls:

| Secret Type | Vault Path | Rotation Policy | Access Pattern |
|-------------|-----------|-----------------|----------------|
| USGBC Arc OAuth | `secret/leed/arc/oauth` | 90 days | Runtime fetch, 1h TTL |
| EC3 API Key | `secret/leed/ec3/api_key` | 180 days | Runtime fetch, 24h TTL |
| NREL PVWatts Key | `secret/leed/nrel/api_key` | 365 days | Runtime fetch, 24h TTL |
| OpenAI API Key | `secret/leed/openai/api_key` | 90 days | Runtime fetch, 1h TTL |
| Database Password | `secret/leed/postgres/password` | 90 days | Startup fetch only |
| Slack Bot Token | `secret/leed/slack/bot_token` | 180 days | Runtime fetch, 24h TTL |

Vault is deployed in HA mode with 3 nodes, auto-unseal via AWS KMS / Azure Key Vault, and audit logs forwarded to a SIEM. No secrets are committed to source control; the CI/CD pipeline injects them via Vault's Kubernetes auth method.

**Document Encryption at Rest (AES-256)**

All generated documents stored in S3/MinIO are encrypted using server-side encryption with AES-256. The document store enforces: (a) bucket versioning to prevent accidental overwrites, (b) lifecycle rules transitioning documents to Glacier after 12 months, (c) cross-region replication for disaster recovery, and (d) access logging for all read/write operations.

**PII Handling for Census/Demographic Data**

Skills that query US Census Bureau APIs (LTc3) and Tree Equity Score (SSc5) handle location data as follows:
- Lat/lon coordinates are hashed (SHA-256) in logs; only the hash is retained long-term
- Census tract IDs are anonymized in analytics exports
- Project addresses are encrypted at rest and only decrypted in-memory during workflow execution
- No PII is transmitted to external APIs beyond what is required for the API call (e.g., address geocoding to Google Maps)
- GDPR data processing agreements are in place with all third-party API providers

**Audit Trails**

Every operation in the platform is logged to PostgreSQL with the following schema:

```sql
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL,
    skill_name VARCHAR(64) NOT NULL,
    workflow_step VARCHAR(128) NOT NULL,
    action VARCHAR(64) NOT NULL,  -- 'api_call', 'calculation', 'hitl_decision', 'document_generated'
    actor VARCHAR(128),  -- 'system', 'user:{id}', 'api:{name}'
    timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    inputs JSONB,
    outputs JSONB,
    checksum VARCHAR(64),  -- SHA-256 of document or data payload
    api_response_code INT,
    duration_ms INT,
    ip_address INET,
    user_agent TEXT
);
```

Logs are retained for 7 years to meet LEED documentation retention requirements and are queryable via the dashboard for project-level audit reports.

**SOC 2 / GDPR Considerations**

| Control Domain | Implementation | Evidence |
|----------------|---------------|----------|
| Access Control | RBAC with project-level permissions; SSO via SAML 2.0 | Quarterly access reviews |
| Data Encryption | TLS 1.3 in transit; AES-256 at rest | Certificate inventory |
| Change Management | GitOps (ArgoCD); mandatory PR review | Git history, PR approvals |
| Monitoring & Alerting | Prometheus + PagerDuty; 24/7 on-call | Incident response logs |
| Backup & Recovery | PostgreSQL PITR (7 days); S3 cross-region replication | Monthly DR drills |
| Vendor Management | DPA with all API providers; annual security review | Signed DPAs on file |
| Data Retention | 7-year document retention; GDPR deletion within 30 days of request | Retention policy document |

The platform is designed to be SOC 2 Type II ready within 6 months of production launch. GDPR compliance is achieved through data minimization (only collecting data required for LEED calculations), purpose limitation (data used only for certification support), and the right to erasure (automated deletion workflows triggered via dashboard request).

---

## Section 4: Skill System Specification

### 4.1 Skill Registry

The following table catalogs all 16 LEED v5 skills implemented as Deer-Flow modules. Each skill is independently versioned, tested, and deployable.

| # | Skill Name | Credit | Points | Automation % | HITL Checkpoints | Complexity | Est. Dev Days |
|---|-----------|--------|--------|-------------|-------------------|------------|---------------|
| 1 | IPp3 Carbon Assessment | IPp3 | Required (Prereq) | 92.5% | 1 (Consultant verification) | Low | 5 |
| 2 | EAp1 Operational Carbon | EAp1 | Required (Prereq) | 89.4% | 1 (Consultant review, 72h SLA) | Low-Medium | 6 |
| 3 | EAp2 Minimum Energy Efficiency | EAp2 | Required (Prereq) | 85.7% | 2 (Modeler + Consultant, 72h each) | Medium | 8 |
| 4 | EAp5 Refrigerant Management | EAp5 | Required (Prereq) | 85.2% | 1 (MEP Engineer, 24h SLA) | Low | 4 |
| 5 | EAc3 Enhanced Energy Efficiency | EAc3 | Up to 10 / 7 | 87.7% | 2 (Modeler + Consultant, 48h each) | Medium-High | 7 |
| 6 | EAc7 Enhanced Refrigerant | EAc7 | 2 | 89.3% | 1 (Mechanical Engineer, 48h) | Low | 4 |
| 7 | MRp2 Embodied Carbon | MRp2 | Required (Prereq) | 87.0% | 2 (Takeoff + EPD matching, 72h each) | Medium | 7 |
| 8 | MRc2 Reduce Embodied Carbon | MRc2 | Up to 6 | 88.4% | 1-2 (LCA Specialist) | Medium | 6 |
| 9 | WEp2 Minimum Water Efficiency | WEp2 | Required (Prereq) | 89.3% | 1 (Consultant, 48h) | Low | 5 |
| 10 | WEc2 Enhanced Water Efficiency | WEc2 | Up to 8 / 7 | 87.5% | 1 (Consultant, 48h) | Medium | 6 |
| 11 | LTc3 Compact & Connected | LTc3 | Up to 6 | 88.0% | 1 (Project Manager, 48h) | Low | 5 |
| 12 | LTc1 Sensitive Land Protection | LTc1 | 1 | 87.6% | 1 (Environmental Consultant, 48h) | Medium | 5 |
| 13 | SSc3 Rainwater Management | SSc3 | 3 | 88.0% | 1 (Civil Engineer, 48h) | Medium | 5 |
| 14 | SSc5 Heat Island Reduction | SSc5 | 2 | 85.3% | 1 (Architect, 48h) | Low | 4 |
| 15 | SSc6 Light Pollution Reduction | SSc6 | 1 | 90.6% | 1 (Lighting Designer, 48h) | Low | 4 |
| 16 | PRc2 LEED AP Verification | PRc2 | 1 | 90.1% | 1 (Project Admin, 24h) | Low | 3 |

**Registry Totals:**

| Metric | Value |
|--------|-------|
| Total Skills | 16 |
| Prerequisites | 5 (IPp3, EAp1, EAp2, EAp5, MRp2, WEp2) |
| Credits | 10 |
| Total Possible Points | 42 points (NC) / 37 points (C&S) |
| Average Automation Level | 88.1% |
| Total HITL Checkpoints | 18 (avg 1.1 per skill) |
| Total Estimated Dev Days | 80 person-days |

---

### 4.2 Skill Interaction Patterns

Skills interact through three primary execution patterns, determined by credit dependencies and data sharing requirements:

**Pattern A: Parallel Execution (Independent Credits)**

Prerequisites and credits with no shared data execute in parallel to minimize wall-clock time. Example: EAp5 (Refrigerant Management), WEp2 (Water Minimum), and SSc5 (Heat Island) can run simultaneously because they consume different input data and produce independent outputs.

```python
# Lead agent spawns sub-agents for parallel execution
sub_agents = [
    {"name": "eap5-agent", "skill": "leed-ea-p5-refrigerant"},
    {"name": "wep2-agent", "skill": "leed-we-p2-water-min"},
    {"name": "ssc5-agent", "skill": "leed-ss-c5-heat-island"},
]
results = await lead_agent.spawn_parallel(sub_agents, shared_inputs)
# Execution time = max(individual skill times), not sum
```

**Pattern B: Sequential Execution (Prerequisite Dependencies)**

Credits that require outputs from prerequisite skills execute sequentially. The workflow graph encodes these dependencies as explicit edges.

| Dependent Skill | Prerequisites Required | Data Passed |
|-----------------|----------------------|-------------|
| IPp3 Carbon Assessment | EAp1 (energy model), EAp5 (refrigerant inventory), MRp2 (material quantities) | `annual_kwh`, `fuel_breakdown`, `refrigerant_types`, `charge_kg`, `material_gwp` |
| WEc2 Enhanced Water | WEp2 (baseline fixture calcs) | `baseline_annual_gal`, `design_annual_gal`, `fixture_schedule` |
| MRc2 Reduce Embodied Carbon | MRp2 (baseline embodied carbon) | `total_kg_co2`, `structural_kg_co2`, `enclosure_kg_co2`, `gwp_intensity` |
| EAc3 Enhanced Energy | EAp2 (model parsing results) | `parsed_model_data`, `cost_summary`, `pct_better` |

```python
# Sequential dependency: EAp1 -> IPp3
workflow.add_edge("eap1_skill", "ipp3_skill")  # EAp1 must complete before IPp3 starts

# Sequential dependency: MRp2 -> MRc2
workflow.add_edge("mrp2_skill", "mrc2_skill")
```

**Dependency Resolution Algorithm:**

The orchestrator uses Kahn's topological sort algorithm on the dependency DAG to determine execution order. Before scheduling, it prunes nodes whose skills were not selected by the consultant, and detects cycles (which indicate a design flaw in the skill dependency declarations). The algorithm produces a linearized execution sequence where every skill appears after all its prerequisites.

```python
def topological_sort(skills: list[str], dependencies: dict[str, list[str]]) -> list[str]:
    """Kahn's algorithm for dependency-aware execution ordering."""
    in_degree = {s: 0 for s in skills}
    adj = {s: [] for s in skills}
    
    for skill, prereqs in dependencies.items():
        for prereq in prereqs:
            if prereq in skills:
                adj[prereq].append(skill)
                in_degree[skill] += 1
    
    queue = [s for s in skills if in_degree[s] == 0]
    result = []
    
    while queue:
        skill = queue.pop(0)
        result.append(skill)
        for dependent in adj[skill]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    if len(result) != len(skills):
        raise ValueError("Circular dependency detected in skill graph")
    
    return result
```

This algorithm guarantees that IPp3 (which depends on EAp1, EAp5, MRp2) never executes before any of its three prerequisites complete, while LTc3 (no dependencies) always appears at the start of the sequence and can execute immediately when the project is initialized.

**Pattern C: Shared State (Cross-Credit Data Flow)**

The project-wide state store (`LEEDProjectState`) acts as a shared data bus. Skills read prerequisite outputs from state and write their own outputs back, enabling both sequential and parallel patterns to coexist.

```python
class LEEDProjectState(TypedDict):
    project_id: str
    location: dict  # lat, lon, country
    
    # Prerequisite outputs (shared)
    eap1_operational_carbon: Optional[dict]
    eap2_energy_results: Optional[dict]
    eap5_refrigerant_inventory: Optional[list]
    mrp2_embodied_carbon: Optional[dict]
    wep2_water_baseline: Optional[dict]
    
    # Credit outputs
    eac3_points: Optional[int]
    wec2_points: Optional[int]
    mrc2_points: Optional[int]
    ip_carbon_projection: Optional[dict]
    
    # Meta
    documents: dict[str, str]  # credit_code -> document path
    hitl_status: dict[str, dict]
    audit_log: list[dict]
```

**Execution Orchestrator Logic:**

```python
async def execute_project_skills(project_state: LEEDProjectState, selected_credits: list[str]):
    """Execute skills with dependency-aware scheduling."""
    
    # Phase 1: Execute all prerequisites in parallel
    prerequisites = [c for c in selected_credits if is_prerequisite(c)]
    prereq_results = await asyncio.gather(*[
        execute_skill(skill, project_state) for skill in prerequisites
    ])
    
    # Merge prerequisite outputs into shared state
    for result in prereq_results:
        project_state[result.output_key] = result.data
    
    # Phase 2: Execute dependent credits in dependency order
    credits = [c for c in selected_credits if not is_prerequisite(c)]
    execution_order = topological_sort(credits, dependency_graph)
    
    for credit in execution_order:
        result = await execute_skill(credit, project_state)
        project_state[result.output_key] = result.data
    
    return project_state
```

**State Synchronization and Conflict Resolution:**

When multiple skills execute in parallel, they may attempt to write to the same state keys. The platform uses an optimistic locking strategy: each skill read receives a state version number; writes are accepted only if the version has not changed. If a conflict is detected, the skill's write is retried after re-reading the latest state. This ensures that the Energy Modeler approving EAp2 calculations does not collide with the MEP Engineer approving EAp5 refrigerant data, even when both HITL checkpoints resolve simultaneously.

**Error Propagation Across Skills:**

Prerequisite failures cascade to dependent skills with explicit error messages. If EAp2 fails due to a missing `.eso` file, EAc3 receives a clear `PrerequisiteNotMetError` with the EAp2 failure reason, rather than attempting to parse non-existent model data. The project dashboard surfaces these cascading errors as a dependency tree with red/green status indicators per skill.

**Resource Quota Management:**

Each skill declares its resource requirements (CPU, memory, disk, expected API calls) in its `SKILL.md` manifest. The orchestrator uses this information to prevent resource exhaustion: energy model parsing skills (EAp2, EAc3) are throttled to 2 concurrent executions per worker to prevent memory spikes from large `.eso` files, while lightweight skills (PRc2, SSc6) can run at higher concurrency.

| Skill | CPU Request | Memory Request | Max Concurrent | API Calls per Execution |
|-------|------------|----------------|----------------|------------------------|
| EAp2 | 2 cores | 4 GB | 2 | 0 (local parsing) |
| EAc3 | 2 cores | 4 GB | 2 | 0 (local parsing) |
| MRp2 | 1 core | 2 GB | 4 | 50 (EPD Registry + EC3) |
| IPp3 | 1 core | 2 GB | 4 | 10 (eGRID + EC3) |
| EAp1 | 1 core | 2 GB | 4 | 5 (eGRID + PVWatts) |
| PRc2 | 0.5 core | 512 MB | 10 | 1 (GBCI Directory) |
| SSc6 | 0.5 core | 512 MB | 10 | 0 (local validation) |

---

### 4.3 Skill Template Specification

Every skill in the registry follows a standardized `SKILL.md` structure. This template ensures consistency across all 16 credits and enables automated skill discovery, validation, and documentation generation.

**Required Sections:**

```markdown
---
name: leed-{credit-code}-{short-name}
version: 1.0.0
author: LEED Automation Platform
description: Automates LEED v5 {Credit Name} ...
---

## Metadata
- **Credit Code:** {XXXxN}
- **Credit Name:** {Full Credit Name}
- **Points:** {Required | Up to N}
- **Automation Level:** {N.N%}
- **Complexity:** {Low | Medium | High}
- **Primary Data Source:** {APIs and references}
- **HITL Required:** {Yes | No}

## Purpose
{1-2 paragraph description of what the skill automates and its scope boundaries}

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| {field_name} | {type} | {source} | {validation rules} |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| {field_name} | {type} | {default} | {description} |

## Workflow Steps (Durable)
### Step N: {Step Name}
- **Type:** {Validation | API Call | Calculation | Document Generation | Human Review}
- **Automated:** {Yes | No}
- **Description:** {Detailed description}
- **Output:** {Output schema}
- **On Failure:** {Failure handling strategy}

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step N | {Role} | {N hours} | {Review instructions} |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| {API Name} | {Purpose} | {Regions} | {Fallback} | {Rate Limit} |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| {Region} | {Available | Limited | Unavailable} | {Notes} |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| {Error Name} | {Action} | {Yes/No} | {N times} |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| {Document Name} | {PDF | XLSX | DOCX | JSON} | {Description} |

## Testing
{pytest commands and test coverage requirements}

## Example Usage (Deer-Flow)
{Python invocation example}

## Deer-Flow Workflow (LangGraph)
{LangGraph StateGraph definition}
```

**Template Validation Rules:**

| Rule | Enforcement | Tool | Severity |
|------|------------|------|----------|
| All required sections present | CI/CD linting | `skill-linter.py` | Blocking |
| Metadata fields complete | Schema validation | Pydantic `SkillManifest` | Blocking |
| API dependencies declared | Pre-deployment check | `api-availability-check.sh` | Blocking |
| Regional availability specified | Pre-execution filter | `RegionalSkillFilter` | Blocking |
| HITL checkpoints have SLA | Workflow compilation | LangGraph validation | Blocking |
| Testing commands provided | CI gate | `pytest` execution | Blocking |
| Output document types declared | Template engine check | `document-schema-validator.py` | Warning |
| Calculation formulas documented | Manual review | Tech lead sign-off | Warning |

**Skill Discovery and Registration:**

Skills are automatically discovered at runtime by scanning the `/mnt/skills/leed/` directory tree. The Skill Registry loads each `SKILL.md` manifest, validates it against the Pydantic `SkillManifest` schema, and registers the skill with its metadata, entry point module, and Docker image reference. This enables hot-loading of new skills without restarting the LangGraph server.

```python
class SkillRegistry:
    def discover_skills(self, skills_dir: Path) -> list[SkillManifest]:
        skills = []
        for skill_dir in skills_dir.glob("*/"):
            manifest_path = skill_dir / "SKILL.md"
            if manifest_path.exists():
                manifest = self._parse_manifest(manifest_path)
                if self._validate_manifest(manifest):
                    skills.append(manifest)
        return skills
    
    def get_skill(self, credit_code: str) -> SkillManifest:
        return next(s for s in self._skills if s.credit_code == credit_code)
    
    def filter_by_region(self, region: str) -> list[SkillManifest]:
        return [s for s in self._skills if s.is_available_in(region)]
```

**Skill Manifest Schema (Pydantic):**

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional

class SkillManifest(BaseModel):
    name: str
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    credit_code: str = Field(pattern=r"^[A-Z]{2}[pc]\d+$")
    credit_name: str
    points: Literal["Required"] | int
    automation_level: float = Field(ge=0.0, le=100.0)
    complexity: Literal["Low", "Medium", "High"]
    hitl_required: bool
    hitl_checkpoints: list[HITLCheckpoint]
    api_dependencies: list[APIDependency]
    regional_availability: dict[str, Literal["Available", "Limited", "Unavailable"]]
    docker_image: str
    entry_point: str  # module path for skill execution
    resource_requirements: ResourceRequirements
```

**Template Engine Pipeline:**

Document generation follows a standardized pipeline: (1) Jinja2 HTML template populated with skill output data, (2) WeasyPrint renders HTML to PDF with embedded vector charts, (3) OpenPyXL generates Excel workbooks with visible formulas for auditor traceability, (4) python-docx produces Word narratives with placeholder fields for final human editing. All templates are versioned alongside their parent skill and validated against output schema constraints before deployment.

---

### 4.4 Skill Lifecycle

Each skill progresses through a standardized lifecycle from development through retirement:

```
Development ──> Testing ──> Staging ──> Production ──> Monitoring ──> Updates ──> Deprecation
```

**Phase 1: Development (Est. 3-7 days per skill)**
- Skill author creates `SKILL.md` manifest following template specification
- Implements LangGraph workflow nodes (validation, API calls, calculations, document generation)
- Creates Jinja2 templates for PDF/Excel/Word outputs
- Writes unit tests for all calculation logic
- Implements error handling with fallback strategies

**Phase 2: Testing (Est. 2-3 days per skill)**

Testing is organized into four test tiers with distinct coverage targets:

| Tier | Test Type | Coverage Target | Execution | CI Gate |
|------|-----------|----------------|-----------|---------|
| Unit | Input validation, calculation logic, edge cases | > 90% code coverage | Local pytest, < 10s | Required |
| Integration | Mocked API responses, end-to-end workflow | All API paths exercised | Dockerized pytest, < 2min | Required |
| HITL Simulation | Checkpoint pausing, resumption, SLA timers | All HITL paths covered | Async test harness, < 5min | Required |
| Regression | Compare outputs against known-good baselines | Output diff < 0.1% | Nightly CI, < 15min | Warning |

The HITL simulation tier is particularly critical: it uses Deer-Flow's `MockHumanReviewNode` to simulate consultant approvals, rejections, and revision requests at each checkpoint, verifying that the workflow correctly branches to the appropriate subsequent node. Without this tier, a bug in conditional edge routing could go undetected until a real consultant encounters a hung workflow.

**Phase 3: Staging (Est. 1-2 days per skill)**

Staging validates skills against real-world data before production release. The staging environment mirrors production infrastructure (same API endpoints, same Vault secrets, same Docker runtime) but with rate-limited API keys and isolated S3 buckets. Each skill is executed against 3-5 real project datasets representing diverse building types, climate zones, and regional contexts. A staging checklist is completed for each skill:

- [ ] Document output quality reviewed by LEED consultant
- [ ] Regional availability filter accuracy verified for 6+ regions
- [ ] HITL notification delivery confirmed (Slack + email fallback)
- [ ] API fallback paths exercised (e.g., eGRID timeout triggers cached data)
- [ ] Error messages are actionable for non-technical users
- [ ] Execution time < 90 seconds for all automated steps
- [ ] Memory usage stays below declared resource limits
- [ ] No PII leaks in logs or API request traces

**Phase 3: Staging (Est. 1-2 days per skill)**
- Deploy to staging environment with live API keys (rate-limited)
- Execute against 3-5 real project datasets
- Validate document output quality with LEED consultants
- Check regional availability filter accuracy
- Verify HITL notification delivery (Slack + email)

**Phase 4: Production (Continuous)**
- Skill registered in production skill registry
- Version pinned for stability: `name: leed-ea-c3-energy-enhanced, version: 1.0.0`
- Monitoring dashboards track: execution time, API error rates, HITL response times, document generation success rate
- Alerting on: API failures > 5%, HITL SLA breaches > 10%, calculation errors > 1%

**Phase 5: Monitoring & Updates (Ongoing)**
- Annual updates for static data dependencies (ASHRAE standards, eGRID data, IPCC factors)
- Quarterly reviews of API availability and rate limit changes
- Bug fixes deployed as patch versions (1.0.1, 1.0.2)
- Feature additions deployed as minor versions (1.1.0)
- Breaking changes deployed as major versions (2.0.0) with migration guide

**Phase 6: Deprecation (As Needed)**
- Deprecated skills remain available for 12 months with warning banners
- Migration path provided to replacement skills
- Final removal announced 90 days in advance

**Versioning Policy:**

| Change Type | Version Bump | Example | Approval Required |
|-------------|-------------|---------|-------------------|
| Bug fix | Patch (x.y.Z) | 1.0.0 -> 1.0.1 | Tech lead |
| New feature / API | Minor (x.Y.z) | 1.0.0 -> 1.1.0 | Engineering manager |
| Breaking change / new standard | Major (X.y.z) | 1.0.0 -> 2.0.0 | Architecture board |
| Data refresh (annual) | Patch (x.y.Z) | 1.0.0 -> 1.0.1+egrid2024 | Tech lead |

---

### 4.5 Skill Dependencies Graph

The following directed acyclic graph (DAG) shows prerequisite and data-sharing relationships between skills:

```
                                    PROJECT INTAKE
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
            ┌───────────┐          ┌───────────┐          ┌───────────┐
            │   EAp1    │          │   EAp5    │          │   MRp2    │
            │ Op Carbon │          │ Refrigerant│          │ Embodied  │
            │ Required  │          │ Required   │          │ Required  │
            └─────┬─────┘          └─────┬─────┘          └─────┬─────┘
                  │                      │                      │
                  │                      │                      │
                  └──────────────────────┼──────────────────────┘
                                         │
                                         ▼
                              ┌───────────────────┐
                              │      IPp3         │
                              │ Carbon Assessment │
                              │    Required       │
                              │ (consumes EAp1,   │
                              │  EAp5, MRp2)      │
                              └───────────────────┘
                                         │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
            ┌───────────┐          ┌───────────┐          ┌───────────┐
            │   EAp2    │          │   WEp2    │          │   PRc2    │
            │ Energy Min│          │ Water Min │          │ LEED AP   │
            │ Required  │          │ Required  │          │ 1 point   │
            └─────┬─────┘          └─────┬─────┘          └───────────┘
                  │                      │
                  │                      │
                  ▼                      ▼
            ┌───────────┐          ┌───────────┐
            │   EAc3    │          │   WEc2    │
            │ Energy    │          │ Water     │
            │ Enhanced  │          │ Enhanced  │
            │ (extends  │          │ (extends  │
            │  EAp2)    │          │  WEp2)    │
            └───────────┘          └───────────┘
                  │
                  │
                  ▼
            ┌───────────┐
            │   EAc7    │
            │ Enhanced  │
            │ Refrigerant│
            └───────────┘
                                         │
                                         ▼
                              ┌───────────────────┐
                              │      MRc2         │
                              │ Reduce Embodied   │
                              │ Carbon            │
                              │ (extends MRp2)    │
                              └───────────────────┘

INDEPENDENT SKILLS (no prerequisites, can run anytime):
┌──────────────────────────────────────────────────────────────────────────┐
│  LTc1 (Sensitive Land) │ LTc3 (Compact & Connected) │ SSc3 (Rainwater)  │
│  SSc5 (Heat Island)    │ SSc6 (Light Pollution)     │                   │
└──────────────────────────────────────────────────────────────────────────┘
```

**Dependency Matrix:**

| Skill | Direct Prerequisites | Data Consumed From | Enables |
|-------|---------------------|-------------------|---------|
| IPp3 | EAp1, EAp5, MRp2 | Energy model, refrigerant inventory, material GWP | None (terminal aggregator) |
| EAc3 | EAp2 | Parsed model data, cost summary, compliance calc | None |
| EAc7 | EAp5 (recommended) | Refrigerant inventory (optional cross-check) | None |
| WEc2 | WEp2 | Baseline/design fixture calcs, fixture schedule | None |
| MRc2 | MRp2 | Baseline embodied carbon, GWP intensity | None |
| LTc3 | None | US Census, Walk Score, GTFS | None |
| LTc1 | None | FEMA, NWI, USFWS, USGS | None |
| SSc3 | None | NOAA Atlas 14, NRCS soils | None |
| SSc5 | None | CRRC, Tree Equity Score | None |
| SSc6 | None | IES TM-15, manufacturer data | None |
| PRc2 | None | GBCI Directory, team roster | None |

**Execution Strategy Based on Dependencies:**

| Phase | Skills Executed | Parallelism | Expected Wall Time |
|-------|----------------|-------------|-------------------|
| Phase 1 | EAp1, EAp5, MRp2, EAp2, WEp2, LTc1, LTc3, SSc3, SSc5, SSc6, PRc2 | Max parallel (11 skills) | ~15 minutes |
| Phase 2 | IPp3 (waits for EAp1+EAp5+MRp2) | Sequential | +~5 minutes |
| Phase 3 | EAc3 (waits for EAp2), WEc2 (waits for WEp2), MRc2 (waits for MRp2) | Parallel (3 skills) | +~10 minutes |
| Phase 4 | EAc7 (waits for EAp5, optional) | Sequential | +~3 minutes |
| **Total** | All 16 skills | Dependency-aware | **~35 minutes** (automated steps only, excluding HITL) |

**Key Design Decisions:**

1. **IPp3 as Terminal Aggregator:** IPp3 is the only skill that consumes outputs from three prerequisite skills. It does not enable downstream credits, making it a natural terminal node in the DAG.

2. **Extension Pattern:** Credits that extend prerequisites (EAc3 extends EAp2, WEc2 extends WEp2, MRc2 extends MRp2, EAc7 extends EAp5) reuse parsed data and add additional calculations. This avoids re-parsing the same energy models or material takeoffs.

3. **Independent Skills:** Site and location-based credits (LTc1, LTc3, SSc3, SSc5, SSc6, PRc2) have no prerequisites and can execute at any time, ideally in Phase 1 for maximum parallelism.

4. **Cross-Credit Shared State:** The project state store enables skills to read outputs from completed skills without explicit edges. For example, IPp3 can read EAp1 data as soon as EAp1 writes to state, even if EAp5 and MRp2 are still running. This "publish-subscribe" pattern reduces overall wall time compared to strict DAG execution.

---

*End of Sections 3-4*


---

# Master Technical Implementation Document

## Section 5: API Integration Specifications

### 5.1 API Integration Architecture

The API Integration Layer serves as the data ingestion backbone of the LEED v5 Automation Platform. It normalizes access to 36 external data sources across government, industry, software platform, and IoT sensor categories. The architecture follows a **layered client pattern** with resilience primitives at every tier.

#### 5.1.1 REST API Client Layer

All external API calls flow through the `LeedApiClient` abstraction, a unified async HTTP client built on `httpx` with the following capabilities:

| Capability | Implementation | Default Config |
|------------|---------------|----------------|
| HTTP transport | `httpx.AsyncClient` | HTTP/2 enabled, `limits=Limits(max_connections=100, max_keepalive_connections=20)` |
| Timeout | Per-API configurable | Connect: 5s, Read: 30s, Write: 10s |
| Request signing | HMAC-SHA256 for internal APIs | Key rotation via Vault |
| Request ID injection | `X-Request-ID` UUID v4 | Propagated across all upstream calls |
| User-Agent | `LEED-Platform/1.0 (project:{project_id})` | Identifies origin for provider analytics |

```python
# /backend/api_client/leed_api_client.py

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from circuitbreaker import circuit

class LeedApiClient:
    def __init__(self, api_config: ApiConfig, cache: RedisCache):
        self.config = api_config
        self.cache = cache
        self.client = httpx.AsyncClient(
            http2=True,
            timeout=httpx.Timeout(
                connect=api_config.timeout_connect,
                read=api_config.timeout_read,
                write=api_config.timeout_write
            ),
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20
            )
        )
    
    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    @circuit(failure_threshold=5, recovery_timeout=60, expected_exception=httpx.HTTPStatusError)
    async def fetch(self, endpoint: str, params: dict = None, 
                    cache_key: str = None, ttl: int = 3600) -> dict:
        # 1. Check cache
        if cache_key and (cached := await self.cache.get(cache_key)):
            return cached
        
        # 2. Execute request with auth injection
        response = await self.client.get(
            f"{self.config.base_url}{endpoint}",
            params=params,
            headers=self._auth_headers()
        )
        response.raise_for_status()
        data = response.json()
        
        # 3. Write to cache
        if cache_key:
            await self.cache.set(cache_key, data, ex=ttl)
        
        return data
```

#### 5.1.2 Rate Limiting and Quota Management

Each API integration declares its rate limit profile in `api_limits.yaml`. The system enforces limits via a **token bucket algorithm** implemented in Redis, with per-API, per-project, and per-key granularity.

```yaml
# /backend/config/api_limits.yaml
api_limits:
  epa_egrid:
    requests_per_period: 10000    # Effectively unlimited
    period_seconds: 3600
    burst_capacity: 100
  
  noaa_climate:
    requests_per_period: 1000     # Free tier daily limit
    period_seconds: 86400
    burst_capacity: 50
  
  ec3_database:
    requests_per_period: 5000     # Research tier
    period_seconds: 3600
    burst_capacity: 100
  
  google_maps:
    requests_per_period: 100000   # Pay-per-use billing
    period_seconds: 86400
    burst_capacity: 1000
    budget_alert_usd: 500         # Cost guardrail
  
  walk_score:
    requests_per_period: 5000     # Professional tier
    period_seconds: 86400
    burst_capacity: 100
```

| API | Rate Limit Strategy | Quota Enforcement Point | Overflow Action |
|-----|--------------------|------------------------|-----------------|
| Government (free) | Token bucket in Redis | Gateway middleware | Queue + exponential backoff |
| Commercial (paid) | Token bucket + spend cap | Gateway + billing alert | Hard stop + admin alert |
| OAuth 2.0 services | Per-token bucket + refresh | Auth middleware | Refresh token + retry |
| Certificate-based | Connection pool limit | Network layer | Queue with priority |

#### 5.1.3 Caching Strategy (Redis with TTL)

Redis Cluster (6 nodes, 3 masters, 3 replicas) handles all API response caching. Cache keys follow the namespace pattern: `leed:api:{api_name}:{hash(params)}:{version}`.

| Cache Tier | Storage | Use Case | Eviction Policy |
|------------|---------|----------|-----------------|
| L1 - Hot | Redis (in-memory) | Real-time lookups (weather, AQI) | LRU, max 128MB per API |
| L2 - Warm | Redis (AOF-persisted) | Semi-static data (grid factors, EPDs) | TTL-based automatic |
| L3 - Cold | PostgreSQL (JSONB) | Archived snapshots for audit | Manual, 7-year retention |

```python
# Cache key builder with versioning for data integrity
def build_cache_key(api_name: str, params: dict, data_version: str) -> str:
    param_hash = hashlib.sha256(
        json.dumps(params, sort_keys=True).encode()
    ).hexdigest()[:12]
    return f"leed:api:{api_name}:{param_hash}:{data_version}"
```

#### 5.1.4 Fallback Chains

Every API integration defines a **three-tier fallback chain**:

1. **Primary**: Live API call with fresh data
2. **Secondary**: Cached data from Redis (stale but valid)
3. **Tertiary**: Static fallback dataset bundled with platform releases

| API | Primary | Secondary (Cache TTL) | Tertiary (Static) |
|-----|---------|----------------------|-------------------|
| EPA eGRID | Live API | 1 year | Last annual release JSON |
| NOAA Climate | Live API | 1 hour | Historical climate normals |
| EC3 Database | Live API | 24 hours | Baseline material averages |
| USGBC Arc | Live API | 15 minutes | Local project snapshot |
| NREL PVWatts | Live API | 30 days | Regional solar averages |

#### 5.1.5 Circuit Breaker Pattern

The `circuitbreaker` library wraps all external API calls with per-API circuit breaker instances. Circuit state transitions are emitted as events to the monitoring system.

| Circuit State | Trigger | Behavior | Auto-Recovery |
|--------------|---------|----------|---------------|
| **Closed** | Healthy | Requests flow normally | N/A |
| **Open** | 5 failures in 60s | All requests fail fast with `CircuitOpenError` | Probe after 60s timeout |
| **Half-Open** | Recovery timeout elapsed | Single probe request allowed | Success: Close; Failure: Open |

```python
@circuit(failure_threshold=5, recovery_timeout=60, 
         expected_exception=httpx.HTTPStatusError,
         name="epa_egrid_circuit")
async def fetch_egrid_data(region: str) -> dict:
    # Circuit breaker wraps the API call
    return await epa_client.fetch("/egrid/data", {"region": region})
```

### 5.2 Priority API Integrations Table

The following table maps all 36 APIs to integration priority, development effort, enabled credits, and business value. Priorities are assigned based on: (a) number of downstream credits enabled, (b) criticality to high-value credits (carbon, energy, water), (c) integration complexity, and (d) data uniqueness (no substitutes available).

| Priority | API | Provider | Integration Effort | Auth Method | Credits Enabled | Business Value | Fallback Available |
|----------|-----|----------|-------------------|-------------|-----------------|----------------|-------------------|
| **P0** | **EPA eGRID** | EPA | 2 days | Public access | IPp3, EAp1, EAc4 | **Critical** - Grid emission factors required for all carbon calculations | Yes (annual static) |
| **P0** | **EC3 Database** | Building Transparency | 3 days | API Key (free) | IPp3, MRp2, MRc2 | **Critical** - 20,000+ EPDs for embodied carbon | Yes (baseline averages) |
| **P0** | **USGBC Arc Platform** | USGBC | 5 days | OAuth 2.0 | All reporting credits | **Critical** - Direct submission pipeline to LEED Online | No (must retry) |
| **P1** | **NOAA Climate Data Online** | NOAA | 1 day | API Key (free) | IPp1, SSc3, SSp1 | **High** - Weather data for climate resilience | Yes (climate normals) |
| **P1** | **NREL PVWatts** | NREL | 1 day | API Key (free) | EAc4 | **High** - Solar production estimates for renewable energy credits | Yes (regional averages) |
| **P1** | **US Census Bureau API** | US Census | 2 days | API Key (free) | IPp2, LTc2, LTc3 | **High** - Demographics for equity and connectivity credits | Yes (ACS 5-year snapshot) |
| **P1** | **FEMA Flood Map Service** | FEMA | 1 day | None / API Key | IPp1, LTc1 | **High** - Flood zone data for site protection | Yes (FIRM panel archive) |
| **P1** | **NOAA Precipitation Frequency** | NOAA | 1 day | None | SSc3 | **High** - Rainfall depth-duration-frequency for stormwater | Yes (Atlas 14 static) |
| **P1** | **ENERGY STAR Product API** | EPA | 1 day | Public access | WEp2, LTc5 | **High** - Product efficiency ratings for water and energy | Yes (quarterly snapshot) |
| **P1** | **Google Maps Platform** | Google | 1 day | API Key (paid) | LTc3, EQp3 | **High** - Geocoding, distance, elevation for transit credits | Yes (cached geocodes) |
| **P1** | **Green-e Registry** | CRS | 1 day | Public access | EAc4 | **High** - REC and carbon offset verification | Yes (quarterly download) |
| **P1** | **EPA AQI API** | EPA | 1 day | API Key (free) | EQp2 | **High** - Air quality data for indoor environmental quality | Yes (static AQI zones) |
| **P1** | **GREENGUARD Database** | UL Environment | 1 day | Public access | MRc3 | **High** - Low-emitting product certifications | Yes (quarterly snapshot) |
| **P1** | **FloorScore Database** | RFCI | 1 day | Public access | MRc3 | **High** - Flooring emissions certifications | Yes (quarterly snapshot) |
| **P1** | **HPD Repository API** | HPD Collaborative | 2 days | Registration | MRc4 | **High** - Health Product Declarations for material health | Yes (monthly snapshot) |
| **P2** | **USGS National Map API** | USGS | 2 days | None | LTc1, SSp1 | **Medium** - Elevation, topography, hydrography | Yes (3DEP archive) |
| **P2** | **NRCS Soil Survey API** | USDA NRCS | 3 days | None | SSc3, SSp1 | **Medium** - Soil properties for stormwater and open space | Yes (SSURGO static) |
| **P2** | **EPA EJScreen** | EPA | 1 day | Public access | IPp2 | **Medium** - Environmental justice metrics | Yes (annual snapshot) |
| **P2** | **USFWS Critical Habitat** | USFWS | 1 day | None | LTc1 | **Medium** - Endangered species habitat data | Yes (quarterly download) |
| **P2** | **GBCI Credential Directory** | GBCI | 1 day | On request | PRc2 | **Medium** - LEED AP credential verification | Yes (weekly snapshot) |
| **P2** | **Green Button API** | Utilities/NIST | 3 days | OAuth 2.0 | EAp4, EAc5 | **Medium** - Interval energy usage from utilities | No (utility-dependent) |
| **P2** | **EnergyPlus Python (Eppy)** | NREL/Open Source | 3 days | Open source | EAp1, EAp2, EAc3 | **Medium** - Energy model IDF manipulation | Yes (local install) |
| **P2** | **ArcGIS REST API** | Esri | 3 days | API Key / OAuth | LT credits, SS credits | **Medium** - GIS spatial analysis | Yes (cached layers) |
| **P2** | **Procore API** | Procore | 3 days | OAuth 2.0 | IPc1, EAp3 | **Medium** - Project documents, RFIs, submittals | Yes (project snapshot) |
| **P2** | **IAQ Sensor APIs** | Awair, Kaiterra | 2 days | API Key | EQc5 | **Medium** - Indoor air quality monitoring | No (sensor-dependent) |
| **P2** | **Smart Water Meter APIs** | Various | 5 days | API Key / Certificate | WEp1, WEc1 | **Medium** - Water consumption and leak detection | No (manufacturer-specific) |
| **P2** | **EPA Brownfields API** | EPA | 1 day | Public access | LTc2 | **Medium** - Brownfield site assessment data | Yes (annual snapshot) |
| **P2** | **GTFS Realtime** | Transit agencies | 3 days | Varies by agency | LTc3, LTc4 | **Medium** - Transit schedules and real-time updates | Yes (static GTFS) |
| **P2** | **One Click LCA API** | One Click LCA | 3 days | API Token (license) | MRp2, MRc2 | **Medium** - Life cycle assessment calculations | Yes (last known values) |
| **P3** | **Tally API** | Building Transparency / Autodesk | 3 days | License + API Key | IPp3, MRp2, MRc2 | **Low-Medium** - Revit-integrated LCA (overlaps EC3) | Yes (EC3 fallback) |
| **P3** | **Walk Score API** | Walk Score / Redfin | 1 day | API Key (paid) | LTc3 | **Low-Medium** - Walkability scores (Google Maps partial substitute) | Yes (cached scores) |
| **P3** | **OpenADR API** | OpenADR Alliance | 3 days | Certificate-based | EAc6 | **Low** - Demand response signals (specialized credit) | No (event-driven) |
| **P3** | **Autodesk Forge** | Autodesk | 7 days | OAuth 2.0 | Multiple (BIM) | **Low-Medium** - BIM model extraction and viewer | Yes (cached model data) |
| **P3** | **Autodesk Revit API** | Autodesk | 7 days | License + API access | MRp2, MRc2, WEp2 | **Low-Medium** - Direct Revit model element extraction | No (requires Revit) |
| **P3** | **BAS/BMS Protocols (BACnet)** | ASHRAE / Various | 7 days | Network access | EAc5, WEc1, EQc5 | **Low** - Building automation data (on-premise only) | No (network-dependent) |
| **P3** | **IES VE API** | IES Ltd | 4 days | License required | EA credits | **Low** - Energy simulation results (EnergyPlus substitute) | Yes (EnergyPlus fallback) |

**Implementation Timeline by Priority:**

| Sprint | Priority | APIs | Cumulative | Effort |
|--------|----------|------|-----------|--------|
| Sprint 1 (Week 1) | P0 | EPA eGRID, EC3, USGBC Arc | 3 APIs | 10 dev-days |
| Sprint 2 (Week 2) | P1 | NOAA Climate, NREL PVWatts, US Census, FEMA, NOAA Precip, ENERGY STAR, Google Maps, Green-e, EPA AQI, GREENGUARD, FloorScore, HPD | 15 APIs | 18 dev-days |
| Sprint 3 (Week 3) | P2 | USGS, NRCS, EPA EJScreen, USFWS, GBCI, Green Button, Eppy, ArcGIS, Procore, IAQ Sensors, Water Meters, Brownfields, GTFS, One Click LCA | 29 APIs | 31 dev-days |
| Sprint 4 (Week 4-5) | P3 | Tally, Walk Score, OpenADR, Autodesk Forge, Revit API, BACnet, IES VE | 36 APIs | 25 dev-days |

### 5.3 API Authentication & Security

#### 5.3.1 API Key Rotation Schedule

| Key Type | Rotation Frequency | Rotation Method | Notification |
|----------|-------------------|-----------------|--------------|
| Government API keys (NOAA, NREL, Census) | 90 days | Automated via Vault | Email to platform admin |
| Commercial API keys (Google Maps, Walk Score) | 180 days | Manual + automated | Email + Slack to billing admin |
| EC3 API key | 90 days | Automated via Vault | Email to platform admin |
| Internal HMAC signing keys | 30 days | Automated via Vault | Audit log only |
| TLS certificates (OpenADR, BACnet) | 365 days | Automated ACME | Email to infrastructure team |

```python
# /backend/auth/vault_key_rotation.py

from hvac import Client as VaultClient
from datetime import datetime, timedelta

class KeyRotationManager:
    def __init__(self, vault_client: VaultClient):
        self.vault = vault_client
        self.rotation_schedule = {
            "gov_api_keys": timedelta(days=90),
            "commercial_api_keys": timedelta(days=180),
            "internal_hmac": timedelta(days=30),
            "tls_certs": timedelta(days=365)
        }
    
    async def rotate_if_needed(self, key_path: str) -> bool:
        meta = await self.vault.secrets.kv.v2.read_secret_metadata(
            path=key_path
        )
        last_rotation = datetime.fromisoformat(
            meta["data"]["created_time"]
        )
        key_type = self._classify_key(key_path)
        
        if datetime.utcnow() - last_rotation > self.rotation_schedule[key_type]:
            await self._perform_rotation(key_path)
            return True
        return False
```

#### 5.3.2 OAuth 2.0 Flow for USGBC Arc

The USGBC Arc Platform API requires OAuth 2.0 with authorization code grant. This is the most security-critical integration because it writes data to LEED Online.

| OAuth Parameter | Value | Notes |
|-----------------|-------|-------|
| Grant type | Authorization Code + PKCE | PKCE required for public clients |
| Authorization endpoint | `https://www.usgbc.org/oauth/authorize` | User-facing consent screen |
| Token endpoint | `https://www.usgbc.org/oauth/token` | Backend-only, client secret required |
| Scope | `project:read project:write credit:submit` | Minimum viable scope |
| Token lifetime | Access: 1 hour, Refresh: 30 days | Auto-refresh via background task |
| Redirect URI | `https://platform.leedauto.com/auth/callback` | HTTPS only, registered with USGBC |

```python
# OAuth 2.0 token refresh with automatic retry

async def refresh_usgbc_token(refresh_token: str) -> TokenPair:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://www.usgbc.org/oauth/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": settings.USGBC_CLIENT_ID,
                "client_secret": settings.USGBC_CLIENT_SECRET
            },
            timeout=30.0
        )
        response.raise_for_status()
        token_data = response.json()
        
        return TokenPair(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token", refresh_token),
            expires_at=datetime.utcnow() + timedelta(seconds=token_data["expires_in"])
        )
```

**Token Storage:**
- Encrypted at rest using Vault Transit engine (AES-256-GCM)
- Access tokens in Redis with TTL matching expiration
- Refresh tokens in Vault KV v2 with versioning

#### 5.3.3 Certificate-Based Authentication for OpenADR

OpenADR 2.0b requires mutual TLS (mTLS) with X.509 certificates signed by the OpenADR Alliance root CA.

| Certificate Component | Specification | Storage |
|----------------------|---------------|---------|
| Client certificate | X.509 v3, RSA 2048-bit, SHA-256 | Vault PKI engine |
| Private key | RSA 2048-bit, unencrypted in memory only | Vault, never persisted to disk |
| CA bundle | OpenADR Alliance root + intermediate | Mounted as Kubernetes secret |
| TLS version | 1.2 minimum, 1.3 preferred | Enforced in `ssl_context` |

```python
# OpenADR mTLS client configuration

import ssl
from pathlib import Path

async def create_openadr_client(cert_path: Path, key_path: Path, ca_path: Path):
    ssl_context = ssl.create_default_context(cafile=ca_path)
    ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
    
    return httpx.AsyncClient(
        verify=ssl_context,
        http2=False  # OpenADR uses HTTP/1.1
    )
```

#### 5.3.4 Secret Management (Vault)

HashiCorp Vault is the single source of truth for all API credentials. The architecture uses:

| Vault Feature | Use Case | Path Pattern |
|--------------|----------|--------------|
| KV v2 | Static API keys, tokens | `leed/apis/{api_name}/credentials` |
| Transit | Encryption of sensitive response data | `leed/transit/api-responses` |
| PKI | Certificate generation for OpenADR, BACnet | `leed/pki/openadr` |
| Dynamic secrets | Database credentials for API cache layer | `leed/database/cache` |
| Audit | All credential access logged | Syslog + Splunk forwarder |

**Access Control:**
- API client pods use Kubernetes ServiceAccount JWT authentication to Vault
- Each pod receives a wrapped token valid for 1 hour
- Credential read policies are scoped per API (e.g., `read-leed-apis-epa-egrid`)
- No human access to production credentials except break-glass procedure

### 5.4 API Error Handling & Resilience

#### 5.4.1 Retry Strategies (Exponential Backoff)

| HTTP Status | Classification | Retry Strategy | Max Retries |
|-------------|---------------|----------------|-------------|
| 429 Too Many Requests | Rate limit | Exponential backoff with jitter, respect `Retry-After` | 5 |
| 502 Bad Gateway | Transient | Exponential backoff: 2s, 4s, 8s, 16s, 32s | 5 |
| 503 Service Unavailable | Transient | Same as 502 + circuit breaker trigger | 5 |
| 504 Gateway Timeout | Transient | Same as 502 | 5 |
| 401 Unauthorized | Auth failure | No retry; trigger token refresh | 0 |
| 403 Forbidden | Auth/permission | No retry; alert admin | 0 |
| 404 Not Found | Data missing | No retry; return empty result | 0 |
| 5xx (other) | Server error | Linear backoff, alert on 3rd failure | 3 |

```python
# Retry configuration with jitter to prevent thundering herd

from tenacity import (
    retry, stop_after_attempt, wait_exponential_jitter,
    retry_if_exception_type, before_sleep_log
)
import logging

logger = logging.getLogger("api_resilience")

class RetryConfig:
    TRANSIENT_ERRORS = (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError)
    
    @staticmethod
    def get_retry_policy(api_name: str, status_code: int = None):
        if status_code == 429:
            return {
                "stop": stop_after_attempt(5),
                "wait": wait_exponential_jitter(initial=2, max=120),
                "retry": retry_if_exception_type(httpx.HTTPStatusError),
                "before_sleep": before_sleep_log(logger, logging.WARNING)
            }
        return {
            "stop": stop_after_attempt(4),
            "wait": wait_exponential_jitter(initial=1, max=60),
            "retry": retry_if_exception_type(RetryConfig.TRANSIENT_ERRORS),
            "before_sleep": before_sleep_log(logger, logging.WARNING)
        }
```

#### 5.4.2 Circuit Breaker Configuration

| API | Failure Threshold | Recovery Timeout | Half-Open Max Calls | Monitoring Metric |
|-----|------------------|-------------------|---------------------|-------------------|
| EPA eGRID | 5 failures / 60s | 60s | 1 | `circuit_epa_egrid_state` |
| EC3 Database | 5 failures / 60s | 120s | 1 | `circuit_ec3_state` |
| USGBC Arc | 3 failures / 60s | 300s | 1 | `circuit_usgbc_state` |
| NOAA Climate | 10 failures / 60s | 30s | 2 | `circuit_noaa_state` |
| NREL PVWatts | 5 failures / 60s | 60s | 1 | `circuit_nrel_state` |
| Google Maps | 5 failures / 60s | 60s | 1 | `circuit_google_state` |
| ArcGIS | 5 failures / 60s | 120s | 1 | `circuit_arcgis_state` |

#### 5.4.3 Graceful Degradation

The platform implements a **degradation cascade** when APIs fail:

```
[Live API] → [Cached Data] → [Static Fallback] → [Synthetic Estimate] → [Human Input Required]
   │               │                │                    │                  │
   │           (Redis TTL)    (Bundled JSON)       (ML model + rules)     (HITL trigger)
   │               │                │                    │                  │
 Fresh          Stale but        Last known          AI-generated       Escalate to
 accurate       acceptable       annual values       conservative       reviewer with
                              estimate            data gap notice
```

| Degradation Level | Data Quality | User Notification | HITL Trigger |
|------------------|--------------|-----------------|--------------|
| L1 - Cached | Good | None | No |
| L2 - Static | Acceptable | Info banner | No |
| L3 - Synthetic | Review required | Warning banner | Yes |
| L4 - Missing | Incomplete | Error banner | Yes (blocking) |

#### 5.4.4 Alert Thresholds for API Health

Alerts are routed to PagerDuty with severity levels based on customer impact.

| Alert Condition | Severity | Notification Channel | Response SLA |
|-----------------|----------|---------------------|--------------|
| P0 API circuit open > 5 min | P1 (Critical) | PagerDuty + Slack #alerts-critical + SMS | 15 min |
| P0 API circuit open > 15 min | P1 (Critical) | Escalate to engineering manager | 5 min |
| P1 API circuit open > 30 min | P2 (High) | PagerDuty + Slack #alerts-high | 1 hour |
| API error rate > 10% for 5 min | P2 (High) | Slack #alerts-high | 1 hour |
| API latency p99 > 10s for 10 min | P3 (Medium) | Slack #alerts-medium | 4 hours |
| API cost > 150% of daily budget | P2 (High) | PagerDuty + email to billing admin | 1 hour |
| Cache hit rate < 50% for 30 min | P3 (Medium) | Slack #alerts-medium | 4 hours |

### 5.5 Data Freshness & Caching

The following table defines refresh frequencies and cache TTLs for all data types consumed by the platform. TTLs are optimized to balance data accuracy with API cost and rate limit compliance.

| Data Type | Primary Source | Refresh Frequency | Cache TTL | Fallback Source | Data Versioning |
|-----------|--------------|-------------------|-----------|-----------------|-------------------|
| Grid emission factors (CO2, CH4, N2O) | EPA eGRID | Annual (Q1 release) | 1 year (31,536,000s) | Previous year eGRID | `egrid-{YYYY}` |
| GWP values (refrigerants) | IPCC AR6 | Every 5-7 years | Permanent (no expiry) | IPCC AR5 | `ipcc-ar6-v1` |
| EPD embodied carbon data | EC3 Database | Real-time | 24 hours (86,400s) | EC3 weekly export | `ec3-{YYYY-MM-DD}` |
| Material health data (HPDs) | HPD Repository | Weekly batch | 7 days (604,800s) | HPD quarterly export | `hpd-{YYYY-WW}` |
| Weather / climate normals | NOAA Climate | Daily | 1 hour (3,600s) | Climate normals (static) | `noaa-{YYYYMMDD-HH}` |
| Rainfall depth-frequency | NOAA Atlas 14 | Annual | 1 year | Previous Atlas | `atlas14-v3` |
| Solar resource data | NREL PVWatts | Monthly | 30 days (2,592,000s) | NSRDB static | `pvwatts-v8` |
| Air quality index | EPA AirNow | Hourly | 1 hour | Static AQI zones | `aqi-{YYYYMMDD-HH}` |
| Flood zone maps | FEMA NFHL | Annual | 6 months (15,552,000s) | FIRM panel archive | `nfhl-{YYYY}` |
| Demographic data | US Census ACS | Annual | 1 year | Decennial Census | `acs-5year-{YYYY}` |
| Product efficiency ratings | ENERGY STAR | Quarterly | 90 days (7,776,000s) | Previous quarter | `es-{YYYY-Q}` |
| Low-emitting certifications | GREENGUARD | Weekly | 7 days | Previous week | `gg-{YYYY-WW}` |
| Flooring certifications | FloorScore | Weekly | 7 days | Previous week | `fs-{YYYY-WW}` |
| REC / carbon offsets | Green-e | Real-time | 24 hours | Quarterly registry | `greene-{YYYYMMDD}` |
| Walk / transit scores | Walk Score | Monthly | 30 days | Cached scores | `ws-{YYYY-MM}` |
| Soil survey data | USDA NRCS | Annual | 1 year | SSURGO static | `ssurgo-{YYYY}` |
| Wetland / habitat data | USFWS NWI | Quarterly | 90 days | Previous quarter | `nwi-{YYYY-Q}` |
| Brownfield sites | EPA | Annual | 1 year | Previous year | `bf-{YYYY}` |
| EJ screening metrics | EPA EJScreen | Annual | 1 year | Previous year | `ejs-{YYYY}` |
| Transit schedules | GTFS | Daily | 24 hours | Static GTFS | `gtfs-{YYYYMMDD}` |
| Utility interval data | Green Button | Real-time | 15 minutes | Aggregated monthly | `gb-{YYYYMMDDHHMM}` |
| IAQ sensor readings | Awair / Kaiterra | Real-time | 5 minutes | Last known value | `iaq-{YYYYMMDDHHMM}` |
| Water meter readings | Various | Real-time | 15 minutes | Last known value | `wm-{YYYYMMDDHHMM}` |
| Demand response events | OpenADR | Event-driven | Duration of event | None (event-driven) | `adr-{event_id}` |
| BIM model elements | Autodesk Forge | Per-project | 7 days | Cached model export | `bim-{project_id}` |
| Energy model outputs | EnergyPlus | Per-simulation | 7 days | Previous simulation | `eplus-{project_id}` |
| Credential verification | GBCI | Weekly | 7 days | Previous week | `gbci-{YYYY-WW}` |

---

## Section 6: HITL & Workflow Design

### 6.1 HITL Architecture

The Human-in-the-Loop (HITL) system ensures that all AI-generated credit documentation receives expert review before submission to USGBC. The architecture is built on Deer-Flow's messaging channel infrastructure, extended with a custom React-based review dashboard for complex multi-document reviews.

#### 6.1.1 Messaging Channels

| Channel | Use Case | Notification Type | Response Latency | Escalation Path |
|---------|----------|-------------------|------------------|-----------------|
| **Slack** | Primary channel for LEED consultants | Interactive blocks with Approve/Reject/Revise buttons | Real-time (WebSocket) | Auto-escalate to email after 50% SLA elapsed |
| **Email** | Secondary channel; formal approvals; external reviewers | HTML digest with review links | Near real-time (poll: 60s) | Auto-escalate to manager email after 90% SLA |
| **Web UI** | Complex multi-credit reviews; document preview; annotation | Full review dashboard | Real-time (SSE/WebSocket) | In-app alert + Slack ping |
| **Telegram** | Mobile notifications for urgent reviews | Inline keyboard buttons | Real-time | Escalate to SMS after 80% SLA |
| **SMS** | Break-glass escalation only | Text with review URL | Near real-time | None (final channel) |

**Channel Selection Logic:**
```python
# /backend/hitl/channel_router.py

def select_channel(reviewer: User, credit_code: str, 
                   urgency: str, review_complexity: str) -> list:
    channels = []
    
    # Primary: Slack for all internal LEED APs
    if reviewer.slack_id and reviewer.preferences.slack_enabled:
        channels.append("slack")
    
    # Email always included as fallback
    channels.append("email")
    
    # Web UI for complex reviews (>3 documents or >10 checklist items)
    if review_complexity == "high":
        channels.insert(0, "web_ui")
    
    # Telegram for mobile-first reviewers
    if reviewer.telegram_id and reviewer.preferences.telegram_enabled:
        channels.append("telegram")
    
    # SMS for urgent reviews only
    if urgency == "urgent" and reviewer.phone:
        channels.append("sms")
    
    return channels
```

#### 6.1.2 SLA Tracking and Escalation

Each HITL review task carries a Service Level Agreement (SLA) based on credit complexity and business criticality.

| Credit Complexity | Base SLA | Reviewer Tier | Escalation at 50% SLA | Escalation at 90% SLA |
|-------------------|----------|---------------|----------------------|----------------------|
| Simple (1-2 docs, <5 checklist items) | 24 hours | Any LEED AP | Email reminder | Manager notification |
| Standard (3-5 docs, 5-10 checklist items) | 48 hours | LEED AP with specialty | Slack DM + email | Manager + project lead |
| Complex (>5 docs, >10 checklist items, calculations) | 72 hours | Senior LEED AP or PE | Slack + web UI alert | Director notification |
| Critical (carbon credits, legal exposure) | 24 hours | Principal / Project Director | Immediate manager ping | Auto-reassign to backup |

**SLA Monitoring Implementation:**
```python
# SLA tracking with automatic escalation

class SLAMonitor:
    def __init__(self, redis: Redis, notification_service: NotificationService):
        self.redis = redis
        self.notifications = notification_service
    
    async def track_task(self, task_id: str, reviewer_id: str, 
                         sla_hours: int, credit_code: str):
        key = f"hitl:sla:{task_id}"
        expires_at = datetime.utcnow() + timedelta(hours=sla_hours)
        
        await self.redis.hset(key, mapping={
            "reviewer_id": reviewer_id,
            "credit_code": credit_code,
            "expires_at": expires_at.isoformat(),
            "status": "pending",
            "escalation_50_sent": "false",
            "escalation_90_sent": "false"
        })
        await self.redis.expire(key, int(sla_hours * 3600 * 1.5))  # 1.5x buffer
    
    async def check_escalations(self):
        """Run every 5 minutes via Celery beat"""
        pending_tasks = await self.redis.keys("hitl:sla:*")
        
        for task_key in pending_tasks:
            task = await self.redis.hgetall(task_key)
            expires = datetime.fromisoformat(task["expires_at"])
            remaining_pct = (expires - datetime.utcnow()) / (
                expires - datetime.fromisoformat(task.get("created_at", task["expires_at"]))
            ) * 100
            
            if remaining_pct <= 50 and task["escalation_50_sent"] == "false":
                await self._send_50_escalation(task)
            
            if remaining_pct <= 10 and task["escalation_90_sent"] == "false":
                await self._send_90_escalation(task)
            
            if datetime.utcnow() > expires:
                await self._handle_sla_breach(task)
```

#### 6.1.3 Checkpoint Placement Strategy

HITL checkpoints are placed at deterministic steps in each credit workflow. The placement follows three principles:

1. **After data aggregation**: Once all external data is fetched and calculations are complete
2. **Before document generation**: Before PDF/Excel outputs are finalized (to avoid rework)
3. **Before USGBC submission**: Final gate before any data leaves the platform

| Workflow Phase | Typical Step | Checkpoint? | Rationale |
|---------------|--------------|-------------|-----------|
| Input validation | Step 1-2 | No | Automated validation handles this |
| Data fetching | Step 3-5 | No | API resilience layer handles failures |
| Calculation | Step 6-7 | **Yes** - Preliminary review | Catch methodology errors early |
| Report generation | Step 8 | **Yes** - Primary review | Review complete document package |
| Quality assurance | Step 9 | **Yes** - Final review | Last gate before submission |
| USGBC submission | Step 10 | **Yes** - Submission approval | Legal/contractual sign-off |

#### 6.1.4 Approval / Rejection / Revision Workflow

When a reviewer receives a HITL task, three actions are available:

| Action | Workflow Effect | Data Persistence | Re-engagement Required |
|--------|----------------|------------------|----------------------|
| **Approve** | Workflow resumes to next node; documents locked | Full audit trail; timestamp + reviewer ID | None |
| **Request Changes** | Workflow rewinds to designated step (default: calculation step); revision notes attached to state | Comments stored in thread; previous version archived | Automatic re-execution; re-review triggered |
| **Reject** | Workflow halts; credit marked as "needs manual preparation"; project lead notified | Rejection reason logged; state snapshot preserved for analysis | Project lead must re-initiate or assign to different reviewer |

```python
# Conditional edge routing in LangGraph based on HITL response

workflow.add_conditional_edges(
    "hitl_review",
    route_by_hitl_action,
    {
        "approve": "finalize_documents",
        "request_changes": "recalculate_with_feedback",
        "reject": "manual_preparation_required",
        "escalate": "director_review"
    }
)

def route_by_hitl_action(state: LEEDState) -> str:
    action = state["hitl_result"]["action"]
    
    if action == "request_changes":
        # Store feedback for recalculation context
        state["revision_notes"] = state["hitl_result"]["comments"]
        state["return_to_step"] = state["hitl_result"].get("return_to_step", "calculate")
    
    return action
```

### 6.2 HITL Checkpoint Specifications Table

The following table defines checkpoints for the 16 highest-priority LEED v5 credits. Each checkpoint specifies the workflow step, required reviewer role, SLA, and the checklist items for review.

| Credit | Credit Name | Checkpoint Step | Reviewer Role | Min Credential | SLA | Review Items |
|--------|-------------|-----------------|---------------|--------------|-----|--------------|
| IPp3 | Carbon Assessment | Step 7 (calculation complete) | LEED AP BD+C | BD+C specialty | 72h | Energy model inputs verified; material quantities match BOQ; grid emission factors match project eGRID subregion; refrigerant types and charges match specs; embodied carbon values sourced from valid EPDs; 25-year projection methodology matches LEED v5 guidance |
| IPp3 | Carbon Assessment | Step 9 (pre-submission) | Principal / LEED Fellow | Any LEED AP + 10+ yrs exp | 24h | Decarbonization plan is actionable; refrigerant management plan includes phase-out schedule; total carbon budget within target; all supporting documentation attached |
| EAp1 | Operational Carbon Projection | Step 7 | LEED AP BD+C or O+M | BD+C or O+M | 72h | Energy use intensity (EUI) baseline from approved model; grid factors from eGRID 20XX; on-site renewables accounted; refrigerant GWP values from IPCC AR6; decarbonization milestones realistic |
| EAc4 | Renewable Energy | Step 6 | LEED AP BD+C | BD+C | 48h | PVWatts production estimates match system sizing; Green-e RECs valid and unretired; on-site renewable fractions calculated correctly; utility rate structures applied accurately |
| MRp2 | Quantify Embodied Carbon | Step 7 | LEED AP BD+C | BD+C | 72h | Material quantities extracted from BIM or verified BOQ; EC3 category mappings correct; EPD scope matches (cradle-to-gate vs cradle-to-grave); system boundary consistent across all materials; life cycle stages A1-A3 included |
| MRc2 | Reduce Embodied Carbon | Step 7 | LEED AP BD+C | BD+C | 72h | Baseline building definition matches LEED guidance; product-specific EPDs prioritized over industry averages; percent reduction calculated against correct baseline; structural materials identified as top 10 by cost |
| MRc3 | Low-Emitting Materials | Step 6 | LEED AP ID+C or BD+C | ID+C or BD+C | 48h | GREENGUARD / FloorScore certifications current (not expired); CDPH Standard Method version correct; VOC limit values match credit requirements; product categories match specification sections |
| MRc4 | Building Product Selection | Step 7 | LEED AP BD+C | BD+C | 72h | EPDs from valid program operators (ISO 14025); HPDs at v2.2 or later; FSC chain-of-custody certificates current; responsible sourcing claims verified; product counts meet credit thresholds |
| SSc3 | Rainwater Management | Step 6 | LEED AP BD+C or Landscape | BD+C or SITES AP | 48h | NOAA rainfall depths from Atlas 14 v3; soil infiltration rates from NRCS SSURGO; stormwater model (if used) calibrated; runoff volumes calculated for 95th percentile event; LID strategies documented |
| WEp2 | Minimum Water Efficiency | Step 5 | LEED AP BD+C or WELL AP | BD+C | 24h | ENERGY STAR fixture flow rates match product specs; occupancy counts from approved program; water use baseline calculated per WE prerequisite; product model numbers verified |
| EAc7 | Enhanced Refrigerant Management | Step 6 | LEED AP BD+C or PE | BD+C or PE license | 48h | Refrigerant GWP values from EPA SNAP / IPCC AR6; total refrigerant charge calculations accurate; equipment efficiencies from AHRI directory; leak rate assumptions documented |
| LTc3 | Compact and Connected Development | Step 6 | LEED AP ND or BD+C | ND or BD+C | 48h | Walk Score matches project address; GTFS transit data current; census block group demographics correct; FAR / density calculations match zoning; diverse uses within 1/2-mile radius verified |
| LTc1 | Sensitive Land Protection | Step 6 | LEED AP BD+C or Landscape | BD+C | 48h | FEMA flood zone designation matches official maps; wetland data from NWI current; USFWS critical habitat search complete; prime farmland from NRCS correct; site plan boundaries accurate |
| IPp2 | Human Impact Assessment | Step 6 | LEED AP BD+C or SITES AP | BD+C or SITES AP | 48h | Census block group data from ACS 5-year; EJScreen indicators mapped correctly; low-income / minority populations identified per HUD definition; sensitive institutions within 1 mile verified |
| PRc2 | LEED AP on Project | Step 4 | LEED AP BD+C | BD+C | 24h | GBCI credential verification current; LEED AP specialty matches project type; credential not expired or revoked; project role description adequate |
| EAp5 | Fundamental Refrigerant Management | Step 5 | LEED AP BD+C | BD+C | 24h | EPA SNAP approved refrigerant list current; Montreal Protocol phase-out schedule applied; CFC-based equipment identified if present; replacement plan documented |

### 6.3 Review Dashboard Design

The HITL Review Dashboard is a React-based single-page application integrated into the platform frontend. It provides a unified interface for all review tasks regardless of the notification channel that initiated them.

#### 6.3.1 Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  HITL Review Dashboard                                    [User]  │
├──────────────────┬──────────────────────────────────────────────┤
│                  │                                              │
│  TASK QUEUE      │  DOCUMENT PREVIEW                            │
│  ┌────────────┐  │  ┌──────────────────────────────────────┐    │
│  │ ▶ IPp3     │  │  │ [PDF Viewer / Excel Grid /         │    │
│  │   Carbon   │  │  │  Image Gallery / Map Overlay]      │    │
│  │   Due: 18h │  │  │                                      │    │
│  ├────────────┤  │  │  Page 3 of 12                        │    │
│  │   EAc4     │  │  └──────────────────────────────────────┘    │
│  │   Solar    │  │                                              │
│  │   Due: 42h │  │  REVIEW CHECKLIST                            │
│  ├────────────┤  │  ┌──────────────────────────────────────┐    │
│  │   MRp2     │  │  │ □ Energy model inputs verified         │    │
│  │   Embodied │  │  │ □ Material quantities match BOQ      │    │
│  │   Due: 66h │  │  │ □ Grid emission factors verified     │    │
│  └────────────┘  │  │ □ EPD sources current and valid      │    │
│                  │  │ □ Calculation methodology correct    │    │
│  FILTERS         │  │  │ □ Supporting docs attached           │    │
│  [All] [Due Soon]│  │  └──────────────────────────────────────┘    │
│  [Overdue]       │  │                                              │
│                  │  │  COMMENT THREAD                              │
│                  │  │  ┌──────────────────────────────────────┐    │
│                  │  │  │ [AI]: Generated 25-year projection │    │
│                  │  │  │ [Reviewer]: Please verify concrete    │    │
│                  │  │  │             quantity is post-tension │    │
│                  │  │  │ [AI]: Adjusted to 1,240 m³          │    │
│                  │  │  │ [Add comment...]                     │    │
│                  │  │  └──────────────────────────────────────┘    │
│                  │  │                                              │
│                  │  │  SLA TIMER          ACTIONS                   │
│                  │  │  ┌────────┐  ┌────┐ ┌─────────┐ ┌───────┐   │
│                  │  │  │ ⏱ 18h  │  │ ✅ │ │ 📝 Revise│ │ ❌ Rej │   │
│                  │  │  │ remaining│  │ Approve│ │         │ │       │   │
│                  │  │  └────────┘  └────┘ └─────────┘ └───────┘   │
│                  │  │                                              │
└──────────────────┴──────────────────────────────────────────────┘
```

#### 6.3.2 Component Specifications

| Component | Technology | Key Features | Accessibility |
|-----------|-----------|-------------|---------------|
| **Document Preview** | `react-pdf` (PDF), `ag-grid-react` (Excel), `leaflet` (Maps) | Multi-format rendering; page navigation; zoom; text search | Keyboard shortcuts; screen reader labels; high-contrast mode |
| **Checklist** | Custom React + `formik` | Required/optional items; progress bar; auto-save state; partial completion warning | ARIA checkboxes; focus management; error announcements |
| **Comment Thread** | Custom React + SSE | Real-time updates; @mentions; threaded replies; markdown support | Live region for new messages; keyboard navigation |
| **SLA Countdown** | `react-countdown` | Color-coded (green >50%, yellow <50%, red <10%); pulsating at <1h | Screen reader announces time remaining every 15 min |
| **Action Buttons** | Custom React | Approve (green), Request Changes (amber), Reject (red); confirmation dialogs for destructive actions | High-contrast focus indicators; confirmation for reject |

**TypeScript Interface Definitions:**
```typescript
// /frontend/src/types/hitl.ts

interface HITLTask {
  id: string;
  project_id: string;
  credit_code: string;
  credit_name: string;
  workflow_step: number;
  step_name: string;
  reviewer: {
    user_id: string;
    name: string;
    email: string;
    slack_id?: string;
    credential: string;  // e.g., "LEED AP BD+C"
  };
  documents: Document[];
  checklist: ChecklistItem[];
  comments: Comment[];
  sla: {
    assigned_at: string;  // ISO 8601
    expires_at: string;
    hours_total: number;
    hours_remaining: number;
  };
  status: "pending" | "approved" | "rejected" | "changes_requested" | "escalated";
  priority: "low" | "normal" | "high" | "urgent";
}

interface ChecklistItem {
  id: string;
  text: string;
  required: boolean;
  checked: boolean;
  category: "data_verification" | "calculation" | "documentation" | "compliance";
  help_text?: string;
  reference_link?: string;
}

interface Comment {
  id: string;
  author: "ai" | "reviewer" | "system";
  user_id?: string;
  text: string;
  timestamp: string;
  reply_to?: string;
  attachments?: Attachment[];
}
```

#### 6.3.3 Review Actions API

| Endpoint | Method | Auth | Body | Response | Rate Limit |
|----------|--------|------|------|----------|------------|
| `/api/v1/hitl/tasks` | GET | Bearer + role: `leed_ap` | `?status=pending&project_id=xxx` | `HITLTask[]` | 100/min |
| `/api/v1/hitl/tasks/{task_id}` | GET | Bearer + task assignee | - | `HITLTask` | 100/min |
| `/api/v1/hitl/tasks/{task_id}/approve` | POST | Bearer + task assignee | `{checklist: {...}, comments: string, final_note?: string}` | `{status: "approved", workflow_resumed: true}` | 20/min |
| `/api/v1/hitl/tasks/{task_id}/reject` | POST | Bearer + task assignee | `{reason: string, comments: string}` | `{status: "rejected", workflow_state: "manual_preparation"}` | 20/min |
| `/api/v1/hitl/tasks/{task_id}/request-changes` | POST | Bearer + task assignee | `{comments: string, return_to_step?: number, checklist_feedback: {...}}` | `{status: "changes_requested", workflow_rewound_to: number}` | 20/min |
| `/api/v1/hitl/tasks/{task_id}/escalate` | POST | Bearer + task assignee | `{reason: string, target_reviewer?: string}` | `{status: "escalated", new_assignee: string}` | 10/min |
| `/api/v1/hitl/tasks/{task_id}/comments` | POST | Bearer + task assignee | `{text: string, reply_to?: string}` | `Comment` | 50/min |

### 6.4 Workflow State Machine

The platform uses **LangGraph** for durable workflow execution. Each credit workflow is modeled as a directed state graph with checkpoint persistence to PostgreSQL (via `PostgresSaver`).

#### 6.4.1 State Definition

```python
# /backend/workflows/state.py

from typing import TypedDict, Optional, Literal, Annotated
from operator import add

class LEEDState(TypedDict):
    # Project identification
    project_id: str
    credit_code: str
    
    # Workflow progression
    current_step: int
    step_history: Annotated[list, add]  # Accumulates across retries
    
    # Data containers
    inputs: dict                    # Validated user inputs
    api_data: dict                  # Fetched external data
    calculations: dict              # Computed values
    documents: dict                 # Generated document paths
    
    # HITL state
    hitl_task_id: Optional[str]
    hitl_result: Optional[dict]     # {action: str, comments: str, reviewer_id: str}
    revision_count: Annotated[int, add]  # Tracks rework cycles
    
    # Quality gates
    validation_errors: list
    confidence_score: float         # AI confidence 0.0-1.0
    
    # Final status
    status: Literal["pending", "in_progress", "awaiting_review", 
                    "approved", "rejected", "submitted", "error"]
    submitted_to_usgbc: bool
    usgbc_submission_id: Optional[str]
```

#### 6.4.2 State Transition Diagram

```
                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  validate   │
                    │   inputs    │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │ invalid    │ valid      │
              ▼            ▼            │
       ┌─────────┐  ┌─────────────┐    │
       │  ERROR  │  │  fetch_api  │    │
       │ (retry) │  │    data     │    │
       └────┬────┘  └──────┬──────┘    │
            │              │            │
            │    ┌─────────┼─────────┐  │
            │    │ failure │ success │  │
            │    ▼         ▼         │  │
            │ ┌────────┐ ┌──────────┐│  │
            │ │ fallback│ │ calculate││  │
            │ │  cache   │ │          ││  │
            │ └────┬───┘ └────┬─────││  │
            │      │          │      ││  │
            └──────┘          ▼      ││  │
                         ┌──────────┐││  │
                         │  HITL    │◄┘│  │
                         │checkpoint│  │  │
                         │ (step N) │  │  │
                         └────┬─────┘  │  │
                              │        │  │
              ┌───────────────┼────────┼──┘
              │               │        │
    ┌─────────┼─────────┐     │        │
    │ approve │ reject  │ changes    │
    ▼         ▼         ▼     │        │
 ┌──────┐ ┌────────┐ ┌──────┐│        │
 │generate│ │ MANUAL │ │recalc││        │
 │ docs   │ │ PREP   │ │with  ││        │
 └──┬───┘ └────────┘ │feedback│        │
    │                └──┬───┘        │
    │                   │              │
    │    ┌──────────────┘              │
    │    │                             │
    │    ▼                             │
    │ ┌──────────┐                     │
    │ │  HITL    │◄────────────────────┘
    │ │ (final)  │
    │ └────┬─────┘
    │      │
    │ ┌────┴────┐
    │ │ approve │ reject
    │ ▼         ▼
    │┌────────┐ ┌────────┐
    ││submit  │ │ MANUAL  │
    ││to USGBC│ │ PREP    │
    │└───┬────┘ └────────┘
    │    │
    │    ▼
    │ ┌─────────┐
    │ │  END    │
    │ │submitted│
    │ └─────────┘
    │
    └──────────────────────┘
```

#### 6.4.3 LangGraph Node Definitions

| Node Name | Function | Input State | Output State | Idempotent | Checkpoint After |
|-----------|----------|-------------|--------------|-----------|------------------|
| `validate_inputs` | Schema validation, type coercion, range checks | `inputs` | `validation_errors` (empty = pass) | Yes | Yes |
| `fetch_api_data` | Parallel API calls with fallback chains | `inputs` | `api_data` | Yes (cache-aware) | Yes |
| `calculate` | Credit-specific calculations | `inputs`, `api_data` | `calculations`, `confidence_score` | Yes | Yes |
| `hitl_preliminary` | First HITL checkpoint (methodology review) | `calculations` | `hitl_task_id`, `awaiting_review` | No | Yes (blocking) |
| `generate_documents` | PDF/Excel/HTML generation | `calculations`, `api_data` | `documents` | Yes | Yes |
| `hitl_final` | Final document review checkpoint | `documents` | `hitl_result` | No | Yes (blocking) |
| `quality_assurance` | Automated QA: completeness, cross-reference, consistency | `documents` | `validation_errors` | Yes | Yes |
| `submit_usgbc` | Upload to LEED Online via Arc API | `documents` | `usgbc_submission_id` | No | Yes |
| `recalculate_with_feedback` | Adjust calculations per reviewer comments | `calculations`, `hitl_result` | `calculations` (revised) | No | Yes |
| `manual_preparation` | Hand off to manual workflow, archive AI attempt | `state` | `status: "manual"` | Yes | Yes |

#### 6.4.4 Conditional Edge Configuration

```python
# /backend/workflows/credit_workflows.py

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver

builder = StateGraph(LEEDState)

# Add all nodes
builder.add_node("validate", validate_inputs)
builder.add_node("fetch_data", fetch_api_data)
builder.add_node("calculate", calculate_credit)
builder.add_node("hitl_preliminary", create_hitl_checkpoint)
builder.add_node("generate", generate_documents)
builder.add_node("hitl_final", create_hitl_checkpoint)
builder.add_node("qa", quality_assurance)
builder.add_node("submit", submit_to_usgbc)
builder.add_node("recalculate", recalculate_with_feedback)
builder.add_node("manual", manual_preparation)

# Define edges
builder.set_entry_point("validate")
builder.add_edge("validate", "fetch_data")
builder.add_edge("fetch_data", "calculate")
builder.add_edge("calculate", "hitl_preliminary")
builder.add_edge("generate", "hitl_final")
builder.add_edge("hitl_final", "qa")
builder.add_edge("qa", "submit")
builder.add_edge("submit", END)
builder.add_edge("manual", END)

# Conditional edges from HITL checkpoints
def route_preliminary(state: LEEDState):
    action = state.get("hitl_result", {}).get("action")
    if action == "approve":
        return "generate"
    elif action == "request_changes":
        return "recalculate"
    elif action == "reject":
        return "manual"
    return "hitl_preliminary"  # Still awaiting review

builder.add_conditional_edges(
    "hitl_preliminary",
    route_preliminary,
    {
        "generate": "generate",
        "recalculate": "recalculate",
        "manual": "manual",
        "hitl_preliminary": "hitl_preliminary"  # Loop until resolved
    }
)

def route_final(state: LEEDState):
    action = state.get("hitl_result", {}).get("action")
    if action == "approve":
        return "qa"
    elif action == "request_changes":
        return "generate"  # Regenerate documents with changes
    elif action == "reject":
        return "manual"
    return "hitl_final"

builder.add_conditional_edges(
    "hitl_final",
    route_final,
    {
        "qa": "qa",
        "generate": "generate",
        "manual": "manual",
        "hitl_final": "hitl_final"
    }
)

# Recalculation loop feeds back to preliminary review
builder.add_edge("recalculate", "hitl_preliminary")

# Compile with persistence
with PostgresSaver.from_conn_string(settings.DATABASE_URL) as checkpointer:
    workflow = builder.compile(checkpointer=checkpointer)
```

#### 6.4.5 Checkpoint Persistence

| Checkpoint Property | Value | Purpose |
|--------------------|-------|---------|
| Storage backend | PostgreSQL 15+ with JSONB columns | Durable, queryable state history |
| Table name | `langgraph_checkpoints` | Managed by PostgresSaver |
| Thread ID format | `{project_id}:{credit_code}:{timestamp}` | Unique workflow instance |
| Retention policy | 7 years (aligned with LEED documentation requirements) | Regulatory compliance |
| Encryption | AES-256 at rest (PostgreSQL TDE) | Protect sensitive project data |
| Backup | Daily snapshots to S3 with 30-day retention | Disaster recovery |

---

## Appendix A: API Integration Quick Reference

| API | Base URL | Auth Header | Key Path in Vault |
|-----|----------|-------------|-------------------|
| EPA eGRID | `https://www.epa.gov/egrid/` | None | N/A |
| EC3 Database | `https://etl-api.buildingtransparency.org/` | `Authorization: Bearer {token}` | `leed/apis/ec3/token` |
| USGBC Arc | `https://api.usgbc.org/v3/` | `Authorization: Bearer {access_token}` | `leed/apis/usgbc/oauth` |
| NOAA Climate | `https://www.ncei.noaa.gov/access/services/data/v1` | `token={api_key}` | `leed/apis/noaa/key` |
| NREL PVWatts | `https://developer.nrel.gov/api/pvwatts/v8/` | `api_key={key}` | `leed/apis/nrel/key` |
| US Census | `https://api.census.gov/data/` | `key={api_key}` | `leed/apis/census/key` |
| FEMA NFHL | `https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer` | None | N/A |
| Google Maps | `https://maps.googleapis.com/maps/api/` | `key={api_key}` | `leed/apis/google/key` |
| Green-e | `https://www.green-e.org/api/` | None | N/A |
| Procore | `https://api.procore.com/rest/v1.0/` | `Authorization: Bearer {token}` | `leed/apis/procore/oauth` |

## Appendix B: HITL State Machine Truth Table

| Current State | HITL Action | Next State | Side Effects |
|--------------|-------------|------------|--------------|
| `awaiting_review` (preliminary) | `approve` | `generate_documents` | Lock calculation inputs |
| `awaiting_review` (preliminary) | `request_changes` | `recalculate` | Store feedback in state; increment `revision_count` |
| `awaiting_review` (preliminary) | `reject` | `manual_preparation` | Archive state snapshot; notify project lead |
| `awaiting_review` (final) | `approve` | `quality_assurance` | Lock documents; create submission package |
| `awaiting_review` (final) | `request_changes` | `generate_documents` | Unlock document templates; apply feedback |
| `awaiting_review` (final) | `reject` | `manual_preparation` | Archive all outputs; notify project lead |
| `in_progress` (any step) | `escalate` | `awaiting_review` (new assignee) | Reassign task; reset SLA timer; log escalation |



---

# Master Technical Implementation Document: LEED v5 AI Automation Platform

## Section 7: Implementation Roadmap

### 7.1 Phase 1: Foundation (Weeks 1–2)

The Foundation Phase establishes the platform's core infrastructure on Deer-Flow, validates the end-to-end workflow, and delivers the first fully functional credit skill. The goal is not breadth but confidence in the architecture, deployment pipeline, and human-in-the-loop (HITL) channel.

**Week 1: Deer-Flow Setup and Configuration**

| Day | Task | Deliverable | Owner |
|-----|------|-------------|-------|
| 1 | Clone Deer-Flow repository (`bytedance/deer-flow`) and run `make setup` | Local running instance | DevOps |
| 1 | Configure `config.yaml`: GPT-4o model, AioSandboxProvider, Slack channel | Validated configuration file | DevOps |
| 2 | Build and deploy Docker Compose stack (LangGraph server, gateway, sandbox) | All containers healthy | DevOps |
| 2 | Provision PostgreSQL metadata store and persistent volume for `/mnt/user-data` | Database schema initialized | DevOps |
| 3 | Create `skills/leed/` directory structure for 16 Tier-1 credits | Directory tree with `__init__.py` | Backend |
| 3 | Implement base `LEEDSkill` class extending Deer-Flow's skill contract | Base class with validation hooks | Backend |
| 4–5 | Set up CI/CD pipeline: GitHub Actions → Docker build → staging deploy | Green pipeline on first push | DevOps |

The configuration file (`config.yaml`) for this phase:

```yaml
models:
  - name: gpt-4o
    display_name: GPT-4o
    use: langchain_openai:ChatOpenAI
    model: gpt-4o
    api_key: ${OPENAI_API_KEY}
    temperature: 0.1

sandbox:
  use: deerflow.community.aio_sandbox:AioSandboxProvider
  provisioner_url: http://sandbox:8080
  timeout_seconds: 300

channels:
  slack:
    enabled: true
    bot_token: ${SLACK_BOT_TOKEN}
    app_token: ${SLACK_APP_TOKEN}
    default_channel: "#leed-hitl"
```

**Week 2: First Skill Implementation (PRc2 — LEED AP Credential Verification)**

PRc2 is selected as the first skill because it has the simplest input schema (team roster), no external calculations, a single API dependency (GBCI Credential Directory), and a binary pass/fail outcome. This makes it ideal for validating the entire pipeline from skill invocation through HITL to document generation.

| Step | Activity | Checkpoint |
|------|----------|------------|
| 1 | Write `skills/leed/pr-c2/SKILL.md` with Deer-Flow compatible frontmatter | SKILL.md passes schema validation |
| 2 | Implement `pr-c2` workflow: validate roster → query GBCI API → match credentials → flag missing | Unit tests pass (pytest) |
| 3 | Build Jinja2 document template: `pr-c2-credential-report.html` | Template renders with sample data |
| 4 | Configure HITL checkpoint at Step 2 (credential verification results) | Slack notification fires correctly |
| 5 | Run 5 end-to-end tests: valid roster, missing AP, expired credential, API timeout, malformed input | All 5 pass with correct branching |
| 6 | Execute load test: 50 concurrent PRc2 invocations | p95 latency < 30s, 0% error rate |

The PRc2 skill workflow:

```markdown
## Workflow
1. [AGENT] Validate input roster JSON against schema
2. [TOOL:gbci_lookup] Query GBCI Credential Directory for each team member
3. [AGENT] Cross-match returned credentials against LEED AP requirements
4. [HITL] Send verification summary to Slack with approve/reject buttons
5. [AGENT:report_generator] Generate credential verification PDF
6. [AGENT] Archive output to project persistent storage
```

**End-to-End Workflow Validation**

The E2E validation suite covers:

1. **Happy path**: Complete roster → all credentials verified → HITL approves → PDF generated
2. **API degradation**: GBCI API returns 503 → exponential backoff (1s, 2s, 4s) → fallback to cached directory snapshot
3. **HITL rejection**: Reviewer rejects with comment → workflow rewinds to Step 2 → corrected data re-submitted
4. **Sandbox isolation**: Malicious bash command in skill definition → sandbox kills container, workflow fails gracefully

**HITL Channel Testing (Slack)**

| Test Case | Expected Behavior |
|-----------|-----------------|
| Consultant receives notification | Slack DM with document preview and action buttons |
| Approve action | Workflow resumes to document generation within 5s |
| Reject with comments | Workflow rewinds to previous step, comments stored in state |
| SLA breach (24h elapsed) | Auto-escalation to project manager channel; skill flagged for manual review |
| Channel failure (Slack down) | Fallback to email via SendGrid; workflow pauses, not fails |

---

### 7.2 Phase 2: MVP Skills (Weeks 3–5)

Phase 2 expands from one skill to eight priority skills, integrates the core external APIs, establishes the document template library, and delivers the first version of the consultant dashboard. The eight skills are chosen based on automation confidence score, point value, and API readiness.

**Priority Skill Selection Rationale**

| Skill | Credit | Points | Automation % | Primary API | Why Priority |
|-------|--------|--------|--------------|-------------|--------------|
| WEp2 | Minimum Water Efficiency | 0 (Prereq) | 89.3% | WaterSense/ENERGY STAR | Simple fixture schedule calculations; unlocks water credits |
| IPp1 | Climate Resilience Assessment | 0 (Prereq) | 78.5% | NOAA, Census | Foundation for all IP credits; regional data readily available |
| IPp2 | Human Impact Assessment | 0 (Prereq) | 82.7% | Census, EPA EJScreen | Social equity data accessible via Census API |
| MRc3 | Low-Emitting Materials | 2 | 80.6% | EC3, CDPH | High automation, clear compliance thresholds |
| EQp1 | Minimum Indoor Air Quality | 0 (Prereq) | — | ASHRAE 62.1 tables | Table lookups, no live API dependency |
| EQp2 | Fundamental Air Quality | 0 (Prereq) | 82.5% | EPA AirNow | Simple pollutant threshold comparisons |
| EAp5 | Fundamental Refrigerant Mgmt | 0 (Prereq) | 85.2% | EPA SNAP, AHRI | Equipment schedule parsing + GWP lookup |
| EAc7 | Enhanced Refrigerant Mgmt | 2 | 89.3% | EPA SNAP, IPCC GWP | Builds on EAp5 logic; high point value |

**Week 3: Core API Integration Layer**

All eight skills share a common API integration layer. The layer is built as Deer-Flow tools (`/backend/deerflow/tools/leed/`) with standardized interfaces:

| API | Tool Class | Auth Method | Rate Limit | Fallback Strategy |
|-----|-----------|-------------|------------|-------------------|
| EPA eGRID | `EPAeGRIDTool` | None (public) | 1000 req/hr | Cached annual snapshot (updated quarterly) |
| EPA SNAP | `EPASNAPTool` | API key | 500 req/hr | Local refrigerant GWP database (IPCC AR6) |
| NOAA Climate | `NOAAClimateTool` | Token | 500 req/day | PRISM climate normals (pre-downloaded) |
| EC3 Database | `EC3DatabaseTool` | Bearer token | 200 req/min | CLF Material Baselines CSV (updated monthly) |
| US Census | `CensusAPITool` | Key | No hard limit | Tiger/Line shapefiles (pre-downloaded for top 100 MSAs) |
| ENERGY STAR | `EnergyStarTool` | OAuth 2.0 | 1000 req/day | Product registry XML dump (weekly sync) |
| WaterSense | `WaterSenseTool` | None (public) | No limit | Local fixture efficiency database |
| AHRI Directory | `AHRIDirectoryTool` | Key | 500 req/hr | Quarterly certification CSV export |

Each tool implements the following contract:

```python
class LEEDAPITool(BaseTool):
    name: str
    description: str
    auth_method: AuthMethod
    rate_limit: RateLimit
    fallback_strategy: FallbackStrategy
    
    async def run(self, **kwargs) -> dict:
        # 1. Check rate limit bucket
        # 2. Execute API call with timeout
        # 3. Validate response schema
        # 4. Cache successful response (TTL varies by API)
        # 5. On failure: execute fallback, log degradation event
```

API health monitoring is configured via a scheduled heartbeat job (every 5 minutes) that probes each endpoint and records latency and availability to Prometheus.

**Week 4: Skill Implementation Sprint**

Skills are developed in parallel by three engineers, each owning 2–3 skills. All skills follow the same development checklist:

1. SKILL.md with inputs, workflow, HITL configuration, outputs
2. Input JSON schema with `pydantic` validation
3. Workflow graph with LangGraph state definition
4. Unit tests: mock all APIs, 90%+ coverage
5. Integration tests: call real APIs in sandbox, 5 sample projects
6. Document template (HTML + Jinja2)
7. HITL checkpoint configuration
8. Cross-skill dependency declaration (e.g., EAc7 depends on EAp5 outputs)

**Week 5: Document Template Library and Dashboard v1**

Eight document templates are created, one per MVP skill. Templates are HTML/Jinja2 based and render to PDF via WeasyPrint:

| Template | Output Format | Pages (est.) | Key Sections |
|----------|---------------|--------------|--------------|
| `we-p2-water-min.html` | PDF | 3–5 | Fixture schedule, flow rates, compliance table |
| `ip-p1-climate-resilience.html` | PDF | 8–12 | Hazard summary, adaptation measures, maps |
| `ip-p2-human-impact.html` | PDF | 6–10 | Demographics, equity analysis, mitigation plan |
| `mr-c3-low-emitting.html` | PDF + Excel | 10–20 | Product list, VOC limits, compliance matrix |
| `eq-p1-min-iaq.html` | PDF | 4–6 | Ventilation rates, ASHRAE 62.1 references |
| `eq-p2-fundamental-aq.html` | PDF | 5–8 | Pollutant thresholds, testing protocols |
| `ea-p5-refrigerant.html` | PDF + Excel | 6–10 | Equipment schedule, GWP calculations, phase-out |
| `ea-c7-enhanced-refrigerant.html` | PDF | 8–12 | Baseline comparison, alternatives analysis |

The Consultant Dashboard v1 is a React application with these views:

- **Project List**: All active LEED projects with automation status
- **Credit Board**: Kanban-style view of credits (Not Started → In Progress → HITL Review → Complete)
- **HITL Inbox**: Pending reviews with SLA countdowns
- **Document Vault**: Generated documents with version history
- **API Health**: Real-time status of all integrated APIs

---

### 7.3 Phase 3: Tier 1 Completion (Weeks 6–8)

Phase 3 implements the remaining 8 Tier-1 skills, integrates advanced APIs for geospatial and energy analysis, builds regional data filtering middleware, and enhances the HITL dashboard with batch review capabilities.

**Remaining Tier-1 Skills (Weeks 6–7)**

| Skill | Credit | Points | Automation % | New APIs Required |
|-------|--------|--------|--------------|-------------------|
| IPp3 | Carbon Assessment | 0 (Prereq) | 92.5% | EPA eGRID, EC3, IPCC |
| EAp1 | Operational Carbon Projection | 0 (Prereq) | 89.4% | EPA eGRID, NREL PVWatts |
| EAp2 | Minimum Energy Efficiency | 0 (Prereq) | 85.7% | EnergyPlus (local) |
| MRp2 | Quantify Embodied Carbon | 0 (Prereq) | 87.0% | EC3, CLF Baselines |
| EAc3 | Enhanced Energy Efficiency | 10 | 87.7% | EnergyPlus, ASHRAE 90.1 |
| WEc2 | Enhanced Water Efficiency | 8 | 87.5% | Irrigation calculators, NOAA ET |
| MRc2 | Reduce Embodied Carbon | 6 | 88.4% | EC3, Tally, One Click LCA |
| LTc3 | Compact & Connected Dev | 6 | 88.0% | Walk Score, GTFS, Census |
| SSc3 | Rainwater Management | 3 | 88.0% | NOAA rainfall, NRCS Soil Survey |
| SSc5 | Heat Island Reduction | 2 | 85.3% | SRI databases, Tree Equity Score |
| SSc6 | Light Pollution Reduction | 1 | 90.6% | IES TM-15-11, manufacturer DB |
| LTc1 | Sensitive Land Protection | 1 | 87.6% | FEMA NFHL, NWI, USFWS |
| PRc2 | LEED AP | 1 | 90.1% | GBCI Credential Directory |
| EAc7 | Enhanced Refrigerant | 2 | 89.3% | EPA SNAP, IPCC GWP |
| MRc3 | Low-Emitting Materials | 2 | 80.6% | EC3, CDPH |

Note: Some MVP skills from Phase 2 are refined; new skills in Phase 3 include IPp3, EAp1, EAp2, MRp2, EAc3, WEc2, MRc2, LTc3, SSc3, SSc5, SSc6, LTc1.

**Advanced API Integrations**

| API | Tool Class | Purpose | Limitation |
|-----|-----------|---------|------------|
| NREL PVWatts | `NRELPVWattsTool` | Renewable energy potential estimates | US-only locations |
| USGS National Map | `USGSMapTool` | Topography, watershed boundaries | Rate limited to 10 req/sec |
| FEMA NFHL | `FEMANFHLTool` | Flood hazard zone identification | Requires NFHL service agreement |
| NRCS Soil Survey | `NRCSSoilTool` | Soil hydrologic group for stormwater | Spatial queries only |
| GTFS Feeds | `GTFSFeedTool` | Transit access and frequency | Feed availability varies by agency |
| Walk Score | `WalkScoreTool` | Walkability and transit scores | 5000 calls/day on paid tier |
| Tree Equity Score | `TreeEquityTool` | Urban canopy coverage | US Census tracts only |
| Green-e Climate | `GreeneClimateTool` | Renewable energy certificate tracking | Membership required |

**Regional Data Filtering Middleware**

Not all APIs have global or national coverage. The `RegionalSkillFilter` middleware gates skill availability based on project location:

```python
class RegionalSkillFilter:
    """Filter skills based on regional data availability."""
    
    COVERAGE_MAP = {
        "epa_egrid": ["US"],           # US-only
        "ec3": ["US", "CA", "EU"],     # Limited international
        "walk_score": ["US", "CA", "AU"],
        "noaa_climate": ["US"],
        "nrel_pvwatts": ["US"],
        "fema_nfhl": ["US"],
        "usgs": ["US"],
    }
    
    def filter_skills(self, project_location: GeoPoint, skills: list) -> list:
        available = []
        for skill in skills:
            required = skill.metadata.get("required_apis", [])
            unavailable = [a for a in required 
                          if not self.is_available(a, project_location)]
            if unavailable:
                available.append({
                    **skill,
                    "disabled": True,
                    "reason": f"Unavailable APIs: {', '.join(unavailable)}",
                    "manual_override": True
                })
            else:
                available.append(skill)
        return available
```

When a skill is disabled for a region, the consultant dashboard shows a grayed-out card with an explanation and a "Request Manual Override" button, which triggers an email to the platform administrator.

**HITL Dashboard Enhancements (Week 8)**

- **Batch Review Mode**: Group related skills (e.g., EAp5 + EAc7 refrigerant pair) into a single review bundle
- **Side-by-Side Comparison**: Show AI-generated document next to LEED v5 reference guide excerpt for easy validation
- **Confidence Indicators**: Color-coded badges (Green: >90% confidence, Yellow: 70–90%, Red: <70%) on every AI-generated section
- **Review History**: Full audit trail of who approved what, when, with comments
- **SLA Analytics**: Average review time per consultant, bottleneck identification

---

### 7.4 Phase 4: Production Hardening (Weeks 9–10)

Phase 4 transitions the platform from functional to production-grade. This includes load testing, security hardening, USGBC Arc integration for direct submission, comprehensive monitoring, and documentation/training.

**Load Testing and Performance Optimization**

| Test Scenario | Target Metric | Baseline (Phase 3) | Target (Phase 4) |
|-------------|-------------|-------------------|-----------------|
| Single skill E2E latency (p99) | < 60s | 85s | 45s |
| 16-skill parallel execution | < 5 min | 8 min | 4 min |
| Concurrent projects (100) | 0% error | 2% timeout | 0% error |
| Document generation throughput | 10 docs/min | 6 docs/min | 15 docs/min |
| HITL notification latency | < 10s | 15s | 5s |

Optimization strategies:
1. **API Response Caching**: Redis layer with TTLs tuned per API (NOAA: 1 day, EPA eGRID: 7 days, EC3: 1 hour)
2. **Skill Pre-warming**: Sandbox containers kept warm for frequently used skills
3. **Parallel API Calls**: `asyncio.gather()` for independent API fetches within a skill
4. **Document Generation Queue**: Celery workers with priority routing (HITL-blocked docs get priority)

**Security Audit and Penetration Testing**

| Area | Test | Tool | Acceptance Criteria |
|------|------|------|---------------------|
| API Gateway | OWASP Top 10 | Burp Suite | Zero critical/high findings |
| Sandbox Escape | Container breakout | Custom scripts | No host access from sandbox |
| Data Encryption | TLS 1.3, AES-256 at rest | SSL Labs, manual review | A+ rating, encrypted volumes |
| Authentication | JWT validation, token expiry | Custom scripts | No valid token reuse after logout |
| PII Handling | Census data exposure | Static analysis | No PII logged or cached beyond session |
| Dependency Scan | Known CVEs | Snyk, Trivy | Zero critical CVEs in production image |

**USGBC Arc Integration for Direct Submission**

The USGBC Arc platform provides a REST API for LEED Online submissions. Integration enables direct upload of generated documentation:

```python
class USGBCArcTool(BaseTool):
    name = "usgbc_arc"
    description = "Submit credit documentation to LEED Online"
    
    async def run(self, project_id: str, credit_code: str, 
                  documents: list[Document]) -> dict:
        # 1. Authenticate with OAuth 2.0 client credentials
        token = await self.get_access_token()
        
        # 2. Upload documents to Arc document store
        upload_results = []
        for doc in documents:
            result = await self.upload_document(project_id, doc, token)
            upload_results.append(result)
        
        # 3. Submit credit with document references
        submission = await self.submit_credit(
            project_id=project_id,
            credit_code=credit_code,
            document_ids=[r["id"] for r in upload_results],
            token=token
        )
        
        return {
            "submission_id": submission["id"],
            "status": submission["status"],  # "submitted" | "under_review"
            "document_urls": [r["url"] for r in upload_results],
            "arc_link": f"https://arc.usgbc.org/projects/{project_id}/credits/{credit_code}"
        }
```

API endpoint details:

| Endpoint | Method | Auth | Rate Limit | Fallback |
|----------|--------|------|------------|----------|
| `https://api.usgbc.org/v3/auth/token` | POST | Client credentials | N/A | Cached token (59 min TTL) |
| `https://api.usgbc.org/v3/projects/{id}/documents` | POST | Bearer token | 100 req/min | Queue for retry |
| `https://api.usgbc.org/v3/projects/{id}/credits/{code}/submit` | POST | Bearer token | 50 req/min | Manual download + upload |

**Monitoring and Alerting Setup**

Prometheus + Grafana stack deployed alongside the application:

| Metric | Alert Threshold | Notification Channel |
|--------|-----------------|----------------------|
| API error rate > 10% for 5 min | PagerDuty (Critical) | #leed-alerts (Slack) |
| Skill execution failure rate > 5% | PagerDuty (Warning) | #leed-alerts (Slack) |
| HITL SLA breach (review > 24h) | Email to project manager | #leed-ops (Slack) |
| Document generation queue depth > 100 | Auto-scale Celery workers | #leed-ops (Slack) |
| Sandbox container crash loop | PagerDuty (Critical) | #leed-alerts (Slack) |
| API latency p99 > 10s | PagerDuty (Warning) | #leed-alerts (Slack) |

**Documentation and Training Materials**

| Document | Audience | Format | Length |
|----------|----------|--------|--------|
| Platform Administration Guide | DevOps / SRE | Markdown + PDF | 80 pages |
| LEED Consultant Training | End users | Video + interactive walkthrough | 4 hours |
| Skill Development Guide | Backend engineers | Markdown with code examples | 60 pages |
| API Integration Reference | Backend engineers | OpenAPI spec + examples | Auto-generated |
| Troubleshooting Runbook | Support team | Confluence | 40 pages |
| LEED v5 Credit Mapping | All stakeholders | Spreadsheet + narrative | 1 per credit |

---

### 7.5 Resource Requirements Table

| Phase | Engineers | Duration | Skills Delivered | APIs Integrated | Points Automated |
|-------|-----------|----------|------------------|-----------------|------------------|
| 1 | 2 | 2 weeks | 1 (PRc2) | 0 (internal only) | 0 |
| 2 | 3 | 3 weeks | 8 (WEp2, IPp1, IPp2, MRc3, EQp1, EQp2, EAp5, EAc7) | 8 (EPA, NOAA, EC3, Census, ENERGY STAR, WaterSense, AHRI, GBCI) | 2 |
| 3 | 4 | 3 weeks | 16 (all Tier 1) | 20+ (NREL, USGS, FEMA, NRCS, Walk Score, GTFS, Tree Equity, etc.) | 40 |
| 4 | 3 | 2 weeks | 16 (hardened) | 20+ (USGBC Arc added) | 40 |
| **Total** | **3.25 FTE avg** | **10 weeks** | **16 skills** | **20+ APIs** | **40 points** |

Engineer role breakdown across phases:

| Role | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|------|---------|---------|---------|---------|
| DevOps / Platform | 1.0 | 0.5 | 0.5 | 1.0 |
| Backend / Skills | 1.0 | 2.0 | 2.5 | 1.0 |
| Frontend / Dashboard | 0 | 0.5 | 1.0 | 1.0 |
| QA / Test Automation | 0 | 0 | 0 | 1.0 |
| **Total** | **2.0** | **3.0** | **4.0** | **3.0** |

Infrastructure cost estimates (monthly, production):

| Component | Specification | Monthly Cost |
|-----------|-------------|--------------|
| Compute (ECS/EKS) | 6 nodes × 8 vCPU / 32 GB | $1,200 |
| GPU (OpenAI via API) | GPT-4o tokens | $800–2,500 (variable) |
| PostgreSQL (RDS) | db.r6g.xlarge, Multi-AZ | $450 |
| Redis (ElastiCache) | cache.r6g.large | $180 |
| Document storage (S3) | 500 GB, infrequent access | $25 |
| CDN (CloudFront) | Template assets, PDFs | $50 |
| Monitoring (Grafana Cloud) | Pro plan | $100 |
| **Total** | | **$2,805–4,505** |

---

### 7.6 Milestone Timeline (Gantt-Style Text Table)

| Week | Milestone | Deliverable | Owner | Dependencies |
|------|-----------|-------------|-------|--------------|
| 1 | Deer-Flow infrastructure live | Running Docker Compose stack; `make setup` passes | DevOps | None |
| 1 | CI/CD pipeline green | GitHub Actions builds and deploys to staging | DevOps | Deer-Flow repo |
| 2 | First skill end-to-end | PRc2 completes full workflow: input → HITL → PDF | Backend | Week 1 infrastructure |
| 2 | HITL channel validated | Slack approve/reject/comment actions resume workflow | Backend | PRc2 skill |
| 3 | API integration layer | 8 tools with auth, rate limiting, caching, fallback | Backend | Week 2 baseline |
| 3 | WEp2 + EQp1 skills | Water efficiency and IAQ prerequisite working | Backend | API layer |
| 4 | IPp1 + IPp2 skills | Climate resilience and human impact working | Backend | Census + NOAA APIs |
| 4 | MRc3 + EQp2 skills | Low-emitting materials and air quality working | Backend | EC3 + EPA AirNow |
| 4 | EAp5 + EAc7 skills | Refrigerant management pair working | Backend | EPA SNAP + AHRI |
| 5 | Document template library | 8 templates render to PDF, pass visual QA | Backend | All MVP skills |
| 5 | Consultant dashboard v1 | React app with project list, credit board, HITL inbox | Frontend | Week 4 skills |
| 6 | Energy + water credits | EAc3 (10 pts), WEc2 (8 pts), EAp1, EAp2 | Backend | EnergyPlus integration |
| 6 | Embodied carbon credits | MRc2 (6 pts), MRp2, IPp3 | Backend | EC3 advanced queries |
| 7 | Site + transport credits | LTc3 (6 pts), SSc3 (3 pts), LTc1 (1 pt) | Backend | GTFS + Walk Score |
| 7 | Environmental credits | SSc5 (2 pts), SSc6 (1 pt) | Backend | SRI + IES databases |
| 8 | Regional filtering live | Skills automatically disabled for unsupported regions | Backend | All 16 skills |
| 8 | HITL dashboard v2 | Batch review, confidence indicators, SLA analytics | Frontend | Dashboard v1 |
| 9 | Load testing complete | All p99 targets met; auto-scaling rules active | DevOps | All features |
| 9 | Security audit clean | Zero critical findings; pen test report signed off | DevOps | Production candidate |
| 10 | USGBC Arc integration | Direct submission from platform to LEED Online | Backend | Security audit |
| 10 | Monitoring operational | All alerts configured; on-call rotation active | DevOps | Production deploy |
| 10 | Training delivery | Consultant training completed; documentation published | Product | All of above |
| 10 | **Production launch** | **Platform live for pilot customers** | **All** | **All milestones** |

Critical path: Week 1 (infra) → Week 2 (PRc2) → Week 3 (API layer) → Week 4 (6 more skills) → Week 5 (dashboard) → Week 9 (hardening) → Week 10 (production).

Slack (non-critical path) exists in Weeks 6–8 where additional skills are built in parallel and can be delayed by up to 1 week without impacting the production launch.

---

## Section 8: Risk Assessment & Quality Assurance

### 8.1 Technical Risks Table

| Risk | Probability | Impact | Mitigation | Owner | Monitoring |
|------|------------|--------|------------|-------|------------|
| **API rate limiting** | Medium | Medium | Exponential backoff with jitter; Redis caching with API-specific TTLs; fallback to local snapshots; circuit breaker pattern (PyCircuitBreaker) | Backend | API error rate dashboard; 429 response counter |
| **API deprecation or breaking change** | Low | High | Abstraction layer (`LEEDAPITool` base class) decouples skills from API specifics; multi-source fallback (e.g., EC3 + CLF Baselines for embodied carbon); automated contract tests run nightly against live APIs | Backend | Nightly API contract test in CI; deprecation notice scraping |
| **Energy model parsing errors** | Medium | High | Multi-format support: EnergyPlus `.eso`/`.csv`, eQUEST `.SIM`, IES `.csv`, OpenStudio `.sql`; schema validation before parsing; graceful degradation to manual upload prompt when format unrecognized; checksum validation on uploaded files | Backend | Parser success/failure rate by format |
| **HITL SLA breaches** | Medium | Medium | Configurable SLA per skill (default 24h, extendable to 72h for complex credits); auto-escalation to secondary reviewer after 50% of SLA elapsed; auto-approve with "expedited review" flag if SLA expires; SLA analytics to identify chronic bottlenecks | Product | Average review time per consultant; SLA breach rate |
| **Incorrect credit interpretation by LLM** | Low | High | RAG (Retrieval-Augmented Generation) over LEED v5 reference guide vector store; prompt engineering with explicit requirement quoting; confidence scoring per section; mandatory HITL review for any section with confidence < 85% | AI / Backend | Confidence score distribution; HITL rejection rate by skill |
| **Sandbox escape or code injection** | Low | Critical | Docker seccomp profiles; read-only root filesystem; no network egress except to allowlisted APIs; CPU/memory limits per container; gVisor or Firecracker for ultra-sensitive skills; automated container image scanning | DevOps | Container security scan results; sandbox crash logs |
| **Data loss or corruption** | Low | High | Automatic checkpointing every workflow step to PostgreSQL; S3 versioning on all generated documents; point-in-time recovery for RDS; daily automated backups to cross-region S3; document hash verification | DevOps | Backup success rate; RPO/RTO metrics |
| **USGBC Arc API changes** | Medium | High | Abstraction wrapper around Arc API; staging project for integration testing; manual submission fallback (download docs, upload via LEED Online UI); quarterly API compatibility audit | Backend | Arc API contract test; submission success rate |
| **Regional data incompleteness** | Medium | Medium | Regional skill filter gates unavailable skills; manual override workflow for exceptions; pre-project data availability assessment report; graceful degradation to conservative assumptions with explicit flagging | Backend | Disabled skill count by region |
| **LLM hallucination in calculations** | Low | High | All numeric calculations executed in Python (sandbox), not by LLM; LLM only generates narrative text and structures output; unit test every calculation path with known-good reference cases; cross-reference checking between related credits | Backend | Calculation unit test pass rate |

**Risk Heat Map Summary**

| | Low Impact | Medium Impact | High Impact |
|--|------------|---------------|-------------|
| **Low Probability** | — | — | API deprecation; LLM misinterpretation; sandbox escape; data loss |
| **Medium Probability** | — | API rate limiting; HITL SLA; regional data gaps | Energy model parsing |
| **High Probability** | — | — | — |

The highest-severity risks (low probability / high impact) receive the most defensive engineering: multiple fallback layers, abstraction, and extensive testing.

---

### 8.2 Quality Assurance Framework

The QA framework operates at four layers: code quality, skill correctness, document quality, and cross-credit consistency.

**Layer 1: Automated Code Testing**

| Test Type | Scope | Target Coverage | Tools |
|-----------|-------|-----------------|-------|
| Unit tests | Individual functions, API tools, calculation modules | 90%+ | pytest, pytest-asyncio, pytest-cov |
| Integration tests | Skill workflows with mocked external APIs | 100% of skills | pytest, responses (HTTP mocking) |
| E2E tests | Full workflow: input upload → skill execution → HITL → PDF | 100% of skills | Playwright (dashboard), custom API client |
| Contract tests | Live API schema validation (nightly) | 100% of APIs | schemathesis, custom probes |
| Regression tests | Full 16-skill suite on reference projects | Weekly | CI pipeline |

Every skill must pass the following test gates before merge:

1. **Input Validation Gate**: 50 synthetic input variations (valid, borderline, malformed, missing fields)
2. **Calculation Gate**: 10 known-good reference cases with published expected outputs
3. **API Resilience Gate**: Each API tool tested with timeout, 429, 500, and malformed response scenarios
4. **HITL Gate**: All three actions (approve, reject, request_changes) exercised
5. **Document Gate**: Generated document passes structural schema (sections present, tables complete)

**Layer 2: Validation Against LEED v5 Reference Guide**

The LEED v5 reference guide is chunked, embedded, and stored in a vector database (Pinecone/Weaviate). During skill development and testing:

| Activity | Method | Frequency |
|----------|--------|-----------|
| Requirement traceability | Each skill requirement mapped to reference guide section ID | Once per skill |
| Automated compliance check | RAG query validates that skill output addresses every requirement | Every test run |
| Cross-reference verification | Related credits checked for consistency (e.g., EAp1 carbon baseline must match IPp3 projection) | Every project build |
| Update regression | When LEED v5 updates, re-run all skills against new reference guide | On USGBC release |

**Layer 3: Confidence Scoring for AI-Generated Content**

Every AI-generated section of a document receives a confidence score:

```python
class ConfidenceScorer:
    """Assign confidence to AI-generated content sections."""
    
    def score(self, section: DocumentSection) -> float:
        factors = {
            "source_citation_density": len(section.citations) / len(section.sentences),
            "calculation_verification": section.has_calculated_values and section.calculation_checksum_valid,
            "reference_guide_alignment": self.rag_similarity(section.text, section.requirement_id),
            "historical_accuracy": self.historical_error_rate(section.skill_name, section.section_type),
            "input_completeness": section.input_completeness_score,
        }
        
        # Weighted average
        weights = {"source_citation_density": 0.25, "calculation_verification": 0.30,
                   "reference_guide_alignment": 0.25, "historical_accuracy": 0.10,
                   "input_completeness": 0.10}
        
        score = sum(factors[k] * weights[k] for k in factors)
        return round(score, 2)
```

| Confidence Range | Badge Color | HITL Requirement | Action |
|------------------|-------------|------------------|--------|
| 0.95 – 1.00 | Green | Optional | Auto-approve available |
| 0.85 – 0.94 | Yellow | Required (expedited) | Standard HITL workflow |
| 0.70 – 0.84 | Orange | Required (extended SLA) | Flagged for senior reviewer |
| < 0.70 | Red | Required (mandatory) | Blocked until manual review |

**Layer 4: Document Template Validation**

Each template undergoes:

1. **Schema validation**: Required placeholders present (`{{ project_id }}`, `{{ total_co2 }}`, etc.)
2. **Render validation**: Template renders without Jinja2 errors for 100 sample data sets
3. **Visual QA**: PDF output reviewed for formatting, pagination, table alignment
4. **LEED compliance**: Template structure matches USGBC submission format requirements
5. **Accessibility**: PDF passes WCAG 2.1 AA for tagged structure and alt text

---

### 8.3 Monitoring & Alerting

**API Health Dashboard**

| Metric | Collection Method | Granularity | Retention |
|--------|-------------------|-------------|-----------|
| Availability (up/down) | HTTP probe every 60s | Per endpoint | 90 days |
| Response time (p50, p95, p99) | Prometheus histogram | Per endpoint | 30 days |
| Error rate by status code | Application middleware | Per endpoint + code | 90 days |
| Rate limit proximity | Response header inspection | Per API key | 30 days |
| Cache hit rate | Redis INFO | Per API tool | 30 days |

Dashboard URL: `https://grafana.leed-platform.internal/d/api-health`

**Skill Execution Success Rates**

| Metric | Definition | Alert Threshold |
|--------|------------|-----------------|
| Success rate | `(completed / invoked) × 100` | < 95% for 10 min |
| Mean execution time | Average from invocation to completion | > 120s for 15 min |
| HITL bottleneck rate | `(blocked_at_hitl / invoked) × 100` | > 40% for 1 hour |
| Retry rate | `(retried / invoked) × 100` | > 10% for 10 min |
| Document generation failure | `(failed_docs / requested_docs) × 100` | > 2% for 5 min |

Per-skill breakdowns are available to identify which credits are most problematic.

**HITL Response Times**

| Metric | Target | Alert |
|--------|--------|-------|
| Median time to first response | < 4 hours | > 8 hours |
| Median time to approve/reject | < 12 hours | > 24 hours |
| SLA breach rate | < 5% | > 10% |
| Escalation rate | < 3% | > 8% |

**Document Generation Quality Scores**

An automated quality pipeline scores every generated document:

| Dimension | Weight | Scoring Method |
|-----------|--------|----------------|
| Completeness (all required sections present) | 25% | Schema validation against template checklist |
| Accuracy (calculations match inputs) | 30% | Re-calculation verification in sandbox |
| Citations (every claim has source) | 20% | Citation density + source validity check |
| Readability (Flesch-Kincaid grade) | 10% | NLP analysis; target < 14 for technical docs |
| Formatting (PDF structure, tags) | 15% | PDF/A validation + accessibility scan |

A composite quality score (0–100) is stored with each document. Documents scoring < 80 trigger an automatic quality review ticket.

**Error Rate Tracking**

Errors are classified by tier:

| Tier | Examples | Response | SLA |
|------|----------|----------|-----|
| T1 (Critical) | Sandbox escape, data corruption, auth breach | PagerDuty + immediate rollback | 15 min |
| T2 (High) | API down > 5 min, skill crash loop, document generation failure | Slack alert + auto-retry | 1 hour |
| T3 (Medium) | Single API timeout, cache miss storm, HITL SLA breach | Slack notification + ticket | 4 hours |
| T4 (Low) | Cosmetic PDF issue, minor formatting deviation | Weekly digest | 1 week |

All errors are captured with full context (stack trace, input hash, API response snapshot, workflow state) and stored in S3 for 1 year.

---

### 8.4 Compliance & Audit Trail

The platform maintains a comprehensive audit trail suitable for GBCI (Green Business Certification Inc.) review during LEED project audits.

**Calculation Versioning**

Every calculation is versioned and reproducible:

```python
class CalculationRecord:
    calculation_id: str           # UUID v4
    skill_name: str                 # e.g., "ea-c3-energy-efficiency"
    skill_version: str              # e.g., "1.2.3"
    formula_hash: str               # SHA-256 of formula source code
    inputs_hash: str                # SHA-256 of serialized inputs
    parameters: dict                # All constants, thresholds, emission factors
    api_sources: list               # [{"api": "epa_egrid", "version": "2023", "retrieved_at": "..."}]
    output: dict                    # Numerical results
    executed_at: datetime           # Timestamp
    sandbox_id: str                 # Container ID for reproduction
    
    def verify(self) -> bool:
        # Re-run calculation in fresh sandbox with same inputs
        # Compare output to stored output
        return rerun_output == self.output
```

| Requirement | Implementation |
|-------------|---------------|
| Calculation reproducibility | Every calculation can be re-executed in a fresh sandbox with identical inputs |
| Formula immutability | Skill code is Git-versioned; formula hash locks the exact code used |
| Parameter traceability | All constants (GWP values, emission factors, thresholds) stored with source and date |
| Input integrity | Input JSON is hashed at ingestion; any tampering detected |

**Source Data Citation**

Every document includes a "Data Sources and References" appendix:

| Citation Type | Format | Example |
|---------------|--------|---------|
| API data | `[API Name, Version, Retrieval Date, Query Parameters]` | EPA eGRID 2023, retrieved 2026-03-15, region: RFCW |
| Static database | `[Database Name, Version, Release Date]` | EC3 Database v2.4, March 2026 release |
| Emission factor | `[Source, Factor Value, Unit, Date]` | IPCC AR6 GWP-100, R-410A = 2088 kg CO2e/kg, 2021 |
| Code reference | `[Standard, Section, Year]` | ASHRAE 90.1-2019, Section 6.5.1 |
| Manufacturer data | `[Manufacturer, Product, Certification ID, Date]` | ABC Corp, Model X, AHRI Cert #12345, 2026 |

**Human Review Annotations**

All HITL interactions are preserved:

| Field | Stored Value |
|-------|--------------|
| Reviewer identity | GBCI credential number + platform user ID |
| Review timestamp | UTC with millisecond precision |
| Action taken | Approve / Reject / Request Changes |
| Checklist responses | JSON object with boolean per checklist item |
| Free-text comments | Full text with markdown formatting |
| Document version reviewed | Hash of document at time of review |
| Time spent reviewing | Client-side timer (honor system) |

Annotations are append-only and cryptographically signed with the platform's private key to prevent tampering.

**Full Audit Trail for GBCI Review**

For any LEED credit submitted through the platform, a complete audit package can be exported:

```
audit-package-{project_id}-{credit_code}-{timestamp}.zip
├── manifest.json              # Index of all files
├── calculation/
│   ├── calculation_record.json
│   ├── formula_source.py
│   ├── inputs.json
│   └── outputs.json
├── data_sources/
│   ├── api_responses/         # Raw API responses (redacted keys)
│   └── static_references/     # Database snapshots used
├── documents/
│   ├── generated_pdf.pdf
│   └── generation_template.html
├── hitl/
│   ├── review_record.json
│   ├── reviewer_credentials.pdf
│   └── comments.txt
├── workflow/
│   ├── state_graph.json       # Full LangGraph state history
│   └── execution_log.jsonl    # Step-by-step execution trace
└── signatures/
    ├── calculation_signature.json
    └── document_signature.json
```

The export is generated on-demand via API:

| Endpoint | Method | Auth | Rate Limit |
|----------|--------|------|------------|
| `/api/v1/audit/export` | POST | Project admin | 10 req/hour |

The audit trail satisfies the following compliance requirements:

| Requirement | Standard | Platform Evidence |
|-------------|----------|-------------------|
| Calculation transparency | LEED v5 Reference Guide | Versioned formulas, reproducible sandbox runs |
| Data provenance | ISO 9001 | API response caching with timestamps |
| Human oversight | GBCI Review Manual | HITL review records with credential verification |
| Document integrity | 21 CFR Part 11 (optional) | Cryptographic signatures on all outputs |
| Change tracking | AIA Best Practices | Git history of all skill and template changes |
