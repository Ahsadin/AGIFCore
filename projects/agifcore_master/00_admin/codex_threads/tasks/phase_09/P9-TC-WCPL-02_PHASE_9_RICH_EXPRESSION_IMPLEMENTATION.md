# P9-TC-WCPL-02 Phase 9 Rich Expression Implementation

## Header

- Task Card ID: `P9-TC-WCPL-02`
- Phase: `9`
- Title: `Phase 9 Rich Expression Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `World & Conversation Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `019d44ac-9a9f-7d63-ac3c-0bb5832b7be0`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-ACL-01_PHASE_9_BOUNDARIES_AND_CONTRACTS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-WCPL-01_PHASE_9_EXECUTION_DECOMPOSITION.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
  - `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/contracts.py`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/teaching.py`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/comparison.py`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/planning.py`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/synthesis.py`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/analogy.py`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/concept_composition.py`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/cross_domain_composition.py`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/audience_aware_explanation_quality.py`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/rich_expression_turn.py`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/__init__.py`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/05_testing/*`
  - `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
  - all Phase 7 and Phase 8 runtime files
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p9-tc-pg-02-phase-9-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P9-TC-WCPL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the full governed Phase 9 runtime package above approved Phase 7 and Phase 8 inputs and below Phase 10 and Phase 11.
- Expected Outputs:
  - complete Phase 9 runtime package under `04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/`
- Non-Goals:
  - changing Phase 7 or Phase 8 runtime truth
  - implementing Phase 10 or Phase 11
  - writing verifiers, evidence, demos, audit, or validation artifacts
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - hand off to `Test & Replay Lead`
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression`
- Required Verifier Paths:
  - hand off to `Test & Replay Lead`
- Required Evidence Output Paths:
  - hand off to `Test & Replay Lead`
- Required Demo Path:
  - hand off to `Release & Evidence Lead`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-AUDIT-01_PHASE_9_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-ACL-02_PHASE_9_BOUNDARY_CHECK.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_USER_VERDICT.md`
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

## Work Method

1. Build the typed contracts first.
2. Implement each rich-expression lane as a separate module instead of one giant style engine.
3. Keep all Phase 7 and Phase 8 inputs read-only.
4. Emit a Phase 9 overlay turn record with explicit Phase 9 trace refs where applicable.
5. Fail closed when analogy or composition is unsupported.

## Cross-Checks

- No Phase 10 behavior.
- No Phase 11 behavior.
- No live external search execution.
- No support-state upgrades by language alone.
- No direct mutation of Phase 7 or Phase 8 state.
