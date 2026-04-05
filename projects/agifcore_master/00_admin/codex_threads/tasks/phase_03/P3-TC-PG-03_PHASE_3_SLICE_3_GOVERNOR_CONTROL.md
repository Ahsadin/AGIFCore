# Task Card

## Header

- Task Card ID: `P3-TC-PG-03`
- Phase: `3`
- Title: `Phase 3 Slice 3 Governor Control`
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
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/lifecycle_engine.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/scheduler.py`
  - `projects/agifcore_master/02_requirements/DEPLOYMENT_PROFILES.md`
  - committed Slice 2 outputs on the MA-02 lane

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-PG-03_PHASE_3_SLICE_3_GOVERNOR_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-KPL-03_PHASE_3_SLICE_3_SPLIT_MERGE_AND_PROFILE_BUDGETS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-TRL-03_PHASE_3_SLICE_3_SPLIT_MERGE_AND_PROFILE_VERIFIERS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ACL-03_PHASE_3_SLICE_3_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ASA-03_PHASE_3_SLICE_3_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-MA-03_PHASE_3_SLICE_3_MERGE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-04_PHASE_3_SLICE_3_AUDIT_REPORT.md`
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

- Branch Name: `codex/tc-p3-tc-pg-03-phase-3-slice-3-governor-control`
- Worktree Path: `.worktrees/P3-TC-PG-03`
- Rollback Tag Name: `rollback/P3-TC-PG-03/20260330-0000`

## Objective

- Goal:
  - keep Slice 3 bounded to split/merge rules and profile budget rules
  - open the Slice 3 task-card set before any Slice 3 code lands
  - stop after Slice 3 audit and integration, without starting Slice 4 in this lane
- Expected Outputs:
  - governed Slice 3 task-card set exists
  - Slice 3 runtime, verifiers, and evidence files exist
  - Slice 3 ends at audited integrated status
- Non-Goals:
  - bundle integrity implementation
  - final Phase 3 closeout
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
- Slice 4 did not start in this lane

## Governor Method

1. branch Slice 3 from the committed Slice 2 merge lane
2. create task cards before any Slice 3 runtime or verifier changes
3. keep one active build pod by default
4. keep runtime scope limited to `split_merge_rules.py` and `profile_budget_rules.py`
5. stop after Slice 3 audit and integration

## No Approval Implied

This task card governs Slice 3 only. It does not approve Phase 3, does not close Phase 3, and does not authorize Phase 4.
