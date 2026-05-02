"""Skills listing route — exposes available LEED skill manifests."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from agents.skill_adapter import SkillLoader

router = APIRouter(prefix="/skills", tags=["skills"])

_loader = SkillLoader()


@router.get("/")
async def list_skills() -> list[dict[str, Any]]:
    """List all available LEED skill manifests."""
    manifests = _loader.list_skills()
    return [m.model_dump() for m in manifests]


@router.get("/{credit_code}")
async def get_skill(credit_code: str) -> dict[str, Any]:
    """Get a specific skill manifest by credit code."""
    try:
        manifest = _loader.load_by_credit_code(credit_code)
    except FileNotFoundError:
        raise HTTPException(404, f"Skill not found for credit code: {credit_code}")
    return manifest.model_dump()
