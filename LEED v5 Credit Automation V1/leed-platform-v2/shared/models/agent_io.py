"""Agent execution request and result models.

These are the contracts between the platform (Restate) and the agent layer.
Provider-neutral — any AgentExecutionProvider must accept and return these.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Evidence Extraction
# ---------------------------------------------------------------------------

class ExtractedProduct(BaseModel):
    """A single product/material/system extracted from uploaded documents."""
    product_name: str
    manufacturer: str | None = None
    category: str | None = None
    model_number: str | None = None

    # Credit-specific fields (populated depending on credit)
    voc_content: str | None = None
    flow_rate: str | None = None
    gwp_value: float | None = None
    certification: str | None = None

    source_file: str
    source_page: int | None = None
    confidence: float = 0.0


class MissingEvidence(BaseModel):
    """An evidence gap identified by the extraction agent."""
    product_name: str | None = None
    field_name: str | None = None
    missing_evidence: str
    suggestion: str | None = None


class EvidenceExtractionRequest(BaseModel):
    """Request to extract structured evidence from uploaded files."""
    credit_code: str
    project_id: str
    file_paths: list[str]             # S3 keys of uploaded files
    skill_instructions: str | None = None
    input_schema: dict[str, Any] | None = None
    additional_context: dict[str, Any] = Field(default_factory=dict)


class EvidenceExtractionResult(BaseModel):
    """Structured output from evidence extraction agent."""
    credit_code: str
    extracted_products: list[ExtractedProduct] = Field(default_factory=list)
    missing_items: list[MissingEvidence] = Field(default_factory=list)
    raw_tables: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    agent_model: str | None = None
    execution_time_ms: int | None = None
    token_usage: dict[str, int] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Narrative Generation
# ---------------------------------------------------------------------------

class NarrativeSection(BaseModel):
    """A section of a LEED credit narrative."""
    heading: str
    content: str
    references: list[str] = Field(default_factory=list)


class NarrativeRequest(BaseModel):
    """Request to draft a LEED credit narrative."""
    credit_code: str
    project_id: str
    project_summary: dict[str, Any]
    evidence_data: dict[str, Any]
    calculation_results: dict[str, Any] = Field(default_factory=dict)
    skill_instructions: str | None = None
    tone: str = "professional"
    max_words: int = 2000


class NarrativeResult(BaseModel):
    """Generated narrative output."""
    credit_code: str
    sections: list[NarrativeSection] = Field(default_factory=list)
    word_count: int = 0
    references: list[str] = Field(default_factory=list)
    agent_model: str | None = None
    execution_time_ms: int | None = None


# ---------------------------------------------------------------------------
# Image Analysis
# ---------------------------------------------------------------------------

class DetectedElement(BaseModel):
    """An element detected from an image (site plan, lighting layout, etc.)."""
    element_type: str
    label: str | None = None
    value: str | None = None
    location: str | None = None
    confidence: float = 0.0


class ImageAnalysisRequest(BaseModel):
    """Request to analyze images (site plans, material schedules, etc.)."""
    credit_code: str
    project_id: str
    image_paths: list[str]            # S3 keys
    analysis_type: str                # "site_plan", "lighting_layout", "material_schedule"
    skill_instructions: str | None = None


class ImageAnalysisResult(BaseModel):
    """Structured output from image analysis agent."""
    credit_code: str
    detected_elements: list[DetectedElement] = Field(default_factory=list)
    measurements: dict[str, Any] = Field(default_factory=dict)
    annotations: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    agent_model: str | None = None
    execution_time_ms: int | None = None


# ---------------------------------------------------------------------------
# Sandbox Task (generic code execution)
# ---------------------------------------------------------------------------

class SandboxTaskRequest(BaseModel):
    """Request to execute a task in a sandboxed environment."""
    credit_code: str
    project_id: str
    task_type: str
    script_path: str | None = None    # Path within the skill bundle
    script_content: str | None = None
    input_data: dict[str, Any] = Field(default_factory=dict)
    file_paths: list[str] = Field(default_factory=list)
    timeout_seconds: int = 120


class SandboxTaskResult(BaseModel):
    """Output from sandbox execution."""
    credit_code: str
    success: bool
    output_data: dict[str, Any] = Field(default_factory=dict)
    output_files: list[str] = Field(default_factory=list)
    stdout: str | None = None
    stderr: str | None = None
    execution_time_ms: int | None = None


# ---------------------------------------------------------------------------
# Certification Matching
# ---------------------------------------------------------------------------

class CertificationMatch(BaseModel):
    """Result of matching a product against certification databases."""
    product_name: str
    manufacturer: str | None = None
    certification_name: str | None = None   # GREENGUARD Gold, FloorScore, etc.
    certified: bool = False
    certified_value: str | None = None      # e.g. certified flow rate
    deviation_pct: float | None = None
    expiry_date: datetime | None = None
    source_url: str | None = None


class CertificationMatchRequest(BaseModel):
    """Request to match products against certification databases."""
    credit_code: str
    project_id: str
    products: list[ExtractedProduct]
    certification_databases: list[str] = Field(
        default_factory=lambda: ["greenguard", "floorscore", "watersense", "energy_star"]
    )


class CertificationMatchResult(BaseModel):
    """Certification matching results."""
    credit_code: str
    matches: list[CertificationMatch] = Field(default_factory=list)
    unmatched_products: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    agent_model: str | None = None
    execution_time_ms: int | None = None
