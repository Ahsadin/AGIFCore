# P14-TC-PSPL-02 Phase 14 Sandbox Profile Implementation

## Header

- Task Card ID: `P14-TC-PSPL-02`
- Phase: `14`
- Title: `Phase 14 Sandbox Profile Implementation`
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
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-ACL-01_PHASE_14_BOUNDARIES_AND_CONTRACTS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-PSPL-01_PHASE_14_SANDBOX_PROFILE_SCALE_DECOMPOSITION.md`
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
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/05_testing/*`
  - `projects/agifcore_master/06_outputs/*`
  - all Phase 15 and later artifacts
  - all lower-phase runtime files
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p14-tc-pg-02-phase-14-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P14-TC-PSPL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the full Phase 14 sandbox/profile runtime package above approved Phase 13 runtime truth and below Phase 15 and Phase 16.
- Expected Outputs:
  - complete Phase 14 runtime package under `04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/`
- Non-Goals:
  - changing Phase 13 public runtime truth
  - implementing Phase 15 or Phase 16
  - writing audit or validation artifacts
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - hand off to `Test & Replay Lead`
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox`
- Required Verifier Paths:
  - hand off to `Test & Replay Lead`
- Required Evidence Output Paths:
  - hand off to `Test & Replay Lead`
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

1. Build the typed contracts first.
2. Keep Phase 13 product-runtime inputs read-only.
3. Keep sandbox, limits, manifests, budgets, and dormant proofs as separate modules instead of one mixed deployment shell.
4. Fail closed whenever a path would leak into Phase 15 or Phase 16 behavior.
5. Keep profile differences explicit and bounded without creating correctness privilege.

## Cross-Checks

- No Phase 15 behavior.
- No Phase 16 behavior.
- No hidden correctness path.
- No direct mutation of lower-phase runtime truth.
- No label-only sandbox or manifest claims.
