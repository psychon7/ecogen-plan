# LEED v5 Automation Opportunity Analysis — Execution Plan

## Objective
Analyze the full LEED v5 BD+C credit system to identify credits that can be 100% automated using AI/LLM/agentic/multimodal technologies, producing a comprehensive report with credit-by-credit automation blueprints, MVP recommendations, and platform architecture.

## Stage 1 — Document Ingestion & Credit Extraction
- **Goal**: Read and parse the LEED v5 BD+C Rating System PDF to extract all credits, their requirements, documentation types, and submission requirements.
- **Agents**: Document Analysis Agent
- **Output**: Structured inventory of all LEED v5 credits with documentation requirements

## Stage 2 — Deep Research (Parallel Swarm)
- **Goal**: Multi-dimensional research to classify each credit's automation potential
- **Skill**: deep-research-swarm (Route B — Focused Search with specific dimensions)
- **Parallel Research Tracks**:
  1. **Track A**: Credits requiring narratives, plans, policies, checklists (document-heavy credits)
  2. **Track B**: Credits requiring calculations, data analysis, spreadsheets (calculation-heavy credits)
  3. **Track C**: Credits requiring site photos, drawings, visual evidence (multimodal credits)
  4. **Track D**: Credits requiring public data, GIS, climate data, web research (data-fetch credits)
  5. **Track E**: Credits requiring product data, material schedules, procurement records (procurement credits)
  6. **Track F**: Credits requiring commissioning, MEP, engineering simulations (technical credits)
- **Output**: Per-credit automation classification with scores and rationale

## Stage 3 — Report Writing
- **Goal**: Compose the full 10-section analysis report
- **Skill**: report-writing
- **Input**: Stage 1 credit inventory + Stage 2 research findings
- **Output**: Complete markdown report with all required sections

## Stage 4 — Artifact Production
- **Goal**: Convert final markdown report to .docx
- **Skill**: docx
- **Output**: Professional Word document

## Deliverables
1. Comprehensive LEED v5 Credit Automation Matrix
2. Top credit automation blueprints (detailed per-credit workflows)
3. MVP scope recommendation (5-10 credits)
4. Platform architecture design
5. Evidence pack standard
6. Risk & quality control framework
7. Final .docx report
