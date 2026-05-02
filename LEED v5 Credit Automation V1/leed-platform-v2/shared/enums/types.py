"""Shared enumerations for the LEED automation platform."""

from enum import StrEnum


class WorkflowStatus(StrEnum):
    """Durable workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED_HITL = "paused_hitl"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class HITLStatus(StrEnum):
    """Human-in-the-loop review task status."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    CHANGES_REQUESTED = "changes_requested"
    ESCALATED = "escalated"
    EXPIRED = "expired"


class HITLAction(StrEnum):
    """Reviewer action on a HITL task."""
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_CHANGES = "request_changes"
    ESCALATE = "escalate"


class CreditStatus(StrEnum):
    """Project credit instance status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    AWAITING_REVIEW = "awaiting_review"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    MANUAL_REQUIRED = "manual_required"
    FAILED = "failed"


class AutomationLevel(StrEnum):
    """Skill automation tier classification."""
    FULLY_AUTOMATED = "fully_automated"
    MOSTLY_AUTOMATED = "mostly_automated"
    ASSISTED = "assisted"
    MANUAL_WITH_TEMPLATES = "manual_with_templates"


class ConfidenceTier(StrEnum):
    """Evidence confidence tier (drives review intensity)."""
    TIER_A = "A"  # High confidence, standard review
    TIER_B = "B"  # Medium confidence, detailed review
    TIER_C = "C"  # Low confidence, senior review required


class EvidenceType(StrEnum):
    """Type of evidence item in the audit trail."""
    EXTRACTED_FIELD = "extracted_field"
    CITATION = "citation"
    CALCULATION_INPUT = "calculation_input"
    CALCULATION_OUTPUT = "calculation_output"
    API_RESPONSE = "api_response"
    REVIEWER_NOTE = "reviewer_note"
    UPLOADED_DOCUMENT = "uploaded_document"


class DataFallbackLevel(StrEnum):
    """External data source fallback hierarchy."""
    LIVE_API = "live_api"
    CACHED = "cached"
    STATIC_SNAPSHOT = "static_snapshot"
    MANUAL_ENTRY = "manual_entry"


class DocumentFormat(StrEnum):
    """Generated document format."""
    PDF = "pdf"
    XLSX = "xlsx"
    DOCX = "docx"
    JSON = "json"
    ZIP = "zip"


class LEEDCategory(StrEnum):
    """LEED v5 credit categories."""
    IP = "Integrative Process"
    LT = "Location and Transportation"
    SS = "Sustainable Sites"
    WE = "Water Efficiency"
    EA = "Energy and Atmosphere"
    MR = "Materials and Resources"
    EQ = "Indoor Environmental Quality"
    IN = "Innovation"
    RP = "Regional Priority"


class BuildingType(StrEnum):
    """Supported building types for LEED rating."""
    OFFICE = "office"
    RETAIL = "retail"
    RESIDENTIAL = "residential"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    HOSPITALITY = "hospitality"
    WAREHOUSE = "warehouse"
    MIXED_USE = "mixed_use"
    OTHER = "other"


class RatingSystem(StrEnum):
    """LEED rating system type."""
    BD_C = "BD+C"  # Building Design and Construction
    ID_C = "ID+C"  # Interior Design and Construction
    O_M = "O+M"    # Operations and Maintenance


class TargetLevel(StrEnum):
    """LEED certification target level."""
    CERTIFIED = "Certified"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"
