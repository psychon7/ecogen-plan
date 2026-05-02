# Technical Stack Reference
## Ecogen LEED v5 Automation Platform — Implementation Details

**Source:** Kimi_Agent_LEED v5 Credit Automation/tech_impl_sec01–04.md  
**Purpose:** Single reference for all implementation specifics; read alongside MASTER_PLAN.md

---

## 1. Core Stack Decisions

### 1.1 Why Deer-Flow v2.0

Deer-Flow (ByteDance open-source, 60k+ GitHub stars) provides:
- LangGraph durable workflows with PostgreSQL checkpoint persistence out of the box
- Skill-based modular architecture (one skill = one container)
- Built-in HITL pause/resume hooks
- Reduces build from 40–48 weeks (from-scratch) to 10 weeks
- 70–80% of required infrastructure pre-built; 20–30% LEED-specific on top

**Interface boundary:** Ecogen wraps Deer-Flow behind a `DurableOrchestrator` abstraction (`skills/durable_workflow.py`). Direct Deer-Flow API calls must not appear in skill code — use the orchestrator interface only.

### 1.2 Technology Versions

| Technology | Version | Notes |
|-----------|---------|-------|
| Python | 3.12 | Required for skills and backend |
| FastAPI | Latest stable | API gateway |
| LangGraph | Latest stable | Workflow state graphs |
| PostgreSQL | 15 + PostGIS | State, audit, geo queries |
| Redis | 7, Cluster mode | Cache, pub/sub, token bucket |
| React | 18 | Frontend |
| TypeScript | 5+ | Frontend type safety |
| Vite | Latest | Frontend build |
| Docker | Latest | Skill containers |
| Kubernetes | 1.28+ | Production orchestration |

---

## 2. Data Models

### 2.1 LEEDProjectState (Shared Across All Skills)

```python
class LEEDProjectState(TypedDict):
    project_id: str
    credit_code: str
    current_step: int
    inputs: dict                    # Validated user inputs
    api_data: dict                  # Fetched external data
    calculations: dict              # Computed values
    documents: dict[str, str]       # credit_code -> document path
    hitl_task_id: Optional[str]
    hitl_result: Optional[dict]     # {action, comments, reviewer_id, return_to_step}
    revision_count: int
    validation_errors: list
    confidence_score: float         # 0.0–1.0
    status: Literal["pending", "in_progress", "awaiting_review",
                    "approved", "rejected", "submitted", "error"]
    submitted_to_usgbc: bool
    usgbc_submission_id: Optional[str]
```

### 2.2 SkillManifest (Pydantic)

```python
class SkillManifest(BaseModel):
    name: str
    version: str                        # Semantic versioning
    credit_code: str                    # Pattern: [A-Z]{2}[pc]\d+
    credit_name: str
    points: Literal["Required"] | int
    automation_level: float             # 0–100%
    complexity: Literal["Low", "Medium", "High"]
    hitl_required: bool
    hitl_checkpoints: list[HITLCheckpoint]
    api_dependencies: list[APIDependency]
    regional_availability: dict[str, Literal["Available", "Limited", "Unavailable"]]
    docker_image: str
    entry_point: str
    resource_requirements: ResourceRequirements
```

### 2.3 CalculationRecord (Audit Trail)

```python
class CalculationRecord:
    calculation_id: str                 # UUID v4
    skill_name: str
    skill_version: str
    formula_hash: str                   # SHA-256 of formula source
    inputs_hash: str                    # SHA-256 of serialized inputs
    parameters: dict                    # All constants, thresholds used
    api_sources: list                   # [{"api", "version", "retrieved_at"}]
    output: dict
    executed_at: datetime
    sandbox_id: str                     # Container ID for reproduction
```

### 2.4 HITLTask

```typescript
interface HITLTask {
  id: string;
  project_id: string;
  credit_code: string;
  reviewer: { user_id: string; name: string; email: string; slack_id: string; credential: string };
  documents: Document[];
  checklist: ChecklistItem[];          // Required/optional per credit
  comments: Comment[];                 // Threaded, @mention support
  sla: { assigned_at: Date; expires_at: Date; hours_remaining: number };
  status: "pending" | "approved" | "rejected" | "changes_requested";
}
```

---

## 3. API Integration Layer

### 3.1 Unified HTTP Client

```python
class LeedApiClient:
    # httpx.AsyncClient with HTTP/2 and connection pooling
    # Timeouts: connect 5s, read 30s, write 10s
    # Request signing: HMAC-SHA256 for internal APIs

    @retry(stop_after_attempt(4), wait_exponential(multiplier=1, min=2, max=60))
    @circuit(failure_threshold=5, recovery_timeout=60)
    async def fetch(endpoint, params, cache_key=None, ttl=3600):
        # 1. Check Redis cache
        # 2. Execute request with auth headers
        # 3. Validate response schema
        # 4. Write to cache with TTL
        # 5. Return data
```

### 3.2 Authentication Methods by API

| Auth Type | APIs | Implementation |
|-----------|------|----------------|
| Public | EPA eGRID, NOAA, USGS | No auth needed |
| API Key (header) | NREL, Census, NOAA paid | `X-API-Key` + Vault storage |
| OAuth 2.0 | USGBC Arc, Procore, Green Button | Auth code + PKCE; 1h access, 30d refresh |
| Certificate/mTLS | OpenADR 2.0b, BACnet | X.509 v3 RSA 2048-bit, Vault PKI |
| Bearer Token | EC3, GBCI | `Authorization: Bearer {token}` |

### 3.3 Caching Strategy (Redis Cluster)

| Tier | Storage | TTL | Use Case |
|------|---------|-----|---------|
| L1 Hot | Redis in-memory | 1 hour | Real-time lookups (weather, AQI) |
| L2 Warm | Redis AOF-persisted | 1–7 days | Semi-static (grid factors, EPDs) |
| L3 Cold | PostgreSQL JSONB | 7 years | Archived snapshots for audit |

### 3.4 Data Freshness Requirements

| Data Type | Cache TTL | Fallback |
|-----------|-----------|---------|
| Grid emission factors (eGRID) | 1 year | Previous year eGRID |
| EPD embodied carbon (EC3) | 24 hours | EC3 weekly export |
| Weather / climate (NOAA) | 1 hour | Climate normals (static) |
| Solar resource (NREL NSRDB) | 30 days | Regional averages |
| Product certifications | 7–90 days | Previous certification period |
| Demographic data (ACS) | 1 year | Decennial Census |

### 3.5 Fallback Hierarchy (Per API)

```
Live API → Redis cache (stale) → Static snapshot → Synthetic estimate → HITL manual entry
```

Circuit breaker: 5 failures in 60s → open state. Auto-recovery after timeout. Skills must declare fallback behavior in SKILL.md.

---

## 4. Calculation Algorithms

### 4.1 Five-Stage Calculation Pipeline

1. **Data Ingestion** — API calls with auto-retry and fallback
2. **Validation Gate** — schema validation, range checks, freshness verification
3. **Transformation** — raw API response → normalized inputs via mapping tables
4. **Execution** — deterministic calculation using pre-validated formula templates
5. **Output Formatting** — LEED-compliant output with units, precision, source citations

### 4.2 Calculation Types & Complexity

| Type | Credits Using It | Complexity | Validation Rule |
|------|-----------------|-----------|-----------------|
| Carbon/GWP | IPp3, EAp5, EAc7, MRp2, MRc2 | Medium-High | Cross-check IPCC AR6 Table 7.15 |
| Database verification | PRc2, SSc6, SSc5 | Low | Certification expiry within project period |
| Area/volume | MRp2, SSc5, SSc3 | Low-Medium | BIM-to-spec reconciliation ±5% tolerance |
| % reduction / improvement | WEp2, WEc2, EAc3, EAp2 | Mixed | WE calculations are deterministic; EAp2/EAc3 parse completed model outputs and require energy modeler review |
| Water / fixture flow | WEp2, WEc2 | Medium | Fixture flow rates ≤ WaterSense limits |
| Energy / EUI | EAp1, EAp2, EAc3 | High | ±10% of measured for existing buildings |
| GIS / spatial overlap | LTc1, LTc3, SSc3 | Medium-High | Boundary must use project site polygon |

### 4.3 Dependency Resolution (Topological Sort)

Credit skills that depend on other skills' outputs use Kahn's algorithm:

```python
def resolve_execution_order(skills: list[str], dependencies: dict) -> list[str]:
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
        for dep in adj[skill]:
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)
    if len(result) != len(skills):
        raise ValueError("Circular dependency detected")
    return result
```

**Known dependency chain:** IPp3 ← EAp1 + EAp5 + MRp2. These must complete before IPp3 can start.

### 4.4 Confidence Scoring Formula

```python
def compute_confidence(section: DocumentSection) -> float:
    factors = {
        "source_citation_density": len(section.citations) / max(len(section.sentences), 1),
        "calculation_verification": float(section.has_calculated_values
                                          and section.calculation_checksum_valid),
        "reference_guide_alignment": rag_similarity(section.text, section.requirement_id),
        "historical_accuracy": 1.0 - historical_error_rate(section.skill_name),
        "input_completeness": section.input_completeness_score,
    }
    weights = {
        "source_citation_density": 0.25,
        "calculation_verification": 0.30,
        "reference_guide_alignment": 0.25,
        "historical_accuracy": 0.10,
        "input_completeness": 0.10,
    }
    score = sum(factors[k] * weights[k] for k in factors)
    # Floor rule: any critical component < 0.70 → whole package is Tier C
    critical_components = ["calculation_verification", "reference_guide_alignment"]
    if any(factors[k] < 0.70 for k in critical_components):
        score = min(score, 0.74)  # Force into Tier C
    return score
```

### 4.5 Optimistic Locking for Parallel Skills

When multiple skills execute in parallel and write to shared `LEEDProjectState`:
- Each skill read receives a state version number
- Writes accepted only if version unchanged since last read
- Conflict → skill retries after re-reading latest state
- Prevents collision when multiple HITL checkpoints resolve simultaneously

---

## 5. Document Generation Pipeline

All skills use the same pipeline:

```
Jinja2 template
    ↓ (context dict: calculations, api_data, project_info)
Rendered HTML
    ↓ WeasyPrint (for PDF)  |  openpyxl (for XLSX)  |  python-docx (for DOCX)
Final document
    ↓ MD5 checksum
Stored in S3/MinIO with version tag
    ↓
Audit manifest JSON (filename, checksum, generated_at, skill_version, inputs_hash)
```

**Template location:** `skills/<slug>/templates/` (one Jinja2 template per output document)  
**Rendering engine:**
- PDF: WeasyPrint (HTML→PDF) or ReportLab (complex charts)
- XLSX: openpyxl with formulas + conditional formatting intact
- DOCX: python-docx from `.docx` base template

---

## 6. Infrastructure Architecture

### 6.1 Deployment Topology

```
┌─────────────────────────────────────────────────────────────────────┐
│                  ECOGEN LEED AUTOMATION PLATFORM                     │
├─────────────────────────────────────────────────────────────────────┤
│  FRONTEND: React 18 + TypeScript — CDN + S3 static hosting          │
│  API GATEWAY: FastAPI + Uvicorn — 2–20 pods HPA, 200ms p99          │
│  WORKFLOW ENGINE: LangGraph Server (stateful, affinity routing)      │
│  SKILL CONTAINERS: Docker per credit (warm standby pools)            │
│  PERSISTENCE: PostgreSQL 15 (master + 2 replicas)                   │
│  CACHE: Redis 7 Cluster (6 nodes)                                   │
│  DOCUMENT STORE: S3/MinIO (versioned, AES-256)                       │
│  SECRETS: HashiCorp Vault HA (3-node, auto-unseal)                  │
│  MESSAGING: Redis Streams / RabbitMQ (<1s delivery)                 │
│  MONITORING: Prometheus + Grafana + PagerDuty                        │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Scaling Strategy

| Component | Method | Metric | Target |
|-----------|--------|--------|--------|
| Frontend | CDN + S3 | Concurrent users | Unlimited (static) |
| API Gateway | K8s HPA | CPU/memory | 70% threshold |
| Workflow Engine | Stateful affinity routing | Project throughput | 100 projects/day |
| Skill Containers | Per-credit warm pool | Concurrency per skill | 2–10 |
| PostgreSQL | Read replicas | Query load | 5,000 ops/sec |
| Redis | Cluster mode | Memory utilization | 80% threshold |

### 6.3 Security Controls

| Control | Implementation | Standard |
|---------|---------------|---------|
| API Key Management | HashiCorp Vault, 90–180 day rotation | SOC 2 Type II |
| Encryption in Transit | TLS 1.3, HTTPS only | NIST SP 800-52B |
| Encryption at Rest | AES-256 (PostgreSQL + S3) | FIPS 140-2 |
| PII Handling | SHA-256 hashing of lat/lon; Census tract anonymization | GDPR |
| Audit Trails | PostgreSQL with 7-year retention, cryptographic signing | LEED documentation requirements |
| HITL Permissions | RBAC per project; SSO via SAML 2.0 | SOC 2 / GDPR |
| Backup & Recovery | PITR (7 days) PostgreSQL; cross-region S3 replication | RPO < 1min / RTO < 4hrs |

---

## 7. Quality Assurance

### 7.1 Four-Layer QA

1. **Automated Code Testing** (pytest, responses, Playwright)
   - Unit: 90%+ coverage
   - Integration: 100% of skills with mocked APIs
   - E2E: Full workflow per skill
   - Contract tests: Live API schema validation (nightly)

2. **LEED Compliance Validation**
   - RAG over LEED v5 reference guide (vector store)
   - Requirement traceability matrix per skill
   - Automated cross-reference checking for related credits
   - LEED v5 addenda trigger regression tests

3. **Confidence Scoring** (0.0–1.0 per document section)
   - Green ≥ 0.95: Lightweight named review; no auto-approval for compliance-critical packages
   - Yellow 0.85–0.94: Required HITL (expedited SLA)
   - Orange 0.70–0.84: Required HITL (extended SLA, senior reviewer)
   - Red < 0.70: Mandatory HITL, blocking

4. **Document Quality Scoring** (automated)
   - Completeness 25%: Schema validation
   - Accuracy 30%: Calculation re-verification
   - Citations 20%: Citation density + source validity
   - Readability 10%: Flesch-Kincaid < 14
   - Formatting 15%: PDF/A validation + accessibility

### 7.2 Audit Package (Per Credit Submission)

```
audit-package-{project_id}-{credit_code}.zip
├── calculation/    — formula source, inputs, outputs, versioning
├── data_sources/   — API responses (API keys redacted), static references
├── documents/      — generated PDF, HTML template
├── hitl/           — review record, reviewer credentials, comments
├── workflow/       — state graph history, execution log
└── signatures/     — cryptographic signatures (SHA-256)
```

7-year retention required for GBCI compliance audits.

---

## 8. HITL Notification & Escalation

### 8.1 Notification Channels

| Channel | Use Case | Latency | Escalation |
|---------|----------|---------|-----------|
| Slack (primary) | LEED consultants | Real-time (WebSocket) | Auto-escalate to email @ 50% SLA |
| Email (fallback) | External reviewers | ~60s polling | Auto-escalate to manager @ 90% SLA |
| Web UI (complex) | Multi-credit reviews | Real-time (SSE) | In-app alert + Slack ping |
| SMS (break-glass) | Final escalation only | Near real-time | None (final channel) |

### 8.2 Review Actions

| Action | Workflow Effect | Re-engagement |
|--------|----------------|--------------|
| Approve | Resume to next node; documents locked | None |
| Request Changes | Rewind to `return_to_step`; notes attached | Auto re-execution + re-review |
| Reject | Credit → "needs_manual"; project lead notified | Project lead must re-initiate |
| Escalate | Reassign to different reviewer; reset SLA | New reviewer gets full context |

### 8.3 Review Dashboard Components

- **Document Preview:** react-pdf (PDF), ag-grid-react (Excel), leaflet (maps)
- **Checklist:** Custom React + formik, auto-save, progress bar
- **Comment Thread:** Real-time SSE, @mentions, markdown support
- **SLA Countdown:** Color-coded timer (green >50%, yellow <50%, red <10%)
- **Confidence Badges:** Per-section (Green >90%, Yellow 70–90%, Red <70%)
