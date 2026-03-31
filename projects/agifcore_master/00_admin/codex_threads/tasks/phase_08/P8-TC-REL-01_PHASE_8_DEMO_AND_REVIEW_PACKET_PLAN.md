# Task Card

## Header

- Task Card ID: `P8-TC-REL-01`
- Phase: `8`
- Title: `Phase 8 Demo And Review Packet Plan`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles:
  - `Test & Replay Lead`
  - `Program Governor`
  - `Validation Agent`
  - `Anti-Shortcut Auditor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `separate-session-required`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `separate-session-required`
- Required Reads:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 6 and Phase 7 demo bundles
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-TRL-01_PHASE_8_TEST_AND_EVIDENCE_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-REL-01_PHASE_8_DEMO_AND_REVIEW_PACKET_PLAN.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-pg-01-phase-8-plan`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P8-TC-REL-01/20260331-0000`

## Objective

- Goal:
  - define the later Phase 8 demo-bundle shape and review packet surfaces
- Expected Outputs:
  - demo bundle layout
  - science explanation demo surface
  - bounded live-fact demo surface
  - ordered user review packet
- Non-Goals:
  - release execution
  - public claims
  - demo acceptance
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none in this planning task
- Required Build Commands:
  - none
- Required Verifier Paths:
  - later `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
- Required Evidence Output Paths:
  - later `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Required Demo Path:
  - later `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_demo_index.md`

## Handoff Records

- Audit Report Path:
  - later `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ASA-01_PHASE_8_PLAN_AUDIT.md`
- Extra Audit Report Path:
  - `n/a`
- Governor Verification Record Path:
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_VALIDATION_REQUEST.md`
- User Verdict Path:
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path:
  - later `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_demo_index.md`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- demo bundle layout is exact
- science explanation demo surface is exact
- bounded live-fact demo surface is exact
- review packet order is exact
- no public-release packaging creep exists
- rollback path is defined

## Work Method

1. define the demo bundle layout
2. define the science explanation demo surface
3. define the bounded live-fact demo surface
4. define the review packet order for the user

## Cross-Checks

- demos must stay inspectable from files alone
- no demo may imply acceptance or phase completion
- no public-release packaging creep

## Exit Criteria

- later review packet is exact, ordered, and bounded

## Handoff Target

`Program Governor` then `Validation Agent`

## No Approval Implied

Demo-package planning is not demo acceptance.
