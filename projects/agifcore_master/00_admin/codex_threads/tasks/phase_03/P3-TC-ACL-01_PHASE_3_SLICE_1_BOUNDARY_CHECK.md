# Task Card

## Header

- Task Card ID: `P3-TC-ACL-01`
- Phase: `3`
- Title: `Slice 1 Boundary Check`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `pending_spawn`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/03_design/CELL_FAMILIES.md`
  - `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/cell_registry.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/lifecycle_engine.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/cell_contracts.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/tissue_manifests.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_manifest.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_schema_validation.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ACL-01_PHASE_3_SLICE_1_BOUNDARY_CHECK.md`
- Forbidden Files:
  - all `04_execution/*`
  - all `05_testing/*`
  - all `06_outputs/*`
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-acl-01-phase-3-slice-1-boundary-check`
- Worktree Path: `.worktrees/P3-TC-ACL-01`
- Rollback Tag Name: `rollback/P3-TC-ACL-01/20260330-0000`

## Objective

- Goal:
  - confirm that slice-1 cell contracts, tissue manifests, bundle manifest, and schema validation stay inside the approved Phase 3 and Phase 2 boundary
- Expected Outputs:
  - boundary-safe slice-1 structural runtime choices
  - no Phase 4 leakage
  - no bundle-integrity overreach into slice 1
- Non-Goals:
  - architecture redesign
  - new design documents
  - approval or validation
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_cell_contracts.py`
  - `python3 projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_validation.py`
- Required Build Commands:
  - none
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
- Merge Arbiter: `inactive for slice-1 startup`
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

1. check the slice-1 runtime files against the Phase 3 plan and the approved Phase 2 kernel constraints
2. confirm no hidden activation, trust-band, split/merge, or Phase 4 logic appears
3. confirm `bundle_manifest.py` stays a metadata surface and not an integrity engine
4. report any boundary violation back to the Program Governor immediately

## Cross-Checks

- no second lifecycle state machine
- no hidden Phase 4 scope
- no contract values are silently renamed

## Exit Criteria

- slice-1 runtime files are boundary-safe or explicitly blocked

## Handoff Target

`Program Governor`

## No Approval Implied

This boundary check is a control pass only. It does not approve the phase or the slice.
