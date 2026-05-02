# Screen: Project Detail

## Purpose

Central workspace for one LEED project. Shows credit pursuit, evidence pack status, confidence, regional support, required reviewers, team roles, and manual fallback needs.

## Layout Structure

```text
ProjectHeader
  name, address, rating system, target level, phase, region support
ProgressOverview
  pursued points, submission-ready points, submitted points, awarded points
CreditBoard
  filters, search, credit cards
TeamAndReviewers
  team members, credentials, assigned reviewer roles
ExceptionsPanel
  blockers, regional gaps, stale data, manual-prep items
```

## Progress Overview

Show separate status buckets:

| Bucket | Meaning |
|--------|---------|
| Pursued | Credit is targeted by the project team |
| Draft | Evidence pack is being prepared |
| In Review | Awaiting named human review |
| Internally Approved | Approved by required reviewer(s) |
| Submission-Ready | Export package ready for manual upload |
| Submitted | Uploaded to LEED Online/Arc by user |
| Awarded | Accepted by USGBC/GBCI review |

Never label internally approved points as awarded points.

## Credit Card Fields

Each credit card displays:

- Credit code and name.
- Point value or prerequisite flag.
- Product mode: `AI-generated draft`, `AI-assisted`, `documentation-only`, `manual-prep`.
- Regional support: full, limited, manual input required, unavailable.
- Confidence tier: A/B/C or "not assessed."
- Status bucket.
- Required reviewer role(s).
- Open blocker count.
- Evidence gap count.
- Dependencies, such as WEp2 before WEc2 or EAp5 before EAc7.

## Credit Card States

### Not Started

- Badge: "Not Started."
- Primary action: "Prepare Evidence Pack."

### Draft

- Badge: "Draft."
- Primary action: "Continue Draft."
- Shows missing input count.

### In Review

- Badge: "In Review."
- Secondary action: "View Review."
- Shows reviewer, SLA, confidence tier, and blocker count.

### Changes Requested

- Badge: "Changes Requested."
- Primary action: "Revise Evidence."
- Shows return step and reviewer comment summary.

### Internally Approved

- Badge: "Internally Approved."
- Secondary action: "View Approval Record."
- Not equivalent to submitted or awarded.

### Submission-Ready

- Badge: "Submission-Ready."
- Primary action: "Export Package."
- Requires all required approvals and no unresolved blockers.

### Manual Preparation Required

- Badge: "Manual Preparation Required."
- Primary action: "Open Manual Workflow."
- Shows reason: unsupported region, insufficient source coverage, rejected automation path, or specialist decision.

## User Actions

| Action | Trigger | Result |
|--------|---------|--------|
| Prepare Evidence Pack | Click credit action | Open credit evidence pack workflow |
| Continue Draft | Click action | Resume saved workflow |
| View Review | Click review status | Open HITL review task |
| Export Package | Click action | Generate/download manual-upload package |
| Open Manual Workflow | Click action | Open manual-prep checklist and evidence tracker |
| Filter Credits | Select filters | Filter by status, confidence, category, region support, reviewer |
| Assign Reviewer | Click reviewer control | Assign or change required reviewer |
| Invite Member | Click invite | Add user and role/credential metadata |

## API Dependencies

```yaml
GET /api/projects/{id}:
  response:
    id: string
    name: string
    address: string
    rating_system: string
    target_level: string
    region_support_summary: string
    status_counts: object
    point_summary:
      pursued: number
      internally_approved: number
      submission_ready: number
      submitted: number
      awarded: number

GET /api/projects/{id}/credits:
  response:
    credits:
      - id: string
        code: string
        name: string
        points: number
        product_mode: string
        status: string
        confidence_tier: string
        region_support: string
        required_reviewers: array
        blocker_count: number
        evidence_gap_count: number
        dependencies: array

GET /api/projects/{id}/team:
  response:
    members:
      - id: string
        name: string
        email: string
        role: string
        credentials: array
```

---

*Version: 1.1*
*Last Updated: 2026-05-02*
