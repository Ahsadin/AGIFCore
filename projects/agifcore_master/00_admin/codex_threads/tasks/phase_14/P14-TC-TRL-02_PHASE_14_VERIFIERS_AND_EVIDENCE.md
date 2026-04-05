# P14-TC-TRL-02 Phase 14 Verifiers And Evidence

## Header

- Task Card ID: `P14-TC-TRL-02`
- Phase: `14`
- Title: `Phase 14 Verifiers and Evidence`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Product & Sandbox Pod Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `local_test_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/`
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
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/`
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/04_execution/*`
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_demo_bundle/*`
  - all Phase 15 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/`
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_demo_bundle/`

## Branch And Worktree

- Branch Name: `codex/tc-p14-tc-pg-02-phase-14-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P14-TC-TRL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the Phase 14 verifier family and machine-readable evidence package against the built runtime.
- Expected Outputs:
  - full Phase 14 verifier family under `05_testing/phase_14_sandbox_profiles_and_scale_realization/`
  - machine-readable evidence under `06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/`
- Non-Goals:
  - changing runtime logic
  - writing audit or validation records
  - writing the review demo bundle
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 14 verifier family
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization`
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
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_evidence_manifest.json`
- Required Demo Path:
  - hand off to `Release & Evidence Lead`

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

1. Add one verifier per major Phase 14 subsystem.
2. Keep evidence machine-readable and tied to actual runtime outputs.
3. Add checks for sandbox fail-closed behavior, Wasmtime limit trips, literal manifests, profile sameness, active-budget enforcement, and dormant-survival continuity.
4. Do not fix runtime logic directly; hand failures back to the active build pod.

## Cross-Checks

- No runtime authoring.
- No Phase 15 behavior.
- No Phase 16 behavior.
- No empty report files.
- No demo claims without evidence.
