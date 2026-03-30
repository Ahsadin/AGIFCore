# Task Card

## Header

- Task Card ID: `P1-TC-ACL-01`
- Phase: `1`
- Title: `Phase 1 architecture and contract freezing`
- Status: `closed`
- Issued By: `Program Governor`
- Issued On: `2026-03-29 22:40 CEST`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles: `Program Governor`, `Constitution Keeper`
- Allowed Models: `gpt-5.4`
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
  - current placeholder files in `projects/agifcore_master/03_design/`
  - later `SC` and `CK` first-pass outputs once available

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/03_design/ARCHITECTURE_OVERVIEW.md`
  - `projects/agifcore_master/03_design/CELL_FAMILIES.md`
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
  - `projects/agifcore_master/03_design/SKILL_GRAPH_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
  - `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
  - `projects/agifcore_master/03_design/PUBLIC_RELEASE_MODEL.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/P1-TC-ACL-01_PHASE_1_ARCHITECTURE_AND_CONTRACT.md`
- Forbidden Files:
  - `projects/agifcore_master/02_requirements/*`
  - provenance files
  - `projects/agifcore_master/04_execution/*`
- Allowed Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/`
- Forbidden Folders:
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/04_execution/`

## Branch And Worktree

- Branch Name: `codex/tc-p1-tc-acl-01-phase-1-architecture-and-contract`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P1-TC-ACL-01`
- Rollback Tag Name: `rollback/P1-TC-ACL-01/20260329-2240`

## Objective

- Goal: start the Phase 1 architecture lane and replace design placeholders with substantive drafts aligned to the frozen master plan.
- Expected Outputs:
  - `TRACE_CONTRACT.md`
  - substantive drafts across the full design pack
- Non-Goals:
  - provenance authoring
  - requirement-pack authoring
  - runtime implementation
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `test -f projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `wc -l projects/agifcore_master/03_design/*.md`
- Required Build Commands: `none`
- Required Verifier Paths: `none`
- Required Evidence Output Paths: `none`
- Required Demo Path: `direct inspection of the trace contract and design-pack drafts`

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
