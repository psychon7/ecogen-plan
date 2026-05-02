# Screen: HITL Review

## Purpose

Interface for qualified reviewers to inspect an AI-prepared evidence pack, verify sources/calculations/narratives, leave comments, and approve, request changes, reject to manual preparation, reassign, or escalate.

## Layout Structure

```text
ReviewHeader
  credit, project, package version, reviewer role, SLA, confidence tier
TaskQueue
  optional list of assigned review tasks
EvidenceViewer
  PDF/report, spreadsheet, source document, image, map, or extracted-data view
ReviewPanel
  checklist, confidence, exceptions, comments, actions
AuditPanel
  workflow history, reviewer decisions, source changes
```

## Review Header

Shows:

- Credit and evidence pack version.
- Project and rating system.
- Submitted by and submitted timestamp.
- Required reviewer role and assigned reviewer.
- Credential/scope requirement.
- SLA countdown and escalation state.
- Confidence tier and open blocker count.

## Evidence Viewer

The viewer supports:

- Generated PDF/DOCX narrative preview.
- Calculation workbook/table preview.
- Source document preview with page/row/locator.
- Extracted field table.
- Image or map overlays where applicable.
- Side-by-side source vs generated claim comparison.

Toolbar:

- Search.
- Page/sheet navigation.
- Zoom.
- Source locator.
- Open in new panel.
- Download artifact.

## Review Checklist

Checklist items are credit-specific and categorized:

| Category | Examples |
|----------|----------|
| Data verification | Inputs match source documents, manual assumptions labeled |
| Calculation | Formula, units, thresholds, intermediate values reviewed |
| Documentation | Required narratives, tables, and forms present |
| Compliance | Requirement-to-evidence matrix complete |
| Regional/manual fallback | Substitutions and manual entries acceptable |

Items may be required or optional. Required blockers prevent approval unless resolved or overridden with justification.

## Confidence And Exceptions

The review panel displays:

- Tier A/B/C.
- Component scores.
- Degradation factors.
- Open exceptions.
- Suggested fixes.
- Whether final export is blocked.

Tier C requires comprehensive review and correction before submission-ready status.

## Comments

Reviewers can comment on:

- Evidence pack section.
- Calculation cell or row.
- Extracted field.
- Source document locator.
- Narrative paragraph.
- Overall package.

Each comment has:

- Severity: info, warning, blocker.
- Status: open, resolved, overridden.
- Owner.
- Timestamp.

## Actions

### Approve

Available only when required checklist items and blockers are resolved or explicitly overridden with justification.

Effect:

- Records reviewer identity, credential/scope, timestamp, package version, checklist state, and comments.
- Moves workflow to the next gate or "Internally Approved."

### Request Changes

Returns workflow to a named step with comments attached.

Return options:

- Inputs.
- Extracted Data.
- Calculations.
- Evidence Pack Generation.
- Reviewer Recheck.

### Reject To Manual Preparation

Used when the AI-assisted path should not continue safely.

Effect:

- Marks credit as "Manual Preparation Required."
- Archives AI attempt and reason.
- Notifies project lead.

### Reassign

Moves task to another qualified reviewer and records reason.

### Escalate

Routes to senior reviewer, project director, or specialist role.

## States

| State | Behavior |
|-------|----------|
| Loading | Skeleton viewer and disabled checklist |
| Document load error | Show download fallback and preserve review task |
| Incomplete checklist | Approve disabled; tooltip explains missing items |
| Blockers open | Approve disabled unless override policy allows |
| SLA approaching | Warning badge and escalation action |
| Approved | Success message and return to queue |
| Changes requested | Confirmation and workflow return step |
| Manual preparation | Confirmation and manual workflow link |

## User Actions

| Action | Trigger | Result |
|--------|---------|--------|
| Check Item | Click checkbox | Mark checklist item complete |
| Add Comment | Select target and type | Save threaded comment |
| Mark Blocker | Set severity | Prevent approval until resolved/overridden |
| Approve | Click Approve | Record approval and resume workflow |
| Request Changes | Click action | Open return-step modal |
| Reject To Manual Prep | Click action | Archive attempt and hand off |
| Reassign | Click action | Select new qualified reviewer |
| Escalate | Click action | Notify escalation target |
| Download Artifact | Click download | Download evidence artifact |

## API Dependencies

```yaml
GET /api/reviews/{id}:
  response:
    id: string
    evidence_pack_id: string
    credit_code: string
    credit_name: string
    project_name: string
    package_version: string
    submitter_name: string
    reviewer_role: string
    reviewer_credential_required: string
    submitted_at: string
    due_at: string
    confidence: object
    exceptions: array
    artifacts: array
    checklist: array
    comments: array
    audit_events: array

POST /api/reviews/{id}/approve:
  request:
    checklist: array
    comments: string
    overrides: array
    signature: object
  response:
    status: string
    evidence_pack_id: string

POST /api/reviews/{id}/request-changes:
  request:
    return_to_step: string
    reason: string
    specific_issues: array
  response:
    status: string

POST /api/reviews/{id}/reject-manual:
  request:
    reason: string
    manual_owner_id: string
  response:
    status: string

POST /api/reviews/{id}/reassign:
  request:
    new_reviewer_id: string
    note: string
  response:
    status: string
```

---

*Version: 1.1*
*Last Updated: 2026-05-02*
