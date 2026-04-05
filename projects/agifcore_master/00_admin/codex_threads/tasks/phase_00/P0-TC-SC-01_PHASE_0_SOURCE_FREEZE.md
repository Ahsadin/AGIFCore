# Task Card

## Header

- Task Card ID: `P0-TC-SC-01`
- Phase: `0`
- Title: `Phase 0 source-freeze inventory and method`
- Status: `closed`
- Issued By: `Program Governor`
- Issued On: `2026-03-29 21:24 CEST`

## Role Assignment

- Active Build Role: `Source Cartographer`
- Supporting Roles: `Program Governor`, `Constitution Keeper`
- Allowed Models: `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5.4`
- Build Pod Agent Session ID: `n/a`
- Merge Arbiter Session ID: `n/a`
- Validation Agent Session ID: `n/a`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-TC-SC-01_PHASE_0_SOURCE_FREEZE.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - `projects/agifcore_master/02_requirements/*`
  - `projects/agifcore_master/03_design/*`
  - `projects/agifcore_master/04_execution/*`
- Allowed Folders:
  - `projects/agifcore_master/01_plan/`
- Forbidden Folders:
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/04_execution/`

## Branch And Worktree

- Branch Name: `codex/tc-p0-tc-sc-01-phase-0-source-freeze`
- Worktree Path: `.worktrees/P0-TC-SC-01`
- Rollback Tag Name: `rollback/P0-TC-SC-01/20260329-2124`

## Objective

- Goal: author the canonical source-freeze inventory and source-freeze method artifacts.
- Expected Outputs:
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
- Non-Goals:
  - row-by-row inheritance mapping
  - component catalog work
  - runtime rebuild mapping
  - runtime implementation
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `test -f projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
  - `test -f projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
  - `rg -n 'SRC-001|SRC-002|SRC-003|SRC-004|rebuild_clean|port_with_provenance|adapt_for_research_only|reject' projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
- Required Build Commands: `none`
- Required Verifier Paths: `none`
- Required Evidence Output Paths: `none`
- Required Demo Path: `direct inspection of the source-pool table and source-freeze method`

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
