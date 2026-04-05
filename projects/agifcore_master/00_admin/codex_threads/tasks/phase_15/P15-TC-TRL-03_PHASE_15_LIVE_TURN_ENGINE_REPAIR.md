# P15-TC-TRL-03 Phase 15 Live Turn Engine Repair

- Task Card ID: `P15-TC-TRL-03`
- Phase: `15`
- Title: `Broaden the real live turn engine without demo-only shortcuts`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-04-01`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Architecture & Contract Lead`, `Anti-Shortcut Auditor`, `Validation Agent`, `Release & Evidence Lead`
- Allowed Models: `gpt-5.4`, `gpt-5.3-codex`, `gpt-5.4-mini`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
  - `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/interactive_turn.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/product_runtime_shell.py`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_interactive_chat.py`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/run_phase_15_interactive_chat_demo.py`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/phase_15_interactive_chat_report.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/phase_15_reproducibility_report.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/phase_15_closure_audit_report.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/phase_15_evidence_manifest.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_demo_bundle/INTERACTIVE_CHAT.md`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle/REVIEW_FIRST.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-AUDIT-01_PHASE_15_FINAL_PACKAGE_AUDIT_REPORT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_VALIDATION_REQUEST.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 16 artifacts
  - unrelated earlier-phase runtime modules unless direct integration is required

## Objective

- Goal:
  - replace the shallow bounded shell behavior with a broader real live AGIFCore turn engine inside the existing runtime path
- Expected Outputs:
  - broader question handling in the real interactive path
  - selective and truthful phase-usage evidence
  - updated verifier matrix and refreshed Phase 15 review surfaces
- Non-Goals:
  - Phase 16 work
  - external knowledge integration
  - hardcoded prompt-answer tables
  - phase approval or closure

## Verification

- Required Test Commands:
  - `python3 -m compileall projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime`
  - `python3 -m compileall projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit`
  - `python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_interactive_chat.py`
  - `python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_reproducibility.py`
  - `python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_closure_audit.py`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_demo_bundle/launch_phase_15_interactive_chat.sh`

## No Approval Implied

This task card governs a live-turn repair only.
It does not approve or close Phase 15.
