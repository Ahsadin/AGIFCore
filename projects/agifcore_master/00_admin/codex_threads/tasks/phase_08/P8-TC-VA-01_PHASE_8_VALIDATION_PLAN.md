# Task Card

## Header

- Task Card ID: `P8-TC-VA-01`
- Phase: `8`
- Title: `Phase 8 Validation Plan`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Validation Agent`
- Supporting Roles:
  - `Program Governor`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `separate-session-required`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `separate-session-required`
- Required Reads:
  - full `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - audit output
  - governor verification output
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-VA-01_PHASE_8_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_VALIDATION_REQUEST.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-pg-01-phase-8-plan`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P8-TC-VA-01/20260331-0000`

## Objective

- Goal:
  - validate the final Phase 8 planning package before user review
- Expected Outputs:
  - validation-plan record
  - later review-request path and scope
- Non-Goals:
  - authoring plan content
  - runtime behavior
  - phase approval
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ASA-01_PHASE_8_PLAN_AUDIT.md`
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

- plan is checked for decision completeness
- every closure requirement has a later artifact path
- user-review demos are inspectable and truthful
- no author and validator role collision exists
- no implied approval exists
- rollback path is defined

## Work Method

1. confirm the plan is decision-complete
2. confirm every required closure requirement has a later artifact path
3. confirm the user-review demos are inspectable and truthful
4. prepare the later review request only after audit and governor verification exist

## Cross-Checks

- no author and validator role collision
- no missing review surface
- no implied approval

## Exit Criteria

- review request scope is exact and inspectable

## Handoff Target

`Program Governor`

## No Approval Implied

Validation asks for review and does not mark the phase earned.
