# Task Card

## Header

- Task Card ID: `P8-TC-TRL-01`
- Phase: `8`
- Title: `Phase 8 Test And Evidence Plan`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles:
  - `Release & Evidence Lead`
  - `Program Governor`
  - `Validation Agent`
  - `Anti-Shortcut Auditor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `separate-session-required`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `separate-session-required`
- Required Reads:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 6 and Phase 7 verifier families and evidence bundles
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-TRL-01_PHASE_8_TEST_AND_EVIDENCE_PLAN.md`
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
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P8-TC-TRL-01/20260331-0000`

## Objective

- Goal:
  - define the Phase 8 verifier, evidence, and closure-check family
- Expected Outputs:
  - one verifier per major Phase 8 subsystem group
  - evidence report and manifest plan
  - failure signatures for every closure requirement
- Non-Goals:
  - runtime behavior implementation
  - writing verifier code in this run
  - evidence generation in this run
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

- verifier families are planned
- evidence reports and manifest contents are planned
- budget-bound, anti-bluff, anti-theater, and anti-live-fact-guessing checks are planned
- failure signatures are planned
- no runtime behavior is implemented through testing design
- rollback path is defined

## Work Method

1. define one verifier per major Phase 8 subsystem group
2. define evidence reports and manifest contents
3. define budget-bound, anti-bluff, anti-theater, and anti-live-fact-guessing checks
4. define failure signatures for each closure requirement

## Cross-Checks

- tests must verify separation between priors, inference, region selection, causal chains, current-world reasoning, visible summaries, and reflection
- causal-chain outputs must be machine-checkable
- bounded current-world reasoning must enforce freshness honesty
- visible reasoning summaries must stay public-summary-only

## Exit Criteria

- later test and evidence path is decision-complete

## Handoff Target

`Release & Evidence Lead` then `Program Governor`

## No Approval Implied

Verification planning does not earn the phase.
