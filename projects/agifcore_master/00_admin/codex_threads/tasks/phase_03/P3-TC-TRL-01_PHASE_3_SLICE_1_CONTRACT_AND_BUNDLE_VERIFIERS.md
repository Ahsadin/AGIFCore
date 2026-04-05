# Task Card

## Header

- Task Card ID: `P3-TC-TRL-01`
- Phase: `3`
- Title: `Slice 1 Contract And Bundle Verifiers`
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
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/cell_contracts.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/tissue_manifests.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_manifest.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_schema_validation.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_cell_contracts.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_validation.py`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_cell_contracts_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_validation_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_demo_index.md`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_bundle_validation_demo.md`
- Forbidden Files:
  - all runtime files outside read-only inspection
  - all Phase 3 closeout artifacts
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/07_assets/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-trl-01-phase-3-slice-1-contract-and-bundle-verifiers`
- Worktree Path: `.worktrees/P3-TC-TRL-01`
- Rollback Tag Name: `rollback/P3-TC-TRL-01/20260330-0000`

## Objective

- Goal:
  - verify slice-1 cell-contract and bundle-schema behavior and produce starter evidence plus demo outputs
- Expected Outputs:
  - passing cell-contract verifier
  - passing bundle-validation verifier
  - machine-readable evidence manifest and two reports
  - human-inspectable demo index and bundle-validation demo
- Non-Goals:
  - tissue orchestration verifier
  - split/merge verifier
  - bundle integrity verifier
  - final phase review surfaces
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
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
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_cell_contracts_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_validation_report.json`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_bundle_validation_demo.md`

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

1. import the slice-1 runtime modules directly from the execution folder
2. assert valid and invalid contract cases
3. assert valid and invalid bundle-manifest and schema-linkage cases
4. write machine-readable evidence
5. write one slice-1 demo index and one bundle-validation demo
6. stop at slice 1 only

## Cross-Checks

- evidence must point to real verifier results, not summary text only
- demo must stay inside slice-1 structural scope
- verifiers must fail loudly if output files are missing

## Exit Criteria

- both verifiers exit `0`
- evidence manifest and both reports exist
- demo index and demo markdown exist

## Handoff Target

`Program Governor`

## No Approval Implied

Passing these verifiers does not approve Phase 3 and does not authorize slice 2.
