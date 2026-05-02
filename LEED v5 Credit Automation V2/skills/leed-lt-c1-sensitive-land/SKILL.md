---
name: leed-lt-c1-sensitive-land
version: 1.0.0
author: LEED Automation Platform
description: Automates LTc1 Sensitive Land Protection credit compliance through GIS overlay analysis against FEMA floodplains, NWI wetlands, USFWS critical habitats, NRCS prime farmland, and USGS slope data.
---

## Metadata
- **Credit Code:** LTc1
- **Credit Name:** Sensitive Land Protection
- **Points:** 1 point
- **Automation Level:** 87.6%
- **Complexity:** Medium
- **Primary Data Source:** FEMA NFHL, NWI, USFWS Critical Habitat, USDA NRCS Soil Surveys, USGS National Map
- **HITL Required:** Yes

## Purpose
Determines if a project site overlaps with sensitive lands (floodplains, wetlands, endangered species habitats, prime farmland, or public parkland) by executing automated GIS overlay and buffer analysis against US federal geospatial data layers, producing compliance documentation and GIS maps.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| project_id | string | User / PMS | UUID format, non-empty |
| site_boundary | GeoJSON (Polygon) | User / GIS import | Valid GeoJSON, area > 0, WGS84 CRS |
| site_area_acres | float | User / CAD export | > 0, matches boundary calculated area ±5% |
| project_name | string | User | Non-empty, max 200 chars |
| project_address | string | User | Non-empty, contains city, state |
| existing_site_conditions | enum | User | "greenfield", "brownfield", "remediated", "previously_developed" |
| contact_email | string | User | Valid email format |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| buffer_distance_ft | float | 50.0 | Buffer radius around site boundary for proximity analysis |
| slope_threshold_percent | float | 15.0 | Maximum allowable slope percentage for prime farmland exemption |
| brownfield_documentation | File (PDF) | null | EPA or state remediation certification for brownfield sites |
| previous_land_use | string | null | Historical land use description (e.g., "industrial", "agricultural") |
| parkland_exemption_claim | boolean | false | If true, trigger additional parkland proximity check |
| parkland_buffer_ft | float | 100.0 | Buffer for public parkland proximity analysis |
| output_language | string | "en" | ISO 639-1 code for report language |
| include_slope_analysis | boolean | true | Whether to perform USGS DEM slope analysis |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. Parse and validate the GeoJSON site boundary using `shapely` — ensure valid Polygon, no self-intersections, area > 0.
  2. Reproject to WGS84 (EPSG:4326) if CRS is specified otherwise.
  3. Compute area in acres from boundary geometry using `geopy` + `pyproj` (Albers Equal Area for accuracy).
  4. Cross-check `site_area_acres` against computed area; fail if deviation > 5%.
  5. Validate `existing_site_conditions`: if "brownfield" or "remediated", ensure `brownfield_documentation` is provided.
  6. Validate email format with `email-validator`.
- **Output:** `ValidatedInputs` dict with reprojected boundary geometry, computed area, and cleaned fields.
- **On Failure:** Return HTTP 400 with detailed validation errors; log to structured error log; do NOT proceed.

### Step 2: Fetch FEMA Floodplain Data
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. Query FEMA NFHL REST MapServer to identify 100-year floodplain (SFHA) polygons intersecting the site boundary + buffer.
  2. Endpoint: `https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query`
  3. Parameters: `geometry={site_envelope}`, `geometryType=esriGeometryEnvelope`, `spatialRel=esriSpatialRelIntersects`, `outFields=FLD_ZONE,SFHA_TF`, `returnGeometry=true`, `f=json`
  4. Filter results to `SFHA_TF = 'T'` (within Special Flood Hazard Area) or `FLD_ZONE` in ['A', 'AE', 'AH', 'AO', 'V', 'VE'].
  5. Perform spatial intersection between site boundary and returned floodplain polygons.
- **Output:** `FloodplainResult` — list of intersecting floodplain features with overlap area (acres), FLD_ZONE codes, and intersection geometry.
- **On Failure:** If API timeout (>30s), retry up to 3x with exponential backoff. If persistent failure, fall back to cached NFHL data (if < 90 days old). If no cached data, escalate to HITL.

### Step 3: Fetch NWI Wetland Data
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. Query USFWS National Wetlands Inventory (NWI) WMS/WFS for wetland polygons intersecting site boundary + buffer.
  2. Endpoint: `https://www.fws.gov/wetlands/arcgis/rest/services/Wetlands/MapServer/0/query`
  3. Parameters: `geometry={site_envelope}`, `geometryType=esriGeometryEnvelope`, `spatialRel=esriSpatialRelIntersects`, `outFields=ATTRIBUTE,WETLAND_TYPE`, `returnGeometry=true`, `f=json`
  4. Filter to non-"upland" classifications (exclude `WETLAND_TYPE = 'Upland'`).
  5. Perform spatial intersection to calculate exact wetland overlap area.
- **Output:** `WetlandResult` — intersecting wetland features with overlap area, wetland classification codes, and intersection geometry.
- **On Failure:** Retry 3x. NWI WMS fallback via `https://www.fws.gov/wetlands/geoserver/wms?SERVICE=WMS&REQUEST=GetMap`. If all fail, escalate to HITL.

### Step 4: Fetch USFWS Critical Habitat Data
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. Query USFWS ECOS Critical Habitat portal for designated critical habitat polygons.
  2. Endpoint: `https://ecos.fws.gov/ecp/pull/crithab.cgi`
  3. Alternative direct REST: `https://ecos.fws.gov/arcgis/rest/services/crithab/crithab_ao/MapServer/0/query`
  4. Parameters: `geometry={site_envelope}`, `geometryType=esriGeometryEnvelope`, `spatialRel=esriSpatialRelIntersects`, `outFields=spcode,sciname,comname,unit`, `returnGeometry=true`, `f=json`
  5. Perform spatial intersection to calculate overlap area and identify affected species.
- **Output:** `CriticalHabitatResult` — intersecting habitat units with species scientific/common names, overlap area, and intersection geometry.
- **On Failure:** Retry 3x. Fall back to USFWS IPaC (Information for Planning and Consultation) API. If persistent failure, escalate to HITL.

### Step 5: Fetch NRCS Prime Farmland Data
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. Query USDA NRCS Soil Survey Geographic (SSURGO) database via Soil Data Access (SDA) or Web Soil Survey REST API.
  2. Endpoint: `https://SDMDataAccess.sc.egov.usda.gov/Tabular/SDMTabularService/postRest`
  3. Execute SQL via SDA:
     ```sql
     SELECT mu.mukey, mu.musym, comp.compname, comp.majcompflag,
            comp.farmlndcl, muarea_wt.interp_area
     FROM mapunit mu
     INNER JOIN component comp ON mu.mukey = comp.mukey
     INNER JOIN muarea_wt ON mu.mukey = muarea_wt.mukey
     WHERE mu.mukey IN (
       SELECT mukey FROM SDA_Get_Mukey_from_intersection_with_WktWgs84('{site_wkt}')
     )
     AND comp.majcompflag = 'Yes'
     AND comp.farmlndcl LIKE '%Prime%'
     ```
  4. Alternative: Web Soil Survey AOI query via `https://websoilsurvey.nrcs.usda.gov/wss/aoi` workflow.
  5. Calculate prime farmland overlap area weighted by component percentage.
- **Output:** `PrimeFarmlandResult` — intersecting map units with farmland classification, weighted overlap area, and SSURGO mukeys.
- **On Failure:** Retry 3x. Fall back to STATSGO2 (generalized soil data) if SSURGO unavailable. If persistent failure, escalate to HITL.

### Step 6: Perform Slope Analysis (USGS DEM)
- **Type:** API Call + Calculation
- **Automated:** Yes
- **Description:**
  1. Fetch USGS 3D Elevation Program (3DEP) DEM tile covering site boundary.
  2. Endpoint: `https://portal.opentopography.org/API/globaldem?demtype=SRTMGL1&south={}&north={}&west={}&east={}&outputFormat=GTiff`
  3. Alternative: USGS National Map TNM Elevation Point Query Service `https://nationalmap.gov/epqs/pqs.php?x={lon}&y={lat}&units=Feet&output=json`
  4. Calculate slope percentage across site boundary using GDAL `gdaldem slope` or rasterio + numpy:
     ```python
     slope = numpy.degrees(numpy.arctan(numpy.sqrt(dx**2 + dy**2)))  # percent = tan(angle)*100
     ```
  5. Identify areas exceeding `slope_threshold_percent`.
  6. Slope > 15% is a prime farmland exemption criterion under NRCS rules.
- **Output:** `SlopeResult` — max slope, mean slope, area exceeding threshold, slope raster clipped to site boundary.
- **On Failure:** If DEM unavailable, use SRTM 30m global DEM fallback. If still unavailable, mark slope analysis as "incomplete" and flag for HITL.

### Step 7: Perform Parkland Proximity Check (Optional)
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. If `parkland_exemption_claim` is false, skip and mark as `not_applicable`.
  2. Query USGS Protected Areas Database (PAD-US) for public parkland/recreation areas.
  3. Endpoint: `https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/PADUS_ProtectedAreas/FeatureServer/0/query`
  4. Parameters: `geometry={site_envelope}`, `spatialRel=esriSpatialRelIntersects`, `outFields=Own_Type,Mang_Type,Des_Tp`, `returnGeometry=true`, `f=json`
  5. Filter for `Own_Type = 'Federal' OR Own_Type = 'State' OR Own_Type = 'Local'` with `Des_Tp` containing "Park" or "Recreation".
  6. Perform buffer analysis: check if parkland polygon intersects site boundary expanded by `parkland_buffer_ft`.
- **Output:** `ParklandResult` — nearby parkland features with distance to site, ownership type, and designation.
- **On Failure:** Retry 2x. PAD-US data is updated annually; if unavailable, note in report and flag for HITL.

### Step 8: Consolidate Overlap Analysis
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Union all intersecting geometries from Steps 2–7.
  2. Calculate total sensitive land overlap area (acres) and percentage of total site area.
  3. Determine credit achievability:
     - If NO overlap with any sensitive land category → Credit is ACHIEVABLE.
     - If overlap exists AND `existing_site_conditions` in ["brownfield", "remediated"] AND valid brownfield documentation provided → Credit may be achievable (requires LEED reviewer interpretation).
     - If overlap exists AND `existing_site_conditions` = "greenfield" → Credit is NOT ACHIEVABLE.
     - If prime farmland overlap exists AND slope > 15% → Apply NRCS exemption; prime farmland may not disqualify.
  4. Generate sensitivity score (0–100): weighted combination of overlap percentages across categories.
  5. Prepare structured `AnalysisSummary` with all findings, geometries, and compliance determination.
- **Output:** `AnalysisSummary` dict with achievability flag, overlap breakdown, sensitivity score, and reasoning.
- **On Failure:** If geometric operations fail (invalid topology), log error and escalate to HITL.

### Step 9: HITL Checkpoint — GIS Boundary & Overlap Verification
- **Type:** Human Review
- **Automated:** No
- **Description:**
  1. Pause workflow and notify assigned reviewer via email/SMS with a review link.
  2. Present to reviewer:
     - Site boundary overlay map (interactive) showing all sensitive land layers.
     - Tabular summary of overlaps with acreages and percentages.
     - Individual layer toggles for FEMA, NWI, USFWS, NRCS, USGS slope.
     - Compliance determination (achievable / not achievable / needs interpretation).
  3. Reviewer must confirm:
     - Site boundary accuracy (correct lat/lon, proper projection).
     - Overlap interpretation (false positives from GIS data alignment issues).
     - Brownfield/remediation documentation validity (if applicable).
     - Slope threshold applicability.
  4. Reviewer options: `APPROVE`, `REJECT_WITH_COMMENTS`, `REQUEST_REANALYSIS`.
- **Output:** `HITLReviewResult` with reviewer decision, timestamp, comments, and verified flag.
- **On Failure:** If reviewer does not respond within SLA, escalate to senior reviewer and send reminder. After 2x SLA, auto-approve with warning flag if confidence score > 90%; otherwise escalate to project manager.

### Step 10: Generate Output Documents
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. **Sensitive Land Analysis Report (PDF):**
     - Executive summary with compliance determination.
     - Methodology section describing each API query, buffer distance, slope calculation method.
     - Detailed findings per category (floodplain, wetland, critical habitat, prime farmland, slope, parkland).
     - Overlap tables with acres, percentages, and affected species (if habitat).
     - Screenshots of GIS overlay maps.
     - Brownfield documentation appendix (if applicable).
     - Data source citations with access dates and API URLs.
     - Generated using `reportlab` + `matplotlib` for tables/charts.
  2. **GIS Overlap Map (PDF):**
     - Multi-layer map rendered with `geopandas` + `matplotlib` or `folium` + `pdfkit`.
     - Layers: site boundary (red), floodplain (blue), wetland (teal), critical habitat (orange), prime farmland (green), slope > threshold (yellow hatching), parkland (purple).
     - Legend, scale bar, north arrow, and data source attribution.
     - A4/Letter format, 300 DPI.
  3. **Compliance Declaration (DOCX):**
     - LEED v5 LTc1 formal compliance declaration template.
     - Auto-filled project details, site area, analysis date, and determination.
     - Signature blocks for project team and reviewer.
     - Generated using `python-docx` from Jinja2 template.
- **Output:** Three document objects with file paths, checksums, and generation timestamps.
- **On Failure:** If document generation fails (missing fonts, template errors), retry once with fallback template. If persistent, log error and return raw JSON analysis for manual report creation.

### Step 11: Finalize & Persist Results
- **Type:** Calculation / Persistence
- **Automated:** Yes
- **Description:**
  1. Compute MD5 checksums for all output documents.
  2. Persist `AnalysisSummary`, `HITLReviewResult`, document paths, and raw API responses to project database.
  3. Emit structured event to LEED compliance tracking system.
  4. Send notification email to `contact_email` with results summary and document download links.
  5. Update skill execution status to `COMPLETED`.
- **Output:** `FinalResult` dict with all document paths, URLs, compliance status, and audit trail.
- **On Failure:** If persistence fails, retry 3x. If database unavailable, queue results to local disk and alert ops team.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 9: GIS Boundary & Overlap Verification | LEED AP or GIS Analyst | 48 hours | Verify: (1) site boundary accurately reflects project limits, (2) GIS overlaps are genuine (not data misalignment artifacts), (3) brownfield documentation is current and complete if applicable, (4) slope threshold selection is appropriate for site context. Use interactive map to toggle layers. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| FEMA NFHL MapServer (REST) | 100-year floodplain (SFHA) intersection | US only | Cached NFHL data (90-day TTL) | No explicit limit; 10 req/min recommended |
| NWI MapServer (REST) | Wetland polygon intersection | US only | NWI WMS GetMap; local NWI geodatabase | No explicit limit; 10 req/min recommended |
| USFWS ECOS Critical Habitat | Endangered species habitat intersection | US only | USFWS IPaC API; local critical habitat shapefile | 100 req/min |
| USDA NRCS Soil Data Access (SDA) | SSURGO prime farmland query | US only | STATSGO2 generalized soils; Web Soil Survey manual export | 100 req/min via REST; SDA SQL has no explicit limit |
| USGS 3DEP / TNM Elevation | DEM download for slope analysis | US primary; SRTM global | SRTM 30m global DEM; ASTER GDEM | 3DEP: no limit; TNM: 10 req/sec |
| USGS PAD-US | Public parkland/recreation proximity | US only | Local PAD-US shapefile download (annual) | No explicit limit; 10 req/min recommended |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | All APIs fully operational; primary target region. |
| Puerto Rico / US Territories | Limited | FEMA NFHL covers PR; NWI and NRCS may have gaps in Pacific territories. |
| Canada | Unavailable | No equivalent federal API integrations; manual data submission required. |
| Mexico | Unavailable | No equivalent federal API integrations; manual data submission required. |
| International (non-North America) | Unavailable | All primary data sources are US federal; international projects require manual GIS analysis with local data. |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Invalid GeoJSON boundary | Return 400, log structured error | Yes (email) | 0 |
| Site area mismatch > 5% | Return 400, prompt user to verify | Yes (email) | 0 |
| FEMA NFHL timeout / 5xx | Retry with exponential backoff, then use cached data | Yes if all retries fail | 3 |
| NWI service unavailable | Retry, then use WMS fallback | Yes if all retries fail | 3 |
| USFWS ECOS timeout | Retry, then use IPaC fallback | Yes if all retries fail | 3 |
| NRCS SDA SQL error | Retry, then use STATSGO2 | Yes if all retries fail | 3 |
| USGS DEM unavailable | Use SRTM 30m global fallback | Yes if fallback fails | 2 |
| Geometry topology error during overlay | Log error, flag for HITL review | Yes (immediate) | 0 |
| HITL reviewer no-response (48h) | Escalate to senior reviewer, then auto-approve if confidence > 90% | Yes (escalation chain) | N/A |
| Document generation failure | Retry with fallback template, then return raw JSON | Yes if persistent | 1 |
| Database persistence failure | Queue to local disk, alert ops | Yes (ops team) | 3 |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Sensitive Land Analysis Report | PDF | Comprehensive report with methodology, findings per category, overlap tables, GIS screenshots, data citations, and brownfield appendix. |
| GIS Overlap Map | PDF | Multi-layer cartographic map showing site boundary and all sensitive land overlays with legend, scale, and attribution. |
| Compliance Declaration | DOCX | LEED v5 LTc1 formal declaration with auto-filled project data, compliance determination, and signature blocks. |

## Testing
```bash
# Unit tests for validation, API clients, and calculations
python -m pytest skills/leed-lt-c1-sensitive-land/tests/

# Integration tests with mocked APIs
python -m pytest skills/leed-lt-c1-sensitive-land/tests/integration/ -v

# End-to-end test with sample site boundary (Denver, CO — no sensitive land)
python -m pytest skills/leed-lt-c1-sensitive-land/tests/e2e/test_clean_site.py

# End-to-end test with sample site boundary (New Orleans, LA — floodplain overlap)
python -m pytest skills/leed-lt-c1-sensitive-land/tests/e2e/test_floodplain_overlap.py
```

## Example Usage (OpenAI Agents SDK + Restate)
```python
from leed_platform.skills import LEEDLTC1SensitiveLandSkill

skill = LEEDLTC1SensitiveLandSkill(
    project_id="leed-proj-2025-8842",
    inputs={
        "project_name": "Riverside Office Complex",
        "project_address": "1200 Riverfront Drive, New Orleans, LA 70130",
        "site_boundary": {
            "type": "Polygon",
            "coordinates": [[[-90.07, 29.95], [-90.07, 29.96], [-90.06, 29.96], [-90.06, 29.95], [-90.07, 29.95]]]
        },
        "site_area_acres": 12.5,
        "existing_site_conditions": "greenfield",
        "contact_email": "pm@example.com",
        "buffer_distance_ft": 50.0,
        "slope_threshold_percent": 15.0,
        "include_slope_analysis": True,
        "parkland_exemption_claim": False,
    }
)

result = await skill.execute()

# result structure:
# {
#   "compliance_status": "NOT_ACHIEVABLE",  # or "ACHIEVABLE" / "NEEDS_INTERPRETATION"
#   "sensitivity_score": 78.4,
#   "overlaps": {
#     "floodplain": {"overlap_acres": 3.2, "percentage": 25.6, "zones": ["AE"]},
#     "wetland": {"overlap_acres": 0.0, "percentage": 0.0, "classifications": []},
#     "critical_habitat": {"overlap_acres": 0.0, "percentage": 0.0, "species": []},
#     "prime_farmland": {"overlap_acres": 0.0, "percentage": 0.0, "mapunits": []},
#     "slope_exceeds_threshold": {"overlap_acres": 0.0, "percentage": 0.0, "max_slope": 4.2},
#     "parkland": {"nearby": False, "distance_ft": None}
#   },
#   "documents": {
#     "analysis_report": "/mnt/agents/output/projects/leed-proj-2025-8842/LTc1_Analysis_Report.pdf",
#     "gis_map": "/mnt/agents/output/projects/leed-proj-2025-8842/LTc1_GIS_Overlap_Map.pdf",
#     "compliance_declaration": "/mnt/agents/output/projects/leed-proj-2025-8842/LTc1_Compliance_Declaration.docx"
#   },
#   "hitl_review": {
#     "required": True,
#     "status": "PENDING",
#     "review_url": "https://review.ecogen.io/hitl/ltc1/..."
#   },
#   "audit_trail": [...]
# }
```

## Platform Workflow (OpenAI Agents SDK + Restate)
```python
from langgraph.graph import StateGraph, END
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

class ComplianceStatus(Enum):
    ACHIEVABLE = "ACHIEVABLE"
    NOT_ACHIEVABLE = "NOT_ACHIEVABLE"
    NEEDS_INTERPRETATION = "NEEDS_INTERPRETATION"
    PENDING_REVIEW = "PENDING_REVIEW"

@dataclass
class LEEDState:
    project_id: str
    inputs: Dict[str, Any]
    validated: bool = False
    floodplain_result: Optional[Dict] = None
    wetland_result: Optional[Dict] = None
    habitat_result: Optional[Dict] = None
    farmland_result: Optional[Dict] = None
    slope_result: Optional[Dict] = None
    parkland_result: Optional[Dict] = None
    analysis_summary: Optional[Dict] = None
    hitl_status: str = "NOT_REQUIRED"
    compliance_status: ComplianceStatus = ComplianceStatus.PENDING_REVIEW
    documents: Dict[str, str] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    retry_counts: Dict[str, int] = field(default_factory=lambda: {k: 0 for k in [
        "fema", "nwi", "usfws", "nrcs", "usgs_dem", "parkland", "documents", "persist"
    ]})

# --- Node Functions ---

async def validate_inputs(state: LEEDState) -> LEEDState:
    """Step 1: Parse, validate, and reproject GeoJSON; check area consistency."""
    from leed_platform.validators import GeoJSONValidator, AreaValidator, EmailValidator
    try:
        boundary = GeoJSONValidator.validate(state.inputs["site_boundary"])
        computed_acres = AreaValidator.geojson_to_acres(boundary)
        assert abs(computed_acres - state.inputs["site_area_acres"]) / computed_acres <= 0.05
        EmailValidator.validate(state.inputs["contact_email"])
        if state.inputs.get("existing_site_conditions") in ("brownfield", "remediated"):
            assert state.inputs.get("brownfield_documentation"), "Brownfield docs required"
        state.validated = True
    except Exception as e:
        state.errors.append(f"VALIDATION_ERROR: {str(e)}")
    return state

async def fetch_fema_data(state: LEEDState) -> LEEDState:
    """Step 2: Query FEMA NFHL for 100-year floodplain intersection."""
    from leed_platform.apis import FEMANFHLClient
    if not state.validated:
        return state
    client = FEMANFHLClient()
    try:
        state.floodplain_result = await client.query_floodplain(
            boundary=state.inputs["site_boundary"],
            buffer_ft=state.inputs.get("buffer_distance_ft", 50.0)
        )
    except Exception as e:
        if state.retry_counts["fema"] < 3:
            state.retry_counts["fema"] += 1
            # LangGraph will route back to this node via conditional edge
        else:
            state.errors.append(f"FEMA_API_FAILED: {str(e)}")
            state.floodplain_result = {"status": "ERROR", "overlap_acres": 0, "fallback": "cached"}
    return state

async def fetch_nwi_data(state: LEEDState) -> LEEDState:
    """Step 3: Query NWI for wetland intersection."""
    from leed_platform.apis import NWIClient
    if not state.validated:
        return state
    client = NWIClient()
    try:
        state.wetland_result = await client.query_wetlands(
            boundary=state.inputs["site_boundary"],
            buffer_ft=state.inputs.get("buffer_distance_ft", 50.0)
        )
    except Exception as e:
        if state.retry_counts["nwi"] < 3:
            state.retry_counts["nwi"] += 1
        else:
            state.errors.append(f"NWI_API_FAILED: {str(e)}")
            state.wetland_result = {"status": "ERROR", "overlap_acres": 0, "fallback": "wms"}
    return state

async def fetch_usfws_data(state: LEEDState) -> LEEDState:
    """Step 4: Query USFWS ECOS for critical habitat intersection."""
    from leed_platform.apis import USFWSCriticalHabitatClient
    if not state.validated:
        return state
    client = USFWSCriticalHabitatClient()
    try:
        state.habitat_result = await client.query_critical_habitat(
            boundary=state.inputs["site_boundary"],
            buffer_ft=state.inputs.get("buffer_distance_ft", 50.0)
        )
    except Exception as e:
        if state.retry_counts["usfws"] < 3:
            state.retry_counts["usfws"] += 1
        else:
            state.errors.append(f"USFWS_API_FAILED: {str(e)}")
            state.habitat_result = {"status": "ERROR", "overlap_acres": 0, "fallback": "ipac"}
    return state

async def fetch_nrcs_data(state: LEEDState) -> LEEDState:
    """Step 5: Query USDA NRCS SDA for prime farmland intersection."""
    from leed_platform.apis import NRCSSoilDataClient
    if not state.validated:
        return state
    client = NRCSSoilDataClient()
    try:
        state.farmland_result = await client.query_prime_farmland(
            boundary=state.inputs["site_boundary"]
        )
    except Exception as e:
        if state.retry_counts["nrcs"] < 3:
            state.retry_counts["nrcs"] += 1
        else:
            state.errors.append(f"NRCS_API_FAILED: {str(e)}")
            state.farmland_result = {"status": "ERROR", "overlap_acres": 0, "fallback": "statsgo2"}
    return state

async def perform_slope_analysis(state: LEEDState) -> LEEDState:
    """Step 6: Fetch USGS DEM and calculate slope percentage."""
    from leed_platform.apis import USGSDEMClient
    from leed_platform.calculations import SlopeCalculator
    if not state.validated or not state.inputs.get("include_slope_analysis", True):
        state.slope_result = {"status": "SKIPPED"}
        return state
    dem_client = USGSDEMClient()
    try:
        dem_path = await dem_client.download_dem_for_boundary(
            boundary=state.inputs["site_boundary"]
        )
        calculator = SlopeCalculator(dem_path)
        state.slope_result = calculator.analyze_site_slope(
            boundary=state.inputs["site_boundary"],
            threshold_percent=state.inputs.get("slope_threshold_percent", 15.0)
        )
    except Exception as e:
        if state.retry_counts["usgs_dem"] < 2:
            state.retry_counts["usgs_dem"] += 1
        else:
            state.errors.append(f"USGS_DEM_FAILED: {str(e)}")
            state.slope_result = {"status": "ERROR", "fallback": "srtm30"}
    return state

async def fetch_parkland_data(state: LEEDState) -> LEEDState:
    """Step 7: Query PAD-US for public parkland proximity (optional)."""
    from leed_platform.apis import PADUSClient
    if not state.validated or not state.inputs.get("parkland_exemption_claim", False):
        state.parkland_result = {"status": "NOT_APPLICABLE"}
        return state
    client = PADUSClient()
    try:
        state.parkland_result = await client.query_parkland_proximity(
            boundary=state.inputs["site_boundary"],
            buffer_ft=state.inputs.get("parkland_buffer_ft", 100.0)
        )
    except Exception as e:
        if state.retry_counts["parkland"] < 2:
            state.retry_counts["parkland"] += 1
        else:
            state.errors.append(f"PADUS_API_FAILED: {str(e)}")
            state.parkland_result = {"status": "ERROR", "nearby": False}
    return state

async def consolidate_analysis(state: LEEDState) -> LEEDState:
    """Step 8: Union overlaps and determine credit achievability."""
    from leed_platform.calculations import SensitiveLandAnalyzer
    if not state.validated:
        return state
    analyzer = SensitiveLandAnalyzer()
    state.analysis_summary = analyzer.consolidate(
        floodplain=state.floodplain_result,
        wetland=state.wetland_result,
        habitat=state.habitat_result,
        farmland=state.farmland_result,
        slope=state.slope_result,
        parkland=state.parkland_result,
        site_area_acres=state.inputs["site_area_acres"],
        existing_conditions=state.inputs["existing_site_conditions"],
        brownfield_docs=state.inputs.get("brownfield_documentation")
    )
    state.compliance_status = ComplianceStatus(state.analysis_summary["compliance_status"])
    return state

async def human_review_checkpoint(state: LEEDState) -> LEEDState:
    """Step 9: HITL — pause and notify reviewer."""
    from leed_platform.hitl import HITLManager
    if not state.validated:
        return state
    # HITL always triggered for LTc1 due to GIS interpretation complexity
    hitl = HITLManager(
        skill="leed-lt-c1-sensitive-land",
        project_id=state.project_id,
        sla_hours=48,
        reviewer_role="LEED_AP_GIS"
    )
    review = await hitl.request_review(
        analysis=state.analysis_summary,
        maps=state.documents.get("gis_map"),
        context="Verify GIS boundary accuracy and overlap interpretation for sensitive land credit."
    )
    state.hitl_status = review.status  # "PENDING", "APPROVED", "REJECTED", "REANALYSIS"
    if review.status == "APPROVED":
        state.compliance_status = ComplianceStatus(state.analysis_summary["compliance_status"])
    elif review.status == "REJECTED":
        state.compliance_status = ComplianceStatus.PENDING_REVIEW
        state.errors.append(f"HITL_REJECTED: {review.comments}")
    return state

async def generate_documents(state: LEEDState) -> LEEDState:
    """Step 10: Generate PDF analysis report, GIS map, and DOCX declaration."""
    from leed_platform.documents import PDFReportGenerator, GISMapGenerator, DOCXDeclarationGenerator
    if not state.validated:
        return state
    try:
        report_gen = PDFReportGenerator(template="ltc1_analysis_report")
        state.documents["analysis_report"] = await report_gen.generate(
            project_id=state.project_id,
            inputs=state.inputs,
            analysis=state.analysis_summary,
            hitl=state.hitl_status
        )
        map_gen = GISMapGenerator(template="ltc1_gis_overlay")
        state.documents["gis_map"] = await map_gen.generate(
            boundary=state.inputs["site_boundary"],
            layers={
                "floodplain": state.floodplain_result,
                "wetland": state.wetland_result,
                "habitat": state.habitat_result,
                "farmland": state.farmland_result,
                "slope": state.slope_result,
                "parkland": state.parkland_result
            }
        )
        decl_gen = DOCXDeclarationGenerator(template="ltc1_compliance_declaration")
        state.documents["compliance_declaration"] = await decl_gen.generate(
            project_id=state.project_id,
            inputs=state.inputs,
            analysis=state.analysis_summary,
            compliance_status=state.compliance_status.value
        )
    except Exception as e:
        if state.retry_counts["documents"] < 1:
            state.retry_counts["documents"] += 1
            # Retry with fallback template
        else:
            state.errors.append(f"DOCUMENT_GENERATION_FAILED: {str(e)}")
    return state

async def finalize_results(state: LEEDState) -> LEEDState:
    """Step 11: Persist, emit events, notify stakeholders."""
    from leed_platform.persistence import ProjectStore
    from leed_platform.notifications import EmailNotifier
    if not state.validated:
        return state
    store = ProjectStore()
    try:
        await store.persist_lt_c1_results(
            project_id=state.project_id,
            analysis=state.analysis_summary,
            hitl=state.hitl_status,
            documents=state.documents,
            audit=state.errors
        )
        notifier = EmailNotifier()
        await notifier.send_lt_c1_completion(
            to=state.inputs["contact_email"],
            project_id=state.project_id,
            status=state.compliance_status.value,
            documents=state.documents
        )
    except Exception as e:
        if state.retry_counts["persist"] < 3:
            state.retry_counts["persist"] += 1
        else:
            state.errors.append(f"PERSISTENCE_FAILED: {str(e)}")
            # Queue to local disk for manual recovery
    return state

# --- Conditional Routing ---

def route_after_fema(state: LEEDState) -> str:
    if state.floodplain_result and state.floodplain_result.get("status") != "ERROR":
        return "fetch_nwi"
    if state.retry_counts["fema"] < 3:
        return "fetch_fema"  # Retry
    return "fetch_nwi"  # Continue with degraded data

def route_after_analysis(state: LEEDState) -> str:
    if state.errors and any("HITL" in e for e in state.errors):
        return "hitl_review"
    # LTc1 always requires HITL for GIS verification
    return "hitl_review"

def route_after_hitl(state: LEEDState) -> str:
    if state.hitl_status == "REANALYSIS":
        return "consolidate"
    return "generate_documents"

# --- Build LangGraph Workflow ---

workflow = StateGraph(LEEDState)
workflow.add_node("validate", validate_inputs)
workflow.add_node("fetch_fema", fetch_fema_data)
workflow.add_node("fetch_nwi", fetch_nwi_data)
workflow.add_node("fetch_usfws", fetch_usfws_data)
workflow.add_node("fetch_nrcs", fetch_nrcs_data)
workflow.add_node("slope_analysis", perform_slope_analysis)
workflow.add_node("fetch_parkland", fetch_parkland_data)
workflow.add_node("consolidate", consolidate_analysis)
workflow.add_node("hitl_review", human_review_checkpoint)
workflow.add_node("generate_documents", generate_documents)
workflow.add_node("finalize", finalize_results)

workflow.set_entry_point("validate")
workflow.add_conditional_edges("validate", lambda s: "fetch_fema" if s.validated else END)
workflow.add_conditional_edges("fetch_fema", route_after_fema)
workflow.add_edge("fetch_nwi", "fetch_usfws")
workflow.add_edge("fetch_usfws", "fetch_nrcs")
workflow.add_edge("fetch_nrcs", "slope_analysis")
workflow.add_edge("slope_analysis", "fetch_parkland")
workflow.add_edge("fetch_parkland", "consolidate")
workflow.add_conditional_edges("consolidate", route_after_analysis)
workflow.add_conditional_edges("hitl_review", route_after_hitl)
workflow.add_edge("generate_documents", "finalize")
workflow.add_edge("finalize", END)

ltc1_skill_app = workflow.compile()
```
