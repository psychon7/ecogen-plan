# HITL And Durable Workflows

## Principle

HITL is not a user-interface flourish. It is the control layer that keeps Ecogen professionally usable. A credit package is not submission-ready until qualified human review has approved the relevant calculations, assumptions, evidence, and narrative.

## Workflow State Machine

Canonical workflow statuses:

```text
pending -> running -> paused_for_review -> running -> completed
                         |                  |
                         v                  v
                  changes_requested -> running
                         |
                         v
                    manual_mode

Any state can move to failed with recoverable error metadata.
```

## Canonical Status And Action Names

Implementation must normalize prototype names to these canonical values:

| Concept | Canonical value | Prototype value to replace |
|---------|-----------------|----------------------------|
| Waiting for review | `paused_for_review` | `WorkflowStatus.PAUSED` / `paused` |
| Reviewer asks for edits | `changes_requested` | overloaded `HITLStatus.REJECTED` |
| Irrecoverable rejection | `failed` with rejection metadata | `HITLStatus.REJECTED` with no workflow rewind |
| Manual handling | `manual_mode` | ad hoc fallback flags |

HITL actions must be `approve`, `request_changes`, `reject`, and `reassign`. `request_changes` must carry `return_to_step`; `reject` must either fail the workflow or explicitly enter `manual_mode`.

## Durable Workflow Requirements

The workflow engine must:

- Persist state after every step.
- Resume from the last completed step.
- Store input schema version, skill version, LEED requirement version, and source versions.
- Support per-step retry, timeout, idempotency key, and failure policy.
- Store step outputs as typed JSON with references to large artifacts in object storage.
- Pause at HITL checkpoints without holding worker resources.
- Rewind to a named step when review requests changes.
- Preserve complete audit history even when a workflow is rerun.

Treat external submission/upload to Arc, LEED Online, or USGBC systems as out of scope for V1 automation. Workflows may generate export packages and manual-upload manifests, but final submission requires a human approval checkpoint and explicit user action.

## HITL Task Contract

Each review task must include:

- Task id, workflow id, project id, credit code, step name.
- Reviewer role and assigned reviewer.
- SLA hours, escalation policy, created/assigned/completed timestamps.
- Evidence pack links and source index.
- Checklist with required and optional items.
- Confidence score breakdown and flagged assumptions.
- Approve, request changes, reject, and reassign actions.
- Reviewer comments, checklist results, reviewer identity, and digital signature metadata.
- `return_to_step` for changes or rejection.

Notification routing should support in-app as the source of truth, with email or chat notifications as delivery channels. If a channel fails, the HITL task remains active and a fallback notification should be attempted; notification failure must not approve or reject a package.

## Review Roles

| Review Type | Role | Default SLA |
|-------------|------|-------------|
| Low-risk credit final review | LEED consultant or project manager | 24h |
| Carbon/material review | LCA or carbon reviewer | 48h |
| Energy model review | Energy modeler or licensed engineer | 48-72h |
| GIS/site review | GIS analyst/planner | 48h |
| Legal/process documents | Legal/project manager as applicable | 48h |

SLA expiry must never auto-approve a compliance package. Expiry may escalate, reassign, or move to `manual_mode`, but approval always requires a qualified reviewer identity and signature.

## Confidence Tiers

| Tier | Score | Meaning | Requirement |
|------|-------|---------|-------------|
| A | >=0.90 | Source-backed, deterministic, complete | Standard review |
| B | 0.75-0.89 | Minor gaps, moderate extraction uncertainty, narrow threshold | Section review required |
| C | <0.75 | Critical uncertainty, missing sources, low-confidence extraction | Comprehensive review and correction |

A floor rule applies: if any critical input, formula, or source coverage score is below 0.70, the evidence pack is Tier C regardless of weighted average.

The default confidence score should be a weighted blend: calculation accuracy 30%, evidence provenance 25%, narrative quality 20%, source coverage 15%, and cross-credit consistency 10%. Degradation factors must be visible to reviewers, with concrete guidance such as "upload manufacturer cut sheet" or "replace stale API factor" to improve the tier.

## Canonical Workflow State Shape

Every persisted workflow state should include:

| Field | Purpose |
|-------|---------|
| `workflow_id`, `project_id`, `credit_code` | Identity and routing |
| `skill_version`, `schema_version`, `leed_requirement_version` | Reproducibility |
| `status`, `current_node`, `completed_nodes` | Resume and UI status |
| `inputs`, `normalized_data`, `calculations` | Typed state payloads |
| `evidence_records`, `artifact_refs`, `confidence` | Audit-ready outputs |
| `hitl_task_id`, `review_history` | Human review linkage |
| `errors`, `fallbacks_used`, `source_health` | Failure and degradation record |

## Prototype Gaps To Fix

The existing `skills/durable_workflow.py` and `skills/hitl_system.py` are useful prototypes. Before production implementation:

- Fix enum serialization/deserialization for workflow and HITL status.
- Add explicit workflow rewind on HITL rejection.
- Add idempotency keys to prevent duplicate API calls/documents on resume.
- Add artifact references and checksums to workflow state.
- Add source/evidence ids to every calculation and document step.
- Add SLA escalation that changes workflow state, not just task status.
- Add tests for pause/resume/reject/reload behavior.
