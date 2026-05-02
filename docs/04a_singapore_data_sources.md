# Singapore Data Sources & Regional Equivalents

## Overview

Singapore lacks many of the US-centric government APIs (FEMA, EPA, NOAA, USGS, Census) that form the backbone of the platform's US automation. However, Singapore has a mature open-data ecosystem through **data.gov.sg**, strong government agencies (NEA, BCA, PUB, LTA, EMA, NParks, SLA), and regional standards (SS, BCA Green Mark) that provide equivalent or substitute data for most LEED v5 credits.

Where no API exists, the platform provides structured **manual data entry workflows** with validation rules, reference links, and template checklists so consultants can source and input data efficiently.

---

## Singapore Government API Catalog

### Climate, Weather & Environmental Data

| API / Source | Provider | URL | Auth | Data Types | US Equivalent | Credits Supported | Complexity |
|---|---|---|---|---|---|---|---|
| **NEA Real-time Weather API** | National Environment Agency (via data.gov.sg) | `https://api.data.gov.sg/v1/environment/` | None (public) | Temperature, humidity, rainfall, wind speed/direction, UV index | NOAA Climate Data, NWS API | IPp1, SSc3, SSp1, SSc4 | Low |
| **NEA 2-Hour Weather Forecast** | NEA | `https://api.data.gov.sg/v1/environment/2-hour-weather-forecast` | None | Nowcast by planning area | NWS Forecast | IPp1 | Low |
| **NEA 24-Hour Weather Forecast** | NEA | `https://api.data.gov.sg/v1/environment/24-hour-weather-forecast` | None | Daily forecast | NWS Extended | IPp1 | Low |
| **NEA Rainfall API** | NEA | `https://api.data.gov.sg/v1/environment/rainfall` | None | Real-time rainfall across 50+ stations (mm) | NOAA Precipitation Frequency | SSc3 | Low |
| **MSS Historical Climate Data** | Meteorological Service Singapore | `https://www.weather.gov.sg/climate-historical-daily/` | None (download) | Historical daily records: temp, rain, wind, humidity, sunshine | NOAA Climate Normals | IPp1, SSc3, EAc4 | Low |
| **MSS Climate Normals (1991-2020)** | MSS | `https://www.weather.gov.sg/climate-climate-of-singapore/` | None (static) | 30-year monthly averages for all climate variables | NOAA Climate Normals | IPp1, SSc3, SSp1 | Low |
| **NEA PSI / Air Quality API** | NEA | `https://api.data.gov.sg/v1/environment/psi` | None | PSI, PM2.5, PM10, O3, CO, SO2, NO2 by region | EPA AirNow AQI | EQp2, EQp1 | Low |
| **NEA PM2.5 API** | NEA | `https://api.data.gov.sg/v1/environment/pm25` | None | Hourly PM2.5 readings by region | EPA AirNow | EQp2, EQc5 | Low |
| **NEA UV Index API** | NEA | `https://api.data.gov.sg/v1/environment/uv-index` | None | Hourly UV index | EPA UV Index | SSc4 | Low |

### Geospatial, Land Use & Demographics

| API / Source | Provider | URL | Auth | Data Types | US Equivalent | Credits Supported | Complexity |
|---|---|---|---|---|---|---|---|
| **OneMap API** | Singapore Land Authority (SLA) | `https://www.onemap.gov.sg/api/` | API Token (free) | Geocoding, reverse geocoding, routing, coordinate conversion, planning areas, 100+ thematic layers | USGS National Map, Google Maps, Census geo | LTc1, LTc3, SSp1, Multiple | Medium |
| **OneMap Population Query** | SLA / Dept of Statistics | `https://www.onemap.gov.sg/api/public/popquery/` | API Token | Population demographics by planning area (age, income, education, employment, housing) | US Census API | IPp2, LTc2, LTc3 | Medium |
| **OneMap Planning Area API** | SLA | `https://www.onemap.gov.sg/api/public/planningarea/` | API Token | 55 planning area boundaries and coordinates | Census Block Groups | LTc3 | Low |
| **OneMap Themes API** | SLA | `https://www.onemap.gov.sg/api/public/themesvc/` | API Token | 100+ thematic layers: parks, heritage, schools, hospitals, community, etc. | USGS, Census TIGER | Multiple LT/SS | Medium |
| **URA Master Plan Zoning** | Urban Redevelopment Authority | `https://www.ura.gov.sg/maps/api/` | Registration | Zoning, land use, plot ratio, building height, conservation areas | Local zoning maps | LTc2, LTc3, SSp1 | Medium |
| **URA Space Usage / Property Data** | URA | `https://www.ura.gov.sg/reis/datashare` | Registration | Property transactions, rental, occupancy, private residential | Census housing data | LTc3 | Medium |
| **SingStat API** | Dept of Statistics | `https://tablebuilder.singstat.gov.sg/api/` | None (public) | Population, household, income, employment, economic indicators | US Census ACS | IPp2, LTc2, LTc3 | Medium |
| **data.gov.sg Datasets** | GovTech | `https://data.gov.sg/` | None | 5000+ datasets across 65+ agencies | data.gov | Multiple | Low-Medium |

### Flood, Hazard & Environmental Protection

| API / Source | Provider | URL | Auth | Data Types | US Equivalent | Credits Supported | Complexity |
|---|---|---|---|---|---|---|---|
| **PUB Flood Risk Map** | PUB (National Water Agency) | `https://www.pub.gov.sg/drainage/floodmanagement` | None (interactive map, no public API) | Flood-prone areas, drainage infrastructure | FEMA NFHL | LTc1 | Manual |
| **NEA Flood Sensors API** | NEA (via data.gov.sg) | `https://api.data.gov.sg/v1/environment/` | None | Water level sensors at drains and canals | USGS water level gauges | LTc1 | Low |
| **NParks Nature Areas / Biodiversity** | National Parks Board | `https://www.nparks.gov.sg/biodiversity` | None (download / GIS layers) | Nature reserves, nature areas, heritage trees, flora/fauna | USFWS Critical Habitat | LTc1 | Manual |
| **NParks Trees.sg** | NParks | `https://www.nparks.gov.sg/treessg` | None (map interface) | Individual tree records, species, location, heritage status | USDA PLANTS | SSc2, SSc4 | Manual |
| **BCA Contaminated Land Register** | BCA / NEA | Government records (no public API) | FOI request | Contaminated sites, remediation status | EPA Brownfields | LTc2 | Manual |
| **PUB Drainage & Sewerage Data** | PUB | `https://www.pub.gov.sg/drainage` | None (reference) | Drainage standards, design rainfall, ABC Waters guidelines | NRCS + NOAA Atlas 14 | SSc3 | Manual |

### Transit & Transportation

| API / Source | Provider | URL | Auth | Data Types | US Equivalent | Credits Supported | Complexity |
|---|---|---|---|---|---|---|---|
| **LTA DataMall API** | Land Transport Authority | `https://datamall.lta.gov.sg/content/datamall/en/dynamic-data.html` | Account Key (free) | Bus arrival, bus routes/stops, taxi availability, traffic, carpark, train disruptions, EV charging points, geospatial transport data | GTFS, Walk Score | LTc3, LTc4, LTc5 | Low |
| **LTA Bus Routes & Stops** | LTA | DataMall dynamic API | Account Key | Complete bus service routes, stop locations, first/last bus | GTFS Static | LTc3 | Low |
| **LTA Train Station Data** | LTA | DataMall static datasets | Account Key | MRT/LRT station locations, ridership, network map | GTFS | LTc3, LTc4 | Low |
| **LTA EV Charging Points** | LTA | DataMall static datasets | Account Key | EV charging station locations, types, availability | ENERGY STAR EVSE | LTc5 | Low |
| **LTA Taxi Availability** | LTA | DataMall dynamic API | Account Key | Real-time taxi locations | — | LTc4 | Low |
| **OneMap Routing API** | SLA | `https://www.onemap.gov.sg/api/public/routingsvc/` | API Token | Public transport, driving, walking, cycling routes with time/distance | Google Maps Distance Matrix | LTc3, LTc4 | Low |
| **GTFS Singapore** | LTA (published) | Via DataMall | Account Key | Standard GTFS feed for Singapore public transport | GTFS US agencies | LTc3, LTc4 | Low |

### Energy, Grid & Renewables

| API / Source | Provider | URL | Auth | Data Types | US Equivalent | Credits Supported | Complexity |
|---|---|---|---|---|---|---|---|
| **EMA Singapore Energy Statistics** | Energy Market Authority | `https://www.ema.gov.sg/resources/singapore-energy-statistics` | None (download) | Electricity generation by fuel, consumption by sector, grid emission factor, energy intensity | EPA eGRID | IPp3, EAp1, EAc4 | Manual |
| **EMA Half-Hourly System Demand** | EMA | `https://www.emcsg.com/MarketData/` | None (download) | Real-time electricity demand, generation mix, wholesale prices | EIA data | EAc6 | Medium |
| **SP Group Utilities API** | SP Group | `https://www.spgroup.com.sg/` | Account login | Electricity & gas consumption data, billing | Green Button API | EAp4, EAc5 | Medium |
| **SERIS Solar Data** | Solar Energy Research Institute of Singapore | `https://www.seris.nus.edu.sg/` | Research access | Solar irradiance, PV performance data for Singapore | NREL PVWatts, NSRDB | EAc4 | Medium |
| **PVGIS (EU JRC)** | European Commission JRC | `https://re.jrc.ec.europa.eu/pvg_tools/` | None | Solar PV production estimates (covers Singapore) | NREL PVWatts | EAc4 | Low |
| **NEA Energy Efficiency Standards** | NEA | `https://www.nea.gov.sg/our-services/climate-change-energy-efficiency` | None (reference) | MELS (Minimum Energy Labelling Scheme), energy efficiency standards | ENERGY STAR | WEp2 | Manual |
| **Singapore Grid Emission Factor** | EMA / NEA | Published annually by NEA/NCCS | None (static) | Grid emission factor (kg CO2/kWh) — approx 0.4085 kg CO2/kWh (2023) | EPA eGRID subregion | IPp3, EAp1 | Low |

### Water

| API / Source | Provider | URL | Auth | Data Types | US Equivalent | Credits Supported | Complexity |
|---|---|---|---|---|---|---|---|
| **PUB Water Conservation Data** | PUB | `https://www.pub.gov.sg/savewater` | None (reference) | Water conservation requirements, mandatory WELS ratings, per-capita consumption targets | EPA WaterSense | WEp1, WEp2, WEc1 | Manual |
| **PUB WELS (Water Efficiency Labelling)** | PUB | `https://www.pub.gov.sg/wels` | None (product search) | Water efficiency ratings for fixtures (taps, showers, dual-flush, urinals, washing machines) | EPA WaterSense Product DB | WEp2, WEc1 | Low |
| **PUB ABC Waters Design Guidelines** | PUB | `https://www.pub.gov.sg/abcwaters` | None (reference) | Stormwater management, bioretention, rain gardens, design rainfall | NOAA Atlas 14 + NRCS | SSc3 | Manual |
| **PUB Design Rainfall Data** | PUB | Published in Code of Practice | None (static) | IDF curves, design storms for Singapore | NOAA Precipitation Frequency | SSc3 | Low |

### Materials, Products & Certifications

| API / Source | Provider | URL | Auth | Data Types | US Equivalent | Credits Supported | Complexity |
|---|---|---|---|---|---|---|---|
| **EC3 Database** | Building Transparency | `https://buildingtransparency.org/ec3/` | API Key | Embodied carbon data (global coverage including SG) | Same (EC3) | IPp3, MRp2, MRc2 | Medium |
| **One Click LCA** | One Click LCA Ltd | `https://www.oneclicklca.com/` | License | LCA with Singapore-specific datasets | Same (One Click LCA) | MRp2, MRc2 | Medium |
| **EPD International Registry** | EPD International | `https://www.environdec.com/` | API on request | Environmental Product Declarations (global) | Same (EPD Registry) | MRc4 | Low |
| **SGBC Certified Products** | Singapore Green Building Council | `https://www.sgbc.sg/sgbc-certified-products` | None (search) | Green-certified building products in Singapore (SGLS, Green Label) | GREENGUARD, Green-e | MRc3, MRc4 | Manual |
| **Singapore Green Label Scheme** | Singapore Environment Council | `https://www.sgls.sec.org.sg/` | None (search) | Eco-label for products meeting environmental standards | GREENGUARD, Green-e | MRc3, MRc4 | Low |
| **BCA Green Mark Products** | BCA | `https://www1.bca.gov.sg/buildsg/sustainability` | None (search) | Green Mark certified products and buildings | ENERGY STAR, LEED | Multiple | Manual |
| **SGBC Product Directory** | SGBC | `https://www.sgbc.sg/` | None | Singapore-certified green building products & materials | UL GREENGUARD / FloorScore | MRc3, MRc4 | Manual |

### Building Standards & Codes

| Source | Provider | Data Types | US Equivalent | Credits Supported |
|---|---|---|---|---|
| **SS 553:2016 (Air-conditioning)** | Enterprise Singapore | Air-con design, energy efficiency, ventilation | ASHRAE 90.1 | EAp2, EAc2 |
| **SS 554:2016 (Indoor Air Quality)** | Enterprise Singapore | Ventilation rates, IAQ parameters | ASHRAE 62.1 | EQp1, EQc1 |
| **SS 530:2014 (Lighting)** | Enterprise Singapore | Lighting power density by space type | ASHRAE 90.1 (lighting) | EQc6, SSc5, SSc6 |
| **BCA Green Mark 2021** | BCA | Energy, water, materials, IAQ, sustainability benchmarks | LEED reference guide | Multiple |
| **SS 531:2006 (Thermal Comfort)** | Enterprise Singapore | Thermal comfort parameters for tropical climate | ASHRAE 55 | EQc2 |
| **SCDF Fire Code** | Singapore Civil Defence Force | Fire safety, egress, materials | IBC / NFPA | SSp1 |
| **BCA Code on Accessibility** | BCA | Universal design requirements | ADA standards | IPc1 |
| **AHRI Directory** | AHRI | Refrigerant equipment data (global) | Same (AHRI) | EAp5, EAc7 |
| **EPA SNAP (Refrigerants)** | EPA | Approved refrigerants & GWP values (applicable globally) | Same (EPA SNAP) | EAp5, EAc7 |

---

## Credit-by-Credit: Singapore Source Mapping

### IP — Integrative Process

| Credit | US Source | Singapore Equivalent | Availability | Notes |
|---|---|---|---|---|
| **IPp1** Climate Resilience | NOAA, NWS, FEMA NFHL | NEA Weather API + MSS Climate Data + PUB Flood Map | **Limited** | No flood zone API — use PUB interactive maps + manual input |
| **IPp2** Human Impact | Census, EPA EJScreen | SingStat + OneMap Population Query | **Limited** | No EJ screening equivalent. Use SingStat demographics + manual community assessment |
| **IPp3** Carbon Assessment | EPA eGRID, EC3 | EMA Grid EF (static) + EC3 (global) | **Full** | Singapore grid EF published annually. EC3 works globally |
| **IPc1** Integrative Design | NREL energy targets | BCA energy benchmarks + SS 553 | **Limited** | No API — use BCA published benchmarks + manual input |

### LT — Location & Transportation

| Credit | US Source | Singapore Equivalent | Availability | Notes |
|---|---|---|---|---|
| **LTc1** Sensitive Land | FEMA NFHL, USFWS, USGS 3DEP, NWI | PUB Flood Map, NParks Nature Areas, OneMap | **Limited** | No flood zone API. NParks provides nature reserve boundaries as GIS layers. Manual upload required |
| **LTc2** Priority Considerations | EPA Brownfields, Census | NEA contaminated sites + SingStat + OneMap | **Manual** | No contaminated land public API. Consultant must source from NEA records |
| **LTc3** Compact Development | Walk Score, Census, GTFS | LTA DataMall + OneMap Routing + SingStat Population | **Full** | Singapore has excellent transit data. Calculate transit score from LTA bus/MRT frequency data |
| **LTc4** Low-Carbon Transport | GTFS, Walk Score | LTA DataMall (bus arrivals, routes, EV points) + OneMap Routing | **Full** | Real-time bus/MRT data available |
| **LTc5** EV Infrastructure | ENERGY STAR EVSE | LTA EV Charging Points dataset | **Full** | LTA publishes EV charging point data |

### SS — Sustainable Sites

| Credit | US Source | Singapore Equivalent | Availability | Notes |
|---|---|---|---|---|
| **SSp1** Site Assessment | USGS National Map, NRCS Soil | OneMap + NParks + PUB drainage data | **Limited** | No soil survey API. Use NParks ecological data + consultant site assessment |
| **SSc2** Habitat Conservation | USFWS, USDA PLANTS | NParks biodiversity data, Trees.sg | **Limited** | NParks maintains species lists. No API — use published datasets + manual input |
| **SSc3** Rainwater Management | NOAA Atlas 14, NRCS Soil | PUB Design Rainfall + ABC Waters Guidelines | **Limited** | PUB publishes IDF curves in Code of Practice. No API — static data + manual input |
| **SSc4** Heat Resilience | NOAA Climate, Tree Equity Score | NEA Weather API + NParks tree canopy data | **Limited** | Real-time weather available. Tree canopy data via Trees.sg (no API) |
| **SSc5** Heat Island Reduction | CRRC | SGBC certified products + manufacturer data | **Manual** | No Singapore equivalent of CRRC. Source SRI from manufacturer specs + SGBC directory |
| **SSc6** Light Pollution | IES TM-15-11 (static) | Same IES standard applies globally | **Full** | Static standard — same for all regions |
| **SSc7** Site Outdoor Lighting | IES RP-8 (static) | SS 530:2014 + IES standards | **Full** | Use Singapore Standard + IES |

### WE — Water Efficiency

| Credit | US Source | Singapore Equivalent | Availability | Notes |
|---|---|---|---|---|
| **WEp1** Water Use Reduction | Smart water meters | SP Group utility data | **Limited** | SP Group provides consumption data via portal. No standardized API |
| **WEp2** Minimum Water Efficiency | ENERGY STAR, WaterSense | PUB WELS (Water Efficiency Labelling) | **Full** | WELS is mandatory in Singapore. Product database searchable online |
| **WEc1** Water Use Reduction | WaterSense, SWMM | PUB WELS + PUB water conservation data | **Limited** | WELS for fixtures. Stormwater via PUB Code of Practice |

### EA — Energy & Atmosphere

| Credit | US Source | Singapore Equivalent | Availability | Notes |
|---|---|---|---|---|
| **EAp1** Operational Carbon | EPA eGRID, PVWatts | EMA Grid EF + PVGIS/SERIS solar data | **Full** | Grid EF published annually. PVGIS covers Singapore for solar estimates |
| **EAp2** Min Energy Performance | EnergyPlus/Eppy, ASHRAE 90.1 | EnergyPlus (global) + SS 553 + BCA energy code | **Full** | EnergyPlus works globally with Singapore weather files |
| **EAp5** Refrigerant Mgmt | EPA SNAP, AHRI | EPA SNAP (global) + AHRI (global) + NEA F-gas regulations | **Full** | Montreal Protocol applies globally. AHRI directory is international |
| **EAc4** Renewable Energy | NREL PVWatts, Green-e, NSRDB | PVGIS + SERIS + EMA renewable data + Singapore RECs | **Limited** | PVGIS provides good estimates. Singapore REC market is newer — verify through SP Group / renewable retailers |
| **EAc7** Enhanced Refrigerant | EPA SNAP, AHRI, IPCC GWP | Same global sources | **Full** | Refrigerant data is international |

### MR — Materials & Resources

| Credit | US Source | Singapore Equivalent | Availability | Notes |
|---|---|---|---|---|
| **MRp2** Embodied Carbon | EC3, Tally | EC3 (global) + One Click LCA (SG database) | **Full** | Both tools have Singapore/APAC coverage |
| **MRc2** Reduce Embodied Carbon | EC3, Tally, One Click LCA | Same global tools | **Full** | EC3 and One Click LCA cover SG |
| **MRc3** Low-Emitting Materials | GREENGUARD, FloorScore | SGBC Certified Products + Singapore Green Label | **Limited** | GREENGUARD is global. SGLS is Singapore-specific equivalent |
| **MRc4** Product Procurement | EPD, HPD, FSC | EPD International (global) + SGBC Directory | **Limited** | EPD Registry is global. SGBC for local certified products |

### EQ — Indoor Environmental Quality

| Credit | US Source | Singapore Equivalent | Availability | Notes |
|---|---|---|---|---|
| **EQp1** Minimum IAQ | AirNow, ASHRAE 62.1 | NEA PSI API + SS 554 | **Full** | NEA provides real-time air quality. SS 554 is Singapore's ventilation standard |
| **EQp2** Environmental Tobacco Smoke | AirNow | NEA PSI API + Singapore smoking regulations | **Full** | Singapore has strict anti-smoking laws |
| **EQc2** Thermal Comfort | ASHRAE 55, CBE | SS 531 + CBE Thermal Comfort Tool (global) | **Full** | CBE tool works globally. SS 531 for tropical comfort |
| **EQc3** Daylight | Radiance/DIVA, IES LM-83 | Same simulation tools (global) | **Full** | Daylight simulation is software-based |
| **EQc5** IAQ Assessment | IAQ sensor APIs | Same sensor APIs (Awair, Kaiterra available in SG) | **Full** | Global IAQ sensor vendors available |

### PR — Project Priorities

| Credit | US Source | Singapore Equivalent | Availability | Notes |
|---|---|---|---|---|
| **PRc2** LEED AP | GBCI Credential Directory | Same (GBCI is global) | **Full** | GBCI directory covers global credentials |

---

## Singapore Regional Availability Summary

| Category | Status | % API Coverage | % Manual Input | Notes |
|---|---|---|---|---|
| **Climate / Weather** | Full | 90% | 10% | NEA + MSS APIs are excellent |
| **Air Quality** | Full | 95% | 5% | NEA PSI/PM2.5 APIs are comprehensive |
| **Demographics** | Limited | 60% | 40% | SingStat + OneMap good but no EJ screening |
| **Transit / Transport** | Full | 95% | 5% | LTA DataMall is world-class |
| **Flood / Hazard** | Manual | 10% | 90% | PUB has maps but no public API |
| **Soil / Ecology** | Manual | 5% | 95% | No soil survey API. NParks data is downloadable GIS |
| **Grid Emissions** | Full | 80% | 20% | EMA publishes annually. Static but reliable |
| **Solar / Renewables** | Limited | 60% | 40% | PVGIS works. Local SERIS data is research-only |
| **Water Fixtures** | Full | 70% | 30% | PUB WELS database is searchable |
| **Materials / EPD** | Full | 80% | 20% | EC3, One Click LCA, EPD International are global |
| **Product Certs** | Limited | 40% | 60% | SGBC directory is web-only, not API |
| **Building Codes** | Manual | 0% | 100% | SS standards are purchased documents, not APIs |
| **Refrigerants** | Full | 90% | 10% | AHRI, EPA SNAP are global |
| **GIS / Mapping** | Full | 90% | 10% | OneMap API is comprehensive |

**Overall Singapore Automation Level: ~65% API-assisted, ~35% manual input required**

Compared to US (~95% API / ~5% manual), Singapore requires more consultant-driven data entry but still achieves strong automation for transit, weather, air quality, materials, and energy categories.

---

## Data Freshness & Update Schedule (Singapore)

| Dataset | Frequency | Source | Storage |
|---|---|---|---|
| NEA Weather/Air Quality | Real-time (1-5 min) | data.gov.sg APIs | Redis cache |
| MSS Climate Normals | Decadal (static) | MSS website | PostgreSQL |
| SingStat Demographics | Annual | SingStat TableBuilder | PostgreSQL |
| EMA Grid Emission Factor | Annual | NEA/NCCS publication | PostgreSQL |
| PUB WELS Products | Quarterly | PUB website | PostgreSQL |
| LTA Transit Data | Real-time | DataMall API | Redis + PostgreSQL |
| LTA EV Charging Points | Monthly | DataMall static | PostgreSQL |
| SGBC Certified Products | Quarterly | SGBC website | PostgreSQL |
| EC3 / EPD Data | Per-query / Quarterly | EC3 API / EPD Registry | PostgreSQL |
| PUB Design Rainfall | Static (updated per code revision) | Code of Practice | PostgreSQL |
| NParks Biodiversity | Annual | GIS layer downloads | PostGIS |
