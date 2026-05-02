# System Architecture

## Architecture Summary

Ecogen uses a modular web application architecture with durable credit workflows. The platform is planned around React, FastAPI, PostgreSQL/PostGIS, Redis, Celery/RabbitMQ, object storage, and a Deer-Flow/LangGraph-compatible skill orchestration layer.

The design should keep Deer-Flow behind an internal abstraction. Deer-Flow is the accepted foundation, but version-specific claims and API features must be verified before implementation.

The internal abstraction should be LangGraph-compatible even when Deer-Flow is used underneath: a typed state object, named nodes, conditional edges, checkpoint persistence, and resumable HITL pauses. This lets the platform swap orchestration details without rewriting every skill.

## Target Stack

| Layer | Canonical Choice |
|-------|------------------|
| Frontend | React with TypeScript |
| Backend API | Python 3.12, FastAPI |
| Database | PostgreSQL 15+ with PostGIS |
| Cache/session/rate limit | Redis |
| Background work | Celery + RabbitMQ |
| Workflow orchestration | Deer-Flow conventions with LangGraph-style durable state |
| Document storage | S3/GCS/Azure Blob with versioning |
| Document generation | Jinja2/HTML templates to PDF, DOCX, XLSX |
| GIS | PostGIS plus ArcGIS/OSM/vendor integrations where needed |
| Auth | JWT access/refresh tokens, organization/project RBAC |

## Core Services

| Service | Responsibility |
|---------|----------------|
| API gateway | Auth, project APIs, credit APIs, upload/download, review endpoints |
| Project service | Organizations, projects, team, rating system, region, project memory |
| Credit registry | Canonical credit metadata, inputs, reviewers, automation levels, availability |
| Skill runtime | Runs one credit skill workflow with persisted state and step contracts |
| Integration layer | External API clients, auth, rate limits, caching, fallbacks, source freshness |
| Extraction service | PDF/Excel/model/CAD/BIM parsing and confidence scoring |
| Calculation service | Deterministic formula implementations and test fixtures |
| Document service | Evidence pack, narrative, workbook, and report rendering |
| HITL service | Review tasks, SLA, comments, approvals, rejection loops, escalation |
| Audit service | Immutable event log, source registry, artifact hash, reviewer record |

## API Client Contract

All external integrations should use a shared client pattern:

- Typed request and response models.
- `httpx.AsyncClient` or equivalent async transport.
- Per-source timeout, retry, backoff, and circuit breaker settings.
- Redis-backed token buckets for rate limits.
- Versioned cache keys that include source name, endpoint, query, region, and source data vintage.
- Four-level fallback: primary API, secondary/cache/static dataset, guided manual data entry, then HITL/expert escalation.
- Source health events for latency, error rate, stale data, auth failure, and rate-limit proximity.
- Region-aware source routing: on project creation, the source router selects the correct API client or manual workflow per credit and region.

## Manual Data Acquisition

When API sources are unavailable for a project's region, the platform activates structured manual data entry workflows. This is a first-class data acquisition mode with:

- Guided entry forms with region-specific instructions and source links.
- Evidence upload and verification (PDF, screenshots, URLs).
- Confidence scoring based on data provenance (API > government pub > industry standard > manufacturer > estimate).
- Validation gates with range checks, unit consistency, and completeness verification.
- Full audit trail: every manual entry is timestamped, attributed, and immutable.
- Data reuse across credits within a project.

See [04b_manual_data_input_framework.md](04b_manual_data_input_framework.md) for the complete specification.

## Agent Model

The project-level lead agent orchestrates credit selection and dependency awareness. Each credit has a credit agent or skill instance. Credit agents can use specialized sub-agents, but the production boundary is service/tool based:

- Data extractor: parses uploaded documents and specialized model outputs.
- Calculation engine: runs formulas and unit conversions.
- Report generator: renders templates and output artifacts.
- Review checker: validates completeness, ranges, citations, formulas, and evidence.

Agents do not make final compliance decisions. They prepare evidence for review.

## Data Model Summary

The canonical platform data model includes:

- Organization, user, role, and project membership.
- Project, location, rating system, building type, target certification.
- Credit definitions and project credit instances.
- Workflow instances, steps, state, retry/error data, HITL task id.
- Documents, uploads, generated artifacts, source records, checksums.
- API integration definitions, API call logs, cache records, freshness metadata.
- HITL tasks, checklist results, comments, reviewer identities, decisions.
- Activity log and audit trail.

## Runtime Flow

1. Project intake creates the regional and project context.
2. Credit selector filters skills by data availability, region, and dependencies.
3. User starts a credit workflow and uploads inputs.
4. Extraction normalizes data and records confidence.
5. Source router determines API availability for project region.
6. APIs fetch external sources with cache and fallback metadata.
7. For unavailable sources, manual data collection workflow activates with guided forms and source guidance.
8. Calculation nodes run deterministic formulas (same pipeline for API and manual data).
9. QA checks completeness, ranges, source coverage, and confidence.
10. Evidence pack drafts are generated.
11. HITL review pauses the workflow.
12. Approval finalizes export; rejection rewinds to a defined step.

## Workflow Node Contract

Every workflow node should declare:

| Field | Meaning |
|-------|---------|
| `node_name` | Stable id used in checkpoints and `return_to_step` |
| `node_type` | validation, extraction, api_fetch, calculation, qa, document_generation, hitl, export |
| `inputs` | Required state fields or artifact refs |
| `outputs` | Typed state updates and artifact refs |
| `retry_policy` | Retry count, timeout, backoff, idempotency key |
| `fallback_policy` | Cache/static/manual path when automated data fails |
| `evidence_policy` | Source ids, formula refs, confidence updates |

## V1 Submission Boundary

V1 generates packages for manual upload. The architecture should include an `ArcExport` interface and feature flag, but direct Arc submission remains disabled until access, schema, write permissions, rate limits, and legal terms are verified.
