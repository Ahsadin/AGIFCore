# P5-TC-ACL-01 Phase 5 Boundary Check

## Header

- Task Card ID: `P5-TC-ACL-01`
- Phase: `5`
- Title: `Phase 5 Boundary Check`
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
  - `projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/SKILL_GRAPH_MODEL.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - approved Phase 2, 3, and 4 runtime surfaces

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-ACL-01_PHASE_5_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-NOTE-ACL-01_PHASE_5_BOUNDARY_NOTES.md`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p5-tc-acl-01-phase-5-boundary-check`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P5-TC-ACL-01`
- Rollback Tag Name: `rollback/P5-TC-ACL-01/<yyyymmdd-hhmm>`

## Objective

- Goal: review the built Phase 5 package against the locked graph boundaries, the approved Phase 4 memory-plane interfaces, and the forbidden Phase 6 and 7 leakage list.
- Expected Outputs:
  - this task card
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-NOTE-ACL-01_PHASE_5_BOUNDARY_NOTES.md`
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

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-AUDIT-01_PHASE_5_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_USER_VERDICT.md`
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

1. Review the built runtime surfaces against the Phase 5 graph boundary rules.
2. Check that graph logic consumes Phase 4 exports read-only and does not mutate memory-plane stores directly.
3. Check that no Phase 6 world-model behavior or Phase 7 conversation behavior leaked into the package.
4. Write a concrete boundary note for Program Governor and later audit.

## Cross-Checks

- No one giant graph shortcut.
- No Phase 4 absorption.
- No Phase 6 drift.
- No Phase 7 drift.
- No approval implied.
