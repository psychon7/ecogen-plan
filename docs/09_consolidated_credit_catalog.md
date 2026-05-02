# Ecogen - Consolidated Credit Catalog
## Kimi-Aligned Production Suites Plus Assisted Inventory

**Source:** `Kimi_Agent_LEED v5 Credit Automation/leed_automation_sec00.md`, `leed_automation_sec01.md`, `research/*.md`, `skills/*/SKILL.md`, `EXECUTIVE_SUMMARY_REALISTIC.md`, and `LEED_v5_Realistic_Implementation_Guide.md`.

**Canonical interpretation:** The commercial MVP is not "all 16 generated skills." It is the five Kimi-recommended production suites below, governed by the repository's realism rules: evidence-pack preparation, mandatory HITL, regional source gating, and manual Arc-compatible export in V1.

---

## Production MVP Suites

| Priority | Suite | Credits | Automation Stance | HITL Need | Main Caveats |
|----------|-------|---------|-------------------|-----------|--------------|
| 1 | Water Efficiency | WEp2 + WEc2 | High assisted; deterministic fixture/equipment calculations and WEc2 optimization | LEED consultant validates fixture schedule, occupancy, formulas, and assumptions | Product databases and fixture standards vary by region; manual entry must remain first-class |
| 2 | Refrigerant Management | EAp5 + EAc7 | High assisted; inventory parsing, GWP lookup, leakage/LCCP calculations | MEP/LEED reviewer validates equipment schedule, refrigerant identity, and phase-out flags | AHRI/EPA/global refrigerant data coverage differs by market and manufacturer |
| 3 | Quality Plans | EQp1 + EQp2 | AI-assisted plan generation plus ventilation/source-control calculation support | LEED/IAQ reviewer validates plan scope, HVAC assumptions, filtration/ventilation evidence | Needs official LEED v5 requirement verification and ASHRAE/source licensing before formulas are locked |
| 4 | Integrative Process Assessment | IPp1 + IPp2 | AI-assisted public-source research, synthesis, and narrative drafting | LEED/resilience/equity reviewer validates source selection, findings, and project-specific claims | Regional government datasets vary sharply; confidence must degrade visibly |
| 5 | Low-Emitting Materials | MRc3 | High assisted product screening against certification/VOC evidence | Materials/LEED reviewer validates product matches, certificates, and exceptions | Certification databases can be fragmented, paywalled, stale, or region-specific |

## Prototype Scope

The 14-day effort should be framed as a technical prototype, not a commercial MVP. Current assumption:

| Prototype Credit | Purpose |
|------------------|---------|
| PRc2 | Simplest end-to-end pipeline validation: intake, lookup, HITL, document generation, audit trail |
| WEp2 | First market-facing wedge and foundation for WEc2 |
| EAp5/EAc7 | Shared-input calculation bundle that proves suite review and batch evidence packs |

## Assisted Catalog

These generated Kimi/root skills remain useful as implementation inventory. They should be presented as assisted, prototype, or deferred until source access, tests, regional coverage, and reviewer workflows are proven.

| Credit | Slug | Role | Boundary |
|--------|------|------|----------|
| PRc2 | `pr_c2_leed_ap` | Prototype/reference | High automation only with verified GBCI/directory access; always keep final/exception review |
| SSc6 | `ss_c6_light_pollution` | Assisted | Lighting designer/LEED review of BUG ratings, zones, cut sheets, and controls |
| SSc5 | `ss_c5_heat_island` | Assisted | SRI/material/source verification and site-area review required |
| SSc3 | `ss_c3_rainwater` | Assisted | US precipitation/soil paths strongest; international projects often require manual data |
| MRp2 | `mr_p2_embodied` | Assisted | LCA/takeoff and EPD matching require specialist review |
| MRc2 | `mr_c2_embodied_reduce` | Assisted | Import and validate WBLCA/EPD outputs; do not claim autonomous WBLCA |
| IPp3 | `ip_p3_carbon` | Assisted | Aggregates energy, refrigerant, and materials data; high dependency risk |
| EAp1 | `ea_p1_operational_carbon` | Assisted | Parses completed model outputs and grid factors; energy/carbon reviewer required |
| EAp2 | `ea_p2_energy_min` | Assist-only/deferred | Parse completed qualified model outputs only; no autonomous energy modeling |
| EAc3 | `ea_c3_energy_enhanced` | Assist-only/deferred | Parse completed qualified model outputs only; no autonomous Appendix G modeling |
| LTc3 | `lt_c3_compact` | Assisted | Depends on regional GTFS, density, zoning, and GIS coverage |
| LTc1 | `lt_c1_land_protect` | Assisted | Boundary and overlay interpretation require GIS analyst review, especially outside US datasets |

## Import Rules

1. Keep one independently testable skill per credit, even when credits are sold as suites.
2. Every compliance-critical package requires named human approval before "submission-ready."
3. Automation percentages control review depth and confidence labels, not whether review exists.
4. V1 exports Arc-compatible/manual-upload evidence packs; direct Arc submission remains V2+.
5. Energy-model credits parse completed outputs from qualified modelers; Ecogen does not create or validate energy models autonomously.
6. Regional source support must be modeled per credit/source, not as a platform-wide claim.
7. Kimi `.skill` and `skills/*/SKILL.md` files are draft inputs; normalize slugs, schemas, HITL actions, failure modes, and regional fallbacks before implementation.
