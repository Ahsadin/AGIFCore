# Task Card

## Header

- Task Card ID: `P0-TC-PG-01`
- Phase: `0`
- Title: `Phase 0 plan and gate reconciliation`
- Status: `closed`
- Issued By: `Program Governor`
- Issued On: `2026-03-29 21:24 CEST`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Constitution Keeper`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `n/a`
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

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-TC-PG-01_PHASE_0_PLAN_AND_GATE_RECONCILIATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/*`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - `projects/agifcore_master/02_requirements/*`
  - `projects/agifcore_master/03_design/*`
  - `projects/agifcore_master/04_execution/*`
- Allowed Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/`
- Forbidden Folders:
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/04_execution/`

## Branch And Worktree

- Branch Name: `codex/tc-p0-tc-pg-01-phase-0-reset-source-freeze`
- Worktree Path: `none`
- Rollback Tag Name: `rollback/P0-TC-PG-01/20260329-2124`

## Objective

- Goal: author the canonical Phase 0 plan, open the Phase 0 role-task map, and reconcile truthful Phase 0 gate language.
- Expected Outputs:
  - `projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
  - a Phase 0 task-card set
  - a truthful `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` Phase 0 note
- Non-Goals:
  - Phase 1 execution
  - Phase 2 planning
  - runtime implementation
  - approval or freeze claims
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `test -f projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
  - `test -f projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `find projects/agifcore_master/00_admin/codex_threads/tasks/phase_00 -maxdepth 1 -type f | sort`
- Required Build Commands: `none`
- Required Verifier Paths: `none`
- Required Evidence Output Paths: `none`
- Required Demo Path: `direct inspection of the canonical Phase 0 plan and the Phase 0 gate row`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-AUDIT-01_PHASE_0_PLAN_AND_ARTIFACT_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive by default`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined
