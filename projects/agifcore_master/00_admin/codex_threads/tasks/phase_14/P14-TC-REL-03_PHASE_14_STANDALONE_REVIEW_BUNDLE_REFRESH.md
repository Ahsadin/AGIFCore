# P14-TC-REL-03 Phase 14 Standalone Review Bundle Refresh

## Header

- Task Card ID: `P14-TC-REL-03`
- Phase: `14`
- Title: `Phase 14 Standalone Review Bundle Refresh`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Test & Replay Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `separate_release_thread_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_VALIDATION_REQUEST.md`
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_review_bundle/`
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_review_bundle.zip`
- Forbidden Files:
  - `projects/agifcore_master/04_execution/*`
  - `projects/agifcore_master/05_testing/*`
  - all Phase 15 and later artifacts

## Branch And Worktree

- Branch Name: `codex/tc-p13-tc-pg-03-phase-13-closeout`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P14-TC-REL-03/<yyyymmdd-hhmm>`

## Objective

- Goal: refresh the standalone Phase 14 review bundle so the strengthened manifest package is easy to inspect externally.
- Expected Outputs:
  - refreshed standalone review bundle folder and zip
- Non-Goals:
  - runtime authorship
  - verifier authorship
  - approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - bundle rerun commands if asked by `Program Governor`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - all copied Phase 14 verifier files
- Required Evidence Output Paths:
  - all copied Phase 14 evidence files
- Required Demo Path:
  - all copied Phase 14 demo files

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-AUDIT-01_PHASE_14_FINAL_PACKAGE_AUDIT_REPORT.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_USER_VERDICT.md`

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

1. Keep review files easy to find.
2. Copy only real outputs.
3. Do not imply approval.

## Cross-Checks

- No missing review file.
- No stale review packet.
- No Phase 15 leak.
