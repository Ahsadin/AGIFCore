# P10-TC-TRL-02 Phase 10 Verifiers And Evidence

## Header

- Task Card ID: `P10-TC-TRL-02`
- Phase: `10`
- Title: `Phase 10 Verifiers and Evidence`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Meta & Growth Pod Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `local_test_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
  - `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/`
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/`
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
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/`
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_evidence/`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/04_execution/*`
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_demo_bundle/*`
  - all Phase 11 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/`
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_demo_bundle/`

## Branch And Worktree

- Branch Name: `codex/tc-p10-tc-pg-02-phase-10-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P10-TC-TRL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the Phase 10 verifier family and machine-readable evidence package against the built runtime.
- Expected Outputs:
  - full Phase 10 verifier family under `05_testing/phase_10_meta_cognition_and_critique/`
  - machine-readable evidence under `06_outputs/phase_10_meta_cognition_and_critique/phase_10_evidence/`
- Non-Goals:
  - changing runtime logic
  - writing audit or validation records
  - writing the review demo bundle
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `yes`

## Verification

- Required Test Commands:
  - full Phase 10 verifier family
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique`
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
  - `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_evidence/phase_10_evidence_manifest.json`
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

1. Mirror the proven Phase 9 verifier and evidence pattern where it still fits.
2. Add one verifier per major Phase 10 subsystem.
3. Keep evidence machine-readable and tied to actual runtime outputs.
4. Add danger-zone checks for unsupported self-assertion, empty skepticism, and prose-only diagnosis.
5. Do not fix runtime logic directly; hand failures back to the active build pod.

## Cross-Checks

- No runtime authoring.
- No Phase 11 behavior.
- No Phase 12 behavior.
- No empty report files.
- No demo claims without evidence.
