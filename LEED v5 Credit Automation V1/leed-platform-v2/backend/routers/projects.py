"""Project management routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from shared.models.domain import ProjectModel

router = APIRouter(prefix="/projects", tags=["projects"])


class CreateProjectRequest(BaseModel):
    name: str
    building_type: str
    rating_system: str
    target_level: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str = "US"
    description: str | None = None


class SelectCreditsRequest(BaseModel):
    credits: list[dict[str, Any]]


# In-memory store for POC — replaced by Postgres in production
_projects: dict[str, dict[str, Any]] = {}


@router.post("/", status_code=201)
async def create_project(body: CreateProjectRequest) -> dict[str, Any]:
    """Create a new LEED project."""
    project = ProjectModel(**body.model_dump())
    _projects[project.id] = project.model_dump()
    return {"id": project.id, "name": project.name}


@router.get("/{project_id}")
async def get_project(project_id: str) -> dict[str, Any]:
    """Retrieve project details."""
    project = _projects.get(project_id)
    if not project:
        raise HTTPException(404, f"Project {project_id} not found")
    return project


@router.get("/")
async def list_projects() -> list[dict[str, Any]]:
    """List all projects."""
    return list(_projects.values())
