# P14-TC-PSPL-03 Phase 14 Manifest Strengthening Implementation

## Header

- Task Card ID: `P14-TC-PSPL-03`
- Phase: `14`
- Title: `Phase 14 Manifest Strengthening Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Product & Sandbox Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `separate_build_thread_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/contracts.py`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/cell_manifest.py`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/tissue_manifest.py`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/active_cell_budget.py`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/dormant_cell_survival.py`
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/sandbox_profile_shell.py`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-ACL-02_PHASE_14_MANIFEST_STRENGTHENING_BOUNDARY.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/05_testing/*`
  - `projects/agifcore_master/06_outputs/*`
  - all Phase 15 and later artifacts

## Branch And Worktree

- Branch Name: `codex/tc-p13-tc-pg-03-phase-13-closeout`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P14-TC-PSPL-03/<yyyymmdd-hhmm>`

## Objective

- Goal: strengthen the existing Phase 14 manifest and tissue runtime so differentiation is real, bounded, and machine-checkable.
- Expected Outputs:
  - updated runtime manifest/tissue/budget/dormant-survival logic
- Non-Goals:
  - verifier authorship
  - audit authorship
  - validation authorship
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

1. Keep literal `1024` cells and literal `32` tissues.
2. Add only structured fields that affect runtime logic or validation.
3. Make active-budget or dormant-proof logic consume the strengthened structure where needed.
4. Do not broaden outside Phase 14.

## Cross-Checks

- No filler metadata.
- No Phase 15 behavior.
- No verifier weakening.
