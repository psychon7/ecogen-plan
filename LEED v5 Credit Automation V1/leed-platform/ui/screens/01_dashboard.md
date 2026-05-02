# Screen: Dashboard

## Purpose

Main entry point after login. Shows project health, review workload, evidence pack readiness, regional/manual blockers, and next actions without implying points have been awarded.

## Primary Users

- Senior LEED consultants
- Sustainability project managers
- Specialist reviewers
- Building-owner viewers with limited permissions

## Layout Structure

```text
TopBar
Sidebar
MainContent
  Header: greeting, new project
  PortfolioStats: active projects, evidence packs in review, submission-ready packages, awarded points
  ReviewQueue: assigned tasks, SLA, confidence tier, blocker count
  ProjectList: project cards with status and risk
  Exceptions: regional data gaps, manual-prep handoffs, stale sources
```

## Components

### Portfolio Stats

| Stat | Meaning |
|------|---------|
| Active projects | Projects with open credit work |
| In review | Evidence packs awaiting named human approval |
| Submission-ready | Internally approved packages ready for manual upload |
| Awarded points | Points accepted by USGBC, when known |

Do not combine pursued, internally approved, submitted, and awarded points into a single progress number.

### Project Card

Each card shows:

- Project name, location, rating system, target level.
- Region support summary: full, limited, manual input, unavailable.
- Package status counts: draft, in review, submission-ready, submitted, awarded.
- Highest risk: Tier C, overdue review, missing source, regional fallback, manual preparation.
- Next action.

### Review Queue

Each item shows:

- Credit code and name.
- Project name.
- Reviewer role and assignee.
- SLA time remaining.
- Confidence tier A/B/C.
- Required action: review, request changes, reassign, resolve blocker.
- Blocker count and exception count.

### Exceptions

Shows cross-project items that need attention:

- Low-confidence evidence packs.
- Stale API data.
- Regional data substitutions.
- Manual data entry required.
- Packages routed to manual preparation.
- Overdue reviews.

## States

### Loading

- Skeleton placeholders for project cards, stats, and review queue.

### Empty

- Show "No projects yet."
- Primary action: "Create Project."

### Error

- Show failed sections independently.
- Allow retry without hiding cached data.

## User Actions

| Action | Trigger | Result |
|--------|---------|--------|
| Create Project | Click "New Project" | Open project creation flow |
| Open Project | Click project card | Navigate to project detail |
| Review Task | Click review queue item | Navigate to HITL review |
| Resolve Exception | Click exception | Open relevant evidence pack section |
| Filter Queue | Select filters | Filter by role, SLA, confidence, project, credit, status |
| Search | Type search query | Search projects, credits, documents, reviewers |

## API Dependencies

```yaml
GET /api/dashboard/stats:
  response:
    active_projects: number
    evidence_packs_in_review: number
    submission_ready_packages: number
    awarded_points: number
    overdue_reviews: number

GET /api/projects?limit=:
  response:
    projects:
      - id: string
        name: string
        location: string
        rating_system: string
        target_level: string
        region_support: string
        status_counts: object
        highest_risk: string

GET /api/reviews/pending:
  response:
    reviews:
      - id: string
        credit_code: string
        credit_name: string
        project_name: string
        reviewer_role: string
        assignee_name: string
        due_at: string
        confidence_tier: string
        blocker_count: number
```

---

*Version: 1.1*
*Last Updated: 2026-05-02*
