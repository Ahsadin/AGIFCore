# AGIFCore Project Rules

This override applies to everything under `projects/agifcore_master/`.

Read these files before any work:

1. `PROJECT_README.md`
2. `DECISIONS.md`
3. `CHANGELOG.md`
4. `01_plan/MASTER_PLAN.md`
5. `02_requirements/ROLE_AUTHORITY_RULES.md`
6. `02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
7. `02_requirements/FOLDER_OWNERSHIP_POLICY.md`
8. `02_requirements/MODEL_TIER_POLICY.md`
9. `01_plan/VALIDATION_PROTOCOL.md`

Rules:

- `01_plan/MASTER_PLAN.md` is frozen until the user explicitly approves a revision.
- Every task must align to the frozen master plan and the active phase plan.
- Every phase closes only after a user-reviewed demo and explicit user approval.
- AGIFCore uses a governed build machine, not a generic manager/worker chain.
- Program Governor is the ultimate agent authority below the user.
- Specialized planning, build, test, audit, merge, validation, and release roles must follow the frozen role manifest.
- Build agents are outside the AGIFCore runtime and may never be treated as runtime truth.
- No agent may both write and validate the same artifact.
- Program Governor must independently inspect code, rerun checks, and verify demos. Report text alone is not enough.
- Program Governor is the only role that may ask the user for final phase review.
- One active build pod is the default unless the governor explicitly authorizes more parallel build work.
