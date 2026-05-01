# User Flow: Credit Automation

## Flow Overview

User automates a single LEED credit from data input to document generation.

## Entry Points
- Project dashboard credit card
- Deep link from notification
- "Continue" from previous session

## Flow Steps

### Step 1: Select Credit
**Screen:** Project Dashboard

**User Actions:**
- Click on credit card (e.g., "IPp3 - Carbon Assessment")

**System Response:**
- Navigate to credit detail page
- Load credit configuration
- Show automation wizard

### Step 2: Review Credit Overview
**Screen:** Credit Overview

**Display:**
- Credit name and description
- Points available
- Automation level (e.g., "85% automated")
- Required inputs list
- Expected outputs
- Regional availability status

**User Actions:**
- Review requirements
- Click "Start Automation"
- Or click "Learn More" for documentation

### Step 3: Input Data
**Screen:** Data Input Form

**Dynamic Fields based on credit:**

For IPp3 (Carbon Assessment):
| Field | Type | Source |
|-------|------|--------|
| Energy Model Output | File upload | EnergyPlus, IES, Trace |
| Material Quantities | File upload or manual | Excel, BIM export |
| Service Life | Number input | Default: 25 years |
| Refrigerant Schedule | File upload | HVAC schedule |

**Upload Interface:**
- Drag-and-drop zone
- File type validation
- Progress indicator
- Preview for valid files

**User Actions:**
- Upload required files
- Fill manual fields
- Click "Continue"

**System Response:**
- Validate file formats
- Parse uploaded files
- Extract structured data
- Show data preview

**Error States:**
- Invalid file format → Show accepted formats
- Missing required data → Highlight missing fields
- Parse error → Show preview, allow manual correction

### Step 4: Review Extracted Data
**Screen:** Data Preview

**Display:**
- Structured data extracted from files
- Tables with editable values
- Validation indicators (green check / yellow warning)
- Confidence scores per field

**User Actions:**
- Review extracted data
- Edit incorrect values
- Add missing data
- Click "Confirm & Calculate"

**System Response:**
- Save confirmed data
- Trigger calculation workflow
- Show progress indicator

### Step 5: Calculation Progress
**Screen:** Calculation Progress

**Display:**
- Progress bar with step names
- Real-time status updates
- Estimated time remaining
- Cancel button

**Steps shown:**
1. Validating inputs ✓
2. Fetching grid emission factors... ⏳
3. Calculating operational carbon (pending)
4. Calculating embodied carbon (pending)
5. Generating report (pending)

**System Actions:**
- Execute durable workflow
- Call external APIs
- Run calculations
- Handle retries on failure

**User Actions:**
- Wait for completion
- Or cancel (saves progress)

### Step 6: Review Results
**Screen:** Calculation Results

**Display:**
- Summary metrics (e.g., "Total 25-year CO2: 2,100 tonnes")
- Breakdown charts (pie chart by source)
- Key findings
- Confidence score
- Generated documents preview

**User Actions:**
- Review results
- Click "View Full Report" to see document
- Click "Looks Good, Submit for Review"
- Or click "Make Changes" to adjust inputs

### Step 7: HITL Submission
**Screen:** Submit for Review

**Display:**
- Reviewer selection dropdown
- Priority level (Normal/Urgent)
- Notes field
- Document attachments

**User Actions:**
- Select reviewer
- Add notes
- Click "Submit"

**System Response:**
- Create HITL task
- Send notification to reviewer
- Update credit status to "In Review"
- Show confirmation

### Step 8: Confirmation
**Screen:** Submission Confirmation

**Display:**
- Success message
- Expected review time (e.g., "Within 24 hours")
- Link to track status
- Option to start another credit

**User Actions:**
- Return to project dashboard
- Or start another credit

## Alternative Flow: Direct Approval (Low-Risk Credits)

For credits with >90% automation and no HITL requirement:
- Skip Step 7
- Generate final documents immediately
- Mark credit as "Complete"
- Allow download of submission package

## Edge Cases

### EC-1: API timeout
- Retry 3x with exponential backoff
- If still failing, pause and notify user
- Allow manual data entry as fallback

### EC-2: Calculation error
- Show error details
- Log for debugging
- Allow retry or manual correction

### EC-3: Reviewer rejects
- Return to Step 3 with comments
- Highlight areas needing correction
- Preserve previous data

### EC-4: User cancels mid-calculation
- Save workflow state
- Allow resume from last completed step
- Show "Continue" option on dashboard

## Success Criteria
- Credit completed in < 10 minutes (simple) or < 30 minutes (complex)
- All calculations validated
- Documents generated successfully
- HITL task created (if required)

---

*Version: 1.0*
*Last Updated: 2026-03-21*
