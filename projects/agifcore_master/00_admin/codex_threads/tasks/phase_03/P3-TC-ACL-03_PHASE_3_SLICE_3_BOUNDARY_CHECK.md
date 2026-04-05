# Task Card

## Header

- Task Card ID: `P3-TC-ACL-03`
- Phase: `3`
- Title: `Slice 3 Boundary Check`
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
  - `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/lifecycle_engine.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/split_merge_rules.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/profile_budget_rules.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_split_merge.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_profile_budgets.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ACL-03_PHASE_3_SLICE_3_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-NOTE-ACL-03_PHASE_3_SLICE_3_BOUNDARY_NOTES.md`
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

- Branch Name: `codex/tc-p3-tc-acl-03-phase-3-slice-3-boundary-check`
- Worktree Path: `.worktrees/P3-TC-ACL-03`
- Rollback Tag Name: `rollback/P3-TC-ACL-03/20260330-0000`

## Objective

- Goal:
  - confirm Slice 3 split/merge and profile-budget work stays inside the approved Phase 3 and Phase 2 boundary
- Expected Outputs:
  - no Phase 4 leakage
  - no second lifecycle state machine
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

1. check Split 3 runtime files against the Phase 3 plan and the approved Phase 2 lifecycle constraints
2. confirm split/merge rules preserve lineage, role-family bounds, and policy-bounded transitions
3. confirm profile-budget rules stay constrained to laptop, mobile, and builder with no correctness privilege drift
4. report any boundary violation back to the Program Governor immediately

## Cross-Checks

- no Phase 4 scope
- no direct lifecycle-engine reimplementation
- no builder privilege overriding truth rules
- no profile-budget logic hidden inside unrelated modules

## Exit Criteria

- Slice 3 runtime files are boundary-safe or explicitly blocked

## Handoff Target

`Program Governor`

## No Approval Implied

This boundary check is a control pass only. It does not approve the phase or the slice.
