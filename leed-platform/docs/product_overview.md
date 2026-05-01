# LEED AI Platform — Product Overview

## Problem Statement

LEED consultants spend 60-80% of project time on manual documentation:
- Copying data between spreadsheets
- Formatting reports for USGBC submission
- Verifying calculations across multiple tools
- Chasing missing information from project teams

**The result:** Projects take 6-12 months, consultants burn out, and sustainability goals slip.

## Solution

An AI-powered platform that automates LEED v5 credit documentation through:
1. **Intelligent data ingestion** — Parse energy models, drawings, schedules
2. **Automated calculations** — Run credit formulas with verified accuracy
3. **Document generation** — Produce audit-ready USGBC submissions
4. **Human-in-the-loop** — Expert review at critical checkpoints

## Target Users

### Primary: LEED Consultants
- Work at sustainability consulting firms
- Manage 5-15 projects simultaneously
- Bill $150-250/hour
- Pain: Documentation time eats margins

### Secondary: Project Managers
- Coordinate with architects, engineers, contractors
- Need visibility into credit status
- Pain: No single source of truth

### Tertiary: Building Owners
- Pay for LEED certification
- Want faster time-to-certification
- Pain: Unclear progress, missed deadlines

## Core Use Cases

### UC-1: Project Setup (5 minutes)
User creates project, specifies building type, location, target certification level.

### UC-2: Credit Automation (per credit)
User uploads source documents → AI extracts data → generates calculations → produces USGBC-ready submission.

### UC-3: Expert Review
LEED consultant reviews AI-generated documentation, approves or requests changes.

### UC-4: Progress Tracking
Project manager views dashboard of all credits, status, points achieved, remaining work.

### UC-5: USGBC Submission
Platform packages all documentation into USGBC Arc-compatible format for direct upload.

## Success Metrics

### User Metrics
- Time per credit: 8 hours → 2 hours (75% reduction)
- Projects per consultant per year: 10 → 25
- User satisfaction (NPS): > 50

### Business Metrics
- Credits automated per month: > 500
- API uptime: 99.9%
- Document generation accuracy: > 98%

### Product Metrics
- Credit completion rate: > 90%
- HITL approval rate: > 85%
- Time to first credit: < 10 minutes

## Differentiation

| Competitor | Approach | Our Advantage |
|------------|----------|---------------|
| Tally | Embodied carbon only | Full LEED coverage |
| cove.tool | Energy modeling | Document automation |
| Manual process | 100% human | 80% automated + expert review |

## Business Model

- **Freemium:** 2 credits free per month
- **Pro:** $299/month per user (unlimited credits)
- **Enterprise:** Custom pricing + API access

## Roadmap

### V1.0 (MVP) — 8 Credits
IPp3, WEp2, EAp5, MRp2, SSc6, PRc2, EAc7, SSc5

### V1.5 — 12 Credits
Add: EAp1, EAp2, WEc2, SSc3

### V2.0 — 16 Credits
Add: EAc3, MRc2, LTc3, LTc1

### V2.5 — Platform
USGBC Arc integration, API access, white-label

---

*Version: 1.0*
*Last Updated: 2026-03-21*
