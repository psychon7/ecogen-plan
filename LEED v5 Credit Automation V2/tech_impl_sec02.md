# Master Technical Implementation Document

## Section 3: Deer-Flow Platform Architecture

### 3.1 System Overview

The LEED v5 Automation Platform is built on **Deer-Flow**, ByteDance's open-source "SuperAgent Harness" (60.2k GitHub stars, v2.0). Deer-Flow provides the foundational infrastructure for skill-based agent orchestration, durable workflow execution, and human-in-the-loop (HITL) coordination. Rather than building a custom workflow engine from scratch -- an estimated 12-week engineering effort -- the platform leverages Deer-Flow's proven architecture and extends it with LEED-specific skills, API integrations, and document templates.

**Core Architectural Principles:**

| Principle | Implementation | Rationale |
|-----------|---------------|-----------|
| Skill-based modularity | One skill per LEED credit/prerequisite | Isolated development, testing, and deployment per credit |
| Durable workflows | LangGraph with checkpoint persistence | Survives restarts, API failures, and multi-day HITL delays |
| Sandboxed execution | Docker containers per skill | Prevents cross-credit contamination; energy model parsing isolated |
| Memory persistence | PostgreSQL + Redis | Project state survives session termination; full audit trail |
| Human-in-the-Loop | Slack / Email / Web UI | Consultant review at critical checkpoints with SLA enforcement |

**Platform Foundation Provided by Deer-Flow:**

```
LEED v5 Automation Platform (Built on Deer-Flow)
================================================================
Included (70-80% of infrastructure):
  - Skill system and registry
  - Sub-agent orchestration (parallel/sequential)
  - LangGraph durable workflows with checkpointing
  - Docker sandbox execution
  - Memory / state persistence
  - HITL channels (Slack, Telegram, Email)
  - Web UI (React frontend)
  - API gateway (FastAPI)

Built on Top (LEED-specific layer):
  - 16 LEED credit skills
  - 36 API integration tools
  - Document templates (Jinja2)
  - Regional availability filter
  - HITL dashboard enhancements
```

**LangGraph Durable Workflows:**

Deer-Flow uses LangGraph as its workflow engine. Each skill defines a `StateGraph` where nodes represent workflow steps (validation, API calls, calculations, document generation) and edges define execution flow, including conditional routing based on HITL decisions. Checkpointing persists state to PostgreSQL after every node execution, enabling workflows to survive server restarts and resume from exact failure points.

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Workflow survives restarts; each node is checkpointed automatically
workflow = StateGraph(LEEDState)
workflow.add_node("validate", validate_inputs)
workflow.add_node("fetch_data", fetch_api_data)
workflow.add_node("calculate", perform_calculations)
workflow.add_node("hitl_review", human_review_checkpoint)
workflow.add_node("generate", generate_documents)

# Conditional edges based on HITL response
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: state["hitl_result"]["action"],
    {"approve": "generate", "reject": "validate", "request_changes": "calculate"}
)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

**Skill-Based Architecture:**

Each of the 16 LEED credits is implemented as a Deer-Flow skill -- a self-contained module with its own `SKILL.md` manifest, workflow graph, input/output schemas, templates, and test suite. Skills are mounted at `/mnt/skills/leed/` and discovered at runtime by the skill registry.

**Sandbox Execution:**

Each skill executes within an isolated Docker container provisioned by Deer-Flow's `AioSandboxProvider`. Energy model parsing, PDF generation, and Excel compilation occur in sandboxed environments with no access to other skills' data or the host system. Files are persisted across workflow steps at `/mnt/user-data/outputs/` and retained per the project's data retention policy (default: 24 months).

**Memory System:**

Deer-Flow's memory system stores project-specific facts and intermediate calculation results in PostgreSQL, keyed by `thread_id` (project identifier). This enables multi-session workflows where a consultant can start an energy analysis on Monday, receive a Slack HITL notification Tuesday, approve calculations Wednesday, and find the workflow resumed exactly where it left off.

---

### 3.2 Core Components Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LEED v5 AUTOMATION PLATFORM                           │
│                         (Built on Deer-Flow v2.0)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FRONTEND LAYER                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  React + TypeScript Dashboard                                       │   │
│  │  - Credit selection wizard    - HITL review interface              │   │
│  │  - Project dashboard          - Document preview                   │   │
│  │  - Regional availability map  - USGBC submission tracker           │   │
│  └────────────────────┬────────────────────────────────────────────────┘   │
│                       │ HTTPS / WebSocket                                   │
│  API GATEWAY          ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  FastAPI Gateway                                                    │   │
│  │  - JWT authentication         - Rate limiting (100 req/min)        │   │
│  │  - Request routing            - Webhook handling for HITL          │   │
│  │  - API key management (Vault)   - Request/response logging           │   │
│  └────────────────────┬────────────────────────────────────────────────┘   │
│                       │ gRPC / HTTP                                           │
│  WORKFLOW ENGINE      ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  LangGraph Server (Python)                                          │   │
│  │  - StateGraph compilation     - Checkpoint persistence (PostgreSQL)│   │
│  │  - Node execution scheduler   - Conditional edge routing             │   │
│  │  - Parallel sub-agent spawn   - Error recovery & retry logic         │   │
│  └────────────────────┬────────────────────────────────────────────────┘   │
│                       │ Docker socket API                                     │
│  SANDBOX LAYER        ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Docker Container Pool                                              │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        ┌──────────┐        │   │
│  │  │ IP-p3    │ │ EAp1     │ │ WEp2     │  ...   │ SSc6     │        │   │
│  │  │ Carbon   │ │ OpCarbon │ │ WaterMin │        │ Light    │        │
│  │  └──────────┘ └──────────┘ └──────────┘        └──────────┘        │   │
│  │  /mnt/skills/leed/       /mnt/user-data/outputs/                   │   │
│  └────────────────────┬────────────────────────────────────────────────┘   │
│                       │ API calls (HTTPS)                                     │
│  EXTERNAL APIs        ▼                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  EPA eGRID │ EC3 Database │ USGBC Arc │ NREL PVWatts │ NOAA Atlas   │   │
│  │  EPA SNAP  │ EPD Registry │ AHRI Dir  │ Walk Score   │ CRRC         │   │
│  │  Google Maps│ US Census │ NRCS Soils│ IES TM-15    │ FEMA NFHL    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  PERSISTENCE LAYER                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ PostgreSQL   │  │ Redis        │  │ S3 / MinIO   │  │ Vault        │   │
│  │ (State,      │  │ (Cache,      │  │ (Documents,  │  │ (API Keys,   │   │
│  │  Audit Logs) │  │  Pub/Sub)    │  │  Artifacts)  │  │  Secrets)    │   │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                             │
│  HITL CHANNELS                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                       │
│  │ Slack Bot    │  │ Email (SES)  │  │ Web UI       │                       │
│  │ (Primary)    │  │ (Fallback)   │  │ (Dashboard)  │                       │
│  └──────────────┘  └──────────────┘  └──────────────┘                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 3.3 Component Specifications Table

| Component | Technology | Purpose | Scaling Strategy | SLA Target |
|-----------|-----------|---------|------------------|------------|
| **Frontend** | React 18 + TypeScript + Vite | Consultant dashboard, HITL review UI, project tracking | CDN (CloudFront) + S3 static hosting | 99.9% uptime |
| **API Gateway** | FastAPI + Uvicorn | Auth (JWT), routing, rate limiting, request validation | Horizontal (Kubernetes HPA, 2-20 pods) | 200ms p99 latency |
| **LangGraph Server** | Python 3.11 + LangGraph 0.0.x | Workflow engine, checkpoint management, node scheduling | Stateful (1 pod per project partition) | Checkpoint < 500ms |
| **Skill Containers** | Docker + Python 3.11 | Credit-specific agent execution (parsing, calculation, docs) | Per-credit pool (warm standby containers) | Cold start < 5s |
| **Memory Store** | PostgreSQL 15 + pgvector | Project state, workflow checkpoints, audit logs | Master-replica (2 replicas, async) | RPO < 1min |
| **Cache / Pub-Sub** | Redis 7 (Cluster) | API response cache, HITL notification queue, rate limit counters | 3-master cluster with replicas | < 5ms read |
| **Document Store** | S3 / MinIO | Generated PDFs, XLSX, DOCX, ZIP packages, manifest JSON | Object storage (versioned, encrypted) | 99.99% durability |
| **Secrets Manager** | HashiCorp Vault | API keys, OAuth credentials, DB passwords | HA cluster (3 nodes, auto-unseal) | 99.99% availability |
| **Message Queue** | Redis Streams / RabbitMQ | HITL notification delivery, async document generation | Pub/sub with consumer groups | Delivery < 1s |
| **Monitoring** | Prometheus + Grafana | Metrics, alerting, SLA tracking | 2-replica Prometheus, shared Grafana | 15s scrape interval |

---

### 3.4 Data Flow

The following describes the complete data flow for a typical project executing multiple LEED credits from intake through submission:

**Step 1 — Project Intake**
The consultant creates a project via the React dashboard, entering building type, location (lat/lon or address), target certification level, and team roster. The API Gateway validates inputs and creates a project record in PostgreSQL with a unique `thread_id`. Project metadata is saved to Deer-Flow memory.

**Step 2 — Credit Selection**
The consultant selects credits to pursue from the 16-skill registry. The RegionalSkillFilter middleware evaluates each skill against project location, disabling skills whose required APIs are unavailable in that region (e.g., EPA eGRID for non-US projects triggers a warning and fallback data path).

**Step 3 — Skill Execution (Parallel Where Independent)**
The LangGraph Server spawns sub-agents for each selected credit. Independent prerequisites (EAp1, EAp2, EAp5, MRp2, WEp2) execute in parallel. Dependent credits (IPp3 requires EAp1 + EAp5 + MRp2 outputs) execute sequentially after prerequisites complete.

**Step 4 — API Data Fetching**
Each skill fetches required data from external APIs: EPA eGRID for grid factors, EC3 for embodied carbon EPDs, NREL PVWatts for solar potential, NOAA Atlas 14 for rainfall data. API responses are cached in Redis with TTL appropriate to data volatility (eGRID: 1 year; EC3: 24 hours).

**Step 5 — Calculations**
Skills perform credit-specific calculations using validated API data. All calculations use explicit formulas with unit conversion tracking. Results are stored in the workflow state and logged to the audit trail.

**Step 6 — HITL Review Checkpoints**
When a skill reaches a HITL checkpoint, the workflow pauses and persists state. A notification is dispatched via the primary channel (Slack) with fallback to email. The consultant reviews parsed data, calculations, and draft documents through the web UI, then approves, rejects, or requests changes. The workflow resumes based on the decision.

**Step 7 — Document Generation**
Upon HITL approval, skills generate submission documents using Jinja2 HTML templates rendered to PDF via WeasyPrint, Excel workbooks via OpenPyXL, and Word narratives via python-docx. Documents include embedded calculation formulas for auditor verification.

**Step 8 — Package Assembly**
The Package Assembly skill (a meta-skill) collects all approved credit documents, generates a project-level manifest.json with SHA-256 checksums, bundles into a ZIP archive, and uploads to the document store.

**Step 9 — USGBC Arc Submission**
For credits configured for direct submission, the platform authenticates to the USGBC Arc API via OAuth 2.0 and uploads documents to the appropriate credit folders. Submission IDs are stored in project state.

**Step 10 — Export & Archive**
The consultant downloads the complete submission package. All intermediate artifacts, API responses, and audit logs are archived to S3 with 7-year retention per LEED documentation requirements.

---

### 3.5 Security & Compliance

**API Key Management (HashiCorp Vault)**

All external API credentials are stored in HashiCorp Vault with the following access controls:

| Secret Type | Vault Path | Rotation Policy | Access Pattern |
|-------------|-----------|-----------------|----------------|
| USGBC Arc OAuth | `secret/leed/arc/oauth` | 90 days | Runtime fetch, 1h TTL |
| EC3 API Key | `secret/leed/ec3/api_key` | 180 days | Runtime fetch, 24h TTL |
| NREL PVWatts Key | `secret/leed/nrel/api_key` | 365 days | Runtime fetch, 24h TTL |
| OpenAI API Key | `secret/leed/openai/api_key` | 90 days | Runtime fetch, 1h TTL |
| Database Password | `secret/leed/postgres/password` | 90 days | Startup fetch only |
| Slack Bot Token | `secret/leed/slack/bot_token` | 180 days | Runtime fetch, 24h TTL |

Vault is deployed in HA mode with 3 nodes, auto-unseal via AWS KMS / Azure Key Vault, and audit logs forwarded to a SIEM. No secrets are committed to source control; the CI/CD pipeline injects them via Vault's Kubernetes auth method.

**Document Encryption at Rest (AES-256)**

All generated documents stored in S3/MinIO are encrypted using server-side encryption with AES-256. The document store enforces: (a) bucket versioning to prevent accidental overwrites, (b) lifecycle rules transitioning documents to Glacier after 12 months, (c) cross-region replication for disaster recovery, and (d) access logging for all read/write operations.

**PII Handling for Census/Demographic Data**

Skills that query US Census Bureau APIs (LTc3) and Tree Equity Score (SSc5) handle location data as follows:
- Lat/lon coordinates are hashed (SHA-256) in logs; only the hash is retained long-term
- Census tract IDs are anonymized in analytics exports
- Project addresses are encrypted at rest and only decrypted in-memory during workflow execution
- No PII is transmitted to external APIs beyond what is required for the API call (e.g., address geocoding to Google Maps)
- GDPR data processing agreements are in place with all third-party API providers

**Audit Trails**

Every operation in the platform is logged to PostgreSQL with the following schema:

```sql
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL,
    skill_name VARCHAR(64) NOT NULL,
    workflow_step VARCHAR(128) NOT NULL,
    action VARCHAR(64) NOT NULL,  -- 'api_call', 'calculation', 'hitl_decision', 'document_generated'
    actor VARCHAR(128),  -- 'system', 'user:{id}', 'api:{name}'
    timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
    inputs JSONB,
    outputs JSONB,
    checksum VARCHAR(64),  -- SHA-256 of document or data payload
    api_response_code INT,
    duration_ms INT,
    ip_address INET,
    user_agent TEXT
);
```

Logs are retained for 7 years to meet LEED documentation retention requirements and are queryable via the dashboard for project-level audit reports.

**SOC 2 / GDPR Considerations**

| Control Domain | Implementation | Evidence |
|----------------|---------------|----------|
| Access Control | RBAC with project-level permissions; SSO via SAML 2.0 | Quarterly access reviews |
| Data Encryption | TLS 1.3 in transit; AES-256 at rest | Certificate inventory |
| Change Management | GitOps (ArgoCD); mandatory PR review | Git history, PR approvals |
| Monitoring & Alerting | Prometheus + PagerDuty; 24/7 on-call | Incident response logs |
| Backup & Recovery | PostgreSQL PITR (7 days); S3 cross-region replication | Monthly DR drills |
| Vendor Management | DPA with all API providers; annual security review | Signed DPAs on file |
| Data Retention | 7-year document retention; GDPR deletion within 30 days of request | Retention policy document |

The platform is designed to be SOC 2 Type II ready within 6 months of production launch. GDPR compliance is achieved through data minimization (only collecting data required for LEED calculations), purpose limitation (data used only for certification support), and the right to erasure (automated deletion workflows triggered via dashboard request).

---

## Section 4: Skill System Specification

### 4.1 Skill Registry

The following table catalogs all 16 LEED v5 skills implemented as Deer-Flow modules. Each skill is independently versioned, tested, and deployable.

| # | Skill Name | Credit | Points | Automation % | HITL Checkpoints | Complexity | Est. Dev Days |
|---|-----------|--------|--------|-------------|-------------------|------------|---------------|
| 1 | IPp3 Carbon Assessment | IPp3 | Required (Prereq) | 92.5% | 1 (Consultant verification) | Low | 5 |
| 2 | EAp1 Operational Carbon | EAp1 | Required (Prereq) | 89.4% | 1 (Consultant review, 72h SLA) | Low-Medium | 6 |
| 3 | EAp2 Minimum Energy Efficiency | EAp2 | Required (Prereq) | 85.7% | 2 (Modeler + Consultant, 72h each) | Medium | 8 |
| 4 | EAp5 Refrigerant Management | EAp5 | Required (Prereq) | 85.2% | 1 (MEP Engineer, 24h SLA) | Low | 4 |
| 5 | EAc3 Enhanced Energy Efficiency | EAc3 | Up to 10 / 7 | 87.7% | 2 (Modeler + Consultant, 48h each) | Medium-High | 7 |
| 6 | EAc7 Enhanced Refrigerant | EAc7 | 2 | 89.3% | 1 (Mechanical Engineer, 48h) | Low | 4 |
| 7 | MRp2 Embodied Carbon | MRp2 | Required (Prereq) | 87.0% | 2 (Takeoff + EPD matching, 72h each) | Medium | 7 |
| 8 | MRc2 Reduce Embodied Carbon | MRc2 | Up to 6 | 88.4% | 1-2 (LCA Specialist) | Medium | 6 |
| 9 | WEp2 Minimum Water Efficiency | WEp2 | Required (Prereq) | 89.3% | 1 (Consultant, 48h) | Low | 5 |
| 10 | WEc2 Enhanced Water Efficiency | WEc2 | Up to 8 / 7 | 87.5% | 1 (Consultant, 48h) | Medium | 6 |
| 11 | LTc3 Compact & Connected | LTc3 | Up to 6 | 88.0% | 1 (Project Manager, 48h) | Low | 5 |
| 12 | LTc1 Sensitive Land Protection | LTc1 | 1 | 87.6% | 1 (Environmental Consultant, 48h) | Medium | 5 |
| 13 | SSc3 Rainwater Management | SSc3 | 3 | 88.0% | 1 (Civil Engineer, 48h) | Medium | 5 |
| 14 | SSc5 Heat Island Reduction | SSc5 | 2 | 85.3% | 1 (Architect, 48h) | Low | 4 |
| 15 | SSc6 Light Pollution Reduction | SSc6 | 1 | 90.6% | 1 (Lighting Designer, 48h) | Low | 4 |
| 16 | PRc2 LEED AP Verification | PRc2 | 1 | 90.1% | 1 (Project Admin, 24h) | Low | 3 |

**Registry Totals:**

| Metric | Value |
|--------|-------|
| Total Skills | 16 |
| Prerequisites | 5 (IPp3, EAp1, EAp2, EAp5, MRp2, WEp2) |
| Credits | 10 |
| Total Possible Points | 42 points (NC) / 37 points (C&S) |
| Average Automation Level | 88.1% |
| Total HITL Checkpoints | 18 (avg 1.1 per skill) |
| Total Estimated Dev Days | 80 person-days |

---

### 4.2 Skill Interaction Patterns

Skills interact through three primary execution patterns, determined by credit dependencies and data sharing requirements:

**Pattern A: Parallel Execution (Independent Credits)**

Prerequisites and credits with no shared data execute in parallel to minimize wall-clock time. Example: EAp5 (Refrigerant Management), WEp2 (Water Minimum), and SSc5 (Heat Island) can run simultaneously because they consume different input data and produce independent outputs.

```python
# Lead agent spawns sub-agents for parallel execution
sub_agents = [
    {"name": "eap5-agent", "skill": "leed-ea-p5-refrigerant"},
    {"name": "wep2-agent", "skill": "leed-we-p2-water-min"},
    {"name": "ssc5-agent", "skill": "leed-ss-c5-heat-island"},
]
results = await lead_agent.spawn_parallel(sub_agents, shared_inputs)
# Execution time = max(individual skill times), not sum
```

**Pattern B: Sequential Execution (Prerequisite Dependencies)**

Credits that require outputs from prerequisite skills execute sequentially. The workflow graph encodes these dependencies as explicit edges.

| Dependent Skill | Prerequisites Required | Data Passed |
|-----------------|----------------------|-------------|
| IPp3 Carbon Assessment | EAp1 (energy model), EAp5 (refrigerant inventory), MRp2 (material quantities) | `annual_kwh`, `fuel_breakdown`, `refrigerant_types`, `charge_kg`, `material_gwp` |
| WEc2 Enhanced Water | WEp2 (baseline fixture calcs) | `baseline_annual_gal`, `design_annual_gal`, `fixture_schedule` |
| MRc2 Reduce Embodied Carbon | MRp2 (baseline embodied carbon) | `total_kg_co2`, `structural_kg_co2`, `enclosure_kg_co2`, `gwp_intensity` |
| EAc3 Enhanced Energy | EAp2 (model parsing results) | `parsed_model_data`, `cost_summary`, `pct_better` |

```python
# Sequential dependency: EAp1 -> IPp3
workflow.add_edge("eap1_skill", "ipp3_skill")  # EAp1 must complete before IPp3 starts

# Sequential dependency: MRp2 -> MRc2
workflow.add_edge("mrp2_skill", "mrc2_skill")
```

**Dependency Resolution Algorithm:**

The orchestrator uses Kahn's topological sort algorithm on the dependency DAG to determine execution order. Before scheduling, it prunes nodes whose skills were not selected by the consultant, and detects cycles (which indicate a design flaw in the skill dependency declarations). The algorithm produces a linearized execution sequence where every skill appears after all its prerequisites.

```python
def topological_sort(skills: list[str], dependencies: dict[str, list[str]]) -> list[str]:
    """Kahn's algorithm for dependency-aware execution ordering."""
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
        for dependent in adj[skill]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    if len(result) != len(skills):
        raise ValueError("Circular dependency detected in skill graph")
    
    return result
```

This algorithm guarantees that IPp3 (which depends on EAp1, EAp5, MRp2) never executes before any of its three prerequisites complete, while LTc3 (no dependencies) always appears at the start of the sequence and can execute immediately when the project is initialized.

**Pattern C: Shared State (Cross-Credit Data Flow)**

The project-wide state store (`LEEDProjectState`) acts as a shared data bus. Skills read prerequisite outputs from state and write their own outputs back, enabling both sequential and parallel patterns to coexist.

```python
class LEEDProjectState(TypedDict):
    project_id: str
    location: dict  # lat, lon, country
    
    # Prerequisite outputs (shared)
    eap1_operational_carbon: Optional[dict]
    eap2_energy_results: Optional[dict]
    eap5_refrigerant_inventory: Optional[list]
    mrp2_embodied_carbon: Optional[dict]
    wep2_water_baseline: Optional[dict]
    
    # Credit outputs
    eac3_points: Optional[int]
    wec2_points: Optional[int]
    mrc2_points: Optional[int]
    ip_carbon_projection: Optional[dict]
    
    # Meta
    documents: dict[str, str]  # credit_code -> document path
    hitl_status: dict[str, dict]
    audit_log: list[dict]
```

**Execution Orchestrator Logic:**

```python
async def execute_project_skills(project_state: LEEDProjectState, selected_credits: list[str]):
    """Execute skills with dependency-aware scheduling."""
    
    # Phase 1: Execute all prerequisites in parallel
    prerequisites = [c for c in selected_credits if is_prerequisite(c)]
    prereq_results = await asyncio.gather(*[
        execute_skill(skill, project_state) for skill in prerequisites
    ])
    
    # Merge prerequisite outputs into shared state
    for result in prereq_results:
        project_state[result.output_key] = result.data
    
    # Phase 2: Execute dependent credits in dependency order
    credits = [c for c in selected_credits if not is_prerequisite(c)]
    execution_order = topological_sort(credits, dependency_graph)
    
    for credit in execution_order:
        result = await execute_skill(credit, project_state)
        project_state[result.output_key] = result.data
    
    return project_state
```

**State Synchronization and Conflict Resolution:**

When multiple skills execute in parallel, they may attempt to write to the same state keys. The platform uses an optimistic locking strategy: each skill read receives a state version number; writes are accepted only if the version has not changed. If a conflict is detected, the skill's write is retried after re-reading the latest state. This ensures that the Energy Modeler approving EAp2 calculations does not collide with the MEP Engineer approving EAp5 refrigerant data, even when both HITL checkpoints resolve simultaneously.

**Error Propagation Across Skills:**

Prerequisite failures cascade to dependent skills with explicit error messages. If EAp2 fails due to a missing `.eso` file, EAc3 receives a clear `PrerequisiteNotMetError` with the EAp2 failure reason, rather than attempting to parse non-existent model data. The project dashboard surfaces these cascading errors as a dependency tree with red/green status indicators per skill.

**Resource Quota Management:**

Each skill declares its resource requirements (CPU, memory, disk, expected API calls) in its `SKILL.md` manifest. The orchestrator uses this information to prevent resource exhaustion: energy model parsing skills (EAp2, EAc3) are throttled to 2 concurrent executions per worker to prevent memory spikes from large `.eso` files, while lightweight skills (PRc2, SSc6) can run at higher concurrency.

| Skill | CPU Request | Memory Request | Max Concurrent | API Calls per Execution |
|-------|------------|----------------|----------------|------------------------|
| EAp2 | 2 cores | 4 GB | 2 | 0 (local parsing) |
| EAc3 | 2 cores | 4 GB | 2 | 0 (local parsing) |
| MRp2 | 1 core | 2 GB | 4 | 50 (EPD Registry + EC3) |
| IPp3 | 1 core | 2 GB | 4 | 10 (eGRID + EC3) |
| EAp1 | 1 core | 2 GB | 4 | 5 (eGRID + PVWatts) |
| PRc2 | 0.5 core | 512 MB | 10 | 1 (GBCI Directory) |
| SSc6 | 0.5 core | 512 MB | 10 | 0 (local validation) |

---

### 4.3 Skill Template Specification

Every skill in the registry follows a standardized `SKILL.md` structure. This template ensures consistency across all 16 credits and enables automated skill discovery, validation, and documentation generation.

**Required Sections:**

```markdown
---
name: leed-{credit-code}-{short-name}
version: 1.0.0
author: LEED Automation Platform
description: Automates LEED v5 {Credit Name} ...
---

## Metadata
- **Credit Code:** {XXXxN}
- **Credit Name:** {Full Credit Name}
- **Points:** {Required | Up to N}
- **Automation Level:** {N.N%}
- **Complexity:** {Low | Medium | High}
- **Primary Data Source:** {APIs and references}
- **HITL Required:** {Yes | No}

## Purpose
{1-2 paragraph description of what the skill automates and its scope boundaries}

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| {field_name} | {type} | {source} | {validation rules} |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| {field_name} | {type} | {default} | {description} |

## Workflow Steps (Durable)
### Step N: {Step Name}
- **Type:** {Validation | API Call | Calculation | Document Generation | Human Review}
- **Automated:** {Yes | No}
- **Description:** {Detailed description}
- **Output:** {Output schema}
- **On Failure:** {Failure handling strategy}

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step N | {Role} | {N hours} | {Review instructions} |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| {API Name} | {Purpose} | {Regions} | {Fallback} | {Rate Limit} |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| {Region} | {Available | Limited | Unavailable} | {Notes} |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| {Error Name} | {Action} | {Yes/No} | {N times} |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| {Document Name} | {PDF | XLSX | DOCX | JSON} | {Description} |

## Testing
{pytest commands and test coverage requirements}

## Example Usage (Deer-Flow)
{Python invocation example}

## Deer-Flow Workflow (LangGraph)
{LangGraph StateGraph definition}
```

**Template Validation Rules:**

| Rule | Enforcement | Tool | Severity |
|------|------------|------|----------|
| All required sections present | CI/CD linting | `skill-linter.py` | Blocking |
| Metadata fields complete | Schema validation | Pydantic `SkillManifest` | Blocking |
| API dependencies declared | Pre-deployment check | `api-availability-check.sh` | Blocking |
| Regional availability specified | Pre-execution filter | `RegionalSkillFilter` | Blocking |
| HITL checkpoints have SLA | Workflow compilation | LangGraph validation | Blocking |
| Testing commands provided | CI gate | `pytest` execution | Blocking |
| Output document types declared | Template engine check | `document-schema-validator.py` | Warning |
| Calculation formulas documented | Manual review | Tech lead sign-off | Warning |

**Skill Discovery and Registration:**

Skills are automatically discovered at runtime by scanning the `/mnt/skills/leed/` directory tree. The Skill Registry loads each `SKILL.md` manifest, validates it against the Pydantic `SkillManifest` schema, and registers the skill with its metadata, entry point module, and Docker image reference. This enables hot-loading of new skills without restarting the LangGraph server.

```python
class SkillRegistry:
    def discover_skills(self, skills_dir: Path) -> list[SkillManifest]:
        skills = []
        for skill_dir in skills_dir.glob("*/"):
            manifest_path = skill_dir / "SKILL.md"
            if manifest_path.exists():
                manifest = self._parse_manifest(manifest_path)
                if self._validate_manifest(manifest):
                    skills.append(manifest)
        return skills
    
    def get_skill(self, credit_code: str) -> SkillManifest:
        return next(s for s in self._skills if s.credit_code == credit_code)
    
    def filter_by_region(self, region: str) -> list[SkillManifest]:
        return [s for s in self._skills if s.is_available_in(region)]
```

**Skill Manifest Schema (Pydantic):**

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional

class SkillManifest(BaseModel):
    name: str
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    credit_code: str = Field(pattern=r"^[A-Z]{2}[pc]\d+$")
    credit_name: str
    points: Literal["Required"] | int
    automation_level: float = Field(ge=0.0, le=100.0)
    complexity: Literal["Low", "Medium", "High"]
    hitl_required: bool
    hitl_checkpoints: list[HITLCheckpoint]
    api_dependencies: list[APIDependency]
    regional_availability: dict[str, Literal["Available", "Limited", "Unavailable"]]
    docker_image: str
    entry_point: str  # module path for skill execution
    resource_requirements: ResourceRequirements
```

**Template Engine Pipeline:**

Document generation follows a standardized pipeline: (1) Jinja2 HTML template populated with skill output data, (2) WeasyPrint renders HTML to PDF with embedded vector charts, (3) OpenPyXL generates Excel workbooks with visible formulas for auditor traceability, (4) python-docx produces Word narratives with placeholder fields for final human editing. All templates are versioned alongside their parent skill and validated against output schema constraints before deployment.

---

### 4.4 Skill Lifecycle

Each skill progresses through a standardized lifecycle from development through retirement:

```
Development ──> Testing ──> Staging ──> Production ──> Monitoring ──> Updates ──> Deprecation
```

**Phase 1: Development (Est. 3-7 days per skill)**
- Skill author creates `SKILL.md` manifest following template specification
- Implements LangGraph workflow nodes (validation, API calls, calculations, document generation)
- Creates Jinja2 templates for PDF/Excel/Word outputs
- Writes unit tests for all calculation logic
- Implements error handling with fallback strategies

**Phase 2: Testing (Est. 2-3 days per skill)**

Testing is organized into four test tiers with distinct coverage targets:

| Tier | Test Type | Coverage Target | Execution | CI Gate |
|------|-----------|----------------|-----------|---------|
| Unit | Input validation, calculation logic, edge cases | > 90% code coverage | Local pytest, < 10s | Required |
| Integration | Mocked API responses, end-to-end workflow | All API paths exercised | Dockerized pytest, < 2min | Required |
| HITL Simulation | Checkpoint pausing, resumption, SLA timers | All HITL paths covered | Async test harness, < 5min | Required |
| Regression | Compare outputs against known-good baselines | Output diff < 0.1% | Nightly CI, < 15min | Warning |

The HITL simulation tier is particularly critical: it uses Deer-Flow's `MockHumanReviewNode` to simulate consultant approvals, rejections, and revision requests at each checkpoint, verifying that the workflow correctly branches to the appropriate subsequent node. Without this tier, a bug in conditional edge routing could go undetected until a real consultant encounters a hung workflow.

**Phase 3: Staging (Est. 1-2 days per skill)**

Staging validates skills against real-world data before production release. The staging environment mirrors production infrastructure (same API endpoints, same Vault secrets, same Docker runtime) but with rate-limited API keys and isolated S3 buckets. Each skill is executed against 3-5 real project datasets representing diverse building types, climate zones, and regional contexts. A staging checklist is completed for each skill:

- [ ] Document output quality reviewed by LEED consultant
- [ ] Regional availability filter accuracy verified for 6+ regions
- [ ] HITL notification delivery confirmed (Slack + email fallback)
- [ ] API fallback paths exercised (e.g., eGRID timeout triggers cached data)
- [ ] Error messages are actionable for non-technical users
- [ ] Execution time < 90 seconds for all automated steps
- [ ] Memory usage stays below declared resource limits
- [ ] No PII leaks in logs or API request traces

**Phase 3: Staging (Est. 1-2 days per skill)**
- Deploy to staging environment with live API keys (rate-limited)
- Execute against 3-5 real project datasets
- Validate document output quality with LEED consultants
- Check regional availability filter accuracy
- Verify HITL notification delivery (Slack + email)

**Phase 4: Production (Continuous)**
- Skill registered in production skill registry
- Version pinned for stability: `name: leed-ea-c3-energy-enhanced, version: 1.0.0`
- Monitoring dashboards track: execution time, API error rates, HITL response times, document generation success rate
- Alerting on: API failures > 5%, HITL SLA breaches > 10%, calculation errors > 1%

**Phase 5: Monitoring & Updates (Ongoing)**
- Annual updates for static data dependencies (ASHRAE standards, eGRID data, IPCC factors)
- Quarterly reviews of API availability and rate limit changes
- Bug fixes deployed as patch versions (1.0.1, 1.0.2)
- Feature additions deployed as minor versions (1.1.0)
- Breaking changes deployed as major versions (2.0.0) with migration guide

**Phase 6: Deprecation (As Needed)**
- Deprecated skills remain available for 12 months with warning banners
- Migration path provided to replacement skills
- Final removal announced 90 days in advance

**Versioning Policy:**

| Change Type | Version Bump | Example | Approval Required |
|-------------|-------------|---------|-------------------|
| Bug fix | Patch (x.y.Z) | 1.0.0 -> 1.0.1 | Tech lead |
| New feature / API | Minor (x.Y.z) | 1.0.0 -> 1.1.0 | Engineering manager |
| Breaking change / new standard | Major (X.y.z) | 1.0.0 -> 2.0.0 | Architecture board |
| Data refresh (annual) | Patch (x.y.Z) | 1.0.0 -> 1.0.1+egrid2024 | Tech lead |

---

### 4.5 Skill Dependencies Graph

The following directed acyclic graph (DAG) shows prerequisite and data-sharing relationships between skills:

```
                                    PROJECT INTAKE
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
            ┌───────────┐          ┌───────────┐          ┌───────────┐
            │   EAp1    │          │   EAp5    │          │   MRp2    │
            │ Op Carbon │          │ Refrigerant│          │ Embodied  │
            │ Required  │          │ Required   │          │ Required  │
            └─────┬─────┘          └─────┬─────┘          └─────┬─────┘
                  │                      │                      │
                  │                      │                      │
                  └──────────────────────┼──────────────────────┘
                                         │
                                         ▼
                              ┌───────────────────┐
                              │      IPp3         │
                              │ Carbon Assessment │
                              │    Required       │
                              │ (consumes EAp1,   │
                              │  EAp5, MRp2)      │
                              └───────────────────┘
                                         │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
            ┌───────────┐          ┌───────────┐          ┌───────────┐
            │   EAp2    │          │   WEp2    │          │   PRc2    │
            │ Energy Min│          │ Water Min │          │ LEED AP   │
            │ Required  │          │ Required  │          │ 1 point   │
            └─────┬─────┘          └─────┬─────┘          └───────────┘
                  │                      │
                  │                      │
                  ▼                      ▼
            ┌───────────┐          ┌───────────┐
            │   EAc3    │          │   WEc2    │
            │ Energy    │          │ Water     │
            │ Enhanced  │          │ Enhanced  │
            │ (extends  │          │ (extends  │
            │  EAp2)    │          │  WEp2)    │
            └───────────┘          └───────────┘
                  │
                  │
                  ▼
            ┌───────────┐
            │   EAc7    │
            │ Enhanced  │
            │ Refrigerant│
            └───────────┘
                                         │
                                         ▼
                              ┌───────────────────┐
                              │      MRc2         │
                              │ Reduce Embodied   │
                              │ Carbon            │
                              │ (extends MRp2)    │
                              └───────────────────┘

INDEPENDENT SKILLS (no prerequisites, can run anytime):
┌──────────────────────────────────────────────────────────────────────────┐
│  LTc1 (Sensitive Land) │ LTc3 (Compact & Connected) │ SSc3 (Rainwater)  │
│  SSc5 (Heat Island)    │ SSc6 (Light Pollution)     │                   │
└──────────────────────────────────────────────────────────────────────────┘
```

**Dependency Matrix:**

| Skill | Direct Prerequisites | Data Consumed From | Enables |
|-------|---------------------|-------------------|---------|
| IPp3 | EAp1, EAp5, MRp2 | Energy model, refrigerant inventory, material GWP | None (terminal aggregator) |
| EAc3 | EAp2 | Parsed model data, cost summary, compliance calc | None |
| EAc7 | EAp5 (recommended) | Refrigerant inventory (optional cross-check) | None |
| WEc2 | WEp2 | Baseline/design fixture calcs, fixture schedule | None |
| MRc2 | MRp2 | Baseline embodied carbon, GWP intensity | None |
| LTc3 | None | US Census, Walk Score, GTFS | None |
| LTc1 | None | FEMA, NWI, USFWS, USGS | None |
| SSc3 | None | NOAA Atlas 14, NRCS soils | None |
| SSc5 | None | CRRC, Tree Equity Score | None |
| SSc6 | None | IES TM-15, manufacturer data | None |
| PRc2 | None | GBCI Directory, team roster | None |

**Execution Strategy Based on Dependencies:**

| Phase | Skills Executed | Parallelism | Expected Wall Time |
|-------|----------------|-------------|-------------------|
| Phase 1 | EAp1, EAp5, MRp2, EAp2, WEp2, LTc1, LTc3, SSc3, SSc5, SSc6, PRc2 | Max parallel (11 skills) | ~15 minutes |
| Phase 2 | IPp3 (waits for EAp1+EAp5+MRp2) | Sequential | +~5 minutes |
| Phase 3 | EAc3 (waits for EAp2), WEc2 (waits for WEp2), MRc2 (waits for MRp2) | Parallel (3 skills) | +~10 minutes |
| Phase 4 | EAc7 (waits for EAp5, optional) | Sequential | +~3 minutes |
| **Total** | All 16 skills | Dependency-aware | **~35 minutes** (automated steps only, excluding HITL) |

**Key Design Decisions:**

1. **IPp3 as Terminal Aggregator:** IPp3 is the only skill that consumes outputs from three prerequisite skills. It does not enable downstream credits, making it a natural terminal node in the DAG.

2. **Extension Pattern:** Credits that extend prerequisites (EAc3 extends EAp2, WEc2 extends WEp2, MRc2 extends MRp2, EAc7 extends EAp5) reuse parsed data and add additional calculations. This avoids re-parsing the same energy models or material takeoffs.

3. **Independent Skills:** Site and location-based credits (LTc1, LTc3, SSc3, SSc5, SSc6, PRc2) have no prerequisites and can execute at any time, ideally in Phase 1 for maximum parallelism.

4. **Cross-Credit Shared State:** The project state store enables skills to read outputs from completed skills without explicit edges. For example, IPp3 can read EAp1 data as soon as EAp1 writes to state, even if EAp5 and MRp2 are still running. This "publish-subscribe" pattern reduces overall wall time compared to strict DAG execution.

---

*End of Sections 3-4*
