# Skill: LTc1 - Sensitive Land Protection

## Metadata
- **Credit Code:** LTc1
- **Credit Name:** Sensitive Land Protection
- **Points:** 1
- **Automation Level:** 60%
- **Complexity:** High
- **Primary Data Source:** GIS APIs (US) / Manual (Other)
- **HITL Required:** Yes (Significant)

## Purpose
Cultivate community resilience by avoiding development of environmentally sensitive lands that provide critical ecosystem services.

## Inputs (Required)
| Field | Type | Source | Validation |
|-------|------|--------|------------|
| project_location | coordinates | User input | Valid lat/lon |
| site_boundary | polygon | Upload | Valid GeoJSON |

## Inputs (Optional)
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| is_previously_developed | boolean | null | If known, skip GIS analysis |
| manual_constraints | array | [] | User-provided constraint data |

## Workflow Steps (Durable)

### Step 1: validate_inputs
- **Type:** Validation
- **Automated:** Yes
- **Description:** Verify coordinates and boundary polygon

### Step 2: detect_region
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Determine country/region from coordinates
- **Output:** {country_code, region, data_availability}

### Step 3: check_previously_developed (Option 1)
- **Type:** User Input
- **Automated:** No
- **Description:** Ask user if site is previously developed
- **Condition:** If user confirms previously developed, skip to Step 10
- **Shortcut:** If is_previously_developed == true, credit achieved

### Step 4: query_fema_flood_zones (US only)
- **Type:** API Call
- **Automated:** Yes
- **API:** FEMA NFHL
- **Condition:** US location
- **Timeout:** 30 seconds
- **Output:** {flood_zones: array, sfha: boolean}
- **On Failure:** Flag for manual flood zone check

### Step 5: query_wetlands (US only)
- **Type:** API Call
- **Automated:** Yes
- **API:** National Wetlands Inventory (NWI)
- **Condition:** US location
- **Output:** {wetlands: array, buffer_violations: array}
- **On Failure:** Flag for manual wetland check

### Step 6: query_critical_habitat (US only)
- **Type:** API Call
- **Automated:** Yes
- **API:** USFWS Critical Habitat
- **Condition:** US location
- **Output:** {species: array, habitats: array}
- **On Failure:** Flag for manual habitat check

### Step 7: query_prime_farmland (US only)
- **Type:** API Call
- **Automated:** Yes
- **API:** USDA NRCS
- **Condition:** US location
- **Output:** {prime_farmland: boolean, acres: number}
- **On Failure:** Flag for manual farmland check

### Step 8: query_slope (US only)
- **Type:** API Call
- **Automated:** Yes
- **API:** USGS 3DEP
- **Condition:** US location
- **Output:** {slope_analysis: object, steep_slopes: array}
- **On Failure:** Flag for manual slope analysis

### Step 9: HITL_DATA_COLLECTION (Non-US or API failures)
- **Type:** Human Data Entry
- **Automated:** No
- **Condition:** Non-US location OR any API failure
- **Assignee:** GIS Analyst / Project Team
- **SLA:** 48 hours
- **Instructions:**
  - For non-US projects: Provide constraint data manually
  - For API failures: Verify/correct automated data
- **Form Fields:**
  - Previously developed? (Y/N)
  - Flood zone designation (if any)
  - Wetlands within 50ft? (Y/N)
  - Critical habitat present? (Y/N)
  - Prime farmland? (Y/N)
  - Steep slopes (40-60%)? (Y/N)
  - Water bodies within 100ft? (Y/N)

### Step 10: analyze_constraints
- **Type:** Calculation
- **Automated:** Yes
- **Description:** Analyze all constraint data
- **Rules:**
  - If previously developed → Credit achieved
  - If prime farmland → Credit NOT achievable
  - If floodplain → Must protect 100ft buffer
  - If wetlands → Must protect 50ft buffer
  - If critical habitat → Credit NOT achievable
  - If steep slopes → Must protect 40-60% of slopes
- **Output:** {achievable: boolean, constraints: array, requirements: array}

### Step 11: generate_constraint_map
- **Type:** Document Generation
- **Automated:** Partial
- **Description:** Generate GIS overlay map
- **US:** Automated from API data
- **Non-US:** Uses manual data, simplified map
- **Output:** PDF map with constraint overlays

### Step 12: HITL_VERIFICATION
- **Type:** Human Review
- **Automated:** No
- **Assignee:** LEED Consultant / GIS Analyst
- **SLA:** 24 hours
- **Instructions:**
  1. Verify constraint data is accurate
  2. Check buffer distances are correct
  3. Confirm credit achievability assessment
  4. Review constraint map for accuracy
- **Checklist:**
  - [ ] Constraint data verified
  - [ ] Buffer distances correct
  - [ ] Credit achievability confirmed
  - [ ] Map accuracy verified

### Step 13: generate_report
- **Type:** Document Generation
- **Automated:** Yes
- **Template:** lt_c1_land_protection.html
- **Output:** PDF report with analysis and map

## HITL Checkpoints
| Step | Reviewer | SLA | Instructions |
|------|----------|-----|--------------|
| Data collection (non-US) | GIS Analyst | 48h | Provide constraint data manually |
| Verification | LEED Consultant | 24h | Verify constraints and approve |

## API Dependencies
| API | Purpose | Regional Availability | Fallback | Rate Limit |
|-----|---------|----------------------|----------|------------|
| FEMA NFHL | Flood zones | US only | Manual flood map review | Unlimited |
| NWI | Wetlands | US only | Manual wetland survey | Unlimited |
| USFWS | Critical habitat | US only | Manual species survey | Unlimited |
| USDA NRCS | Prime farmland | US only | Manual soil survey | Unlimited |
| USGS 3DEP | Elevation/slope | US only | Manual topographic review | Unlimited |
| OpenStreetMap | Base mapping | Global | None | Unlimited |

## Regional Availability
| Region | Status | Notes |
|--------|--------|-------|
| United States | Full | All 5 APIs available |
| Canada | Limited | Use OpenStreetMap + manual data |
| European Union | Limited | Use OpenStreetMap + manual data |
| United Kingdom | Limited | Use OpenStreetMap + manual data |
| Australia | Limited | Use OpenStreetMap + manual data |
| Other | Minimal | Manual data entry required |

## Why 60% Automation?
This skill has limited automation because:
1. **GIS data is US-centric** - Only US has comprehensive free GIS APIs
2. **Constraint analysis requires expertise** - Buffer distances, protected species
3. **Site-specific interpretation** - Each site is unique
4. **Regulatory complexity** - Varies by jurisdiction

**For US projects:** 85% automation possible
**For non-US projects:** 30% automation (mostly document generation)

## Data Collection Strategy for Non-US Projects

### Option 1: Partner with Local GIS Providers
- Integrate with national GIS services (e.g., Ordnance Survey UK, IGN France)
- Requires API development for each country
- High development cost, ongoing maintenance

### Option 2: Manual Data Entry (Current Approach)
- Provide structured forms for project teams
- Include guidance for each constraint type
- AI validates completeness, human provides data

### Option 3: Hybrid with OpenStreetMap
- Use OSM for base mapping (global)
- Flag potential constraints from OSM tags
- Human verifies and supplements

## Output Documents
| Document | Format | Description |
|----------|--------|-------------|
| site_constraint_analysis | PDF | Constraint analysis with findings |
| constraint_map | PDF | GIS overlay map showing constraints |
| buffer_calculations | Excel | Buffer distance calculations |
| usgbc_submission_form | PDF | Pre-filled USGBC form |

## Testing
```bash
# US location (automated)
python skills/lt_c1_land_protect/agent.py --test --location "40.7128,-74.0060"

# Non-US location (manual data entry)
python skills/lt_c1_land_protect/agent.py --test --location "51.5074,-0.1278" --manual
```

## Example Usage
```python
from skills.lt_c1_land_protect import LandProtectionSkill

# US project (automated)
skill = LandProtectionSkill(
    project_id="123-us",
    inputs={
        "project_location": {"lat": 40.7128, "lon": -74.0060},
        "site_boundary": geojson_polygon
    }
)

# Non-US project (manual data entry required)
skill = LandProtectionSkill(
    project_id="123-uk",
    inputs={
        "project_location": {"lat": 51.5074, "lon": -0.1278},
        "site_boundary": geojson_polygon,
        "manual_constraints": {
            "previously_developed": True,
            "flood_zone": None,
            "wetlands": False,
            "critical_habitat": False,
            "prime_farmland": False,
            "steep_slopes": False
        }
    }
)

result = await skill.execute()
```

## Recommendations

### For Platform Development
1. **Phase 1:** Focus on US market (85% automation)
2. **Phase 2:** Add major markets (UK, CA, AU, EU) with manual data entry
3. **Phase 3:** Integrate national GIS APIs for priority countries

### For Non-US Projects
1. Clearly communicate automation limitations
2. Provide detailed guidance for manual data collection
3. Offer GIS analyst services as add-on
4. Consider partnerships with local consultants

## Known Limitations
1. **GIS APIs are US-only** - Non-US projects require significant manual input
2. **Constraint interpretation** - Requires local regulatory knowledge
3. **Buffer calculations** - May need adjustment for local regulations
4. **Protected species** - Database coverage varies by country
