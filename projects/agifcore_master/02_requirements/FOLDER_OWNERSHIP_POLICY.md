# Folder Ownership Policy

## Purpose

Freeze who is allowed to own which AGIFCore folders so work stays organized and overlap stays controlled.

## Ownership Map

- `00_admin/` -> Program Governor, Validation Agent, Release & Evidence Lead
- `01_plan/` -> Program Governor, Constitution Keeper, Source Cartographer
- `02_requirements/` -> Constitution Keeper
- `03_design/` -> Architecture & Contract Lead
- `04_execution/` -> current active build pod and Merge Arbiter only
- `05_testing/` -> Test & Replay Lead
- `06_outputs/` -> Test & Replay Lead and Release & Evidence Lead
- `07_assets/` -> Product & Sandbox Pod Lead
- `08_logs/` -> Program Governor and explicitly approved utility helpers

## Hard Rules

- No role writes outside its owned folders unless the Program Governor issues an explicit task card.
- No agent may use folder ownership as permission to self-approve work.
- The active build pod may edit only the scoped files named in the task card.
- Merge Arbiter may integrate cleared patches in `04_execution/` but may not rewrite design or requirements on its own.
- Validation Agent reads code, tests, demos, and evidence, but does not implement production behavior.
- Release & Evidence Lead may package outputs and public materials, but may not change technical behavior.

## Default Parallelism Rule

One active build pod is the default.

More parallel build pods require:

- explicit Program Governor approval
- clear disjoint write scopes
- evidence that the added coordination cost is worth it

## Freeze Rule

This ownership map is frozen until the user explicitly approves a revision.
