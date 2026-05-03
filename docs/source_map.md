# Consolidation Source Map

## Purpose

This file records how the old root plans and the imported Kimi plan were consolidated. It should be updated whenever a legacy document is promoted, retired, or contradicted by newer evidence.

## Primary Policy Sources

| Source | Canonical Use |
|--------|---------------|
| `EXECUTIVE_SUMMARY_REALISTIC.md` | Automation realism, HITL stance, Kimi-aligned suite roadmap, regional support tiers |
| `LEED_v5_Realistic_Implementation_Guide.md` | Detailed capability boundaries, skill architecture, durable workflow patterns |
| `.instructions.md` | Agent and product operating principles: realism, human judgment, modularity, regional variation |
| `CLAUDE.md` | Development stack, skill rules, HITL rules, key files, automation tier guidance |
| `AGENTS.md` | Repository-specific preservation rule for realistic automation, mandatory review, regional variability, and one skill per credit |
| `leed-platform/decisions/decision_log.md` | Accepted architecture decisions, prototype-vs-commercial scope, Arc deferral |

## Product And Architecture Sources

| Source | Merged Into |
|--------|-------------|
| `leed-platform/docs/product_overview.md` | `02_product_requirements.md`, `07_delivery_roadmap.md` |
| `leed-platform/docs/user_personas.md` | `02_product_requirements.md` |
| `leed-platform/agents/agent_architecture.md` | `03_system_architecture.md`, `06_hitl_and_durable_workflows.md` |
| `leed-platform/backend/api_spec.yaml` | `03_system_architecture.md`, implementation references |
| `leed-platform/backend/db_schema.sql` | `03_system_architecture.md`, implementation references |
| `leed-platform/ui/` and `leed-platform/ux/` | `02_product_requirements.md`, `06_hitl_and_durable_workflows.md` |
| `leed-platform/infra/deployment_architecture.md` | `03_system_architecture.md` |

## Kimi Sources Promoted As Design Material

| Kimi Source | Promoted Idea | Caveat |
|-------------|---------------|--------|
| `LEED_v5_Credit_Automation_Analysis.md` | 51-credit research matrix, water efficiency wedge, evidence pack standard, confidence tiers | Not canonical credit scope; citation system incomplete |
| `LEED_v5_Technical_Implementation.md` | API client layer, cache tiers, fallback chains, LangGraph state machine, testing gates | Timelines and Tier 1 automation claims require realism correction |
| `skills/*/SKILL.md` | Rich per-skill workflow details, regional availability tables, output artifacts, HITL checklists | Keep repo slug names and realistic percentages; generated 16-skill set is assisted catalog/inventory, not the commercial MVP promise |
| `tech_impl_sec03.md` | Retry/backoff, rate limiting, circuit breakers, HITL channel design | API assumptions must be verified before build |
| `tech_impl_sec04.md` | Production roadmap structure | Reconciled with 14-day prototype, five-suite commercial MVP, and V2 Arc deferral |

## Superseded Or Reference-Only Material

Keep these files for provenance, but do not use them as product truth without the canonical docs:

- `EXECUTIVE_SUMMARY.txt`
- `LEED_v5_Implementation_Guide.txt`
- `data_flow_architecture.md`
- `leed-platform-v2/docs/IMPLEMENTATION_GUIDE.md` *(New Architecture)*
- `INTEGRATION_ANALYSIS_FINAL_REPORT.md`
- `integration_feasibility_summary.md`
- Root `.json`, `.txt`, `.xlsx`, `.png`, and `.docx` analysis artifacts
- `Kimi_Agent_LEED v5 Credit Automation/`
- `Kimi_Agent_LEED v5 Credit Automation.zip`

## Conflict Resolutions

| Conflict | Canonical Resolution |
|----------|----------------------|
| 100% automation vs realistic automation | Use 70-85% as the platform target; 95% only for narrow deterministic workflows with exception review |
| 51-credit broad automation vs generated 16-skill catalog | Treat the 51-credit work as research and the generated 16-skill catalog as assisted implementation inventory; commercial MVP starts with Kimi's five production suites |
| Old 14-day/12-credit MVP claim vs commercial MVP | Use 14 days only as a technical prototype target for workflow state, HITL, evidence export, and a small skill set; production hardening, test coverage, source verification, and regional fallback UX belong to the five-suite commercial roadmap |
| Direct Arc submission in MVP vs manual upload | V1 exports Arc-compatible/manual-upload evidence packs; direct Arc submission is V2 after access verification |
| LTc1 high automation vs US-only GIS limits | LTc1 is 60% realistic and high-risk outside the US |
| EAc3 high automation vs energy modeler judgment | EAc3 is 70% realistic and requires expert energy modeler review |
| PRc2 no HITL vs mandatory review stance | PRc2 remains 95% automated but includes a lightweight final/exception review checkpoint |
