# LEED AI Platform - Product Overview

## Problem Statement

LEED consultants spend a large share of project time on repetitive documentation:

- Moving data between schedules, spreadsheets, and LEED forms.
- Verifying calculations across multiple tools.
- Searching for source data, product certifications, and missing evidence.
- Preparing reviewer-ready narratives, tables, and appendices.
- Coordinating expert review before submission.

The result is slow delivery, inconsistent evidence packages, and expensive reviewer rework.

## Solution

Ecogen is an AI-assisted LEED v5 evidence workspace. It ingests project documents and structured inputs, runs deterministic credit workflows, generates audit-ready evidence packs, and routes every compliance-critical package through qualified human review.

Ecogen prepares review-ready documentation. It does not guarantee points or replace LEED consultants.

## Target Users

### Primary: LEED Consultants

- Manage multiple LEED projects and credit trackers.
- Need faster documentation without sacrificing reviewer confidence.
- Own final credit strategy and approval.

### Secondary: Project Managers

- Coordinate architects, engineers, contractors, and owners.
- Need credit status, evidence gaps, and review bottlenecks in one place.

### Tertiary: Building Owners

- Want clearer progress, faster issue resolution, and fewer surprises.

## Core Use Cases

### UC-1: Project Setup

User creates a project, selects LEED v5 BD+C context, enters location/building metadata, and sees region-filtered credit availability.

### UC-2: Suite Workflow

User starts a suite such as Water Efficiency, uploads fixture schedules or enters data manually, reviews calculations, and receives a source-grounded evidence pack.

### UC-3: Expert Review

The platform creates a HITL task with document preview, confidence flags, source index, calculation workbook, and credit-specific checklist.

### UC-4: Progress Tracking

Project managers see each credit as pursued, draft generated, in review, internally approved, exported, submitted, or awarded.

### UC-5: Evidence Export

V1 exports manual-upload packages. Direct Arc/LEED Online upload is V2+ only after API access, terms, schema, permissions, and final approval flow are verified.

## Product Wedge

The first commercial wedge is Water Efficiency:

| Suite | Credits | Why |
|-------|---------|-----|
| Water Efficiency | WEp2 + WEc2 | Universal prerequisite, deterministic fixture calculations, transparent formulas, clear point optimization |

The broader production MVP follows the Kimi-aligned suite model:

| Priority | Suite | Credits |
|----------|-------|---------|
| 1 | Water Efficiency | WEp2 + WEc2 |
| 2 | Refrigerant Management | EAp5 + EAc7 |
| 3 | Quality Plans | EQp1 + EQp2 |
| 4 | Integrative Process Assessment | IPp1 + IPp2 |
| 5 | Low-Emitting Materials | MRc3 |

Existing generated skills such as IPp3, MRp2, MRc2, SSc3, SSc5, SSc6, LTc1, LTc3, PRc2, EAp1, EAp2, and EAc3 remain an assisted catalog, not the commercial MVP promise.

## Success Metrics

### User Metrics

- Water Efficiency documentation time reduced by 60-80% after source data is available.
- Evidence packs include source index, calculation trail, confidence tier, and review record.
- Reviewer rework decreases through fewer missing evidence items.

### Product Metrics

- 100% of compliance-critical exports have named human approval.
- 100% of factual claims cite upload, API source, static requirement source, or reviewer entry.
- Calculation workflows have golden test fixtures before production use.
- Regional availability is visible before a user starts a credit.

### Business Metrics

- First paid wedge validates on WEp2/WEc2 before broad catalog expansion.
- Suite-level pricing replaces unlimited-credit promises.
- Expansion is tied to verified source access and repeatable evidence pack quality.

## Differentiation

| Alternative | Approach | Ecogen Advantage |
|-------------|----------|------------------|
| Manual process | Consultant assembles everything by hand | Faster evidence assembly with audit trail and review workflow |
| Tally / LCA tools | Embodied carbon modeling | Ecogen consumes outputs and prepares LEED evidence packs |
| Energy modeling tools | Simulation and optimization | Ecogen parses outputs and prepares LEED documentation |
| Generic AI | Unstructured drafting | Source-grounded, credit-specific workflows with mandatory HITL |

## Business Model

- **Starter Suite:** One suite, targeted at boutique consultancies.
- **Professional:** All production MVP suites for firms managing multiple projects.
- **Enterprise:** API access, custom source routing, SSO, audit exports, and firm templates.

Per-credit and free-tier models can remain experiments, but the canonical commercial story should be suite-based.

## Roadmap

### Demo

Prove project intake, workflow execution, HITL review, and evidence export. PRc2 can validate the pipeline; WEp2 should validate the commercial wedge.

### Production MVP

Ship the five Kimi-aligned suites with source verification, regional gating, confidence scoring, reviewer dashboard, and manual export.

### Assisted Catalog

Expose generated skills as assistant workflows only after their inputs, APIs, tests, regional fallbacks, and review checklists are verified.

### V2 Platform

Direct Arc/LEED Online integration, additional credits from the 51-credit matrix, regional source routers, enterprise audit controls, and firm-wide reusable playbooks.

---

*Version: 2.0*
*Last Updated: 2026-05-02*
