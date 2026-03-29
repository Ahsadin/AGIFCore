# Task Card

## Header

- Task Card ID: `P1-TC-TRL-01`
- Phase: `1`
- Title: `Phase 1 validation protocol planning`
- Status: `closed`
- Issued By: `Program Governor`
- Issued On: `2026-03-29 22:40 CEST`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Program Governor`, `Anti-Shortcut Auditor`, `Validation Agent`
- Allowed Models: `gpt-5.4-mini`, `gpt-5.4`
- Build Pod Agent Session ID: `separate agent or session required`
- Merge Arbiter Session ID: `n/a`
- Validation Agent Session ID: `separate agent or session required`
- Required Reads:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/00_admin/VALIDATION_REQUEST_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/GOVERNOR_VERIFICATION_RECORD_TEMPLATE.md`
  - admin templates and closure-gate sections

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/P1-TC-TRL-01_PHASE_1_VALIDATION_PROTOCOL.md`
- Forbidden Files:
  - `projects/agifcore_master/02_requirements/*`
  - `projects/agifcore_master/03_design/*`
  - provenance files
  - `projects/agifcore_master/04_execution/*`
- Allowed Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/`
- Forbidden Folders:
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/04_execution/`

## Branch And Worktree

- Branch Name: `codex/tc-p1-tc-trl-01-phase-1-validation-protocol`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P1-TC-TRL-01`
- Rollback Tag Name: `rollback/P1-TC-TRL-01/20260329-2240`

## Objective

- Goal: author the Phase 1 validation-protocol lane after Workstreams 1-4 have first-pass outputs.
- Expected Outputs:
  - substantive `VALIDATION_PROTOCOL.md` aligned to Phase 1 closure
- Non-Goals:
  - requirement authoring
  - design authoring
  - provenance authoring
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `test -f projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- Required Build Commands: `none`
- Required Verifier Paths: `none`
- Required Evidence Output Paths: `none`
- Required Demo Path: `direct inspection of the revised validation protocol`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/P1-AUDIT-01_PHASE_1_ARTIFACT_COVERAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_01_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_01_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_01_USER_VERDICT.md`
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
