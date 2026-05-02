# Skill Contracts And Credit Catalog

## Directory Standard

Use the repo's existing slug convention. Do not migrate Kimi `leed-*` directory names as canonical.

```text
skills/<credit_slug>/
  SKILL.md
  schemas.py
  agent.py
  calculations.py
  clients.py
  templates/
  fixtures/
  tests/
```

## Required SKILL.md Sections

Each skill contract must include:

- Metadata: credit code, name, rating system, points, realistic automation level, complexity, owner, HITL required.
- Purpose: one concise paragraph.
- Input schema: human-readable table plus machine schema reference.
- Output schema: artifacts, JSON summary, evidence records, confidence scores.
- Durable workflow: step id, step type, dependencies, retry, timeout, output contract, failure behavior.
- HITL checkpoints: reviewer role, SLA, checklist, approval criteria, rejection route, escalation.
- API dependencies: source, auth, region, fallback, rate limit, cache TTL, verification date.
- Regional availability: full, limited, manual, unavailable.
- Error handling: retry, manual correction, pause, fail, escalation.
- Evidence and audit trail: source ids, artifact hashes, calculation formulas, reviewer signatures.
- Acceptance criteria: what must be true before package export.
- Tests and fixtures: test command and fixture inventory.

Each `schemas.py` must define, at minimum:

- `InputSchema` with `schema_version`, `leed_requirement_version`, and credit-specific fields.
- `OutputSchema` with status, artifacts, evidence records, confidence breakdown, and reviewer approvals.
- `EvidenceRecord` with source id, source version/date, extraction method, artifact hash, and confidence.
- `HITLReviewSchema` with reviewer role, checklist results, action, comments, signature metadata, and `return_to_step`.

Fixtures must include one happy path, one missing/invalid input case, one API failure/fallback case, and one HITL request-changes case.

Each skill evidence pack must map to the 12-section package standard in `docs/02_product_requirements.md`.

## Kimi-Aligned Production Suites

The commercial MVP is suite-based. The generated 16-skill catalog remains useful implementation inventory, but it is not the production scope promise.

| Suite | Canonical skills | Automation stance | Primary work | HITL |
|-------|------------------|-------------------|--------------|------|
| Water Efficiency | `we_p2_water_min`, `we_c2_water_enhanced` | High assisted, deterministic calculations | Fixture schedule intake, baseline/design water use, WEc2 point optimization | LEED consultant validates schedule, occupancy, formulas, and regional source substitutions |
| Refrigerant Management | `ea_p5_refrigerant`, `ea_c7_refrigerant_enhanced` | High assisted, rule/calculation heavy | Refrigerant inventory parsing, GWP lookup, leakage/LCCP checks | MEP/LEED reviewer validates equipment schedule, refrigerant identity, regional phase-out flags |
| Quality Plans | `eq_p1_construction_management`, `eq_p2_fundamental_air_quality` | AI-assisted plan/calculation workflows | Construction management plan, IAQ requirements, ventilation/source-control evidence | LEED/IAQ reviewer validates plan scope, HVAC assumptions, and project-specific applicability |
| Integrative Process Assessment | `ip_p1_climate_resilience`, `ip_p2_human_impact` | AI-assisted research and narrative synthesis | Public-source hazard, climate, demographic, and impact assessment evidence | LEED consultant or resilience/equity reviewer validates source fit and narrative claims |
| Low-Emitting Materials | `mr_c3_low_emitting_materials` | High assisted product screening | Product inventory parsing and certification/VOC compliance lookup | Materials/LEED reviewer validates product matches, certificates, and regional database coverage |

`WEp2` should be the first user-facing wedge. `PRc2` remains a good pipeline proof because it exercises intake, external lookup, HITL, and document generation with low calculation risk.

## Assisted Catalog

The older Kimi/generated skill set is still valuable, but these skills should be labeled as assisted, prototype, or deferred until source access, regional coverage, tests, and reviewer UX are proven.

| Slug | Credit | Current Role | Boundary |
|------|--------|--------------|----------|
| `pr_c2_leed_ap` | PRc2 | Prototype/reference skill | Degrades to manual credential verification when GBCI lookup is unavailable |
| `ss_c6_light_pollution` | SSc6 | Assisted catalog | Needs lighting designer review of BUG ratings, zones, and controls |
| `ss_c5_heat_island` | SSc5 | Assisted catalog | Needs SRI/source verification and site/material review |
| `ss_c3_rainwater` | SSc3 | Assisted catalog | Strong US data path; limited/manual outside covered precipitation and soil datasets |
| `mr_p2_embodied` | MRp2 | Assisted catalog | Requires LCA/takeoff review and verified EPD/source matching |
| `ip_p3_carbon` | IPp3 | Assisted catalog | Aggregates energy, refrigerant, and material inputs; do not sell as autonomous carbon compliance |
| `mr_c2_embodied_reduce` | MRc2 | Assisted catalog | Import and validate WBLCA/EPD outputs; do not perform full WBLCA autonomously |
| `ea_p1_operational_carbon` | EAp1 | Assisted catalog | Parse model outputs and grid factors; requires energy/carbon reviewer |
| `ea_p2_energy_min` | EAp2 | Assist-only/deferred | Parse completed qualified model outputs only; no autonomous energy modeling |
| `ea_c3_energy_enhanced` | EAc3 | Assist-only/deferred | Parse completed qualified model outputs only; no autonomous Appendix G modeling |
| `lt_c3_compact` | LTc3 | Assisted catalog | Depends on regional GTFS, density, zoning, and GIS coverage |
| `lt_c1_land_protect` | LTc1 | Assisted catalog | US GIS path strongest; manual/GIS analyst review required for boundary and overlay interpretation |

Only four root skills currently exist. Kimi provides richer drafts for many missing or renamed slugs, but they must be normalized, de-risked, and corrected before becoming canonical.

PRc2 remains listed at 95% only when credential verification is available through an API or verified directory snapshot. If GBCI lookup access is unavailable, PRc2 degrades to assisted/manual verification while retaining the same evidence-pack and HITL requirements.

## Kimi Normalization Matrix

When importing Kimi drafts, use this mapping and overwrite Kimi-specific assumptions:

| Kimi directory | Canonical slug | Canonical automation | Required corrections |
|----------------|----------------|----------------------|----------------------|
| `leed-pr-c2-leed-ap` | `pr_c2_leed_ap` | 95% | Keep HITL final/exception review; remove alternate test path aliases |
| `leed-ip-p3-carbon` | `ip_p3_carbon` | 85% | Replace 92.5%; remove direct Arc submit step; use package export plus human approval |
| `leed-ea-c3-energy-enhanced` | `ea_c3_energy_enhanced` | 70% | Replace 87.7%; emphasize energy modeler review cannot be bypassed |
| `leed-lt-c1-sensitive-land` | `lt_c1_land_protect` | 60% | Replace 87.6%; remove any auto-approval-on-timeout behavior |
| Kimi EQ/IP/MRc3 research docs | `eq_p1_*`, `eq_p2_*`, `ip_p1_*`, `ip_p2_*`, `mr_c3_*` | TBD by suite contract | Create new skill drafts from research before claiming production coverage |
| all Kimi `leed-*` dirs | repo `snake_case` slug | canonical table value | Rename examples to `skills/<canonical_slug>/tests/`; add schemas and fixtures before implementation |

## Migration Rules

1. Keep realistic automation percentages from the root docs.
2. Keep the repo's `snake_case` skill directory names.
3. Import useful Kimi workflow details only after removing direct Arc submission assumptions from V1.
4. Add schemas and fixtures before implementing a skill.
5. Every skill needs at least one HITL checkpoint, even if it is an exception/final review.
6. Every formula must have source/version metadata and golden tests.
7. Every external source must have fallback and manual-entry behavior.

## Test Contract

Each skill must include tests for:

- Input validation and missing fields.
- Formula correctness and unit conversions.
- API timeout, 429, 500, malformed response, auth failure.
- Regional fallback and manual data paths.
- HITL approve, reject, request changes, SLA escalation.
- Workflow reload after persisted state.
- Artifact names, checksums, evidence ids, and output schema.
