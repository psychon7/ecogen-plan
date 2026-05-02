"""LEED Skill Manifest model — platform-owned skill standard."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from shared.enums.types import AutomationLevel


class SkillAgent(BaseModel):
    """An agent used by this skill."""
    name: str
    role: str   # evidence_extraction, certification_matching, narrative_generation


class SkillValidator(BaseModel):
    """A deterministic validation rule for this skill."""
    name: str
    description: str | None = None
    required: bool = True


class WorkflowStep(BaseModel):
    """A single step in the skill's workflow."""
    order: int
    name: str
    step_type: str   # validation, api_call, agent_extraction, calculation, hitl_review, document_generation
    automated: bool = True
    description: str | None = None
    retry_policy: dict[str, Any] = Field(default_factory=lambda: {"max_retries": 3, "backoff": "exponential"})
    timeout_seconds: int = 60
    on_failure: str = "abort"  # abort, continue, escalate


class RegionalAvailability(BaseModel):
    """Regional automation availability for a skill."""
    region: str
    automation_level: AutomationLevel
    available_apis: list[str] = Field(default_factory=list)
    fallback_strategy: str = "manual_entry"


class SkillManifest(BaseModel):
    """Parsed LEED Skill Standard manifest (skill.yaml).

    This is the platform-owned contract for a single LEED credit
    automation skill.  It is NOT tied to Deer-Flow, OpenAI, or any
    specific agent SDK.
    """
    id: str                                 # e.g. "leed.mr_c3.low_emitting_materials"
    credit_code: str                        # e.g. "MRc3"
    credit_name: str                        # e.g. "Low-Emitting Materials"
    leed_version: str = "v5"
    category: str                           # e.g. "MR"
    is_prerequisite: bool = False
    max_points: int = 0
    version: str = "1.0.0"

    automation_level: AutomationLevel = AutomationLevel.MOSTLY_AUTOMATED
    complexity: str = "medium"              # low, medium, high
    requires_human_review: bool = True

    # IO contracts
    inputs: list[dict[str, Any]] = Field(default_factory=list)
    outputs: list[dict[str, Any]] = Field(default_factory=list)

    # Workflow
    workflow_steps: list[WorkflowStep] = Field(default_factory=list)

    # Agents & validators
    agents: list[SkillAgent] = Field(default_factory=list)
    validators: list[SkillValidator] = Field(default_factory=list)

    # Regional
    regional_availability: list[RegionalAvailability] = Field(default_factory=list)

    # Dependencies
    required_apis: list[str] = Field(default_factory=list)
    skill_dependencies: list[str] = Field(default_factory=list)

    # File paths (relative to skill directory)
    instructions_file: str = "instructions.md"
    input_schema_file: str = "input_schema.json"
    output_schema_file: str = "output_schema.json"
    templates_dir: str = "templates"
    scripts_dir: str = "scripts"
