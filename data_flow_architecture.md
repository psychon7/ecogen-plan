
# LEED v5 Automation - Data Flow Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Dashboard  │  │   Reports   │  │   BIM View  │  │  Analytics  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            API GATEWAY LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Kong / AWS API Gateway - Authentication, Rate Limiting, Routing    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MICROSERVICES LAYER                                  │
│                                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ Site Analysis│ │Energy/Carbon │ │   Materials  │ │    Water     │        │
│  │   Service    │ │   Service    │ │   Service    │ │   Service    │        │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ Indoor Env   │ │ Documentation│ │   Project    │ │  Compliance  │        │
│  │   Service    │ │   Service    │ │   Service    │ │   Service    │        │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DATA NORMALIZATION LAYER                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Schema Mapping │ Unit Conversion │ Coordinate Transform │ Temporal │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL API LAYER                                    │
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  GOVERNMENT     │  │    INDUSTRY     │  │   SOFTWARE      │             │
│  │    APIs         │  │     APIs        │  │   Platforms     │             │
│  │ • NOAA          │  │ • USGBC Arc     │  │ • Autodesk Forge│             │
│  │ • EPA           │  │ • EC3           │  │ • EnergyPlus    │             │
│  │ • Census        │  │ • ENERGY STAR   │  │ • GIS Platforms │             │
│  │ • FEMA          │  │ • Walk Score    │  │ • Revit API     │             │
│  │ • USGS          │  │ • Green-e       │  │ • Procore       │             │
│  │ • NREL          │  │ • HPD           │  │ • BMS/BAS       │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA STORAGE LAYER                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ PostgreSQL  │  │ TimescaleDB │  │    Redis    │  │   S3/Blob   │        │
│  │  (Project)  │  │  (Metrics)  │  │   (Cache)   │  │  (Documents)│        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Credit-Specific Data Flows

### IPp1 - Climate Resilience Assessment

```
Project Coordinates (Lat/Long)
         │
         ▼
┌─────────────────┐
│  Geocoding API  │ ──► Location validation
└─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    PARALLEL API CALLS                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │   NOAA   │ │   FEMA   │ │   USGS   │ │  IPCC    │       │
│  │ Climate  │ │  Flood   │ │ Hazards  │ │ Scenarios│       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ Data Aggregator │ ──► Normalize formats, units, time periods
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  Risk Scoring   │ ──► Calculate risk ratings by hazard type
│    Engine       │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Report Generator│ ──► Climate resilience assessment report
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  USGBC Arc API  │ ──► Submit documentation
└─────────────────┘
```

**APIs Required:** NOAA, FEMA, USGS, IPCC data portal
**Frequency:** Batch - per project during pre-design
**Data Volume:** ~10-50 MB per project (includes GIS data)

---

### IPp3 - Carbon Assessment

```
┌─────────────────────────────────────────────────────────────┐
│                      INPUT SOURCES                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Energy Model │  │ BIM + Tally  │  │ Refrigerant  │      │
│  │   Output     │  │   (EC3)      │  │   Schedule   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA EXTRACTION                           │
│  • EUI by fuel type        • Material quantities            │
│  • Annual energy use       • Embodied carbon by material    │
│  • Peak demands            • Construction emissions         │
│  • Operating schedule      • Refrigerant charges            │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ EPA eGRID API   │ ──► Grid emission factors by region
└─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              25-YEAR CARBON PROJECTION                       │
│                                                              │
│  Year 1-5:   Current grid mix + Building performance        │
│  Year 6-15:  Grid decarbonization trajectory                │
│  Year 16-25: Projected low-carbon grid                      │
│                                                              │
│  Components:                                                 │
│  • Operational carbon (energy × emission factor)            │
│  • Embodied carbon (materials + construction)               │
│  • Refrigerant emissions (leakage × GWP)                    │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│            DECARBONIZATION PATHWAY ANALYSIS                  │
│                                                              │
│  Path 1: Electrification                                     │
│    • Heat pump conversion analysis                          │
│    • Electrical capacity assessment                         │
│    • Cost-benefit analysis                                  │
│                                                              │
│  Path 2: Fuel switching + efficiency                        │
│    • Low-carbon fuel options                                │
│    • Efficiency improvements                                │
│    • Phased implementation timeline                         │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ Report Generator│
└─────────────────┘
```

**APIs Required:** EPA eGRID, EC3/Tally, IPCC emission factors
**Frequency:** Batch - updated with design iterations
**Data Volume:** ~5-20 MB per analysis

---

### MRp2 - Quantify and Assess Embodied Carbon

```
┌─────────────────┐
│   BIM Model     │ ──► Revit / IFC format
│  (Autodesk)     │
└─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              AUTOMATED QUANTITY TAKE-OFF                     │
│  │                                                           │
│  ├──► Structural elements (concrete, steel, wood)           │
│  ├──► Enclosure (walls, roofing, glazing)                   │
│  ├──► Hardscape (paving, site elements)                     │
│  └──► Interior elements (finishes, fixtures)                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    MATERIAL MAPPING                          │
│                                                              │
│  BIM Material          ──►    EC3 Category                   │
│  ─────────────────────────────────────────                   │
│  "Concrete 4000 psi"   ──►    "Concrete - Cast-in-Place"    │
│  "Structural Steel A992" ──►  "Steel - Structural"           │
│  "Aluminum Curtainwall" ──►   "Aluminum - Extruded"          │
│                                                              │
│  Mapping confidence score: 0.0 - 1.0                        │
│  Manual review required for < 0.8 confidence                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│   EC3 API Call  │ ──► POST material quantities
│                 │ ◄─── Receive GWP values
└─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    CARBON CALCULATION                        │
│                                                              │
│  Material A: 500 m³ concrete × 350 kg CO2e/m³ = 175 tCO2e   │
│  Material B: 100 tons steel × 1200 kg CO2e/ton = 120 tCO2e  │
│  Material C: ...                                            │
│                                                              │
│  TOTAL EMBODIED CARBON: 1,250 tCO2e                         │
│  Carbon Intensity: 450 kg CO2e/m²                           │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  HOT SPOT       │ ──► Identify top 3 carbon sources
│  IDENTIFICATION │
└─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              REDUCTION STRATEGY RECOMMENDATIONS              │
│                                                              │
│  Hot Spot 1: Concrete (40% of total)                        │
│    • Strategy: Specify high SCM content (30-50% slag)       │
│    • Potential reduction: 25-40%                            │
│    • Cost impact: Minimal                                   │
│                                                              │
│  Hot Spot 2: Steel (25% of total)                           │
│    • Strategy: Specify EAF steel with high recycled content │
│    • Potential reduction: 30-50%                            │
│    • Cost impact: Moderate                                  │
└─────────────────────────────────────────────────────────────┘
```

**APIs Required:** EC3 API, Autodesk Forge/Revit API
**Frequency:** Batch - per design iteration
**Data Volume:** ~2-10 MB per analysis

---

### EAc4 - Renewable Energy

```
┌─────────────────────────────────────────────────────────────┐
│                      INPUT DATA                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Building     │  │ Roof Area    │  │ Local Solar  │      │
│  │ Energy Use   │  │ & Orientation│  │   Resource   │      │
│  │ (kWh/year)   │  │   (m², °)    │  │  (kWh/m²/day)│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ NREL PVWatts API│  │ Shading Analysis│  │ Utility Rate    │
│                 │  │ (Site context)  │  │ API             │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│              SOLAR PRODUCTION ESTIMATION                     │
│                                                              │
│  System Size:        250 kW DC                              │
│  Annual Production:  375,000 kWh/year                       │
│  Capacity Factor:    17.1%                                  │
│  Specific Yield:     1,500 kWh/kW/year                      │
│                                                              │
│  Monthly Production Profile:                                │
│  Jan: 28,500  Feb: 32,000  Mar: 38,000  Apr: 36,500        │
│  May: 35,000  Jun: 33,500  Jul: 34,000  Aug: 35,500        │
│  Sep: 33,000  Oct: 30,500  Nov: 26,000  Dec: 25,500        │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              ENERGY OFFSET CALCULATION                       │
│                                                              │
│  Building Energy Use:        500,000 kWh/year               │
│  Solar Production:           375,000 kWh/year               │
│  ─────────────────────────────────────────────              │
│  On-site Offset:             75%                            │
│  Points Achievable:          EAc4 Tier 1, 4 points          │
│                                                              │
│  Remaining 25% offset options:                              │
│  • Off-site renewables (Green-e certified)                  │
│  • Community solar subscription                             │
│  • Virtual PPA                                              │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ Green-e Registry│ ──► REC verification for off-site
└─────────────────┘
```

**APIs Required:** NREL PVWatts, Green-e Registry, utility rate APIs
**Frequency:** Batch - per renewable energy analysis
**Data Volume:** ~1-5 MB per analysis

---

### EQc2 - Occupant Experience (Daylight Analysis)

```
┌─────────────────┐
│   BIM Model     │ ──► Geometry, materials, glazing
│  (gbXML export) │
└─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│              DAYLIGHT SIMULATION ENGINE                      │
│  (Radiance / DIVA / Ladybug Tools / IES VE)                 │
│                                                              │
│  Input Parameters:                                          │
│  • Weather file (TMY3) - from NOAA                          │
│  • Material reflectances                                    │
│  • Glazing VLT and SHGC                                     │
│  • Shading devices                                          │
│  • Interior furniture layout                                │
│                                                              │
│  Simulation Types:                                          │
│  • sDA (spatial Daylight Autonomy)                          │
│  • ASE (Annual Sunlight Exposure)                           │
│  • Daylight Glare Probability                               │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RESULTS PROCESSING                        │
│                                                              │
│  sDA Analysis:                                              │
│  • 55% of regularly occupied spaces achieve 300 lux for     │
│    50% of occupied hours                                    │
│  • COMPLIANT - 2 points                                     │
│                                                              │
│  ASE Analysis:                                              │
│  • 8% of space exceeds 1000 lux for 250+ hours              │
│  • COMPLIANT (< 10% threshold)                              │
│                                                              │
│  Combined Points: 2 points for sDA + ASE compliance         │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ Report Generator│ ──► Daylight analysis report with visualizations
└─────────────────┘
```

**APIs Required:** NOAA weather data, simulation software APIs
**Frequency:** Batch - per design iteration
**Data Volume:** ~50-200 MB (simulation results)

---

## Integration Patterns

### Pattern 1: Request-Response (Synchronous)
**Use Case:** Simple data lookups, compliance checking
**Example:** Light fixture BUG rating verification
**Flow:**
```
Client ──Request──► API Gateway ──► External API
   ▲                                          │
   └────────────Response─────────────────────┘
```

### Pattern 2: Event-Driven (Asynchronous)
**Use Case:** Design iteration triggers, real-time monitoring
**Example:** BIM model update triggers recalculation
**Flow:**
```
BIM Update ──Event──► Message Queue ──► Processor Service
                                           │
                                           ▼
                                    Recalculate Credits
                                           │
                                           ▼
                                    Update Dashboard
```

### Pattern 3: Batch Processing
**Use Case:** Periodic reporting, historical analysis
**Example:** Monthly energy performance report
**Flow:**
```
Scheduled Job ──► Data Collection ──► Aggregation ──► Report Generation
```

### Pattern 4: Stream Processing
**Use Case:** Real-time monitoring, IoT sensor data
**Example:** Continuous IAQ monitoring
**Flow:**
```
IoT Sensors ──Stream──► Kafka ──► Stream Processor ──► Real-time Dashboard
                              ──► Anomaly Detection ──► Alerts
```

---

## Data Volume Estimates

| Credit Category | Per-Project Data | Frequency | Annual Storage (100 projects) |
|----------------|------------------|-----------|------------------------------|
| IP (Integrative) | 50 MB | Once | 5 GB |
| LT (Location) | 100 MB | Once | 10 GB |
| SS (Sites) | 200 MB | Per iteration | 50 GB |
| WE (Water) | 50 MB | Per iteration | 15 GB |
| EA (Energy) | 500 MB | Per iteration | 100 GB |
| MR (Materials) | 100 MB | Per iteration | 30 GB |
| EQ (Indoor) | 300 MB | Per iteration | 60 GB |
| PR (Priorities) | 20 MB | Once | 2 GB |
| **TOTAL** | **~1.3 GB** | - | **~270 GB** |

---

## Security Considerations

### Data Classification

| Sensitivity | Data Types | Protection |
|------------|-----------|------------|
| **High** | Project location, client information, proprietary designs | Encryption at rest, access controls, audit logging |
| **Medium** | Energy performance, material specifications | HTTPS, API authentication |
| **Low** | Public data (weather, demographics, regulations) | Standard HTTPS |

### API Security Checklist
- [ ] All APIs use HTTPS
- [ ] API keys stored in secure vault (HashiCorp Vault, AWS Secrets Manager)
- [ ] OAuth 2.0 for user authentication
- [ ] Rate limiting implemented
- [ ] Request/response logging for audit
- [ ] Input validation and sanitization
- [ ] Circuit breaker for external API failures

---

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| API Response Time | < 500ms (p95) | For cached/common queries |
| Credit Calculation | < 30 seconds | For complex energy modeling |
| Report Generation | < 2 minutes | Full LEED documentation |
| System Availability | 99.9% | Excluding planned maintenance |
| Data Freshness | Real-time | For IoT sensor integration |

---

## Scalability Considerations

### Horizontal Scaling
- Microservices can scale independently
- API Gateway handles load balancing
- Message queue decouples services

### Caching Strategy
- Redis for API response caching (TTL: 1 hour for government data)
- CDN for static assets and reports
- Database query result caching

### Database Scaling
- PostgreSQL read replicas for reporting
- TimescaleDB partitioning by time for metrics
- Archive old data to cold storage

---

*Architecture document for LEED v5 automation platform*
*Version 1.0*
