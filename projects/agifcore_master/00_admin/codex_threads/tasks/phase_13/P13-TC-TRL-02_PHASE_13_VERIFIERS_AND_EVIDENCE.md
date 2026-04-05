# P13-TC-TRL-02 Phase 13 Verifiers And Evidence

## Header

- Task Card ID: `P13-TC-TRL-02`
- Phase: `13`
- Title: `Phase 13 Verifiers and Evidence`
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
  - `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/`
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
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/`
  - `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/04_execution/*`
  - `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_demo_bundle/*`
  - all Phase 14 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/`
  - `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_demo_bundle/`

## Branch And Worktree

- Branch Name: `codex/tc-p13-tc-pg-02-phase-13-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P13-TC-TRL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the Phase 13 verifier family and machine-readable evidence package against the built runtime.
- Expected Outputs:
  - full Phase 13 verifier family under `05_testing/phase_13_product_runtime_and_ux/`
  - machine-readable evidence under `06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/`
- Non-Goals:
  - changing runtime logic
  - writing audit or validation records
  - writing the review demo bundle
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 13 verifier family
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_runtime_api.py`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_local_runner.py`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_local_gateway.py`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_desktop_ui.py`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_state_export.py`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_trace_export.py`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_memory_review_export.py`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_safe_shutdown.py`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_fail_closed_ux.py`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/verify_phase_13_installer_distribution.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/phase_13_evidence_manifest.json`
- Required Demo Path:
  - hand off to `Release & Evidence Lead`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-AUDIT-01_PHASE_13_FINAL_PACKAGE_AUDIT_REPORT.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_USER_VERDICT.md`

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

1. Add one verifier per major Phase 13 subsystem.
2. Keep evidence machine-readable and tied to actual runtime outputs.
3. Add checks for gateway no-bypass, fail-closed behavior, export integrity, shutdown receipts, and installer local-only scope.
4. Do not fix runtime logic directly; hand failures back to the active build pod.

## Cross-Checks

- No runtime authoring.
- No Phase 14 behavior.
- No Phase 16 behavior.
- No empty report files.
- No demo claims without evidence.
