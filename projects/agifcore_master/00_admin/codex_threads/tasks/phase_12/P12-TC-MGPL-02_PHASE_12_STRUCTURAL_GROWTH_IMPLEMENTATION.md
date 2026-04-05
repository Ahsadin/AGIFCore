# P12-TC-MGPL-02 Phase 12 Structural Growth Implementation

## Header

- Task Card ID: `P12-TC-MGPL-02`
- Phase: `12`
- Title: `Phase 12 Structural Growth Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Meta & Growth Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `local_build_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_12_STRUCTURAL_GROWTH.md`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/`
  - `projects/agifcore_master/04_execution/phase_11_governed_self_improvement/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-ACL-01_PHASE_12_BOUNDARIES_AND_CONTRACTS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-MGPL-01_PHASE_12_EXECUTION_DECOMPOSITION.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
  - `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/contracts.py`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/self_model_feedback.py`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/reflection_control.py`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/curiosity_gap_selection.py`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/theory_formation.py`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/procedure_tool_invention.py`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/self_reorganization.py`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/domain_genesis.py`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/structural_growth_cycle.py`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/__init__.py`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/05_testing/*`
  - `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
  - all Phase 10 and Phase 11 runtime files
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p12-tc-pg-02-phase-12-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P12-TC-MGPL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the full governed Phase 12 runtime package above approved Phase 11 inputs and below Phase 13 and Phase 14.
- Expected Outputs:
  - complete Phase 12 runtime package under `04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/`
- Non-Goals:
  - changing Phase 10 or Phase 11 runtime truth
  - implementing Phase 13 or Phase 14
  - writing audit or validation artifacts
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `yes`

## Verification

- Required Test Commands:
  - hand off to `Test & Replay Lead`
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth`
- Required Verifier Paths:
  - hand off to `Test & Replay Lead`
- Required Evidence Output Paths:
  - hand off to `Test & Replay Lead`
- Required Demo Path:
  - hand off to `Release & Evidence Lead`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-AUDIT-01_PHASE_12_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-AUDIT-02_PHASE_12_DANGER_ZONE_AUDIT_REPORT.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_ADDITIONAL_HUMAN_DEMO_CHECKPOINT.md`

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

1. Build the typed contracts first.
2. Keep all Phase 11 inputs read-only.
3. Implement each Phase 12 subsystem as a separate module instead of one mixed growth engine.
4. Emit a thin Phase 12 overlay contract with explicit Phase 11 trace refs and evidence refs.
5. Fail closed whenever a candidate would leak into product runtime, sandbox/profile behavior, or hidden autonomy.

## Cross-Checks

- No Phase 13 behavior.
- No Phase 14 behavior.
- No hidden autonomy path.
- No direct mutation of Phase 11 state.
- No runtime truth claims based only on polished structural language.
