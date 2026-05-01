# Skill: PRc2 - LEED AP

## Metadata
- **Credit Code:** PRc2
- **Credit Name:** LEED AP
- **Points:** 1
- **Automation Level:** 95%
- **Complexity:** Low
- **Primary Data Source:** API
- **HITL Required:** No (Fully automated)

## Purpose
Encourage team integration required by a LEED AP and streamline application and certification process.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| team_members | array | User input | At least one member |

## Input Schema
```json
{
  "team_members": [
    {
      "name": "string",
      "email": "string",
      "role": "string",
      "leed_ap_number": "string (optional)"
    }
  ],
  "project_rating_system": "BD+C | ID+C | O+M"
}
```

## Workflow Steps (Durable)

### Step 1: validate_inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:** Verify team_members array is valid

### Step 2: verify_credentials
- **Type:** API Call
- **Automated:** Yes
- **API:** GBCI Credential Directory
- **Timeout:** 10 seconds per member
- **Retry:** 3x
- **Description:** Query GBCI for each team member's credential status
- **Output:** Array of {name, credential, status, expiration, specialty}

### Step 3: check_specialty_match
- **Type:** Validation
- **Automated:** Yes
- **Description:** Verify LEED AP specialty matches project type
- **Rules:**
  - BD+C project → LEED AP BD+C
  - ID+C project → LEED AP ID+C  
  - O+M project → LEED AP O+M
- **Output:** {matches: boolean, mismatches: array}

### Step 4: generate_report
- **Type:** Document Generation
- **Automated:** Yes
- **Template:** pr_c2_leed_ap_verification.html
- **Output:** PDF verification report

## HITL Checkpoints
None - fully automated

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| GBCI Credential Directory | Verify LEED AP status | Global | Manual verification | 1000/day |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| All Regions | Full | GBCI is global |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| API timeout | Retry | No | Auto (3x) |
| Credential not found | Flag for manual verification | Yes | Manual |
| Specialty mismatch | Include in report | No | N/A |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| leed_ap_verification | PDF | Credential verification for each team member |

## Testing
```bash
python -m pytest skills/pr_c2_leed_ap/tests/
```

## Example Usage
```python
from skills.pr_c2_leed_ap import LEEDAPSkill

skill = LEEDAPSkill(
    project_id="123",
    inputs={
        "team_members": [
            {"name": "John Doe", "email": "john@example.com", "leed_ap_number": "12345"}
        ],
        "project_rating_system": "BD+C"
    }
)

result = await skill.execute()
# Returns: {status: 'completed', documents: {...}}
```

## Why 95% Automation?
This skill is nearly fully automated because:
1. Single API call to GBCI
2. Clear verification rules
3. No complex calculations
4. No document interpretation
5. Binary pass/fail outcome

The 5% is for handling API failures gracefully.
