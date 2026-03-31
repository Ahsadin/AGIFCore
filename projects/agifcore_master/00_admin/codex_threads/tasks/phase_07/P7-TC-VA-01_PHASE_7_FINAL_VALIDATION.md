# P7-TC-VA-01 Phase 7 Final Validation

## Header

- Task Card ID: `P7-TC-VA-01`
- Phase: `7`
- Title: `Phase 7 Final Validation`
- Status: `complete`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Validation Agent`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `separate_role_lane_required`
- Required Reads:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-AUDIT-01_PHASE_7_FINAL_PACKAGE_AUDIT_REPORT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_GOVERNOR_VERIFICATION_RECORD.md`
  - the full Phase 7 runtime, verifier, evidence, and demo surfaces

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-VA-01_PHASE_7_FINAL_VALIDATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_VALIDATION_REQUEST.md`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - user verdict artifacts
  - all Phase 8+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p7-tc-pg-03-phase-7-closeout`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P7-TC-VA-01/20260331-0000`

## Objective

- Goal: validate that the complete Phase 7 package is ready for final user review without implying approval before the explicit verdict.
- Expected Outputs:
  - this task card
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_VALIDATION_REQUEST.md`
- Non-Goals:
  - runtime authoring
  - verifier authoring
  - demo authoring
  - phase approval

## Work Method

1. Read the validation protocol, audit report, governor verification record, and full package surfaces.
2. Check that the package is complete, inspectable, and still truthful about Phase 7 being `open` before the verdict is recorded.
3. Write the final review request naming the exact files the user must inspect.

## Cross-Checks

- No authoring-role overlap.
- No approval implied.
- No missing required artifact family.

## Exit Criteria

- Validation request is written.
- Final review package is explicit and inspectable.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Validation readiness is not user approval and does not change the phase state.
