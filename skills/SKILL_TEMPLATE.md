# Skill Template

Use this template to create new credit skills.

```markdown
# Skill: [Credit Code] - [Credit Name]

## Metadata
- **Credit Code:** [Code]
- **Credit Name:** [Name]
- **Points:** [X]
- **Automation Level:** [X%]
- **Complexity:** [Low/Medium/High]
- **Primary Data Source:** [API/Calculation/Manual]
- **HITL Required:** [Yes/No]

## Purpose
[One sentence description]

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| | | | |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| | | | |

## Workflow Steps (Durable)

### Step X: [name]
- **Type:** [Validation/API Call/Calculation/Document Generation/Human Review]
- **Automated:** [Yes/No]
- **Description:** [What this step does]
- **Output:** [What it returns]
- **On Failure:** [What happens on error]

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| | | | |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| | | | | |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| | | |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| | | | |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| | | |

## Testing
```bash
python -m pytest skills/[code]/tests/
```

## Example Usage
```python
from skills.[code] import [SkillClass]

skill = [SkillClass](project_id="123", inputs={...})
result = await skill.execute()
```
```

## Automation Level Guidelines

### 95%+ Automation (Low Complexity, API-based)
- Single API call
- Clear pass/fail rules
- No interpretation needed
- Examples: PRc2 (LEED AP), SSc6 (Light Pollution)

### 80-90% Automation (Medium Complexity)
- Multiple API calls
- Calculations with clear formulas
- Template-based document generation
- One HITL checkpoint for final review
- Examples: IPp3 (Carbon), WEp2 (Water), MRp2 (Embodied)

### 60-75% Automation (High Complexity)
- Complex calculations or data interpretation
- Multiple HITL checkpoints
- Expert review required
- Limited regional data availability
- Examples: EAc3 (Energy), LTc1 (Land Protection), MRc2 (Embodied Reduction)

### <60% Automation (Expert Work)
- Requires significant human judgment
- AI assists but cannot automate core work
- May not be worth building as skill
- Examples: Credits requiring custom energy modeling, complex site analysis
