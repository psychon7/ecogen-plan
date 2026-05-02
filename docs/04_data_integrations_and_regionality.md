# Data Integrations And Regionality

## Integration Strategy

External data is useful only when it is licensed, reachable, fresh, regionally applicable, and traceable. Every integration must be modeled as a source with verification status, region, auth method, rate limit, cache policy, fallback, and owner.

## Source Classes

| Class | Examples | Use | Risk |
|-------|----------|-----|------|
| Government APIs | EPA eGRID, NOAA, FEMA, USGS, Census, NRCS | Climate, emissions, hazards, demographics, soils | Often US-only |
| Industry databases | EC3, EPD registries, AHRI, CRRC, GBCI | Materials, products, credentials, refrigerants | Access and terms vary |
| Commercial APIs | Walk Score, Google Maps, ArcGIS, One Click LCA | Transit, location, GIS, LCA | Paid, rate-limited, contract-dependent |
| Design software APIs | Revit, Autodesk Platform Services, EnergyPlus/eppy, IES VE | BIM, CAD, geometry, model output | Specialized files and licenses |
| Static datasets | IPCC factors, ASHRAE tables, LEED reference tables, cached product data | Formulas and fallback values | Must track version/addenda |
| User-provided evidence | Schedules, cut sheets, models, drawings, manual entries | Project-specific truth | Requires confidence scoring and review |

## Required Source Metadata

Each source definition should store:

- Source name, owner, URL, and contact.
- Source type and supported credits.
- Auth method and credential storage path.
- Regions covered and unsupported regions.
- Rate limit, retry, timeout, and cache TTL.
- Data freshness expectation and last verified date.
- Fallback source or manual-entry workflow.
- Legal/commercial status: free, registration, paid, partnership, unknown.
- Evidence locator format for audit trail.

## Regional Availability Model

| Status | Meaning | UI Behavior |
|--------|---------|-------------|
| Full | Required sources available for the region and credit | Show as automatable with standard HITL |
| Limited | Some sources available, lower quality, manual fields likely | Show warning and assisted mode |
| Manual | Automation can calculate/generate after human-supplied data | Show manual data checklist |
| Unavailable | Required data or local expertise missing | Hide or require admin override |

## Regional Notes

| Region | Notes |
|--------|-------|
| United States | Strongest coverage for FEMA, EPA, NOAA, USGS, Census, eGRID, WaterSense, many product databases |
| Canada | Good professional ecosystem; some US data not applicable; provincial and federal substitutions required |
| UK/EU | Strong material and energy data in places; replace Census/EJ/FEMA/eGRID with Eurostat, EEA, Copernicus, ENTSO-E, national datasets |
| Australia/NZ | Use BOM, AEMO/NZEI, WELS/WaterMark, EPD Australasia where applicable |
| Other regions | Expect manual data collection, static factors, local consultant validation, and lower automation |

## Integration Quality Gates

Before a source can be used in an automated skill:

1. Verify access method and terms.
2. Write a typed client or import parser.
3. Add mocked API tests for success, timeout, 429, 500, malformed data, and auth failure.
4. Add a freshness policy and stale-data warning.
5. Add fallback behavior and HITL escalation.
6. Record raw response snapshot or source locator in the audit trail.

## Resilience Contract

Every production API client must define:

| Control | Requirement |
|---------|-------------|
| Rate limiting | Redis token bucket per source and credential |
| Caching | Source-specific TTL plus versioned keys and stale-data warnings |
| Circuit breaker | Closed, open, half-open states with source health events |
| Fallback hierarchy | Primary API, verified cache/static source, then HITL/manual data entry |
| Observability | Latency, error rate, retry count, cache hit rate, stale data, auth failure |
| Evidence | Raw response hash or locator attached to each derived data point |

## High-Risk Assumptions To Verify

- USGBC Arc write API access, schema, permissions, and terms.
- GBCI credential directory API availability.
- EC3 commercial API terms and production rate limits.
- Walk Score commercial access and regional coverage.
- Product databases such as AHRI, CRRC, WaterSense, ENERGY STAR, EPD, HPD, GREENGUARD, and FloorScore.
- Any Deer-Flow built-in connector claims from older research.
