# P8-TC-PG-02 Phase 8 Execution Control

## Header

- Task Card ID: `P8-TC-PG-02`
- Phase: `8`
- Title: `Phase 8 Execution Control`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Architecture & Contract Lead`, `World & Conversation Pod Lead`, `Test & Replay Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-PG-02_PHASE_8_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_EXECUTION_START_BRIEF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_GOVERNOR_VERIFICATION_RECORD.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-wcpl-02-phase-8-science-world-awareness-implementation`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P8-TC-PG-02/<yyyymmdd-hhmm>`

## Objective

- Goal: control the full Phase 8 execution chain without letting phase truth drift or later-phase scope leak in.
- Expected Outputs:
  - this task card
  - the required Phase 8 handoff records when execution reaches those gates
- Non-Goals:
  - phase approval
  - Phase 9 implementation
  - Phase 10 implementation
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 8 verifier family after TRL lands
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_scientific_priors.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_entity_request_inference.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_world_region_selection.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_causal_chain_reasoning.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_bounded_current_world_reasoning.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_visible_reasoning_summaries.py`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_science_reflection.py`
- Required Build Commands:
  - `n/a`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-AUDIT-01_PHASE_8_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_USER_VERDICT.md`
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

1. Keep Phase 8 status truthful as `open` throughout execution.
2. Open and maintain task cards before runtime code and before any verifier or evidence pass.
3. Require runtime, verifier, evidence, demo, audit, governor verification, and validation loops to complete before any review request is drafted.
4. Stop only when the full Phase 8 package is ready for final user review.

## Cross-Checks

- No Phase 9 start.
- No Phase 10 start.
- No live external search execution.
- No phase approval implied.
- No report text accepted as proof by itself.
