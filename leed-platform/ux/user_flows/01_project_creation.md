# User Flow: Project Creation

## Flow Overview

User creates a LEED project and establishes the metadata needed for regional support, credit eligibility, evidence pack preparation, and reviewer routing.

## Entry Points

- Dashboard "New Project."
- Sidebar "Projects."
- Email invitation.

## Flow Steps

### Step 1: Start Project Creation

**Screen:** Project Creation

**System Response:**

- Open project form.
- Pre-fill organization and team data when available.

### Step 2: Enter Project Details

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| Project Name | Text | Yes | Display and audit records |
| Project Code | Text | No | Firm/project tracking |
| Building Type | Select | Yes | Credit applicability |
| LEED Version | Select | Yes | Requirement version |
| Rating System | Select | Yes | Reviewer and credit rules |
| Target Level | Select | Yes | Progress reporting |
| Project Phase | Select | Yes | Evidence availability and workflow guidance |
| Street Address | Text | Yes | Geocoding and regional data |
| City | Text | Yes | Location |
| State/Province | Text | Yes | Region |
| Country | Select | Yes | Regional filtering |
| Postal Code | Text | Yes | Geocoding |

**System Response:**

- Validate required fields.
- Geocode address to latitude/longitude.
- Resolve region support category.
- Detect climate zone and relevant jurisdiction fields when available.

### Step 3: Confirm Location And Region Support

**Display:**

- Map pin and editable coordinates.
- Region support summary.
- Credits likely full, limited/manual, unavailable, or manual-prep.

**User Actions:**

- Confirm location.
- Adjust pin or enter manual latitude/longitude.
- Continue.

**Edge Behavior:**

- Unsupported or limited regions show manual data requirements before the user sees credit cards.
- Manual location entry reduces confidence and appears in the evidence pack audit trail.

### Step 4: Add Team Members And Reviewer Roles

| Field | Type | Required |
|-------|------|----------|
| Name | Text | Yes |
| Email | Email | Yes |
| Project Role | Select | Yes |
| Credential/Specialty | Text/Select | No |
| Review Eligibility | Checkbox/Role | No |

**Roles:**

- Project Manager.
- LEED Consultant.
- Senior LEED AP / Principal Approver.
- Junior Consultant.
- Energy Modeler.
- MEP/PE Reviewer.
- LCA/Embodied Carbon Reviewer.
- GIS/Landscape Reviewer.
- Legal Reviewer.
- Architect.
- Contractor.
- Owner/Viewer.

### Step 5: Select Initial Credit Scope

**Display:**

- Recommended Kimi-aligned suites where applicable.
- Technical demo/assisted catalog credits clearly labeled.
- Region support and required reviewer role per credit.

**User Actions:**

- Select pursued credits.
- Assign default reviewers.
- Continue.

### Step 6: Project Dashboard

**Display:**

- Project header with region support.
- Credit board with pursued/draft/in-review/submission-ready/submitted/awarded statuses.
- Review roles and outstanding setup gaps.

**User Actions:**

- Prepare an evidence pack.
- Invite more team members.
- Resolve region/manual input gaps.

## Edge Cases

### EC-1: User Does Not Know Building Type

- Show brief descriptions.
- Allow "Other" with reduced automation confidence until corrected.

### EC-2: Address Not Found

- Allow manual location entry.
- Show warning about regional data confidence and source-routing impact.

### EC-3: Limited Regional Coverage

- Show available credits.
- Show limited/manual credits with required manual inputs.
- Hide or mark unavailable credits when required data cannot be sourced.

### EC-4: Reviewer Role Missing

- Allow project creation.
- Flag credits requiring reviewer assignment before submission to review.

## Success Criteria

- Project created in under 5 minutes.
- Region support is visible before credit work begins.
- Reviewer roles are captured early enough to avoid blocked packages.
- Dashboard loads with honest credit availability and status labels.

---

*Version: 1.1*
*Last Updated: 2026-05-02*
