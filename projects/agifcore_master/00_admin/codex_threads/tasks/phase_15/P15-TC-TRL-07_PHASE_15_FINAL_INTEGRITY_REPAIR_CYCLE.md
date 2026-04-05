# Task Card

## Header

- Task Card ID: `P15-TC-TRL-07`
- Phase: `15`
- Title: `Final integrity repair cycle for bounded-intelligence closeout`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-04-04`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `architecture_contract`, `anti_shortcut_auditor`, `validation_agent`, `release_evidence`
- Allowed Models: `gpt-5.4`, `gpt-5.3-codex`, `gpt-5.4-mini`
- Build Pod Agent Session ID: `governor-main-thread`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `assigned_later_if_needed`
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
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/BOUNDED_INTELLIGENCE_GATE_SPEC.md`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/bounded_intelligence_benchmark.json`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_REPAIR_CYCLE_02_AUDIT.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/interactive_turn.py`
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/product_runtime_shell.py`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/bounded_intelligence_shadow_benchmark.json`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_shadow_gate.py`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_report.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_failure_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_gate_report.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_gate_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/interactive_turn_records/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_REPAIR_CYCLE_03_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_FAILURE_SUMMARY.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle/REVIEW_FIRST.md`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle.zip`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/bounded_intelligence_benchmark.json`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/BOUNDED_INTELLIGENCE_GATE_SPEC.md`
  - all `projects/agifcore_master/01_plan/PHASE_16*`
  - all unrelated earlier-phase runtime modules unless direct live-turn integrity repair is required
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `.codex/`
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/07_assets/`
  - any Phase 16 output folder

## Branch And Worktree

- Branch Name: `current-thread`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `not_created`

## Objective

- Goal:
  - remove the remaining benchmark-shaped runtime behavior, preserve the frozen bounded-intelligence gate result, add a paraphrased shadow benchmark for integrity checking, and rerun the audit stack honestly
- Expected Outputs:
  - generalized live-turn routing and response composition with less wording-shaped branching
  - unchanged frozen benchmark and thresholds
  - rerun frozen bounded-intelligence gate outputs
  - shadow benchmark and shadow verifier outputs
  - refreshed anti-shortcut audit record and standalone review bundle
- Non-Goals:
  - Phase 16 work
  - benchmark edits
  - threshold edits
  - broad answer-quality tuning
  - phase closure
  - commit or freeze
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 -m compileall /Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime`
  - `python3 -m compileall /Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit`
  - `python3 /Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
  - `python3 /Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_shadow_gate.py`
- Required Build Commands:
  - `none`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_shadow_gate.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_report.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_failure_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_gate_report.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_gate_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/interactive_turn_records/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle/REVIEW_FIRST.md`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_REPAIR_CYCLE_03_AUDIT.md`
- Extra Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_FAILURE_SUMMARY.md`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_VALIDATION_REQUEST.md`
- User Verdict Path:
  - `not_applicable_in_repair_cycle`
- Additional Human Demo Checkpoint Path:
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle/REVIEW_FIRST.md`

## Approval Chain

- Auditor: `anti_shortcut_auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `ahsadin`

## Completion Checklist

- scope stayed inside owned files
- frozen benchmark was not changed
- thresholds were not changed
- benchmark-shaped runtime branches were removed or generalized
- shadow benchmark exists and is audit-only
- required compile checks ran
- frozen gate reran
- shadow benchmark reran
- anti-shortcut audit reran
- updated evidence was produced
- standalone review bundle was refreshed
- rollback path is defined

## No Approval Implied

This task card governs the final integrity repair cycle only.
It does not approve or close Phase 15.
It does not start or close Phase 16.
