# Manual Data Input Framework

## Purpose

When external APIs are unavailable for a region (e.g., Singapore flood maps, soil data, building code parameters), the platform must provide a structured, validated, auditable pathway for consultants to manually source and input the required data. This is not a fallback — it is a **first-class data acquisition mode** with the same confidence scoring, evidence tracking, and HITL review as API-sourced data.

---

## Design Principles

1. **Guided, not open-ended**: Every manual field includes context (what it is, where to find it, what format/units, acceptable range).
2. **Evidence-linked**: Every manual entry must attach a source document (PDF, screenshot, URL, or reference).
3. **Validated at entry**: Range checks, unit validation, format enforcement, and completeness checks run on input.
4. **Confidence-scored**: Manual entries receive a lower base confidence than API data (0.70 vs 0.90) but can be upgraded with verified evidence.
5. **Auditable**: All manual entries are timestamped, attributed to a user, and immutable in the audit trail.
6. **Reusable**: Manual data entered for one credit can be shared across related credits in the same project.

---

## Data Entry Modes

### Mode 1: Structured Form Entry
For data points with known schemas (e.g., fixture flow rates, SRI values, grid emission factors).

```json
{
  "entry_type": "structured",
  "field_id": "grid_emission_factor",
  "credit_code": "IPp3",
  "label": "Grid Emission Factor (kg CO2/kWh)",
  "description": "Annual grid emission factor for the electricity grid serving the project location.",
  "data_type": "number",
  "unit": "kgCO2e/kWh",
  "validation": {
    "min": 0.0,
    "max": 2.0,
    "precision": 4
  },
  "source_guidance": {
    "singapore": {
      "where_to_find": "EMA Singapore Energy Statistics, published annually by NEA/NCCS",
      "url": "https://www.ema.gov.sg/resources/singapore-energy-statistics",
      "typical_value": 0.4085,
      "last_known_year": 2023
    },
    "usa": {
      "where_to_find": "EPA eGRID — automatically fetched via API",
      "url": "https://www.epa.gov/egrid"
    }
  },
  "evidence_required": true,
  "evidence_types": ["pdf", "screenshot", "url"],
  "confidence_base": 0.75,
  "confidence_with_evidence": 0.90
}
```

### Mode 2: Document Upload with Extraction
For data embedded in PDFs, spreadsheets, or scanned documents (e.g., soil reports, flood maps, manufacturer cut sheets).

```json
{
  "entry_type": "document_upload",
  "field_id": "flood_zone_classification",
  "credit_code": "LTc1",
  "label": "Flood Zone Classification",
  "description": "Flood zone classification for the project site from the national flood authority.",
  "accepted_formats": ["pdf", "png", "jpg", "xlsx"],
  "extraction_strategy": "ai_assisted",
  "extraction_prompt": "Extract the flood zone classification for the marked project location from this flood map.",
  "manual_fields_after_upload": [
    {
      "field": "flood_zone",
      "label": "Flood Zone",
      "type": "enum",
      "options": ["No Flood Risk", "Low Risk", "Moderate Risk", "High Risk", "Flood-Prone Area"],
      "source_guidance": {
        "singapore": "Refer to PUB Flood Risk Map at https://www.pub.gov.sg/drainage/floodmanagement",
        "usa": "FEMA NFHL auto-populated"
      }
    },
    {
      "field": "distance_from_flood_zone_m",
      "label": "Distance from nearest flood-prone area (meters)",
      "type": "number",
      "unit": "meters",
      "validation": { "min": 0, "max": 50000 }
    }
  ],
  "confidence_base": 0.65,
  "confidence_with_verified_doc": 0.85
}
```

### Mode 3: Checklist with Evidence
For credits requiring qualitative compliance demonstration (e.g., sensitive land protection, habitat conservation).

```json
{
  "entry_type": "checklist",
  "field_id": "sensitive_land_assessment",
  "credit_code": "LTc1",
  "label": "Sensitive Land Protection Assessment",
  "checklist_items": [
    {
      "id": "not_on_prime_farmland",
      "question": "Is the project site on prime farmland?",
      "type": "boolean",
      "required": true,
      "source_guidance": {
        "singapore": "Singapore has no prime farmland classification. Mark N/A with a note explaining the Singapore land-use context.",
        "usa": "Check NRCS Soil Survey API (auto-populated)"
      },
      "evidence_types": ["url", "screenshot", "note"]
    },
    {
      "id": "not_in_floodplain",
      "question": "Is the project within the 100-year floodplain?",
      "type": "boolean",
      "required": true,
      "source_guidance": {
        "singapore": "Check PUB Flood Risk Map. Singapore uses a different flood classification system — map PUB 'flood-prone' designation to LEED 100-year floodplain equivalent.",
        "usa": "Check FEMA NFHL (auto-populated)"
      }
    },
    {
      "id": "not_on_habitat",
      "question": "Is the project within or adjacent to a critical habitat area?",
      "type": "boolean",
      "required": true,
      "source_guidance": {
        "singapore": "Check NParks Nature Areas map at https://www.nparks.gov.sg/biodiversity. Nature reserves include Bukit Timah, Central Catchment, Sungei Buloh, Labrador. Buffer zone is typically 200m.",
        "usa": "Check USFWS Critical Habitat API (auto-populated)"
      }
    },
    {
      "id": "not_on_wetland",
      "question": "Is the project on or adjacent to a wetland?",
      "type": "boolean",
      "required": true,
      "source_guidance": {
        "singapore": "Check NParks wetland areas. Key wetlands: Sungei Buloh, Kranji Marshes, Mandai Mangrove.",
        "usa": "Check National Wetlands Inventory (auto-populated)"
      }
    }
  ],
  "all_must_pass": true,
  "confidence_base": 0.70,
  "confidence_all_evidenced": 0.88
}
```

### Mode 4: Reference Table Lookup
For data points that come from published standards or tables (e.g., ventilation rates, lighting power densities).

```json
{
  "entry_type": "reference_lookup",
  "field_id": "ventilation_rate",
  "credit_code": "EQp1",
  "label": "Minimum Outdoor Air Ventilation Rate",
  "lookup_table": {
    "singapore": {
      "standard": "SS 554:2016 Code of Practice for Indoor Air Quality for Air-conditioned Buildings",
      "purchase_url": "https://www.singaporestandardseshop.sg/",
      "note": "Values differ from ASHRAE 62.1. Use SS 554 Table 1 for Singapore projects."
    },
    "usa": {
      "standard": "ASHRAE 62.1-2022",
      "note": "Auto-populated from embedded ASHRAE tables"
    }
  },
  "fields": [
    {
      "field": "outdoor_air_per_person",
      "label": "Outdoor Air Rate per Person (L/s/person)",
      "type": "number",
      "unit": "L/s/person",
      "validation": { "min": 0.5, "max": 30.0 }
    },
    {
      "field": "outdoor_air_per_area",
      "label": "Outdoor Air Rate per Floor Area (L/s/m²)",
      "type": "number",
      "unit": "L/s/m²",
      "validation": { "min": 0.0, "max": 5.0 }
    },
    {
      "field": "space_type",
      "label": "Space Type (from standard table)",
      "type": "enum",
      "options": ["Office", "Conference Room", "Retail", "Classroom", "Restaurant", "Lobby", "Corridor", "Other"]
    }
  ],
  "evidence_required": true,
  "evidence_types": ["pdf_page_screenshot", "standard_reference"],
  "confidence_base": 0.80,
  "confidence_with_evidence": 0.92
}
```

---

## Manual Data Input Workflow

```
User selects credit + region
        |
        v
Platform detects data availability for region
        |
        ├── API Available → Auto-fetch (confidence 0.90+)
        │
        ├── API Partial → Auto-fetch what's available + 
        │                  show manual entry form for gaps
        │
        └── No API → Show full manual data entry workflow
                |
                v
        Manual Entry Form rendered with:
        - Field descriptions and guidance
        - "Where to find this" links (region-specific)
        - Validation rules
        - Evidence upload slots
                |
                v
        User enters data + uploads evidence
                |
                v
        Validation Gate:
        - Range checks
        - Unit consistency
        - Completeness check
        - Cross-field logic (e.g., if flood zone = High Risk, distance must be 0)
                |
                ├── Validation Fails → Show errors, allow correction
                │
                └── Validation Passes → 
                        |
                        v
                Confidence Score calculated:
                - Base score by entry mode
                - Evidence quality bonus
                - Data recency bonus/penalty
                - Cross-reference bonus (if matches other project data)
                        |
                        v
                Data stored with:
                - source_type: "manual"
                - entered_by: user_id
                - entered_at: timestamp
                - evidence_refs: [document_ids]
                - confidence_score: 0.XX
                - validation_result: {checks_passed, checks_failed}
                        |
                        v
                Continue to calculation engine
                (same pipeline as API data)
```

---

## Confidence Scoring for Manual Data

| Data Provenance | Base Score | With Evidence | With Verified Evidence |
|---|---|---|---|
| API (primary source) | 0.92 | N/A | N/A |
| API (cached / stale) | 0.80 | N/A | N/A |
| Manual: Government publication | 0.80 | 0.90 | 0.92 |
| Manual: Industry standard | 0.75 | 0.88 | 0.90 |
| Manual: Manufacturer data | 0.70 | 0.82 | 0.88 |
| Manual: Consultant estimate | 0.60 | 0.72 | 0.80 |
| Manual: No evidence | 0.50 | N/A | N/A |

**Evidence verification** means a reviewer has confirmed the source document matches the entered value. This happens during HITL review.

---

## Data Entry Schema (Database)

```sql
CREATE TABLE manual_data_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id),
    credit_code VARCHAR(10) NOT NULL,
    field_id VARCHAR(100) NOT NULL,
    
    -- Data
    value_text TEXT,
    value_numeric NUMERIC,
    value_boolean BOOLEAN,
    value_json JSONB,
    unit VARCHAR(50),
    
    -- Provenance
    source_type VARCHAR(50) NOT NULL DEFAULT 'manual',
    source_description TEXT,
    source_url TEXT,
    source_publication_date DATE,
    
    -- Evidence
    evidence_document_ids UUID[],
    evidence_verified BOOLEAN DEFAULT FALSE,
    evidence_verified_by UUID REFERENCES users(id),
    evidence_verified_at TIMESTAMPTZ,
    
    -- Confidence
    confidence_score NUMERIC(3,2) NOT NULL DEFAULT 0.50,
    confidence_factors JSONB,
    
    -- Validation
    validation_passed BOOLEAN NOT NULL DEFAULT FALSE,
    validation_errors JSONB,
    
    -- Audit
    entered_by UUID NOT NULL REFERENCES users(id),
    entered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by UUID REFERENCES users(id),
    updated_at TIMESTAMPTZ,
    superseded_by UUID REFERENCES manual_data_entries(id),
    
    -- Region
    region VARCHAR(10) NOT NULL,
    
    UNIQUE(project_id, credit_code, field_id, entered_at)
);

CREATE INDEX idx_manual_data_project ON manual_data_entries(project_id);
CREATE INDEX idx_manual_data_credit ON manual_data_entries(credit_code);
CREATE INDEX idx_manual_data_region ON manual_data_entries(region);
```

---

## Regional Source Guidance Templates

Each manual entry field includes region-specific guidance. The platform maintains a `source_guidance` registry:

```json
{
  "field_id": "grid_emission_factor",
  "regions": {
    "US": {
      "auto": true,
      "source": "EPA eGRID API",
      "note": "Auto-fetched by subregion"
    },
    "SG": {
      "auto": false,
      "source": "EMA Singapore Energy Statistics",
      "url": "https://www.ema.gov.sg/resources/singapore-energy-statistics",
      "instructions": "1. Navigate to EMA Energy Statistics page\n2. Download the latest annual report\n3. Find 'Grid Emission Factor' in the Electricity section\n4. Enter value in kgCO2e/kWh\n5. Upload the PDF page as evidence",
      "typical_value": 0.4085,
      "last_known_year": 2023,
      "update_frequency": "annual"
    },
    "EU": {
      "auto": false,
      "source": "ENTSO-E Transparency Platform / National grid operator",
      "url": "https://transparency.entsoe.eu/",
      "instructions": "Use country-specific grid emission factor from national energy statistics or ENTSO-E"
    }
  }
}
```

---

## UI Components Required

### 1. Manual Data Entry Panel
- Appears when a credit's data source is unavailable for the project region
- Shows field-by-field entry with inline guidance
- Evidence upload dropzone per field
- Real-time validation feedback
- Progress indicator (X of Y fields completed)

### 2. Source Guidance Sidebar
- Region-specific instructions
- Direct links to government portals
- "Where to find this data" accordion
- Typical/expected values for sanity checking
- Screenshot examples of where to find data

### 3. Evidence Manager
- Upload documents (PDF, images, spreadsheets)
- Tag evidence to specific fields
- Preview uploaded documents
- Evidence reuse across credits (e.g., same flood map for LTc1 and SSc3)

### 4. Data Completeness Dashboard
- Per-credit: API-sourced vs. manual-sourced vs. missing
- Per-project: Overall data completeness percentage
- Actionable items: "3 fields need manual input for LTc1"
- Confidence heatmap by credit

### 5. Regional Data Availability Indicator
- On project creation, show data availability matrix for selected region
- Color-coded: Green (API), Yellow (partial/manual), Red (unavailable)
- Estimated manual effort hours per credit
- Suggested order of data collection

---

## Integration with Existing Architecture

### Workflow Node: `manual_data_collection`

```python
class ManualDataCollectionNode:
    """Workflow node that pauses execution to collect manual data."""
    
    node_type = "manual_data_collection"
    
    def execute(self, state: WorkflowState) -> WorkflowState:
        required_fields = self.get_required_manual_fields(
            credit_code=state.credit_code,
            region=state.project.region
        )
        
        filled_fields = self.get_existing_manual_data(
            project_id=state.project_id,
            credit_code=state.credit_code
        )
        
        missing = [f for f in required_fields if f.field_id not in filled_fields]
        
        if missing:
            return state.pause(
                status="waiting_for_manual_data",
                missing_fields=missing,
                guidance=self.generate_guidance(missing, state.project.region)
            )
        
        # All manual data collected — merge into normalized state
        return state.update(
            manual_data=filled_fields,
            data_sources=self.tag_sources(filled_fields)
        )
```

### Fallback Chain Update

The existing three-level fallback becomes four levels:

```
1. Primary API (real-time fetch)
2. Cached API data (within TTL)
3. Static dataset (pre-loaded batch data)
4. Manual data entry (with guided workflow)
5. HITL escalation (expert consultant sourcing)
```

Level 4 is the new addition. It is triggered automatically when the regional source router determines no API or static dataset exists for the required field in the project's region.
