# P8-TC-REL-02 Phase 8 Demo Bundle

## Header

- Task Card ID: `P8-TC-REL-02`
- Phase: `8`
- Title: `Phase 8 Demo Bundle`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Test & Replay Lead`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/`
- Forbidden Files:
  - any Phase 9 and later artifact
  - any runtime file
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/phase_09_*`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-wcpl-02-phase-8-science-world-awareness-implementation`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P8-TC-REL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: package the Phase 8 science-explanation and bounded live-fact demos in a directly reviewable form.
- Expected Outputs:
  - runnable demo JSON files
  - matching markdown review surfaces
  - demo index
- Non-Goals:
  - phase approval
  - runtime behavior changes
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/run_phase_08_science_explanation_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/run_phase_08_bounded_live_fact_demo.py`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-AUDIT-01_PHASE_8_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_USER_VERDICT.md`
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

1. Package the science explanation demo from real runtime and verifier outputs.
2. Package the bounded live-fact demo from real runtime and verifier outputs.
3. Build matching markdown and JSON review surfaces.
4. Keep every demo claim linked to evidence files.

## Cross-Checks

- No demo may imply phase completion.
- No demo may claim unsupported exact current facts.
- No public-release packaging creep.
- No hidden-thought disclosure inside the visible reasoning summary surface.
