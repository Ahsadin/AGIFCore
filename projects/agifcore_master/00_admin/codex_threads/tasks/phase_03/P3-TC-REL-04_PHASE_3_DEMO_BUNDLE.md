# Task Card

## Header

- Task Card ID: `P3-TC-REL-04`
- Phase: `3`
- Title: `Phase 3 Demo Bundle`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Test & Replay Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `pending_spawn`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - all current Phase 3 evidence reports on the MA-04 lane
  - current demo bundle files on the MA-04 lane

## Scope Control

- Owned Files:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_demo_index.md`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_tissue_orchestration_demo.md`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_split_merge_demo.md`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_bundle_validation_demo.md`
- Forbidden Files:
  - all runtime files
  - all verifier files
  - all evidence json files
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/07_assets/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-rel-04-phase-3-demo-bundle`
- Worktree Path: `.worktrees/P3-TC-REL-04`
- Rollback Tag Name: `rollback/P3-TC-REL-04/20260330-0000`

## Objective

- Goal:
  - build the final Phase 3 demo bundle from real integrated evidence only
- Expected Outputs:
  - updated demo index
  - tissue orchestration demo
  - split and merge demo
  - bundle validation demo updated to include integrity evidence
- Non-Goals:
  - runtime changes
  - verifier changes
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none authored here; rely on existing reports
- Required Build Commands:
  - none
- Required Verifier Paths:
  - all current `verify_phase_03_*` files on the MA-04 lane
- Required Evidence Output Paths:
  - all current `phase_03_*_report.json` files on the MA-04 lane
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-07_PHASE_3_FINAL_PACKAGE_AUDIT_REPORT.md`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_VALIDATION_REQUEST.md`

## Completion Checklist

- every demo points to real integrated evidence
- no demo claims Phase 3 is approved or closed
- demo index is current and complete

## Work Method

1. inspect the integrated evidence reports
2. update the old slice-1-only demo files to reflect the full Phase 3 package
3. add the missing tissue orchestration and split/merge demos
4. keep all demo wording factual and review-oriented

## No Approval Implied

The demo bundle is for review only. It does not approve or close Phase 3.
