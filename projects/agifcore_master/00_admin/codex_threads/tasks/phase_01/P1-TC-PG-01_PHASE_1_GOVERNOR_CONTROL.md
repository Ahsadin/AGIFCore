# Task Card

## Header

- Task Card ID: `P1-TC-PG-01`
- Phase: `1`
- Title: `Phase 1 governor control and gate alignment`
- Status: `ready_for_user_review`
- Issued By: `Program Governor`
- Issued On: `2026-03-29 22:40 CEST`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Constitution Keeper`, `Architecture & Contract Lead`
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
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
  - `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/PROOF_DOMAIN_MATRIX.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/P1-TC-PG-01_PHASE_1_GOVERNOR_CONTROL.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/02_requirements/*`
  - `projects/agifcore_master/03_design/*`
  - `projects/agifcore_master/04_execution/*`
  - provenance files owned by `SC`
- Allowed Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/`
- Forbidden Folders:
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/04_execution/`

## Branch And Worktree

- Branch Name: `codex/tc-p1-tc-pg-01-phase-1-governor-control`
- Worktree Path: `none`
- Rollback Tag Name: `rollback/P1-TC-PG-01/20260329-2240`

## Objective

- Goal: control the frozen Phase 1 execution order, open the Phase 1 task-card set, and later author the Governor-owned Phase 1 planning files when the baseline says they are ready.
- Expected Outputs:
  - active/inactive role control for Phase 1
  - Governor-owned Phase 1 files only when their entry conditions are met
  - truthful gate and closure alignment
- Non-Goals:
  - requirement-pack authoring
  - design-pack authoring
  - provenance authoring
  - runtime implementation
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `test -f projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - `test -f projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `find projects/agifcore_master/00_admin/codex_threads/tasks/phase_01 -maxdepth 1 -type f | sort`
- Required Build Commands: `none`
- Required Verifier Paths: `none`
- Required Evidence Output Paths: `none`
- Required Demo Path: `direct inspection of the Governor-owned Phase 1 files and the Phase 1 task-card set`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/P1-AUDIT-01_PHASE_1_ARTIFACT_COVERAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_01_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_01_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_01_USER_VERDICT.md`
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
