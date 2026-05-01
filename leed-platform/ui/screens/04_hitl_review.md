# Screen: HITL Review

## Purpose
Interface for LEED consultants to review AI-generated credit documentation and approve or request changes.

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ TOP BAR                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ SIDEBAR │ MAIN CONTENT                                                      │
│         │                                                                   │
│         │ ┌─────────────────────────────────────────────────────────────┐ │
│         │ │ REVIEW HEADER                                               │ │
│         │ │ [← Back to Reviews]                                         │ │
│         │ │                                                             │ │
│         │ │ Review: IPp3 - Carbon Assessment                            │ │
│         │ │ Project: Acme HQ | Submitted by: Jennifer Lee | 2h ago      │ │
│         │ │ Due: 22 hours remaining                                     │ │
│         │ └─────────────────────────────────────────────────────────────┘ │
│         │                                                                   │
│         │ ┌─────────────────────────────────────┬───────────────────────┐ │
│         │ │                                     │                       │ │
│         │ │  DOCUMENT PREVIEW                   │  REVIEW CHECKLIST     │ │
│         │ │  ┌─────────────────────────────┐    │                       │ │
│         │ │  │                             │    │  ☑ Energy model       │ │
│         │ │  │    PDF Viewer               │    │     inputs verified   │ │
│         │ │  │                             │    │                       │ │
│         │ │  │                             │    │  ☐ Material           │ │
│         │ │  │                             │    │     quantities        │ │
│         │ │  │                             │    │     accurate          │ │
│         │ │  │                             │    │                       │ │
│         │ │  │                             │    │  ☐ Grid factors       │ │
│         │ │  │                             │    │     appropriate       │ │
│         │ │  │                             │    │                       │ │
│         │ │  │                             │    │  ☐ Calculations       │ │
│         │ │  │                             │    │     reasonable        │ │
│         │ │  │                             │    │                       │ │
│         │ │  │                             │    │  ☐ Hotspots           │ │
│         │ │  │                             │    │     identified        │ │
│         │ │  └─────────────────────────────┘    │                       │ │
│         │ │                                     │                       │ │
│         │ │  [Download PDF] [Download Excel]    │  Comments             │ │
│         │ │                                     │  ┌─────────────────┐  │ │
│         │ │                                     │  │                 │  │ │
│         │ │                                     │  │                 │  │ │
│         │ │                                     │  └─────────────────┘  │ │
│         │ │                                     │                       │ │
│         │ │                                     │  [Approve]            │ │
│         │ │                                     │  [Request Changes]    │ │
│         │ │                                     │                       │ │
│         │ └─────────────────────────────────────┴───────────────────────┘ │
│         │                                                                   │
└─────────┴───────────────────────────────────────────────────────────────────┘
```

## Component Tree

```
HITLReview
├── TopBar
├── Sidebar
└── MainContent
    ├── ReviewHeader
    │   ├── BackButton
    │   ├── ReviewTitle
    │   ├── MetaInfo
    │   │   ├── Project Name
    │   │   ├── Submitter
    │   │   └── Time Ago
    │   └── SLABadge
    ├── ReviewContent (2-column)
    │   ├── LeftColumn (60%)
    │   │   ├── DocumentViewer
    │   │   │   └── PDFViewer
    │   │   └── DownloadButtons
    │   └── RightColumn (40%)
    │       ├── ChecklistPanel
    │       │   └── ChecklistItem (×N)
    │       ├── CommentsPanel
    │       │   └── TextArea
    │       └── ActionButtons
    │           ├── ApproveButton
    │           └── RejectButton
```

## Document Viewer

### Features
- PDF rendering with pagination
- Zoom in/out (50% - 200%)
- Page navigation (prev/next, jump to page)
- Full-screen mode
- Text selection
- Print button

### Toolbar
```
┌─────────────────────────────────────────────────────────┐
│ [←] [→] Page 3 of 12 [Zoom: 100%] [⊕] [⊖] [⛶] [🖨️]    │
└─────────────────────────────────────────────────────────┘
```

## Checklist Panel

### Structure
- Section title: "Review Checklist"
- Checkboxes with labels
- All unchecked by default
- Required: All must be checked to approve

### Credit-Specific Checklists

**IPp3 - Carbon Assessment:**
- [ ] Energy model inputs verified
- [ ] Material quantities accurate
- [ ] Grid emission factors appropriate
- [ ] Calculations reasonable
- [ ] Top 3 hotspots identified

**WEp2 - Water Efficiency:**
- [ ] Fixture schedule complete
- [ ] Flow rates verified
- [ ] Occupancy counts accurate
- [ ] Calculations correct
- [ ] Percentage reduction calculated

**EAc3 - Energy Efficiency:**
- [ ] Proposed model accuracy verified
- [ ] Baseline model compliance confirmed
- [ ] Modeling assumptions reviewed
- [ ] Energy rates validated
- [ ] Percent improvement calculated

## Comments Panel

### Structure
- Label: "Comments (required for rejection)"
- Textarea: 4 rows
- Placeholder: "Add notes or feedback..."

### Characteristics
- Optional for approval
- Required for rejection
- Max 2000 characters
- Supports newlines

## Action Buttons

### Approve Button
- Variant: Primary
- Size: Large
- Icon: Checkmark
- Text: "Approve"
- State: Disabled until all checklist items checked

### Request Changes Button
- Variant: Secondary
- Size: Large
- Icon: Arrow-left
- Text: "Request Changes"
- Opens rejection modal

## Rejection Modal

### Structure
```
┌─────────────────────────────────────────┐
│ Request Changes                    [X]  │
├─────────────────────────────────────────┤
│                                         │
│ Return to step:                         │
│ ┌─────────────────────────────────────┐ │
│ │ Data Input                          │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Reason for rejection:                   │
│ ┌─────────────────────────────────────┐ │
│ │                                     │ │
│ │                                     │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Specific issues:                        │
│ ☐ Energy model needs correction         │
│ ☐ Material quantities incorrect         │
│ ☐ Calculations need revision            │
│                                         │
│          [Cancel]  [Submit Request]     │
│                                         │
└─────────────────────────────────────────┘
```

## Spacing & Layout

### Review Header
- Padding: 24px 32px
- Border-bottom: 1px solid `color.neutral.200`

### Main Content (2-column)
- Display: grid
- Grid: 60% / 40%
- Gap: 32px
- Padding: 32px
- Height: calc(100vh - 200px)
- Overflow: auto

### Document Viewer
- Height: 500px
- Border: 1px solid `color.neutral.200`
- Radius: `borderRadius.lg`

### Right Panel
- Position: sticky
- Top: 32px
- Background: `color.base.white`
- Padding: 24px
- Border: 1px solid `color.neutral.200`
- Radius: `borderRadius.lg`

## Typography

| Element | Font Size | Weight | Color |
|---------|-----------|--------|-------|
| Review Title | 24px | 700 | `color.neutral.900` |
| Meta Info | 14px | 400 | `color.neutral.500` |
| SLA Badge | 12px | 600 | `color.semantic.warning.dark` |
| Panel Title | 16px | 600 | `color.neutral.900` |
| Checklist Item | 14px | 400 | `color.neutral.700` |
| Button Text | 16px | 600 | varies |

## Colors

| Element | Token |
|---------|-------|
| Page background | `color.neutral.50` |
| Panel background | `color.base.white` |
| Panel border | `color.neutral.200` |
| SLA warning | `color.semantic.warning.light` |
| Approve button | `color.semantic.success` |
| Reject button | `color.semantic.error` |

## States

### Loading
- Show skeleton for document viewer
- Checklist disabled
- Buttons disabled

### Document Load Error
- Show error message
- Provide download link as fallback
- Log error for investigation

### Incomplete Checklist
- Approve button disabled
- Tooltip: "Complete all checklist items to approve"

### SLA Approaching
- Badge changes to red
- Show warning banner
- Offer reassign option

### Approved
- Show success toast
- Redirect to reviews list
- Update credit status

### Rejected
- Show confirmation
- Notify submitter
- Return to reviews list

## User Actions

| Action | Trigger | Result |
|--------|---------|--------|
| Check Item | Click checkbox | Mark item complete |
| Uncheck Item | Click checkbox | Mark item incomplete |
| Add Comment | Type in textarea | Save comment |
| Approve | Click button (all items checked) | Approve credit, notify submitter |
| Request Changes | Click button | Open rejection modal |
| Download PDF | Click button | Download document |
| Download Excel | Click button | Download workbook |
| Reassign | Click reassign | Open reassign modal |

## Micro-interactions

### Checkbox Check
- Scale up briefly (1.1)
- Duration: 150ms
- Easing: `motion.easing.bounce`

### Approve Button Enable
- Fade from disabled to enabled
- Duration: `motion.duration.fast`

### Document Page Change
- Fade transition
- Duration: `motion.duration.normal`

### Modal Open
- Fade in + scale up (0.95 → 1)
- Duration: `motion.duration.normal`
- Easing: `motion.easing.out`

## API Dependencies

```yaml
GET /api/reviews/{id}:
  response:
    id: string
    credit_code: string
    credit_name: string
    project_name: string
    submitter_name: string
    submitted_at: string
    due_at: string
    document_url: string
    excel_url: string
    checklist: array
      - id: string
        label: string
        checked: boolean

POST /api/reviews/{id}/approve:
  request:
    checklist: array
    comments: string
  response:
    status: string
    credit_id: string

POST /api/reviews/{id}/reject:
  request:
    return_to_step: string
    reason: string
    specific_issues: array
  response:
    status: string
    credit_id: string

POST /api/reviews/{id}/reassign:
  request:
    new_reviewer_id: string
    note: string
  response:
    status: string
```

---

*Version: 1.0*
*Last Updated: 2026-03-21*
