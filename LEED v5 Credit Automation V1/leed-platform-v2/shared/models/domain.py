"""Core domain models — projects, credits, evidence, workflows."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from shared.enums.types import (
    BuildingType,
    ConfidenceTier,
    CreditStatus,
    DataFallbackLevel,
    DocumentFormat,
    EvidenceType,
    HITLAction,
    HITLStatus,
    RatingSystem,
    TargetLevel,
    WorkflowStatus,
)


# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------

class ProjectModel(BaseModel):
    """Canonical project representation."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str | None = None
    name: str
    code: str | None = None
    description: str | None = None

    building_type: BuildingType
    leed_version: str = "v5"
    rating_system: RatingSystem
    target_level: TargetLevel

    address: str
    city: str
    state: str
    zip_code: str
    country: str = "US"
    latitude: float | None = None
    longitude: float | None = None
    region: str | None = None

    credits_completed: int = 0
    credits_total: int = 0
    points_achieved: int = 0
    points_target: int = 0

    status: str = "active"
    created_by: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Credit instance (project-scoped)
# ---------------------------------------------------------------------------

class CreditModel(BaseModel):
    """A single LEED credit instance attached to a project."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    credit_code: str          # e.g. "WEp2", "MRc3"
    credit_name: str
    is_prerequisite: bool = False
    max_points: int = 0

    status: CreditStatus = CreditStatus.NOT_STARTED
    progress: int = 0         # 0-100

    input_data: dict[str, Any] = Field(default_factory=dict)
    extracted_data: dict[str, Any] = Field(default_factory=dict)
    calculation_results: dict[str, Any] = Field(default_factory=dict)
    confidence_score: float | None = None
    confidence_tier: ConfidenceTier | None = None

    points_achieved: int | None = None
    regional_status: str = "available"

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------

class EvidenceItem(BaseModel):
    """A single piece of auditable evidence."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_credit_id: str
    workflow_id: str | None = None

    evidence_type: EvidenceType
    source_file: str | None = None
    source_page: int | None = None
    locator: str | None = None       # page/table/cell/field/API path

    extracted_value: Any = None
    normalized_value: Any = None
    confidence: float = 0.0
    requires_human_review: bool = False

    checksum: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ConfidenceScore(BaseModel):
    """Weighted confidence score for a credit package."""
    overall: float
    tier: ConfidenceTier
    components: dict[str, float] = Field(default_factory=dict)
    floor_triggered: bool = False     # True if any component < 0.70


# ---------------------------------------------------------------------------
# Workflow state
# ---------------------------------------------------------------------------

class WorkflowState(BaseModel):
    """Snapshot of a durable credit workflow run."""
    workflow_id: str
    project_id: str
    credit_id: str
    credit_code: str

    status: WorkflowStatus = WorkflowStatus.PENDING
    current_step: int = 0
    current_step_name: str | None = None
    total_steps: int = 0

    step_results: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None
    retry_count: int = 0

    hitl_task_id: str | None = None
    confidence_score: float | None = None

    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# HITL
# ---------------------------------------------------------------------------

class HITLTask(BaseModel):
    """Human-in-the-loop review task."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str
    project_id: str
    credit_code: str
    step_name: str

    assignee_role: str = "leed_consultant"
    assignee_id: str | None = None
    assignee_email: str | None = None

    status: HITLStatus = HITLStatus.PENDING
    priority: str = "normal"

    documents: list[str] = Field(default_factory=list)
    checklist: list[str] = Field(default_factory=list)
    instructions: str = ""
    confidence_scores: dict[str, float] = Field(default_factory=dict)

    sla_hours: int = 24
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None

    completed_at: datetime | None = None


class HITLDecision(BaseModel):
    """Reviewer decision on a HITL task."""
    task_id: str
    action: HITLAction
    reviewer_id: str
    reviewer_email: str | None = None
    comments: str | None = None
    rejection_reason: str | None = None
    return_to_step: int | None = None
    checklist_results: dict[str, bool] = Field(default_factory=dict)
    decided_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Source tracking
# ---------------------------------------------------------------------------

class SourceSnapshot(BaseModel):
    """Record of an external data retrieval for audit."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str | None = None
    source_name: str
    source_type: str            # api, static_dataset, uploaded_document, manual_entry
    source_version: str | None = None
    url: str | None = None
    query_params: dict[str, Any] = Field(default_factory=dict)

    fallback_level: DataFallbackLevel = DataFallbackLevel.LIVE_API
    response_checksum: str | None = None
    confidence: float = 1.0
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Document / evidence package
# ---------------------------------------------------------------------------

class GeneratedDocument(BaseModel):
    """A single generated document artifact."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_credit_id: str
    workflow_id: str | None = None
    name: str
    format: DocumentFormat
    storage_path: str
    checksum: str | None = None
    file_size_bytes: int | None = None
    template_version: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EvidencePackage(BaseModel):
    """The full audit-ready evidence package for one credit."""
    project_id: str
    credit_code: str
    documents: list[GeneratedDocument] = Field(default_factory=list)
    evidence_items: list[EvidenceItem] = Field(default_factory=list)
    calculation_records: list[dict[str, Any]] = Field(default_factory=list)
    source_snapshots: list[SourceSnapshot] = Field(default_factory=list)
    manifest_checksum: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Audit log entry (append-only)
# ---------------------------------------------------------------------------

class AuditLogEntry(BaseModel):
    """Immutable audit log record."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    actor_id: str | None = None
    actor_type: str = "system"     # system, user, agent
    project_id: str | None = None
    credit_code: str | None = None
    workflow_id: str | None = None
    event_type: str
    event_data: dict[str, Any] = Field(default_factory=dict)
    input_checksum: str | None = None
    output_checksum: str | None = None
