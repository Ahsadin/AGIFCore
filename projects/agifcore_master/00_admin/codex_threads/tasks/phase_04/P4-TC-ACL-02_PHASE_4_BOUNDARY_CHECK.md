# P4-TC-ACL-02 Phase 4 Boundary Check

## Header

- Task Card ID: `P4-TC-ACL-02`
- Phase: `4`
- Title: `Phase 4 Boundary Check`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - approved Phase 2 and Phase 3 runtime surfaces

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-ACL-02_PHASE_4_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-NOTE-ACL-02_PHASE_4_BOUNDARY_NOTES.md`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - all Phase 5+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p4-tc-acl-02-phase-4-boundary-check`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-ACL-02`
- Rollback Tag Name: `rollback/P4-TC-ACL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: review the built Phase 4 package against Phase 2 kernel seams, Phase 3 structure seams, and the locked Phase 4 boundaries.
- Expected Outputs:
  - this task card
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-NOTE-ACL-02_PHASE_4_BOUNDARY_NOTES.md`
- Non-Goals:
  - runtime authoring
  - verifier authoring
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

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-02_PHASE_4_FINAL_PACKAGE_AUDIT_REPORT.md`
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

1. Review the built runtime surfaces against the Phase 4 memory-plane boundary rules.
2. Check that rollback-safe updates really stay anchored to Phase 2 rollback and replay seams.
3. Check that no Phase 5 graph logic or Phase 7 conversation logic leaked into the package.
4. Write a concrete boundary note for Program Governor and later audit.

## Cross-Checks

- No giant-store shortcut.
- No Phase 5 drift.
- No Phase 7 drift.
- No approval implied.
