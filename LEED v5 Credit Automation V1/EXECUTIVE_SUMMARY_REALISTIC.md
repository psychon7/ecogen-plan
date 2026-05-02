# LEED v5 AI Automation Platform - Realistic Executive Summary

## The Honest Assessment: What's Really Possible

Ecogen is an AI-assisted LEED v5 documentation platform for consultants. It can reduce repetitive documentation, calculation, evidence assembly, and review-prep work, but it does not replace LEED consultants, energy modelers, LCA practitioners, GIS analysts, commissioning authorities, or final professional judgment.

The newer Kimi research corpus changes the product emphasis. The older plan treated the generated 16-skill set as the MVP. The stronger commercial plan is a suite-based launch: start with high-confidence, repeatable credit families, then keep the 16 generated skills as an assisted catalog and implementation inventory.

| Old Assumption | Updated Position |
|----------------|------------------|
| "100% automation" | Most supported credits are 50-85% automated, with a few deterministic workflows reaching 90%+ before review |
| "16-credit MVP" | Five production MVP suites: WEp2+WEc2, EAp5+EAc7, EQp1+EQp2, IPp1+IPp2, MRc3 |
| "14 days to build MVP" | 14 days is an internal demo/proof; production suite MVP is a multi-month build |
| "AI interprets site plans" | AI cannot reliably interpret CAD/site plans; use CAD/GIS tools plus human verification |
| "Fully autonomous" | Human approval is mandatory for compliance-critical outputs |
| "Works globally" | Data availability is credit-specific and region-specific; manual and assisted modes are first-class paths |

---

## What AI Can Actually Do

### High Confidence

1. Template-driven document generation from structured inputs.
2. Deterministic calculations with explicit formulas and unit tests.
3. Document and spreadsheet parsing where the source structure is known.
4. API/data lookup against verified public, licensed, or customer-provided sources.
5. Evidence pack assembly with source indexes, formula trails, confidence tiers, and review records.

### Medium Confidence

1. OCR extraction from inconsistent PDFs and submittals.
2. Multi-source web research for climate, hazard, demographic, product, or regional data.
3. Matching materials, fixtures, luminaires, or equipment to product databases.
4. Drafting narratives from structured facts.

### Low Confidence / Not Autonomous

1. Energy model creation, calibration, or optimization.
2. Whole-building LCA modeling.
3. Field verification, lab testing, or commissioning execution.
4. Complex CAD/site-plan interpretation without specialized tools.
5. Final compliance decisions or point guarantees.

---

## Kimi-Aligned Credit Priorities

### Production MVP Suites

| Suite | Credits | Automation Posture | Why It Leads |
|-------|---------|--------------------|--------------|
| Water Efficiency | WEp2 + WEc2 | High, calculation-driven | Universal prerequisite, transparent fixture math, clear point-optimization story |
| Refrigerant Management | EAp5 + EAc7 | High, database/calculation-driven | Shared equipment schedule and GWP lookup pipeline |
| Quality Plans | EQp1 + EQp2 | Medium-high, plan/calculation workflow | Repeatable plans and ventilation/filtration checks with reviewer sign-off |
| Integrative Process Assessment | IPp1 + IPp2 | Medium-high, research/narrative workflow | High consultant time burden, public data retrieval, professional judgment retained |
| Low-Emitting Materials | MRc3 | High value, medium build complexity | Large manual product-certification lookup burden across many products |

Water Efficiency should be the first user-facing wedge. Start with manual or spreadsheet fixture input, expose every formula, and add OCR/product matching only after the workflow is trusted.

### Assisted Catalog

These generated skills remain valuable, but should be sold as assisted workflows unless source access, test coverage, regional gating, and review paths are verified:

| Credit | Treatment |
|--------|-----------|
| IPp3 Carbon Assessment | Cross-credit compilation after EAp1, EAp5, and MRp2 inputs are available |
| MRp2 Quantify Embodied Carbon | EPD parsing, matching, and reporting; LCA scope and quantities need expert review |
| MRc2 Reduce Embodied Carbon | Automate EPD/threshold paths; treat WBLCA as external expert-tool output |
| SSc3 Rainwater, SSc5 Heat Island, SSc6 Light Pollution | Useful calculation/document workflows with site/data verification gates |
| LTc3 Compact and Connected Development | Strong in data-rich regions; degrade gracefully where Walk Score/GTFS/local data are weak |
| LTc1 Sensitive Land Protection | US-centric GIS workflow; non-US projects require manual local GIS analysis |
| PRc2 LEED AP | Excellent pipeline proof, but low standalone commercial value |
| EAp1 Operational Carbon | Useful but region-sensitive due to grid factor and projection data |

### Assist-Only / Defer

EAp2, EAc2, and EAc3 should not be positioned as energy modeling automation. Ecogen can parse completed model outputs, check consistency, calculate points from model results, and draft documentation. Qualified modelers still create and validate the models.

---

## Architecture: Skill-Based With Suite Orchestration

Each LEED credit remains independently testable as a skill, but product packaging should group skills into suites where data naturally flows across credits.

```text
skills/
  we_p2_water_min/
  we_c2_water_enhanced/
  ea_p5_refrigerant/
  ea_c7_refrigerant/
  eq_p1_construction_management/        # to create
  eq_p2_fundamental_air_quality/        # to create
  ip_p1_climate_resilience/             # to create
  ip_p2_human_impact/                   # to create
  mr_c3_low_emitting_materials/         # to create
  assisted_catalog/
    ip_p3_carbon/
    mr_p2_embodied/
    mr_c2_embodied_reduce/
    ea_p2_energy_min/
    ea_c3_energy_enhanced/
```

Every skill contract should include:

- Required inputs and accepted manual fallbacks.
- Data/API dependencies with regional availability.
- Calculation and validation steps.
- Confidence scoring and degradation reasons.
- HITL checkpoints with reviewer role and SLA.
- Output evidence pack manifest.
- Tests for inputs, calculations, failure paths, HITL pause/resume, and regional fallback.

---

## Human-in-the-Loop Design

Automation percentage changes review depth, not whether review exists. Every compliance-critical package needs human approval before it becomes submission-ready.

| Workflow | Review Owner | Review Focus |
|----------|--------------|--------------|
| WEp2/WEc2 | LEED consultant | Fixture schedule completeness, occupancy assumptions, formula results |
| EAp5/EAc7 | LEED consultant or MEP reviewer | Equipment schedule coverage, refrigerant types, charges, GWP assumptions |
| EQp1/EQp2 | Contractor, energy/MEP reviewer, LEED AP | Plan commitments, VRP calculations, filtration and project-type assumptions |
| IPp1/IPp2 | LEED AP/project lead | Hazard/demographic source relevance, local context, narrative accuracy |
| MRc3 | LEED/materials reviewer | Product category assignment, certification validity, exception handling |
| Energy modeling credits | Energy modeler | Model output correctness, baseline/proposed mapping, point calculation |
| Embodied carbon/WBLCA | LCA practitioner | Scope, quantities, EPD matching, tool output consistency |
| GIS/site credits | GIS/planning reviewer | Boundary, dataset currency, local interpretation |

---

## Regional Data Availability

Regional support must be evaluated per credit and per data source.

| Region Pattern | Product Behavior |
|----------------|------------------|
| Full source coverage | Show as high-confidence automation with normal review |
| Partial source coverage | Show as assisted mode with explicit missing-source warnings and manual fields |
| Weak/no source coverage | Hide the automation claim or offer manual evidence pack assembly |
| API/license unverified | Keep behind feature flag until terms, rate limits, and source quality are confirmed |

Examples:

- LTc1 is US-first because FEMA/NWI/USFWS/NRCS/PAD-US sources are US federal datasets.
- LTc3 degrades outside US/Canada/Australia because Walk Score and GTFS coverage vary.
- EAp1 depends on grid factor and future projection sources; non-US workflows need regional source routers or manual overrides.
- Refrigerant GWP data is broadly global, but AHRI/EPA SNAP and regional phase-out rules vary.

---

## Delivery Roadmap

### 14-Day Internal Demo

Purpose: prove project intake, skill execution, evidence pack export, audit trail, and HITL pause/resume. This is not the commercial MVP.

Recommended demo path:

1. PRc2 as the simplest pipeline proof.
2. WEp2 as the first commercial wedge.
3. EAp5/EAc7 to prove shared input reuse.
4. One assisted skill such as MRp2 or IPp3 to prove reviewer-heavy workflows.

### Production MVP: Five Suites

| Phase | Scope | Notes |
|-------|-------|-------|
| Phase 1 | WEp2/WEc2, EAp5/EAc7, EQp1 first pass | Build shared parsing, calculation, evidence pack, and HITL foundations |
| Phase 2 | EQp2, IPp1/IPp2, MRc3 | Add ASHRAE table handling, public data research agents, product-certification lookup |
| Phase 3 | Cross-suite integration and beta hardening | Confidence tiers, regional source routers, reviewer dashboard, customer pilots |

The Kimi-aligned production roadmap is closer to months than days. The fast demo is still useful, but it should not be described as production-ready automation.

---

## Investment And Returns

### Development Model

- 14-day demo: small team, mocked/sandboxed APIs, limited evidence pack output.
- Production suite MVP: 4-6 engineers plus LEED/product review support over multiple phases.
- Ongoing cost drivers: document parsing, API subscriptions, source caching, evidence storage, LLM usage, reviewer workflow operations.

### Business Value

- Strongest near-term paid wedge: Water Efficiency suite.
- Highest product-value follow: MRc3 due to product-certification lookup burden.
- Best trust builder: transparent formulas, source citations, reviewer approval records.
- Most important sales caveat: Ecogen prepares evidence packs and accelerates review; it does not guarantee points.

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Overstating automation | Use "draft", "assist", "evidence pack", and "review-ready"; avoid "fully automated" |
| Regional data gaps | Source routers, manual fallback fields, visible availability badges |
| Hallucinated narratives | Source-grounded generation and requirement-to-evidence matrix |
| Calculation errors | Versioned formulas, golden test fixtures, spreadsheet audit trails |
| Reviewer rejection | Human checklist, confidence tier, exception report, reviewer notes |
| API/licensing uncertainty | Feature flags until source access and terms are verified |

---

## Success Metrics

### Technical

- Calculation accuracy: 99% on unit-tested deterministic formulas.
- Evidence pack completeness: 95% for required sections before human approval.
- Source traceability: 100% of factual claims tied to upload, API source, or reviewer entry.
- HITL completion: SLA compliance tracked per reviewer role.

### Business

- Water Efficiency suite time saved: target 60-80% of documentation effort after manual input.
- Production MVP suite time saved: target 94-152 consultant-hours/project only after source access and workflows are verified.
- Reviewer confidence: reduction in missing evidence and reviewer rework.
- Consultant capacity: more projects per consultant without removing professional accountability.

---

## The Bottom Line

### What We're Building

A suite-based LEED v5 evidence automation platform that prepares source-grounded, calculation-backed, review-ready documentation packages with mandatory human approval.

### What We're Not Building

- A fully autonomous LEED consultant.
- A direct USGBC submission robot in V1.
- An energy modeler, LCA practitioner, GIS analyst, or commissioning authority replacement.
- A global automation claim that ignores regional data gaps.

### Next Steps

1. Update platform docs and seed catalogs to present the Kimi-aligned suite roadmap.
2. Create missing skill drafts for IPp1, IPp2, MRc3, EQp1, and EQp2.
3. Keep existing 16 skill drafts as an assisted catalog with explicit regional and HITL caveats.
4. Verify official LEED v5 source licensing, addenda workflow, API access, and product database terms.
5. Build the first paid wedge around WEp2/WEc2 with transparent formulas and manual upload fallback.

---

*Document Version: 2.0*
*Updated: May 2, 2026*
*Primary alignment source: Kimi LEED v5 credit automation research corpus plus Ecogen realism guardrails*
