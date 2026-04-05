# P9-TC-TRL-02 Phase 9 Verifiers and Evidence

## Header

- Task Card ID: `P9-TC-TRL-02`
- Phase: `9`
- Title: `Phase 9 Verifiers and Evidence`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `World & Conversation Pod Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `019d44ad-31ec-7df1-98e3-8a6305819aa9`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
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
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/`
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/*`
  - `projects/agifcore_master/04_execution/*`
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/*`
  - all Phase 10 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/`
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/`

## Branch And Worktree

- Branch Name: `codex/tc-p9-tc-pg-02-phase-9-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P9-TC-TRL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the Phase 9 verifier family and machine-readable evidence package against the built runtime.
- Expected Outputs:
  - full Phase 9 verifier family under `05_testing/phase_09_rich_expression_and_composition/`
  - machine-readable evidence under `06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/`
- Non-Goals:
  - changing runtime logic
  - writing audit or validation records
  - writing the review demo bundle
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 9 verifier family
- Required Build Commands:
  - `python3 -m compileall projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_teaching.py`
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_comparison.py`
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_planning.py`
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_synthesis.py`
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_analogy.py`
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_concept_composition.py`
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_cross_domain_composition.py`
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/verify_phase_09_audience_aware_explanation_quality.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_evidence_manifest.json`
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

1. Mirror the proven Phase 8 verifier and evidence pattern where it still fits.
2. Add one verifier per rich-expression lane.
3. Keep evidence machine-readable and tied to actual runtime outputs.
4. Add fail-closed checks for unsupported analogy and unsupported cross-domain composition.
5. Do not fix runtime logic directly; hand failures back to the active build pod.

## Cross-Checks

- No runtime authoring.
- No Phase 10 behavior.
- No Phase 11 behavior.
- No empty report files.
- No demo claims without evidence.
