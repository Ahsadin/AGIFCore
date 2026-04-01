# P14-TC-REL-02 Phase 14 Demo Bundle

## Header

- Task Card ID: `P14-TC-REL-02`
- Phase: `14`
- Title: `Phase 14 Demo Bundle`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Test & Replay Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `local_release_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/`

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_demo_bundle/`
- Forbidden Files:
  - any Phase 15 and later artifact
  - any runtime file
  - any verifier file
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`

## Branch And Worktree

- Branch Name: `codex/tc-p14-tc-pg-02-phase-14-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P14-TC-REL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: package the Phase 14 sandbox enforcement, laptop, mobile constrained, and manifest-audit demos in a directly reviewable form.
- Expected Outputs:
  - runnable demo JSON files
  - matching markdown review surfaces
  - demo index
- Non-Goals:
  - phase approval
  - runtime behavior changes

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/run_phase_14_sandbox_enforcement_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/run_phase_14_laptop_profile_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/run_phase_14_mobile_constrained_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/run_phase_14_manifest_audit_demo.py`
- Required Build Commands:
  - `n/a`
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

1. Package the sandbox enforcement demo from real runtime and verifier outputs.
2. Package the laptop profile demo from real profile and budget outputs.
3. Package the mobile constrained demo from real bounded budget and fail-closed outputs.
4. Package the manifest audit demo from literal manifests and dormant-survival outputs.
5. Keep every demo claim linked to evidence files.

## Cross-Checks

- No demo may imply phase completion.
- No demo may hide blocked paths behind polished success text.
- No Phase 15 or Phase 16 claim may appear in the packaged demos.
- No public-release packaging creep.

## Exit Criteria

- Demo bundle is directly reviewable and evidence-linked.
- Handoff target is ready for later audit and Governor verification.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Demo packaging is not phase approval and does not change Phase 14 from `open`.
