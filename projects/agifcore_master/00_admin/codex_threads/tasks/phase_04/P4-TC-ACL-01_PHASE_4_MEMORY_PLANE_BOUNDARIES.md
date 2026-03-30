# P4-TC-ACL-01 Phase 4 Memory Plane Boundaries

## Header

- Task Card ID: `P4-TC-ACL-01`
- Phase: `4`
- Title: `Phase 4 Memory Plane Boundaries`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles: `Source Cartographer`, `Memory & Graph Pod Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `not_assigned`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-ACL-01_PHASE_4_MEMORY_PLANE_BOUNDARIES.md`
- Forbidden Files:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 5+ artifacts
- Allowed Folders:
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

- Goal: freeze the distinct boundaries, leak rules, and allowed transitions for all Phase 4 memory planes.
- Expected Outputs:
  - this task card
- Non-Goals:
  - runtime implementation
  - graph implementation
  - conversation implementation
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

1. Define working, episodic, semantic, procedural, and continuity planes as distinct surfaces.
2. Define correction, promotion, compression, forgetting, retirement, and review boundaries.
3. Define explicit forbidden leak paths.
4. Keep Phase 4 above approved kernel and structure seams and below Phase 5 and 7.

## Cross-Checks

- No giant untyped store.
- No Phase 5 graph logic in Phase 4.
- No Phase 7 conversation behavior in Phase 4.
