# P14-TC-TRL-03 Phase 14 Manifest Strengthening Verification

## Header

- Task Card ID: `P14-TC-TRL-03`
- Phase: `14`
- Title: `Phase 14 Manifest Strengthening Verification`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Release & Evidence Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `separate_test_thread_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/_phase_14_verifier_common.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_cell_manifest.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_tissue_manifest.py`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/run_phase_14_manifest_audit_demo.py`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-ACL-02_PHASE_14_MANIFEST_STRENGTHENING_BOUNDARY.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/`
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/`
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_demo_bundle/`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/04_execution/*`
  - all Phase 15 and later artifacts

## Branch And Worktree

- Branch Name: `codex/tc-p13-tc-pg-03-phase-13-closeout`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P14-TC-TRL-03/<yyyymmdd-hhmm>`

## Objective

- Goal: update or add the minimum verifier and evidence logic needed to prove family differentiation, tissue specialization, exemplar structure, and constraint diversity are real.
- Expected Outputs:
  - updated verifier logic
  - updated evidence reports
  - updated demo outputs if needed
- Non-Goals:
  - runtime authorship
  - audit authorship
  - validation authorship
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - all 9 existing `verify_phase_14_*` scripts
  - any added Phase 14 differentiation verifier
  - all 4 existing Phase 14 demo runners
- Required Build Commands:
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

1. Keep the 9 existing verifiers intact as named interfaces.
2. Add only the minimum extra checks needed to prove differentiation is real.
3. Make every new claim machine-readable in evidence.

## Cross-Checks

- No verifier weakening.
- No fake evidence.
- No Phase 15 leak.
