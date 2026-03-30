# Task Card

## Header

- Task Card ID: `P3-TC-ACL-03`
- Phase: `3`
- Title: `Slice 3 Boundary Check`
- Status: `ready_for_audit`
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
  - `AGENTS.md`
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/cell_registry.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/lifecycle_engine.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/scheduler.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/workspace_state.py`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-NOTE-ACL-01_PHASE_3_SLICE_1_BOUNDARY_NOTES.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-NOTE-ACL-02_PHASE_3_SLICE_2_BOUNDARY_NOTES.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ACL-03_PHASE_3_BOUNDARY_CHECK.md`
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
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-ACL-03`
- Rollback Tag Name: `rollback/P3-TC-ACL-03/20260330-0000`

## Objective

- Goal:
  - check whether `split_merge_rules` and `profile_budget_rules` stay inside the approved Phase 3 boundary, remain subordinate to the approved Phase 2 lifecycle and scheduler substrate, and do not leak into Phase 4 memory scope
- Expected Outputs:
  - a real Slice 3 boundary note
  - explicit statement of whether the note is provisional, pass, or blocking
  - exact post-integration checks if Slice 3 runtime is not yet present in this lane
- Non-Goals:
  - runtime edits
  - verifier edits
  - evidence edits
  - approval or validation
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none in this lane because no owned verifier surface exists for this task
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_lifecycle.py`
- Required Evidence Output Paths:
  - none owned by this task
- Required Demo Path:
  - none owned by this task

## Handoff Records

- Audit Report Path:
  - `n/a`
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
- Merge Arbiter: `inactive for this boundary pass`
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

1. inspect the approved Phase 2 lifecycle, registry, scheduler, and workspace boundaries that Slice 3 must not replace
2. inspect the current Phase 3 Slice 1 and Slice 2 notes and runtime surfaces already present in this lane
3. check whether `split_merge_rules.py` and `profile_budget_rules.py` exist in this lane and whether any other Phase 3 runtime file already hides that logic
4. write a narrow note that records real boundary rules and an honest verdict

## Cross-Checks

- no second lifecycle state machine
- no scheduler reimplementation
- no Phase 4 memory-plane logic
- no hidden Slice 3 logic already embedded in Slice 1 or Slice 2 files

## Exit Criteria

- Slice 3 is marked either `pass` or `provisional/blocking` with exact reasons and next checks

## Handoff Target

`Program Governor`

## No Approval Implied

This boundary check is a control pass only. It does not approve the phase or the slice.
