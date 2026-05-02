# Delivery Roadmap

## Timeline Reconciliation

The old and new plans contain three different timelines: a 14-day prototype, a 10-week hardening plan, and an 8-month/18-month expansion. The Kimi research makes the product boundary clearer: 14 days can prove workflow mechanics, but the commercial production MVP should be the five-suite scope.

- 14-day demo: prove end-to-end flow with a small credit set and manual export.
- Production MVP: ship the five Kimi-aligned suites with source verification, tests, regional gating, confidence scoring, and reviewer workflows.
- Assisted catalog: expose the generated 16-skill inventory only where source access, regional fallback, and review checklists are ready.
- V2 and beyond: direct Arc integration, deeper regional expansion, more credits, enterprise controls.

## Phase 0: Consolidation And Source Verification

Duration: 1 week.

Deliverables:

- Canonical docs and source map.
- Confirm official LEED v5 requirement sources and addenda workflow.
- Verify access assumptions for Arc, GBCI, EC3, product databases, Walk Score, and GIS APIs.
- Normalize `SKILL_TEMPLATE.md` to the extended contract.

## Phase 1: 14-Day Demo

Goal: demonstrate the core user journey, not full production readiness.

Recommended proof credits:

- PRc2 as the simplest pipeline proof.
- WEp2 as the first commercial wedge.
- EAp5/EAc7 to prove shared-input reuse.
- One assisted workflow such as MRp2 or IPp3 to prove expert review and confidence handling.

Deliverables:

- Project intake and credit selector.
- Durable workflow prototype wired to persisted state.
- HITL task creation and approval/rejection flow.
- Manual-upload evidence pack export.
- Mocked or sandboxed API clients for all external sources.
- Golden calculation tests for demo formulas.

Water Efficiency should be the first user-facing wedge inside this demo: manual/spreadsheet fixture input first, transparent WEp2 calculations, then WEc2 optimization once shared data structures are stable.

## Phase 2: Production MVP, Foundation

Focus:

- Platform foundation: FastAPI, PostgreSQL/PostGIS, Redis, object storage, worker queue.
- Auth, organization/project RBAC, upload service, document storage.
- Shared API client base: retry, timeout, cache, rate limit, fallback, source metadata.
- Shared skill runtime and HITL service.
- Productionize WEp2/WEc2, EAp5/EAc7, and EQp1 first-pass workflows with tests, fixtures, and evidence pack format.

Exit criteria:

- Every production workflow has schema tests, calculation tests, API failure tests, HITL tests, and artifact contract tests.
- Direct Arc upload remains disabled; manual export works.

## Phase 3: Production MVP, Suite Expansion

Focus:

- Add EQp2, IPp1/IPp2, and MRc3.
- Build regional filtering middleware.
- Add confidence scoring, evidence ledger, and audit export.
- Add reviewer dashboard, SLA escalation, and batch review.
- Add observability: workflow, API, document generation, HITL bottlenecks.

Exit criteria:

- Five suites are documented, normalized, testable, and region-gated.
- Assisted catalog skills remain behind capability labels until parsers, source access, and HITL checklists are verified.
- High-risk credits clearly run in assisted/manual mode.
- All output packages include source index, confidence tier, and review record.

## V2 Scope

- Direct Arc submission only after verified API write access, schema, permissions, rate limits, and terms.
- Additional credit families from the 51-credit Kimi research matrix.
- Regional source routers for Canada, UK/EU, Australia/NZ, and selected APAC markets.
- Enterprise controls: SSO, audit exports, retention policies, admin source-health dashboard.

## Team Model

| Track | Owner | Focus |
|-------|-------|-------|
| Frontend | 1 engineer | Project dashboard, credit wizard, HITL review, evidence preview |
| Backend/API | 1 engineer | FastAPI, data model, auth, uploads, workflow APIs |
| Skill runtime | 1 engineer | Durable workflow, HITL, artifact generation, tests |
| Credit skills | 2 engineers | Credit implementations, fixtures, API clients, calculations |
| Product/LEED reviewer | Fractional | Requirement verification, review checklists, acceptance criteria |
