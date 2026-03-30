# Task Card

## Header

- Task Card ID: `P3-TC-TRL-03`
- Phase: `3`
- Title: `Slice 3 Split Merge And Profile Verifiers`
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
  - `projects/agifcore_master/02_requirements/DEPLOYMENT_PROFILES.md`
  - current Slice 1 and Slice 2 evidence files in your lane

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_split_merge.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_profile_budgets.py`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_split_merge_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_profile_budget_report.json`
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

- Branch Name: `codex/tc-p3-tc-trl-03-phase-3-slice-3-split-merge-and-profile-verifiers`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-03`
- Rollback Tag Name: `rollback/P3-TC-TRL-03/20260330-0000`

## Objective

- Goal:
  - verify Slice 3 split/merge behavior and profile-budget behavior and produce honest evidence
- Expected Outputs:
  - passing Slice 3 split/merge verifier on the integrated package
  - passing Slice 3 profile-budget verifier on the integrated package
  - machine-readable Slice 3 reports
  - refreshed evidence manifest that references all current real Phase 3 report files
- Non-Goals:
  - demo bundle authoring
  - bundle integrity verification
  - final phase review surfaces
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_split_merge.py`
  - `python3 projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_profile_budgets.py`
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_split_merge.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_profile_budgets.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_split_merge_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_profile_budget_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`
- Required Demo Path:
  - `n/a for Slice 3`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-04_PHASE_3_SLICE_3_AUDIT_REPORT.md`
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
- Merge Arbiter: `inactive until Slice 3 clears audit`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- rollback path is defined

## Work Method

1. wire both verifiers to the same self-contained repo-relative import strategy used in the earlier slices
2. verify valid and invalid split/merge proposals against the real runtime API
3. verify laptop, mobile, and builder profile-budget behavior against the real runtime API
4. keep evidence honest if your own lane lacks runtime files
5. refresh the shared evidence manifest only from real report files

## Cross-Checks

- no fake passing reports in a non-integrated lane
- no profile-budget behavior without explicit frozen profile names
- no split/merge pass without lineage and role-family guards

## Exit Criteria

- both Slice 3 verifiers exist and are runnable on an integrated package
- Slice 3 report files exist
- the evidence manifest remains honest

## Handoff Target

`Program Governor`

## No Approval Implied

Passing the Slice 3 verifiers does not approve Phase 3 and does not authorize Slice 4 automatically.
