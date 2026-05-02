# SKILL.md

## Metadata
- **Credit Code:** EAp5
- **Credit Name:** Fundamental Refrigerant Management
- **Points:** Required (Prerequisite)
- **Automation Level:** 85.2%
- **Complexity:** Low
- **Primary Data Sources:** EPA SNAP Program, AHRI Directory, IPCC AR6 GWP values
- **Data Availability Score:** 90/100
- **Real-time:** Yes (for EPA SNAP & AHRI lookups)
- **HITL Required:** Yes

## Purpose
Automate the creation, validation, and documentation of a project's refrigerant inventory to demonstrate that all HVAC&R equipment uses refrigerants compliant with LEED v5's fundamental refrigerant management requirements (no CFCs, GWP thresholds met, and inventory accurately quantified).

## Inputs (Required)

| Field | Type | Source | Validation |
|-------|------|--------|------------|
| `equipment_schedule` | XLSX / CSV | Upload | Must contain columns: `equipment_id`, `equipment_type`, `manufacturer`, `model`, `refrigerant_type`, `refrigerant_charge_kg`, `refrigerant_charge_lbs`, `num_units`, `location_zone`. |
| `project_location` | String | Project Profile | Valid ISO 3166-1 alpha-2 country code + optional region/state code (e.g., `US-CA`, `CA-ON`). |
| `leak_rate_assumption` | Float | Upload or Default | Annual leakage rate as a decimal (e.g., `0.02` = 2%). Validated to be between `0.001` and `0.5`. |

## Inputs (Optional)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `regulatory_framework` | String | `"LEEDv5"` | Can be `"LEEDv5"`, `"ASHRAE_15_34"`, or `"EU_F_Gas"` to apply regional phase-out rules. |
| `gwp_time_horizon` | String | `"100yr"` | Time horizon for GWP values: `"20yr"`, `"100yr"` (default), or `"500yr"`. |
| `include_emission_projection` | Boolean | `true` | Whether to calculate the 25-year emission projection. |
| `equipment_certifications` | JSON | `{}` | Optional mapping of `equipment_id` -> `certification_number` (e.g., AHRI certificate) for cross-reference. |

## Workflow Steps (Durable)

### Step 1: Validate Inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:**
  1. Parse `equipment_schedule` (XLSX/CSV) into a structured pandas DataFrame.
  2. Validate required columns exist. If `refrigerant_charge_kg` is missing but `refrigerant_charge_lbs` is present, convert using `kg = lbs * 0.453592`.
  3. Check for null or invalid values (e.g., negative charge, zero units).
  4. Validate `project_location` against a known list of ISO country codes.
  5. Return a validated DataFrame and a list of parsing warnings (if any).
- **Output:** `validated_dataframe`, `validation_warnings`
- **On Failure:** Return HTTP 400 with a detailed error log indicating missing columns, invalid rows, and suggested corrections. Do NOT proceed.

### Step 2: Fetch Refrigerant Properties
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. For each unique `refrigerant_type` in the schedule, query the internal **IPCC AR6 GWP Static Database** to retrieve:
     - `gwp_value` (based on `gwp_time_horizon`)
     - `chemical_formula`
     - `is_cfc` (Boolean)
     - `is_hcfc` (Boolean)
  2. If a refrigerant is not found in the static database, attempt a fallback lookup via the **EPA SNAP Approved Substitutes API** (`https://www.epa.gov/snap/snap-substitutes`) to identify the chemical blend and estimate GWP.
  3. Flag any refrigerant where `is_cfc == true` as an immediate compliance failure.
- **Output:** `refrigerant_properties_map` (dict: `refrigerant_type` -> properties)
- **On Failure:** If a refrigerant type is completely unrecognized, flag it for HITL review in Step 6.

### Step 3: Cross-Reference Equipment Certifications
- **Type:** API Call
- **Automated:** Yes
- **Description:**
  1. For each unique `manufacturer` + `model` combination, query the **AHRI Directory API** (`https://www.ahridirectory.org/`) to verify:
     - Certified refrigerant type matches the submitted `refrigerant_type`.
     - Certified charge amount is within ±10% of the submitted `refrigerant_charge`.
  2. Log discrepancies as warnings.
  3. If `equipment_certifications` is provided, prioritize the AHRI certificate number for a direct lookup to ensure accuracy.
- **Output:** `certification_verification_results` (list of match/mismatch/warning records)
- **On Failure:** If AHRI API is unreachable, log a warning and skip this step; do not block the workflow.

### Step 4: Perform Calculations
- **Type:** Calculation
- **Automated:** Yes
- **Description:**
  1. **Total Refrigerant Charge:**
     - `total_charge_kg = Σ(refrigerant_charge_kg * num_units)` for all equipment rows.
  2. **Weighted Average GWP:**
     - `weighted_avg_gwp = Σ(refrigerant_charge_kg * num_units * gwp_value) / total_charge_kg`
  3. **Compliance Check:**
     - If any equipment has `is_cfc == true` -> `COMPLIANCE_FAIL` (CFCs are prohibited).
     - If `regulatory_framework == "LEEDv5"`: No explicit GWP cap for the prerequisite, but flag any refrigerant with GWP > 2000 as a "High-GWP Warning" for consideration.
  4. **25-Year Emission Projection (optional):**
     - `emission_projection_kg_co2e = total_charge_kg * leak_rate_assumption * weighted_avg_gwp * 25`
- **Output:** `calculation_results` (JSON object containing all computed metrics and compliance status)
- **On Failure:** If division by zero occurs (e.g., zero total charge), return a math error and halt.

### Step 5: Apply Regional Phase-Out Rules
- **Type:** Calculation / API Call
- **Automated:** Yes
- **Description:**
  1. Based on `project_location` and `regulatory_framework`, apply known regional phase-out schedules (e.g., EU F-Gas Regulation, US EPA SNAP Rules 20/21, Canada's ODS regulations).
  2. Check if any `refrigerant_type` is scheduled for phase-out in the project's region within the building's operational lifetime (e.g., 25 years).
  3. Flag phase-out risks in the compliance report.
- **Output:** `regional_compliance_flags` (list of warnings about future phase-outs)
- **On Failure:** If regional rules are unknown for the location, log a warning and continue.

### Step 6: Human Review Checkpoint (HITL)
- **Type:** Human Review
- **Automated:** No
- **Description:**
  1. Present the aggregated refrigerant inventory, GWP analysis, and flagged discrepancies (from AHRI cross-reference and unknown refrigerants) to a human reviewer.
  2. Reviewer must verify:
     - Refrigerant types and charges are accurately transcribed from the original equipment schedules/submittals.
     - Any flagged mismatches (e.g., AHRI says R-454B, schedule says R-410A) are resolved.
     - Any refrigerants not found in the database are manually identified and GWP values provided.
  3. Reviewer can approve, reject, or request corrections.
- **Output:** `hitl_approval_status` (`approved`, `rejected`, `corrections_needed`)
- **On Failure:** If rejected, workflow halts and returns feedback to the user.

### Step 7: Generate Output Documents
- **Type:** Document Generation
- **Automated:** Yes
- **Description:**
  1. **Refrigerant Inventory & GWP Analysis (PDF):**
     - Table of all equipment with charges, refrigerants, and GWP values.
     - Summary of total charge, weighted average GWP, and compliance status.
     - 25-year emission projection chart (if enabled).
  2. **Compliance Declaration (DOCX):**
     - Formal letter stating that the project does not use CFC-based refrigerants.
     - Statement of weighted average GWP and confirmation of compliance with LEED v5 EAp5.
     - Appendices for AHRI certifications and EPA SNAP listings.
  3. **Calculation Table (XLSX):**
     - Raw data + calculated columns (total charge per row, GWP, CO2e) for auditor review.
- **Output:** `document_package` (paths to generated PDF, DOCX, XLSX)
- **On Failure:** If document generation fails (e.g., missing template), retry once. If retry fails, notify human operator.

## HITL Checkpoints

| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| 6 | LEED Project Administrator / MEP Engineer | 24 hours | 1. Verify refrigerant types and charges against original equipment schedules. <br> 2. Resolve any AHRI certification mismatches. <br> 3. Manually identify GWP for any refrigerants not in the IPCC/EPA database. <br> 4. Confirm compliance declaration text is accurate. |

## API Dependencies

| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| **EPA SNAP Substitutes API** | Verify approved refrigerants and retrieve GWP estimates | US (Global read access) | Static IPCC AR6 database | Public, no strict limit; throttle to 1 req/sec |
| **AHRI Directory API** | Verify equipment certifications and refrigerant charges | Global (US-centric data) | Manual AHRI certificate PDF lookup | ~1000 requests/day |
| **IPCC AR6 Static DB** | Primary GWP values for all refrigerants | Global | Manual lookup from IPCC report tables | N/A (local data) |

## Regional Availability

| Region | Status | Notes |
|--------|--------|-------|
| US | Available | Full EPA SNAP and AHRI integration. US-specific phase-out rules (SNAP Rules 20/21) applied. |
| Canada | Available | AHRI data applicable. Canadian ODS regulations cross-referenced. |
| EU / UK | Available | EU F-Gas Regulation phase-out schedule applied. AHRI coverage may be partial for EU-specific models. |
| APAC | Available | IPCC GWP data is global. AHRI coverage varies by manufacturer; fallback to manual certification. |
| Middle East / Africa | Available | IPCC GWP data is global. Regional phase-out rules may be limited; generic Montreal Protocol rules applied. |
| Latin America | Available | IPCC GWP data is global. AHRI coverage for major manufacturers (Carrier, Trane, Daikin) is good. |

## Error Handling

| Error | Action | Human Notification | Retry |
|-------|--------|-------------------|-------|
| Invalid equipment schedule format | Halt workflow, return 400 error with column mapping guide | Yes (immediate email) | No |
| Unknown refrigerant type | Flag for HITL review in Step 6 | Yes (in HITL dashboard) | No (requires human input) |
| AHRI API timeout / 429 | Skip Step 3, log warning, continue workflow | No (logged only) | Yes (2 retries with backoff) |
| EPA SNAP API failure | Use IPCC static DB fallback | No | Yes (2 retries) |
| Division by zero in calculation | Halt workflow, return math error | Yes | No |
| Document generation failure | Retry once, then alert human operator | Yes (if retry fails) | Yes (1 retry) |
| HITL rejection | Halt workflow, return reviewer feedback to user | Yes | N/A |

## Output Documents

| Document | Format | Description |
|----------|--------|-------------|
| Refrigerant Inventory & GWP Analysis | PDF | Complete inventory table, summary metrics, compliance status, and emission projection chart. |
| Compliance Declaration | DOCX | Formal signed-ready declaration confirming no CFC use and LEED v5 EAp5 compliance. |
| Calculation Table | XLSX | Detailed spreadsheet with all inputs, intermediate calculations, and GWP values for auditor traceability. |

## Testing

```bash
# Unit tests for calculation logic, API mocks, and document generation
python -m pytest skills/leed-ea-p5-refrigerant/tests/

# Key test cases:
# 1. test_validate_inputs_missing_columns
# 2. test_gwp_calculation_weighted_average
# 3. test_cfc_detection_failure
# 4. test_ahri_api_timeout_fallback
# 5. test_emission_projection_formula
# 6. test_document_generation_end_to_end
```

## Example Usage (Deer-Flow)

```python
from deerflow.skills import RefrigerantManagementSkill

skill = RefrigerantManagementSkill(
    project_id="12345",
    inputs={
        "equipment_schedule": "/uploads/hvac_schedule.xlsx",
        "project_location": "US-CA",
        "leak_rate_assumption": 0.02,
        "regulatory_framework": "LEEDv5",
        "gwp_time_horizon": "100yr",
        "include_emission_projection": True,
    }
)

# Execute the full workflow
result = await skill.execute()

# Expected result structure:
# {
#   "compliance_status": "PASS",
#   "total_charge_kg": 1250.5,
#   "weighted_avg_gwp": 675.4,
#   "emission_projection_kg_co2e": 421875.0,
#   "documents": {
#     "inventory_pdf": "/output/refrigerant_inventory.pdf",
#     "declaration_docx": "/output/compliance_declaration.docx",
#     "calculations_xlsx": "/output/calculation_table.xlsx"
#   },
#   "hitl_checkpoint": None  # or details if flagged
# }
```

## Deer-Flow Workflow (LangGraph)

```python
from langgraph.graph import StateGraph, END
from deerflow.skills.leed_ea_p5_refrigerant import states, nodes

# Define the state schema
class EAp5State(dict):
    """State schema for EAp5 Refrigerant Management workflow."""
    project_id: str
    inputs: dict
    validated_df: any  # pandas DataFrame
    refrigerant_props: dict
    certification_results: list
    calculations: dict
    regional_flags: list
    hitl_status: str  # "pending", "approved", "rejected"
    documents: dict
    errors: list

# Initialize the workflow
workflow = StateGraph(EAp5State)

# Add nodes
workflow.add_node("validate", nodes.validate_inputs_node)
workflow.add_node("fetch_props", nodes.fetch_refrigerant_properties_node)
workflow.add_node("certify", nodes.cross_reference_ahri_node)
workflow.add_node("calculate", nodes.perform_calculations_node)
workflow.add_node("regional", nodes.apply_regional_rules_node)
workflow.add_node("hitl_review", nodes.human_review_checkpoint_node)  # HITL gate
workflow.add_node("generate", nodes.generate_documents_node)

# Define edges
workflow.set_entry_point("validate")
workflow.add_edge("validate", "fetch_props")
workflow.add_edge("fetch_props", "certify")
workflow.add_edge("certify", "calculate")
workflow.add_edge("calculate", "regional")
workflow.add_edge("regional", "hitl_review")

# Conditional edge from HITL
workflow.add_conditional_edges(
    "hitl_review",
    lambda state: "generate" if state.get("hitl_status") == "approved" else END,
    {"generate": "generate", END: END}
)

workflow.add_edge("generate", END)

# Compile the graph
app = workflow.compile()

# Run the workflow
initial_state = {
    "project_id": "12345",
    "inputs": {...},
    "errors": []
}
result = await app.ainvoke(initial_state)
```

---

## Appendix A: IPCC AR6 GWP Reference Values (Common Refrigerants)

| Refrigerant | Chemical Formula | 100-yr GWP | Is CFC? | Is HCFC? |
|-------------|------------------|------------|---------|----------|
| R-11 | CCl3F | 5,350 | Yes | No |
| R-12 | CCl2F2 | 10,900 | Yes | No |
| R-22 | CHClF2 | 1,810 | No | Yes |
| R-134a | CH2FCF3 | 1,430 | No | No |
| R-410A | R-32/125 (50/50) | 2,088 | No | No |
| R-407C | R-32/125/134a (23/25/52) | 1,774 | No | No |
| R-32 | CH2F2 | 675 | No | No |
| R-454B | R-32/1234yf (68.9/31.1) | 466 | No | No |
| R-1234yf | CF3CF=CH2 | <1 | No | No |
| R-1234ze(E) | CF3CH=CHF | <1 | No | No |
| R-513A | R-1234yf/134a (56/44) | 631 | No | No |
| R-515B | R-1234ze(E)/227ea (91/9) | 299 | No | No |
| R-516A | R-1234yf/134a/152a (77.5/8.5/14) | 439 | No | No |
| R-744 (CO2) | CO2 | 1 | No | No |
| R-717 (Ammonia) | NH3 | 0 | No | No |

*Note: The skill references a complete local IPCC AR6 database. The table above is illustrative.*

## Appendix B: Compliance Rules Summary

### LEED v5 EAp5 Requirements
1. **No CFCs:** The project must not use CFC-based refrigerants in any new or existing HVAC&R equipment.
2. **Inventory:** A complete inventory of all refrigerants used must be provided, including type and total charge.
3. **No GWP Cap for Prerequisite:** Unlike the credit (EAc4), the prerequisite does not enforce a specific GWP threshold. However, documenting GWP is required to inform the 25-year emission projection.

### Regional Phase-Out Rules (Examples)
- **US EPA SNAP Rule 20:** Phases out certain HFCs in specific end-uses (e.g., R-404A, R-507A in supermarket refrigeration).
- **US EPA SNAP Rule 21:** Phases out HFCs in chillers and other applications.
- **EU F-Gas Regulation (517/2014):** Mandates GWP-based bans and quota system for HFCs.
- **Canada:** Follows Montreal Protocol schedule for HCFC phase-out.