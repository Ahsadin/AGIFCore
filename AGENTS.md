# AGIFCore Repo Rules

This repository has one canonical long-term project:

- `projects/agifcore_master/`

Before starting any work in this repo, read these files in order:

1. `projects/agifcore_master/PROJECT_README.md`
2. `projects/agifcore_master/DECISIONS.md`
3. `projects/agifcore_master/CHANGELOG.md`
4. `projects/agifcore_master/01_plan/MASTER_PLAN.md`
5. `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
6. `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`

Working rules:

- Treat `projects/agifcore_master/` as the only canonical source of truth.
- No implementation work starts until the master plan and role rules are read.
- `01_plan/MASTER_PLAN.md` is frozen. Do not change it unless the user explicitly authorizes a master-plan revision.
- Every phase ends only after user review and explicit user approval.
- Governor is the ultimate authority for project truth and acceptance.
- Manager reports to Governor.
- Workers execute bounded tasks and may not claim phase closure.
- Keep AGIFCore local-first, no-LLM, no hidden-model, no cloud-correctness, replayable, reversible, auditable, and fail-closed.
- Keep changes small, organized, and reversible.

