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

