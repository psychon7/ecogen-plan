# Decisions And Open Questions

## Accepted Decisions

| ADR | Decision | Consolidated Interpretation |
|-----|----------|-----------------------------|
| ADR-001 | Use Deer-Flow as foundation | Use Deer-Flow conventions behind an internal skill runtime abstraction; verify version-specific claims before build |
| ADR-002 | PostgreSQL with PostGIS | Required for project data, JSONB workflow state, and GIS queries |
| ADR-003 | FastAPI backend | Python-native async API layer for workflow and integration calls |
| ADR-004 | React + TypeScript frontend | Standard web app stack for dashboards and review UI |
| ADR-005 | HITL for complex credits | Expand to HITL for every compliance-critical package, with lightweight review for low-risk credits |
| ADR-006 | Regional credit filtering | Required before showing automation status to users |
| ADR-007 | JWT authentication | Keep with RBAC and project-level permissions |
| ADR-008 | S3 document storage | Use versioned object storage for uploads and generated artifacts |
| ADR-009 | Celery + RabbitMQ workers | Use for long-running workflow, parsing, and document generation jobs |
| ADR-010 | Freemium pricing | Proposed, not canonical; keep pricing open |
| ADR-011 | Prototype timeline vs commercial MVP | 14 days is a technical prototype target for workflow state, HITL, evidence pack export, and a small skill set. The commercial MVP is Kimi's five-suite scope, not the generated 16-skill catalog |
| ADR-012 | No USGBC integration in V1 | Canonical: V1 manual export, V2 direct Arc only after verification |

## Open Questions

| Question | Why It Matters | Owner |
|----------|----------------|-------|
| Which official LEED v5 reference/source files are licensed for internal use? | Skills need requirement traceability and addenda updates | Product/legal |
| What Arc API access is actually available for write/upload workflows? | Determines V2 submission automation | Partnerships/backend |
| Is GBCI credential lookup API accessible for PRc2? | PRc2 may need manual verification fallback | Backend/product |
| What EC3/One Click LCA production terms apply? | Carbon skills depend on material data access | Product/legal |
| Should `EAp2` be in V1.5 or remain assist-only until energy model parsers mature? | Prevents overpromising energy automation | LEED/engineering |
| Which regional markets launch after the US? | Determines source router priorities | Product |
| Which pricing model is canonical? | Old docs disagree: per-credit/project/subscription vs freemium/pro | GTM |
| Do Kimi 51-credit matrix scores map to current USGBC LEED v5 requirements? | Requires official verification before broader roadmap | Research |
| What is the build order for the missing Kimi priority skills? | EQp1, EQp2, IPp1, IPp2, and MRc3 are commercial MVP suites but are not fully represented in the older generated 16-skill catalog | Product/engineering |

## Near-Term Decisions Needed

1. Adopt the extended `SKILL.md` schema and update `skills/SKILL_TEMPLATE.md`.
2. Decide the exact prototype skill set; current assumption is PRc2 for pipeline validation, WEp2 for the first wedge, and EAp5/EAc7 for a shared-input workflow.
3. Select the first production evidence pack format and artifact manifest schema.
4. Verify official LEED v5 requirement/addenda workflow.
5. Confirm API/source access for the production suites: WaterSense, ENERGY STAR, EPA SNAP/IPCC/AHRI, EQ material/IAQ plan references, public integrative-process data sources, and GREENGUARD/FloorScore/HPD/Declare sources for MRc3.
