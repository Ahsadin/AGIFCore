# Task Card

## Header

- Task Card ID: `P3-TC-PG-05`
- Phase: `3`
- Title: `Phase 3 Review Package`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Release & Evidence Lead`, `Anti-Shortcut Auditor`, `Validation Agent`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `n/a`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `pending_spawn`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - committed Slice 1 to Slice 4 outputs on the MA-04 lane

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-PG-05_PHASE_3_REVIEW_PACKAGE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-REL-04_PHASE_3_DEMO_BUNDLE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ASA-05_PHASE_3_FINAL_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-VA-04_PHASE_3_VALIDATION_REQUEST.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_GOVERNOR_VERIFICATION_RECORD.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - any user verdict file
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/07_assets/`
  - `projects/agifcore_master/08_logs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-pg-05-phase-3-review-package`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-PG-05`
- Rollback Tag Name: `rollback/P3-TC-PG-05/20260330-0000`

## Objective

- Goal:
  - prepare the final Phase 3 review package without changing phase truth or asking for approval inside the repo files
- Expected Outputs:
  - governor verification record
  - final demo bundle task-card set
  - final package audit task-card set
  - validation request task-card set
- Non-Goals:
  - phase approval
  - phase-truth mutation
  - Phase 4 work
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - all Phase 3 verifiers already on disk and rerun by Governor as needed
- Required Build Commands:
  - none
- Required Verifier Paths:
  - complete `verify_phase_03_*` family currently present on the MA-04 lane
- Required Evidence Output Paths:
  - complete `phase_03_*_report.json` family and `phase_03_evidence_manifest.json`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-07_PHASE_3_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `n/a`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_VALIDATION_REQUEST.md`
- User Verdict Path:
  - `deferred until user review`
- Additional Human Demo Checkpoint Path:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_demo_index.md`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- governor verification record is complete
- validation request exists
- phase truth remains open

## Governor Method

1. define final demo, audit, and validation lanes
2. wait for the final demo bundle and final audit to complete
3. independently verify the final package
4. hand the package to Validation Agent
5. stop at user review

## No Approval Implied

This task card prepares the review package only. It does not approve Phase 3 and does not authorize Phase 4.
