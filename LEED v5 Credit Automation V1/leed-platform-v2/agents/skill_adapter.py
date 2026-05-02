"""Skill loader and adapter layer.

Loads LEED skill bundles from disk, parses skill.yaml manifests,
and prepares agent context for the chosen execution provider.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import yaml

from shared.models.skill import SkillManifest

logger = logging.getLogger(__name__)

SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"


class SkillLoader:
    """Discovers and loads LEED Skill Standard bundles from the skills/ directory."""

    def __init__(self, skills_root: Path = SKILLS_ROOT) -> None:
        self._root = skills_root
        self._cache: dict[str, SkillManifest] = {}

    def load(self, credit_slug: str) -> SkillManifest:
        """Load a skill manifest by directory slug (e.g. 'mr_c3_low_emitting')."""
        if credit_slug in self._cache:
            return self._cache[credit_slug]

        skill_dir = self._root / credit_slug
        manifest_path = skill_dir / "skill.yaml"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Skill manifest not found: {manifest_path}")

        with open(manifest_path) as f:
            raw = yaml.safe_load(f)

        manifest = SkillManifest(**raw)
        self._cache[credit_slug] = manifest
        logger.info("Loaded skill %s (%s)", manifest.id, manifest.credit_code)
        return manifest

    def load_by_credit_code(self, credit_code: str) -> SkillManifest:
        """Load skill manifest by LEED credit code (e.g. 'MRc3')."""
        for d in self._root.iterdir():
            if not d.is_dir():
                continue
            manifest_path = d / "skill.yaml"
            if not manifest_path.exists():
                continue
            with open(manifest_path) as f:
                raw = yaml.safe_load(f)
            if raw.get("credit_code") == credit_code:
                return self.load(d.name)
        raise FileNotFoundError(f"No skill found for credit code: {credit_code}")

    def list_skills(self) -> list[SkillManifest]:
        """Return all available skill manifests."""
        manifests = []
        for d in sorted(self._root.iterdir()):
            if not d.is_dir():
                continue
            try:
                manifests.append(self.load(d.name))
            except Exception as e:
                logger.warning("Skipping skill %s: %s", d.name, e)
        return manifests

    def get_instructions(self, credit_slug: str) -> str:
        """Load the agent-facing instructions.md for a skill."""
        path = self._root / credit_slug / "instructions.md"
        if not path.exists():
            return ""
        return path.read_text()

    def get_input_schema(self, credit_slug: str) -> dict[str, Any]:
        """Load the JSON Schema for skill inputs."""
        path = self._root / credit_slug / "input_schema.json"
        if not path.exists():
            return {}
        return json.loads(path.read_text())

    def get_output_schema(self, credit_slug: str) -> dict[str, Any]:
        """Load the JSON Schema for skill outputs."""
        path = self._root / credit_slug / "output_schema.json"
        if not path.exists():
            return {}
        return json.loads(path.read_text())


class OpenAISkillAdapter:
    """Prepares a skill bundle for execution via the OpenAI Agents SDK.

    Builds the agent system prompt by combining:
    - Skill instructions
    - Input/output schemas
    - Credit-specific rules
    """

    def __init__(self, loader: SkillLoader | None = None) -> None:
        self._loader = loader or SkillLoader()

    def prepare_agent_context(
        self,
        credit_slug: str,
        project_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build the agent system prompt and tool config for a skill."""
        manifest = self._loader.load(credit_slug)
        instructions = self._loader.get_instructions(credit_slug)
        input_schema = self._loader.get_input_schema(credit_slug)
        output_schema = self._loader.get_output_schema(credit_slug)

        system_prompt = self._build_system_prompt(manifest, instructions, output_schema)

        return {
            "manifest": manifest.model_dump(),
            "system_prompt": system_prompt,
            "input_schema": input_schema,
            "output_schema": output_schema,
            "project_data": project_data or {},
        }

    @staticmethod
    def _build_system_prompt(
        manifest: SkillManifest,
        instructions: str,
        output_schema: dict[str, Any],
    ) -> str:
        parts = [
            f"# LEED Credit: {manifest.credit_code} — {manifest.credit_name}",
            f"Category: {manifest.category} | Points: {manifest.max_points} | Prerequisite: {manifest.is_prerequisite}",
            "",
        ]
        if instructions:
            parts.append("## Instructions")
            parts.append(instructions)
            parts.append("")
        if output_schema:
            parts.append("## Required Output Schema")
            parts.append(f"```json\n{json.dumps(output_schema, indent=2)}\n```")
            parts.append("")
        parts.append(
            "## Rules\n"
            "- Every extracted item MUST include source_file and source_page.\n"
            "- Assign a confidence score (0.0–1.0) to every item.\n"
            "- List all missing evidence clearly.\n"
            "- Return ONLY valid JSON matching the output schema.\n"
            "- Do NOT make compliance decisions — only extract and propose.\n"
        )
        return "\n".join(parts)
