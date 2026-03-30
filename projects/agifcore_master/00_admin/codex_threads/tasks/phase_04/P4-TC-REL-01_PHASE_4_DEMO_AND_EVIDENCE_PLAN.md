# P4-TC-REL-01 Phase 4 Demo And Evidence Plan

## Header

- Task Card ID: `P4-TC-REL-01`
- Phase: `4`
- Title: `Phase 4 Demo And Evidence Plan`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Test & Replay Lead`, `Program Governor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `not_assigned`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-REL-01_PHASE_4_DEMO_AND_EVIDENCE_PLAN.md`
- Forbidden Files:
  - all `projects/agifcore_master/04_execution/*`
  - all public release artifacts
  - all Phase 5+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/07_assets/`

## Branch And Worktree

- Branch Name: `planned_on_freeze`
- Worktree Path: `planned_on_freeze`
- Rollback Tag Name: `planned_on_freeze`

## Objective

- Goal: define the later demo bundle and evidence package shape for Phase 4.
- Expected Outputs:
  - this task card
- Non-Goals:
  - runtime implementation
  - public release execution
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands: `n/a`
- Required Build Commands: `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/`
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

1. Define the demo bundle for memory carry-forward, correction, and forgetting/compression.
2. Keep evidence machine-readable and grouped by verifier surface.
3. Make the later review packet inspectable from files alone.
4. Keep public release work out of Phase 4 planning.

## Cross-Checks

- No missing demo surface.
- No summary-only evidence claim.
- No phase approval implied.
