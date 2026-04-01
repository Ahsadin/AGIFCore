# P14-TC-PG-03 Phase 14 Manifest Strengthening Control

## Header

- Task Card ID: `P14-TC-PG-03`
- Phase: `14`
- Title: `Phase 14 Manifest Strengthening Control`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Architecture & Contract Lead`, `Product & Sandbox Pod Lead`, `Test & Replay Lead`, `Anti-Shortcut Auditor`, `Validation Agent`, `Release & Evidence Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `local_governor_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `separate_validation_thread_required`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/`
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-PG-03_PHASE_14_MANIFEST_STRENGTHENING_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_VALIDATION_REQUEST.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 15 and later artifacts

## Branch And Worktree

- Branch Name: `codex/tc-p13-tc-pg-03-phase-13-closeout`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P14-TC-PG-03/<yyyymmdd-hhmm>`

## Objective

- Goal: control the focused Phase 14 manifest-strengthening pass and close the phase only if the strengthened package is honestly closure-ready.
- Expected Outputs:
  - direct verification record
  - validation request
  - closeout truth updates only if all closure conditions pass
- Non-Goals:
  - Phase 15 start
  - weakening any verifier
  - approving the phase without full evidence
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - all 9 existing `verify_phase_14_*` scripts
  - all 4 existing Phase 14 demo runners
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox`
  - `python3 -m compileall projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/`
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

1. Read current Phase 14 runtime, tests, and outputs first.
2. Require role-separated author, audit, validation, and review-bundle lanes.
3. Close Phase 14 only if every closure condition passes without an unresolved blocker.
4. Keep Phase 15 blocked.

## Cross-Checks

- No Phase 15 start.
- No verifier weakening.
- No approval without evidence.
