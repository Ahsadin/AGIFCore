# P14-TC-PG-02 Phase 14 Execution Control

## Header

- Task Card ID: `P14-TC-PG-02`
- Phase: `14`
- Title: `Phase 14 Execution Control`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Architecture & Contract Lead`, `Product & Sandbox Pod Lead`, `Test & Replay Lead`, `Release & Evidence Lead`
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
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-PG-02_PHASE_14_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_PLAN_FREEZE_HANDOFF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_EXECUTION_START_BRIEF.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - all Phase 15 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`

## Branch And Worktree

- Branch Name: `codex/tc-p14-tc-pg-02-phase-14-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P14-TC-PG-02/<yyyymmdd-hhmm>`

## Objective

- Goal: control the full Phase 14 execution chain without letting phase truth drift or Phase 15 or Phase 16 scope leak in.
- Expected Outputs:
  - this task card
  - the required Phase 14 handoff records when execution reaches those gates
  - execution-start truth for the user-directed Phase 14 baseline
- Non-Goals:
  - phase approval
  - Phase 15 implementation
  - Phase 16 implementation
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 14 verifier family after TRL lands
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_sandbox.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_wasmtime_fuel.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_wasmtime_memory.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_wasmtime_wall_time.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_cell_manifest.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_tissue_manifest.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_profile_manifests.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_active_cell_budget.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_dormant_cell_survival.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-AUDIT-01_PHASE_14_FINAL_PACKAGE_AUDIT_REPORT.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_USER_VERDICT.md`

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

1. Keep Phase 14 truthful as `open` throughout execution.
2. Freeze the user-directed execution baseline before runtime code begins.
3. Require sandbox, limits, manifests, profile, budget, proof, verifier, evidence, and demo surfaces before any later audit or validation request.
4. Do not let sandbox/profile work leak into Phase 15 final-proof or Phase 16 release/publication behavior.
5. Stop only when the full implementation, verifier, evidence, and demo package is ready for separate audit and validation lanes.

## Cross-Checks

- No Phase 15 start.
- No Phase 16 start.
- No hidden correctness privilege.
- No report text accepted as proof by itself.
- No phase approval implied.
