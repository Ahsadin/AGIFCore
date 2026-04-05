# P10-TC-ASA-02 Phase 10 Final Audit

## Header

- Task Card ID: `P10-TC-ASA-02`
- Phase: `10`
- Title: `Phase 10 Final Audit`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Anti-Shortcut Auditor`
- Supporting Roles: `Constitution Keeper`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `local_audit_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/`
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-ASA-02_PHASE_10_FINAL_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-01_PHASE_10_FINAL_PACKAGE_AUDIT_REPORT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-02_PHASE_10_DANGER_ZONE_AUDIT_REPORT.md`
- Forbidden Files:
  - any runtime, verifier, or output file
  - all Phase 11 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p10-tc-pg-02-phase-10-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P10-TC-ASA-02/<yyyymmdd-hhmm>`

## Objective

- Goal: audit the full Phase 10 package for fake completeness, danger-zone drift, and unverifiable demos.
- Expected Outputs:
  - standard final audit report
  - extra danger-zone audit report
- Non-Goals:
  - fixing implementation
  - phase approval

## Verification

- Required Test Commands:
  - inspect already-generated verifier and demo outputs
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

1. Audit the runtime package, verifier family, evidence manifest, and demo bundle directly.
2. Check for unsupported self-assertion, empty skepticism, prose-only diagnosis, and hidden Phase 11 or 12 drift.
3. Write one standard package audit and one extra danger-zone audit.

## Cross-Checks

- No rewriting the runtime during audit.
- No self-improvement or structural-growth semantics may pass as Phase 10.
- No demo claim may stand without evidence linkage.
