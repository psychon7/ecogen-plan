# Ecogen LEED v5 Automation Plan

This repository is the planning and architecture workspace for Ecogen, a practical LEED v5 automation platform for consultants. The consolidated plan lives in `docs/`; older root reports and the imported Kimi package are retained as evidence and source material.

## Canonical Stance

Ecogen automates documentation, calculation, evidence assembly, and review preparation. It does not replace LEED consultants, licensed engineers, energy modelers, GIS analysts, or project managers.

Non-negotiables:

- Realistic automation target: 70-85% for most supported credits, not 100%.
- Human-in-the-loop review is mandatory for compliance-critical outputs and low-confidence data.
- Specialized tools handle CAD, BIM, GIS, energy models, parsing, and deterministic formulas; AI drafts, summarizes, validates, and routes.
- Regional data availability is a product constraint, especially outside the United States.
- One LEED credit equals one independently testable skill.
- V1 produces Arc-compatible/manual-upload evidence packs. Direct Arc submission is V2 until API access and terms are verified.

## Canonical Docs

| File | Purpose |
|------|---------|
| [docs/00_platform_brief.md](docs/00_platform_brief.md) | Short executive brief and product thesis |
| [docs/01_realistic_automation_model.md](docs/01_realistic_automation_model.md) | Automation tiers, credit scope, capability boundaries |
| [docs/02_product_requirements.md](docs/02_product_requirements.md) | Personas, workflows, MVP requirements, metrics |
| [docs/03_system_architecture.md](docs/03_system_architecture.md) | Target stack, service boundaries, agents, data model |
| [docs/04_data_integrations_and_regionality.md](docs/04_data_integrations_and_regionality.md) | API strategy, source freshness, regional fallbacks |
| [docs/05_skill_contracts_and_credit_catalog.md](docs/05_skill_contracts_and_credit_catalog.md) | Skill schema, credit catalog, migration rules |
| [docs/06_hitl_and_durable_workflows.md](docs/06_hitl_and_durable_workflows.md) | HITL model, durable workflow contract, audit trail |
| [docs/07_delivery_roadmap.md](docs/07_delivery_roadmap.md) | 14-day prototype, five-suite production roadmap, V2 scope |
| [docs/08_decisions_and_open_questions.md](docs/08_decisions_and_open_questions.md) | ADR summary, unresolved decisions, conflict register |
| [docs/source_map.md](docs/source_map.md) | What was merged, superseded, or kept as reference |

## Source Priority

When documents conflict, resolve in this order:

1. `EXECUTIVE_SUMMARY_REALISTIC.md`, `.instructions.md`, `CLAUDE.md`
2. `AGENTS.md` and `LEED_v5_Realistic_Implementation_Guide.md`
3. `leed-platform/decisions/decision_log.md`
4. `leed-platform/` product, architecture, backend, UI, auth, and infrastructure specs
5. `skills/` prototypes and root analysis artifacts
6. `Kimi_Agent_LEED v5 Credit Automation/` as imported research and implementation inspiration

## Current External Anchors

Checked on 2026-05-02:

- USGBC LEED v5 overview: https://www.usgbc.org/leed/v5
- USGBC BD+C one-page fact sheet: https://www.usgbc.org/sites/default/files/2025-05/LEED_LEED-v5-One-Pagers-Fact-Sheet_BD%2BC_v4_DL.pdf
- USGBC LEED v5 FAQ: https://support.usgbc.org/hc/en-us/articles/12169190314003-LEED-v5-FAQ
- USGBC addenda database: https://www.usgbc.org/leedaddenda
