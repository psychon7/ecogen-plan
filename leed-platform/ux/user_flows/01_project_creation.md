# User Flow: Project Creation

## Flow Overview

User creates a new LEED project, specifying basic information that enables credit automation.

## Entry Points
- Dashboard "New Project" button
- Sidebar navigation
- Deep link from email invitation

## Flow Steps

### Step 1: Start Project Creation
**Screen:** Project Creation Modal

**User Actions:**
- Click "New Project" button
- Or accept email invitation

**System Response:**
- Open modal with form
- Pre-fill if from invitation

### Step 2: Enter Project Details
**Screen:** Project Details Form

**Fields:**
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Project Name | Text | Yes | Max 100 chars |
| Project Code | Text | No | Auto-generated if blank |
| Building Type | Select | Yes | Office, Retail, Healthcare, etc. |
| LEED Version | Select | Yes | v4, v4.1, v5 |
| Rating System | Select | Yes | BD+C, ID+C, O+M |
| Target Level | Select | Yes | Certified, Silver, Gold, Platinum |
| Street Address | Text | Yes | For location detection |
| City | Text | Yes | - |
| State/Province | Text | Yes | - |
| Country | Select | Yes | For regional filtering |
| Postal Code | Text | Yes | - |

**User Actions:**
- Fill all required fields
- Click "Continue"

**System Response:**
- Validate fields
- Geocode address to lat/lng
- Detect region for credit availability
- Show loading state

**Error States:**
- Missing required fields → Highlight fields, show message
- Invalid address → Suggest corrections
- Unsupported region → Show limited credit availability

### Step 3: Confirm Location
**Screen:** Location Confirmation

**Display:**
- Map pin at detected location
- "Is this correct?" confirmation
- Option to adjust pin

**User Actions:**
- Confirm location
- Or drag pin to correct location
- Click "Continue"

**System Response:**
- Save lat/lng
- Query available credits for region
- Proceed to team setup

### Step 4: Add Team Members
**Screen:** Team Setup

**Fields:**
| Field | Type | Required |
|-------|------|----------|
| Name | Text | Yes |
| Email | Email | Yes |
| Role | Select | Yes |
| LEED AP Number | Text | No |

**Roles:**
- Project Manager
- LEED Consultant
- Energy Modeler
- Architect
- MEP Engineer
- Contractor
- Owner

**User Actions:**
- Add team members
- Or skip and add later
- Click "Create Project"

**System Response:**
- Send email invitations
- Create project in database
- Initialize project workspace
- Redirect to project dashboard

### Step 5: Project Dashboard
**Screen:** Project Dashboard

**Display:**
- Project header with name, location, target
- Credit grid showing available credits
- Progress summary (0/N credits started)
- Team member list

**User Actions:**
- Browse available credits
- Click credit to start automation
- Invite more team members
- Edit project settings

## Edge Cases

### EC-1: User doesn't know building type
- Show descriptions for each type
- Allow "Other" with text field

### EC-2: Address not found
- Allow manual lat/lng entry
- Show warning about limited automation

### EC-3: Region has limited credit availability
- Show available credits
- Explain limitations
- Offer manual entry option

### EC-4: Team member already has account
- Auto-link to existing user
- Send notification instead of invitation

## Success Criteria
- Project created in < 5 minutes
- All required fields validated
- Team members notified
- Dashboard loads with correct credits

---

*Version: 1.0*
*Last Updated: 2026-03-21*
