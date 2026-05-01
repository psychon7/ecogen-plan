# Skill: IPp3 - Carbon Assessment

## Metadata
- **Credit Code:** IPp3
- **Credit Name:** Carbon Assessment
- **Points:** 0 (Prerequisite)
- **Automation Level:** 85%
- **Complexity:** Medium
- **Primary Data Source:** API + Calculation
- **HITL Required:** Yes (Final review)

## Purpose
Understand and reduce long-term direct and indirect carbon emissions including on-site combustion, grid-supplied electricity, refrigerants, and embodied carbon.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| project_location | coordinates | User input | Valid lat/lon |
| energy_model_output | JSON/file | Upload | Required fields: electricity_kwh, natural_gas_therms, steam_mmbtu |
| material_quantities | JSON | Upload or manual | Array of {name, quantity, unit} |
| service_life | integer | User input | 25-100 years |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| refrigerant_schedule | JSON/file | None | Array of {type, charge_kg, gwp} |
| grid_region | string | Auto-detect | Override auto-detected grid region |
| use_future_projections | boolean | True | Include NREL Cambium projections (US only) |

## Workflow Steps (Durable)

### Step 1: validate_inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:** Verify all required inputs present and valid
- **Output:** ValidationResult
- **On Failure:** Stop, notify user of missing fields

### Step 2: fetch_grid_emission_factors
- **Type:** API Call
- **Automated:** Yes
- **API:** EPA eGRID (US) or National Grid API
- **Timeout:** 30 seconds
- **Retry:** 3x with exponential backoff
- **Output:** {co2_factor, ch4_factor, n2o_factor, year, source}
- **On Failure:** Use default factors, flag for manual verification

### Step 3: fetch_embodied_carbon_data
- **Type:** API Call
- **Automated:** Yes
- **API:** EC3 Database (Building Transparency)
- **Timeout:** 60 seconds
- **Retry:** 3x
- **Description:** Query EC3 for each material's GWP
- **Output:** Array of {material, gwp_per_unit, total_gwp, data_quality}
- **On Failure:** Flag materials for manual EPD entry

### Step 4: calculate_operational_carbon
- **Type:** Calculation
- **Automated:** Yes
- **Formula:**
  ```
  annual_co2 = (electricity_kwh * grid_co2_factor) + 
               (natural_gas_therms * 0.0053) + 
               (steam_mmbtu * 66.3)
  25yr_co2 = annual_co2 * service_life
  ```
- **Output:** {annual_operational_co2, 25yr_operational_co2}
- **On Failure:** Log error, stop workflow

### Step 5: calculate_refrigerant_emissions
- **Type:** Calculation
- **Automated:** Yes
- **Formula:**
  ```
  For each refrigerant:
    emissions = charge_kg * gwp * 0.025 * service_life
  total = sum(all refrigerants)
  ```
- **Output:** {refrigerant_co2, breakdown_by_type}
- **On Failure:** Set to 0, log warning

### Step 6: calculate_embodied_carbon
- **Type:** Calculation
- **Automated:** Yes
- **Formula:**
  ```
  For each material:
    material_co2 = quantity * gwp_per_unit
  total = sum(all materials)
  top_3 = sort by material_co2, take top 3
  ```
- **Output:** {embodied_co2, top_3_hotspots, material_breakdown}
- **On Failure:** Log error, stop workflow

### Step 7: generate_projection
- **Type:** Calculation
- **Automated:** Yes
- **Formula:**
  ```
  total_25yr_co2 = 25yr_operational_co2 + refrigerant_co2 + embodied_co2
  ```
- **Output:** {operational, refrigerant, embodied, total_25yr_co2}

### Step 8: generate_future_projections (US only)
- **Type:** API Call
- **Automated:** Yes
- **API:** NREL Cambium
- **Condition:** use_future_projections == true AND US location
- **Output:** {decarbonization_scenarios, projected_grid_factors}

### Step 9: generate_report
- **Type:** Document Generation
- **Automated:** Yes
- **Template:** ip_p3_carbon_report.html
- **Output:** PDF report, Excel workbook
- **On Failure:** Retry 2x, then stop

### Step 10: HITL_REVIEW
- **Type:** Human Review
- **Automated:** No
- **Assignee:** LEED Consultant
- **SLA:** 24 hours
- **Instructions:**
  1. Verify energy model inputs match project
  2. Check material quantities are accurate
  3. Confirm grid emission factors are appropriate for location
  4. Review calculations for reasonableness
  5. Check top 3 carbon hotspots are identified correctly
- **Checklist:**
  - [ ] Energy model inputs verified
  - [ ] Material quantities accurate
  - [ ] Grid factors appropriate
  - [ ] Calculations reasonable
  - [ ] Hotspots correctly identified
- **On Rejection:** Return to specified step with comments

### Step 11: finalize_output
- **Type:** Output Generation
- **Automated:** Yes
- **Description:** Generate final PDF, Excel, and USGBC submission form
- **Output:** {pdf_report, excel_workbook, usgbc_form}

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| After report generation | LEED Consultant | 24h | Review calculations and approve |
| If API data missing | Data Steward | 48h | Provide manual data entry |
| Final submission | Project Manager | 24h | Approve for USGBC submission |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| EPA eGRID | Grid emission factors | US only | National grid data | 1000/day |
| EC3 Database | Embodied carbon | Global | Manual EPD entry | 1000/day |
| NREL Cambium | Future grid scenarios | US only | Skip projections | 1000/hour |
| IPCC AR6 | GWP values | Global | Static data file | N/A |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Full | All APIs available |
| Canada | Full | Use NRCan for grid data |
| European Union | Partial | Use EU grid data, no Cambium |
| United Kingdom | Partial | Use UK grid data, no Cambium |
| Australia | Partial | Use AEMO data, no Cambium |
| Other | Partial | Grid data may need manual entry |

## Error Handling
| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| API timeout | Retry with backoff | No | Auto (3x) |
| Invalid coordinates | Stop, prompt user | Yes | Manual |
| Missing material data | Flag for manual entry | Yes | Manual |
| Calculation mismatch | Alert reviewer | Yes | Manual |
| EC3 material not found | Suggest alternatives | Yes | Manual |

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| carbon_projection_report | PDF | 25-year projection with charts and analysis |
| calculation_workbook | Excel | Detailed calculations with formulas visible |
| usgbc_submission_form | PDF | Pre-filled USGBC submission template |
| material_hotspots | PDF | Top 3 carbon hotspots with reduction strategies |

## Testing
```bash
# Run unit tests
python -m pytest skills/ip_p3_carbon/tests/

# Run integration test
python skills/ip_p3_carbon/agent.py --test-mode --project-id=test123

# Run with sample data
python skills/ip_p3_carbon/agent.py --input-file=sample_data.json
```

## Example Usage
```python
from skills.ip_p3_carbon import CarbonAssessmentSkill

skill = CarbonAssessmentSkill(
    project_id="123",
    inputs={
        "project_location": {"lat": 40.7128, "lon": -74.0060},
        "energy_model_output": {
            "electricity_kwh": 500000,
            "natural_gas_therms": 10000,
            "steam_mmbtu": 0
        },
        "material_quantities": [
            {"name": "Concrete - 30 MPa", "quantity": 1000, "unit": "m3"},
            {"name": "Steel - Rebar", "quantity": 50000, "unit": "kg"}
        ],
        "service_life": 25,
        "refrigerant_schedule": [
            {"type": "R-410A", "charge_kg": 100, "gwp": 2088}
        ]
    }
)

result = await skill.execute()
# Returns: {status: 'completed', documents: {...}, review_record: {...}}
```

## Confidence Score Calculation
```python
def calculate_confidence(inputs, api_results):
    score = 100
    
    # Deduct for missing optional data
    if 'refrigerant_schedule' not in inputs:
        score -= 5
    
    # Deduct for API fallbacks
    if api_results['grid_source'] != 'EPA eGRID':
        score -= 10
    
    # Deduct for EC3 material matches
    poor_matches = sum(1 for m in api_results['materials'] if m['match_quality'] < 0.8)
    score -= poor_matches * 5
    
    return max(score, 50)  # Minimum 50% confidence
```

## Known Limitations
1. **Future projections** only available for US (NREL Cambium)
2. **Material matching** to EC3 database may require human verification for non-standard materials
3. **Grid emission factors** outside US/CA/EU/UK/AU may need manual entry
4. **Refrigerant GWP values** assume 2.5% annual leak rate (may vary by system type)

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-21 | Initial release |
