# P12-TC-REL-02 Phase 12 Demo Bundle

## Header

- Task Card ID: `P12-TC-REL-02`
- Phase: `12`
- Title: `Phase 12 Demo Bundle`
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
  - `projects/agifcore_master/01_plan/PHASE_12_STRUCTURAL_GROWTH.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/`

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_demo_bundle/`
- Forbidden Files:
  - any Phase 13 and later artifact
  - any runtime file
  - any verifier file
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`

## Branch And Worktree

- Branch Name: `codex/tc-p12-tc-pg-02-phase-12-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P12-TC-REL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: package the Phase 12 structural-growth and theory-growth demos in a directly reviewable form.
- Expected Outputs:
  - runnable demo JSON files
  - matching markdown review surfaces
  - demo index
- Non-Goals:
  - phase approval
  - runtime behavior changes

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_12_structural_growth/run_phase_12_structural_growth_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_12_structural_growth/run_phase_12_theory_growth_demo.py`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-AUDIT-01_PHASE_12_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-AUDIT-02_PHASE_12_DANGER_ZONE_AUDIT_REPORT.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_ADDITIONAL_HUMAN_DEMO_CHECKPOINT.md`

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

1. Package the structural-growth demo from real runtime and verifier outputs.
2. Package the theory-growth demo from real runtime and verifier outputs.
3. Build matching markdown and JSON review surfaces.
4. Keep every demo claim linked to evidence files.

## Cross-Checks

- No demo may imply phase completion.
- No demo may hide uncertainty or budget limits behind polished growth language.
- No product-runtime or sandbox/profile claim may appear in the packaged demos.
- No public-release packaging creep.

## Exit Criteria

- Demo bundle is directly reviewable and evidence-linked.
- Handoff target is ready for later audit and Governor verification.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Demo packaging is not phase approval and does not change Phase 12 from `open`.
