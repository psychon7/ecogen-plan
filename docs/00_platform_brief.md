# Platform Brief

## Executive Summary

Ecogen is a LEED v5 automation platform for consultants. It reduces the repetitive work of credit documentation by ingesting project data, running deterministic calculations, assembling evidence packs, drafting narratives, and routing outputs through human review. The platform is explicitly assistant-first: AI accelerates the work, while humans remain accountable for compliance decisions.

The realistic product target is 70-85% automation across supported credits. Some workflows can approach 95% automation because they are narrow, deterministic, and API-backed. Other workflows, especially energy modeling, whole-building life-cycle assessment, site/GIS interpretation, and compliance sign-off, require expert review. This stance resolves the older plan's optimism and preserves the project principle: save time without pretending that professional judgment can be removed.

## What Ecogen Builds

- Credit-specific automation skills, one LEED credit per independently testable module.
- Project intake that resolves building type, location, rating system, region, and data availability.
- Structured upload and parsing for schedules, spreadsheets, PDFs, energy model exports, BIM/CAD outputs, and product documentation.
- Deterministic calculation engines for water, refrigerants, carbon, energy deltas, heat island, light pollution, and embodied carbon.
- Evidence packs that include source documents, calculations, confidence scores, human review records, and audit trail.
- Manual-upload/Arc-compatible deliverables in V1; direct Arc submission only after verified V2 integration.

## What Ecogen Does Not Build

- A fully autonomous LEED certification agent.
- AI interpretation of complex CAD/site plans without specialized tools and human verification.
- Final compliance approval without qualified human sign-off.
- Global full automation where regional data sources are unavailable.

## MVP Wedge

The best first commercial wedge is Water Efficiency:

1. WEp2 - Minimum Water Efficiency
2. WEc2 - Enhanced Water Efficiency

Water efficiency is calculation-driven, universal, easy for consultants to verify, and valuable even before the full platform exists. The first build should support manual fixture entry and spreadsheet upload before OCR/product-matching automation; the same fixture and occupancy data then feeds WEc2 optimization.

The 14-day demo can still use PRc2 as a pipeline proof and EAp5/EAc7 as a shared-input workflow, but the commercial MVP should be framed around Kimi's five suites: Water Efficiency, Refrigerant Management, Quality Plans, Integrative Process Assessment, and Low-Emitting Materials.

## Trust Model

Every evidence pack should make the reviewer comfortable answering four questions:

- Where did each data point come from?
- Which formula or rule transformed it?
- What is the confidence level and why?
- Which qualified person approved or corrected it?

This trust model is the main product moat. Speed matters, but auditability is what makes the output usable in a LEED workflow.
