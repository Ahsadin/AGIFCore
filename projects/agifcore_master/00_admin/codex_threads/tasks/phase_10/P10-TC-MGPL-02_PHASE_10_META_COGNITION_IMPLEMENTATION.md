# P10-TC-MGPL-02 Phase 10 Meta-Cognition Implementation

## Header

- Task Card ID: `P10-TC-MGPL-02`
- Phase: `10`
- Title: `Phase 10 Meta-Cognition Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Meta & Growth Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `local_build_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-ACL-01_PHASE_10_BOUNDARIES_AND_CONTRACTS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-MGPL-01_PHASE_10_EXECUTION_DECOMPOSITION.md`
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
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/contracts.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/self_model.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/meta_cognition_layer.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/attention_redirect.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/meta_cognition_observer.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/skeptic_counterexample.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/strategy_journal.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/thinker_tissue.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/surprise_engine.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/theory_fragments.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/weak_answer_diagnosis.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/meta_cognition_turn.py`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/__init__.py`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/05_testing/*`
  - `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
  - all Phase 7, 8, and 9 runtime files
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p10-tc-pg-02-phase-10-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P10-TC-MGPL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the full governed Phase 10 runtime package above approved Phase 7, Phase 8, and Phase 9 inputs and below Phase 11 and Phase 12.
- Expected Outputs:
  - complete Phase 10 runtime package under `04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/`
- Non-Goals:
  - changing Phase 7, Phase 8, or Phase 9 runtime truth
  - implementing Phase 11 or Phase 12
  - writing verifiers, evidence, demos, audit, or validation artifacts
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `yes`

## Verification

- Required Test Commands:
  - hand off to `Test & Replay Lead`
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition`
- Required Verifier Paths:
  - hand off to `Test & Replay Lead`
- Required Evidence Output Paths:
  - hand off to `Test & Replay Lead`
- Required Demo Path:
  - hand off to `Release & Evidence Lead`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-01_PHASE_10_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-02_PHASE_10_DANGER_ZONE_AUDIT_REPORT.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_USER_VERDICT.md`
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
2. Implement each Phase 10 subsystem as a separate module instead of one giant introspection engine.
3. Keep all Phase 7, Phase 8, and Phase 9 inputs read-only.
4. Emit a Phase 10 overlay turn record with explicit Phase 10 trace refs.
5. Fail closed when contradiction or weak-support conditions require honest fallback.

## Cross-Checks

- No Phase 11 behavior.
- No Phase 12 behavior.
- No hidden self-improvement path.
- No direct mutation of Phase 7, Phase 8, or Phase 9 state.
- No runtime truth claims based only on polished critique language.
