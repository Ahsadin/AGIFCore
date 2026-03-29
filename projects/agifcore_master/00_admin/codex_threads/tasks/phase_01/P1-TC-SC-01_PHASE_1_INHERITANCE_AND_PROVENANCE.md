# Task Card

## Header

- Task Card ID: `P1-TC-SC-01`
- Phase: `1`
- Title: `Phase 1 inheritance and provenance mapping`
- Status: `closed`
- Issued By: `Program Governor`
- Issued On: `2026-03-29 22:40 CEST`

## Role Assignment

- Active Build Role: `Source Cartographer`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4-mini`, `gpt-5.4`
- Build Pod Agent Session ID: `separate agent or session required`
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
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
  - relevant v1/tasklet/v2 lineage sources

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/P1-TC-SC-01_PHASE_1_INHERITANCE_AND_PROVENANCE.md`
- Forbidden Files:
  - `projects/agifcore_master/02_requirements/*`
  - `projects/agifcore_master/03_design/*`
  - `projects/agifcore_master/04_execution/*`
- Allowed Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/`
- Forbidden Folders:
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/04_execution/`

## Branch And Worktree

- Branch Name: `codex/tc-p1-tc-sc-01-phase-1-inheritance-and-provenance`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P1-TC-SC-01`
- Rollback Tag Name: `rollback/P1-TC-SC-01/20260329-2240`

## Objective

- Goal: author the Phase 1 inheritance, source-coverage, and runtime-rebuild mapping lane from the frozen source-freeze baseline.
- Expected Outputs:
  - `COMPONENT_CATALOG.md`
  - `SOURCE_INHERITANCE_MATRIX.md`
  - `RUNTIME_REBUILD_MAP.md`
- Non-Goals:
  - requirement-pack authoring
  - design-pack authoring
  - runtime code porting
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `test -f projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `test -f projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `test -f projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - `rg -n 'SRC-001|SRC-002|SRC-003|SRC-004' projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
- Required Build Commands: `none`
- Required Verifier Paths: `none`
- Required Evidence Output Paths: `none`
- Required Demo Path: `direct inspection of the inheritance matrix, component catalog, and runtime rebuild map`

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
