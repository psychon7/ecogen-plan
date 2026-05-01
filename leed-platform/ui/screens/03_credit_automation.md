# Screen: Credit Automation

## Purpose
Wizard interface for automating a single LEED credit. Guides user through data input, validation, calculation, and submission.

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ TOP BAR                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ SIDEBAR │ MAIN CONTENT                                                      │
│         │                                                                   │
│         │ ┌─────────────────────────────────────────────────────────────┐ │
│         │ │ WIZARD HEADER                                               │ │
│         │ │ [← Back] IPp3 - Carbon Assessment              [Save & Exit]│ │
│         │ │ 0 pts | 85% automated | Project: Acme HQ                    │ │
│         │ └─────────────────────────────────────────────────────────────┘ │
│         │                                                                   │
│         │ ┌─────────────────────────────────────────────────────────────┐ │
│         │ │ PROGRESS STEPS                                              │ │
│         │ │ ●────●────○────○────○                                       │ │
│         │ │ Input  Data  Calc  Review Submit                            │ │
│         │ └─────────────────────────────────────────────────────────────┘ │ │
│         │                                                                   │
│         │ ┌─────────────────────────────────────────────────────────────┐ │
│         │ │ STEP CONTENT                                                │ │
│         │ │                                                             │ │
│         │ │ Upload Required Files                                       │ │
│         │ │                                                             │ │
│         │ │ ┌───────────────────────────────────────────────────────┐   │ │
│         │ │ │ 📄 Energy Model Output                                  │   │ │
│         │ │ │ Drag & drop or click to browse                          │   │ │
│         │ │ │ Accepted: .html, .csv, .xml                            │   │ │
│         │ │ └───────────────────────────────────────────────────────┘   │ │
│         │ │                                                             │ │
│         │ │ ┌───────────────────────────────────────────────────────┐   │ │
│         │ │ │ 📄 Material Quantities                                  │   │ │
│         │ │ │ Drag & drop or click to browse                          │   │ │
│         │ │ │ Accepted: .xlsx, .csv                                   │   │ │
│         │ │ └───────────────────────────────────────────────────────┘   │ │
│         │ │                                                             │ │
│         │ │ Service Life (years)                                        │ │
│         │ │ ┌───────────────────────────────────────────────────────┐   │ │
│         │ │ │ 25                                                      │   │ │
│         │ │ └───────────────────────────────────────────────────────┘   │ │
│         │ │                                                             │ │
│         │ │ [Continue →]                                                │ │
│         │ │                                                             │ │
│         │ └─────────────────────────────────────────────────────────────┘ │
│         │                                                                   │
│         │ ┌─────────────────────────────────────────────────────────────┐ │
│         │ │ HELP PANEL (collapsible)                                    │ │
│         │ │ ℹ️ About this credit                                        │ │
│         │ │ This credit calculates 25-year carbon...                    │ │
│         │ └─────────────────────────────────────────────────────────────┘ │
│         │                                                                   │
└─────────┴───────────────────────────────────────────────────────────────────┘
```

## Wizard Steps

### Step 1: Overview
- Credit description
- Required inputs list
- Expected outputs preview
- "Start Automation" button

### Step 2: Data Input
- File upload zones
- Manual input fields
- Validation in real-time
- "Continue" button

### Step 3: Data Review
- Extracted data preview
- Editable tables
- Confidence indicators
- "Confirm & Calculate" button

### Step 4: Calculation
- Progress indicator
- Real-time status updates
- Cancel option
- Results preview on complete

### Step 5: Review & Submit
- Generated documents preview
- Summary metrics
- Submit for review button
- Or download directly (if no HITL)

## Component Tree

```
CreditAutomation
├── TopBar
├── Sidebar
└── MainContent
    ├── WizardHeader
    │   ├── BackButton
    │   ├── CreditInfo
    │   │   ├── Code & Name
    │   │   └── Meta (points, automation, project)
    │   └── SaveExitButton
    ├── StepIndicator
    │   └── Step (×5)
    ├── StepContent (dynamic)
    │   ├── OverviewStep
    │   ├── DataInputStep
    │   │   ├── FileUpload (×N)
    │   │   └── InputFields
    │   ├── DataReviewStep
    │   │   └── DataTable
    │   ├── CalculationStep
    │   │   └── ProgressIndicator
    │   └── SubmitStep
    │       ├── DocumentPreview
    │       └── SubmitButton
    └── HelpPanel
```

## File Upload Component

### Default State
- Border: 2px dashed `color.neutral.300`
- Background: `color.neutral.50`
- Icon: Upload cloud
- Text: "Drag and drop or click to browse"
- Subtext: "Accepted formats: .html, .csv, .xml"

### Drag Over State
- Border: 2px dashed `color.primary.500`
- Background: `color.primary.50`

### Uploading State
- Progress bar
- File name
- Cancel button

### Success State
- Checkmark icon
- File name
- File size
- Remove button

### Error State
- Error icon
- Error message
- Retry button

## Data Table Component

### Structure
```
┌─────────────────────────────────────────────────────────┐
│ Material Name          │ Quantity │ Unit │ GWP/kg │ CO2 │
├─────────────────────────────────────────────────────────┤
│ Concrete - 30 MPa      │ 1,000    │ m3   │ 250    │ ✓   │
│ Steel - Rebar          │ 50,000   │ kg   │ 1.2    │ ⚠️  │
│ [+ Add Material]                                        │
└─────────────────────────────────────────────────────────┘
```

### Validation Indicators
- ✓ Green: High confidence (>90%)
- ⚠️ Yellow: Medium confidence (70-90%)
- ❌ Red: Low confidence (<70%) or error

### Inline Editing
- Click cell to edit
- Save on blur or Enter
- Cancel on Escape

## Progress Indicator

### Structure
```
┌─────────────────────────────────────────────────────────┐
│ Calculating Carbon Projection...                        │
│                                                         │
│ ████████████░░░░░░░░  60%                               │
│                                                         │
│ ✓ Validating inputs                                     │
│ ✓ Fetching grid emission factors                        │
│ ⏳ Calculating operational carbon...                    │
│ ○ Calculating embodied carbon                           │
│ ○ Generating report                                     │
│                                                         │
│ [Cancel]                                                │
└─────────────────────────────────────────────────────────┘
```

### Animation
- Progress bar: smooth width transition
- Step icons: fade in on complete
- Current step: pulsing indicator

## Spacing & Layout

### Wizard Header
- Padding: 20px 32px
- Border-bottom: 1px solid `color.neutral.200`

### Step Indicator
- Padding: 24px 32px
- Centered
- Max-width: 600px

### Step Content
- Padding: 32px
- Max-width: 800px
- Centered

### Help Panel
- Position: sticky bottom
- Padding: 16px 32px
- Background: `color.semantic.info.light`
- Border-top: 1px solid `color.semantic.info.DEFAULT`

## Typography

| Element | Font Size | Weight | Color |
|---------|-----------|--------|-------|
| Credit Code | 14px | 600 | `color.primary.600` |
| Credit Name | 24px | 700 | `color.neutral.900` |
| Step Label | 12px | 500 | `color.neutral.500` |
| Step Label Active | 12px | 600 | `color.primary.600` |
| Section Title | 18px | 600 | `color.neutral.900` |
| Upload Text | 16px | 500 | `color.neutral.700` |
| Upload Subtext | 14px | 400 | `color.neutral.500` |

## Colors

| Element | Token |
|---------|-------|
| Active step | `color.primary.600` |
| Completed step | `color.semantic.success.DEFAULT` |
| Pending step | `color.neutral.300` |
| Upload zone default | `color.neutral.50` |
| Upload zone drag | `color.primary.50` |
| Help panel bg | `color.semantic.info.light` |

## States

### Loading (Initial)
- Show skeleton for step content
- Step indicator visible

### Validation Error
- Highlight invalid fields
- Show error message below field
- Disable continue button

### Calculation Running
- Show progress indicator
- Disable navigation
- Allow cancel

### Calculation Complete
- Show results summary
- Enable document preview
- Show submit button

### API Error
- Show error toast
- Allow retry
- Preserve user data

## User Actions

| Action | Trigger | Result |
|--------|---------|--------|
| Upload File | Drop or click | Validate, parse, show preview |
| Remove File | Click remove | Clear file, reset field |
| Edit Data | Click cell | Inline edit mode |
| Continue | Click button | Validate, proceed to next step |
| Go Back | Click back | Save progress, previous step |
| Cancel Calculation | Click cancel | Stop workflow, save state |
| Submit | Click submit | Create HITL task |
| Save & Exit | Click button | Save progress, exit to dashboard |

## Micro-interactions

### File Upload Success
- Checkmark animates in
- Duration: 300ms
- Easing: `motion.easing.bounce`

### Step Transition
- Content fades out/in
- Duration: `motion.duration.normal`
- Easing: `motion.easing.DEFAULT`

### Progress Bar
- Smooth width animation
- Duration: 300ms per update
- Easing: `motion.easing.out`

### Validation Error
- Field shakes (translateX ±4px)
- Duration: 300ms
- Error message fades in

## API Dependencies

```yaml
GET /api/credits/{code}:
  response:
    code: string
    name: string
    points: number
    automation_level: number
    description: string
    required_inputs: array
    expected_outputs: array

POST /api/credits/{code}/upload:
  request:
    file: binary
    input_type: string
  response:
    extracted_data: object
    confidence_scores: object
    validation_errors: array

POST /api/credits/{code}/calculate:
  request:
    inputs: object
  response:
    workflow_id: string
    status: string

GET /api/workflows/{id}/status:
  response:
    status: string
    progress: number
    current_step: string
    results: object

POST /api/credits/{code}/submit:
  request:
    workflow_id: string
    reviewer_id: string
  response:
    hitl_task_id: string
    status: string
```

---

*Version: 1.0*
*Last Updated: 2026-03-21*
