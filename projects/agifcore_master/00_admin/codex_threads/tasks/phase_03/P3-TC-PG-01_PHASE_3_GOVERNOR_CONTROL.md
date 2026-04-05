# Task Card

## Header

- Task Card ID: `P3-TC-PG-01`
- Phase: `3`
- Title: `Phase 3 Governor Control`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Architecture & Contract Lead`, `Kernel Pod Lead`, `Test & Replay Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `n/a`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-PG-01_PHASE_3_GOVERNOR_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_PLAN_FREEZE_HANDOFF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_EXECUTION_START_BRIEF.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 4+ artifacts
  - any Phase 3 user verdict artifact
  - any Phase 3 final validation request artifact
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/07_assets/`
  - `projects/agifcore_master/08_logs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-pg-01-phase-3-governor-control`
- Worktree Path: `.worktrees/P3-TC-PG-01`
- Rollback Tag Name: `rollback/P3-TC-PG-01/20260330-0000`

## Objective

- Goal:
  - keep the frozen Phase 3 baseline in governed execution control
  - open and govern the Phase 3 slice-1 execution, test, and boundary-review task cards
  - stop only at the audit boundary while Phase 3 remains open
- Expected Outputs:
  - governed task-card set exists for slice 1 startup
  - Phase 3 slice-1 runtime, schema, verifier, and starter evidence surfaces are present
  - slice 1 stops at `ready_for_audit`
- Non-Goals:
  - approving Phase 3
  - starting Phase 4
  - starting slice 2
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_cell_contracts.py`
  - `python3 projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_validation.py`
- Required Build Commands:
  - none for slice 1
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_cell_contracts.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_validation.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/`

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

## Governor Method

1. keep Phase 3 truth aligned to `open`
2. create task cards before any slice-1 code lands
3. spawn the active role workers as separate identities with one active build pod by default
4. keep slice 1 bounded to contracts, manifests, bundle manifest, and schema validation
5. stop implementation at the audit boundary

## No Approval Implied

This task card opens execution control only. It does not approve the phase, does not close the phase, and does not authorize Phase 4.
