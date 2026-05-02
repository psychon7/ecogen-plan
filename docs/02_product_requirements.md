# Product Requirements

## Product Positioning

Ecogen is an AI-powered LEED documentation assistant for consultants. The product promise is faster, more consistent, more auditable documentation, not autonomous certification.

## Users

| Persona | Need | Product Response |
|---------|------|------------------|
| Senior LEED consultant | Move faster without losing control | Review queues, confidence scores, evidence packs, reusable templates |
| Sustainability project manager | Track progress and blockers | Credit board, status, SLA, reviewer assignments, package readiness |
| Junior consultant | Prepare drafts correctly | Guided intake, validation, inline corrections, evidence mapping |
| Building owner | Understand progress and risk | Project-level dashboard, time saved, remaining manual work |
| Specialist reviewer | Verify only relevant content | Role-based HITL tasks for energy, GIS, LCA, MEP, legal |

## V1 User Workflows

### Project Intake

The user creates a project with building type, location, target certification level, rating system, project phase, team roster, and region. The system geocodes the address, resolves region-specific data availability, and displays supported credits with automation confidence.

### Credit Automation

The user selects a credit, uploads required documents, reviews extracted data, resolves missing fields, runs calculations, previews outputs, and submits the package to HITL review.

For the Water Efficiency wedge, the MVP should be calculation-first: manual entry and spreadsheet upload for fixture schedules, transparent baseline/design formulas, and WEp2 output that can later feed WEc2 optimization. OCR from cut sheets and automated product matching are phase-2 accelerators, not blockers for the first usable workflow.

### HITL Review

The reviewer receives a task with document preview, source data, formulas, flagged assumptions, confidence scoring, checklist, comments, approve/request-changes/reject actions, and SLA countdown.

### Evidence Pack Export

V1 exports a download package suitable for manual upload to Arc/LEED Online. The package includes calculation workbook, narrative/report, source index, confidence scorecard, audit trail, and review record.

Every exported evidence pack should follow a standard 12-section structure:

| Section | Purpose |
|---------|---------|
| 1. Cover and credit summary | Project, credit, rating system, package status |
| 2. Requirement summary | Applicable LEED v5 requirement version and addenda date |
| 3. Input inventory | Uploaded files, manual fields, API data, assumptions |
| 4. Source document index | Source ids, locators, dates, versions, hashes |
| 5. Extracted data | Normalized tables and extraction confidence |
| 6. Calculation workbook/report | Formulas, units, intermediate values, final result |
| 7. Generated narrative | Draft text or compliance rationale for review |
| 8. Compliance matrix | Requirement-to-evidence mapping |
| 9. Confidence assessment | A/B/C tier, component scores, degradation factors |
| 10. Audit trail | Workflow steps, API calls, retries, data changes |
| 11. Human review annotations | Checklist, comments, corrections, approvals |
| 12. Exception report | Missing data, fallbacks, manual items, unresolved risk |

## V1 Functional Requirements

| Area | Requirement |
|------|-------------|
| Project setup | Create projects, team members, roles, region, rating system, target credits |
| Credit registry | Maintain production suite scope, prototype skills, assisted catalog labels, automation level, inputs, APIs, regional support, and reviewers |
| Document intake | Upload PDFs, XLSX/CSV, model outputs, product cut sheets, schedules, images |
| Extraction | Parse structured data, surface confidence, allow inline correction |
| Calculations | Run formula-based calculations in code with unit tests and traceable formulas |
| Evidence pack | Generate PDF/DOCX/XLSX plus source index, confidence score, audit trail |
| HITL | Assign reviewer, pause workflow, approve/request changes/reject, resume or rewind |
| Regional filtering | Show full, limited, manual, or unavailable status by credit and region |
| Audit | Record inputs, API responses, formulas, output versions, reviewer decisions |

## V1 Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| Accuracy | Calculation functions must have golden tests and unit conversion tests |
| Reliability | Workflows resume after API failure, worker restart, and HITL delay |
| Security | Project documents and API keys encrypted; RBAC enforced |
| Observability | Track workflow duration, API failures, HITL bottlenecks, approval/rejection rates |
| Usability | Consultant can complete a simple credit package in less than 30 minutes excluding review wait |
| Trust | Every generated factual claim and calculation links to source data or a formula |

## Success Metrics

These are product hypotheses and operating targets, not externally proven guarantees. They should be recalibrated after pilot projects and reviewer feedback.

| Metric | Target |
|--------|--------|
| Time saved per supported credit | 60-70% after review |
| Calculation accuracy | 99% on tested formulas |
| Evidence pack approval rate | >85% after first review |
| Workflow completion rate | >90% excluding missing user data |
| Reviewer confidence | NPS >40 for consultant reviewers |
| Regional availability honesty | 0 credits shown as fully automated when required data is unavailable |
