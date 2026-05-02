"""OpenAI Agents SDK implementation of AgentExecutionProvider.

Uses the openai-agents library to orchestrate tool-using agents with
structured output enforcement.  File uploads go through the OpenAI
Files API; results are parsed into the platform's Pydantic models.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from agents import Agent, Runner, function_tool
from openai import AsyncOpenAI

from agents.provider import AgentExecutionProvider
from shared.config import settings
from shared.models.agent_io import (
    CertificationMatch,
    CertificationMatchRequest,
    CertificationMatchResult,
    DetectedElement,
    EvidenceExtractionRequest,
    EvidenceExtractionResult,
    ExtractedProduct,
    ImageAnalysisRequest,
    ImageAnalysisResult,
    MissingEvidence,
    NarrativeRequest,
    NarrativeResult,
    NarrativeSection,
    SandboxTaskRequest,
    SandboxTaskResult,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tool definitions available to extraction agents
# ---------------------------------------------------------------------------

@function_tool
def search_leed_rules(credit_code: str, query: str) -> str:
    """Search LEED v5 reference rules for a specific credit code and query."""
    # In production, queries a vector store or loaded reference text.
    return json.dumps({
        "credit_code": credit_code,
        "query": query,
        "result": f"LEED v5 reference text for {credit_code} (placeholder — load from skill bundle)",
    })


@function_tool
def query_product_database(product_name: str, manufacturer: str | None = None) -> str:
    """Query certification databases (GREENGUARD, FloorScore, WaterSense, ENERGY STAR)."""
    return json.dumps({
        "product_name": product_name,
        "manufacturer": manufacturer,
        "certifications": [],
        "note": "Placeholder — call real certification API via ExternalDataService",
    })


# ---------------------------------------------------------------------------
# Provider implementation
# ---------------------------------------------------------------------------

class OpenAIAgentsProvider(AgentExecutionProvider):
    """Executes agent tasks using the OpenAI Agents SDK."""

    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_model
        self._extraction_model = settings.openai_extraction_model

    # ----- Evidence Extraction -----------------------------------------------

    async def extract_evidence(
        self, request: EvidenceExtractionRequest
    ) -> EvidenceExtractionResult:
        start = time.monotonic()

        system_prompt = self._build_extraction_prompt(request)

        agent = Agent(
            name="EvidenceExtractionAgent",
            instructions=system_prompt,
            model=self._extraction_model,
            tools=[search_leed_rules, query_product_database],
        )

        user_message = (
            f"Extract structured evidence from the uploaded files for LEED credit {request.credit_code}.\n"
            f"Files: {json.dumps(request.file_paths)}\n"
            f"Return JSON with 'extracted_products' and 'missing_items' arrays."
        )

        result = await Runner.run(agent, user_message)
        parsed = self._parse_json_output(result.final_output)

        elapsed_ms = int((time.monotonic() - start) * 1000)

        return EvidenceExtractionResult(
            credit_code=request.credit_code,
            extracted_products=[ExtractedProduct(**p) for p in parsed.get("extracted_products", [])],
            missing_items=[MissingEvidence(**m) for m in parsed.get("missing_items", [])],
            raw_tables=parsed.get("raw_tables", []),
            warnings=parsed.get("warnings", []),
            agent_model=self._extraction_model,
            execution_time_ms=elapsed_ms,
        )

    # ----- Narrative Generation -----------------------------------------------

    async def draft_credit_narrative(
        self, request: NarrativeRequest
    ) -> NarrativeResult:
        start = time.monotonic()

        agent = Agent(
            name="NarrativeGenerationAgent",
            instructions=(
                f"You are a senior LEED consultant drafting a credit narrative for {request.credit_code}.\n"
                f"Tone: {request.tone}. Max words: {request.max_words}.\n"
                "Return JSON with 'sections' (array of {{heading, content, references}}) and 'word_count'."
            ),
            model=self._model,
        )

        user_message = (
            f"Project summary:\n{json.dumps(request.project_summary, indent=2)}\n\n"
            f"Evidence data:\n{json.dumps(request.evidence_data, indent=2)}\n\n"
            f"Calculation results:\n{json.dumps(request.calculation_results, indent=2)}"
        )

        result = await Runner.run(agent, user_message)
        parsed = self._parse_json_output(result.final_output)

        elapsed_ms = int((time.monotonic() - start) * 1000)

        return NarrativeResult(
            credit_code=request.credit_code,
            sections=[NarrativeSection(**s) for s in parsed.get("sections", [])],
            word_count=parsed.get("word_count", 0),
            references=parsed.get("references", []),
            agent_model=self._model,
            execution_time_ms=elapsed_ms,
        )

    # ----- Image Analysis -----------------------------------------------------

    async def analyze_images(
        self, request: ImageAnalysisRequest
    ) -> ImageAnalysisResult:
        start = time.monotonic()

        agent = Agent(
            name="ImageAnalysisAgent",
            instructions=(
                f"Analyze images for LEED credit {request.credit_code}.\n"
                f"Analysis type: {request.analysis_type}.\n"
                "Return JSON with 'detected_elements' (array of {{element_type, label, value, confidence}}), "
                "'measurements', 'annotations', and 'warnings'."
            ),
            model=self._model,
        )

        user_message = f"Analyze these images: {json.dumps(request.image_paths)}"
        result = await Runner.run(agent, user_message)
        parsed = self._parse_json_output(result.final_output)

        elapsed_ms = int((time.monotonic() - start) * 1000)

        return ImageAnalysisResult(
            credit_code=request.credit_code,
            detected_elements=[DetectedElement(**e) for e in parsed.get("detected_elements", [])],
            measurements=parsed.get("measurements", {}),
            annotations=parsed.get("annotations", []),
            warnings=parsed.get("warnings", []),
            agent_model=self._model,
            execution_time_ms=elapsed_ms,
        )

    # ----- Certification Matching ----------------------------------------------

    async def match_certifications(
        self, request: CertificationMatchRequest
    ) -> CertificationMatchResult:
        start = time.monotonic()

        products_data = [p.model_dump() for p in request.products]

        agent = Agent(
            name="CertificationMatchingAgent",
            instructions=(
                f"Match products against certification databases for LEED credit {request.credit_code}.\n"
                f"Databases to check: {json.dumps(request.certification_databases)}.\n"
                "Return JSON with 'matches' (array of {{product_name, manufacturer, certification_name, "
                "certified, certified_value, deviation_pct}}) and 'unmatched_products'."
            ),
            model=self._model,
            tools=[query_product_database],
        )

        user_message = f"Products to match:\n{json.dumps(products_data, indent=2)}"
        result = await Runner.run(agent, user_message)
        parsed = self._parse_json_output(result.final_output)

        elapsed_ms = int((time.monotonic() - start) * 1000)

        return CertificationMatchResult(
            credit_code=request.credit_code,
            matches=[CertificationMatch(**m) for m in parsed.get("matches", [])],
            unmatched_products=parsed.get("unmatched_products", []),
            warnings=parsed.get("warnings", []),
            agent_model=self._model,
            execution_time_ms=elapsed_ms,
        )

    # ----- Sandbox Task -------------------------------------------------------

    async def run_sandbox_task(
        self, request: SandboxTaskRequest
    ) -> SandboxTaskResult:
        start = time.monotonic()

        script = request.script_content or "(no script provided)"

        agent = Agent(
            name="SandboxAgent",
            instructions=(
                f"Execute the following task for LEED credit {request.credit_code}.\n"
                f"Task type: {request.task_type}.\n"
                "Return JSON with 'success', 'output_data', and optionally 'stdout'/'stderr'."
            ),
            model=self._model,
        )

        user_message = (
            f"Script:\n```python\n{script}\n```\n\n"
            f"Input data:\n{json.dumps(request.input_data, indent=2)}"
        )

        result = await Runner.run(agent, user_message)
        parsed = self._parse_json_output(result.final_output)

        elapsed_ms = int((time.monotonic() - start) * 1000)

        return SandboxTaskResult(
            credit_code=request.credit_code,
            success=parsed.get("success", False),
            output_data=parsed.get("output_data", {}),
            output_files=parsed.get("output_files", []),
            stdout=parsed.get("stdout"),
            stderr=parsed.get("stderr"),
            execution_time_ms=elapsed_ms,
        )

    # ----- Helpers ------------------------------------------------------------

    def _build_extraction_prompt(self, request: EvidenceExtractionRequest) -> str:
        base = (
            f"You are an expert LEED evidence extraction agent for credit {request.credit_code}.\n"
            "Your job is to read uploaded documents (PDFs, images, spreadsheets) and extract "
            "structured evidence with source citations.\n\n"
            "Rules:\n"
            "- Every extracted item MUST include source_file and source_page.\n"
            "- Assign a confidence score (0.0–1.0) to every item.\n"
            "- List missing evidence clearly.\n"
            "- Return ONLY valid JSON matching the output schema.\n"
        )
        if request.skill_instructions:
            base += f"\nCredit-specific instructions:\n{request.skill_instructions}\n"
        return base

    @staticmethod
    def _parse_json_output(raw: str) -> dict[str, Any]:
        """Best-effort JSON extraction from agent output."""
        text = raw.strip()
        # Strip markdown fences if present
        if text.startswith("```"):
            lines = text.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Agent returned non-JSON output; wrapping as raw_text")
            return {"raw_text": raw, "warnings": ["Agent output was not valid JSON"]}
