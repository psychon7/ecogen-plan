"""CreditWorkflow — Restate Workflow keyed by (project_id, credit_id).

This is the heart of the platform.  Each LEED credit runs through an
8-step durable workflow.  Restate manages retries, state persistence,
and crash recovery.  The workflow NEVER lets an agent decide whether
to advance — only your platform validates and progresses.
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Any

import restate
from restate import Workflow, WorkflowContext, WorkflowSharedContext

from shared.enums.types import CreditStatus, HITLStatus, WorkflowStatus

logger = logging.getLogger(__name__)

credit_workflow = Workflow("CreditWorkflow")


# ---------------------------------------------------------------------------
# Durable promise names
# ---------------------------------------------------------------------------

HITL_PROMISE = "hitl_review_decision"


# ---------------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------------

@credit_workflow.main()
async def run(ctx: WorkflowContext, request: dict[str, Any]) -> dict[str, Any]:
    """Execute the full credit automation workflow.

    Steps:
      1. validate_inputs
      2. fetch_external_data
      3. run_agent_extraction
      4. validate_extraction
      5. run_calculations
      6. pause_for_review  (HITL — durable promise)
      7. generate_documents
      8. finalize_package
    """
    project_id = request["project_id"]
    credit_code = request["credit_code"]
    credit_id = request.get("credit_id", f"{project_id}:{credit_code}")
    file_paths = request.get("file_paths", [])
    skill_id = request.get("skill_id", "")

    workflow_id = ctx.key()
    logger.info("CreditWorkflow[%s] starting for %s / %s", workflow_id, project_id, credit_code)

    results: dict[str, Any] = {}

    # ---- Step 1: Validate inputs -------------------------------------------
    ctx.set("status", WorkflowStatus.RUNNING)
    ctx.set("current_step", "validate_inputs")

    validation = await ctx.run(
        "validate_inputs",
        lambda: _validate_inputs(file_paths, request),
    )
    results["validate_inputs"] = validation
    if not validation.get("valid"):
        ctx.set("status", WorkflowStatus.FAILED)
        return {"status": "failed", "error": "Input validation failed", "details": validation}

    # ---- Step 2: Fetch external data ----------------------------------------
    ctx.set("current_step", "fetch_external_data")

    external_data = await ctx.run(
        "fetch_external_data",
        lambda: _fetch_external_data_stub(credit_code, project_id, request),
    )
    results["fetch_external_data"] = external_data

    # ---- Step 3: Run agent extraction ----------------------------------------
    ctx.set("current_step", "run_agent_extraction")

    # Idempotency key prevents duplicate agent calls on retry
    idempotency_key = _make_idempotency_key(workflow_id, "agent_extraction", file_paths)

    extraction = await ctx.run(
        "run_agent_extraction",
        lambda: _run_agent_extraction_stub(
            credit_code, project_id, file_paths, skill_id, idempotency_key,
        ),
    )
    results["run_agent_extraction"] = extraction

    # ---- Step 4: Validate extraction -----------------------------------------
    ctx.set("current_step", "validate_extraction")

    validation_result = await ctx.run(
        "validate_extraction",
        lambda: _validate_extraction(extraction, credit_code),
    )
    results["validate_extraction"] = validation_result

    # ---- Step 5: Run calculations --------------------------------------------
    ctx.set("current_step", "run_calculations")

    calculations = await ctx.run(
        "run_calculations",
        lambda: _run_calculations_stub(credit_code, extraction, external_data, request),
    )
    results["run_calculations"] = calculations

    # ---- Step 6: Pause for HITL review (durable promise) ---------------------
    ctx.set("current_step", "pause_for_review")
    ctx.set("status", WorkflowStatus.PAUSED_HITL)

    logger.info("CreditWorkflow[%s] pausing for HITL review", workflow_id)

    # Create HITL task metadata for the dashboard
    hitl_task = {
        "workflow_id": workflow_id,
        "project_id": project_id,
        "credit_code": credit_code,
        "extraction_summary": _summarize_extraction(extraction),
        "calculation_summary": calculations,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
    }
    ctx.set("hitl_task", hitl_task)

    # Wait for consultant to approve/reject via the dashboard
    hitl_decision = await ctx.promise(HITL_PROMISE).value()

    logger.info("CreditWorkflow[%s] HITL decision received: %s", workflow_id, hitl_decision.get("action"))

    if hitl_decision.get("action") == "reject":
        ctx.set("status", WorkflowStatus.FAILED)
        return {
            "status": "rejected",
            "reason": hitl_decision.get("rejection_reason", "Reviewer rejected"),
            "results": results,
        }

    if hitl_decision.get("action") == "request_changes":
        # In a full implementation, this would loop back to a specific step.
        ctx.set("status", WorkflowStatus.FAILED)
        return {
            "status": "changes_requested",
            "comments": hitl_decision.get("comments"),
            "return_to_step": hitl_decision.get("return_to_step"),
            "results": results,
        }

    results["hitl_decision"] = hitl_decision

    # ---- Step 7: Generate documents ------------------------------------------
    ctx.set("current_step", "generate_documents")
    ctx.set("status", WorkflowStatus.RUNNING)

    documents = await ctx.run(
        "generate_documents",
        lambda: _generate_documents_stub(credit_code, project_id, extraction, calculations),
    )
    results["generate_documents"] = documents

    # ---- Step 8: Finalize package --------------------------------------------
    ctx.set("current_step", "finalize_package")

    package = await ctx.run(
        "finalize_package",
        lambda: _finalize_package(project_id, credit_code, results),
    )
    results["finalize_package"] = package

    ctx.set("status", WorkflowStatus.COMPLETED)
    ctx.set("current_step", "done")

    logger.info("CreditWorkflow[%s] completed successfully", workflow_id)

    return {"status": "completed", "results": results}


# ---------------------------------------------------------------------------
# Shared handler: resolve HITL promise from dashboard
# ---------------------------------------------------------------------------

@credit_workflow.handler()
async def resolve_review(ctx: WorkflowSharedContext, decision: dict[str, Any]) -> dict[str, Any]:
    """Called by the FastAPI review endpoint to resolve the HITL promise."""
    await ctx.promise(HITL_PROMISE).resolve(decision)
    return {"resolved": True, "action": decision.get("action")}


@credit_workflow.handler()
async def get_workflow_status(ctx: WorkflowSharedContext) -> dict[str, Any]:
    """Query current workflow state without blocking."""
    status = await ctx.get("status") or WorkflowStatus.PENDING
    step = await ctx.get("current_step") or "unknown"
    hitl_task = await ctx.get("hitl_task")

    return {
        "workflow_id": ctx.key(),
        "status": status,
        "current_step": step,
        "hitl_task": hitl_task,
    }


# ---------------------------------------------------------------------------
# Step implementations (stubs — replaced by real services)
# ---------------------------------------------------------------------------

def _validate_inputs(file_paths: list[str], request: dict[str, Any]) -> dict[str, Any]:
    """Validate that required files and data are present."""
    errors = []
    if not file_paths:
        errors.append("No files uploaded")
    if not request.get("credit_code"):
        errors.append("credit_code is required")
    if not request.get("project_id"):
        errors.append("project_id is required")
    return {"valid": len(errors) == 0, "errors": errors}


def _fetch_external_data_stub(
    credit_code: str, project_id: str, request: dict[str, Any]
) -> dict[str, Any]:
    """Placeholder — replaced by ExternalDataService calls."""
    return {
        "credit_code": credit_code,
        "sources_queried": [],
        "data": {},
        "note": "Stub — implement ExternalDataService integration",
    }


def _run_agent_extraction_stub(
    credit_code: str,
    project_id: str,
    file_paths: list[str],
    skill_id: str,
    idempotency_key: str,
) -> dict[str, Any]:
    """Placeholder — replaced by AgentService call through provider."""
    return {
        "credit_code": credit_code,
        "extracted_products": [],
        "missing_items": [],
        "idempotency_key": idempotency_key,
        "note": "Stub — implement OpenAIAgentsProvider.extract_evidence()",
    }


def _validate_extraction(extraction: dict[str, Any], credit_code: str) -> dict[str, Any]:
    """Deterministic validation of agent extraction output."""
    warnings = []
    products = extraction.get("extracted_products", [])
    for p in products:
        if not p.get("source_file"):
            warnings.append(f"Product '{p.get('product_name')}' missing source_file")
        if (p.get("confidence") or 0) < 0.5:
            warnings.append(f"Product '{p.get('product_name')}' has low confidence ({p.get('confidence')})")

    return {
        "valid": len(warnings) == 0 or all("low confidence" in w for w in warnings),
        "warnings": warnings,
        "product_count": len(products),
        "missing_count": len(extraction.get("missing_items", [])),
    }


def _run_calculations_stub(
    credit_code: str,
    extraction: dict[str, Any],
    external_data: dict[str, Any],
    request: dict[str, Any],
) -> dict[str, Any]:
    """Placeholder — replaced by CalculationService."""
    return {
        "credit_code": credit_code,
        "results": {},
        "pass": False,
        "note": "Stub — implement CalculationService for this credit",
    }


def _generate_documents_stub(
    credit_code: str,
    project_id: str,
    extraction: dict[str, Any],
    calculations: dict[str, Any],
) -> dict[str, Any]:
    """Placeholder — replaced by DocumentService."""
    return {
        "credit_code": credit_code,
        "documents": [],
        "note": "Stub — implement DocumentService for PDF/XLSX generation",
    }


def _finalize_package(
    project_id: str, credit_code: str, results: dict[str, Any]
) -> dict[str, Any]:
    """Assemble the evidence package manifest."""
    manifest = {
        "project_id": project_id,
        "credit_code": credit_code,
        "steps_completed": list(results.keys()),
        "finalized_at": datetime.utcnow().isoformat(),
    }
    manifest_json = json.dumps(manifest, sort_keys=True)
    manifest["checksum"] = hashlib.sha256(manifest_json.encode()).hexdigest()
    return manifest


def _summarize_extraction(extraction: dict[str, Any]) -> dict[str, Any]:
    """Create a reviewer-friendly summary of extraction results."""
    return {
        "product_count": len(extraction.get("extracted_products", [])),
        "missing_count": len(extraction.get("missing_items", [])),
    }


def _make_idempotency_key(workflow_id: str, step: str, file_paths: list[str]) -> str:
    """Generate a deterministic idempotency key to prevent duplicate agent calls."""
    data = f"{workflow_id}:{step}:{json.dumps(sorted(file_paths))}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]
