# Skill: EAc3 - Enhanced Energy Efficiency

## Metadata
- **Credit Code:** EAc3
- **Credit Name:** Enhanced Energy Efficiency
- **Points:** 10 (NC) / 7 (CS) - **HIGHEST POINT VALUE**
- **Automation Level:** 70%
- **Complexity:** High
- **Primary Data Source:** Energy Model Output + Calculation
- **HITL Required:** Yes (Expert review required)

## Purpose
Reduce environmental and economic harm from excessive energy use by achieving increasing levels of energy efficiency.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| proposed_energy_model | file | Upload | EnergyPlus, IES, Trace, or eQuest format |
| baseline_energy_model | file | Upload | Per ASHRAE 90.1 Appendix G |
| building_type | string | User input | Valid ASHRAE type |
| climate_zone | string | User input | Valid ASHRAE climate zone |
| floor_area | number | User input | > 0 |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| modeling_software | string | "auto-detect" | EnergyPlus, IES-VE, Trace 3D, eQuest |
| baseline_method | string | "Appendix G" | Alternative compliance method |
| energy_cost_rates | object | Auto-fetch | {electricity: $/kWh, gas: $/therm} |

## The Reality: Why Only 70% Automation?

### What AI CAN Do (70%):
1. Parse energy model outputs (structured data)
2. Calculate percent improvement: `(Baseline - Proposed) / Baseline * 100`
3. Map improvement to points (6-50% = 1-10 points)
4. Generate comparison reports
5. Validate data completeness

### What AI CANNOT Do (30% - Requires Human):
1. **Verify model accuracy** - AI cannot tell if energy model is correct
2. **Assess modeling assumptions** - Baseline vs proposed assumptions
3. **Evaluate optimization strategies** - What improvements are feasible?
4. **Interpret complex results** - Unusual energy patterns
5. **Make compliance decisions** - Final approval requires expertise

### The Energy Modeling Problem

```
Energy modeling is EXPERT WORK requiring:
- Understanding of building physics
- Knowledge of HVAC systems
- Familiarity with ASHRAE 90.1 Appendix G
- Experience with modeling software
- Judgment on reasonable assumptions

AI can ASSIST but not REPLACE energy modelers.
```

## Workflow Steps (Durable)

### Step 1: validate_inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:** Verify all required files and data present
- **Checks:**
  - Files are valid energy model formats
  - Building type is valid
  - Climate zone is valid
  - Floor area > 0

### Step 2: parse_energy_models
- **Type:** Data Extraction
- **Automated:** Yes
- **Description:** Extract energy consumption data from model outputs
- **Supported Formats:**
  - EnergyPlus: HTML/CSV output
  - IES-VE: ApacheSim results
  - Trace 3D: Load summary
  - eQuest: SIM file output
- **Output:** {annual_energy_cost, energy_by_end_use, peak_demands}
- **On Failure:** Stop, request correct format

### Step 3: fetch_energy_rates
- **Type:** API Call
- **Automated:** Yes
- **API:** EIA (US) or national energy statistics
- **Description:** Get local energy cost rates
- **Output:** {electricity_rate, gas_rate, source}
- **On Failure:** Use default rates, flag for manual entry

### Step 4: calculate_energy_costs
- **Type:** Calculation
- **Automated:** Yes
- **Formula:**
  ```
  Proposed Cost = (Electricity_kWh * Elec_Rate) + (Gas_Therms * Gas_Rate)
  Baseline Cost = (Baseline_Elec_kWh * Elec_Rate) + (Baseline_Gas_Therms * Gas_Rate)
  ```
- **Output:** {proposed_cost, baseline_cost}

### Step 5: calculate_percent_improvement
- **Type:** Calculation
- **Automated:** Yes
- **Formula:**
  ```
  % Improvement = (Baseline_Cost - Proposed_Cost) / Baseline_Cost * 100
  ```
- **Output:** {percent_improvement, cost_savings}

### Step 6: calculate_points
- **Type:** Calculation
- **Automated:** Yes
- **LEED v5 Points Table:**
  | Improvement | Points |
  |-------------|--------|
  | 6% | 1 |
  | 10% | 2 |
  | 14% | 3 |
  | 18% | 4 |
  | 22% | 5 |
  | 26% | 6 |
  | 30% | 7 |
  | 34% | 8 |
  | 38% | 9 |
  | 42% | 10 |
- **Output:** {points_achievable, next_threshold}

### Step 7: generate_comparison_report
- **Type:** Document Generation
- **Automated:** Yes
- **Template:** ea_c3_energy_comparison.html
- **Output:** PDF comparison report

### Step 8: HITL_ENERGY_MODELER_REVIEW
- **Type:** Expert Review
- **Automated:** No
- **Assignee:** Energy Modeler / LEED Consultant
- **SLA:** 48 hours
- **Critical:** This step is REQUIRED - AI cannot approve energy models
- **Instructions:**
  1. Verify proposed energy model is accurate
  2. Confirm baseline model follows ASHRAE 90.1 Appendix G
  3. Check modeling assumptions are reasonable
  4. Validate energy rates are appropriate
  5. Confirm percent improvement calculation is correct
  6. Assess if optimization opportunities exist
- **Checklist:**
  - [ ] Proposed model accuracy verified
  - [ ] Baseline model compliance confirmed
  - [ ] Modeling assumptions reviewed
  - [ ] Energy rates validated
  - [ ] Calculations checked
  - [ ] Optimization opportunities identified
- **On Rejection:** Return to appropriate step with detailed comments

### Step 9: identify_optimization_opportunities
- **Type:** AI Analysis
- **Automated:** Yes
- **Description:** AI suggests potential improvements based on model data
- **Output:** {opportunities: array, estimated_impact: array}
- **Examples:**
  - "HVAC efficiency improvement could add 3% savings"
  - "Lighting power density reduction could add 2% savings"
- **Note:** These are SUGGESTIONS only - energy modeler decides feasibility

### Step 10: generate_final_report
- **Type:** Document Generation
- **Automated:** Yes
- **Template:** ea_c3_enhanced_energy.html
- **Output:** Final PDF report, Excel workbook

### Step 11: HITL_FINAL_APPROVAL
- **Type:** Final Review
- **Automated:** No
- **Assignee:** Project Manager / LEED AP
- **SLA:** 24 hours
- **Instructions:**
  1. Review all documentation
  2. Confirm points achievable
  3. Approve for USGBC submission
- **Checklist:**
  - [ ] All documentation reviewed
  - [ ] Points achievable confirmed
  - [ ] Ready for submission

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Energy modeler review | Energy Modeler | 48h | Verify model accuracy and approve calculations |
| Final approval | Project Manager | 24h | Approve for USGBC submission |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| EIA | Energy cost rates | US only | Manual entry | 1000/day |
| National stats | Energy rates | Country-specific | Manual entry | Varies |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Full | EIA data available |
| Canada | Full | NRCan data available |
| European Union | Full | Eurostat data available |
| United Kingdom | Full | BEIS data available |
| Australia | Full | AEMO data available |
| Other | Partial | May need manual energy rate entry |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Invalid model format | Stop, request correct format | Yes | Manual |
| Model parsing failure | Stop, flag for manual review | Yes | Manual |
| Energy rates unavailable | Use defaults, flag for review | Yes | Manual |
| Negative improvement | Alert, likely model error | Yes | Manual |
| Improvement > 60% | Flag for verification | Yes | Manual |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| energy_comparison_report | PDF | Proposed vs baseline comparison |
| calculation_workbook | Excel | Detailed calculations |
| optimization_opportunities | PDF | AI-suggested improvements |
| usgbc_submission_form | PDF | Pre-filled USGBC form |

## Testing
```bash
# Run with sample energy models
python skills/ea_c3_energy_enhanced/agent.py \
  --proposed-model sample_proposed.idf \
  --baseline-model sample_baseline.idf \
  --building-type "Office" \
  --climate-zone "4A"
```

## Example Usage
```python
from skills.ea_c3_energy_enhanced import EnergyEfficiencySkill

skill = EnergyEfficiencySkill(
    project_id="123",
    inputs={
        "proposed_energy_model": "/path/to/proposed.html",
        "baseline_energy_model": "/path/to/baseline.html",
        "building_type": "Office",
        "climate_zone": "4A",
        "floor_area": 50000
    }
)

result = await skill.execute()
# Returns: {status: 'completed', points: 7, documents: {...}}
```

## Integration with Energy Modeling Software

### EnergyPlus
```python
# Parse EnergyPlus HTML output
def parse_energyplus_output(html_path):
    tables = extract_tables_from_html(html_path)
    
    # Extract key values
    annual_electricity = tables['Annual Building Utility Performance Summary']['Electricity']['Total']
    annual_gas = tables['Annual Building Utility Performance Summary']['Natural Gas']['Total']
    
    return {
        'electricity_kwh': annual_electricity,
        'gas_therms': annual_gas
    }
```

### IES-VE
```python
# Parse IES ApacheSim results
def parse_ies_output(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Extract energy consumption
    annual_results = root.find('.//AnnualResults')
    electricity = float(annual_results.find('Electricity').text)
    gas = float(annual_results.find('NaturalGas').text)
    
    return {
        'electricity_kwh': electricity,
        'gas_therms': gas
    }
```

## Why This Credit Requires Expert Review

### Example Scenario
```
AI Calculation:
- Baseline Cost: $100,000
- Proposed Cost: $75,000
- Improvement: 25%
- Points: 6

Human Review Reveals:
- Baseline model used wrong HVAC efficiency
- Correct baseline: $90,000
- Actual improvement: 16.7%
- Correct points: 3

AI cannot detect modeling errors - only humans can.
```

## Recommendations

### For Platform Users
1. Always have energy modeler review AI calculations
2. Use AI for initial analysis, expert for final approval
3. Don't skip HITL checkpoints - they're there for a reason

### For Platform Development
1. Invest in robust energy model parsers
2. Build validation rules to catch obvious errors
3. Make HITL workflow seamless for energy modelers
4. Provide clear guidance on what AI can/cannot do

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-21 | Initial release with 70% automation target |
