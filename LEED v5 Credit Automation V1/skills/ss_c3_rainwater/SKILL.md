---
name: leed-ss-c3-rainwater
version: 1.0.0
author: LEED Automation Platform
description: Automates LEED v5 SSc3 Rainwater Management credit — GI sizing, runoff retention, and percentile-based compliance
---

## Metadata
- **Credit Code:** SSc3
- **Credit Name:** Rainwater Management
- **Points:** 3
- **Automation Level:** 88.0%
- **Complexity:** Medium
- **Primary Data Source:** NOAA Atlas 14, NRCS Soil Survey, USGS National Map
- **HITL Required:** Yes

## Purpose
Automates the calculation, validation, and documentation required for LEED v5 SSc3 Rainwater Management by fetching NOAA Atlas 14 rainfall data, querying NRCS soil properties and USGS topographic data, computing runoff and green infrastructure (GI) retention volumes, and producing compliance reports for either the percentile (80th/95th) or green infrastructure (LID/GI) compliance pathway.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `project_lat` | float | Project intake / user | -90 to 90, non-null |
| `project_lon` | float | Project intake / user | -180 to 180, non-null |
| `site_area_sqft` | float | Project intake / user | > 0 |
| `impervious_pct` | float | Project intake / user | 0.0 to 100.0 |
| `compliance_pathway` | str | User selection | OneOf: `percentile_80`, `percentile_95`, `gi_lid` |
| `gi_measures` | list[dict] | User / design team | Each dict must contain: `type`, `area_sqft`, `depth_in`, `retention_rate` |

### `gi_measures` Schema
| Key | Type | Description |
|-----|------|-------------|
| `type` | str | OneOf: `bioswale`, `rain_garden`, `permeable_pavement`, `green_roof`, `cistern`, `infiltration_trench` |
| `area_sqft` | float | Surface footprint of the GI measure in square feet |
| `depth_in` | float | Effective depth / media depth in inches |
| `retention_rate` | float | Fraction of stormwater retained (0.0–1.0) |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `design_storm_duration_hr` | int | 24 | Storm duration for runoff calculation |
| `runoff_coefficient` | float | 0.95 | Runoff coefficient for impervious surfaces (C=0.95 typical for asphalt/concrete) |
| `evapotranspiration_factor` | float | 0.0 | ET loss fraction applied to retention volume |
| `soil_override` | dict | null | Manual override of NRCS soil properties (keys: `hydrologic_group`, `infiltration_rate_in_hr`, `porosity`) |
| `elevation_override_ft` | float | null | Manual override of site elevation in feet |
| `include_climate_change_adjustment` | bool | true | Apply NOAA Atlas 14 projected adjustment factor |
| `output_format` | str | `pdf` | OneOf: `pdf`, `docx` |
| `project_name` | str | "Unnamed Project" | Used in report headers |
| `project_address` | str | null | Street address for geocoding verification |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:** 
  1. Enforce schema on all required and optional inputs.
  2. Ensure `impervious_pct` + pervious assumptions ≤ 100%.
  3. Validate `gi_measures` list — each entry must have `type`, `area_sqft`, `depth_in`, `retention_rate` within bounds.
  4. Ensure `compliance_pathway` is one of the three allowed values.
  5. Cross-check that `gi_measures` is non-empty when `compliance_pathway == "gi_lid"`.
  6. Convert `site_area_sqft` and `impervious_pct` into `impervious_area_sqft` internally.
- **Output:** `ValidationResult` object with cleaned inputs or `ValidationError` list.
- **On Failure:** Terminate workflow; return error payload to caller with field-level messages.

### Step 2: Fetch NOAA Atlas 14 Rainfall Data
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. Call NOAA Precipitation Frequency Data Server (`https://hdsc.nws.noaa.gov/cgi-bin/hdsc/new/cgi_readPfds.py?lat={lat}&lon={lon}&data=depth&unit=english&series=pds&returnInterval=100&temporalResolution=24h&startYear=0&endYear=2023`) to retrieve 24-hour precipitation depths.
  2. Parse response for 80th and 95th percentile rainfall depths (inches) for the project location.
  3. If `include_climate_change_adjustment` is true, apply the NOAA Atlas 14 projected adjustment factor (typically 1.05–1.15 depending on region).
  4. Cache raw NOAA response in project-scoped blob storage for audit trail.
- **Output:** `NOAARainfallData` — `{p80_in: float, p95_in: float, raw_data_url: str, adjustment_applied: bool, adjustment_factor: float}`
- **On Failure:** Retry 3× with exponential backoff (2s, 4s, 8s). After retries, fail over to `USGS US GHCN` daily rainfall dataset or manual HITL input prompt.

### Step 3: Fetch NRCS Soil Survey Data
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. Call NRCS Soil Survey API (`https://sdmdataaccess.sc.egov.usda.gov/Tabular/SDMTabularService/post.rest`) with SOAP/REST payload requesting `mapunit` and `component` tables for the bounding box around `project_lat`, `project_lon` (±0.001°).
  2. Extract key soil properties:
     - `hydrologic_group` (A/B/C/D)
     - `infiltration_rate_in_hr` (Ksat)
     - `porosity` (available water storage)
     - `surface_texture`
  3. If `soil_override` is provided, merge override fields (override takes precedence).
  4. Calculate area-weighted average infiltration rate if multiple map units intersect the site.
- **Output:** `SoilProperties` — `{hydrologic_group: str, infiltration_rate_in_hr: float, porosity: float, map_unit_id: str, source: "NRCS" | "override"}`
- **On Failure:** Retry 2×. On final failure, use `soil_override` if provided; otherwise flag HITL checkpoint for manual soil entry.

### Step 4: Fetch USGS Elevation / Topography
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. Call USGS National Map 3DEP Elevation Point Query Service (`https://nationalmap.gov/epqs/pqs.php?x={lon}&y={lat}&units=Feet&output=json`) to retrieve site elevation.
  2. If the point query fails, fallback to USGS National Elevation Dataset (NED) WCS service for a 30m × 30m grid cell centered on project location.
  3. Use elevation data to compute slope grade (%) from nearest neighbor cells, which informs GI placement constraints and drainage direction.
- **Output:** `TopographyData` — `{elevation_ft: float, slope_pct: float, dem_resolution_m: float, source_url: str}`
- **On Failure:** Retry 2×. On final failure, use `elevation_override_ft` if provided; otherwise flag HITL checkpoint for manual elevation entry. Slope computation may be skipped with a warning.

### Step 5: Compute Runoff Volume
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Select target rainfall depth from NOAA data based on `compliance_pathway`:
     - `percentile_80` → `p80_in`
     - `percentile_95` → `p95_in`
     - `gi_lid` → `p80_in` (recommended baseline)
  2. Compute **impervious area**:  
     `impervious_area_sqft = site_area_sqft × (impervious_pct / 100.0)`
  3. Compute **runoff volume** using the Rational Method variant:  
     `runoff_volume_cuft = rainfall_depth_in × impervious_area_sqft × runoff_coefficient × (1 ft / 12 in)`  
     Simplified:  
     `runoff_volume_cuft = (rainfall_depth_in / 12) × impervious_area_sqft × runoff_coefficient`
  4. Apply climate adjustment if enabled: multiply rainfall depth by adjustment factor before computing runoff.
  5. Round to 2 decimal places.
- **Output:** `RunoffVolumeResult` — `{runoff_volume_cuft: float, rainfall_depth_in: float, impervious_area_sqft: float, runoff_coefficient: float, adjustment_factor: float}`
- **On Failure:** Not applicable (pure calculation). Log intermediate values for debugging.

### Step 6: Compute GI / LID Retention Volume
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. For each measure in `gi_measures`, compute effective retention volume:  
     `measure_volume_cuft = area_sqft × (depth_in / 12) × retention_rate`
  2. Sum across all measures:  
     `total_retention_cuft = Σ(measure_volume_cuft)`
  3. Apply evapotranspiration loss if `evapotranspiration_factor > 0`:  
     `adjusted_retention_cuft = total_retention_cuft × (1 - evapotranspiration_factor)`
  4. Generate per-measure breakdown table for reporting.
- **Output:** `RetentionVolumeResult` — `{total_retention_cuft: float, adjusted_retention_cuft: float, measure_breakdown: list[dict], evapotranspiration_factor: float}`
- **On Failure:** Not applicable (pure calculation).

### Step 7: Compliance Check
- **Type:** Calculation / Decision
- **Automated:** Yes
- **Description:**
  1. Compare `adjusted_retention_cuft` against `runoff_volume_cuft`.
  2. Determine compliance status:
     - `PASS` if `adjusted_retention_cuft >= runoff_volume_cuft`
     - `FAIL` if `adjusted_retention_cuft < runoff_volume_cuft`
  3. Compute **retention ratio**:  
     `retention_ratio = adjusted_retention_cuft / runoff_volume_cuft`
  4. For `gi_lid` pathway, additionally check that:
     - At least 2 distinct GI measure types are present (LEED v5 preference for distributed systems)
     - No single measure contributes > 60% of total retention (diversity check)
  5. Compute **design margin**:  
     `design_margin_cuft = adjusted_retention_cuft - runoff_volume_cuft`
- **Output:** `ComplianceResult` — `{status: "PASS" | "FAIL", retention_ratio: float, design_margin_cuft: float, diversity_check: bool, target_percentile: str}`
- **On Failure:** Not applicable (pure calculation).

### Step 8: HITL Checkpoint — GI Design Verification
- **Type:** Human Review
- **Automated:** No
- **Description:**
  1. Pause workflow and present a review package to the designated reviewer:
     - Summary of all GI measures with areas, depths, and retention rates
     - NRCS soil properties and infiltration rates
     - USGS elevation and slope data
     - Computed runoff vs. retention volumes with retention ratio
     - Compliance status (PASS/FAIL)
     - Any API fallback or override flags
  2. Reviewer must confirm:
     - GI design assumptions match site constraints (e.g., green roof structural load, permeable pavement subgrade suitability)
     - Soil infiltration rates are appropriate for proposed GI types
     - Slope and elevation data do not conflict with GI placement
     - All GI areas are feasible within the site plan
  3. Reviewer may:
     - Approve and proceed
     - Reject with comments → workflow returns to Step 1 or Step 6 for input revision
     - Request additional documentation (e.g., geotechnical report)
- **Output:** `HITLReviewResult` — `{approved: bool, reviewer_id: str, timestamp: datetime, comments: str, revision_requested: bool}`
- **On Failure:** If no reviewer action within SLA, escalate to project manager and pause workflow.

### Step 9: Generate Rainwater Management Report (PDF)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Use Jinja2 template (`templates/ssc3_rainwater_report.html`) to render a comprehensive PDF report containing:
     - Project metadata (name, location, site area)
     - NOAA Atlas 14 rainfall data with source URL and date accessed
     - NRCS soil properties table
     - USGS elevation and slope summary
     - Runoff volume calculation with full formula and intermediate values
     - GI / LID measure inventory table with per-measure retention volumes
     - Total retention volume and design margin
     - Compliance determination with explicit LEED pathway reference
     - Assumptions and limitations disclaimer
  2. Convert HTML → PDF via WeasyPrint or Playwright.
  3. Embed NOAA, NRCS, and USGS source data as appendix tables.
  4. Digitally stamp with workflow execution ID and timestamp.
- **Output:** `ReportPDF` — file path to generated PDF document
- **On Failure:** Retry document generation once. On final failure, generate markdown report as fallback and flag for manual PDF conversion.

### Step 10: Generate GI Sizing Calculations (XLSX)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Generate an Excel workbook (`openpyxl`) with the following sheets:
     - **Inputs** — all raw input values with units
     - **Rainfall Data** — NOAA Atlas 14 raw data and selected percentile depths
     - **Soil Data** — NRCS properties with map unit IDs
     - **Runoff Calc** — formula-based runoff calculation with intermediate steps
     - **GI Measures** — per-measure breakdown with volume formulas
     - **Compliance** — summary table with PASS/FAIL determination
     - **Notes** — assumptions, sources, and reviewer comments from HITL
  2. All calculation cells contain Excel formulas (not hardcoded values) so reviewers can audit.
- **Output:** `SizingXLSX` — file path to generated Excel workbook
- **On Failure:** Retry once. On final failure, generate CSV fallback for each sheet.

### Step 11: Generate Site Hydrology Analysis (PDF)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Generate a secondary PDF report focused on site-wide hydrology:
     - Catchment delineation based on USGS DEM data
     - Pre-development vs. post-development runoff comparison
     - Infiltration capacity map (derived from NRCS soil groups)
     - Drainage direction and potential overflow paths
     - Recommendations for additional GI if compliance is marginal
  2. Include a site schematic placeholder for the design team to overlay GI layout.
- **Output:** `HydrologyPDF` — file path to generated hydrology analysis document
- **On Failure:** Retry once. On final failure, generate markdown summary and flag for manual conversion.

### Step 12: Finalize and Persist
- **Type:** API Call / Persistence
- **Automated:** Yes
- **Description:**
  1. Persist all output documents to project-scoped blob storage (S3 / Azure Blob / GCS) with path: `projects/{project_id}/ss-c3-rainwater/{timestamp}/`.
  2. Write a `manifest.json` containing:
     - workflow execution ID
     - all input values (sanitized)
     - all API response metadata (NOAA, NRCS, USGS URLs and timestamps)
     - calculation results (runoff, retention, compliance)
     - HITL review result
     - output document URIs
     - audit hash (SHA-256 of manifest contents)
  3. Update project record in LEED database with credit status and document references.
  4. Return final response to caller.
- **Output:** `FinalResult` — `{project_id: str, credit_code: "SSc3", compliance_status: str, document_uris: dict, manifest_uri: str, execution_id: str}`
- **On Failure:** Retry persistence 2×. On final failure, queue for retry via background job and return partial result with in-memory document buffers.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 8: GI Design Verification | LEED AP / Civil Engineer / Stormwater Designer | 48 hours | Verify GI design assumptions match site constraints (structural loads, soil infiltration suitability, slope stability, utility conflicts). Confirm all GI surface areas and depths are constructible. Review NRCS soil group compatibility with proposed GI types. Check retention rate assumptions against manufacturer data or local performance studies. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| NOAA Atlas 14 PFDS | Rainfall depth-duration-frequency for 80th/95th percentile | United States (50 states + territories) | USGS GHCN daily precipitation historical records | No rate limit (public service) |
| NRCS Soil Survey (SDM Access) | Soil hydrologic group, infiltration rate, porosity | United States (50 states + territories) | NRCS Web Soil Survey manual download; `soil_override` input field | ~100 req/min (no auth required) |
| USGS National Map EPQS | Site elevation and DEM data | United States (50 states + territories) | USGS NED WCS tile service; `elevation_override_ft` input field | No rate limit (public service) |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | Full NOAA Atlas 14, NRCS, and USGS coverage |
| Puerto Rico / US Virgin Islands | Available | NOAA Atlas 14 covers PR/USVI; NRCS soils and USGS DEM available |
| Guam / American Samoa / Northern Mariana Islands | Limited | NOAA Atlas 14 available for some Pacific islands; NRCS soils may be sparse |
| Canada | Limited | NOAA Atlas 14 not available; must use Environment Canada IDF curves via manual HITL |
| International (non-US/Canada) | Unavailable | Requires local DDF/IDF rainfall data, local soil surveys, and local DEM; full HITL fallback |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| NOAA PFDS timeout / 5xx | Log error, wait 2s, retry with exponential backoff (max 3 retries) | No (auto-retry first) | 3 |
| NOAA returns null/no data for lat/lon | Flag for HITL; use USGS GHCN fallback if available | Yes | 0 |
| NRCS SDM timeout / 5xx | Retry 2×, then use `soil_override` or HITL | Yes (on final failure) | 2 |
| NCRS bounding box returns no map units | Flag for HITL; request manual soil properties | Yes | 0 |
| USGS EPQS timeout / 5xx | Retry 2×, then use USGS NED WCS tile service | No (auto-fallback first) | 2 |
| USGS elevation data missing | Use `elevation_override_ft` or HITL | Yes (if no override) | 0 |
| GI retention < runoff (FAIL) | Continue to HITL checkpoint; do not fail workflow | No (intended outcome for design iteration) | N/A |
| PDF generation failure (WeasyPrint) | Retry once with Playwright; fallback to markdown | Yes (on final failure) | 1 |
| XLSX generation failure (openpyxl) | Retry once; fallback to CSV sheets | Yes (on final failure) | 1 |
| Blob storage persistence failure | Retry 2×; queue background job; return in-memory buffers | Yes (on final failure) | 2 |
| Invalid `compliance_pathway` | Terminate workflow immediately; return validation error | Yes | 0 |
| `gi_measures` empty for `gi_lid` pathway | Terminate workflow; require at least one GI measure | Yes | 0 |
| `impervious_pct` > 100 | Terminate workflow; return field-level validation error | No | 0 |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Rainwater Management Report | PDF | Comprehensive credit submission document with all calculations, data sources, and compliance determination |
| GI Sizing Calculations | XLSX | Audit-ready Excel workbook with formula-based calculations across all inputs, rainfall, soil, runoff, and retention |
| Site Hydrology Analysis | PDF | Pre/post development hydrology comparison with catchment delineation and infiltration capacity mapping |
| Manifest | JSON | Machine-readable audit trail of all inputs, API calls, calculations, HITL review, and output document URIs |

## Testing
```bash
# Run all unit and integration tests for SSc3
python -m pytest skills/leed-ss-c3-rainwater/tests/ -v

# Specific test categories
python -m pytest skills/leed-ss-c3-rainwater/tests/test_validation.py -v
python -m pytest skills/leed-ss-c3-rainwater/tests/test_noaa_api.py -v
python -m pytest skills/leed-ss-c3-rainwater/tests/test_nrcs_api.py -v
python -m pytest skills/leed-ss-c3-rainwater/tests/test_usgs_api.py -v
python -m pytest skills/leed-ss-c3-rainwater/tests/test_calculations.py -v
python -m pytest skills/leed-ss-c3-rainwater/tests/test_document_generation.py -v
python -m pytest skills/leed-ss-c3-rainwater/tests/test_hitl_checkpoint.py -v
python -m pytest skills/leed-ss-c3-rainwater/tests/test_integration.py -v
```

## Example Usage (OpenAI Agents SDK + Restate)
```python
from leed_platform.skills import SSc3RainwaterSkill

skill = SSc3RainwaterSkill(
    project_id="leed-proj-2024-001",
    inputs={
        "project_lat": 39.7392,
        "project_lon": -104.9903,
        "site_area_sqft": 50000.0,
        "impervious_pct": 72.5,
        "compliance_pathway": "percentile_95",
        "gi_measures": [
            {
                "type": "bioswale",
                "area_sqft": 1200.0,
                "depth_in": 18.0,
                "retention_rate": 0.85
            },
            {
                "type": "permeable_pavement",
                "area_sqft": 3500.0,
                "depth_in": 6.0,
                "retention_rate": 0.70
            },
            {
                "type": "rain_garden",
                "area_sqft": 800.0,
                "depth_in": 12.0,
                "retention_rate": 0.90
            }
        ],
        "runoff_coefficient": 0.95,
        "evapotranspiration_factor": 0.10,
        "include_climate_change_adjustment": True,
        "project_name": "Denver Office Complex Phase 2"
    }
)
result = await skill.execute()

# result structure:
# {
#   "project_id": "leed-proj-2024-001",
#   "credit_code": "SSc3",
#   "compliance_status": "PASS",
#   "retention_ratio": 1.08,
#   "design_margin_cuft": 420.5,
#   "document_uris": {
#     "report_pdf": "s3://.../ss-c3-rainwater/2024-06-15T10-30-00/rainwater_management_report.pdf",
#     "sizing_xlsx": "s3://.../ss-c3-rainwater/2024-06-15T10-30-00/gi_sizing_calculations.xlsx",
#     "hydrology_pdf": "s3://.../ss-c3-rainwater/2024-06-15T10-30-00/site_hydrology_analysis.pdf",
#     "manifest_json": "s3://.../ss-c3-rainwater/2024-06-15T10-30-00/manifest.json"
#   },
#   "execution_id": "exec-abc123",
#   "hitl_review": {
#     "approved": True,
#     "reviewer_id": "leed-ap-jdoe",
#     "timestamp": "2024-06-15T14:22:00Z",
#     "comments": "GI sizing verified against civil drawings. Approved."
#   }
# }
```

## Platform Workflow (OpenAI Agents SDK + Restate)
```python
from langgraph.graph import StateGraph, END
from leed_platform.state import LEEDState
from leed_platform.nodes import (
    validate_inputs,
    fetch_noaa_data,
    fetch_nrcs_data,
    fetch_usgs_elevation,
    compute_runoff_volume,
    compute_retention_volume,
    check_compliance,
    human_review_checkpoint,
    generate_report_pdf,
    generate_sizing_xlsx,
    generate_hydrology_pdf,
    persist_outputs
)
from leed_platform.edges import route_after_hitl

# Define the state graph
workflow = StateGraph(LEEDState)

# Add nodes
workflow.add_node("validate", validate_inputs)
workflow.add_node("fetch_noaa", fetch_noaa_data)
workflow.add_node("fetch_nrcs", fetch_nrcs_data)
workflow.add_node("fetch_usgs", fetch_usgs_elevation)
workflow.add_node("compute_runoff", compute_runoff_volume)
workflow.add_node("compute_retention", compute_retention_volume)
workflow.add_node("check_compliance", check_compliance)
workflow.add_node("hitl_review", human_review_checkpoint)
workflow.add_node("generate_report", generate_report_pdf)
workflow.add_node("generate_xlsx", generate_sizing_xlsx)
workflow.add_node("generate_hydrology", generate_hydrology_pdf)
workflow.add_node("persist", persist_outputs)

# Define edges
workflow.set_entry_point("validate")
workflow.add_edge("validate", "fetch_noaa")
workflow.add_edge("validate", "fetch_nrcs")
workflow.add_edge("validate", "fetch_usgs")
workflow.add_edge("fetch_noaa", "compute_runoff")
workflow.add_edge("fetch_nrcs", "compute_retention")
workflow.add_edge("fetch_usgs", "compute_retention")
workflow.add_edge("compute_runoff", "check_compliance")
workflow.add_edge("compute_retention", "check_compliance")
workflow.add_edge("check_compliance", "hitl_review")

# HITL routing: approved -> generate documents; rejected -> loop back
workflow.add_conditional_edges(
    "hitl_review",
    route_after_hitl,
    {
        "approved": "generate_report",
        "rejected": "validate",  # Loop back for revision
        "escalated": END
    }
)

workflow.add_edge("generate_report", "generate_xlsx")
workflow.add_edge("generate_xlsx", "generate_hydrology")
workflow.add_edge("generate_hydrology", "persist")
workflow.add_edge("persist", END)

# Compile the graph
app = workflow.compile()

# Execution
# result = await app.ainvoke(initial_state)
```

## Calculation Reference

### Runoff Volume Formula
```
Impervious Area (sq ft) = Site Area (sq ft) × (Impervious % / 100)

Runoff Volume (cu ft) = (Rainfall Depth (in) / 12) × Impervious Area (sq ft) × Runoff Coefficient

Where:
  - Rainfall Depth = p80_in or p95_in from NOAA Atlas 14 (with optional climate adjustment)
  - Runoff Coefficient default = 0.95 (impervious asphalt/concrete)
  - Adjustment: Rainfall Depth = Raw Depth × Climate Adjustment Factor (if enabled)
```

### Retention Volume Formula
```
Per-Measure Volume (cu ft) = GI Area (sq ft) × (GI Depth (in) / 12) × Retention Rate

Total Retention (cu ft) = Σ(Per-Measure Volume)

Adjusted Retention (cu ft) = Total Retention × (1 - Evapotranspiration Factor)

Where:
  - Retention Rate = fraction of stormwater retained (0.0–1.0)
  - Evapotranspiration Factor default = 0.0 (conservative)
```

### Compliance Check
```
Status = "PASS" if Adjusted Retention >= Runoff Volume else "FAIL"

Retention Ratio = Adjusted Retention / Runoff Volume

Design Margin (cu ft) = Adjusted Retention - Runoff Volume
```

### GI Diversity Check (GI/LID Pathway)
```
Diversity Check = (
    (Count of distinct GI types >= 2) AND
    (Max single-measure contribution <= 60% of Total Retention)
)
```

## Data Quality & Audit
- All NOAA, NRCS, and USGS API responses are stored as raw JSON/XML in blob storage.
- Calculation steps are reproducible via the XLSX workbook (live formulas, not values).
- The manifest.json includes SHA-256 hashes of all source data and generated documents.
- HITL review actions are timestamped, attributed to reviewer ID, and immutable once submitted.
- Climate adjustment factors and their sources are logged explicitly for third-party verification.

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-06 | Initial production release for LEED v5 SSc3 |
