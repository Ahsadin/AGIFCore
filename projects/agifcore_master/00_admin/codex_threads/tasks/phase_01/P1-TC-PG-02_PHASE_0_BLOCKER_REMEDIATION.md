# Task Card

## Header

- Task Card ID: `P1-TC-PG-02`
- Phase: `1`
- Title: `Resolve carried Phase 0 blocker artifacts`
- Status: `closed`
- Issued By: `Program Governor`
- Issued On: `2026-03-29 20:59 CEST`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `none`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `n/a (governance-only task; no build pod activated)`
- Merge Arbiter Session ID: `n/a`
- Validation Agent Session ID: `n/a`
- Required Reads:
  - `AGENTS.md`
  - `projects/agifcore_master/AGENTS.override.md`
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_01_PLAN_FREEZE_HANDOFF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/GOVERNOR_NEXT_THREAD_BRIEF.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
  - `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/P1-TC-PG-02_PHASE_0_BLOCKER_REMEDIATION.md`
  - `projects/agifcore_master/01_plan/PHASE_00_AGIF_V2_ARCHIVAL_NOTE.md`
  - `projects/agifcore_master/01_plan/PHASE_00_SOURCE_FREEZE_INVENTORY.md`
  - `projects/agifcore_master/01_plan/PHASE_00_SOURCE_FREEZE_METHOD.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/CHANGELOG.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - `projects/agifcore_master/02_requirements/*`
  - `projects/agifcore_master/03_design/*`
  - `projects/agifcore_master/04_execution/*`
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/`
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/`
- Forbidden Folders:
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p1-tc-pg-02-phase-0-blocker-remediation`
- Worktree Path: `none (branch-only work in the primary checkout)`
- Rollback Tag Name: `rollback/P1-TC-PG-02/20260329-2059`

## Objective

- Goal: create the missing distinct Phase 0 archival and source-freeze artifacts and update the checklist so the blocker state is explicit before any broader Phase 1 execution starts.
- Expected Outputs:
  - one scoped Program Governor task card
  - one distinct AGIF v2 archival note artifact
  - one distinct source-freeze inventory artifact
  - one distinct source-freeze method artifact
  - one checklist update that keeps user-approval truth explicit
  - one changelog entry for the blocker-remediation step
- Non-Goals:
  - Phase 2 planning
  - team redesign
  - Phase 1 requirement-pack drafting
  - Phase 1 design-pack drafting
  - runtime implementation
  - any completion or approval claim
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `test -f projects/agifcore_master/01_plan/PHASE_00_AGIF_V2_ARCHIVAL_NOTE.md`
  - `test -f projects/agifcore_master/01_plan/PHASE_00_SOURCE_FREEZE_INVENTORY.md`
  - `test -f projects/agifcore_master/01_plan/PHASE_00_SOURCE_FREEZE_METHOD.md`
  - `rg -n 'AGIF v2|source freeze|explicit user approval or waiver' projects/agifcore_master/01_plan/PHASE_00_AGIF_V2_ARCHIVAL_NOTE.md projects/agifcore_master/01_plan/PHASE_00_SOURCE_FREEZE_INVENTORY.md projects/agifcore_master/01_plan/PHASE_00_SOURCE_FREEZE_METHOD.md projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- Required Build Commands: `none`
- Required Verifier Paths: `none`
- Required Evidence Output Paths: `none`
- Required Demo Path: `direct file inspection of the Phase 0 blocker artifacts and the updated phase gate checklist`

## Handoff Records

- Audit Report Path: `n/a for this blocker-remediation task`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `n/a for this task-only remediation step`
- Validation Request Path: `n/a`
- User Verdict Path: `n/a`
- Additional Human Demo Checkpoint Path: `n/a`

## Approval Chain

- Auditor: `not started`
- Merge Arbiter: `not started`
- Program Governor: `active`
- User: `pending separate Phase 0 approval after audit and validation`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined
