# Agent Architecture

## Overview

The LEED AI Platform uses the platform as the agent foundation and LangGraph as the durable workflow engine for credit automation. The architecture is skill-based: one independently testable skill per LEED v5 credit or prerequisite, with explicit contracts for inputs, calculations, evidence, regional availability, and human review.

Core stance:

- AI assists; humans decide.
- Numeric calculations run in deterministic Python/tool code, not in the LLM.
- Every compliance-critical output requires at least one HITL checkpoint before it is marked approved.
- Regional data gaps and low-confidence results must be visible to users and preserved in the audit trail.
- V1 produces downloadable submission packages; direct USGBC Arc submission is a feature-flagged V2 capability.

## Agent Hierarchy

```
Lead Agent
  - Project intake and credit selection
  - Regional skill filtering
  - Dependency-aware scheduling
  - Result aggregation and user notifications

Credit Skill Agents
  - One skill per LEED credit/prerequisite
  - LangGraph workflow per skill
  - Own input schema, output schema, tests, templates, HITL checkpoints

Shared Service Agents
  - Document Extraction Agent
  - Calculation Engine Agent
  - Evidence Mapper Agent
  - Report Generator Agent
  - Review Checker Agent
  - Package Assembly Agent
```

## Kimi-Aligned Production Suites

Automation levels are intentionally conservative and should stay aligned with `EXECUTIVE_SUMMARY_REALISTIC.md`. The production MVP is suite-based; the older generated 16-skill set remains an assisted catalog and implementation inventory.

| Suite | Credit Agents | Review Pattern |
|-------|---------------|----------------|
| Water Efficiency | WEp2, WEc2 | LEED consultant review of fixture inputs, occupancy assumptions, formulas, and point optimization |
| Refrigerant Management | EAp5, EAc7 | LEED consultant or MEP reviewer verifies equipment schedule, refrigerant types, charges, and GWP assumptions |
| Quality Plans | EQp1, EQp2 | Contractor/MEP/LEED review of plan commitments, ventilation calculations, and filtration assumptions |
| Integrative Process Assessment | IPp1, IPp2 | LEED AP/project lead review of hazard/demographic sources and local context |
| Low-Emitting Materials | MRc3 | LEED/materials reviewer handles category assignment, certification validity, and exceptions |

Assisted catalog agents: PRc2, IPp3, EAp1, EAp2, EAc3, MRp2, MRc2, SSc3, SSc5, SSc6, LTc1, and LTc3. These agents may be useful before or after the production MVP, but their UI label should reflect review depth and regional/source caveats.

## LangGraph Workflow Pattern

Each skill is compiled as a LangGraph `StateGraph` and checkpointed after every node. The workflow state is keyed by `thread_id = {project_id}:{credit_code}:{workflow_id}` and persists to PostgreSQL so workflows survive restarts, API failures, and multi-day HITL pauses.

Standard nodes:

| Node | Purpose | HITL/Traceability Requirement |
|------|---------|-------------------------------|
| `validate_inputs` | Schema validation, type coercion, required-file checks | Store validation report and input file checksums |
| `extract_project_data` | Parse PDFs, spreadsheets, schedules, model outputs | Store extracted fields with confidence scores |
| `fetch_api_data` | Fetch external data through resilient API tools | Store source snapshot, query params, retrieval timestamp |
| `normalize_data` | Unit conversion, schema mapping, regional source substitution | Store mapping confidence and fallback flags |
| `calculate` | Deterministic credit calculation | Store calculation record, formula hash, inputs hash |
| `hitl_preliminary` | Methodology/data review for complex credits | Pause until approve/request changes/reject |
| `generate_documents` | Render PDF/XLSX/DOCX/JSON artifacts | Store document manifest and checksums |
| `quality_assurance` | Completeness, citation, consistency, confidence gates | Block low-confidence outputs from final approval |
| `hitl_final` | Final professional review | Required before credit status becomes approved |
| `package_export` | Build downloadable V1 submission package | Include manifest, evidence index, audit log |

Example routing:

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver

builder = StateGraph(LEEDState)
builder.add_node("validate_inputs", validate_inputs)
builder.add_node("extract_project_data", extract_project_data)
builder.add_node("fetch_api_data", fetch_api_data)
builder.add_node("normalize_data", normalize_data)
builder.add_node("calculate", calculate_credit)
builder.add_node("hitl_preliminary", create_hitl_checkpoint)
builder.add_node("generate_documents", generate_documents)
builder.add_node("quality_assurance", run_quality_gates)
builder.add_node("hitl_final", create_hitl_checkpoint)
builder.add_node("package_export", package_downloadable_artifacts)
builder.add_node("manual_preparation", manual_preparation)

builder.set_entry_point("validate_inputs")
builder.add_edge("validate_inputs", "extract_project_data")
builder.add_edge("extract_project_data", "fetch_api_data")
builder.add_edge("fetch_api_data", "normalize_data")
builder.add_edge("normalize_data", "calculate")
builder.add_edge("calculate", "hitl_preliminary")
builder.add_edge("generate_documents", "quality_assurance")
builder.add_edge("quality_assurance", "hitl_final")
builder.add_edge("hitl_final", "package_export")
builder.add_edge("package_export", END)
builder.add_edge("manual_preparation", END)

def route_hitl(state: LEEDState) -> str:
    action = state["hitl_result"]["action"]
    if action == "approve":
        return "generate_documents"
    if action == "request_changes":
        return state["hitl_result"].get("return_to_step", "calculate")
    return "manual_preparation"

builder.add_conditional_edges(
    "hitl_preliminary",
    route_hitl,
    {
        "generate_documents": "generate_documents",
        "calculate": "calculate",
        "fetch_api_data": "fetch_api_data",
        "manual_preparation": "manual_preparation",
    },
)

with PostgresSaver.from_conn_string(settings.DATABASE_URL) as checkpointer:
    workflow = builder.compile(checkpointer=checkpointer)
```

## HITL Policy

Every skill has at least one HITL checkpoint. Credits below 85% automation or involving licensed professional judgment have two checkpoints: preliminary methodology/data review and final document review.

HITL actions:

| Action | Workflow Effect | Audit Requirement |
|--------|-----------------|-------------------|
| `approve` | Resume to next node | Reviewer identity, timestamp, checklist, document hash |
| `request_changes` | Rewind to a specified node | Comments, affected fields, prior/new value if known |
| `reject` | Move to manual preparation | Reason, issues, archived AI attempt |
| `escalate` | Reassign review and reset/extend SLA | Old/new assignee, reason, SLA history |

Default SLA guidance:

| Review Type | SLA | Reviewer |
|-------------|-----|----------|
| Simple final review | 24 hours | LEED AP or consultant |
| Standard calculation review | 48 hours | LEED AP with discipline knowledge |
| Complex energy/LCA/GIS review | 72 hours | Energy modeler, LCA expert, GIS/site expert |

## Skill Dependencies

The Lead Agent schedules skills with dependency awareness. Shared outputs are written to project state and referenced by downstream skills instead of being re-parsed.

| Skill | Consumes | Enables |
|-------|----------|---------|
| IPp3 | EAp1, EAp5, MRp2 | Final carbon assessment package |
| EAc3 | EAp2 | Enhanced energy documentation |
| EAc7 | EAp5 | Enhanced refrigerant documentation |
| WEc2 | WEp2 | Enhanced water calculations |
| MRc2 | MRp2 | Embodied carbon reduction credit |

Independent demo skills can include PRc2, WEp2, EAp5, and a small assisted workflow. Production scheduling should prioritize suite dependencies: WEp2 before WEc2, EAp5 before EAc7, EQp1 before EQp2, and IPp1 before IPp2/SSc4-style resilience extensions.

## Evidence And Audit Trail Contract

Every factual claim, extraction, calculation, generated document, and reviewer decision must be traceable.

Required records:

| Record | Contents |
|--------|----------|
| Source snapshot | API/provider name, version, query params, retrieval timestamp, response checksum, data freshness |
| Evidence item | Source reference, extracted value/text, page/table/field locator, confidence, extractor version |
| Calculation record | Skill version, formula hash, input hash, parameters, source IDs, output, sandbox/runtime ID |
| Document manifest | File paths, formats, checksums, template version, source/evidence IDs used |
| HITL record | Reviewer, credential/role, action, checklist, comments, document hash, timestamps |
| Audit export | Manifest zip containing calculations, raw/redacted source snapshots, documents, workflow trace, signatures |

Confidence scoring applies at four levels:

- Extracted field confidence from OCR/parser certainty.
- Source quality and data freshness confidence.
- Calculation confidence from validation and formula checks.
- Generated narrative/document confidence from citation coverage and requirement alignment.

Outputs below the configured confidence threshold must route to HITL before final package export.

## API Tools And Fallbacks

External APIs are accessed through a shared `LEEDAPITool` base class that provides auth injection, timeout handling, token-bucket rate limits, Redis caching, circuit breakers, fallback chains, and source snapshot logging.

Fallback hierarchy:

1. Primary live API.
2. Valid cached response, clearly marked with retrieval time and staleness.
3. Static reference dataset bundled with a versioned platform release.
4. Manual data entry/HITL escalation when coverage or confidence is insufficient.

Regional routing must happen before execution. A credit can be:

| Status | Behavior |
|--------|----------|
| `available` | All required data sources supported for the project region |
| `limited` | Skill can run with fallbacks/manual inputs and visible warnings |
| `unavailable` | Skill is hidden or disabled unless a manual override is approved |

## USGBC Integration Boundary

V1 does not auto-submit to USGBC or Arc. The final workflow step generates a downloadable evidence package with PDF/XLSX/DOCX/JSON artifacts, a manifest, and upload guidance for the consultant.

Direct USGBC Arc integration is a V2 tool behind `ENABLE_USGBC_INTEGRATION=true`. Even in V2, Arc submission must occur only after final HITL approval and must retain manual download/upload as a fallback.

## Monitoring And Observability

Minimum metrics:

| Metric | Dimensions |
|--------|------------|
| Skill success rate | credit code, skill version, region |
| Workflow duration | automated time, HITL wait time, retry time |
| API health | provider, endpoint, error rate, latency, cache hit rate, circuit state |
| Confidence distribution | skill, source, extracted field, document section |
| HITL throughput | reviewer, SLA, action, revision count |
| Document quality | completeness, calculation verification, citation coverage, formatting |

Structured logs must include `workflow_id`, `thread_id`, `project_id`, `credit_code`, `skill_version`, `step_name`, `source_ids`, and any fallback/degradation flags.

---

*Version: 1.1*
*Last Updated: 2026-05-02*
