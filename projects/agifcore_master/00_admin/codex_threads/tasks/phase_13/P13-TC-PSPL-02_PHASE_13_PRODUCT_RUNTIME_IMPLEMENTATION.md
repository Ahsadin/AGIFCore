# P13-TC-PSPL-02 Phase 13 Product Runtime Implementation

## Header

- Task Card ID: `P13-TC-PSPL-02`
- Phase: `13`
- Title: `Phase 13 Product Runtime Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Product & Sandbox Pod Lead`
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
  - `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-ACL-01_PHASE_13_BOUNDARIES_AND_CONTRACTS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-PSPL-01_PHASE_13_PRODUCT_RUNTIME_DECOMPOSITION.md`
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
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/contracts.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/embeddable_runtime_api.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/local_runner.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/local_gateway.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/desktop_ui.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/state_export.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/trace_export.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/memory_review_export.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/safe_shutdown.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/fail_closed_ux.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/installer_distribution.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/product_runtime_shell.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/__init__.py`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/05_testing/*`
  - `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
  - all lower-phase runtime files
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p13-tc-pg-02-phase-13-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P13-TC-PSPL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the full governed Phase 13 product-runtime package above approved Phase 2 through 12 inputs and below Phase 14 and Phase 16.
- Expected Outputs:
  - complete Phase 13 runtime package under `04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/`
- Non-Goals:
  - changing lower-phase runtime truth
  - implementing Phase 14 or Phase 16
  - writing audit or validation artifacts
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - hand off to `Test & Replay Lead`
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime`
- Required Verifier Paths:
  - hand off to `Test & Replay Lead`
- Required Evidence Output Paths:
  - hand off to `Test & Replay Lead`
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

1. Build the typed contracts first.
2. Keep all lower-phase inputs read-only.
3. Keep runner, gateway, desktop UI, exports, shutdown, and installer as separate modules instead of one mixed app shell.
4. Keep `task_submit` and `policy_update` fail-closed in the first execution slice.
5. Fail closed whenever a path would leak into Phase 14 or Phase 16 behavior.

## Cross-Checks

- No Phase 14 behavior.
- No Phase 16 behavior.
- No hidden cognition path.
- No direct mutation of lower-phase state.
- No product shell claims based only on presentation polish.
