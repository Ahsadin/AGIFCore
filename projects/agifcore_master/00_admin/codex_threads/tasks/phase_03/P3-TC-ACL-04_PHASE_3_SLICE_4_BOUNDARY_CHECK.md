# Task Card

## Header

- Task Card ID: `P3-TC-ACL-04`
- Phase: `3`
- Title: `Slice 4 Boundary Check`
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
  - `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_integrity_checks.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_tissue_orchestration.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_integrity.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ACL-04_PHASE_3_SLICE_4_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-NOTE-ACL-04_PHASE_3_SLICE_4_BOUNDARY_NOTES.md`
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

- Branch Name: `codex/tc-p3-tc-acl-04-phase-3-slice-4-boundary-check`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-ACL-04`
- Rollback Tag Name: `rollback/P3-TC-ACL-04/20260330-0000`

## Objective

- Goal:
  - confirm Slice 4 bundle integrity and orchestration verification stay inside the approved Phase 3 and Phase 2 boundary
- Expected Outputs:
  - no sandbox substitution for integrity
  - no Phase 4 leakage
  - no hidden builder correctness privilege
- Non-Goals:
  - runtime authoring
  - verifier authoring
  - approval or validation
- Inherited Lineage Touched: `no`
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
- Required Demo Path:
  - `n/a for Slice 4`

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

## Work Method

1. check bundle-integrity runtime against bundle-schema and product-runtime boundary
2. confirm integrity checks are fail-closed and not delegated to sandbox
3. confirm tissue orchestration verification stays structural and Phase-3-only
4. report any boundary violation back to the Program Governor immediately

## Cross-Checks

- no sandbox implementation
- no Phase 4 scope
- no hidden cloud or builder privilege
- no integrity logic hidden inside unrelated modules

## Exit Criteria

- Slice 4 runtime and verifier files are boundary-safe or explicitly blocked

## Handoff Target

`Program Governor`

## No Approval Implied

This boundary check is a control pass only. It does not approve the phase or the slice.
