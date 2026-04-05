# Task Card

## Header

- Task Card ID: `P0-TC-VA-01`
- Phase: `0`
- Title: `Phase 0 validation request`
- Status: `closed`
- Issued By: `Program Governor`
- Issued On: `2026-03-29 21:24 CEST`

## Role Assignment

- Active Build Role: `Validation Agent`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `n/a`
- Merge Arbiter Session ID: `n/a`
- Validation Agent Session ID: `separate agent or session required`
- Required Reads:
  - audited Phase 0 artifact set
  - governor verification record
  - `projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-REVIEW-SURFACE-01_PHASE_0_REVIEW_PACKET_PLAN.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-TC-VA-01_PHASE_0_VALIDATION_REQUEST.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_VALIDATION_REQUEST.md`
- Forbidden Files:
  - canonical Phase 0 content files
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_USER_VERDICT.md`
  - `projects/agifcore_master/04_execution/*`
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/04_execution/`

## Branch And Worktree

- Branch Name: `codex/tc-p0-tc-va-01-phase-0-validation-request`
- Worktree Path: `.worktrees/P0-TC-VA-01`
- Rollback Tag Name: `rollback/P0-TC-VA-01/20260329-2124`

## Objective

- Goal: produce the later machine-side validation request for user review of the Phase 0 artifact set.
- Expected Outputs:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_VALIDATION_REQUEST.md`
- Non-Goals:
  - canonical content authoring
  - audit work
  - user verdict writing
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `test -f projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_VALIDATION_REQUEST.md`
  - `rg -n 'project structure|archival statement|source-freeze method' projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_VALIDATION_REQUEST.md`
- Required Build Commands: `none`
- Required Verifier Paths: `none`
- Required Evidence Output Paths: `none`
- Required Demo Path: `direct inspection of the validation request against the real Phase 0 artifacts`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-AUDIT-01_PHASE_0_PLAN_AND_ARTIFACT_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive by default`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined
