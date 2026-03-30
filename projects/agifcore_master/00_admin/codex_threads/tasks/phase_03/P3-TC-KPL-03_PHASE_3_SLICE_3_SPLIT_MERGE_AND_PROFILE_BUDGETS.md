# Task Card

## Header

- Task Card ID: `P3-TC-KPL-03`
- Phase: `3`
- Title: `Slice 3 Split Merge And Profile Budgets`
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
  - `projects/agifcore_master/02_requirements/DEPLOYMENT_PROFILES.md`
  - `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/lifecycle_engine.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/cell_contracts.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/tissue_manifests.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/activation_policies.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/trust_bands.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/active_dormant_control.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/split_merge_rules.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/profile_budget_rules.py`
- Forbidden Files:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_integrity_checks.py`
  - all `05_testing/*`
  - all `06_outputs/*`
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/`
- Forbidden Folders:
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-kpl-03-phase-3-slice-3-split-merge-and-profile-budgets`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-KPL-03`
- Rollback Tag Name: `rollback/P3-TC-KPL-03/20260330-0000`

## Objective

- Goal:
  - implement only the Slice 3 structural policy surfaces for split/merge rules and profile budget rules
- Expected Outputs:
  - bounded split/merge rule surface tied to Phase 2 lifecycle split and merge semantics
  - bounded profile-budget rule surface for laptop, mobile, and builder
- Non-Goals:
  - bundle integrity implementation
  - tissue orchestration implementation
  - Phase 4 work
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
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

1. port the strongest split/merge governance substrate from the approved Phase 2 lifecycle surface without reimplementing the lifecycle engine
2. make split/merge rules explicit, replayable, and lineage-aware
3. rebuild profile budget rules cleanly from the frozen deployment profiles and Phase 3 ceilings
4. keep budgets structural and fail-closed, not advisory
5. stop at Slice 3 only

## Cross-Checks

- no second lifecycle state machine
- no Phase 4 memory or Phase 5 graph logic
- no bundle-integrity logic
- no builder privilege beyond budget expansion rules

## Exit Criteria

- both owned runtime files exist
- both Slice 3 verifiers pass on the integrated package
- Slice 3 evidence files are produced

## Handoff Target

`Test & Replay Lead` then `Program Governor`

## No Approval Implied

Completing Slice 3 runtime code does not approve Phase 3, does not merge Slice 3, and does not authorize Slice 4.
