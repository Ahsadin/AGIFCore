# P8-TC-TRL-02 Phase 8 Verifiers And Evidence

## Header

- Task Card ID: `P8-TC-TRL-02`
- Phase: `8`
- Title: `Phase 8 Verifiers And Evidence`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Release & Evidence Lead`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/`
  - approved Phase 7 verifier family and demo bundle

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
  - all files under `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Forbidden Files:
  - any Phase 9 and later artifact
  - any Phase 4, 5, 6, or 7 file
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/phase_09_*`
  - `projects/agifcore_master/04_execution/phase_10_*`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-wcpl-02-phase-8-science-world-awareness-implementation`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P8-TC-TRL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: produce the full machine-checkable Phase 8 verifier family and evidence bundle.
- Expected Outputs:
  - verifier common fixture chain
  - seven subsystem verifiers
  - evidence manifest
- Non-Goals:
  - runtime behavior changes outside what verifier scaffolding requires
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_scientific_priors.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_entity_request_inference.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_world_region_selection.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_causal_chain_reasoning.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_bounded_current_world_reasoning.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_visible_reasoning_summaries.py`
  - `python3 projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_science_reflection.py`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - all files under `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_*.py`
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

1. Create the common fixture and report helpers first.
2. Build one verifier per major Phase 8 subsystem.
3. Make every verifier produce machine-readable evidence.
4. Refresh the evidence manifest only from actual report files.

## Cross-Checks

- No empty report files.
- No pass status without a real runtime import and concrete assertions.
- No unsupported exact current-fact output in test fixtures.
- No visible reasoning summary as hidden-thought leakage.
