"""ProjectObject — Restate Virtual Object keyed by project_id.

Owns the project-level workflow state: selected credits, overall
status, and evidence summary.  All mutations go through Restate
handlers so state is automatically durable.
"""

from __future__ import annotations

import logging
from typing import Any

import restate
from restate import VirtualObject, ObjectContext

from shared.enums.types import CreditStatus

logger = logging.getLogger(__name__)

project_object = VirtualObject("ProjectObject")


# ---------------------------------------------------------------------------
# State keys
# ---------------------------------------------------------------------------

SELECTED_CREDITS = "selected_credits"  # list[dict]
PROJECT_STATUS = "project_status"      # str
EVIDENCE_SUMMARY = "evidence_summary"  # dict


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

@project_object.handler()
async def select_credits(ctx: ObjectContext, credits: list[dict[str, Any]]) -> dict[str, Any]:
    """Register which credits a project will pursue."""
    project_id = ctx.key()
    logger.info("ProjectObject[%s] selecting %d credits", project_id, len(credits))

    await ctx.set(SELECTED_CREDITS, credits)
    await ctx.set(PROJECT_STATUS, "active")
    await ctx.set(EVIDENCE_SUMMARY, {
        c["credit_code"]: {"status": CreditStatus.NOT_STARTED, "progress": 0}
        for c in credits
    })

    return {"project_id": project_id, "credits_selected": len(credits)}


@project_object.handler()
async def get_status(ctx: ObjectContext) -> dict[str, Any]:
    """Return current project status snapshot."""
    project_id = ctx.key()
    credits = await ctx.get(SELECTED_CREDITS) or []
    status = await ctx.get(PROJECT_STATUS) or "unknown"
    summary = await ctx.get(EVIDENCE_SUMMARY) or {}

    completed = sum(1 for v in summary.values() if isinstance(v, dict) and v.get("status") == CreditStatus.COMPLETED)

    return {
        "project_id": project_id,
        "status": status,
        "credits_total": len(credits),
        "credits_completed": completed,
        "evidence_summary": summary,
    }


@project_object.handler()
async def update_credit_status(
    ctx: ObjectContext,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Update the status of a single credit within this project."""
    credit_code = payload["credit_code"]
    new_status = payload["status"]
    progress = payload.get("progress", 0)

    summary = await ctx.get(EVIDENCE_SUMMARY) or {}
    summary[credit_code] = {"status": new_status, "progress": progress}
    await ctx.set(EVIDENCE_SUMMARY, summary)

    # If all credits are completed, mark project done
    credits = await ctx.get(SELECTED_CREDITS) or []
    all_done = len(credits) > 0 and all(
        isinstance(summary.get(c["credit_code"]), dict)
        and summary[c["credit_code"]].get("status") == CreditStatus.COMPLETED
        for c in credits
    )
    if all_done:
        await ctx.set(PROJECT_STATUS, "completed")

    return {"credit_code": credit_code, "status": new_status, "progress": progress}


@project_object.handler()
async def mark_complete(ctx: ObjectContext) -> dict[str, Any]:
    """Force-mark project as completed."""
    project_id = ctx.key()
    await ctx.set(PROJECT_STATUS, "completed")
    logger.info("ProjectObject[%s] marked complete", project_id)
    return {"project_id": project_id, "status": "completed"}
