# Screen: Credit Evidence Pack

## Purpose

Guided interface for preparing one LEED credit evidence pack. The screen supports uploads, manual inputs, extraction review, calculations, narrative drafting, confidence assessment, exception handling, and submission to human review.

## Product Language

Use "Prepare Evidence Pack," "Run Assistant," and "Generate Draft Package." Do not imply unattended completion or reviewless approval. For energy-model credits, state clearly that the user must upload completed model outputs from a qualified modeler.

## Layout Structure

```text
EvidencePackHeader
  credit, project, product mode, region support, required reviewers
StepIndicator
  Overview -> Inputs -> Extracted Data -> Calculations -> Evidence Pack -> Review
MainPanel
  dynamic step content
RightPanel
  confidence tier, exceptions, source coverage, reviewer requirements
HelpPanel
  credit-specific guidance and boundaries
```

## Steps

### Step 1: Overview

Display:

- Credit description and applicable rating system/version.
- Points pursued or prerequisite status.
- Product mode: AI-generated draft, AI-assisted, documentation-only, manual-prep.
- Required inputs and optional inputs.
- Regional support and likely fallback needs.
- Required reviewer roles.
- Expected evidence pack sections.

Primary action: "Prepare Evidence Pack."

### Step 2: Inputs

Display:

- File upload zones for schedules, reports, model outputs, cut sheets, specifications, or source documents.
- Manual fields with units, defaults, and source/assumption labels.
- Regional source substitutions and manual data entry prompts.

Validation:

- File type and schema checks.
- Required fields.
- Unit/range checks.
- Explicit warning for unsupported data regions.

### Step 3: Extracted Data

Display editable extracted data tables with:

- Field value, unit, source document, locator, extraction method, confidence.
- Required/optional indicator.
- Human override controls and override reason.
- Cross-credit links where data is reused.

Confidence indicators:

- High: >=0.90
- Moderate: 0.75-0.89
- Low: <0.75 or critical source gap

### Step 4: Calculations

Display:

- Formula names and versions.
- Inputs, units, intermediate values, results, and thresholds.
- Calculation workbook preview.
- Warnings for narrow thresholds, unit conversion, stale sources, or cross-credit inconsistency.

For energy-model-dependent credits, this step parses and summarizes completed model outputs only.

### Step 5: Evidence Pack Preview

Show the 12 evidence pack sections:

1. Cover and credit summary.
2. Requirement summary.
3. Input inventory.
4. Source document index.
5. Extracted data.
6. Calculation workbook/report.
7. Generated narrative.
8. Compliance matrix.
9. Confidence assessment.
10. Audit trail.
11. Human review annotations.
12. Exception report.

### Step 6: Submit To Review

Display:

- Required reviewer role(s).
- Suggested assignee(s) based on credential and workload.
- SLA and priority.
- Open blockers and exceptions.
- Confidence tier and degradation reasons.
- Notes to reviewer.

Primary action: "Submit To Review." This creates a HITL task and moves the package to "In Review."

## Confidence Panel

The right panel always shows:

- Overall tier A/B/C.
- Component scores: calculation accuracy, evidence provenance, narrative quality, source coverage, cross-credit consistency.
- Degradation factors.
- Required fixes to improve the tier.
- Whether package export is blocked.

## Exception Handling

| Exception | UX Response |
|-----------|-------------|
| API timeout | Retry, cached/static fallback, or manual entry |
| Region unsupported | Show limited/unavailable state and manual workflow |
| Low-confidence extraction | Require human correction or reviewer verification |
| Missing critical source | Block submission to final review until source or override is provided |
| Calculation error | Show failed formula/input, allow correction and rerun |
| Reviewer requests changes | Rewind to named step with reviewer comments preserved |
| Reviewer rejects automation path | Move to manual preparation |

## User Actions

| Action | Trigger | Result |
|--------|---------|--------|
| Upload File | Drop or browse | Validate, parse, preview extracted fields |
| Enter Manual Data | Fill field | Store with assumption/source note |
| Edit Extracted Data | Inline edit | Save override, require reason for critical fields |
| Run Calculation | Click action | Execute tested calculation workflow |
| View Source | Click source link | Open document/page/row locator |
| Resolve Exception | Click exception | Navigate to field, source, or review item |
| Submit To Review | Click action | Create HITL task |
| Save And Exit | Click action | Persist workflow state |

## API Dependencies

```yaml
GET /api/credits/{code}:
  response:
    code: string
    name: string
    points: number
    product_mode: string
    description: string
    required_inputs: array
    expected_outputs: array
    required_reviewers: array
    regional_support: object

POST /api/credits/{code}/upload:
  request:
    file: binary
    input_type: string
  response:
    source_document: object
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
    current_step: string
    results: object
    confidence: object
    exceptions: array

POST /api/evidence-packs/{id}/submit-review:
  request:
    reviewer_id: string
    priority: string
    notes: string
  response:
    hitl_task_id: string
    status: string
```

---

*Version: 1.1*
*Last Updated: 2026-05-02*
