# Task Card

## Header

- Task Card ID: `P3-TC-PG-06`
- Phase: `3`
- Title: `Phase 3 Closeout`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Merge Arbiter`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `n/a`
- Merge Arbiter Session ID: `pending_spawn`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_VALIDATION_REQUEST.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-07_PHASE_3_FINAL_PACKAGE_AUDIT_REPORT.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-PG-06_PHASE_3_CLOSEOUT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_USER_VERDICT.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 4+ artifacts
  - all Phase 3 runtime, testing, evidence, and demo files
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
  - `projects/agifcore_master/01_plan/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-pg-06-phase-3-closeout`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P3-TC-PG-06/20260330-0000`

## Objective

- Goal:
  - record the explicit user approval, update the live Phase 3 gate truth, and stop without starting Phase 4
- Expected Outputs:
  - Phase 3 user verdict record
  - updated `PHASE_INDEX.md`
  - updated `PHASE_GATE_CHECKLIST.md`
  - truthful Decision and Changelog entries
- Non-Goals:
  - Phase 4 planning
  - further Phase 3 implementation
  - rewriting review artifacts
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none beyond confirming the required audit, governor verification, validation request, and user verdict chain exists
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_demo_index.md`

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
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path:
  - `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `Merge Arbiter`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- explicit user verdict is recorded
- live phase-truth files show Phase 3 `approved`
- decision and changelog entries are truthful
- Phase 4 remains not started
- rollback path is defined

## Work Method

1. ensure the reviewed Phase 3 artifacts are integrated onto the closeout branch
2. record the explicit user verdict as `approved`
3. update the live phase-truth files and logs
4. stop after the closeout commit

## Cross-Checks

- no approval is recorded without the full closure chain already on disk
- no Phase 4 artifact is touched
- no Phase 3 runtime artifact is rewritten here

## Exit Criteria

- Phase 3 is marked `approved` in the live phase-truth files
- the user verdict is on disk
- the closeout commit exists

## Handoff Target

`User`

## No Approval Implied

This task card records the user approval that already happened. It does not start Phase 4.
