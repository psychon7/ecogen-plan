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
