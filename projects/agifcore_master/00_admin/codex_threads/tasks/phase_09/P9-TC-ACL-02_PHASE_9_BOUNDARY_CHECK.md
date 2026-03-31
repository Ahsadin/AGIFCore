# P9-TC-ACL-02 Phase 9 Boundary Check

## Header

- Task Card ID: `P9-TC-ACL-02`
- Phase: `9`
- Title: `Phase 9 Boundary Check`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `019d44ac-9867-7213-ba84-4ec33ee11d6f`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/`
  - later `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-ACL-02_PHASE_9_BOUNDARY_CHECK.md`
- Forbidden Files:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p9-tc-pg-02-phase-9-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P9-TC-ACL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: independently confirm that the built Phase 9 runtime stays inside the approved boundaries and overlay-contract rules.
- Expected Outputs:
  - this boundary-check record with pass/fail findings
- Non-Goals:
  - fixing code directly
  - validating the final package
  - approving the phase
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `n/a`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `n/a`
- Required Evidence Output Paths:
  - `n/a`
- Required Demo Path:
  - `n/a`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-AUDIT-01_PHASE_9_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-ACL-02_PHASE_9_BOUNDARY_CHECK.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_USER_VERDICT.md`
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

1. Inspect the implemented Phase 9 runtime directly.
2. Confirm it reads Phase 7 and Phase 8 inputs without mutating them.
3. Confirm it does not smuggle in Phase 10 or Phase 11 behavior.
4. Confirm analogy and composition traces are explicit and bounded.
5. Record clear pass/fail findings only.

## Cross-Checks

- No direct code edits.
- No approval language.
- No final validation claim.
