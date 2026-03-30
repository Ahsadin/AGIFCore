# P4-TC-VA-01 Phase 4 Validation Request

## Header

- Task Card ID: `P4-TC-VA-01`
- Phase: `4`
- Title: `Phase 4 Validation Request`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Validation Agent`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `not_assigned`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - audited Phase 4 planning package
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-VA-01_PHASE_4_VALIDATION_REQUEST.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_VALIDATION_REQUEST.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
  - all runtime and verifier files
  - any user verdict file
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`

## Branch And Worktree

- Branch Name: `planned_on_freeze`
- Worktree Path: `planned_on_freeze`
- Rollback Tag Name: `planned_on_freeze`

## Objective

- Goal: prepare the later user review request from the audited Phase 4 planning package.
- Expected Outputs:
  - this task card
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_VALIDATION_REQUEST.md`
- Non-Goals:
  - plan authoring
  - runtime implementation
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

1. Read the audited Phase 4 plan package.
2. Point the user to exact review surfaces.
3. Keep the request strictly below approval language.
4. Hand the request to Program Governor.

## Cross-Checks

- No self-validation by an authoring role.
- Every review path points to a real file.
- No phase approval implied.
