#!/usr/bin/env python3
"""
PRc2 LEED AP — Reference Implementation Pattern
Skill: leed-pr-c2-leed-ap | Version: 1.0.0
"""

```markdown
---
name: leed-pr-c2-leed-ap
version: 1.0.0
author: LEED Automation Platform
description: Verify at least one principal participant holds a current LEED AP credential with project-appropriate specialty.
---

## Metadata
- **Credit Code:** PRc2
- **Credit Name:** LEED AP
- **Points:** 1
- **Automation Level:** 90.1%
- **Complexity:** Low
- **Primary Data Source:** GBCI Credential Directory API, Project Team Roster (uploaded document)
- **HITL Required:** Yes

## Purpose
Automate the verification that at least one principal project team member holds a current, project-appropriate LEED AP credential, with a single human-in-the-loop checkpoint to confirm active project engagement.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| project_id | str | DeerFlow context | Non-empty UUID or internal project identifier |
| team_roster | List[Dict] | User upload (CSV/XLSX) | Min 1 row; each row must contain `name` and `role` |
| leed_project_type | str | DeerFlow context (LEED v5 credit selection) | Enum: `BD+C`, `ID+C`, `O+M`, `ND`, `Homes` |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| credential_number | str | null | LEED AP credential number (e.g., `LEED AP BD+C 12345`) if known |
| gbci_account_email | str | null | GBCI account email for directory lookup |
| auto_generate_report | bool | True | Whether to auto-generate verification report after HITL |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. Assert `project_id` is non-empty.
  2. Assert `team_roster` is a non-empty list with valid rows (`name`, `role` required per row).
  3. Assert `leed_project_type` is one of the allowed enum values (`BD+C`, `ID+C`, `O+M`, `ND`, `Homes`).
  4. If `credential_number` or `gbci_account_email` are provided, validate formats (credential regex: `^LEED AP [A-Z+&]+ \d+$`; email: standard RFC 5322 reduced).
- **Output:** `ValidatedInputs` dict with sanitized roster and normalized credential hints.
- **On Failure:** Return `ValidationError` with field-level details; halt workflow; notify project admin via email/Slack.

### Step 2: Lookup LEED AP Credentials (GBCI Directory)
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. For each team member where `credential_number` or `gbci_account_email` is provided, call GBCI Credential Directory API (`GET /api/v1/credentials/verify`).
  2. If no explicit credential data is provided, attempt fuzzy directory search using `name` + `role` (supplemental USGBC Member Directory `GET /api/v2/members/search` if enabled).
  3. Parse response for:
     - `credential_status`: `ACTIVE | EXPIRED | REVOKED | NOT_FOUND`
     - `credential_type`: e.g., `LEED AP BD+C`, `LEED AP O+M`
     - `expiration_date`: ISO-8601 date
     - `specialty`: must align with `leed_project_type` mapping:
       - `BD+C` → `LEED AP BD+C` (or `LEED AP` with legacy acceptable per GBCI guidance)
       - `ID+C` → `LEED AP ID+C`
       - `O+M` → `LEED AP O+M`
       - `ND` → `LEED AP ND`
       - `Homes` → `LEED AP Homes`
  4. Determine `specialty_match`: boolean = (`specialty == leed_project_type` OR legacy `LEED AP` grandfathered per project type rules).
  5. Cache API responses for 24 hours (`ttl=86400`) to respect rate limits and avoid duplicate lookups.
- **Output:** `CredentialLookupResult` list — one per team member with fields: `member_name`, `credential_found`, `credential_status`, `specialty_match`, `expiration_date`, `source_api`.
- **On Failure:**
  - GBCI API timeout / 5xx → Retry with exponential backoff (max 3 retries); if still failing, flag for HITL with message "GBCI directory unavailable; manual credential verification required."
  - 4xx (bad request, invalid credential format) → Return `LookupError`; do not retry; notify user to correct input.
  - Rate limit (429) → Backoff 60s, retry 2x; if still limited, queue for deferred retry and notify user.

### Step 3: Compliance Calculation
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. Filter `CredentialLookupResult` to members where:
     - `credential_status == 'ACTIVE'`
     - `specialty_match == True`
     - `expiration_date >= today()`
  2. Compute `compliance_met`: boolean = (`count(filtered_members) >= 1`).
  3. Compute `compliance_score`: float = 1.0 if `compliance_met` else 0.0.
  4. Identify `primary_leed_ap`: the first (or highest-priority by role) qualifying member from the roster.
  5. Return detailed `CalculationResult` including `primary_leed_ap`, `qualifying_members_count`, `disqualifying_members` (with reasons: expired, wrong specialty, not found).
- **Output:** `CalculationResult` dict.
- **On Failure:** If roster parsing produces inconsistent data, return `CalculationError`; log stack trace; notify admin.

### Step 4: HITL Checkpoint — Confirm Active Engagement
- **Type:** Human Review
- **Automated:** No
- **Description:**
  1. Pause workflow; create HITL ticket in DeerFlow Review UI.
  2. Present reviewer with:
     - Identified `primary_leed_ap` (name, credential number, specialty, expiration date, role on roster).
     - Project context (`project_id`, `leed_project_type`).
     - Pre-filled question: "Is this LEED AP actively engaged as a principal participant on this project?"
  3. Reviewer must explicitly select: `APPROVED`, `REJECTED`, or `NEEDS_CLARIFICATION`.
  4. If `APPROVED`: workflow resumes; generate documents.
  5. If `REJECTED`: workflow halts; return `HumanRejectionError`; notify project admin with reason.
  6. If `NEEDS_CLARIFICATION`: workflow pauses; notify admin to update roster / credential info; resume from Step 2 upon resubmission.
- **Output:** `HITLDecision` enum: `APPROVED | REJECTED | NEEDS_CLARIFICATION`.
- **On Failure:** If HITL ticket not claimed within SLA (48 hours), escalate to project manager; send reminder at 24 hours.

### Step 5: Generate Verification Report (PDF)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Using Jinja2 template `templates/prc2_leed_ap_report.html`, render:
     - Project metadata (project name, ID, date).
     - Verified LEED AP details (name, credential number, specialty, status, expiration, GBCI verification timestamp).
     - Compliance statement: "PRc2 LEED AP requirement satisfied: at least one principal participant holds a current LEED AP [Specialty] credential."
     - List of all team members checked (non-qualifying members shown with reason for exclusion).
     - HITL reviewer name, decision timestamp, and confirmation of active engagement.
  2. Convert HTML to PDF via WeasyPrint (or Puppeteer fallback).
  3. Embed digital signature / tamper-evident checksum (SHA-256) in PDF metadata.
- **Output:** `leed_ap_verification_report.pdf` (stored in project document vault; accessible via URL).
- **On Failure:** PDF generation failure → Retry 1x; if still failing, generate DOCX fallback; notify admin.

### Step 6: Generate Credential Confirmation (DOCX)
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. Using Jinja2 template `templates/prc2_credential_confirmation.docx`, generate a concise Word document:
     - Cover: project name, date, credit code PRc2.
     - Section 1: Verified LEED AP profile (name, credential, specialty, GBCI status screenshot reference if available).
     - Section 2: Project team role and HITL confirmation of active engagement.
     - Section 3: Declaration statement for LEED submission.
  2. Save as `.docx` in project vault.
- **Output:** `credential_confirmation.docx`.
- **On Failure:** DOCX generation failure → Retry 1x; if still failing, return error; admin notified.

### Step 7: Persist Results & Close
- **Type:** API Call / Persistence
- **Automated:** Yes
- **Description:**
  1. POST results to DeerFlow project ledger:
     - `credit_code`: PRc2
     - `points_awarded`: 1 (if compliance_met and HITL approved) else 0
     - `compliance_status`: `COMPLIANT | NON_COMPLIANT | PENDING_HITL`
     - `automation_level`: 90.1
     - `document_urls`: [PDF, DOCX]
     - `audit_trail`: all step timestamps, API call logs, HITL decision record
  2. Close workflow; return `SkillResult` to orchestrator.
- **Output:** `SkillResult` JSON.
- **On Failure:** Ledger persistence failure → Retry 3x with exponential backoff; if still failing, queue for retry; notify ops team.

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Step 4: Confirm Active Engagement | LEED AP / Project Manager / Sustainability Lead | 48 hours | Verify that the identified LEED AP (name, credential, specialty) is actively engaged as a principal participant on this specific project. Check project org chart or engagement letter if unsure. Reject if the AP is only nominally listed and not substantively involved. |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| GBCI Credential Directory (`https://www.gbci.org/api/v1/credentials/verify`) | Primary LEED AP credential verification (status, specialty, expiration) | Global | Manual credential check via GBCI web portal + uploaded PDF/screenshot | 100 req/min; burst 200 req/min for 10s |
| USGBC Member Directory (`https://www.usgbc.org/api/v2/members/search`) | Supplemental fuzzy search by name/email when credential number unknown | Global (USGBC members) | Manual team roster review | 60 req/min |
| DeerFlow Internal Ledger (`/api/v1/projects/{project_id}/credits`) | Persist final compliance results and document URLs | Global (project region) | Queue to local Redis; retry every 5 min | 1000 req/min |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| North America (US, CA) | Available | Full GBCI API access; highest data fidelity |
| Europe | Available | GBCI directory global; all specialties verifiable |
| Middle East | Available | GBCI directory global; no restrictions |
| Asia-Pacific | Available | GBCI directory global; latency may be higher; recommend caching |
| Latin America | Available | GBCI directory global; Spanish/Portuguese name matching may require fuzzy logic |
| Africa | Available | GBCI directory global; limited local GBCI offices, but API access unchanged |
| Global (All) | Available | GBCI is international; no region is blocked. Rate-limit caching recommended for high-latency regions. |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Invalid roster format (missing name/role) | Halt workflow; return ValidationError | Yes (project admin) | No |
| Invalid leed_project_type enum | Halt workflow; return ValidationError | Yes (project admin) | No |
| GBCI API timeout (5xx) | Exponential backoff: 2s, 4s, 8s | Yes (ops team after 3rd fail) | 3 |
| GBCI API rate limit (429) | Backoff 60s; retry twice | Yes (user, after 2nd fail) | 2 |
| Credential not found for hinted email/number | Continue; mark `NOT_FOUND`; try fuzzy search | No (silent) | No |
| No qualifying LEED AP after all lookups | Halt at Step 3; set compliance_score=0.0; skip HITL | Yes (project admin) | No |
| HITL ticket unclaimed (48h SLA breach) | Escalate to project manager | Yes (PM + admin) | N/A |
| HITL decision: REJECTED | Halt workflow; return HumanRejectionError | Yes (admin + AP) | No |
| PDF generation failure | Retry 1x; fallback to DOCX | Yes (admin if fallback also fails) | 1 |
| Ledger persistence failure | Retry 3x; queue to Redis | Yes (ops team after 3rd fail) | 3 |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| LEED AP Verification Report | PDF | Comprehensive verification report with credential details, compliance statement, full team audit, HITL confirmation, and tamper-evident checksum |
| Credential Confirmation | DOCX | Concise credential confirmation letter suitable for LEED submission documentation; includes declaration of active engagement |

## Testing
```bash
# Unit tests
python -m pytest skills/prc2/tests/test_validation.py -v
python -m pytest skills/prc2/tests/test_gbci_lookup.py -v
python -m pytest skills/prc2/tests/test_calculation.py -v
python -m pytest skills/prc2/tests/test_document_generation.py -v

# Integration tests (with mocked GBCI API)
python -m pytest skills/prc2/tests/test_integration.py -v

# End-to-end workflow test (LangGraph state machine)
python -m pytest skills/prc2/tests/test_e2e_workflow.py -v
```

## Example Usage (Deer-Flow)
```python
from deerflow.skills import LEEDAPSkill

skill = LEEDAPSkill(
    project_id="proj-abc-123",
    inputs={
        "team_roster": [
            {"name": "Jane Doe", "role": "Sustainability Consultant", "credential_number": "LEED AP BD+C 98765", "gbci_account_email": "jane.doe@firm.com"},
            {"name": "John Smith", "role": "Project Architect"},
        ],
        "leed_project_type": "BD+C",
        "auto_generate_report": True,
    }
)
result = await skill.execute()

# result structure:
# {
#   "credit_code": "PRc2",
#   "points_awarded": 1,
#   "compliance_status": "COMPLIANT",
#   "primary_leed_ap": {
#       "name": "Jane Doe",
#       "credential_number": "LEED AP BD+C 98765",
#       "specialty": "BD+C",
#       "status": "ACTIVE",
#       "expiration_date": "2027-06-15"
#   },
#   "documents": {
#       "verification_report_pdf": "https://vault.deerflow.io/proj-abc-123/prc2/leed_ap_verification_report.pdf",
#       "credential_confirmation_docx": "https://vault.deerflow.io/proj-abc-123/prc2/credential_confirmation.docx"
#   },
#   "hitl_checkpoint": {"step": 4, "decision": "APPROVED", "reviewer": "pm@client.com", "timestamp": "2025-01-15T09:23:00Z"},
#   "audit_trail": [...]
# }
```

## Deer-Flow Workflow (LangGraph)
```python
from langgraph.graph import StateGraph, END
from deerflow.skills.prc2.state import PRc2State
from deerflow.skills.prc2.nodes import (
    validate_inputs,
    lookup_credentials,
    calculate_compliance,
    hitl_confirm_engagement,
    generate_verification_report,
    generate_credential_confirmation,
    persist_results,
)

# Define the workflow graph
workflow = StateGraph(PRc2State)

# Nodes
workflow.add_node("validate", validate_inputs)
workflow.add_node("fetch_data", lookup_credentials)
workflow.add_node("calculate", calculate_compliance)
workflow.add_node("hitl_review", hitl_confirm_engagement)
workflow.add_node("generate_pdf", generate_verification_report)
workflow.add_node("generate_docx", generate_credential_confirmation)
workflow.add_node("persist", persist_results)

# Edges
workflow.set_entry_point("validate")
workflow.add_edge("validate", "fetch_data")
workflow.add_edge("fetch_data", "calculate")

# Conditional routing after calculation
workflow.add_conditional_edges(
    "calculate",
    lambda state: "hitl_review" if state["compliance_met"] else "persist",
    {"hitl_review": "hitl_review", "persist": "persist"}
)

# HITL conditional routing
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: state["hitl_decision"],
    {
        "APPROVED": "generate_pdf",
        "REJECTED": END,           # ends with rejection status
        "NEEDS_CLARIFICATION": END # ends with pending-clarification status
    }
)

# Document generation pipeline
workflow.add_edge("generate_pdf", "generate_docx")
workflow.add_edge("generate_docx", "persist")

# Terminal
workflow.add_edge("persist", END)

# Compile
app = workflow.compile()

# Execution
final_state = await app.ainvoke({
    "project_id": "proj-abc-123",
    "team_roster": [...],
    "leed_project_type": "BD+C",
})
```

## Notes & Edge Cases
- **Legacy LEED AP (without specialty):** Per GBCI guidance, a legacy `LEED AP` (earned before 2009 specialty migration) may satisfy PRc2 for any project type. The `specialty_match` calculation in Step 3 must include this grandfathered rule. If the API returns `credential_type == 'LEED AP'` with no specialty suffix, treat as valid for all project types.
- **Expired credential grace period:** GBCI occasionally offers a 30-day grace period for renewal. The `expiration_date >= today()` check should strictly follow the official expiration date; do not implement custom grace-period logic unless explicitly configured via `gbci_grace_period_enabled` flag (default: False).
- **Multiple qualifying LEED APs:** If more than one team member qualifies, the `primary_leed_ap` should be selected by role priority order: 1) Sustainability Consultant / LEED PM, 2) Architect / Designer, 3) Engineer, 4) Contractor, 5) Owner Rep. This ensures the most relevant AP is featured in the report.
- **Privacy:** GBCI credential numbers are PII-adjacent. Store encrypted at rest (AES-256-GCM). Do not log credential numbers in plaintext; use truncated hashes in audit logs.
- **Non-ASCII names:** GBCI directory supports Unicode. Ensure roster parsing handles diacritics and CJK characters correctly (UTF-8 throughout).
- **Reference Pattern:** This skill is designated the **reference implementation** for all LEED v5 automation skills. Future skills should mirror this file structure, HITL checkpoint style, error handling taxonomy, and LangGraph node/edge patterns.
```
