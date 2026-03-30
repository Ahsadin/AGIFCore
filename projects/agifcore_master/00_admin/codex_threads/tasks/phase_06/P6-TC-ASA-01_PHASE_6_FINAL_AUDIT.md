# P6-TC-ASA-01 Phase 6 Final Audit

## Header

- Task Card ID: `P6-TC-ASA-01`
- Phase: `6`
- Title: `Phase 6 Final Audit`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Anti-Shortcut Auditor`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-PG-02_PHASE_6_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-WCPL-02_PHASE_6_WORLD_SIMULATOR_IMPLEMENTATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-TRL-02_PHASE_6_WORLD_SIMULATOR_VERIFIERS_AND_EVIDENCE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-ACL-02_PHASE_6_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-NOTE-ACL-01_PHASE_6_BOUNDARY_NOTES.md`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-ASA-01_PHASE_6_FINAL_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-AUDIT-01_PHASE_6_FINAL_PACKAGE_AUDIT_REPORT.md`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - any handoff file other than the audit report
  - all Phase 7+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p6-tc-asa-01-phase-6-final-audit`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P6-TC-ASA-01`
- Rollback Tag Name: `rollback/P6-TC-ASA-01/<yyyymmdd-hhmm>`

## Objective

- Goal: audit the full built Phase 6 package for fake completeness, silent omission, unsupported claims, greenfield drift, budget violations, and later-phase leakage.
- Expected Outputs:
  - this task card
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-AUDIT-01_PHASE_6_FINAL_PACKAGE_AUDIT_REPORT.md`
- Non-Goals:
  - fixing runtime
  - fixing verifiers
  - demo authoring
  - phase approval

## Work Method

1. Read the plan, task cards, runtime package, verifier family, evidence manifest, demo bundle, and boundary note.
2. Check that all required Phase 6 surfaces exist and are populated by real outputs.
3. Check for prohibited shortcuts, empty reports, unverifiable claims, budget overrun, and Phase 7 or Phase 8 leakage.
4. Write concrete findings and an explicit pass or blocked judgment for audit only.

## Cross-Checks

- No authoring-role overlap.
- No one giant mixed state shortcut.
- No prose-only world model, future, lane, instrumentation, or usefulness claims.
- No report text accepted without corresponding files.
- No approval implied.

## Exit Criteria

- Audit report is written with concrete file-backed findings.
- Any blocking issue is explicit.
- Handoff target is ready for `Program Governor`.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Audit completion is not phase approval and does not change Phase 6 from `open`.
