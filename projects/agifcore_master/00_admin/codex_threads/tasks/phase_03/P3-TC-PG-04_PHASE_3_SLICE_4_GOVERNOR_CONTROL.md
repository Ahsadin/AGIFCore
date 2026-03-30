# Task Card

## Header

- Task Card ID: `P3-TC-PG-04`
- Phase: `3`
- Title: `Phase 3 Slice 4 Governor Control`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Kernel Pod Lead`, `Architecture & Contract Lead`, `Test & Replay Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `n/a`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - committed Slice 3 outputs on the MA-03 lane

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-PG-04_PHASE_3_SLICE_4_GOVERNOR_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-KPL-04_PHASE_3_SLICE_4_BUNDLE_INTEGRITY_RUNTIME.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-TRL-04_PHASE_3_SLICE_4_INTEGRITY_AND_ORCHESTRATION_VERIFIERS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ACL-04_PHASE_3_SLICE_4_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ASA-04_PHASE_3_SLICE_4_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-MA-04_PHASE_3_SLICE_4_MERGE.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 4+ artifacts
  - any Phase 3 final validation request artifact
  - any Phase 3 user verdict artifact
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
- Forbidden Folders:
  - `projects/agifcore_master/07_assets/`
  - `projects/agifcore_master/08_logs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-pg-04-phase-3-slice-4-governor-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-PG-04`
- Rollback Tag Name: `rollback/P3-TC-PG-04/20260330-0000`

## Objective

- Goal:
  - keep Slice 4 bounded to bundle integrity checks plus the missing tissue-orchestration and bundle-integrity verifier surfaces
  - open the Slice 4 task-card set before any Slice 4 code lands
  - stop after Slice 4 audit and integration, without starting Phase 4
- Expected Outputs:
  - governed Slice 4 task-card set exists
  - Slice 4 runtime, verifiers, and evidence files exist
  - Slice 4 ends at audited integrated status
- Non-Goals:
  - final Phase 3 approval
  - Phase 4 work
  - public release work
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_tissue_orchestration.py`
  - `python3 projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_integrity.py`
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_tissue_orchestration.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_integrity.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_tissue_orchestration_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_integrity_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`
- Required Demo Path:
  - `n/a for Slice 4 build slice`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-06_PHASE_3_SLICE_4_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `n/a`
- Governor Verification Record Path:
  - `deferred until later full-phase verification`
- Validation Request Path:
  - `deferred until later phase closeout`
- User Verdict Path:
  - `deferred until later phase closeout`
- Additional Human Demo Checkpoint Path:
  - `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive until Slice 4 clears audit`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- rollback path is defined
- Phase 4 did not start in this lane

## Governor Method

1. branch Slice 4 from the committed Slice 3 merge lane
2. create task cards before any Slice 4 runtime or verifier changes
3. keep one active build pod by default
4. keep runtime scope limited to `bundle_integrity_checks.py`
5. keep verifier scope limited to tissue orchestration and bundle integrity
6. stop after Slice 4 audit and integration

## No Approval Implied

This task card governs Slice 4 only. It does not approve Phase 3, does not close Phase 3, and does not authorize Phase 4.
