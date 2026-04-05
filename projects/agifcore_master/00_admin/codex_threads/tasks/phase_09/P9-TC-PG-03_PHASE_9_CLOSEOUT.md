# Task Card

## Header

- Task Card ID: `P9-TC-PG-03`
- Phase: `9`
- Title: `Phase 9 Closeout`
- Status: `complete`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `n/a`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `n/a`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `complete`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_VALIDATION_REQUEST.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-AUDIT-01_PHASE_9_FINAL_PACKAGE_AUDIT_REPORT.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-PG-03_PHASE_9_CLOSEOUT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_USER_VERDICT.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 10+ artifacts
  - Phase 9 runtime, testing, evidence, and demo files
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
  - `projects/agifcore_master/01_plan/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p9-tc-pg-02-phase-9-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P9-TC-PG-03/20260331-0000`

## Objective

- Goal:
  - record the explicit user approval, update the live Phase 9 gate truth, and stop without starting Phase 10
- Expected Outputs:
  - Phase 9 user verdict record
  - updated `PHASE_INDEX.md`
  - updated `PHASE_GATE_CHECKLIST.md`
  - truthful Decision and Changelog entries
- Non-Goals:
  - Phase 10 planning
  - further Phase 9 implementation
  - rewriting review artifacts
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none beyond confirming the required audit, governor verification, validation request, and user verdict chain exists
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_evidence_manifest.json`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/phase_09_demo_index.md`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-AUDIT-01_PHASE_9_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `n/a`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_VALIDATION_REQUEST.md`
- User Verdict Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path:
  - `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- explicit user verdict is recorded
- live phase-truth files show Phase 9 `approved`
- decision and changelog entries are truthful
- Phase 10 remains not started
- rollback path is defined

## Work Method

1. ensure the reviewed Phase 9 artifacts are integrated on the execution branch
2. record the explicit user verdict as `approved`
3. update the live phase-truth files and logs
4. stop after the closeout commit

## Cross-Checks

- no approval is recorded without the full closure chain already on disk
- no Phase 10 artifact is touched
- no Phase 9 runtime artifact is rewritten here

## Exit Criteria

- Phase 9 is marked `approved` in the live phase-truth files
- the user verdict is on disk
- the closeout commit exists

## Handoff Target

`User`

## No Approval Implied

This task card records the user approval that already happened. It does not start Phase 10.
