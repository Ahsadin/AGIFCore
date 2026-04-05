# P12-TC-TRL-02 Phase 12 Verifiers And Evidence

## Header

- Task Card ID: `P12-TC-TRL-02`
- Phase: `12`
- Title: `Phase 12 Verifiers and Evidence`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

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
  - `projects/agifcore_master/01_plan/PHASE_12_STRUCTURAL_GROWTH.md`
  - `projects/agifcore_master/04_execution/phase_12_structural_growth/`
  - `projects/agifcore_master/05_testing/phase_11_governed_self_improvement/`
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
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/`
  - `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_evidence/`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/04_execution/*`
  - `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_demo_bundle/*`
  - all Phase 13 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/`
  - `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_demo_bundle/`

## Branch And Worktree

- Branch Name: `codex/tc-p12-tc-pg-02-phase-12-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P12-TC-TRL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the Phase 12 verifier family and machine-readable evidence package against the built runtime.
- Expected Outputs:
  - full Phase 12 verifier family under `05_testing/phase_12_structural_growth/`
  - machine-readable evidence under `06_outputs/phase_12_structural_growth/phase_12_evidence/`
- Non-Goals:
  - changing runtime logic
  - writing audit or validation records
  - writing the review demo bundle
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `yes`

## Verification

- Required Test Commands:
  - full Phase 12 verifier family
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/05_testing/phase_12_structural_growth`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_self_model_feedback.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_reflection_control.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_self_reorganization.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_domain_genesis.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_theory_formation.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_procedure_tool_invention.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_curiosity_gap_selection.py`
  - `projects/agifcore_master/05_testing/phase_12_structural_growth/verify_phase_12_structural_growth_cycle.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_evidence/phase_12_evidence_manifest.json`
- Required Demo Path:
  - hand off to `Release & Evidence Lead`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-AUDIT-01_PHASE_12_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-AUDIT-02_PHASE_12_DANGER_ZONE_AUDIT_REPORT.md`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_ADDITIONAL_HUMAN_DEMO_CHECKPOINT.md`

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

1. Add one verifier per major Phase 12 subsystem and one cycle verifier.
2. Keep evidence machine-readable and tied to actual runtime outputs.
3. Add danger-zone checks for uncontrolled mutation, label-only domain genesis, note-only theory growth, and hidden procedure execution.
4. Do not fix runtime logic directly; hand failures back to the active build pod.

## Cross-Checks

- No runtime authoring.
- No Phase 13 behavior.
- No Phase 14 behavior.
- No empty report files.
- No demo claims without evidence.
