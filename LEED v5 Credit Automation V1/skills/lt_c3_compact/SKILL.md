---
name: leed-lt-c3-compact-connected
version: 1.0.0
author: LEED Automation Platform
description: Automate LTc3 Compact and Connected Development credit calculation and documentation.
---

## Metadata
- **Credit Code:** LTc3
- **Credit Name:** Compact and Connected Development
- **Points:** Up to 6 points
- **Automation Level:** 88.0%
- **Complexity:** Low
- **Primary Data Source:** Walk Score API, GTFS feeds, US Census Bureau API, Google Maps Platform
- **HITL Required:** Yes

## Purpose
Automate the evaluation of project site density, walkability, transit access, and mixed-use context to determine points under LEED v5 LTc3 by aggregating data from Walk Score, GTFS feeds, US Census, and Google Maps, culminating in a points calculation and review-ready PDF/XLSX documentation package.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `project_address` | string | User input | Non-empty, validated via geocoding |
| `gross_floor_area` | number (sq ft / sq m) | User input | > 0, numeric, unit specified |
| `site_area` | number (acres / ha) | User input | > 0, numeric, unit specified |
| `unit_system` | enum ("imperial" \| "metric") | User input | Must be provided; all inputs normalized to metric internally |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `walk_score_api_key` | string | Env var `WALK_SCORE_API_KEY` | Overrides environment variable if provided |
| `google_maps_api_key` | string | Env var `GOOGLE_MAPS_API_KEY` | Overrides environment variable if provided |
| `census_api_key` | string | Env var `CENSUS_API_KEY` | Overrides environment variable if provided |
| `gtfs_feed_url` | string | Auto-resolved via mobilitydatabase.org | Custom GTFS feed URL if auto-resolution fails |
| `building_type` | string | "general" | LEED building type; influences density thresholds |
| `hitl_timeout_hours` | integer | 48 | SLA hours for human-in-the-loop review checkpoint |
| `radius_miles` | number | 0.5 | Distance radius (in miles) for transit stop and diverse-use queries |
| `output_dir` | string | "./output" | Directory for generated documents |

## Workflow Steps (Durable)

### Step 1: Geocode and Normalize Address
- **Type:** Validation / API Call
- **Automated:** Yes
- **Description:** Geocode `project_address` using Google Maps Geocoding API (`https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}`). Extract latitude, longitude, formatted address, and place_id. Normalize all area inputs (GFA and site area) to metric (square meters for GFA, hectares for site area) using conversion constants (1 sq ft = 0.092903 sq m; 1 acre = 0.404686 ha).
- **Output:** `{ lat, lng, formatted_address, place_id, gfa_sq_m, site_area_ha, unit_system }`
- **On Failure:** Retry geocoding up to 3 times with exponential backoff. If persistent, trigger human notification via `notify_human` and halt workflow.

### Step 2: Resolve GTFS Feed for Region
- **Type:** API Call
- **Automated:** Yes
- **Description:** Query the Mobility Database Catalog API (`https://api.mobilitydatabase.org/v1/gtfs_feeds`) using project lat/lng with a bounding box or nearest-search radius (default 25 km). Select the highest-quality feed matching `data_type=gtfs` with status `active`. Cache feed URL. If `gtfs_feed_url` is provided as optional input, skip auto-resolution and validate URL via HEAD request.
- **Output:** `{ gtfs_feed_url, feed_id, feed_name }`
- **On Failure:** If Mobility Database returns no active feeds, fallback to static list of known regional transit feeds (US: transitfeeds.com legacy map, Canada: GTFS-Canada, AU: TfNSW/PTV open data). If all fail, flag for human resolution.

### Step 3: Fetch Walk Score
- **Type:** API Call
- **Automated:** Yes
- **Description:** Call Walk Score API (`https://api.walkscore.com/score/v1/json/?lat={}&lon={}&wsapikey={}`). Extract `walkscore`, `transit.score`, and `bike.score` from response. Also capture `snapped_lat` and `snapped_lon` for ground-truth verification.
- **Output:** `{ walk_score, transit_score, bike_score, snapped_lat, snapped_lon, status }`
- **On Failure:** If API key invalid or rate-limited, retry after 60s. If permanent failure, fallback to Google Maps Pedestrian Access Score (custom proxy) or flag HITL for manual Walk Score entry.

### Step 4: Fetch Transit Stops and Trip Frequency from GTFS
- **Type:** API Call
- **Automated:** Yes
- **Description:** Parse the GTFS feed (zip containing `stops.txt`, `stop_times.txt`, `trips.txt`, `routes.txt`, `calendar.txt`). Filter `stops.txt` to entries within `radius_miles` (default 0.5 mile ≈ 805 m) of project lat/lng using Haversine distance formula. For each qualifying stop, join `stop_times.txt` → `trips.txt` → `routes.txt` to count unique trip arrivals per route type (bus, rail, subway, ferry) within a typical service week (Monday–Sunday from `calendar.txt`). Compute total trips per week and count of distinct transit types.
- **Output:** `{ transit_stops_within_radius, total_trips_per_week, route_types_present, gtfs_coverage_dates }`
- **On Failure:** If feed is malformed or outdated, fallback to GTFS Realtime or static schedule PDF parsing. If unsalvageable, flag HITL for manual transit data entry.

### Step 5: Query Diverse Uses via Google Places
- **Type:** API Call
- **Automated:** Yes
- **Description:** Execute multiple Google Places API Nearby Search calls (`https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={}&type={}&key={}`). Query types required by LEED v5 LTc3 diverse-use criteria: `restaurant`, `grocery_or_supermarket`, `school`, `hospital`, `pharmacy`, `bank`, `shopping_mall`, `park`, `library`, `post_office`, `place_of_worship`, `hardware_store`. Aggregate results, deduplicate by `place_id`, and classify into use categories per LEED credit requirements. Count distinct use types present within radius.
- **Output:** `{ diverse_uses_list, distinct_use_categories_count, total_places_found }`
- **On Failure:** Retry up to 2 times per type. If API quota exceeded, fallback to OpenStreetMap Overpass API (`https://overpass-api.de/api/interpreter`) with equivalent amenity queries.

### Step 6: Fetch US Census Density Data (US projects only)
- **Type:** API Call
- **Automated:** Yes
- **Description:** For projects in the US, call US Census Bureau Geocoder (`https://geocoding.geo.census.gov/geocoder/geographies/coordinates`) to obtain Census tract and block group. Then query ACS 5-Year Estimates API (`https://api.census.gov/data/2022/acs/acs5?get=B01003_001E,B25001_001E,B25024_001E&for=tract:{tract}&in=state:{state}+county:{county}&key={}`) for population and housing unit density. Compute persons per hectare and housing units per hectare for the tract.
- **Output:** `{ census_tract, population, housing_units, persons_per_ha, housing_units_per_ha }`
- **On Failure:** Skip for non-US projects. If Census API fails, retry once; on permanent failure, proceed without census benchmark (density score relies on project-specific density only).

### Step 7: Calculate Density Metric
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Compute Floor Area Ratio (FAR) equivalent: `density = gross_floor_area_sq_m / (site_area_ha * 10000)` (dimensionless ratio). Also compute persons-equivalent density if Census data available: `census_density_context = census_persons_per_ha`. Compare against LEED v5 LTc3 density thresholds (e.g., ≥0.5 FAR for 1 point, ≥1.0 for 2 points, ≥2.0 for 3 points — exact thresholds pulled from latest LEED v5 reference guide, with `building_type` adjustment).
- **Output:** `{ density_ratio, density_points, density_threshold_met, density_tier }`
- **On Failure:** If inputs invalid (zero site area), raise validation error and halt workflow.

### Step 8: Compute Walkability Score Contribution
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Map Walk Score (0–100) to LEED points. LEED v5 LTc3 walkability thresholds: Walk Score ≥70 = 1 point, ≥90 = 2 points. Store intermediate score and justification text.
- **Output:** `{ walk_points, walk_score, walk_threshold_met }`
- **On Failure:** If Walk Score unavailable and no fallback, set `walk_points = 0` with justification in output.

### Step 9: Compute Transit Access Contribution
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Map GTFS-derived transit data to LEED points. Criteria: ≥1 transit stop within 0.5 mile = 1 point. ≥10 trips per weekday (≥50/week) and ≥2 transit types = 1 additional point. If Transit Score from Walk Score ≥50, corroborate with GTFS data; if discrepancy >20%, flag for HITL.
- **Output:** `{ transit_points, stops_count, trips_per_week, transit_types_count, transit_threshold_met }`
- **On Failure:** If GTFS data incomplete, fallback to Walk Score Transit Score alone for point estimation, with disclaimer in documentation.

### Step 10: Compute Mixed-Use / Diverse Uses Contribution
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Count distinct use categories from Google Places results. LEED v5 LTc3 thresholds: ≥3 diverse use types within 0.5 mile = 1 point; ≥5 types = 2 points. Verify minimum one use from each of: retail/grocery, community service, recreation.
- **Output:** `{ mixed_use_points, distinct_categories_count, category_breakdown, mixed_use_threshold_met }`
- **On Failure:** If Google Places fails and OSM fallback also fails, set `mixed_use_points = 0` with explanation.

### Step 11: Aggregate Points and Generate Draft Report
- **Type:** Calculation / Document Generation
- **Automated:** Yes
- **Description:** Sum points across all four dimensions: `total_points = density_points + walk_points + transit_points + mixed_use_points`, capped at maximum 6 points. Generate draft PDF report using `weasyprint` or `reportlab` containing all calculations, API responses, maps, and tables. Generate XLSX workbook with raw data, formulas, and point breakdown.
- **Output:** `{ total_points, draft_pdf_path, draft_xlsx_path, credit_status }`
- **On Failure:** If document generation fails, retry with alternative engine (wkhtmltopdf). On persistent failure, save raw JSON and flag HITL.

### Step 12: HITL Review Checkpoint — Verify Density and Land Use Assumptions
- **Type:** Human Review
- **Automated:** No
- **Description:** Present reviewer with: (1) density calculation inputs and formula, (2) map overlay showing project boundary, radius circle, and detected transit stops/diverse uses, (3) list of auto-detected land use types with confidence scores, (4) option to override any assumption. Reviewer confirms or edits via web UI.
- **Output:** `{ hitl_approved: bool, reviewer_overrides: object, reviewer_notes: string }`
- **On Failure:** If SLA (`hitl_timeout_hours`, default 48h) expires without response, auto-approve with disclaimer flag and proceed. Log escalation to project manager.

### Step 13: Finalize Documents and Deliver
- **Type:** Document Generation
- **Automated:** Yes
- **Description:** Incorporate HITL reviewer overrides (if any) into calculations. Regenerate final PDF (Location Efficiency Analysis, Density and Transit Access Report) and final XLSX (Points Calculation). Stamp with version, timestamp, reviewer name, and disclaimer. Upload to document management system or S3 bucket per project config.
- **Output:** `{ final_pdf_paths: [path1, path2], final_xlsx_path, metadata }`
- **On Failure:** If upload fails, retry 3 times; on permanent failure, save locally and alert ops team.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 12: Verify Density and Land Use Assumptions | LEED Project Administrator or Sustainability Consultant | 48 hours | (1) Confirm GFA and site area values match architectural drawings. (2) Verify project boundary on map overlay is correct. (3) Review auto-detected transit stops — confirm all active routes within 0.5 mile are captured. (4) Review diverse uses list — confirm categories (retail, community, recreation) are accurate; remove false positives (e.g., closed businesses) or add missing uses. (5) Check Walk Score snapped location matches project entrance. (6) Approve or edit; add notes for GBCI reviewer if needed. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| Google Maps Geocoding | Address → lat/lng + place_id | Global | OpenStreetMap Nominatim | 50 QPS (paid tier) |
| Google Maps Places (Nearby Search) | Diverse uses within radius | Global | OpenStreetMap Overpass API | 100 QPS (paid tier) |
| Google Maps Distance Matrix | Distance validation (optional) | Global | OSRM / OpenStreetMap | 100 QPS (paid tier) |
| Walk Score API v1 | Walk, Transit, Bike scores | US, Canada, Australia | Manual entry / proxy scoring | 5 QPS (standard plan) |
| Mobility Database API v1 | GTFS feed discovery | Global (1100+ feeds) | Static regional feed registry | 100 QPS (no key required for catalog) |
| US Census Bureau Geocoder + ACS API | Tract/block group + population density | US only | Skip for non-US; manual entry if needed | 500 QPS (with key) |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Available | Full feature set: Walk Score, GTFS, Census, Google Maps all active |
| Canada | Available | Walk Score covers major metros; GTFS widely available; Census data not used |
| Australia | Available | Walk Score covers major cities; GTFS available via state transit APIs; no Census |
| Europe | Limited | GTFS excellent; Walk Score unavailable — Walk Score fallback to OSM walkability proxy; no Census |
| Asia-Pacific (excl. AU) | Limited | GTFS varies by city; Walk Score unavailable; rely on Google Places + OSM for diverse uses |
| Latin America | Limited | GTFS growing; Walk Score unavailable; Google Maps + OSM fallback |
| Middle East / Africa | Limited | GTFS sparse; Walk Score unavailable; manual HITL entry likely for transit data |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Invalid project address (geocode fails) | Halt workflow, return error | Yes (email + Slack) | 3x with backoff |
| Walk Score API rate limit | Queue for retry | No (auto-recover) | 3x at 60s intervals |
| Walk Score API key invalid | Halt, flag for credential update | Yes | 1x (no point retrying bad key) |
| GTFS feed 404 / stale | Fallback to Mobility Database search; try next feed | No | 2x per feed |
| No GTFS feeds found for region | Proceed with Walk Score Transit Score only; flag HITL | Yes (in HITL instructions) | N/A |
| Google Places quota exceeded | Fallback to OSM Overpass API | No | 2x |
| Census API failure (US only) | Skip census benchmark; proceed with project density only | No | 1x |
| Density calculation division by zero (site_area = 0) | Halt workflow, return validation error | Yes | N/A |
| Walk Score vs GTFS transit discrepancy >20% | Continue but flag in HITL checkpoint | Yes (in HITL UI) | N/A |
| Document generation engine failure | Switch to backup engine (wkhtmltopdf) | No | 2x |
| HITL SLA expired (48h) | Auto-approve with disclaimer; continue | Yes (escalation email) | N/A |
| Final upload failure | Save locally; alert ops for manual upload | Yes | 3x |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| Location Efficiency Analysis | PDF | Executive summary with project context, maps, walk score visualization, transit access map, diverse uses inventory, and points summary |
| Density and Transit Access Report | PDF | Detailed technical appendix showing all API responses, raw GTFS data tables, distance calculations, density formulas, and threshold comparisons |
| Points Calculation Workbook | XLSX | Structured workbook with input tabs, calculation tabs (density, walk, transit, mixed-use), point aggregation, and auto-generated LEED v5 forms |

## Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run unit tests for all workflow steps
python -m pytest skills/leed-lt-c3-compact/tests/

# Run integration tests (requires API keys in .env)
python -m pytest skills/leed-lt-c3-compact/tests/integration/ -m integration

# Run specific step tests
python -m pytest skills/leed-lt-c3-compact/tests/test_geocode.py
python -m pytest skills/leed-lt-c3-compact/tests/test_gtfs.py
python -m pytest skills/leed-lt-c3-compact/tests/test_calculations.py
```

## Example Usage (Deer-Flow)
```python
from deerflow.skills import CompactConnectedSkill

skill = CompactConnectedSkill(
    project_id="leed-2025-0042",
    inputs={
        "project_address": "1500 Market Street, Philadelphia, PA 19102",
        "gross_floor_area": 450000,
        "site_area": 2.5,
        "unit_system": "imperial",
        "building_type": "office",
        "hitl_timeout_hours": 48,
        "radius_miles": 0.5,
    }
)

result = await skill.execute()

# result structure:
# {
#   "total_points": 5,
#   "density_points": 2,
#   "walk_points": 1,
#   "transit_points": 1,
#   "mixed_use_points": 1,
#   "documents": {
#       "location_efficiency_pdf": "/output/leed-2025-0042_LTc3_location_efficiency.pdf",
#       "density_transit_pdf": "/output/leed-2025-0042_LTc3_density_transit.pdf",
#       "points_xlsx": "/output/leed-2025-0042_LTc3_points.xlsx"
#   },
#   "hitl_status": "approved",
#   "metadata": { ... }
# }
```

## Deer-Flow Workflow (LangGraph)
```python
from langgraph.graph import StateGraph, END
from deerflow.skills.leed_lt_c3.state import LTc3State
from deerflow.skills.leed_lt_c3.nodes import (
    geocode_address,
    resolve_gtfs_feed,
    fetch_walk_score,
    fetch_transit_data,
    query_diverse_uses,
    fetch_census_data,
    calculate_density,
    calculate_walk_points,
    calculate_transit_points,
    calculate_mixed_use_points,
    aggregate_points,
    generate_draft_reports,
    hitl_review_checkpoint,
    finalize_documents,
)
from deerflow.human_in_the_loop import create_hitl_node

workflow = StateGraph(LTc3State)

# --- Add nodes ---
workflow.add_node("geocode", geocode_address)
workflow.add_node("resolve_gtfs", resolve_gtfs_feed)
workflow.add_node("walk_score", fetch_walk_score)
workflow.add_node("transit_data", fetch_transit_data)
workflow.add_node("diverse_uses", query_diverse_uses)
workflow.add_node("census_data", fetch_census_data)
workflow.add_node("calc_density", calculate_density)
workflow.add_node("calc_walk", calculate_walk_points)
workflow.add_node("calc_transit", calculate_transit_points)
workflow.add_node("calc_mixed_use", calculate_mixed_use_points)
workflow.add_node("aggregate", aggregate_points)
workflow.add_node("draft_reports", generate_draft_reports)
workflow.add_node("hitl", hitl_review_checkpoint)
workflow.add_node("finalize", finalize_documents)

# --- Define edges ---
workflow.set_entry_point("geocode")
workflow.add_edge("geocode", "resolve_gtfs")
workflow.add_edge("geocode", "walk_score")
workflow.add_edge("geocode", "diverse_uses")
workflow.add_edge("geocode", "census_data")

# GTFS resolution enables transit data fetch
workflow.add_edge("resolve_gtfs", "transit_data")

# All data fetches feed into calculations
workflow.add_edge("walk_score", "calc_walk")
workflow.add_edge("transit_data", "calc_transit")
workflow.add_edge("diverse_uses", "calc_mixed_use")
workflow.add_edge("census_data", "calc_density")
workflow.add_edge("geocode", "calc_density")  # density uses geocoded area too

# Calculations converge at aggregation
workflow.add_edge("calc_density", "aggregate")
workflow.add_edge("calc_walk", "aggregate")
workflow.add_edge("calc_transit", "aggregate")
workflow.add_edge("calc_mixed_use", "aggregate")

# Aggregation triggers draft report generation
workflow.add_edge("aggregate", "draft_reports")

# Draft reports go to HITL
workflow.add_edge("draft_reports", "hitl")

# HITL conditional routing
workflow.add_conditional_edges(
    "hitl",
    lambda state: "finalize" if state.hitl_approved else "awaiting_human",
    {
        "finalize": "finalize",
        "awaiting_human": END,  # workflow pauses, resumed externally
    }
)

workflow.add_edge("finalize", END)

# Compile
app = workflow.compile()

# Execute
initial_state = LTc3State(
    project_id="leed-2025-0042",
    project_address="1500 Market Street, Philadelphia, PA 19102",
    gross_floor_area=450000,
    site_area=2.5,
    unit_system="imperial",
)

# For checkpoint-based resumption after HITL
config = {"configurable": {"thread_id": "leed-ltc3-0042"}}
result = await app.ainvoke(initial_state, config)
```

## Calculation Reference

### Density Calculation
```
density_ratio = gross_floor_area_sq_m / (site_area_ha * 10,000)

# LEED v5 LTc3 density thresholds (building_type = general)
# Tier 1: density_ratio >= 0.5  → 1 point
# Tier 2: density_ratio >= 1.0  → 2 points
# Tier 3: density_ratio >= 2.0  → 3 points

# Adjusted thresholds for specific building types:
# - Residential: 0.4 / 0.8 / 1.6
# - Office: 0.6 / 1.2 / 2.4
# - Mixed-use: 0.5 / 1.0 / 2.0 (default)
```

### Walk Score → Points
```
walk_points = 0
if walk_score >= 90:
    walk_points = 2
elif walk_score >= 70:
    walk_points = 1
```

### Transit Access → Points
```
transit_points = 0
if transit_stops_within_0_5_mile >= 1:
    transit_points = 1
if total_trips_per_week >= 50 and distinct_transit_types >= 2:
    transit_points = 2  # replaces the 1-point tier

# Cross-validation: if abs(walk_score_transit_score - gtfs_derived_score) > 20:
#     flag_for_hitl = True
```

### Mixed Uses → Points
```
mixed_use_points = 0
# Categories: retail/grocery, community_service, recreation, healthcare, education, etc.
distinct_categories = count_unique_categories(diverse_uses_list)

if distinct_categories >= 5:
    mixed_use_points = 2
elif distinct_categories >= 3:
    mixed_use_points = 1

# Must include at least one from: retail/grocery, community_service, recreation
required_present = check_required_categories(diverse_uses_list)
if not required_present:
    mixed_use_points = 0  # override even if count is high
```

### Total Points (capped at 6)
```
total_points = min(
    density_points + walk_points + transit_points + mixed_use_points,
    6
)
```

## Data Retention and Compliance
- All API responses cached in `~/.deerflow/cache/leed-lt-c3/{project_id}/` for 90 days
- HITL reviewer decisions logged with timestamp, reviewer ID, and override details
- Final documents retained per project document retention policy (minimum 7 years for LEED)
- No PII stored in API cache (addresses hashed with SHA-256 for cache keys)
- Census API calls respect US Census Bureau Terms of Service and data use guidelines

## Performance Benchmarks
- End-to-end automation (excluding HITL): < 120 seconds for typical project
- GTFS feed parsing: < 30 seconds for feeds up to 500 MB
- Document generation: < 20 seconds per PDF; < 5 seconds per XLSX
- HITL checkpoint: 48-hour SLA (configurable)

## Changelog
- **v1.0.0** (2025-01): Initial release. Supports Walk Score API, GTFS feeds, US Census, Google Maps. One HITL checkpoint. Target automation: 88%.
