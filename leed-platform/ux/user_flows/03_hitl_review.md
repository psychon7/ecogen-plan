# User Flow: HITL (Human-in-the-Loop) Review

## Flow Overview

LEED consultant reviews AI-generated credit documentation and approves or requests changes.

## Entry Points
- Slack notification
- Email notification
- Dashboard "Pending Reviews" badge
- Direct link from notification

## Flow Steps

### Step 1: Receive Notification
**Channel:** Slack / Email / In-app

**Notification Content:**
- Project name
- Credit name
- Submitted by
- SLA: "Review needed within 24 hours"
- Direct link to review

**User Actions:**
- Click notification link
- Or open dashboard and find review

### Step 2: Review Dashboard
**Screen:** Reviews Dashboard

**Display:**
- List of pending reviews
- Filter by: Project, Credit, Submitter, Due Date
- Sort by: Due date (default), Project, Priority

**Review Card:**
| Field | Display |
|-------|---------|
| Project | "Acme HQ - NYC" |
| Credit | "IPp3 - Carbon Assessment" |
| Submitter | "Jennifer Lee" |
| Submitted | "2 hours ago" |
| Due | "22 hours remaining" |
| Priority | Normal / Urgent |
| Actions | Review / Reassign / Snooze |

**User Actions:**
- Click "Review" on a card
- Or filter/sort to find specific review

### Step 3: Review Interface
**Screen:** Credit Review

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│ HEADER                                              │
│ Project: Acme HQ | Credit: IPp3 Carbon Assessment   │
│ Submitted by: Jennifer Lee | 2 hours ago            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  DOCUMENT PREVIEW (70% width)    │ CHECKLIST      │
│  ┌─────────────────────────┐     │ [ ] Item 1    │
│  │                         │     │ [ ] Item 2    │
│  │   PDF Report Viewer     │     │ [ ] Item 3    │
│  │                         │     │ [ ] Item 4    │
│  │                         │     │               │
│  └─────────────────────────┘     │ COMMENTS      │
│                                  │ [textarea]    │
│  DOWNLOAD: PDF | Excel           │               │
│                                  │ ACTIONS       │
│                                  │ [Approve]     │
│                                  │ [Reject]      │
│                                  │               │
└─────────────────────────────────────────────────────┘
```

**Document Preview:**
- Embedded PDF viewer
- Page navigation
- Zoom controls
- Download button

**Checklist (Credit-specific):**
For IPp3:
- [ ] Energy model inputs verified
- [ ] Material quantities accurate
- [ ] Grid emission factors appropriate
- [ ] Calculations reasonable
- [ ] Top 3 hotspots identified

**User Actions:**
- Review document
- Check off checklist items
- Add comments
- Click "Approve" or "Reject"

### Step 4a: Approve
**Action:** Click "Approve"

**Confirmation Modal:**
- "Are you sure you want to approve?"
- Shows checklist completion status
- Requires all items checked

**User Actions:**
- Confirm approval
- Or cancel and continue review

**System Response:**
- Mark credit as "Approved"
- Generate final documents
- Notify submitter
- Update project dashboard
- Resume workflow for finalization

### Step 4b: Reject
**Action:** Click "Reject"

**Rejection Form:**
| Field | Type | Required |
|-------|------|----------|
| Reason | Textarea | Yes |
| Return to Step | Select | Yes |
| Specific Issues | Checklist | No |

**Return Options:**
- Data Input (Step 3)
- Calculation Review (Step 5)
- Full Restart (Step 1)

**User Actions:**
- Select return step
- Describe issues
- Click "Submit Rejection"

**System Response:**
- Mark credit as "Changes Requested"
- Return workflow to specified step
- Notify submitter with comments
- Preserve previous data for reference

### Step 5: Confirmation
**Screen:** Action Confirmation

**Approve Confirmation:**
- "Credit approved successfully"
- Final documents available for download
- Option to submit to USGBC

**Reject Confirmation:**
- "Changes requested"
- Submitter notified
- Link to track status

## Alternative Flow: Reassign Review

**Trigger:** Reviewer unavailable

**User Actions:**
- Click "Reassign"
- Select new reviewer from team
- Add note explaining reason
- Click "Reassign"

**System Response:**
- Update task assignee
- Notify new reviewer
- Update SLA timer

## Edge Cases

### EC-1: SLA approaching
- Send reminder notification at 4 hours remaining
- Escalate to project manager at 1 hour
- Mark as overdue if missed

### EC-2: Reviewer on vacation
- Auto-reassign based on backup rules
- Or pause and notify project manager

### EC-3: Document won't load
- Show download link as fallback
- Log error for investigation

### EC-4: Checklist incomplete on approve
- Block approval with warning
- Require explicit override with reason

## Success Criteria
- Review completed within SLA
- Clear approve/reject decision
- Actionable feedback on rejection
- All parties notified

---

*Version: 1.0*
*Last Updated: 2026-03-21*
