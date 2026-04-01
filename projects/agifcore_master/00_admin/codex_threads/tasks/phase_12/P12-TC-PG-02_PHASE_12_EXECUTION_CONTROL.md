# P12-TC-PG-02 Phase 12 Execution Control

## Header

- Task Card ID: `P12-TC-PG-02`
- Phase: `12`
- Title: `Phase 12 Execution Control`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Architecture & Contract Lead`, `Meta & Growth Pod Lead`, `Test & Replay Lead`, `Release & Evidence Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `local_governor_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/PHASE_12_STRUCTURAL_GROWTH.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-PG-02_PHASE_12_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_PLAN_FREEZE_HANDOFF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_EXECUTION_START_BRIEF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p12-tc-pg-02-phase-12-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P12-TC-PG-02/<yyyymmdd-hhmm>`

## Objective

- Goal: control the full Phase 12 execution chain without letting phase truth drift or Phase 13 or Phase 14 scope leak in.
- Expected Outputs:
  - this task card
  - the required Phase 12 handoff records when execution reaches those gates
  - execution-start truth for the user-directed Phase 12 baseline
- Non-Goals:
  - phase approval
  - Phase 13 implementation
  - Phase 14 implementation
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `yes`

## Verification

- Required Test Commands:
  - full Phase 12 verifier family after TRL lands
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_self_model_feedback.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_reflection_control.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_self_reorganization.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_domain_genesis.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_theory_formation.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_procedure_tool_invention.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_curiosity_gap_selection.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_structural_growth_cycle.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_demo_bundle/`

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

1. Keep Phase 12 truthful as `open` throughout execution.
2. Freeze the user-directed execution baseline before runtime code begins.
3. Require runtime, verifier, evidence, demo, and danger-zone checkpoint surfaces before any later audit or validation request.
4. Do not let structural growth leak into Phase 13 product runtime or Phase 14 sandbox/profile behavior.
5. Stop only when the full implementation, verifier, evidence, and demo package is ready for separate audit and validation lanes.

## Cross-Checks

- No Phase 13 start.
- No Phase 14 start.
- No live external search execution.
- No phase approval implied.
- No report text accepted as proof by itself.
