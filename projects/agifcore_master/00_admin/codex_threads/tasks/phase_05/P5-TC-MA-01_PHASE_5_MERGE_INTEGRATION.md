# P5-TC-MA-01 Phase 5 Merge Integration

## Header

- Task Card ID: `P5-TC-MA-01`
- Phase: `5`
- Title: `Phase 5 Merge Integration`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Merge Arbiter`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `separate_role_lane_required`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-AUDIT-01_PHASE_5_FINAL_PACKAGE_AUDIT_REPORT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-MGPL-01_PHASE_5_GRAPH_IMPLEMENTATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-TRL-01_PHASE_5_GRAPH_VERIFIERS_AND_EVIDENCE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-ACL-01_PHASE_5_BOUNDARY_CHECK.md`
  - current Phase 5 runtime, test, and output surfaces

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-MA-01_PHASE_5_MERGE_INTEGRATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_MERGE_HANDOFF.md`
- Forbidden Files:
  - any new runtime, verifier, or demo feature files
  - all Phase 6+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - any Phase 6+ family

## Branch And Worktree

- Branch Name: `codex/tc-p5-tc-ma-01-phase-5-merge-integration`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P5-TC-MA-01`
- Rollback Tag Name: `rollback/P5-TC-MA-01/<yyyymmdd-hhmm>`

## Objective

- Goal: integrate approved role-lane outputs into one clean Phase 5 review lane without authoring new functionality.
- Expected Outputs:
  - this task card
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_MERGE_HANDOFF.md`
- Non-Goals:
  - runtime invention
  - verifier invention
  - audit
  - validation
  - phase approval

## Work Method

1. Read the audit outcome and approved role-lane outputs.
2. Confirm no role wrote outside its owned scope.
3. Record the integrated package state and any remaining merge constraints.
4. Hand off the integrated package to `Program Governor` for rerun verification.

## Cross-Checks

- No new functionality added by this role.
- No authoring-role overlap.
- No approval implied.

## Exit Criteria

- Merge handoff exists and names the integrated surfaces.
- No unresolved file-scope conflict remains.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Merge integration is not validation and does not approve the phase.
