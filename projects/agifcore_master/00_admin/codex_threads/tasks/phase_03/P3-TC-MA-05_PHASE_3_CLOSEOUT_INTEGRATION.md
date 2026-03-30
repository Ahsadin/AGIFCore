# Task Card

## Header

- Task Card ID: `P3-TC-MA-05`
- Phase: `3`
- Title: `Phase 3 Closeout Integration`
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-MA-05_PHASE_3_CLOSEOUT_INTEGRATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_VALIDATION_REQUEST.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-07_PHASE_3_FINAL_PACKAGE_AUDIT_REPORT.md`

## Scope Control

- Owned Files:
  - final Phase 3 demo-bundle files
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-07_PHASE_3_FINAL_PACKAGE_AUDIT_REPORT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_VALIDATION_REQUEST.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - any phase-truth file
  - any user verdict file
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-ma-05-phase-3-closeout-integration`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-MA-05`
- Rollback Tag Name: `rollback/P3-TC-MA-05/20260330-0000`

## Objective

- Goal:
  - integrate the cleared final audit, validation request, and demo-bundle commits onto the Phase 3 closeout branch
- Expected Outputs:
  - one clean closeout-ready branch with the full final review package present in the canonical project path
- Non-Goals:
  - changing phase truth
  - approving Phase 3
  - starting Phase 4
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none; Program Governor performs final truth update after integration
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-07_PHASE_3_FINAL_PACKAGE_AUDIT_REPORT.md`
- Required Evidence Output Paths:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_VALIDATION_REQUEST.md`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_demo_index.md`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-07_PHASE_3_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `n/a`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_VALIDATION_REQUEST.md`
- User Verdict Path:
  - `deferred to Program Governor closeout lane`
- Additional Human Demo Checkpoint Path:
  - `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `Merge Arbiter`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- rollback tag exists
- only cleared final review artifacts are integrated
- closeout branch is clean before Governor truth updates

## Work Method

1. create rollback tag
2. cherry-pick the cleared final review commits onto the closeout lane
3. stop without touching phase truth files

## Cross-Checks

- no runtime or test content rewrite
- no phase-truth edits
- no Phase 4 content

## Exit Criteria

- closeout branch contains the final demo bundle, final audit report, and validation request
- worktree is clean

## Handoff Target

`Program Governor`

## No Approval Implied

This integration pass does not approve Phase 3. It only prepares the closeout branch for the already-given user verdict to be recorded.
