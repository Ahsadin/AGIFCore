# P13-TC-REL-02 Phase 13 Demo Bundle

## Header

- Task Card ID: `P13-TC-REL-02`
- Phase: `13`
- Title: `Phase 13 Demo Bundle`
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
  - `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/`

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_demo_bundle/`
- Forbidden Files:
  - any Phase 14 and later artifact
  - any runtime file
  - any verifier file
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`

## Branch And Worktree

- Branch Name: `codex/tc-p13-tc-pg-02-phase-13-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P13-TC-REL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: package the Phase 13 end-to-end, fail-closed, and installer/distribution demos in a directly reviewable form.
- Expected Outputs:
  - runnable demo JSON files
  - matching markdown review surfaces
  - demo index
- Non-Goals:
  - phase approval
  - runtime behavior changes

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/run_phase_13_end_to_end_product_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/run_phase_13_fail_closed_ux_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/run_phase_13_installer_distribution_demo.py`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/`
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

1. Package the end-to-end product demo from real runtime and verifier outputs.
2. Package the fail-closed UX demo from real blocked-state and gateway outputs.
3. Package the installer/distribution demo from the real local bundle and launcher proof.
4. Keep every demo claim linked to evidence files.

## Cross-Checks

- No demo may imply phase completion.
- No demo may hide blocked paths behind polished success text.
- No Phase 14 or Phase 16 claim may appear in the packaged demos.
- No public-release packaging creep.

## Exit Criteria

- Demo bundle is directly reviewable and evidence-linked.
- Handoff target is ready for later audit and Governor verification.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Demo packaging is not phase approval and does not change Phase 13 from `open`.
