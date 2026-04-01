# P13-TC-PG-02 Phase 13 Execution Control

## Header

- Task Card ID: `P13-TC-PG-02`
- Phase: `13`
- Title: `Phase 13 Execution Control`
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
  - `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-PG-02_PHASE_13_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_PLAN_FREEZE_HANDOFF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_EXECUTION_START_BRIEF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - all Phase 14 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`

## Branch And Worktree

- Branch Name: `codex/tc-p13-tc-pg-02-phase-13-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P13-TC-PG-02/<yyyymmdd-hhmm>`

## Objective

- Goal: control the full Phase 13 execution chain without letting phase truth drift or Phase 14 or Phase 16 scope leak in.
- Expected Outputs:
  - this task card
  - the required Phase 13 handoff records when execution reaches those gates
  - execution-start truth for the user-directed Phase 13 baseline
- Non-Goals:
  - phase approval
  - Phase 14 implementation
  - Phase 16 implementation
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 13 verifier family after TRL lands
- Required Build Commands:
  - `n/a`
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
  - `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_demo_bundle/`

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

1. Keep Phase 13 truthful as `open` throughout execution.
2. Freeze the user-directed execution baseline before runtime code begins.
3. Require runtime, verifier, evidence, demo, and local distribution surfaces before any later audit or validation request.
4. Do not let product shell work leak into Phase 14 sandbox/profile/scale behavior or Phase 16 release/publication behavior.
5. Stop only when the full implementation, verifier, evidence, and demo package is ready for separate audit and validation lanes.

## Cross-Checks

- No Phase 14 start.
- No Phase 16 start.
- No hidden cognition lane.
- No report text accepted as proof by itself.
- No phase approval implied.
