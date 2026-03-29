# Task Card

## Header

- Task Card ID: `P1-TC-CK-01`
- Phase: `1`
- Title: `Phase 1 constitution and requirement discipline`
- Status: `closed`
- Issued By: `Program Governor`
- Issued On: `2026-03-29 22:40 CEST`

## Role Assignment

- Active Build Role: `Constitution Keeper`
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
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - current placeholder files in `projects/agifcore_master/02_requirements/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/01_plan/HUMAN_THINKING_TARGET.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/INNOVATION_RULES.md`
  - `projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md`
  - `projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `projects/agifcore_master/02_requirements/BOTTLENECK_ESCALATION_RULES.md`
  - `projects/agifcore_master/02_requirements/DEPLOYMENT_PROFILES.md`
  - `projects/agifcore_master/02_requirements/DOMAIN_MATRIX.md`
  - `projects/agifcore_master/02_requirements/CONVERSATION_SCOPE.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - `projects/agifcore_master/02_requirements/MACHINE_ROLE_POLICY.md`
  - `projects/agifcore_master/02_requirements/PHASE_APPROVAL_RULES.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/P1-TC-CK-01_PHASE_1_REQUIREMENT_DISCIPLINE.md`
- Forbidden Files:
  - `projects/agifcore_master/03_design/*`
  - provenance files
  - `projects/agifcore_master/04_execution/*`
- Allowed Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/`
- Forbidden Folders:
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/04_execution/`

## Branch And Worktree

- Branch Name: `codex/tc-p1-tc-ck-01-phase-1-requirement-discipline`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P1-TC-CK-01`
- Rollback Tag Name: `rollback/P1-TC-CK-01/20260329-2240`

## Objective

- Goal: author the constitution-facing Phase 1 artifacts and replace the Phase 1 requirement placeholders with substantive draft content.
- Expected Outputs:
  - `SYSTEM_CONSTITUTION.md`
  - `HUMAN_THINKING_TARGET.md`
  - substantive Phase 1 drafts for all owned requirement files
- Non-Goals:
  - design-pack authoring
  - provenance authoring
  - runtime implementation
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `test -f projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `test -f projects/agifcore_master/01_plan/HUMAN_THINKING_TARGET.md`
  - `wc -l projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md projects/agifcore_master/02_requirements/INNOVATION_RULES.md projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md projects/agifcore_master/02_requirements/BOTTLENECK_ESCALATION_RULES.md projects/agifcore_master/02_requirements/DEPLOYMENT_PROFILES.md projects/agifcore_master/02_requirements/DOMAIN_MATRIX.md projects/agifcore_master/02_requirements/CONVERSATION_SCOPE.md projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md projects/agifcore_master/02_requirements/MACHINE_ROLE_POLICY.md projects/agifcore_master/02_requirements/PHASE_APPROVAL_RULES.md`
- Required Build Commands: `none`
- Required Verifier Paths: `none`
- Required Evidence Output Paths: `none`
- Required Demo Path: `direct inspection of the constitution artifacts and requirement-pack drafts`

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
