# Task Card

## Header

- Task Card ID: `P8-TC-ASA-01`
- Phase: `8`
- Title: `Phase 8 Plan Audit`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Anti-Shortcut Auditor`
- Supporting Roles:
  - `Program Governor`
- Allowed Models: `gpt-5.4 mini`, `gpt-5.4 nano` utility helpers only
- Build Pod Agent Session ID: `separate-session-required`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `separate-session-required`
- Required Reads:
  - full `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-SC-01_PHASE_8_PROVENANCE_AND_REUSE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-01_PHASE_8_BOUNDARIES_AND_CONTRACTS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-TRL-01_PHASE_8_TEST_AND_EVIDENCE_PLAN.md`
  - relevant approved Phase 6 and Phase 7 plans

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ASA-01_PHASE_8_PLAN_AUDIT.md`
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
- Rollback Tag Name: `rollback/P8-TC-ASA-01/20260331-0000`

## Objective

- Goal:
  - audit the Phase 8 planning package for fake completeness, greenfield recreation, and fake-science risk
- Expected Outputs:
  - explicit blocker list or a no-blocker audit result
  - coverage check for all required sections and subsystem mappings
- Non-Goals:
  - rewriting the plan
  - authoring implementation
  - approving the phase
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none
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
  - `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- all required Phase 8 plan sections are checked
- each major subsystem has a source basis and disposition
- no prose-only causal chain is being passed off as design
- no Phase 9 or Phase 10 behavior is smuggled in
- no approval or completion claim is implied
- rollback path is defined

## Work Method

1. check that all required sections exist
2. check that each major subsystem has a source basis and disposition
3. check that no one mixed reasoning function or prose-only causal chain is being passed off as design
4. check that no approval or completion claim is implied

## Cross-Checks

- no blind rewrite where a plausible substrate exists
- no silent omission of bounded current-world reasoning, visible reasoning summaries, or science reflection
- no Phase 9 or Phase 10 behavior smuggled in
- no empty report path or unverifiable demo plan

## Exit Criteria

- all blockers are either cleared or explicitly raised

## Handoff Target

`Program Governor`

## No Approval Implied

Audit pass is not phase approval.
