# P10-TC-PG-02 Phase 10 Execution Control

## Header

- Task Card ID: `P10-TC-PG-02`
- Phase: `10`
- Title: `Phase 10 Execution Control`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Architecture & Contract Lead`, `Meta & Growth Pod Lead`, `Test & Replay Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `local_governor_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-PG-02_PHASE_10_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_EXECUTION_START_BRIEF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_GOVERNOR_VERIFICATION_RECORD.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p10-tc-pg-02-phase-10-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P10-TC-PG-02/<yyyymmdd-hhmm>`

## Objective

- Goal: control the full Phase 10 execution chain without letting phase truth drift or later-phase scope leak in.
- Expected Outputs:
  - this task card
  - the required Phase 10 handoff records when execution reaches those gates
- Non-Goals:
  - phase approval
  - Phase 11 implementation
  - Phase 12 implementation
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `yes`

## Verification

- Required Test Commands:
  - full Phase 10 verifier family after TRL lands
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_self_model.py`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_meta_cognition_layer.py`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_attention_redirect.py`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_meta_cognition_observer.py`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_skeptic_counterexample.py`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_strategy_journal.py`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_thinker_tissue.py`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_surprise_engine.py`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_theory_fragments.py`
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_weak_answer_diagnosis.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_demo_bundle/`

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

1. Keep Phase 10 status truthful as `open` throughout execution.
2. Open and maintain execution task cards before runtime code and before any verifier or evidence pass.
3. Require runtime, verifier, evidence, demo, audit, governor verification, and validation loops to complete before any review request is drafted.
4. Apply the extra Meta & Growth danger-zone audit and stronger Governor review before validation.
5. Stop only when the full Phase 10 package is ready for final user review.

## Cross-Checks

- No Phase 11 start.
- No Phase 12 start.
- No live external search execution.
- No phase approval implied.
- No report text accepted as proof by itself.
