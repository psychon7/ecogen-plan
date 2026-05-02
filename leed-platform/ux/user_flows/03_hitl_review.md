# User Flow: HITL Review

## Flow Overview

Qualified reviewer inspects an evidence pack and approves, requests changes, rejects to manual preparation, reassigns, or escalates. HITL is mandatory for compliance-critical packages; confidence tier only changes review depth.

## Entry Points

- In-app review queue.
- Email or chat notification.
- Dashboard "In Review" task.
- Direct review link.

## Flow Steps

### Step 1: Receive Notification

**Notification Content:**

- Project name.
- Credit name.
- Evidence pack version.
- Required reviewer role.
- Confidence tier.
- Blocker count.
- SLA.
- Direct review link.

**System Rule:**

Notification failure must not change package state. The in-app task remains the source of truth.

### Step 2: Review Queue

**Display:**

- Pending tasks assigned to the user.
- Filters: project, credit, reviewer role, due date, confidence tier, blocker count, priority.
- Sort: due soon, Tier C first, blocker count, project.

**Review Card:**

| Field | Display |
|-------|---------|
| Project | Project name and location |
| Credit | Code and name |
| Package | Version and status |
| Confidence | A/B/C tier |
| Blockers | Open blocker count |
| Required Role | LEED AP, PE, LCA, GIS, legal, etc. |
| SLA | Time remaining or overdue |
| Actions | Review, reassign, escalate |

### Step 3: Review Evidence Pack

**Screen:** HITL Review

**Reviewer Sees:**

- Evidence pack sections.
- Source documents and extracted fields.
- Calculation workbook or report.
- Generated narrative.
- Compliance matrix.
- Confidence scorecard and degradation factors.
- Exception report.
- Audit trail.
- Credit-specific checklist.
- Comment thread.

**User Actions:**

- Inspect artifacts and source locators.
- Check required checklist items.
- Add comments to fields, calculations, sections, or overall package.
- Mark issues as info, warning, or blocker.
- Choose approve, request changes, reject to manual preparation, reassign, or escalate.

### Step 4a: Approve

**Requirements:**

- Required checklist items complete.
- Blockers resolved or explicitly overridden with justification.
- Reviewer credential/scope matches task.

**System Response:**

- Records reviewer identity, credential/scope, timestamp, package version, checklist state, comments, and signature metadata.
- Moves package to next gate, "Internally Approved," or "Submission-Ready" if all required reviews are complete.
- Notifies submitter and project manager.

### Step 4b: Request Changes

**Form Fields:**

| Field | Required |
|-------|----------|
| Return to Step | Yes |
| Reason | Yes |
| Specific Issues | Optional but recommended |
| Severity | Yes |

**Return Options:**

- Inputs.
- Extracted Data.
- Calculations.
- Evidence Pack Generation.
- Reviewer Recheck.

**System Response:**

- Marks package "Changes Requested."
- Rewinds workflow to selected step.
- Preserves previous version and comments.
- Notifies submitter.

### Step 4c: Reject To Manual Preparation

**Trigger:**

- AI-assisted path is unsuitable.
- Critical data cannot be verified.
- Region/source coverage is insufficient.
- Professional reviewer determines manual handling is required.

**System Response:**

- Marks credit "Manual Preparation Required."
- Archives AI attempt and reason.
- Creates manual-prep task for project lead.
- Keeps evidence and comments available for reuse.

### Step 4d: Reassign Or Escalate

**Reassign:**

- Select another qualified reviewer.
- Add reason.
- SLA updates according to policy.

**Escalate:**

- Route to senior reviewer, principal, project director, or specialist.
- Preserve prior comments and checklist progress.

## Edge Cases

### EC-1: SLA Approaching Or Overdue

- Send reminders.
- Escalate or reassign.
- Never auto-approve.

### EC-2: Reviewer Lacks Credential

- Block approval.
- Offer reassignment to qualified reviewer.

### EC-3: Document Will Not Load

- Provide download fallback.
- Keep review task open.
- Log viewer error.

### EC-4: Checklist Incomplete

- Disable approval.
- Highlight missing required items.

### EC-5: Unresolved Blockers

- Block approval unless override is permitted and justified.

## Success Criteria

- Review decision is explicit and auditable.
- Reviewer comments are actionable and linked to evidence.
- Request changes returns workflow to the correct step.
- Rejection creates a clear manual-prep path.
- Submission-ready status always has named human approval.

---

*Version: 1.1*
*Last Updated: 2026-05-02*
