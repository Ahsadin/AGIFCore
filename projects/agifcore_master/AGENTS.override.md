# AGIFCore Project Rules

This override applies to everything under `projects/agifcore_master/`.

Read these files before any work:

1. `PROJECT_README.md`
2. `DECISIONS.md`
3. `CHANGELOG.md`
4. `01_plan/MASTER_PLAN.md`
5. `02_requirements/ROLE_AUTHORITY_RULES.md`
6. `02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
7. `01_plan/VALIDATION_PROTOCOL.md`

Rules:

- `01_plan/MASTER_PLAN.md` is frozen until the user explicitly approves a revision.
- Every task must align to the frozen master plan and the active phase plan.
- Every phase closes only after a user-reviewed demo and explicit user approval.
- Governor is the ultimate authority.
- Manager reports to Governor.
- Workers report through the assigned manager path and must stay within their scope.
- Workers report results to the manager, the manager reports to the governor, and the governor is the only role that may ask the user for final phase review.
- Governor must independently inspect code, rerun checks, and verify demos. Report text alone is not enough.
- Manager may use `2-5+` workers depending on the task, but the reporting chain may not change.
