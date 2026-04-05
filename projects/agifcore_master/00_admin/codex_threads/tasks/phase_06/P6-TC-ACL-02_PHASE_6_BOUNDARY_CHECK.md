# P6-TC-ACL-02 Phase 6 Boundary Check

## Header

- Task Card ID: `P6-TC-ACL-02`
- Phase: `6`
- Title: `Phase 6 Boundary Check`
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
  - `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - approved Phase 4 and Phase 5 runtime surfaces

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-ACL-02_PHASE_6_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-NOTE-ACL-01_PHASE_6_BOUNDARY_NOTES.md`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p6-tc-acl-02-phase-6-boundary-check`
- Worktree Path: `.worktrees/P6-TC-ACL-02`
- Rollback Tag Name: `rollback/P6-TC-ACL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: review the built Phase 6 package against the locked world-model and simulator boundaries, approved Phase 4 and Phase 5 read-only interfaces, and the forbidden Phase 7 and 8 leakage list.
- Expected Outputs:
  - this task card
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-NOTE-ACL-01_PHASE_6_BOUNDARY_NOTES.md`
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

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-AUDIT-01_PHASE_6_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_USER_VERDICT.md`
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

1. Review the built runtime surfaces against the Phase 6 world-model and simulator boundary rules.
2. Check that Phase 6 consumes Phase 4 and Phase 5 exports read-only and does not mutate memory or graph stores directly.
3. Check that no Phase 7 conversation behavior or Phase 8 world-awareness behavior leaked into the package.
4. Write a concrete boundary note for Program Governor and later audit.

## Cross-Checks

- No one giant mixed state object.
- No Phase 4 absorption.
- No Phase 5 absorption.
- No Phase 7 drift.
- No Phase 8 drift.
- No approval implied.
