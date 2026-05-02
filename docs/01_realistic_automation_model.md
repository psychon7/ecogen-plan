# Realistic Automation Model

## Core Principle

Ecogen automates the repeatable parts of LEED documentation. It does not automate professional accountability. The canonical range is 70-85% automation for most supported credits, with higher percentages only for deterministic, low-risk workflows and lower percentages for expert-heavy credits.

## Capability Boundaries

| Work Type | Reliability | Use In Ecogen | Boundary |
|-----------|-------------|---------------|----------|
| Template document generation | High | Draft reports, forms, narratives, checklists | Human verifies content accuracy |
| API integrations | High when documented | Fetch credential, product, climate, GIS, emissions, and material data | API access, terms, region, freshness must be verified |
| Deterministic calculations | High | Water, carbon, refrigerant, heat island, light pollution, point calculations | Formula source must be explicit and tested |
| Structured extraction | Medium-high | Excel, CSV, XML, structured PDFs, known model outputs | Low-confidence extraction routes to review |
| CAD/BIM/GIS interpretation | Medium | Use AutoCAD/Revit/IFC/ArcGIS/PostGIS tooling first | AI cannot be the measurement authority |
| Energy modeling review | Low-medium | Parse outputs and prepare comparison documentation | Energy modeler remains accountable |
| Regulatory compliance judgment | Low | Provide evidence and draft rationale | Human sign-off required |

## Automation Tiers

| Tier | Range | Pattern | Examples |
|------|-------|---------|----------|
| Production suites | 70-90% draft automation | Shared data pipelines, deterministic calculations, templates, named review | WEp2/WEc2, EAp5/EAc7, EQp1/EQp2, IPp1/IPp2, MRc3 |
| Assisted catalog | 50-85% | Useful generated skills with explicit source, regional, and review caveats | PRc2, IPp3, MRp2, MRc2, EAp1, SSc3, SSc5, SSc6, LTc1, LTc3 |
| Output-parser only | Assist-only | Parse completed specialist outputs; do not automate core professional work | EAp2, EAc2, EAc3, WBLCA-heavy paths |
| Not MVP | Variable | Physical testing, custom field verification, high legal/professional judgment | EQc5, SSp1, commissioning execution, highly project-specific credits |

## Kimi-Aligned Production Suites

| Suite | Credits | Review Owner | Release |
|-------|---------|--------------|---------|
| Water Efficiency | WEp2, WEc2 | LEED consultant | Production MVP |
| Refrigerant Management | EAp5, EAc7 | LEED consultant or MEP reviewer | Production MVP |
| Quality Plans | EQp1, EQp2 | Contractor, MEP/energy reviewer, LEED AP | Production MVP |
| Integrative Process Assessment | IPp1, IPp2 | LEED AP/project lead | Production MVP |
| Low-Emitting Materials | MRc3 | LEED/materials reviewer | Production MVP |

## Assisted Catalog

| Credit | Name | Realistic Automation | Complexity | Review Owner | Release |
|--------|------|----------------------|------------|--------------|---------|
| PRc2 | LEED AP | 95% | Low | LEED consultant or PM exception review | Demo/proof |
| SSc6 | Light Pollution Reduction | 90% | Low | LEED consultant | Assisted |
| SSc5 | Heat Island Reduction | 85% | Medium | LEED consultant | Assisted |
| IPp3 | Carbon Assessment | 70% | Medium | LEED consultant plus carbon reviewer as needed | Assisted |
| MRp2 | Quantify Embodied Carbon | 85% | Medium | LCA reviewer | Assisted |
| EAp1 | Operational Carbon Projection | 80% | Medium | Energy/carbon reviewer | V1.5 |
| SSc3 | Rainwater Management | 80% | Medium | Civil/GIS reviewer | V1.5 |
| EAp2 | Minimum Energy Efficiency | Assist-only | High | Energy modeler | Deferred/parser |
| EAc3 | Enhanced Energy Efficiency | Assist-only | High | Energy modeler | Deferred/parser |
| MRc2 | Reduce Embodied Carbon | 80% | High | LCA expert | V2 |
| LTc3 | Compact and Connected Development | 75% | High | Planner/GIS reviewer | V2 |
| LTc1 | Sensitive Land Protection | 60% | High | GIS analyst | V2 |

## Regional Automation

| Region | Support Model | Expected Automation |
|--------|---------------|---------------------|
| United States | Most public APIs, GIS datasets, product sources, grid factors available | 80-85%+ for supported catalog |
| Canada, UK, EU, Australia, New Zealand | Substitute regional data where available; some manual inputs | 70-80% |
| Other regions | Manual data entry, static datasets, local expert sourcing | 50-60% |

Regional filtering is required before a user sees a credit as automatable. If required APIs are unavailable, the product should either show a warning, switch to assisted/manual mode, or hide the skill.

## LEED Version Watch

LEED v5 is active and current guidance can change through addenda. Every skill must store:

- LEED version and rating system.
- Requirement source/version date.
- Formula/table source and addenda date.
- Last verification date for APIs and static datasets.
- Migration notes when USGBC updates forms, calculators, or credit language.
