# P4-TC-PG-01 Phase 4 Governor Control

## Header

- Task Card ID: `P4-TC-PG-01`
- Phase: `4`
- Title: `Phase 4 Governor Control`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Constitution Keeper`, `Architecture & Contract Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `not_assigned`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-PG-01_PHASE_4_GOVERNOR_CONTROL.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 5+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `planned_on_freeze`
- Worktree Path: `planned_on_freeze`
- Rollback Tag Name: `planned_on_freeze`

## Objective

- Goal: materialize the canonical Phase 4 planning artifact and keep phase truth aligned to the current approved baseline.
- Expected Outputs:
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
  - this task card
- Non-Goals:
  - runtime implementation
  - verifier implementation
  - evidence generation
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands: `n/a`
- Required Build Commands: `n/a`
- Required Verifier Paths: `n/a`
- Required Evidence Output Paths: `n/a`
- Required Demo Path: `n/a`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-01_PHASE_4_PLAN_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `Merge Arbiter`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined

## Work Method

1. Verify that Phase 3 remains `approved` and Phase 4 remains `open`.
2. Materialize the canonical Phase 4 planning artifact.
3. Keep the later default Phase 4 build pod frozen as `Memory & Graph Pod Lead`.
4. Keep the plan strictly below Phase 5 and above the approved Phase 2 and 3 baselines.

## Cross-Checks

- No Phase 5 graph implementation is implied.
- No Phase 7 conversation behavior is implied.
- No phase approval is implied.
