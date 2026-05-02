# Ecogen — LEED v5 Credit Automation Platform
## Master Consolidated Plan

**Date:** 2026-05-02  
**Status:** Active — consolidates `docs/00–08`, Kimi analysis, and `leed-platform/` architecture  
**Authoritative source for:** automation levels, architecture, skill contracts, delivery timeline

---

## 1. Executive Summary

Ecogen automates 70–85% of LEED v5 BD+C documentation work for professional consultants. It is an **AI-assisted platform, not an autonomous agent** — every compliance-critical output requires human approval before submission.

| Metric | Value |
|--------|-------|
| Automation coverage (US projects) | 85%+ |
| Automation coverage (CA/UK/EU/AU) | 70–80% |
| Automation coverage (other regions) | 50–60% |
| Production MVP scope | 5 Kimi-aligned credit suites |
| Research-screened automation candidates (of 51) | 31 automate/assist candidates pending verification |
| Consultant hours saved per project | 94-152 hours for full verified MVP suite scope |
| Commercial value per project | $14,100-$22,800 at $150/hr for verified suite scope |
| Infrastructure cost (monthly) | $2,805–$4,505 |
| Production MVP delivery timeline | Multi-phase build; demo is not production readiness |
| 14-day demo scope | Workflow proof with a small credit set |

**What the platform does:**
- Fetches data from 36 APIs (EPA, NOAA, EC3, GBCI, FEMA, NREL, etc.)
- Runs LEED-compliant calculations with auditable formula trails
- Generates submission-ready evidence packs (PDF/XLSX/DOCX)
- Routes each output through a mandatory Human-in-the-Loop (HITL) review
- Exports directly to USGBC Arc (V2+; V1 uses manual export)

**What the platform does NOT do:**
- Interpret CAD/BIM drawings autonomously — uses AutoCAD API + human verification
- Make final compliance decisions — AI assists, humans decide
- Claim full automation for regions lacking required data APIs
- Submit to USGBC without qualified reviewer sign-off

---

## 2. Product Vision & Positioning

**Core positioning:** "AI-powered LEED documentation assistant" — NOT "automated LEED consultant."  
This distinction is critical for professional liability and consultant trust.

**Trust model — four auditable questions every output must answer:**
1. Where did this data come from? (source citation)
2. How was it transformed? (formula + version hash)
3. How confident is the system? (confidence score 0–100)
4. Who approved it? (reviewer identity + timestamp)

**Competitive moat:** Auditability trail + data network effects. Every project improves the platform's EPD database, climate risk templates, and calculation edge-case handling.

**Primary users:**
| Persona | Role | Main workflow |
|---------|------|---------------|
| Senior LEED Consultant | Credit strategy, final approval | Review HITL tasks, approve evidence packs |
| Junior Consultant | Data entry, document assembly | Upload schedules, track progress |
| Project Manager | Timeline, scope | Dashboard: status, risk, deadlines |
| Specialist Reviewer | Energy modeler / GIS / LCA | Specialist HITL tasks (48–72h SLA) |
| Building Owner | Progress visibility | Summary dashboard (read-only) |

---

## 3. Automation Strategy

### 3.1 Three-Tier Credit Classification

| Tier | Automation | Pattern | Credits |
|------|-----------|---------|---------|
| **1 - Production suites** | 70-90% draft automation | Shared data pipelines + deterministic calculations/templates + HITL | WEp2/WEc2, EAp5/EAc7, EQp1/EQp2, IPp1/IPp2, MRc3 |
| **2 - Assisted catalog** | 50-85% | Useful generated skills with explicit review, source, and regional caveats | PRc2, IPp3, MRp2, MRc2, EAp1, SSc3, SSc5, SSc6, LTc1, LTc3 |
| **3 - Output-parser only** | Assist-only | Parse completed specialist outputs; do not automate core professional work | EAp2, EAc2, EAc3, WBLCA-heavy paths |
| **Not MVP** | Variable | Physical testing, field verification, complex commissioning execution | EQc5, SSp1, commissioning execution, highly project-specific credits |

### 3.2 Regional Availability

| Region | Automation Level | Key Limitation |
|--------|-----------------|----------------|
| United States | 85–95% | Full API coverage |
| Canada | 75–80% | No eGRID; provincial grid data fragmented |
| UK / EU | 70–78% | Copernicus/EEA for climate; no FEMA equivalent |
| Australia / NZ | 70–75% | AEMO grid data; no PVWatts |
| Asia-Pacific / LatAm / MENA | 50–60% | Heavy API gaps; manual data entry required |

Use `get_available_credits(region)` to filter credits before display. Never claim full automation for a region where APIs are unavailable.

### 3.3 Confidence Scoring

| Tier | Score | HITL Requirement |
|------|-------|-----------------|
| A — High | ≥ 0.90 | Lightweight named review; no auto-approval for compliance-critical packages |
| B — Standard | 0.75–0.89 | Required HITL, expedited SLA |
| C — Comprehensive | < 0.75 | Required HITL, senior reviewer, extended SLA |

**Floor rule:** If any single critical component scores < 0.70, the entire evidence pack is downgraded to Tier C regardless of overall average.

---

## 4. Architecture

### 4.1 Multi-Agent Hierarchy

```
Lead Agent (project orchestration, credit selection, DAG scheduling)
└── Credit Agent × 16 (one per LEED credit, independent)
    ├── Data Extractor    — parse EnergyPlus, Excel, PDF, CAD via API
    ├── Calculation Engine — LEED-compliant formulas, audit trail
    ├── Report Generator   — Jinja2 → PDF/XLSX/DOCX via WeasyPrint
    └── Review Checker     — completeness, math, USGBC formatting
```

The Lead Agent resolves execution order using **Kahn's topological sort** over the credit dependency DAG. Independent credits (e.g., EAp5, WEp2, SSc5) execute in parallel; prerequisite chains (e.g., IPp3 depends on EAp1 + EAp5 + MRp2) execute sequentially.

### 4.2 Technology Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Backend | Python 3.12, FastAPI | JWT auth, rate limiting, webhook handling |
| Workflow engine | LangGraph + Deer-Flow v2.0 | Durable workflows, checkpoint persistence |
| Database | PostgreSQL 15 + PostGIS | State, audit logs, 7-year retention |
| Cache | Redis Cluster (6 nodes) | Token bucket rate limiting, API response cache |
| Task queue | Celery / RabbitMQ | Async skill execution |
| Document store | S3 / MinIO | Versioned, AES-256 encrypted |
| Frontend | React 18 + TypeScript + Vite | |
| Secrets | HashiCorp Vault | Auto-unseal via KMS, 90-day key rotation |
| Monitoring | Prometheus + Grafana + PagerDuty | 15s scrape interval |
| Containers | Docker (dev), Kubernetes (prod) | HPA on CPU/memory |

### 4.3 Durable Workflow Pattern

Every credit uses `DurableOrchestrator` (`skills/durable_workflow.py`). State is persisted to PostgreSQL after every step — workflows survive restarts, API failures, and indefinite HITL waits.

```python
@step(name="fetch_grid", retry=3, timeout=30)
async def fetch_grid_factors(context, previous_results):
    return await api.call()
```

**Workflow statuses:** `pending → running → paused (HITL) → completed | failed`

**HITL pause:** raises `WorkflowPaused`; resumes via `orchestrator.resume_after_hitl()` on human response. SLA expiry does **not** auto-approve — it escalates.

### 4.4 Skill Directory Structure

```
skills/
├── <credit_slug>/          # snake_case: ip_p3_carbon, we_p2_water_min, etc.
│   ├── SKILL.md            # Contract (see §5)
│   ├── agent.py            # LangGraph StateGraph
│   ├── calculations.py     # Deterministic formula functions
│   ├── clients.py          # API client wrappers
│   ├── schemas.py          # Pydantic input/output models
│   ├── templates/          # Jinja2 PDF/DOCX templates
│   ├── fixtures/           # Test input JSON files
│   └── tests/              # pytest: unit + integration + E2E
├── durable_workflow.py     # Resumable workflow engine
├── hitl_system.py          # HITL implementation
└── SKILL_TEMPLATE.md       # Contract template for new skills
```

---

## 5. Skill Contract Standard (SKILL.md)

Every skill must define all 21 sections of the SKILL.md contract (see `skills/SKILL_TEMPLATE.md`). Key required fields:

| Section | Required Content |
|---------|----------------|
| Metadata | credit_code, name, points, automation_level %, complexity, hitl_required |
| Inputs table | field, type, source, validation rules |
| Workflow steps | step name, type (Validation/API/Calculation/DocGen/HumanReview), inputs, outputs, retry policy |
| HITL checkpoints | reviewer_role, SLA_hours, checklist items, escalation path |
| API dependencies | api_name, purpose, regional_availability, fallback |
| Regional availability | US/CA/UK/EU/AU/Other status per API |
| Output documents | filename, format, template, LEED submission purpose |
| Test command | `python -m pytest skills/<slug>/tests/` |
| Acceptance criteria | specific pass/fail conditions |
| Evidence policy | how raw API responses are stored for audit |

**Automation level normalization** (applied when importing Kimi skills):
- Use realistic % from `EXECUTIVE_SUMMARY_REALISTIC.md`, not inflated Kimi estimates
- IPp3: use 85% (not 92.5%)
- EAc3: use 70% (not 87.7%)
- LTc1: use 80% (not 87.6%)
- Remove all direct Arc submission from V1 skills (Arc is V2)

---

## 6. HITL Framework

### 6.1 Design Rules

- Every skill has **at least one** HITL checkpoint — no skill bypasses human review for compliance outputs
- SLA expiry **never** auto-approves — it escalates to senior reviewer or moves to manual mode
- On reject: `hitl_result.return_to_step` sends the workflow back to the named step for re-execution
- Confidence tier floor rule: any critical component < 0.70 → whole package = Tier C

### 6.2 SLA Tiers

| Complexity | SLA | Reviewer | Escalation |
|-----------|-----|----------|-----------|
| Simple (1–2 docs) | 24h | Any LEED AP | Email @ 50% SLA |
| Standard (3–5 docs) | 48h | LEED AP (specialty) | Slack + email @ 50% SLA |
| Complex (>5 docs / carbon) | 72h | Senior LEED AP / PE | Slack + web UI @ 50% SLA |

### 6.3 Notification Channels

Primary: Slack (real-time WebSocket)  
Fallback: Email (60s polling)  
Complex reviews: Web UI dashboard (SSE)  
Break-glass: SMS (final escalation only)

### 6.4 HITL Task Contract

```python
HITLTask:
  id, project_id, credit_code
  reviewer: {user_id, name, email, slack_id, credential}
  documents: Document[]          # evidence pack sections
  checklist: ChecklistItem[]     # required + optional per credit
  comments: Comment[]            # threaded, @mention support
  sla: {assigned_at, expires_at, hours_remaining}
  status: pending | approved | rejected | changes_requested
```

### 6.5 Workflow State Machine

```
pending → running → paused_for_review ↔ changes_requested ↔ running → completed
                                    ↘ failed
```

`changes_requested` can loop; `failed` is terminal.

---

## 7. API & Data Strategy

### 7.1 Priority Tiers (36 APIs total)

**P0 — Week 1 (critical path):**
- EPA eGRID (grid emission factors, 2 days)
- EC3 Database (20k+ EPDs, embodied carbon, 3 days)
- USGBC Arc Platform (direct LEED submission, 5 days)

**P1 — Week 2 (~15 APIs):**
NOAA Climate, NREL PVWatts, US Census ACS, FEMA Flood Maps, EPA AQI, ENERGY STAR, Google Maps, Green-e Registry, GREENGUARD, FloorScore, HPD Repository

**P2 — Week 3 (~14 APIs):**
USGS National Map, NRCS Soil Survey, EPA EJScreen, USFWS Critical Habitat, Green Button, EnergyPlus/Eppy, ArcGIS, Procore, IAQ Sensors, Smart Water Meters

**P3 — Week 4 (~7 APIs):**
Tally, Walk Score, OpenADR, Autodesk Forge, Revit API, BACnet, IES VE

### 7.2 Resilience Contract

| Layer | Pattern | Implementation |
|-------|---------|----------------|
| Rate limiting | Token bucket | Redis, per-API + per-project + per-key |
| Retries | Exponential backoff | 2s, 4s, 8s, 16s, 32s + jitter |
| Circuit breaker | Fail-fast | 5 failures / 60s → open; auto-recover after timeout |
| Fallback hierarchy | Graceful degradation | Live API → Redis cache → static snapshot → HITL manual |
| Caching | TTL tiers | Hot (1h), Warm (1–7d), Cold/archive (7yr PostgreSQL) |

### 7.3 High-Risk Assumptions (Must Verify Before Phase 1)

- [ ] USGBC Arc write API — access terms and endpoint availability
- [ ] GBCI credential lookup API — is public access available?
- [ ] EC3 API terms — bulk query limits for automated platforms
- [ ] Walk Score API — coverage and pricing for non-US regions
- [ ] LEED v5 reference guide — licensing for RAG embeddings

---

## 8. Evidence Pack Standard

Every credit produces a 12-section evidence pack:

| # | Section | Content |
|---|---------|---------|
| 1 | Cover | Project info, credit code, automation level, reviewer |
| 2 | Requirement Summary | LEED v5 requirement verbatim + compliance checklist |
| 3 | Input Inventory | All inputs with source, timestamp, validation status |
| 4 | Source Index | All APIs/databases queried with response hashes |
| 5 | Extracted Data | Raw normalized data from APIs |
| 6 | Calculation Workbook | Formula + inputs + outputs (XLSX with formulas intact) |
| 7 | Narrative | AI-generated compliance narrative with citations |
| 8 | Compliance Matrix | Each requirement → evidence mapping |
| 9 | Confidence Report | Per-section confidence scores + tier classification |
| 10 | Audit Trail | Every state transition, API call, HITL decision |
| 11 | Review Annotations | Reviewer comments, checklist responses |
| 12 | Exception Report | Any items below confidence threshold or missing data |

---

## 9. Delivery Roadmap

### 9.1 Three-Horizon Plan

| Horizon | Duration | Scope | Team |
|---------|----------|-------|------|
| Demo | 14 days | Workflow engine, HITL, evidence export, WEp2 wedge proof, mocked/sandbox APIs | 2 FTE |
| MVP | Multi-phase | Five Kimi-aligned suites, source verification, regional gating, production evidence packs | 4-6 engineers + LEED review |
| V2+ | Post-MVP | Arc direct submission, regional expansion, additional 51-credit matrix candidates | TBD |

### 9.2 Phase 0 — Consolidation (1 week, NOW)

- [x] Normalize all SKILL.md files from Kimi to canonical snake_case format
- [x] Apply realistic automation % corrections
- [ ] Verify API access: Arc, GBCI, EC3, Walk Score, LEED v5 reference licensing
- [ ] Confirm demo credit selection (recommended: PRc2 pipeline proof, WEp2 wedge, EAp5/EAc7 shared-input workflow, one assisted workflow)
- [ ] Finalize evidence pack format (render sample for WEp2 or PRc2)

### 9.3 Phase 1 — 14-Day Demo

**Milestone:** a small credit set running end-to-end with mocked/sandboxed APIs and full HITL flow

| Week | Deliverables |
|------|-------------|
| 1 | Platform foundation (FastAPI, PostgreSQL, Redis, Deer-Flow), PRc2 pipeline proof + WEp2 wedge |
| 2 | EAp5/EAc7 shared workflow, one assisted workflow, HITL flow, evidence pack export |

Exit criteria: schema tests pass, artifact contract satisfied, region-gating functional.

### 9.4 Phase 2-3 - Production MVP Suites

| Weeks | Focus |
|-------|-------|
| 1–2 | Infrastructure foundation, first skill E2E, HITL Slack validation |
| 3–5 | 8 priority skills, 8 core APIs, document template library, consultant dashboard v1 |
| 6–8 | Remaining 8 Tier-1 skills, 20+ APIs, regional filtering, confidence scoring, reviewer dashboard v2 |
| 9–10 | Load testing (p99 < 45s, 100 concurrent projects), security audit, monitoring, training materials |

**Team model:**

| Role | FTE | Phases |
|------|-----|--------|
| Backend / Platform | 1.0 | All |
| Skill Engineers | 2.0 | Phases 2–3 |
| Frontend | 0.5–1.0 | Phases 2–3 |
| DevOps | 0.5–1.0 | All |
| LEED Reviewer (part-time) | 0.25 | All |

### 9.5 Infrastructure Costs (Monthly)

| Component | Spec | Cost |
|-----------|------|------|
| Compute (ECS/EKS) | 6 nodes × 8 vCPU / 32 GB | $1,200 |
| LLM (OpenAI/Claude API) | GPT-4o / Claude tokens | $800–$2,500 |
| Database (RDS PostgreSQL 15) | db.r6g.xlarge, Multi-AZ | $450 |
| Cache (ElastiCache Redis 7) | cache.r6g.large, Cluster | $180 |
| Document store (S3/MinIO) | 500 GB, versioned, encrypted | $25 |
| CDN (CloudFront) | Template assets, PDFs | $50 |
| Monitoring (Grafana Cloud Pro) | 15s scrape | $100 |
| **Total** | | **$2,805–$4,505** |

---

## 10. Open Questions & Decisions

### 10.1 Accepted Decisions (ADRs 001–012)

| ADR | Decision |
|-----|---------|
| 001 | Deer-Flow as workflow foundation (saves 10 weeks vs. from-scratch) |
| 002 | PostgreSQL + PostGIS for all state and geo data |
| 003 | FastAPI for API layer |
| 004 | React + TypeScript frontend |
| 005 | HITL required for every credit — no silent pass-through |
| 006 | Regional filtering: hide/warn credits where APIs unavailable |
| 007 | JWT auth for all API endpoints |
| 008 | S3/MinIO for document storage, 7-year retention |
| 009 | Celery + RabbitMQ for async task queue |
| 010 | Freemium pricing model (per-credit + project bundles + enterprise) |
| 011 | 14-day prototype validates workflow mechanics; commercial MVP uses Kimi's five-suite scope |
| 012 | No USGBC Arc submission in V1 — manual export only |

### 10.2 Open Questions (Prioritized)

| Priority | Question | Owner | Blocks |
|----------|---------|-------|--------|
| P0 | Arc write API access & terms? | Partnerships | V2 Arc integration |
| P0 | GBCI credential lookup API — public access? | Partnerships | PRc2 automation |
| P0 | EC3 API terms for automated bulk queries? | Legal | MRp2, IPp3 |
| P1 | LEED v5 reference guide — RAG licensing? | Legal | All skills |
| P1 | Which small prototype set proves the workflow fastest? | Product | Phase 1 |
| P1 | Kimi 51-credit score mapping to v5 requirements verified? | Engineering | V2 expansion |
| P2 | Regional market priority (CA/UK/EU)? | Product | V2 roadmap |
| P2 | Pricing model finalized? | Business | GTM |
| P3 | EAp2/EAc3 energy model parser scope? | Engineering | Tier-3 skills |

---

## 11. Source Map

| This document synthesizes | Source file |
|--------------------------|-------------|
| Automation levels & realism constraints | `EXECUTIVE_SUMMARY_REALISTIC.md`, `docs/01_realistic_automation_model.md` |
| Product requirements & evidence pack | `docs/02_product_requirements.md` |
| System architecture & services | `docs/03_system_architecture.md`, `leed-platform/agents/agent_architecture.md` |
| API strategy & resilience | `docs/04_data_integrations_and_regionality.md` |
| Skill contract standard | `docs/05_skill_contracts_and_credit_catalog.md`, `skills/SKILL_TEMPLATE.md` |
| HITL design & state machine | `docs/06_hitl_and_durable_workflows.md`, `skills/hitl_system.py` |
| Delivery roadmap & ADRs | `docs/07_delivery_roadmap.md`, `docs/08_decisions_and_open_questions.md` |
| Technical stack (Deer-Flow, LangGraph, APIs) | `Kimi_Agent_LEED v5 Credit Automation/tech_impl_sec01-04.md` |
| Generated skill contract drafts | `Kimi_Agent_LEED v5 Credit Automation/skills/*/SKILL.md` |
| Strategic analysis and suite prioritization | `Kimi_Agent_LEED v5 Credit Automation/leed_automation.agent.outline.md`, `Kimi_Agent_LEED v5 Credit Automation/leed_automation_sec00.md` |
