"""Credit workflow routes — start workflows and query status."""

from __future__ import annotations

from typing import Any

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from shared.config import settings

router = APIRouter(prefix="/credits", tags=["credits"])

RESTATE_INGRESS = settings.restate_ingress_url


class StartWorkflowRequest(BaseModel):
    project_id: str
    credit_code: str
    file_paths: list[str] = []
    skill_id: str | None = None
    input_data: dict[str, Any] = {}


@router.post("/workflow/start", status_code=202)
async def start_credit_workflow(body: StartWorkflowRequest) -> dict[str, Any]:
    """Start a durable credit workflow via Restate."""
    workflow_id = f"{body.project_id}:{body.credit_code}"

    payload = body.model_dump()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{RESTATE_INGRESS}/CreditWorkflow/{workflow_id}/run/send",
            json=payload,
            timeout=10.0,
        )
        if resp.status_code >= 400:
            raise HTTPException(502, f"Restate error: {resp.text}")

    return {"workflow_id": workflow_id, "status": "started"}


@router.get("/workflow/{workflow_id}/status")
async def get_workflow_status(workflow_id: str) -> dict[str, Any]:
    """Query the current status of a credit workflow."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{RESTATE_INGRESS}/CreditWorkflow/{workflow_id}/get_workflow_status",
            json={},
            timeout=10.0,
        )
        if resp.status_code >= 400:
            raise HTTPException(502, f"Restate error: {resp.text}")

    return resp.json()
