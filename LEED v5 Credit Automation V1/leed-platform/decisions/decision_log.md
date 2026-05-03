# Decision Log

## ADR-001: Use OpenAI Agents SDK + Restate as Foundation

**Status:** Accepted

**Context:**
We need a workflow orchestration system for credit automation. Options considered: build from scratch, use OpenAI Agents SDK + Restate, or use a general workflow engine such as Temporal.

**Decision:**
Use OpenAI Agents SDK + Restate as the foundation for agent and workflow patterns.

**Rationale:**
- Provides much of the needed skill, HITL, and durable workflow scaffolding.
- Aligns with the skill-based architecture.
- Built on LangGraph patterns.
- Reduces early implementation time.

**Tradeoffs:**
- Faster time to market and reusable patterns.
- Less control over internals.
- May require forking or extension for production-grade review workflow.

---

## ADR-002: PostgreSQL With PostGIS

**Status:** Accepted

**Context:**
Need structured data storage plus geographic queries for location-based credits.

**Decision:**
Use PostgreSQL 15+ with the PostGIS extension.

**Rationale:**
- PostGIS supports location-based credits and regional checks.
- JSONB supports flexible credit and evidence payloads.
- ACID behavior is useful for audit records and workflow state.

---

## ADR-003: FastAPI For Backend

**Status:** Accepted

**Context:**
Need a Python API layer for credit workflows, uploads, calculations, review tasks, and exports.

**Decision:**
Use FastAPI.

**Rationale:**
- Native async support for external APIs and workflow polling.
- Strong typing and OpenAPI generation.
- Fits the Python skill and calculation ecosystem.

---

## ADR-004: React + TypeScript Frontend

**Status:** Accepted

**Context:**
Need a frontend framework for consultant dashboards, evidence pack review, and HITL queues.

**Decision:**
Use React with TypeScript.

**Rationale:**
- Large ecosystem for document viewers, grid components, forms, and data visualization.
- Strong typing for review task and evidence pack contracts.
- Hiring and component-library advantages.

---

## ADR-005: HITL Required For Evidence Packs

**Status:** Accepted

**Context:**
Compliance-critical LEED outputs require professional accountability. Automation level can reduce review effort, but it must not remove human sign-off. Credits such as energy efficiency, embodied carbon, GIS/site analysis, and legal/process documents also require specialist review.

**Decision:**
Require at least one named human approval gate before any evidence pack is marked submission-ready. Automation percentage determines review depth and reviewer specialty, not whether review exists.

**Rationale:**
- Energy modeling requires expert verification.
- Compliance decisions need human accountability.
- Source, calculation, and narrative quality must be traceable.
- Named review builds trust and reduces liability.

**Tradeoffs:**
- Higher accuracy and accountability.
- Slower than unattended automation.
- Requires reviewer availability, escalation, and reassignment handling.

---

## ADR-006: Regional Credit Filtering

**Status:** Accepted

**Context:**
Credit feasibility depends on data availability by region. US coverage is strongest; other regions often require source substitution, static datasets, manual entry, or manual-preparation handoff.

**Decision:**
Filter and label credits by regional data availability.

**Implementation:**
- Detect region from project location.
- Show full, limited/manual-input, unavailable, or manual-prep status by credit.
- Mark data substitutions, stale sources, and manual assumptions in the evidence pack.

---

## ADR-007: JWT For API Authentication

**Status:** Accepted

**Context:**
Need authentication for API access.

**Decision:**
Use JWT access tokens with refresh tokens.

**Rationale:**
- Stateless and compatible with API clients.
- Common pattern for FastAPI applications.

---

## ADR-008: Object Storage For Documents

**Status:** Accepted

**Context:**
Need to store uploads, generated PDFs, spreadsheets, document previews, and evidence pack exports.

**Decision:**
Use S3 or cloud-equivalent object storage with versioning.

**Rationale:**
- Scalable, durable artifact storage.
- Supports immutable file hashes and audit references.
- Lifecycle policies can control cost.

---

## ADR-009: Celery + RabbitMQ For Workers

**Status:** Accepted

**Context:**
Need background processing for uploads, parsing, external API calls, calculations, and document generation.

**Decision:**
Use Celery with RabbitMQ for worker orchestration for distributed task execution.

**Rationale:**
- Mature Python worker ecosystem.
- Supports retries and priority queues.
- Workers can scale independently.

---

## ADR-010: Suite-Based Pricing Hypothesis

**Status:** Proposed

**Context:**
Need a business model for monetization. Kimi research points to value clustering around credit suites, not isolated free credits.

**Decision:**
Use suite-based packaging as the current hypothesis. Starter includes one suite for boutique consultancies; Professional includes the five commercial MVP suites; Enterprise adds integrations, firm templates, API access, and volume pricing. Treat the old free-tier idea as an unvalidated growth experiment, not the default plan.

**Rationale:**
- Credit suites map to consultant workflows and data dependencies.
- Pricing can track review-ready evidence pack value and time saved.
- Enterprise buyers are likely to value review workflow, audit trail, and integrations.
- Avoids implying low-risk self-serve automation before review controls are proven.

---

## ADR-011: Prototype Timeline Vs Commercial MVP Scope

**Status:** Accepted

**Context:**
Need to ship quickly to validate market while avoiding a public promise that the generated 16-skill catalog is production-ready.

**Decision:**
Use a 14-day effort as a technical prototype target for the workflow engine, HITL, evidence pack export, and a small set of skills. Define the commercial MVP around Kimi's five-suite scope once confidence, review, and regional fallback UX are in place.

**Prototype Credits:**
1. PRc2 - LEED AP pipeline validation.
2. WEp2 - Water Efficiency wedge.
3. EAp5/EAc7 - Refrigerant Management.

**Commercial MVP Suites:**
1. WEp2 + WEc2 - Water Efficiency.
2. EAp5 + EAc7 - Refrigerant Management.
3. EQp1 + EQp2 - Quality Plans.
4. IPp1 + IPp2 - Integrative Process Assessments.
5. MRc3 - Low-Emitting Materials.

**Assisted/Deferred Boundaries:**
- EAp2, EAc2, and EAc3 parse completed model outputs only; Ecogen does not create or validate energy models autonomously.
- IPp3, MRp2, MRc2, LTc1, LTc3, SSc3, and SSc5 require explicit source verification, regional gating, and specialist review before production sale.

---

## ADR-012: No USGBC Integration In V1

**Status:** Accepted

**Context:**
USGBC Arc or LEED Online integration could allow direct submission, but V1 should focus on evidence pack quality and review controls.

**Decision:**
Defer direct USGBC integration to V2.

**V1 Output:**
- Download evidence pack with PDF/DOCX/XLSX artifacts, source index, confidence scorecard, audit trail, and human review record.
- User uploads manually to LEED Online.

**V2 Enhancement:**
- Direct USGBC Arc/LEED Online submission only after verified API access and explicit final approval.

---

## ADR-013: Evidence Pack Standard

**Status:** Accepted

**Context:**
Kimi research standardizes output around audit-ready evidence packs rather than isolated generated reports.

**Decision:**
Every supported credit must produce a standard evidence pack with credit summary, requirement version, input inventory, source index, extracted data, calculation workbook/report, generated narrative, compliance matrix, confidence assessment, audit trail, human review annotations, and exception report.

**Rationale:**
- Makes review predictable across credits.
- Prevents unsupported claims from entering submission packages.
- Supports reviewer comments, rework, and audit defense.
- Keeps manual and regional fallback items visible.

---

## ADR-014: Confidence Tiering

**Status:** Accepted

**Context:**
Field-level confidence alone does not tell users whether a package is ready for review or what must be fixed.

**Decision:**
Use package-level confidence tiers A/B/C with visible component scores and degradation factors. Tier C packages require comprehensive review and correction; Tier B requires section review; Tier A still requires standard named human approval.

**Rationale:**
- Turns confidence into actionable UX.
- Gives reviewers a risk-based work queue.
- Makes OCR, stale data, source gaps, unit conversions, and regional substitutions visible.

---

## ADR-015: Manual And Regional Fallback UX

**Status:** Accepted

**Context:**
Regional data coverage varies substantially. Manual entry and manual preparation are normal workflow paths, not errors.

**Decision:**
Show each credit as fully supported, limited/manual input required, or unavailable for the project region. If automated data coverage is insufficient, route to source substitution, static dataset use, manual data entry, specialist review, or manual-preparation handoff.

**Rationale:**
- Avoids implying unattended global support.
- Protects users from silent API/data gaps.
- Lets enterprise users procure third-party data where justified.
- Preserves auditability of manual assumptions.

---

*Version: 1.1*
*Last Updated: 2026-05-02*
