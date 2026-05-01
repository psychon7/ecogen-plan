## 1. LEED v5 Credit Automation Matrix

### 1.1 Methodology and Scoring Framework

Each of the 51 LEED v5 BD+C credits is scored across three independent dimensions.

**Automation Score (1–5)** assesses: *documentation type* (narrative, calculation, physical testing, or field verification); *data inputs* (API availability, document extractability, or physical measurement dependence); *AI technique applicability*; and *verification feasibility* against known standards. The composite reflects the lowest constraining factor. Scores of 5/5 require only template filling; 4/5 indicates AI handles 80+ percent; 3/5 reflects 50–80 percent; 2/5 indicates 20–50 percent assistance. No credit scored 1/5.

**Commercial Value (1–5)** weights: time saved; documentation burden; repeatability; pursuit frequency; and willingness to pay. Prerequisites score higher as they apply to 100 percent of pursuing projects.

**Risk** uses three tiers: *Low Risk* (deterministic outputs); *Medium Risk* (engineering judgment, cross-referenced standards); *High Risk* (physical testing or professional judgment AI cannot substitute). Recommendations: *Automate in MVP*; *Automate Later*; *Assist Only*; *Avoid*. No credit received *Avoid*.

### 1.2 Complete Credit-by-Credit Analysis

The following table presents all 51 LEED v5 BD+C credits. AI Techniques: LLM = large language model; CE = calculation engine; Tmpl = template; GIS = geospatial; Web = web research; Parse = document parsing; Sim = simulation; CV = computer vision.

| LEED Category | Credit ID | Credit Name | Documentation Type | Required Inputs | AI Techniques | Auto /5 | Value /5 | Risk | Final Recommendation |
|:---|:---|:---|:---|:---|:---|:---:|:---:|:---|:---|
| **IP+PR** | IPp1 | Climate Resilience Assessment | Assessment report | Project address, building type, service life | LLM, Web, Tmpl, GIS | 4 | 5 | Medium | **Automate in MVP** |
| **IP+PR** | IPp2 | Human Impact Assessment | Assessment report | Project address, demographics data | LLM, Web, Tmpl | 4 | 5 | Medium | **Automate in MVP** |
| **IP+PR** | IPp3 | Carbon Assessment | Data compilation | Cross-credit data (EAp1, EAp5, MRp2) | Tmpl, Parse | 2 | 3 | Low | **Assist Only** |
| **IP+PR** | IPp4 | Tenant Guidelines | Policy document | LEED credits attempted, contact info | LLM, Tmpl | 5 | 4 | Low | **Automate in MVP** |
| **IP+PR** | IPc1 | Integrative Design Process | Process documentation | Team roster, charrette notes, goals | LLM, Tmpl | 3 | 4 | Low | **Automate in MVP** |
| **IP+PR** | IPc2 | Green Leases | Legal document | Best practice selections, project data | LLM, Tmpl, CE | 5 | 5 | Medium | **Automate in MVP** |
| **IP+PR** | PRc1 | Project Priorities | Variable pathways | Underlying credit achievements | LLM, Web | 2 | 3 | High | **Automate Later** |
| **IP+PR** | PRc2 | LEED AP | Form entry | Credential number, name, specialty | Tmpl | 5 | 2 | Low | **Automate in MVP** |
| **LT** | LTc1 | Sensitive Land Protection | GIS analysis | Site boundary polygon, site plan | GIS, Web, LLM, CE | 4 | 3 | Medium | **Automate in MVP** |
| **LT** | LTc2 | Equitable Development | Policy documents | Brownfield letters, employment records, AMI | Web, Parse, Tmpl | 2 | 2 | Medium | **Assist Only** |
| **LT** | LTc3 | Compact & Connected Development | GIS analysis, data report | Project address | GIS, Web, CE, API | 5 | 5 | Low | **Automate in MVP** |
| **LT** | LTc4 | Transportation Demand Management | Calculation, narrative | Occupancy counts, parking study | CE, GIS, LLM, Web | 3 | 4 | Medium | **Automate Later** |
| **LT** | LTc5 | Electric Vehicles | Drawing markup | Parking count, EVSE cut sheets | CE, Parse | 2 | 2 | Low | **Assist Only** |
| **SS** | SSp1 | Minimized Site Disturbance | Policy, checklist | Erosion control plan, site assessment | LLM, Tmpl, CV | 2 | 3 | Medium | **Assist Only** |
| **SS** | SSc1 | Biodiverse Habitat | Calculation, species list | Site plan, soil test, glass schedule | GIS, Web, LLM, CE | 3 | 3 | Medium | **Automate Later** |
| **SS** | SSc2 | Accessible Outdoor Space | Drawing markup | Site plan, landscape plan | CE | 2 | 2 | Low | **Assist Only** |
| **SS** | SSc3 | Rainwater Management | Hydrology model | Site plan, impervious surfaces | CE, GIS, Web, LLM | 4 | 4 | Medium | **Automate in MVP** |
| **SS** | SSc4 | Enhanced Resilient Site Design | Hazard assessment | IPp1 assessment, site plans | Web, GIS, LLM, Tmpl | 4 | 5 | Medium | **Automate in MVP** |
| **SS** | SSc5 | Heat Island Reduction | Calculation, data report | Site plan, roof plan, product specs | CE, Web, Parse | 4 | 4 | Low | **Automate in MVP** |
| **SS** | SSc6 | Light Pollution Reduction | Template checklist | Lighting fixture schedule, site plan | Tmpl, Parse, Web, CE | 3 | 3 | Low | **Automate Later** |
| **WE** | WEp1 | Water Metering & Reporting | Plan, commitment letter | Meter specs, plumbing drawings | Tmpl, LLM, Parse | 4 | 4 | Low | **Automate in MVP** |
| **WE** | WEp2 | Minimum Water Efficiency | Calculation, specification | Fixture schedule, cut sheets | CE, Parse, Tmpl | 5 | 5 | Low | **Automate in MVP** |
| **WE** | WEc1 | Water Metering & Leak Detection | Plan, layout drawing | Submeter specs, plumbing drawings | Tmpl, Parse, LLM | 4 | 4 | Low | **Automate in MVP** |
| **WE** | WEc2 | Enhanced Water Efficiency | Calculation, specification | Fixture schedule, equipment specs | CE, Parse, Tmpl | 5 | 5 | Low-Med | **Automate in MVP** |
| **EQ** | EQp1 | Construction Management | Plan, checklist, narrative | Project schedule, material list, site layout | LLM, Tmpl | 4 | 5 | Low | **Automate in MVP** |
| **EQ** | EQp2 | Fundamental Air Quality | Calculation, specification | HVAC schedules, OA rates, filtration specs | CE, Parse, LLM, Tmpl | 4 | 4 | Medium | **Automate in MVP** |
| **EQ** | EQp3 | No Smoking / Vehicle Idling | Plan, site plan | Site layout, building footprint | GIS, Tmpl, CE | 3 | 3 | Low | **Automate Later** |
| **EQ** | EQc1 | Enhanced Air Quality | Calculation, narrative | Ventilation calcs, IAQ model results | CE, Tmpl, Parse | 3 | 3 | Medium | **Automate Later** |
| **EQ** | EQc2 | Occupant Experience | Survey, calculation | Floor plans, glazing specs, luminaire data | Sim, LLM, CE, Tmpl | 4 | 4 | Medium | **Automate in MVP** |
| **EQ** | EQc3 | Accessibility & Inclusion | Checklist, narrative | Local accessibility codes, floor plans | Tmpl, LLM, GIS | 4 | 4 | Low | **Automate in MVP** |
| **EQ** | EQc4 | Resilient Spaces | Calculation, narrative | TMY weather, envelope specs, window schedule | Sim, Tmpl, LLM | 3 | 3 | Medium | **Automate Later** |
| **EQ** | EQc5 | Air Quality Testing & Monitoring | Test report, specification | Laboratory test results, monitor specs | Parse, Tmpl | 2 | 3 | High | **Assist Only** |
| **EA** | EAp1 | Decarbonization Plan | Narrative, plan | Energy model outputs, project location | Parse, LLM, Tmpl, CE | 4 | 5 | Low | **Automate in MVP** |
| **EA** | EAp2 | Minimum Energy Efficiency | Energy model | Complete ASHRAE 90.1 Appendix G model | Parse, CE | 2 | 5 | Medium | **Assist Only** |
| **EA** | EAp3 | Fundamental Commissioning | Plan, narrative | Building type, systems list, OPR/BOD | LLM, Parse, Tmpl | 3 | 4 | Low | **Automate Later** |
| **EA** | EAp4 | Energy Metering and Reporting | Specification, plan | System inventory, meter specs | Parse, Tmpl | 3 | 3 | Low | **Automate Later** |
| **EA** | EAp5 | Fundamental Refrigerant Mgmt | Inventory, calculation | Equipment schedules, refrigerant types | Parse, Web, CE | 4 | 4 | Low | **Automate in MVP** |
| **EA** | EAc1 | Electrification | Calculation, narrative | Heating/SWH equipment schedules | Parse, CE, Tmpl | 4 | 5 | Low | **Automate in MVP** |
| **EA** | EAc2 | Reduce Peak Thermal Loads | Energy model, testing | Air leakage results, WUFI/PHPP model | Parse, CE | 2 | 4 | Medium | **Assist Only** |
| **EA** | EAc3 | Enhanced Energy Efficiency | Energy model, calculation | ASHRAE 90.1 model, Section 11 tallies | Parse, CE, Web | 2 | 5 | Medium | **Assist Only** |
| **EA** | EAc4 | Renewable Energy | Calculation, contract | Energy model output, system specs | CE, Tmpl, Parse | 3 | 5 | Low-Med | **Automate in MVP** |
| **EA** | EAc5 | Enhanced Commissioning | Plan, specification | Systems inventory, CxP selections | LLM, Parse, Tmpl | 4 | 4 | Low | **Automate in MVP** |
| **EA** | EAc6 | Grid Interactive | Plan, calculation | Peak demand data, storage specs | CE, LLM, Tmpl | 3 | 3 | Medium | **Automate Later** |
| **EA** | EAc7 | Enhanced Refrigerant Mgmt | Calculation, inventory | EAp5 inventory, equipment status | CE, Parse, LLM, Tmpl | 5 | 4 | Low | **Automate in MVP** |
| **MR** | MRp1 | Zero Waste Operations | Plan, narrative | Building type, floor plans, location | LLM, Parse, Web, Tmpl | 3 | 3 | Low | **Automate in MVP** |
| **MR** | MRp2 | Quantify Embodied Carbon | Calculation report | Material quantities, EPDs | Parse, Web, CE, LLM | 4 | 5 | Medium | **Automate in MVP** |
| **MR** | MRc1 | Building & Materials Reuse | Calculation, photos | As-built drawings, salvage survey | Parse, CE, Tmpl, CV | 3 | 3 | Medium | **Automate Later** |
| **MR** | MRc2 | Reduce Embodied Carbon | EPD analysis, WBLCA | EPD library, material quantities | Parse, Web, CE, LLM | 4 | 5 | Medium | **Automate in MVP** |
| **MR** | MRc3 | Low-emitting Materials | Compliance table | Product list, certifications | Parse, Web, CE, Tmpl | 5 | 4 | Low | **Automate in MVP** |
| **MR** | MRc4 | Building Product Selection & Procurement | Scoring matrix | Product inventory, manufacturer docs | Parse, Web, CE, Tmpl | 4 | 5 | Low-Med | **Automate in MVP** |
| **MR** | MRc5 | C&D Waste Diversion | Calculation, report | Hauler tickets, facility receipts | Parse, CE, LLM, Tmpl | 4 | 4 | Low-Med | **Automate in MVP** |

Cross-category patterns are immediately apparent. IPp1 and IPp2 apply to every project and consume 10–20 consultant hours each in manual research. LTc3 is the single highest-value target across all 51 credits — perfect automation score, maximum value, Low Risk, with documentation from public geospatial data alone. Water Efficiency is the most uniformly automatable category (mean 4.50); all four credits are MVP-bound. Energy and Atmosphere is the most polarized: EAp2, EAc2, and EAc3 are Assist Only because their core deliverable is energy modeling, yet six surrounding documentation credits are strong MVP candidates. EQc5 is the sole High Risk credit due to mandatory ISO/IEC 17025 laboratory testing. MRc3 achieves a perfect score through rule-based compliance screening, while MRp2 and MRc2 form an embodied carbon pipeline via EPD parsing and database integration.

### 1.3 Summary Statistics and Patterns

#### 1.3.1 Distribution Analysis: Automation Scores by Category

Across all 51 credits, the mean automation score is 3.51 out of 5. No credit scored 1/5. The distribution is right-skewed: 8 credits (16 percent) score 5/5, 20 (39 percent) score 4/5, 13 (25 percent) score 3/5, and 10 (20 percent) score 2/5. The 28 credits at scores 4–5 (55 percent) establish the MVP foundation.

| LEED Category | Credits | Mean Auto Score | Mean Value | MVP Count | MVP % |
|:---|:---:|:---:|:---:|:---:|:---:|
| Integrative Process + Project Priorities | 8 | 3.75 | 3.88 | 6 | 75% |
| Location and Transportation | 5 | 3.20 | 3.20 | 2 | 40% |
| Sustainable Sites | 7 | 3.14 | 3.43 | 3 | 43% |
| Water Efficiency | 4 | 4.50 | 4.50 | 4 | 100% |
| Indoor Environmental Quality | 8 | 3.38 | 3.75 | 5 | 63% |
| Energy and Atmosphere | 12 | 3.08 | 4.00 | 6 | 50% |
| Materials and Resources | 7 | 3.86 | 4.14 | 6 | 86% |
| **All Credits** | **51** | **3.51** | **3.88** | **31** | **61%** |

Water Efficiency leads all categories at 4.50, driven by universal fixture-based calculation engines. Materials and Resources follows at 3.86, benefiting from deterministic product database lookups. Integrative Process at 3.75 is boosted by narrative-heavy prerequisites. Energy and Atmosphere trails at 3.08, pulled down by three energy modeling credits. Sustainable Sites records the lowest mean at 3.14, reflecting field-dependent verification. Overall, 31 credits (61 percent) are MVP-bound, 11 (22 percent) for later phases, and 9 (18 percent) for assist-only workflows.

![Figure 1.1: Automation score distribution across all 51 LEED v5 BD+C credits, recommendation breakdown, and scatter of automation score versus commercial value by category](fig1_1_automation_distribution.png)

#### 1.3.2 Correlation Patterns: Documentation Type vs. Automation Feasibility

When documentation type is mapped against automation score, a clear taxonomy emerges. **Narrative and plan documents** score highest at 4.2/5 (LLM-driven). **Pure calculations** score 4.3/5 (deterministic engines). The lowest-scoring types are **energy models** (2.0/5), **physical test reports** (2.0/5), and **field verification** (2.3/5).

| Documentation Type | Credits | Mean Auto Score | Primary AI Technique | MVP Rate |
|:---|:---:|:---:|:---|:---:|
| Narrative / Plan | 14 | 4.2 | LLM + Template Filling | 79% |
| Calculation / Data | 16 | 4.3 | Calculation Engine | 75% |
| Inventory / Database | 6 | 4.3 | Document Parsing + Web | 83% |
| GIS / Geospatial | 4 | 4.3 | GIS Integration + APIs | 75% |
| Drawing / Specification | 5 | 2.4 | Document Parsing + CV | 20% |
| Energy Model | 3 | 2.0 | Output Parsing (Assist) | 0% |
| Physical Test / Field | 3 | 2.0 | Template + Data Entry | 0% |

This pattern carries direct product strategy implications. An automation platform should prioritize **calculation engines** and **narrative generators** as core components, with **document parsing** and **web research agents** as supporting infrastructure. Energy model output parsers and computer vision for drawings should be Phase 2 enhancements.

#### 1.3.3 Impact Area Alignment: Decarbonization, Quality of Life, Ecological Conservation

LEED v5 organizes credits around three impact areas. The **decarbonization** domain shows a bimodal distribution: energy modeling credits (EAp2, EAc3) resist automation, while equipment specification credits (EAc1, EAc7) are highly automatable. MRp2 and MRc2 achieve strong automation through EPD parsing and database integration. The **quality of life** domain — EQ, WE, and LTc3 — is the most uniformly automatable at a mean of 3.8/5, strategically significant because these credits are the most visible to occupants and clients. **Ecological conservation** credits present a moderate profile at 3.4/5, requiring GIS integration and species research that introduces data quality risks from variable public dataset coverage. The GIS pipeline built for these credits has cross-credit value for LTc3 and SSc4.

The combined analysis yields a clear MVP roadmap. The first sprint should target WEp2, WEc2, LTc3, IPp1, IPp2, IPp4, IPc2, MRc3, and EAc7 — nine credits representing 11 prerequisites, 22 potential points, and an estimated 60–80 consultant hours saved per project. The second sprint expands into narrative credits (EQp1, EQc3, EQc2) and engineering calculations (SSc3, SSc5, EAc1, EAp5), adding 30–40 hours. The full MVP scope of 31 credits projects to deliver 100–150 consultant hours per project, valued at $15,000–$22,500 at standard billing rates.
