# Task Card

## Header

- Task Card ID: `P8-TC-ACL-01`
- Phase: `8`
- Title: `Phase 8 Boundaries And Contracts`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles:
  - `Source Cartographer`
  - `Constitution Keeper`
  - `World & Conversation Pod Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `separate-session-required`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `separate-session-required`
- Required Reads:
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 6 and Phase 7 plans
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-SC-01_PHASE_8_PROVENANCE_AND_REUSE.md`
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-01_PHASE_8_BOUNDARIES_AND_CONTRACTS.md`
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
- Rollback Tag Name: `rollback/P8-TC-ACL-01/20260331-0000`

## Objective

- Goal:
  - own Phase 8 boundaries, allowed interfaces, forbidden leaks, and public reasoning-summary scope
- Expected Outputs:
  - explicit subsystem-only boundaries
  - allowed Phase 6 and Phase 7 interface list
  - forbidden Phase 9 and Phase 10 leak list
  - runtime-family implications for later execution
- Non-Goals:
  - redesigning kernel, memory, graph, simulator, conversation, or the team
  - implementation work
  - approval work
- Inherited Lineage Touched: `yes`
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
  - `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- each Phase 8 subsystem has a bounded responsibility
- allowed Phase 6 interfaces are explicit
- allowed Phase 7 interfaces are explicit
- forbidden Phase 9 and Phase 10 leaks are explicit
- no chain-of-thought theater is allowed through the visible summary surface
- rollback path is defined

## Work Method

1. define what belongs in each Phase 8 subsystem only
2. define allowed Phase 6 and Phase 7 interfaces
3. define forbidden Phase 9 and Phase 10 leaks
4. pass runtime-family implications to `Program Governor` and `World & Conversation Pod Lead`

## Cross-Checks

- no one mixed reasoning function
- no final response generation inside Phase 8
- no direct mutation of Phase 6 or Phase 7 state
- no chain-of-thought theater disguised as visible reasoning

## Exit Criteria

- boundary rules are explicit enough to verify later

## Handoff Target

`Program Governor` then `World & Conversation Pod Lead`

## No Approval Implied

Boundary framing is planning truth only.
