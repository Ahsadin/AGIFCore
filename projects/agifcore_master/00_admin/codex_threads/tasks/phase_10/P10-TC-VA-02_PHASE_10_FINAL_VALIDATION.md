# P10-TC-VA-02 Phase 10 Final Validation

## Header

- Task Card ID: `P10-TC-VA-02`
- Phase: `10`
- Title: `Phase 10 Final Validation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Validation Agent`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `local_validation_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `local_validation_thread`
- Required Reads:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-01_PHASE_10_FINAL_PACKAGE_AUDIT_REPORT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-02_PHASE_10_DANGER_ZONE_AUDIT_REPORT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_GOVERNOR_VERIFICATION_RECORD.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-VA-02_PHASE_10_FINAL_VALIDATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_VALIDATION_REQUEST.md`
- Forbidden Files:
  - any runtime, verifier, or output file
  - all Phase 11 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p10-tc-pg-02-phase-10-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P10-TC-VA-02/<yyyymmdd-hhmm>`

## Objective

- Goal: validate the final Phase 10 package and prepare the user review request without implying approval.
- Expected Outputs:
  - final validation task card
  - validation request handoff
- Non-Goals:
  - authoring runtime or verifier logic
  - phase approval

## Verification

- Required Test Commands:
  - inspect the already-rerun verifier family and Governor verification record
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-01_PHASE_10_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-02_PHASE_10_DANGER_ZONE_AUDIT_REPORT.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_USER_VERDICT.md`
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

1. Confirm the full package is present and consistent.
2. Confirm the extra danger-zone audit exists and is not bypassed.
3. Draft the exact user review path without implying approval.

## Cross-Checks

- No author and validator role collision.
- No missing review surface.
- No implied approval.
