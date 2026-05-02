# 6. Platform Architecture

The preceding credit-by-credit analyses identified a recurring pattern: every LEED automation workflow—whether for water efficiency calculations, embodied carbon quantification, or climate resilience assessments—relies on the same underlying capabilities (document ingestion, web research, calculation engines, narrative generation, and quality review). A platform that treats these as shared infrastructure rather than building isolated credit modules can deliver compounding returns: each new credit automated extends the system's reach at marginal incremental cost. This chapter presents the unified platform architecture designed to support the automation scope identified across all 43 credits analyzed—encompassing the Integrative Process (IP), Location & Transportation (LT), Sustainable Sites (SS), Water Efficiency (WE), Energy & Atmosphere (EA), Materials & Resources (MR), and Indoor Environmental Quality (EQ) categories.

## 6.1 Core System Modules

The platform is organized into four core modules that form the data pipeline from project onboarding through submission package generation. Each module is designed as a set of composable services that multiple AI agents can invoke.

### 6.1.1 Project Intake Module

The project intake module establishes the foundational data context that drives all downstream automation. The consultant inputs building type (new construction, core and shell, school, healthcare, or data center), project address with geocoding, gross floor area, occupancy counts (full-time equivalent and transient), intended LEED certification level, and project phase (predesign, design development, construction, or operations). The module performs geocoding to latitude/longitude coordinates, resolves the ASHRAE climate zone (0A through 8) from the project location, identifies the EPA eGRID subregion for carbon emission factors, and auto-detects applicable rating system variations. This single intake action triggers eligibility filtering across all 43 credits: for example, LTc3 Compact & Connected Development requires residential density calculations that are only relevant for certain building types, while EAc1 Electrification COP calculations apply climate zone exclusions for zones 0–2. The module stores all project metadata in the unified data model (Section 6.3), making it available to every agent in the ecosystem.

### 6.1.2 LEED Credit Selector

The credit selector module implements a recommendation engine that scores every credit against the project profile using three dimensions: automation feasibility (the 1–5 scoring system applied throughout the credit analyses), commercial value (point potential multiplied by project applicability), and automation confidence (derived from data completeness). A project with full fixture schedules and equipment cut sheets uploaded would show high confidence for WEp2/WEc2 water calculations, while a project without energy model outputs would flag EAp2 and EAc3 as requiring manual input before automation can proceed. The selector displays credits in a tiered view: Tier 1 (green) indicates full automation readiness with all required inputs present; Tier 2 (amber) indicates partial automation with data gaps flagged; Tier 3 (red) indicates credits that require professional engineering input or physical testing beyond AI capability. For each credit, the module displays the estimated time savings—derived from the per-credit benchmarks established in the research phase, ranging from 65–92% depending on category—and the automation score and point value.[^1^]

### 6.1.3 Document Upload and Parsing Engine

The document parsing engine handles multi-format ingestion: PDF drawings and specifications, Excel/CSV schedules, DWG/DXF CAD files, IFC building models, image files (PNG/JPG of site photos, product cut sheets), and text documents. The engine applies modality-specific processing pipelines. For tabular data (fixture schedules, equipment schedules, material takeoffs), the system uses layout-aware table extraction to recover structured rows with headers, then normalizes column names against a canonical schema—mapping variations like "GPF," "Flush Rate," or "Flow (gpf)" to a unified field. For product cut sheets and EPD PDFs, the parser performs field extraction targeting certification numbers, GWP values, flow rates, COP ratings, and refrigerant types. For CAD and BIM files, the geometry processor extracts floor areas, room boundaries, glazing locations, and spatial relationships needed for daylight proximity calculations and view area analysis. For hauler weight tickets and waste receipts in MRc5, the parser uses OCR with template matching to extract tare weight, gross weight, material type, and destination facility.[^2^] All extracted data receives a confidence score (0.0–1.0) based on extraction certainty; values below 0.85 trigger human review flags.

### 6.1.4 RAG Knowledge Base

The Retrieval-Augmented Generation (RAG) knowledge base indexes three content domains: the LEED v5 reference guide and all associated addenda (primary source), applicable technical standards (ASHRAE 62.1-2022, ASHRAE 90.1-2022, ASHRAE 55-2023, ASHRAE 202-2024, IES LM-83-23, IES TM-30-20, EPA methodologies, IPCC AR6), and all project documents uploaded through the parsing engine. The system uses chunking strategies optimized for technical content—preserving tabular structures for ASHRAE threshold tables and maintaining section hierarchies for reference guide requirements. When an AI agent requires regulatory context (for example, the Credit Narrative Agent drafting a construction management plan for EQp1), the RAG pipeline retrieves the relevant LEED requirement text, applicable ASHRAE sections, and any project-specific design documents that constrain the narrative. Source citations are automatically appended to every generated output, enabling downstream audit verification.

## 6.2 AI Agent Ecosystem

The platform operates as a multi-agent system in which seven specialized AI agents collaborate to process credits end-to-end. Each agent exposes a well-defined interface: input schema, output schema, and confidence scoring. Agents communicate through the shared data model (Section 6.3), not through direct coupling.

### 6.2.1 LEED Requirement Interpreter Agent

The Requirement Interpreter Agent parses LEED credit language into structured, machine-interpretable requirement trees. Given a credit ID (e.g., WEp2), the agent decomposes the requirement into: inputs required, calculations mandated, thresholds to meet, documentation types to produce, and cross-credit dependencies. For WEp2, the agent identifies that the prerequisite requires three compliance paths (fixture efficiency, equipment efficiency, outdoor water use), each with distinct input requirements and calculation formulas.[^3^] This structured decomposition serves as the execution plan that downstream agents follow.

### 6.2.2 Document Extraction Agent

The Document Extraction Agent coordinates the parsing engine (Section 6.1.3) and transforms raw document content into structured entities in the data model. For an equipment schedule, the agent extracts fields including equipment type, manufacturer, model number, refrigerant type, refrigerant charge (lbs), COP, capacity (Btu/hr), and quantity—then validates each field against expected ranges and flags anomalies.[^4^] For EPD PDFs, the agent extracts GWP (A1-A3), declared unit, reference service life, EPD scope, validity date, and third-party verifier. The agent maintains provenance links: every extracted value carries a pointer to the source document, page number, and extraction confidence score.

### 6.2.3 Web Research Agent

The Web Research Agent performs multi-source data retrieval from public APIs and databases. Its capability map spans the full data landscape identified across credit categories: climate and hazard data (NOAA Precipitation Frequency Data Server for SSc3 rainfall calculations, FEMA National Flood Hazard Layer for LTc1 and SSc4, USGS 3D Elevation Program for slope analysis, NOAA Sea Level Rise Viewer for coastal sites); demographic and infrastructure data (U.S. Census Bureau ACS API for IPp2 Human Impact Assessment and LTc3 density calculations, EPA EJScreen for environmental justice indicators, HUD Fair Market Rents for LTc2); transit and location data (Google Maps Distance Matrix API, Walk Score API, TransitLand GTFS feeds for LTc3 trip counting); environmental product data (EC3 API for embodied carbon benchmarks, CRRC Rated Products database for SSc5 SRI values, USDA PLANTS database for SSc1 native species); and air quality data (EPA AirNow for EQp2 outdoor air quality investigation).[^5^] The agent implements parallel query execution, source credibility scoring (prioritizing .gov and .edu domains), and response caching with timestamp tracking to flag data older than 12 months.

### 6.2.4 Calculation Agent

The Calculation Agent executes the quantitative workflows that form the backbone of LEED compliance documentation. Its engine portfolio includes: the Water Calculation Engine (WEp2 baseline vs. proposed fixture calculations, WEc2 multi-option point optimization across six pathways, TIR irrigation calculations per EPA methodology); the Ventilation Calculator (EQp2 ASHRAE 62.1 VRP calculations with zone air distribution effectiveness, OA rate increases for EQc1); the Refrigerant GWP Engine (EAp5 inventory totals, EAc7 weighted average GWP comparison to category benchmarks of 1,400 for HVAC, 700 for data centers, 300 for retail refrigeration);[^6^] the Electrification COP Calculator (EAc1 weighted average COP = $\sum(\text{COP}_i \times \text{Capacity}_i) / \sum\text{Capacity}_i$ with climate zone exclusions); the Embodied Carbon Calculator (MRp2 cradle-to-gate GWP total = $\sum(\text{GWP}_i \times \text{Quantity}_i)$, MRc2 project-average GWP comparison to CLF/EPA industry baselines);[^7^] the Rainwater Management Engine (SSc3 NRCS TR-55 runoff calculations with curve number method); the Heat Island Calculator (SSc5 weighted nonroof/roof equation verification); and the Waste Diversion Engine (MRc5 overall diversion rate = $\sum(\text{Quantity} \times \text{Diversion Rate}) / \sum\text{Quantity}$, source-separated percentage tracking).[^8^] Each engine produces an auditable calculation spreadsheet with all formulas visible and inputs cross-referenced to source documents.

### 6.2.5 Credit Narrative Agent

The Credit Narrative Agent generates the prose documents that accompany calculations in LEED submissions. Operating through structured templates with constrained generation (temperature = 0.3, top-p = 0.8), the agent produces: decarbonization plans (EAp1, capped at two pages with retrofit timelines, cost estimates, and avoided cost calculations); construction management plans (EQp1, seven-section plans covering no-smoking policy, extreme heat protection, HVAC protection, source control, pathway interruption, housekeeping, and scheduling); outdoor air quality investigation reports (EQp2, referencing EPA AirNow data for attainment/nonattainment status); biophilic design narratives (EQc2, addressing all five biophilic principles); accessibility strategy descriptions (EQc3, one to two paragraphs per selected strategy); rainwater management plan narratives (SSc3, LID/GI strategy documentation); and resilient site design narratives (SSc4, hazard-specific strategy documentation with ASCE 24 and FEMA 543 references).[^9^] Every narrative is grounded in project-specific data retrieved from the shared data model and validated against the RAG knowledge base for regulatory accuracy.

### 6.2.6 QA Reviewer Agent

The QA Reviewer Agent operates as a continuous quality layer, running three levels of verification. Level 1 (Automated QA) executes on every calculation: unit tests against known test cases from LEED reference examples, range validation (e.g., fixture flow rates between 0.1–5.0 gpf, water reduction percentages between 0–100%), cross-credit consistency checks (WEp2 proposed consumption must match WEc2 baseline), and completeness verification that all required fields are populated. Level 2 (AI QA Review) flags items for human review: low-confidence OCR extractions (score < 0.85), values outside expected ranges for the building type, first-time project types without historical benchmarks, and complex multi-option credits requiring engineer review. Level 3 (Pre-Submission Review) enforces mandatory professional sign-off: licensed engineer review for all calculations, LEED AP review for narrative documents, and final completeness checks against USGBC requirements.[^10^]

### 6.2.7 Submission Package Agent

The Submission Package Agent assembles the final deliverable for each credit: the calculation spreadsheet, narrative document, source document index, compliance table, evidence item list, and audit trail. The agent compiles all components into the Evidence Pack Standard format (Chapter 7), assigns confidence scores to each section, generates the audit trail documenting every AI action and human review, and exports to LEED Online-compatible formats. For credits with legal document implications (IPc2 Green Leases), the agent routes the package through a mandatory legal review gate before marking it submission-ready.

## 6.3 Data Model

The platform uses a relational data model with JSONB extensions for flexible document storage. The schema is organized into three entity groups.

### 6.3.1 Core Entities

**Project** stores the master record: project_id, building_type, rating_system (BD+C v5), certification_target, address (geocoded to lat/lon), climate_zone, egrid_subregion, gross_floor_area, fte_count, transient_count, project_phase, and created/modified timestamps.

**Building** captures physical attributes: building_id, project_id, stories, total_site_area, conditioned_floor_area, regularly_occupied_area, glazing_area, envelope_specs (U-values, SHGC), and construction_type.

**Credit** maintains the credit registry: credit_id (e.g., "WEp2"), credit_name, category (WE/EQ/EA/MR/LT/SS/IP/PR), automation_score (1–5), status (not_started, in_progress, review_pending, approved, submitted), target_points, and dependencies (array of prerequisite credit IDs).

**Requirement** decomposes each credit into actionable items: requirement_id, credit_id, requirement_type (input/calculation/threshold/documentation), description, source_standard, and completion_status.

**Evidence Item** tracks individual pieces of evidence: evidence_id, requirement_id, source_document_id, evidence_type (calculation/narrative/specification/photograph/certification), content_url, confidence_score, and extraction_metadata.

**Source Document** catalogs all uploaded documents: document_id, project_id, document_type (schedule/drawing/specification/EPD/cut_sheet/test_report/hauler_ticket/receipt), filename, upload_date, parsing_status, and extracted_field_count.

### 6.3.2 Process Entities

**Extracted Field** stores individual data points extracted by the Document Extraction Agent: field_id, document_id, field_name, field_value, confidence_score, page_number, bounding_box (for PDF sources), and extraction_method (OCR/table_parser/BIM_extraction/API_lookup).

**Calculation** records every calculation executed: calculation_id, credit_id, engine_name (e.g., "WaterCalculationEngine"), input_parameters (JSON), formula_applied, result_value, unit, execution_timestamp, and cross_reference to source extracted fields.

**Generated Report** tracks AI-generated documents: report_id, credit_id, agent_name, report_type, template_version, generation_timestamp, character_count, and narrative_coherence_score.

**Review Comment** captures human and AI review annotations: comment_id, target_id (calculations, reports, or evidence items), commenter_type (human/AI), severity (info/warning/blocker), comment_text, resolution_status, and resolution_timestamp.

### 6.3.3 Output Entities

**Submission Package** aggregates credit deliverables: package_id, credit_id, calculation_ids, report_ids, evidence_item_ids, confidence_tier (A/B/C per Section 7.2), package_status, assembly_timestamp, and reviewer_approval_log.

**Audit Trail** maintains an immutable log of every platform action: trail_id, project_id, action_type (upload/extract/calculate/generate/review/approve/submit), actor (agent_name or user_id), timestamp, input_refs, output_refs, and a SHA-256 hash linking to the previous trail entry for tamper evidence.

**Confidence Score** stores per-section confidence: score_id, package_id, section_number, score_value (0.0–1.0), tier (A/B/C), determining_factors (array of confidence/degradation reasons), and override_flag (if human reviewer adjusted the tier).

**Human Review Note** captures reviewer annotations: note_id, submission_package_id, reviewer_id, review_type (technical/regulatory/clarity), note_text, disposition (approved/approved_with_revisions/rejected), and disposition_timestamp.

## 6.4 Technical Stack Recommendations

### 6.4.1 Document Processing

The document processing pipeline requires Python with PyPDF2 and pdfplumber for PDF text/table extraction, OpenCV for image preprocessing and OCR enhancement, shapely and ifcopenshell for BIM geometry processing, pandas for schedule normalization, and a dedicated EPD parsing module using layout analysis to detect ISO 14025/EN 15804 document templates. For hauler ticket OCR in MRc5, a template-matching approach using standard form layouts (Waste Management, Republic Services, Allied Waste) provides higher accuracy than generic OCR.[^11^] All document processing runs asynchronously through a task queue, with extraction jobs dispatched based on document type.

### 6.4.2 LLM Infrastructure

The narrative generation layer uses GPT-4 or Claude 3 Opus via API, with structured output schemas enforced through function calling or constrained decoding. System prompts incorporate project-specific context from the unified data model and regulatory context from the RAG pipeline. All prompts are version-controlled and A/B tested against human-written reference documents. Temperature settings are conservative (0.2–0.4) for factual content and slightly higher (0.5–0.7) for creative strategy recommendations. A local model (Llama 3 70B or equivalent) handles routine template filling and classification tasks to reduce API costs, while frontier models are reserved for complex narrative generation.

### 6.4.3 Data Integration

The platform requires a PostgreSQL database with JSONB columns for flexible document metadata, PostGIS extensions for geospatial queries used in LT and SS credits, and a Redis cache layer for API response caching (NOAA, FEMA, Census data). The API layer uses FastAPI to expose RESTful endpoints for credit calculations, document uploads, and report generation. External API integrations include 20+ public data sources: NOAA PFDS, NRCS Soil Data Access, FEMA NFHL, USGS 3DEP/NHDPlus/NWI, Census ACS, Google Maps Platform, Walk Score, TransitLand, EPA AirNow, EPA EJScreen, EC3, CRRC, USDA PLANTS, and certification databases (GREENGUARD, FloorScore, CRI, HPD Repository, C2C Registry).[^12^] Each integration implements circuit breakers for API unavailability with graceful degradation to manual input.

### 6.4.4 Frontend

The consultant-facing interface uses React with TypeScript, organized around three primary views: the Project Dashboard (credit status overview, points tracking, confidence visualization), the Document Upload Center (drag-and-drop ingestion with extraction preview and confidence indicators), and the Review Portal (side-by-side comparison of AI-generated content against source documents, with inline commenting and approval workflows). Real-time updates via WebSocket connections enable collaborative review when multiple stakeholders (LEED AP, energy modeler, commissioning agent) work on the same project.

# 7. Evidence Pack Standard

Every credit processed by the platform produces an Evidence Pack—a standardized, audit-ready documentation bundle that a LEED reviewer can examine to verify compliance. The Evidence Pack Standard ensures consistency across all 43 automated credits and provides the structural foundation for USGBC submission.

## 7.1 Audit-Ready Package Structure

### 7.1.1 Standard 12-Section Evidence Pack

The platform generates every Evidence Pack following a uniform 12-section structure. This standardization enables reviewers to navigate any credit's documentation with predictable section ordering, and it ensures that no required element is omitted through automation oversight.

| Section | Name | Content Specifications | AI-Generated? |
|:---:|---|---|:---:|
| 1 | Executive Summary | Credit name, points pursued, compliance pathway selected, pass/fail determination, key data sources used | Yes |
| 2 | Methodology Statement | Standards referenced (with versions), calculation approach, assumptions made, data sources with URLs/dates | Yes |
| 3 | Input Data Registry | All input values with source document references, extraction confidence scores, and units | Partial |
| 4 | Calculation Worksheets | Step-by-step calculations with formulas visible, intermediate values, threshold comparisons, pass/fail flags | Yes |
| 5 | Generated Narratives | All AI-generated prose documents with template version, generation timestamp, and word count | Yes |
| 6 | Source Document Index | Complete inventory of uploaded documents with document IDs, parsing status, and extracted field counts | Yes |
| 7 | Evidence Item Compendium | Individual evidence items (certifications, test reports, photographs) cross-referenced to requirements | Yes |
| 8 | Compliance Matrix | Requirement-by-requirement compliance status with evidence references and confidence scores | Yes |
| 9 | Confidence Assessment | AI confidence tier assignment (A/B/C) with explanation of all confidence and degradation factors | Yes |
| 10 | Audit Trail | Chronological log of every AI action, human review event, and approval decision | Yes |
| 11 | Human Review Annotations | All reviewer comments, disposition decisions, and revision requests with reviewer identification | Human |
| 12 | Exception Report | Items flagged for manual review, data gaps, low-confidence extractions, and recommended actions | Yes |

The 12-section structure applies uniformly across calculation-heavy credits (WEp2, WEp2, EAc1, SSc3) and narrative-heavy credits (EAp1, EQp1, IPp1, IPp2). For credits requiring physical testing (EQc5 air quality testing), Section 4 defers to uploaded laboratory reports as primary evidence, with AI-generated parsing as secondary verification.

### 7.1.2 Section Purposes and Content Specifications

Section 1 (Executive Summary) serves as the reviewer entry point, distilling the entire credit into a single page. The AI generates this by aggregating the credit status, points calculation, and key compliance determinants. For WEp2, the summary states: "Water use reduction of 34.2% achieved through fixture efficiency (Option 2), exceeding the 20% prerequisite threshold. All 47 fixtures comply with Table 2 prescriptive rates or are WaterSense labeled."

Sections 2–4 form the technical core. The Methodology Statement explicitly names the standard version (e.g., ASHRAE 62.1-2022, not "the ASHRAE standard") to prevent version mismatch errors that are a common cause of LEED review comments. The Input Data Registry links every value to a source document and extraction confidence score, enabling reviewers to trace any number back to its origin. The Calculation Worksheets use visible formulas (not hidden cell references) so that reviewers can verify the math without platform access.

Sections 5–7 handle documentary evidence. Generated Narratives include the template version identifier so that reviewers can verify the narrative was produced against the correct LEED version. The Source Document Index and Evidence Item Compendium together ensure that every claim in Sections 1–4 is backed by verifiable documentation.

Sections 8–12 constitute the quality layer. The Compliance Matrix maps each LEED requirement to the evidence that satisfies it, mirroring the structure USGBC reviewers use. The Confidence Assessment (detailed in Section 7.2), Audit Trail, Human Review Annotations, and Exception Report together provide transparency into the AI's decision-making and the human oversight applied.

## 7.2 AI Confidence Scoring

### 7.2.1 Confidence Tier System

Every Evidence Pack receives an overall confidence tier based on the weakest-scoring critical section, using a weighted scoring algorithm that emphasizes calculation accuracy and evidence provenance.

| Tier | Label | Score Range | Meaning | Human Review Required |
|:---:|---|:---:|---|:---:|
| A | High Confidence | 0.90–1.00 | All critical inputs from high-confidence extractions or direct entry; calculations verified against known test cases; all thresholds met with margin; source citations complete | Minimal (spot check) |
| B | Moderate Confidence | 0.75–0.89 | One or more inputs from moderate-confidence extraction (0.70–0.89); some thresholds met narrowly; minor data gaps in non-critical sections; recommendations include specific actions to reach Tier A | Required (section review) |
| C | Low Confidence | < 0.75 | Critical inputs from low-confidence extraction (< 0.70); significant data gaps; thresholds not met or met by narrow margin; source citations incomplete; mandatory human review and correction before submission | Required (comprehensive review) |

The overall score is computed as a weighted average: Calculation Accuracy (30%), Evidence Provenance (25%), Narrative Quality (20%), Source Coverage (15%), and Cross-Credit Consistency (10%). The tier is assigned based on the overall score with a floor rule: if any critical section (Calculation, Evidence Provenance, or Source Coverage) scores below 0.70, the package is automatically Tier C regardless of the weighted average.

Confidence degradation factors include: data source age exceeding 12 months (degradation = 0.05 per year), API failure requiring manual entry (degradation = 0.10), OCR confidence below 0.85 (degradation = 0.15), unit conversion performed (degradation = 0.05), and cross-credit inconsistency detected (degradation = 0.20). These factors accumulate and are itemized in Section 9.

### 7.2.2 Confidence Visualization

The frontend displays confidence as a tier badge (A/B/C with color coding) on every credit card in the project dashboard. Clicking through reveals the detailed scorecard: each of the five component scores, the degradation factor inventory, and specific recommendations for tier improvement. For example, a WEp2 package at Tier B might show: "Improve to Tier A by uploading manufacturer cut sheets for 3 fixtures with low-confidence flow rate extractions (currently estimated from schedule text)."

## 7.3 Version Control and Audit Trail

### 7.3.1 Document Tracking

Every document uploaded to the platform receives a unique document identifier (UUID v4) and is stored immutably. When a document is revised (e.g., an updated fixture schedule from the design team), the new version is stored as a separate record with a parent pointer to the previous version. The system maintains a document lineage graph, and any Evidence Pack referencing a superseded document displays a warning banner: "This package references Document XYZ v1, which has been superseded by v2. Recalculation recommended."

### 7.3.2 Human Review Annotations

The Review Portal supports inline commenting on any section of the Evidence Pack. Reviewers can annotate calculation cells ("Verify this urinal count—schedule shows 12 but floor plan shows 14"), narrative paragraphs ("Add reference to local drought ordinance"), and evidence items ("Certificate expired—request updated documentation"). Each annotation carries a severity level (info/warning/blocker), a disposition (open/resolved/overridden), and the reviewer identity with timestamp. Blocker-level annotations must be resolved or explicitly overridden with justification before the package can be marked submission-ready.

The audit trail captures every action: document upload (timestamp, uploader, file hash), AI extraction (agent name, fields extracted, confidence scores), calculation execution (engine name, inputs, outputs, execution time), narrative generation (template version, LLM parameters, output hash), review annotation (reviewer, section, comment, disposition), and approval (reviewer, package version, approval timestamp). The trail uses SHA-256 chaining: each entry's hash incorporates the previous entry's hash, creating tamper-evident sequencing suitable for legal documentation requirements.

# 8. Risk and Quality Control Framework

The automation of LEED documentation introduces risks distinct from manual preparation: AI hallucination in generated narratives, extraction errors from OCR, calculation errors from incorrect formula application, and data staleness from cached API responses. This framework organizes controls into three categories—prevention, detection, and governance—mapped to the specific risk factors identified across all 43 credit analyses.

## 8.1 Prevention Controls

Prevention controls are engineering measures designed to stop errors before they propagate into Evidence Packs. They operate automatically during the generation pipeline.

### 8.1.1 Source-Grounded Generation

Every AI-generated output must be grounded in verified source material. The RAG pipeline (Section 6.1.4) enforces this by constraining narrative generation to content retrieved from the indexed knowledge base—LEED reference guide text, applicable standards, and project documents. The Credit Narrative Agent cannot generate compliance claims without a corresponding RAG retrieval. For calculations, the Calculation Agent refuses to execute if any required input lacks a source document reference. This principle, applied consistently, eliminates hallucinated regulatory references and phantom data points. For MRc3 Low-Emitting Materials, where 200–400 products require certification verification, the source-grounded approach means every compliance claim links to a specific database query result (GREENGUARD, FloorScore, CRI) with a timestamp and URL.[^13^]

### 8.1.2 Rules-Based Validation Engine

A dedicated validation engine enforces hard constraints before any output reaches the Evidence Pack. The engine maintains a ruleset database keyed to credit ID and requirement ID. For WEp2, the engine validates that all fixture flow rates are below Table 2 maximums, that the water reduction percentage is calculated using the correct baseline formula, and that the irrigation TIR calculation applies the EPA methodology (ET₀ × Plant Factor × Area / Irrigation Efficiency).[^14^] For EAc1, the engine validates climate zone exclusions (zones 0–2 excluded from space heating COP determination), confirms the weighted average formula is correctly applied, and checks that the denominator sums all included capacities.[^15^] For SSc3, the engine verifies NRCS curve numbers are within valid ranges (40–98), rainfall depths are retrieved for the correct percentile events (80th/85th/90th), and the weighted CN calculation uses area-proportional weighting. Rule violations generate blockers that prevent Evidence Pack assembly until resolved.

### 8.1.3 Mandatory Evidence Mapping

The platform enforces a "no claim without evidence" policy. Every requirement in the Requirement Interpreter Agent's decomposition must be linked to at least one evidence item before the Compliance Matrix (Section 7.1.2, Section 8) can be marked complete. If WEp2 requires verification that "all toilets are 1.28 gpf or less," the system will not allow package assembly until the fixture schedule extraction shows toilet flow rates meeting this threshold, with each value linked to a source document. Gaps are automatically listed in the Exception Report (Section 12) with specific instructions for remediation.

## 8.2 Detection Controls

Detection controls identify errors that slip past prevention measures. They operate on generated outputs and provide the feedback loop for quality improvement.

### 8.2.1 Hallucination Detection

The QA Reviewer Agent runs a hallucination detection pipeline on all narrative outputs. This pipeline: (1) extracts all factual claims from the generated text (names, numbers, standard references, threshold values); (2) cross-references each claim against the RAG knowledge base and source documents; (3) flags any claim with no supporting source as a hallucination candidate; and (4) assigns a hallucination risk score (0.0–1.0) based on claim density and verification rate. Narratives with risk scores above 0.10 require human review. The detection pipeline specifically targets common LLM failure modes in LEED contexts: invented ASHRAE section numbers, fabricated threshold values, nonexistent EPA methodologies, and incorrect credit prerequisite relationships.

### 8.2.2 Red-Flag Detection

The platform maintains a credit-specific red flag registry derived from common USGBC review comments and consultant experience. Flags include: water reduction percentages above 60% (unusually high, requires verification against fixture schedule completeness); refrigerant GWP values not found in the EPA/IPCC database (possible data entry error or new refrigerant requiring manual review); embodied carbon totals more than 50% below the CLF industry average for the building type (possible scope omission); and ventilation rates more than 30% above ASHRAE 62.1 minimums (possible unit conversion error or incorrect occupant density). Each flag triggers a contextual alert in the Review Portal with recommended verification steps.

### 8.2.3 Reviewer-Style QA Checklist

The QA Reviewer Agent applies a checklist structured to mimic the evaluation approach of a USGBC reviewer or third-party technical reviewer. The checklist covers: completeness (all required documentation items present), correctness (calculations match submitted data), consistency (narratives align with calculations, cross-credit data is consistent), compliance (all thresholds met with appropriate margin), clarity (narratives are understandable to reviewers without project context), and citations (all external data referenced with source and date). The checklist is credit-specific: the EAc7 checklist includes refrigerant charge unit verification (lbs vs. kg), GWP benchmark verification by equipment category, and tCO₂e calculation confirmation, while the MRc3 checklist includes certification validity date verification, CDPH Standard Method version confirmation, and percentage calculation methodology verification.[^16^]

## 8.3 Governance Controls

Governance controls establish the human oversight and organizational processes that ensure AI outputs meet professional standards before reaching USGBC.

### 8.3.1 Human Approval Gate

No Evidence Pack may be marked "submission-ready" without passing through a human approval gate. The gate requires at minimum: a LEED AP review for all narrative documents, a licensed professional engineer (P.E.) review for all engineering calculations (structural, mechanical, electrical, plumbing), and a project manager sign-off for overall package completeness. The approval workflow is role-based: reviewers see only credits in their domain, and approvals are recorded with digital signatures in the Audit Trail. For legal documents (IPc2 Green Leases), a mandatory legal review gate precedes the LEED AP review. The platform tracks approval status per credit and blocks package export until all required approvals are recorded.

### 8.3.2 Version-Controlled Audit Trail

The Audit Trail (Section 6.3.3) provides tamper-evident logging suitable for legal and professional liability defense. Each entry includes: action type, actor identity, timestamp in UTC, input references, output references, and a cryptographic hash. The hash chain ensures that any retroactive modification breaks the chain, making the audit trail suitable for demonstrating that AI-generated content was reviewed by qualified professionals prior to submission. The audit trail is exportable as a standalone PDF appendix for projects requiring enhanced documentation (legal proceedings, insurance claims, or regulatory investigation).

### 8.3.3 Continuous Learning

The platform implements a continuous learning loop that improves automation quality over time. The loop operates as follows: (1) every human review annotation is captured in a feedback database with structured categorization (extraction error, calculation error, narrative inaccuracy, missing requirement, regulatory change); (2) monthly aggregation identifies patterns—recurrent extraction failures for a specific manufacturer cut sheet format, consistent narrative revisions for a particular credit section, or systematic threshold misinterpretations; (3) engineering updates the parsing templates, narrative templates, or validation rules to address the pattern; and (4) A/B testing validates that the update improves quality metrics (confidence scores, review annotation rates, time-to-approval) before full deployment. The feedback database also feeds model fine-tuning: when sufficient annotated examples accumulate for a specific document type or credit category, the platform can fine-tune the local LLM to improve extraction and generation accuracy for that domain. This closed-loop approach ensures the platform demonstrably improves with usage while the layered quality controls prevent performance regression on previously mastered credit categories.

The following table summarizes the complete Risk and Quality Control Framework with control assignments, trigger conditions, and responsible actors:

| Control ID | Category | Control Name | Trigger Condition | Response Action | Responsible Actor |
|:---:|---|---|---|---|---|
| PC-01 | Prevention | Source-Grounded Generation | Every narrative generation request | Constrain output to RAG-retrieved content; block unsupported claims | RAG Pipeline |
| PC-02 | Prevention | Rules-Based Validation | Every calculation execution | Validate against credit-specific rule database; block on violation | Validation Engine |
| PC-03 | Prevention | Mandatory Evidence Mapping | Evidence Pack assembly attempt | Prevent assembly if any requirement lacks evidence linkage | Submission Package Agent |
| PC-04 | Prevention | Input Schema Enforcement | Document upload | Reject documents failing schema validation; flag parsing errors | Document Parsing Engine |
| DC-01 | Detection | Hallucination Detection | Narrative generation complete | Extract and verify all factual claims; flag unsupported claims | QA Reviewer Agent |
| DC-02 | Detection | Red-Flag Detection | Calculation or extraction complete | Compare against anomaly thresholds; generate contextual alerts | QA Reviewer Agent |
| DC-03 | Detection | Reviewer-Style QA Checklist | Evidence Pack assembly complete | Apply credit-specific checklist; flag any failed item | QA Reviewer Agent |
| DC-04 | Detection | Cross-Credit Consistency | Any calculation update | Verify downstream credit data consistency; flag mismatches | Calculation Agent |
| GC-01 | Governance | Human Approval Gate | Evidence Pack marked ready for review | Route to required reviewers; block export until all approvals | Workflow Engine |
| GC-02 | Governance | Version-Controlled Audit Trail | Every platform action | Record tamper-evident log with cryptographic chaining | Audit Trail Service |
| GC-03 | Governance | Confidence Tier Enforcement | Evidence Pack confidence assessment | Tier C packages blocked from export; Tier B requires section review | Submission Package Agent |
| GC-04 | Governance | Continuous Learning | Monthly aggregation | Identify error patterns; update templates/rules; A/B test changes | Engineering Team |
| GC-05 | Governance | Data Staleness Monitoring | API response retrieval | Flag cached data older than 12 months; trigger refresh | Web Research Agent |

The framework's layered design—prevention at the generation stage, detection at the review stage, governance at the organizational stage—ensures that AI automation augments rather than replaces professional judgment. The estimated risk reduction is substantial: prevention controls eliminate an estimated 80–85% of common errors before they reach human review, detection controls catch 10–15% of residual issues, and governance controls ensure the remaining 5% is identified and corrected by qualified professionals before USGBC submission. This architecture enables the platform to achieve the per-credit time savings documented throughout the research phase—ranging from 65% for complex narrative credits to 92% for rule-based compliance credits—while maintaining documentation quality that meets or exceeds manually prepared submissions.
