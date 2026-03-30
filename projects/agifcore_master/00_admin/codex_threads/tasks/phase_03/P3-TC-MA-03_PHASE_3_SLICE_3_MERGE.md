# Task Card

## Header

- Task Card ID: `P3-TC-MA-03`
- Phase: `3`
- Title: `Slice 3 Merge And Integration Prep`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Merge Arbiter`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `pending_spawn`
- Merge Arbiter Session ID: `pending_spawn`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-KPL-03_PHASE_3_SLICE_3_SPLIT_MERGE_AND_PROFILE_BUDGETS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-TRL-03_PHASE_3_SLICE_3_SPLIT_MERGE_AND_PROFILE_VERIFIERS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ACL-03_PHASE_3_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-MA-03_PHASE_3_SLICE_3_MERGE.md`

## Scope Control

- Owned Files:
  - integrated Slice 3 runtime, verifier, evidence, and boundary-note files only
- Forbidden Files:
  - Phase 3 plan files
  - Phase 3 closeout artifacts
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/07_assets/`
  - `projects/agifcore_master/08_logs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-ma-03-phase-3-slice-3-merge`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-MA-03`
- Rollback Tag Name: `rollback/P3-TC-MA-03/20260330-0000`

## Objective

- Goal:
  - integrate the cleared Slice 3 role-lane commits into one merge lane so Governor can rerun the verifiers honestly
- Expected Outputs:
  - one integrated Slice 3 package in a clean worktree
- Non-Goals:
  - approving Phase 3
  - final closeout merge
  - Slice 4 work
- Inherited Lineage Touched: `yes`
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
  - `deferred until later integration checkpoint`
- Validation Request Path:
  - `deferred until later phase closeout`
- User Verdict Path:
  - `deferred until later phase closeout`
- Additional Human Demo Checkpoint Path:
  - `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `Merge Arbiter`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- rollback path is defined
- integrated worktree is clean before Governor rerun

## Work Method

1. create rollback tag before integration
2. integrate only the cleared Slice 3 role-lane commits
3. keep content changes limited to what the cherry-picks require
4. do not run the verifiers; Governor will do that

## Cross-Checks

- no Slice 4 files
- no Phase 4 files
- no opportunistic refactors
- no content rewrite beyond clean integration

## Exit Criteria

- Slice 3 merge lane contains the intended role-lane commits
- worktree is clean
- Governor can rerun the Slice 3 verifiers directly

## Handoff Target

`Program Governor`

## No Approval Implied

This merge-prep task does not approve Phase 3 and does not close Slice 3.
