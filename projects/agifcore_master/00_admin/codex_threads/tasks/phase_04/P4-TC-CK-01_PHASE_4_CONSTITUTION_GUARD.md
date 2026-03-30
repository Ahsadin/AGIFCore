# P4-TC-CK-01 Phase 4 Constitution Guard

## Header

- Task Card ID: `P4-TC-CK-01`
- Phase: `4`
- Title: `Phase 4 Constitution Guard`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Constitution Keeper`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `not_assigned`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/PHASE_APPROVAL_RULES.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-CK-01_PHASE_4_CONSTITUTION_GUARD.md`
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

- Goal: guard Phase 4 against constitution drift, hidden-memory shortcuts, and later-phase leakage.
- Expected Outputs:
  - this task card
- Non-Goals:
  - runtime implementation
  - verifier implementation
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
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

1. Review the Phase 4 plan against constitution, non-negotiables, and approval rules.
2. Check that Phase 4 does not absorb graph implementation or conversation behavior.
3. Check that correction, review, and rollback-safe update claims stay governed and auditable.
4. Report any drift back to Program Governor.

## Cross-Checks

- No hidden autonomy path.
- No one-store shortcut accepted.
- No approval language.
