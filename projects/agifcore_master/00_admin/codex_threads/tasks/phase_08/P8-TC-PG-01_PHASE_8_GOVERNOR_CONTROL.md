# Task Card

## Header

- Task Card ID: `P8-TC-PG-01`
- Phase: `8`
- Title: `Phase 8 Governor Control`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles:
  - `Constitution Keeper`
  - `Source Cartographer`
  - `Architecture & Contract Lead`
  - `World & Conversation Pod Lead`
  - `Test & Replay Lead`
  - `Anti-Shortcut Auditor`
  - `Validation Agent`
  - `Release & Evidence Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `governor-thread`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `separate-session-required`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
  - `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-PG-01_PHASE_8_GOVERNOR_CONTROL.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
  - earlier phase-truth files except to report a prerequisite mismatch
- Allowed Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-pg-01-phase-8-plan`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P8-TC-PG-01/20260331-0000`

## Objective

- Goal:
  - own prerequisite truth, the Phase 8 plan, task-card map, artifact matrix, budget envelope, and closure chain
- Expected Outputs:
  - canonical Phase 8 planning file
  - Phase 8 planning task-card set
  - locked role map, workstreams, and closure mapping
- Non-Goals:
  - Phase 8 runtime code
  - Phase 8 verifier code
  - Phase 8 evidence generation
  - Phase 9 planning
  - any commit, freeze, or approval action
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - confirm Phase 7 remains `approved` and Phase 8 remains `open`
  - confirm `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md` exists
  - confirm the Phase 8 task-card files exist under `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/`
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `n/a`
- Required Evidence Output Paths:
  - `n/a`
- Required Demo Path:
  - `n/a`

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

- Phase 7 approval truth is verified directly
- active, consult-only, and inactive roles are fixed
- the Phase 8 plan is section-complete and decision-complete
- future artifact families and closure mapping are explicit
- no runtime, testing, or output families are created in this task
- rollback path is defined

## Work Method

1. verify Phase 7 approval truth
2. lock active, consult-only, and inactive roles
3. consolidate reuse, boundary, runtime-family, verifier, and demo outputs
4. lock future artifact families and closure mapping

## Cross-Checks

- no Phase 9 planning
- no Phase 10 planning
- no live external search execution
- no approval language

## Exit Criteria

- the plan is section-complete and decision-complete

## Handoff Target

`Anti-Shortcut Auditor`

## No Approval Implied

This task ends at plan readiness only. Phase 8 remains `open`.
