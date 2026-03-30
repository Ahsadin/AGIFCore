# P4-TC-TRL-01 Phase 4 Memory Verification Plan

## Header

- Task Card ID: `P4-TC-TRL-01`
- Phase: `4`
- Title: `Phase 4 Memory Verification Plan`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Release & Evidence Lead`, `Program Governor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `not_assigned`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 2 and Phase 3 verifier families
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-TRL-01_PHASE_4_MEMORY_VERIFICATION_PLAN.md`
- Forbidden Files:
  - all `projects/agifcore_master/04_execution/*`
  - all Phase 5+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`

## Branch And Worktree

- Branch Name: `planned_on_freeze`
- Worktree Path: `planned_on_freeze`
- Rollback Tag Name: `planned_on_freeze`

## Objective

- Goal: freeze the verifier family, machine-readable evidence outputs, and demo-proof surfaces for Phase 4.
- Expected Outputs:
  - this task card
- Non-Goals:
  - runtime implementation
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands: `n/a`
- Required Build Commands: `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_working_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_episodic_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_semantic_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_procedural_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_continuity_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_corrections_and_promotion.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_forgetting_and_compression.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_rollback_safe_updates.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_memory_review.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-01_PHASE_4_PLAN_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `Merge Arbiter`
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

1. Define one verifier per plane plus lifecycle and rollback-safe update verifiers.
2. Define negative fail-closed checks for correction, forgetting, compression, and review.
3. Keep evidence machine-readable and tied to real verifier outputs.
4. Keep the three required user demos inspectable from files alone.

## Cross-Checks

- Every required Phase 4 subsystem has a verifier path.
- Report text does not replace actual checks.
- Demo paths point to real evidence files.
