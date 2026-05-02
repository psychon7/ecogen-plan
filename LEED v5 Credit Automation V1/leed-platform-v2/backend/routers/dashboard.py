"""Dashboard routes — stats, active workflows, SLA alerts."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
async def get_dashboard_stats() -> dict[str, Any]:
    """Return high-level dashboard statistics."""
    # In production, query Postgres + Restate for live data
    return {
        "active_projects": 0,
        "active_workflows": 0,
        "pending_reviews": 0,
        "completed_credits": 0,
        "sla_alerts": 0,
    }
