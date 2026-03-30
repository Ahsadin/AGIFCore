# Task Card

## Header

- Task Card ID: `P3-TC-TRL-04`
- Phase: `3`
- Title: `Slice 4 Integrity And Orchestration Verifiers`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Kernel Pod Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `pending_spawn`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - current Slice 1, Slice 2, and Slice 3 evidence files in your lane

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_tissue_orchestration.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_integrity.py`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_tissue_orchestration_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_integrity_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`
- Forbidden Files:
  - all runtime files outside read-only inspection
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/`
  - all Phase 3 closeout artifacts
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/07_assets/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-trl-04-phase-3-slice-4-integrity-and-orchestration-verifiers`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04`
- Rollback Tag Name: `rollback/P3-TC-TRL-04/20260330-0000`

## Objective

- Goal:
  - verify the missing tissue-orchestration surface and the new bundle-integrity runtime, then refresh honest evidence
- Expected Outputs:
  - passing tissue orchestration verifier on the integrated package
  - passing bundle integrity verifier on the integrated package
  - machine-readable Slice 4 reports
  - refreshed evidence manifest that references all current real Phase 3 report files
- Non-Goals:
  - demo bundle authoring
  - final phase review surfaces
  - Phase 4 work
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
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

1. reuse the self-contained repo-relative import strategy from earlier slices
2. verify tissue membership and orchestration constraints against the actual runtime API
3. verify bundle-integrity happy path and fail-closed negative cases against the actual runtime API
4. refresh the shared evidence manifest only from real report files

## Cross-Checks

- no fake passing reports in a non-integrated lane
- no demo authoring here
- no bundle-integrity pass without manifest and inventory checks

## Exit Criteria

- both Slice 4 verifiers exist and are runnable on an integrated package
- Slice 4 report files exist
- the evidence manifest remains honest

## Handoff Target

`Program Governor`

## No Approval Implied

Passing the Slice 4 verifiers does not approve Phase 3 and does not authorize final closeout automatically.
