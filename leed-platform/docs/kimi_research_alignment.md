# Kimi Research Alignment

## Purpose

This note aligns the `leed-platform/` plan with the newer Kimi LEED v5 credit automation research. It should be treated as the local bridge between the older platform plan and the newer research corpus under `Kimi_Agent_LEED v5 Credit Automation/`.

## Controlling Sources

| Source | Use |
|--------|-----|
| `Kimi_Agent_LEED v5 Credit Automation/leed_automation_sec00.md` | 51-credit research summary, five-suite MVP recommendation, time-savings ranges, risk controls |
| `Kimi_Agent_LEED v5 Credit Automation/leed_automation_sec01.md` | Credit-by-credit automation matrix, first-sprint targets, assist-only flags |
| `Kimi_Agent_LEED v5 Credit Automation/LEED_v5_Technical_Implementation.md` | API resilience, source routing, fallback chains, HITL state machine, audit package concepts |
| `Kimi_Agent_LEED v5 Credit Automation/skills/*/SKILL.md` | Detailed workflow drafts, regional availability, failure modes, output artifacts |
| `EXECUTIVE_SUMMARY_REALISTIC.md` and `.instructions.md` | Realism guardrails: AI assists, humans decide, regional variability, one skill per credit |

Where Kimi files disagree, prefer the 51-credit research matrix and the repository realism guardrails over inflated "fully automated" or no-review claims.

## Research Findings To Promote

Kimi analyzed 51 LEED v5 BD+C credits and scored them by automation suitability, commercial value, and risk. The strongest product signal is not "automate every credit"; it is to launch with high-confidence credit suites where data dependencies reinforce each other.

| Product Priority | Credits | Why |
|------------------|---------|-----|
| Water Efficiency wedge | WEp2 + WEc2 | Universal prerequisite, deterministic fixture calculations, clear point optimization story |
| Refrigerant Management | EAp5 + EAc7 | Equipment schedule parsing plus GWP lookup, narrow reviewer scope |
| Quality Plans | EQp1 + EQp2 | Repeatable plan/checklist workflows with clear evidence requirements |
| Integrative Process Assessment | IPp1 + IPp2 | High consultant time burden, public data and narrative synthesis, reviewer judgment still required |
| Low-Emitting Materials | MRc3 | High manual lookup burden across product certifications |

The old 8-credit list remains useful for a technical demo and generated skill inventory, but it should not be presented as the commercial MVP scope without the research caveat.

## Roadmap Alignment

| Stage | Aligned Scope | Notes |
|-------|---------------|-------|
| Pipeline proof | PRc2 | Use as the simplest end-to-end validation of intake, HITL, document generation, and audit trail. It is not the market wedge. |
| First user-facing wedge | WEp2, then WEc2 | Start with manual/spreadsheet fixture input and transparent formulas; add OCR/product matching after the workflow is trusted. |
| Production MVP suites | WEp2, WEc2, EAp5, EAc7, EQp1, EQp2, IPp1, IPp2, MRc3 | This is the Kimi-aligned commercial story. |
| Assisted catalog | IPp3, MRp2, MRc2, SSc3, SSc5, LTc3, LTc1, PRc2, SSc6, EAp1 | Useful skill drafts, but require explicit review, regional gating, and source verification before being sold as production-ready. |
| Assist-only / defer | EAp2, EAc2, EAc3, physical testing, field-verification credits | Parse completed outputs and prepare documentation; do not claim autonomous modeling or compliance verification. |

## Product Rules

- Use "prepare evidence pack," "run assistant," or "generate draft package" instead of "fully automate" in user-facing copy.
- Every compliance-critical package needs named human approval before it becomes submission-ready.
- Automation percentage changes review depth, not whether review exists.
- Points are estimates until submitted and awarded; UI should distinguish pursued, internally approved, submitted, and awarded.
- Direct Arc/LEED Online submission is V2+ and requires verified API access plus explicit final approval.
- Manual entry, regional source substitution, and manual-preparation handoff are first-class paths, not failures.

## Evidence Pack Standard

Every supported credit should produce an evidence pack with:

1. Credit summary and rating-system/version metadata.
2. Requirement source and addenda date.
3. Input inventory for uploads, manual fields, API data, and assumptions.
4. Source index with locators, retrieval dates, versions, and hashes.
5. Extracted data with field confidence.
6. Calculation workbook or report with formulas and intermediate values.
7. Generated narrative or compliance rationale.
8. Requirement-to-evidence matrix.
9. Confidence tier with degradation reasons and recommended fixes.
10. Workflow/audit trail with retries, fallbacks, and data changes.
11. Human review record with reviewer identity, credential/scope, decision, comments, and timestamp.
12. Exception report for missing data, regional limits, manual items, and unresolved risks.

## Open Verification Items

- Confirm official LEED v5 requirement/source licensing and addenda workflow.
- Verify API access for GBCI, Arc/LEED Online, WaterSense, ENERGY STAR, EPA SNAP, AHRI, EC3, GREENGUARD/FloorScore, Walk Score, GTFS, and regional substitutes.
- Create missing skill drafts for the research-priority suites that do not yet exist in the current generated 16-skill set.
- Normalize Kimi-generated skill automation percentages against the 51-credit matrix and the realistic automation model before seeding production data.
