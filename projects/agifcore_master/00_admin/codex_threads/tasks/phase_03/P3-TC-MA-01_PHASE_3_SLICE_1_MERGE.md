# Task Card

## Header

- Task Card ID: `P3-TC-MA-01`
- Phase: `3`
- Title: `Slice 1 Integration Merge`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Merge Arbiter`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `pending_spawn`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-PG-01_PHASE_3_GOVERNOR_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ASA-01_PHASE_3_SLICE_1_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-KPL-01_PHASE_3_SLICE_1_CELL_TISSUES_AND_BUNDLE_SCHEMA.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-TRL-01_PHASE_3_SLICE_1_CONTRACT_AND_BUNDLE_VERIFIERS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ACL-01_PHASE_3_SLICE_1_BOUNDARY_CHECK.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/cell_contracts.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/tissue_manifests.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_manifest.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_schema_validation.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/schemas/phase_03_cell_contract.schema.json`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/schemas/phase_03_tissue_manifest.schema.json`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/schemas/phase_03_bundle_manifest.schema.json`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_cell_contracts.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_validation.py`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_cell_contracts_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_validation_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_demo_index.md`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_bundle_validation_demo.md`
- Forbidden Files:
  - all Phase 4+ artifacts
  - any slice-2 file
  - any task-card file outside this merge lane unless needed for audit records
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/03_design/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-ma-01-phase-3-slice-1-merge`
- Worktree Path: `.worktrees/P3-TC-MA-01`
- Rollback Tag Name: `rollback/P3-TC-MA-01/20260330-0000`

## Objective

- Goal:
  - integrate the three cleared slice-1 role-lane commits into one clean merge lane
- Expected Outputs:
  - a single integrated slice-1 branch state
  - no content drift beyond the cleared patches
- Non-Goals:
  - new feature work
  - slice 2
  - Phase 4

## Verification

- Required Test Commands:
  - later Governor rerun of the two slice-1 verifiers after merge
- Required Build Commands:
  - none beyond integration merges
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_cell_contracts.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_validation.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-01_PHASE_3_SLICE_1_AUDIT_REPORT.md`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_GOVERNOR_VERIFICATION_RECORD.md`

## Work Method

1. merge the cleared KPL, TRL, and ACL slice-1 branches into this lane
2. keep the integration limited to the already-cleared slice-1 files
3. do not rename or broaden content unless required for merge hygiene
4. hand the integrated lane back to the Program Governor for direct rerun of the verifiers

## Cross-Checks

- no slice-2 files enter the lane
- no Phase 4 files enter the lane
- no content change beyond integration hygiene

## Exit Criteria

- the integrated lane contains the cleared slice-1 runtime, test, evidence, and boundary-note files
- Governor can rerun both verifiers from the integrated lane

## Handoff Target

`Program Governor`

## No Approval Implied

This task card only authorizes slice-1 integration. It does not approve Phase 3 and does not authorize slice 2.
