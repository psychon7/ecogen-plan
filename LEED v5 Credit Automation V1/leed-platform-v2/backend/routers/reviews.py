"""HITL review routes — resolve Restate durable promises."""

from __future__ import annotations

from typing import Any

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from shared.config import settings
from shared.enums.types import HITLAction

router = APIRouter(prefix="/reviews", tags=["reviews"])

RESTATE_INGRESS = settings.restate_ingress_url


class ReviewDecisionRequest(BaseModel):
    action: HITLAction
    reviewer_id: str
    reviewer_email: str | None = None
    comments: str | None = None
    rejection_reason: str | None = None
    return_to_step: int | None = None
    checklist_results: dict[str, bool] = {}


@router.post("/{workflow_id}/decide", status_code=200)
async def submit_review_decision(
    workflow_id: str,
    body: ReviewDecisionRequest,
) -> dict[str, Any]:
    """Submit a HITL review decision, resolving the Restate durable promise."""
    decision = body.model_dump()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{RESTATE_INGRESS}/CreditWorkflow/{workflow_id}/resolve_review",
            json=decision,
            timeout=10.0,
        )
        if resp.status_code >= 400:
            raise HTTPException(502, f"Restate error: {resp.text}")

    return resp.json()
