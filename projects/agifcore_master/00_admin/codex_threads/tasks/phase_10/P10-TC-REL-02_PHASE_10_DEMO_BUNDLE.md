# P10-TC-REL-02 Phase 10 Demo Bundle

## Header

- Task Card ID: `P10-TC-REL-02`
- Phase: `10`
- Title: `Phase 10 Demo Bundle`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Test & Replay Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `local_release_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/`

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_demo_bundle/`
- Forbidden Files:
  - any Phase 11 and later artifact
  - any runtime file
  - any verifier file
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`

## Branch And Worktree

- Branch Name: `codex/tc-p10-tc-pg-02-phase-10-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P10-TC-REL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: package the Phase 10 `why was this weak` and contradiction demos in a directly reviewable form.
- Expected Outputs:
  - runnable demo JSON files
  - matching markdown review surfaces
  - demo index
- Non-Goals:
  - phase approval
  - runtime behavior changes

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/run_phase_10_why_was_this_weak_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/run_phase_10_contradiction_demo.py`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-01_PHASE_10_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-02_PHASE_10_DANGER_ZONE_AUDIT_REPORT.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `n/a`

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

1. Package the `why was this weak` demo from real runtime and verifier outputs.
2. Package the contradiction demo from real runtime and verifier outputs.
3. Build matching markdown and JSON review surfaces.
4. Keep every demo claim linked to evidence files.

## Cross-Checks

- No demo may imply phase completion.
- No demo may hide uncertainty or support-state limits behind polished critique language.
- No self-improvement or structural-growth claim may appear in the packaged demos.
- No public-release packaging creep.

## Exit Criteria

- Demo bundle is directly reviewable and evidence-linked.
- Handoff target is ready for audit and Governor verification.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Demo packaging is not phase approval and does not change Phase 10 from `open`.
