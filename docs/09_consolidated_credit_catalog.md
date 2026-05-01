# Ecogen — Consolidated Credit Catalog (Tier 1 MVP)
## All 16 Tier-1 Skills with Normalized Automation Levels

**Source:** Kimi_Agent_LEED v5 Credit Automation/skills/ + normalization from EXECUTIVE_SUMMARY_REALISTIC.md  
**Normalization applied:** automation % corrected to realistic bounds; Arc submission removed from V1; V1 uses manual export only

---

## Tier 1A — Full Automation (90–95%)

### PRc2 — LEED AP Designation
| Field | Value |
|-------|-------|
| **Credit code** | PRc2 |
| **Points** | 1 |
| **Automation level** | 95% |
| **Complexity** | Low |
| **HITL checkpoints** | 1 (48h) |
| **Skill slug** | `pr_c2_leed_ap` |

**Inputs:** Team roster CSV/XLSX (name, role), LEED project type, credential number (optional)  
**Workflow:** Validate → GBCI credential lookup → compliance check → HITL (AP active engagement confirmation) → PDF report + DOCX credential confirmation  
**HITL:** LEED AP or PM confirms identified AP is actively engaged on project  
**APIs:** GBCI Credential Directory, USGBC Member Directory  
**Regional availability:** US ✓, CA ✓, UK ✓, EU ✓, AU ✓, Other ✓ (GBCI is global)  
**Output:** LEED AP Verification Report (PDF), Credential Confirmation (DOCX)

---

### SSc6 — Light Pollution Reduction
| Field | Value |
|-------|-------|
| **Credit code** | SSc6 |
| **Points** | 1 |
| **Automation level** | 95% |
| **Complexity** | Low |
| **HITL checkpoints** | 1 (24h) |
| **Skill slug** | `ss_c6_light_pollution` |

**Inputs:** Exterior lighting schedule (fixture types, lumens, CCT, BUG ratings), site boundary, lighting zone (LZ0–LZ4)  
**Workflow:** Validate → IES TM-15-11 BUG rating lookup → uplight/backlight compliance check → HITL (lighting designer review) → PDF narrative + compliance table  
**APIs:** IES BUG rating database, CRRC (if applicable)  
**Regional availability:** US ✓, CA ✓, UK ✓ (adapt to BS EN 12464), EU ✓, AU ✓  
**Output:** Light Pollution Reduction Narrative (PDF), Fixture Compliance Table (XLSX)

---

### EAp5 — Refrigerant Management (Prerequisite)
| Field | Value |
|-------|-------|
| **Credit code** | EAp5 |
| **Points** | Required |
| **Automation level** | 93% |
| **Complexity** | Low |
| **HITL checkpoints** | 1 (24h) |
| **Skill slug** | `ea_p5_refrigerant` |

**Inputs:** Refrigerant inventory (type, charge kg, equipment name), equipment count, building area  
**Workflow:** Validate → IPCC AR6 GWP lookup → leakage rate calculation → lifecycle climate performance (LCCP) → compliance check (no CFC, HCFC limits) → HITL → PDF narrative  
**APIs:** EPA refrigerant registry, IPCC AR6 GWP tables (static), AHRI equipment database  
**Regional availability:** US ✓, CA ✓, UK ✓, EU ✓ (F-Gas regs apply), AU ✓  
**Output:** Refrigerant Management Narrative (PDF), Refrigerant Inventory (XLSX)

---

### EAc7 — Enhanced Refrigerant Management
| Field | Value |
|-------|-------|
| **Credit code** | EAc7 |
| **Points** | 1 |
| **Automation level** | 92% |
| **Complexity** | Low |
| **HITL checkpoints** | 1 (24h) |
| **Skill slug** | `ea_c7_refrigerant` |

**Inputs:** Refrigerant inventory, equipment charge/age/leakage data, natural refrigerant alternatives considered  
**Workflow:** Validate → GWP lookup → LCCP calculation → enhanced thresholds check → natural refrigerant credit path → HITL → PDF narrative  
**APIs:** IPCC AR6 GWP tables, AHRI, EPA  
**Regional availability:** US ✓, CA ✓, UK ✓, EU ✓, AU ✓  
**Output:** Enhanced Refrigerant Assessment (PDF), Calculation Summary (XLSX)

---

## Tier 1B — AI-Assisted (80–90%)

### WEp2 — Minimum Water Efficiency (Prerequisite)
| Field | Value |
|-------|-------|
| **Credit code** | WEp2 |
| **Points** | Required |
| **Automation level** | 90% |
| **Complexity** | Medium |
| **HITL checkpoints** | 1 (48h) |
| **Skill slug** | `we_p2_water_min` |

**Inputs:** Fixture schedule CSV/XLSX (type, flow rate, flush volume), occupancy (FTE/transient/resident), building type, gender ratio  
**Workflow:** Validate → EPA WaterSense product lookup → ENERGY STAR appliance data → baseline calculation (LEED v5 fixture rates) → design calculation → % reduction → HITL (fixture schedule + occupancy verification) → PDF narrative + XLSX workbook  
**HITL:** Consultant verifies fixture schedule matches specs, occupancy counts approved  
**APIs:** EPA WaterSense Product Database, ENERGY STAR Product API (Socrata)  
**Regional:** US ✓, CA ✓ (adapt to Model National Energy Code), UK ✓ (WRAS fittings), EU ✓, AU ✓ (WELS scheme)  
**Output:** Water Use Calculations (PDF), Fixture Compliance Table (XLSX), Compliance Narrative (DOCX)

---

### WEc2 — Enhanced Water Efficiency
| Field | Value |
|-------|-------|
| **Credit code** | WEc2 |
| **Points** | Up to 4 |
| **Automation level** | 88% |
| **Complexity** | Medium |
| **HITL checkpoints** | 1 (48h) |
| **Skill slug** | `we_c2_water_enhanced` |

**Inputs:** Same as WEp2 + advanced fixture specs, process water data, cooling tower data (if applicable), site water harvesting  
**Workflow:** Same as WEp2 + advanced reductions path → points calculation → HITL → evidence pack  
**APIs:** EPA WaterSense, ENERGY STAR, NOAA (rainfall data for harvesting calc)  
**Regional:** US ✓, CA ✓, UK ✓, EU ✓, AU ✓  
**Output:** Enhanced Water Use Calculations (PDF), Points Determination (XLSX)

---

### SSc5 — Heat Island Reduction
| Field | Value |
|-------|-------|
| **Credit code** | SSc5 |
| **Points** | 2 |
| **Automation level** | 88% |
| **Complexity** | Medium |
| **HITL checkpoints** | 1 (48h) |
| **Skill slug** | `ss_c5_heat_island` |

**Inputs:** Roof area/slope/materials with SRI values, non-roof hardscape areas/materials, parking specs (total/covered spaces), tree canopy area, site area  
**Workflow:** Validate → CRRC SRI product lookup → Tree Equity Score fetch → roof SRI compliance calc → non-roof paving calc → parking calc → canopy calc → points aggregation → HITL (SRI value verification) → PDF + XLSX  
**HITL:** Sustainability consultant verifies SRI values against CRRC database and product datasheets  
**APIs:** CRRC Rated Products Directory, American Forests Tree Equity Score  
**Regional:** US ✓, CA ✓, UK ✓ (adapt SRI thresholds), EU ✓, AU ✓  
**Output:** Heat Island Reduction Calculations (PDF), SRI Compliance Table (XLSX), Material Summary (PDF)

---

### MRp2 — Embodied Carbon Assessment (Prerequisite)
| Field | Value |
|-------|-------|
| **Credit code** | MRp2 |
| **Points** | Required |
| **Automation level** | 85% |
| **Complexity** | Medium-High |
| **HITL checkpoints** | 2 (72h each) |
| **Skill slug** | `mr_p2_embodied` |

**Inputs:** Material takeoff CSV/XLSX (material_name, category, quantity, unit), building area, service life, LCA software (Tally/One Click LCA), structural/enclosure system confirmation  
**Workflow:** Validate → EPD parsing → EC3 + EPD Registry lookup → fuzzy material matching → HITL-1 (takeoff completeness review, 72h) → system classification → HITL-2 (EPD matching + GWP value review, 72h, LCA Specialist) → CLF baseline comparison → GWP intensity calc → PDF/XLSX/PDF  
**HITL-1:** Engineer/Consultant verifies material takeoff completeness  
**HITL-2:** LCA Specialist verifies EPD matches and GWP values  
**APIs:** EC3 Database, EPD Registry, One Click LCA, CLF Baselines  
**Regional:** US ✓, CA ✓, UK ✓ (EN 15804 EPDs), EU ✓, AU ✓ (limited EPD coverage → Manual required)  
**Output:** Embodied Carbon Assessment Report (PDF), Material-GWP Table (XLSX), EPD Summary (PDF), Baseline Comparison (PDF)

---

### IPp3 — Carbon Assessment (Prerequisite)
| Field | Value |
|-------|-------|
| **Credit code** | IPp3 |
| **Points** | Required |
| **Automation level** | 85% |
| **Complexity** | High |
| **HITL checkpoints** | 1 (72h) |
| **Skill slug** | `ip_p3_carbon` |

**Inputs:** Annual energy use (kWh by fuel type), refrigerant inventory, material quantities, project location, service life  
**Depends on:** EAp1 (energy model), EAp5 (refrigerant), MRp2 (materials)  
**Workflow:** Validate → eGRID grid factor lookup → EC3 embodied carbon factors → operational carbon calc → refrigerant carbon calc → embodied carbon calc → 25-year projection → HITL (energy model + refrigerant + materials + grid factor verification) → PDF/XLSX  
**HITL:** LEED AP BD+C verifies: energy model inputs, refrigerant types/charges, material quantities vs BOQ, eGRID subregion selection  
**APIs:** EPA eGRID, EC3 Database, One Click LCA, IPCC AR6 GWP tables  
**Regional:** US ✓, CA ✓ (provincial grid), UK ✓ (DESNZ emission factors), EU ✓ (national grid factors), AU ✓ (AEMO)  
**Output:** 25-Year Carbon Projection Report (PDF), Decarbonization Pathway (PDF), Calculation Spreadsheet (XLSX)

---

### SSc3 — Rainwater Management
| Field | Value |
|-------|-------|
| **Credit code** | SSc3 |
| **Points** | Up to 3 |
| **Automation level** | 82% |
| **Complexity** | Medium |
| **HITL checkpoints** | 1 (48h) |
| **Skill slug** | `ss_c3_rainwater` |

**Inputs:** Site area, impervious cover (pre/post), green infrastructure specs (rain gardens, green roofs, cisterns), project location  
**Workflow:** Validate → NOAA Atlas 14 precipitation data → pre/post runoff calculation (curve number method) → green infrastructure credit → percentile threshold check → points determination → HITL → PDF + XLSX  
**HITL:** Civil/landscape engineer verifies runoff calculations and GI specs  
**APIs:** NOAA Atlas 14, USGS StreamStats, NRCS curve number tables  
**Regional:** US ✓, CA ✓ (adapt IDF curves), UK ✓ (Flood Estimation Handbook), EU — Limited, AU — Limited  
**Output:** Rainwater Management Calculations (PDF), Runoff Reduction Table (XLSX)

---

### EAp1 — Operational Energy Performance (Prerequisite)
| Field | Value |
|-------|-------|
| **Credit code** | EAp1 |
| **Points** | Required |
| **Automation level** | 80% |
| **Complexity** | Medium-High |
| **HITL checkpoints** | 1 (48h) |
| **Skill slug** | `ea_p1_op_carbon` |

**Inputs:** Energy model output files (EnergyPlus IDF/OSM or eQuest/DOE2), building type, climate zone, ASHRAE 90.1-2022 baseline  
**Workflow:** Validate → parse energy model → extract EUI → ASHRAE baseline lookup → compliance check → HITL (energy modeler verification) → PDF narrative  
**HITL:** Energy Modeler verifies model inputs, baseline assumptions, climate zone  
**APIs:** EnergyPlus/Eppy parser, ASHRAE 90.1-2022 reference tables, DOE EnergyPlus Weather files  
**Regional:** US ✓, CA ✓ (NECB baseline), UK ✓ (Part L), EU — Limited (adapt to EPBD), AU — Limited  
**Output:** Energy Performance Prerequisite Compliance (PDF), EUI Comparison Table (XLSX)

---

## Tier 1C — Expert-Assisted (60–80%)

### LTc1 — Sensitive Land Protection
| Field | Value |
|-------|-------|
| **Credit code** | LTc1 |
| **Points** | 1 |
| **Automation level** | 80% |
| **Complexity** | Medium-High |
| **HITL checkpoints** | 1 (48h, GIS Analyst) |
| **Skill slug** | `lt_c1_land_protect` |

**Inputs:** Site boundary GeoJSON, site area (acres), project address, existing conditions (greenfield/brownfield)  
**Workflow:** Validate → FEMA floodplain lookup → NWI wetland query → USFWS critical habitat → NRCS prime farmland → USGS slope analysis → overlap consolidation → HITL (GIS analyst verifies boundary accuracy and overlap interpretation) → PDF + map PDF  
**HITL:** GIS Analyst — verifies boundary alignment, sensitive land overlay interpretation, edge cases  
**APIs:** FEMA NFHL REST, NWI WMS/WFS, USFWS ECOS, USDA NRCS SDA, USGS 3DEP/TNM, USGS PAD-US  
**Regional:** US ✓, CA — Limited (NWI not applicable → provincial wetland data), UK — Limited (EA Flood Map, Natural England), EU — Limited, AU — Limited  
**Output:** Sensitive Land Analysis Report (PDF), GIS Overlap Map (PDF), Compliance Declaration (DOCX)

---

### LTc3 — Compact Development
| Field | Value |
|-------|-------|
| **Credit code** | LTc3 |
| **Points** | Up to 5 |
| **Automation level** | 75% |
| **Complexity** | High |
| **HITL checkpoints** | 2 (48h each) |
| **Skill slug** | `lt_c3_compact` |

**Inputs:** Project address, building program (GFA, uses), parcel area, local zoning data  
**Workflow:** Validate → Census density lookup → Walk Score / GTFS transit data → residential/non-residential density calc → diverse uses inventory → HITL-1 (data verification) → points calc → HITL-2 (final review) → PDF  
**APIs:** US Census ACS, Walk Score, GTFS feeds, OpenStreetMap, local zoning APIs  
**Regional:** US ✓, CA ✓, UK ✓, EU — Limited (GTFS coverage varies), AU — Limited  
**Output:** Compact Development Analysis (PDF), Density Calculation (XLSX), Transit Access Summary (PDF)

---

### MRc2 — Embodied Carbon Reduction
| Field | Value |
|-------|-------|
| **Credit code** | MRc2 |
| **Points** | Up to 3 |
| **Automation level** | 70% |
| **Complexity** | High |
| **HITL checkpoints** | 2 (72h each) |
| **Skill slug** | `mr_c2_embodied_reduce` |

**Inputs:** Same as MRp2 + product-specific EPDs, LCA report (if available), baseline building definition  
**Workflow:** Same as MRp2 + reduction pathway analysis → product alternative comparison → optimization recommendations → HITL-1 (material scope) → HITL-2 (LCA specialist final) → evidence pack  
**APIs:** EC3, EPD Registry, One Click LCA, Tally, CLF Baselines  
**Regional:** US ✓, CA ✓, UK ✓, EU ✓, AU — Limited (EPD gaps → Manual)  
**Output:** Embodied Carbon Reduction Report (PDF), Reduction Pathway (XLSX), EPD Comparison (PDF)

---

### EAc3 — Enhanced Energy Efficiency
| Field | Value |
|-------|-------|
| **Credit code** | EAc3 |
| **Points** | Up to 10 (NC) / 7 (C&S) |
| **Automation level** | 70% |
| **Complexity** | High |
| **HITL checkpoints** | 2 (48h each) |
| **Skill slug** | `ea_c3_energy_enhanced` |

**Inputs:** Energy model files (IDF/OSM/eQuest/TRACE/IES-VE), building type, climate zone, modeler-claimed improvement %  
**Workflow:** Validate → parse model outputs → compute EUI improvement % → ASHRAE 90.1 baseline → points determination → HITL-1 (Energy Modeler verifies parsed data, 48h) → cost savings calculation → narrative generation → HITL-2 (LEED Consultant reviews narrative and points, 48h)  
**HITL-1:** Energy Modeler — verifies parsed energy data, confirms baseline assumptions  
**HITL-2:** LEED Consultant — reviews narrative, points claim, supporting data  
**APIs:** EnergyPlus/Eppy, ASHRAE 90.1-2022 reference, WeasyPrint/ReportLab  
**Regional:** US ✓, CA ✓ (NECB), UK ✓ (Part L), EU — Limited, AU — Limited  
**Output:** Enhanced Energy Efficiency Narrative (PDF), Points Calculation (XLSX), Energy Model Summary (PDF), Submission Package (ZIP)

---

### EAp2 — Minimum Energy Performance (Prerequisite)
| Field | Value |
|-------|-------|
| **Credit code** | EAp2 |
| **Points** | Required |
| **Automation level** | 65% |
| **Complexity** | High |
| **HITL checkpoints** | 2 (48h each) |
| **Skill slug** | `ea_p2_energy_min` |

**Inputs:** Same as EAp1 + detailed system descriptions, HVAC specs, envelope specs  
**Workflow:** Validate → energy model parse → ASHRAE 90.1 compliance path determination → mandatory requirements check → HITL-1 → prescriptive/performance check → HITL-2 → compliance report  
**Note:** Most complex prerequisite — requires detailed energy model review by qualified modeler. Cannot shortcut.  
**APIs:** EnergyPlus, ASHRAE 90.1-2022, DOE weather files  
**Regional:** US ✓, CA ✓, UK ✓, EU — Limited, AU — Limited  
**Output:** Energy Compliance Prerequisite Report (PDF), Mandatory Requirements Checklist (XLSX)

---

## Summary Table

| Credit | Slug | Tier | Auto% | HITL | Points |
|--------|------|------|-------|------|--------|
| PRc2 | pr_c2_leed_ap | 1A | 95% | 1 × 48h | 1 |
| SSc6 | ss_c6_light_pollution | 1A | 95% | 1 × 24h | 1 |
| EAp5 | ea_p5_refrigerant | 1A | 93% | 1 × 24h | Req |
| EAc7 | ea_c7_refrigerant | 1A | 92% | 1 × 24h | 1 |
| WEp2 | we_p2_water_min | 1B | 90% | 1 × 48h | Req |
| WEc2 | we_c2_water_enhanced | 1B | 88% | 1 × 48h | ≤4 |
| SSc5 | ss_c5_heat_island | 1B | 88% | 1 × 48h | 2 |
| MRp2 | mr_p2_embodied | 1B | 85% | 2 × 72h | Req |
| IPp3 | ip_p3_carbon | 1B | 85% | 1 × 72h | Req |
| SSc3 | ss_c3_rainwater | 1B | 82% | 1 × 48h | ≤3 |
| EAp1 | ea_p1_op_carbon | 1B | 80% | 1 × 48h | Req |
| LTc1 | lt_c1_land_protect | 1C | 80% | 1 × 48h GIS | 1 |
| LTc3 | lt_c3_compact | 1C | 75% | 2 × 48h | ≤5 |
| MRc2 | mr_c2_embodied_reduce | 1C | 70% | 2 × 72h | ≤3 |
| EAc3 | ea_c3_energy_enhanced | 1C | 70% | 2 × 48h | ≤10 |
| EAp2 | ea_p2_energy_min | 1C | 65% | 2 × 48h | Req |

**Typical project coverage:** A commercial NC project pursuing certification will likely use 10–12 of these skills, covering 35–45 LEED points and saving 60–100 consultant hours.
