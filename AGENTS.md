# Repository Guidelines

## Project Structure & Module Organization

This repository is the planning and architecture workspace for Ecogen, a LEED v5 automation platform. Top-level analysis files such as `EXECUTIVE_SUMMARY_REALISTIC.md`, `LEED_v5_Realistic_Implementation_Guide.md`, and `data_flow_architecture.md` are source-of-truth planning documents. The `leed-platform/` directory contains product, architecture, UI, backend, auth, and infrastructure specifications. The `skills/` directory contains LEED credit automation skill drafts, shared workflow prototypes (`durable_workflow.py`, `hitl_system.py`), and `SKILL_TEMPLATE.md` for new credit skills. Generated analysis artifacts are stored as `.json`, `.txt`, `.xlsx`, `.png`, and `.docx` files at the repository root.

## Build, Test, and Development Commands

No package manifest or build system is currently present. Use these commands when working with the existing prototypes and documentation:

```bash
python skills/durable_workflow.py
```

Runs the durable workflow prototype directly.

```bash
python -m pytest skills/
```

Expected test command once tests are added under `skills/**/tests/`.

```bash
rg "HITL" leed-platform skills
```

Searches architecture and skill files quickly for implementation references.

## Coding Style & Naming Conventions

Use Python 3.12 style for prototype code. Prefer 4-space indentation, `snake_case` for functions and variables, and `PascalCase` for classes such as orchestrators or agents. Keep one LEED credit per skill directory, using lowercase credit-style names such as `ip_p3_carbon/` or `ea_c3_energy_enhanced/`. Markdown files should use descriptive headings, short sections, and tables for structured contracts, matching `skills/SKILL_TEMPLATE.md`.

## Testing Guidelines

Place skill tests in `skills/<credit_code>/tests/` and name files `test_<behavior>.py`. Tests should cover input validation, calculation outputs, HITL pause/resume behavior, and regional data fallbacks. For workflow changes, include failure and retry cases so durable state behavior is verified.

## Commit & Pull Request Guidelines

Current history contains only `Initial commit`, so no formal commit convention is established. Use short, imperative commit subjects such as `Add carbon skill validation notes` or `Update HITL workflow schema`. Pull requests should include a concise summary, affected paths, validation performed, and screenshots only when UI specs or visual artifacts change. Link related issues or decision-log entries when applicable.

## Agent-Specific Instructions

Treat `EXECUTIVE_SUMMARY_REALISTIC.md`, `.instructions.md`, and `CLAUDE.md` as primary context before changing platform assumptions. Preserve the project stance: realistic automation levels, mandatory human review for compliance-critical outputs, regional data variability, and one independently testable skill per LEED credit.
