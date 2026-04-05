# Task Card

## Header

- Task Card ID: `P0-TC-ASA-01`
- Phase: `0`
- Title: `Audit Phase 0 archival and source-freeze artifacts`
- Status: `closed`
- Issued By: `Program Governor`
- Issued On: `2026-03-29 21:11 CEST`

## Role Assignment

- Active Build Role: `Anti-Shortcut Auditor`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4-mini`, `gpt-5.4`
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
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
  - `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/AUDIT_REPORT_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/P1-TC-PG-02_PHASE_0_BLOCKER_REMEDIATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-TC-PG-01_PHASE_0_PLAN_AND_GATE_RECONCILIATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-TC-CK-01_PHASE_0_ARCHIVAL_NOTE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-TC-SC-01_PHASE_0_SOURCE_FREEZE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-TC-TRL-01_PHASE_0_PROJECT_STRUCTURE_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-TC-REL-01_PHASE_0_REVIEW_SURFACE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-TC-VA-01_PHASE_0_VALIDATION_REQUEST.md`
  - `projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
  - `projects/agifcore_master/01_plan/AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md`
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
  - `projects/agifcore_master/01_plan/PROJECT_STRUCTURE_AUDIT.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-TC-ASA-01_PHASE_0_ARTIFACT_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-AUDIT-01_PHASE_0_ARTIFACT_AUDIT_REPORT.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - `projects/agifcore_master/02_requirements/*`
  - `projects/agifcore_master/03_design/*`
  - `projects/agifcore_master/04_execution/*`
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/02_requirements/`
  - `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p0-tc-asa-01-phase-0-plan-audit`
- Worktree Path: `.worktrees/P0-TC-ASA-01`
- Rollback Tag Name: `rollback/P0-TC-ASA-01/20260329-2124`

## Objective

- Goal: independently check that the canonical Phase 0 artifact set exists, that older `PHASE_00_*` files are treated only as noncanonical inputs, and that the phase gate checklist tells the truth without implying approval.
- Expected Outputs:
  - one audit report for the canonical Phase 0 artifact set
  - one explicit audit result: `pass`, `fail`, or `pass_with_blockers`
  - one recommended next step for Program Governor
- Non-Goals:
  - Phase 1 drafting
  - Phase 2 planning
  - runtime implementation
  - changing canonical planning, requirement, or design content
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `test -d projects/agifcore_master/00_admin`
  - `test -d projects/agifcore_master/01_plan`
  - `test -f projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
  - `test -f projects/agifcore_master/01_plan/AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md`
  - `test -f projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
  - `test -f projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
  - `test -f projects/agifcore_master/01_plan/PROJECT_STRUCTURE_AUDIT.md`
  - `rg -n 'noncanonical|AGIF v2|SRC-001|audit, governor verification, validation request, and separate user approval' projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md projects/agifcore_master/01_plan/AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md projects/agifcore_master/01_plan/PROJECT_STRUCTURE_AUDIT.md projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- Required Build Commands: `none`
- Required Verifier Paths: `none`
- Required Evidence Output Paths: `none`
- Required Demo Path: `direct inspection of the canonical Phase 0 plan, archival statement, source-freeze artifacts, project-structure audit, and the Phase 0 row in PHASE_GATE_CHECKLIST.md`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/P0-AUDIT-01_PHASE_0_PLAN_AND_ARTIFACT_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_00_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `n/a`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined
