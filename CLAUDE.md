# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ecogen is a LEED v5 credit automation platform for LEED consultants. It automates 70-85% of documentation work through a skill-based, multi-agent system with mandatory Human-in-the-Loop (HITL) checkpoints. The platform is **not** a replacement for consultants — AI assists, humans decide.

Key constraints from `EXECUTIVE_SUMMARY_REALISTIC.md`:
- The production MVP is suite-based: WEp2+WEc2, EAp5+EAc7, EQp1+EQp2, IPp1+IPp2, and MRc3.
- The generated 16-skill set is an assisted catalog and implementation inventory, not the commercial MVP promise.
- Regional support is credit-specific; show warnings, manual mode, or hide workflows where source data is weak.
- AI cannot reliably interpret CAD drawings - use specialized tools (AutoCAD API) + human verification.
- Regulatory compliance decisions always require human sign-off.

## Tech Stack

**Backend:** Python 3.12, FastAPI, PostgreSQL 15+ with PostGIS, Redis, Celery/RabbitMQ  
**Frontend:** React (TypeScript/TSX), design tokens JSON system  
**Infrastructure:** Docker (dev), Kubernetes (prod), S3/GCS document storage  
**Agent framework:** Deer-Flow (referenced in architecture docs) with custom `DurableOrchestrator`

## Development Commands

No build files exist yet — the repo is in the planning/architecture phase. When implementing, the expected commands are:

```bash
# Backend
pip install -r requirements.txt
uvicorn main:app --reload

# Run tests for a single skill
python -m pytest skills/<credit_code>/tests/

# Run all skill tests
python -m pytest skills/

# Frontend
npm install
npm run dev
npm run build
```

The durable workflow engine can be exercised directly:
```bash
python skills/durable_workflow.py
```

## Architecture

### Directory Structure

```
ecogen-plan/
├── MASTER_PLAN.md                 # SINGLE SOURCE OF TRUTH — read this first
├── docs/                          # Ordered planning sequence
│   ├── 00_platform_brief.md
│   ├── 01_realistic_automation_model.md
│   ├── 02_product_requirements.md
│   ├── 03_system_architecture.md
│   ├── 04_data_integrations_and_regionality.md
│   ├── 05_skill_contracts_and_credit_catalog.md
│   ├── 06_hitl_and_durable_workflows.md
│   ├── 07_delivery_roadmap.md
│   ├── 08_decisions_and_open_questions.md
│   ├── 09_consolidated_credit_catalog.md  # Assisted catalog plus normalized credit metadata
│   └── 10_technical_stack_reference.md    # Full tech stack, algorithms, APIs
├── skills/                        # Generated credit automation skills (one per LEED credit)
│   ├── ip_p3_carbon/             # Each skill: SKILL.md (+ agent.py, calcs, templates, tests)
│   ├── ea_c3_energy_enhanced/
│   ├── ea_c7_refrigerant/
│   ├── ea_p1_op_carbon/
│   ├── ea_p2_energy_min/
│   ├── ea_p5_refrigerant/
│   ├── lt_c1_land_protect/
│   ├── lt_c3_compact/
│   ├── mr_c2_embodied_reduce/
│   ├── mr_p2_embodied/
│   ├── pr_c2_leed_ap/
│   ├── ss_c3_rainwater/
│   ├── ss_c5_heat_island/
│   ├── ss_c6_light_pollution/
│   ├── we_c2_water_enhanced/
│   ├── we_p2_water_min/
│   ├── durable_workflow.py       # Resumable workflow engine
│   ├── hitl_system.py            # Human-in-the-Loop implementation
│   └── SKILL_TEMPLATE.md         # Contract template for new skills
├── Kimi_Agent_LEED v5 Credit Automation/  # SOURCE ARCHIVE — do not edit
└── leed-platform/
    ├── agents/agent_architecture.md
    ├── backend/
    ├── ui/
    ├── infra/
    └── docs/
```

### Multi-Agent Hierarchy

```
Lead Agent (project orchestration)
└── Credit Agents × 16 (one per LEED credit)
    └── Sub-Agents:
        ├── Data Extractor  (parse EnergyPlus, Excel, PDF, CAD)
        ├── Calculation Engine (carbon, water, energy formulas)
        ├── Report Generator (Jinja2 → PDF/Excel)
        └── Review Checker (completeness, math, USGBC formatting)
```

Each Credit Agent extends a `CreditAgent` base class with `execute()`, `validate_inputs()`, `fetch_data()`, `calculate()`, and `generate_documents()` methods.

### Durable Workflow Pattern

Every credit workflow uses `DurableOrchestrator` (`skills/durable_workflow.py`). State is persisted as JSON after each step so workflows survive server restarts, API failures, and long HITL waits.

```python
@step(name="fetch_grid", retry=3, timeout=30)
async def fetch_grid_factors(context, previous_results):
    # Retried automatically on timeout/error; resumes from here after restart
    return await api.call()
```

Workflows have five statuses: `pending → running → paused (HITL) → completed | failed`. When a HITL checkpoint fires, the workflow raises `WorkflowPaused` and halts; it resumes via `orchestrator.resume_after_hitl()` when the human responds.

### Skill Contract

Every skill must follow `skills/SKILL_TEMPLATE.md`, which defines:
- **Metadata:** credit code, automation level %, complexity, HITL required
- **Inputs table:** field, type, source, validation
- **Workflow steps:** each step typed as Validation / API Call / Calculation / Document Generation / Human Review
- **HITL checkpoints table:** reviewer role, SLA hours, review instructions
- **API dependencies table:** regional availability + fallback
- **Output documents table**
- **Test command** and **example usage**

### Production Suite Priority

| Priority | Suite | Credits |
|----------|-------|---------|
| 1 | Water Efficiency | WEp2, WEc2 |
| 2 | Refrigerant Management | EAp5, EAc7 |
| 3 | Quality Plans | EQp1, EQp2 |
| 4 | Integrative Process Assessment | IPp1, IPp2 |
| 5 | Low-Emitting Materials | MRc3 |

Existing generated skills such as PRc2, IPp3, MRp2, MRc2, EAp1, EAp2, EAc3, SSc3, SSc5, SSc6, LTc1, and LTc3 should be treated as assisted catalog workflows until source access, tests, regional fallbacks, and HITL checklists are verified.

### HITL Design Rules

- Every skill has at least one HITL checkpoint
- HITL UI: document preview, review checklist (checkboxes), approve/reject, comments, SLA countdown
- SLA defaults: 24h for standard review, 48h for expert review (energy modeler, GIS analyst, LCA expert)
- On reject, `hitl_result` carries `return_to_step` so the workflow can re-run from the correct point

### Regional Data Handling

Use `get_available_credits(region)` to filter credits by data availability before showing them to the user. Credits that lack required APIs for a region should either show a warning ("manual data entry required") or be hidden. Never claim full automation for a region where APIs are unavailable.

## Key Files to Read First

| File | Why |
|------|-----|
| `MASTER_PLAN.md` | **Start here** — single consolidated source of truth for the entire platform |
| `docs/09_consolidated_credit_catalog.md` | Assisted catalog metadata, APIs, and HITL specs |
| `docs/10_technical_stack_reference.md` | Full tech stack, data models, algorithms, infrastructure |
| `EXECUTIVE_SUMMARY_REALISTIC.md` | Authoritative automation levels + what AI can/cannot do |
| `.instructions.md` | Agent operating principles (realism-first, HITL-first, modular) |
| `skills/durable_workflow.py` | Workflow engine — read before writing any new skill |
| `skills/hitl_system.py` | HITL implementation |
| `skills/SKILL_TEMPLATE.md` | Required contract for every new skill |
| `skills/<slug>/SKILL.md` | Skill-specific contract (16 skills available) |
| `leed-platform/agents/agent_architecture.md` | Full agent hierarchy with code examples |

## Design Principles

1. **Realism over optimism** — always use the realistic automation % from `EXECUTIVE_SUMMARY_REALISTIC.md`, not inflated claims
2. **HITL is not optional** — never design a skill that bypasses human review for compliance-critical outputs
3. **Specialized tools before AI** — use CAD APIs / OCR / structured parsers for data extraction; use AI only for summarization and generation
4. **One skill = one credit** — each skill is independently buildable and testable; avoid cross-skill dependencies
5. **Confidence scoring** — flag low-confidence AI outputs; never silently pass uncertain results to USGBC submission
