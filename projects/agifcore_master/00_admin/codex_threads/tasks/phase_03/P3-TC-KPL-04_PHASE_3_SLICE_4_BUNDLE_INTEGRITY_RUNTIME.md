# Task Card

## Header

- Task Card ID: `P3-TC-KPL-04`
- Phase: `3`
- Title: `Slice 4 Bundle Integrity Runtime`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Kernel Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`, `Test & Replay Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `pending_spawn`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_manifest.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_schema_validation.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_integrity_checks.py`
- Forbidden Files:
  - all other runtime files
  - all `05_testing/*`
  - all `06_outputs/*`
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/`
- Forbidden Folders:
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-kpl-04-phase-3-slice-4-bundle-integrity-runtime`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-KPL-04`
- Rollback Tag Name: `rollback/P3-TC-KPL-04/20260330-0000`

## Objective

- Goal:
  - implement only the Slice 4 runtime surface for bundle integrity checks
- Expected Outputs:
  - explicit bundle-integrity runtime that validates inventories and hashes and fails closed
- Non-Goals:
  - schema validation reimplementation
  - sandbox implementation
  - Phase 4 work
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_integrity.py`
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_integrity.py`
- Required Evidence Output Paths:
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

1. port the strongest bundle-integrity substrate without importing sandbox or product-runtime execution
2. keep integrity checks fail-closed and inspectable
3. validate file inventory, digest expectations, and manifest linkage
4. stop at Slice 4 only

## Cross-Checks

- no schema-validation rewrite
- no sandbox implementation
- no Phase 4 memory or Phase 5 graph logic
- no cloud or hidden correctness path

## Exit Criteria

- `bundle_integrity_checks.py` exists
- Slice 4 verifiers pass on the integrated package
- Slice 4 evidence files are produced

## Handoff Target

`Test & Replay Lead` then `Program Governor`

## No Approval Implied

Completing Slice 4 runtime code does not approve Phase 3, does not merge Slice 4, and does not authorize Phase 4.
