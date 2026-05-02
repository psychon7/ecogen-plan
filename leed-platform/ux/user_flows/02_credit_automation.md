# User Flow: Credit Evidence Pack Preparation

## Flow Overview

User prepares a single LEED credit evidence pack from inputs to draft package and submits it for human review. The flow never bypasses required professional approval for compliance-critical outputs.

## Entry Points

- Project credit card "Prepare Evidence Pack."
- Dashboard exception or review request.
- Deep link from notification.
- "Continue Draft" from a saved workflow.

## Flow Steps

### Step 1: Select Credit

**Screen:** Project Detail

**User Actions:**

- Click "Prepare Evidence Pack" on a credit card.

**System Response:**

- Load credit configuration.
- Load regional support and required reviewer roles.
- Open Credit Evidence Pack screen.

### Step 2: Review Credit Overview

**Display:**

- Credit name, description, points/prerequisite status.
- Product mode: AI-generated draft, AI-assisted, documentation-only, or manual-prep.
- Required inputs and expected evidence pack sections.
- Regional availability and fallback status.
- Required reviewer roles.
- Explicit boundaries, such as "Ecogen parses completed energy model outputs; it does not create the model."

**User Actions:**

- Review scope and boundaries.
- Click "Prepare Evidence Pack."
- Or open manual-prep path if automation is unsuitable.

### Step 3: Input Evidence

**Screen:** Inputs

**Inputs may include:**

| Input | Type | Source |
|-------|------|--------|
| Fixture schedule | Upload/manual | Excel, CSV, PDF, manual table |
| Equipment schedule | Upload/manual | MEP schedule, Revit export |
| Energy model output | Upload | Completed model output from qualified modeler |
| Product certifications | Upload/API | Cut sheets, certification databases |
| Regional data | API/manual | Public API, static source, manual analyst input |
| Assumptions | Manual | User-entered with source note |

**System Response:**

- Validate file formats and schemas.
- Parse available data.
- Surface missing fields and manual entry prompts.
- Log regional substitutions and fallbacks.

### Step 4: Review Extracted Data

**Display:**

- Editable extracted data tables.
- Source locators and extraction method.
- Field confidence.
- Required/optional status.
- Manual override reason fields.

**User Actions:**

- Confirm extracted data.
- Correct values.
- Add missing source or assumption notes.
- Continue to calculations.

**System Response:**

- Save confirmed data.
- Update confidence tier and degradation factors.

### Step 5: Run Calculations And QA

**Display:**

- Workflow step progress.
- Formula names, units, intermediate values, and result preview.
- Automated QA checks and red flags.

**System Actions:**

- Execute deterministic calculation engines.
- Apply rules-based validation.
- Detect stale sources, unit inconsistencies, outliers, or missing evidence.
- Pause or route to manual input if required.

### Step 6: Evidence Pack Preview

**Display:**

- 12-section evidence pack preview.
- Confidence tier A/B/C.
- Component scorecard.
- Exception report.
- Compliance matrix.
- Generated narrative and calculation workbook.

**User Actions:**

- Resolve open exceptions.
- Regenerate sections after data changes.
- Submit to review.

### Step 7: Submit To HITL Review

**Display:**

- Required reviewer role(s).
- Suggested reviewers and credentials.
- SLA and priority.
- Reviewer notes field.
- Open blocker warning.

**User Actions:**

- Select reviewer.
- Add notes.
- Click "Submit To Review."

**System Response:**

- Create HITL task.
- Notify reviewer.
- Update credit status to "In Review."
- Preserve workflow state.

### Step 8: Review Outcome

**Approve:**

- Package moves to the next review gate or "Internally Approved."
- If all required reviews are complete and blockers are resolved, package can become "Submission-Ready."

**Request Changes:**

- Workflow rewinds to the named step.
- Reviewer comments remain attached to affected fields/sections.

**Reject To Manual Preparation:**

- Credit status becomes "Manual Preparation Required."
- AI attempt is archived with reason.

## Alternative Flow: Reduced Review For Tier A

Tier A packages may use a shorter checklist or spot-check review, but still require named human approval before submission-ready status.

## Edge Cases

### EC-1: API Timeout

- Retry with backoff.
- Use cached/static fallback if allowed.
- Request manual entry when coverage is insufficient.
- Record fallback in audit trail and confidence degradation.

### EC-2: Calculation Error

- Show formula/input that failed.
- Preserve data.
- Allow correction and rerun.

### EC-3: Low Confidence Or Missing Source

- Block final review if critical.
- Show required fix.
- Allow reviewer override only with justification where policy permits.

### EC-4: Unsupported Region

- Offer manual-prep path or limited/manual workflow.
- Do not show the credit as fully supported.

### EC-5: User Cancels Mid-Calculation

- Save workflow state.
- Allow resume from last completed durable step.

## Success Criteria

- User understands automation boundary before starting.
- Every critical value has a source or explicit manual assumption.
- Confidence and exceptions are visible before review.
- HITL task is created for every compliance-critical package.

---

*Version: 1.1*
*Last Updated: 2026-05-02*
