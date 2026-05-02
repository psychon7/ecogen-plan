"""Provider-neutral agent execution interface.

Every agent runtime (OpenAI Agents SDK, Claude, local VLM, human fallback)
implements this ABC.  Restate calls these methods — the provider handles
model selection, file I/O, and structured output enforcement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from shared.models.agent_io import (
    CertificationMatchRequest,
    CertificationMatchResult,
    EvidenceExtractionRequest,
    EvidenceExtractionResult,
    ImageAnalysisRequest,
    ImageAnalysisResult,
    NarrativeRequest,
    NarrativeResult,
    SandboxTaskRequest,
    SandboxTaskResult,
)


class AgentExecutionProvider(ABC):
    """Contract for all agent execution runtimes.

    Restate services depend only on this interface — never on a
    concrete SDK.  This prevents vendor lock-in and allows swapping
    providers at runtime.
    """

    @abstractmethod
    async def extract_evidence(
        self, request: EvidenceExtractionRequest
    ) -> EvidenceExtractionResult:
        """Read uploaded files and extract structured evidence."""

    @abstractmethod
    async def draft_credit_narrative(
        self, request: NarrativeRequest
    ) -> NarrativeResult:
        """Generate a LEED credit narrative from structured evidence."""

    @abstractmethod
    async def analyze_images(
        self, request: ImageAnalysisRequest
    ) -> ImageAnalysisResult:
        """Interpret site plans, lighting layouts, material schedules, etc."""

    @abstractmethod
    async def match_certifications(
        self, request: CertificationMatchRequest
    ) -> CertificationMatchResult:
        """Match extracted products against certification databases."""

    @abstractmethod
    async def run_sandbox_task(
        self, request: SandboxTaskRequest
    ) -> SandboxTaskResult:
        """Execute a script in a sandboxed environment."""
