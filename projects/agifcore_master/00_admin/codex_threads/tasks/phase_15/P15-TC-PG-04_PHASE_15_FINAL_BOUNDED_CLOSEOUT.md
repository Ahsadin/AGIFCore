# Task Card

## Header

- Task Card ID: `P15-TC-PG-04`
- Phase: `15`
- Title: `Final bounded-intelligence closeout`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-04-05`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `constitution_guard`, `architecture_contract`, `test_replay`, `anti_shortcut_auditor`, `validation_agent`, `release_evidence`
- Allowed Models: `gpt-5.4`, `gpt-5.4-mini`
- Build Pod Agent Session ID: `governor-main-thread`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `role-separated closeout lane`
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
  - `projects/agifcore_master/01_plan/AGIFCORE_BOUNDED_INTELLIGENCE_CLAIM_BOUNDARY.md`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/BOUNDED_INTELLIGENCE_GATE_SPEC.md`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_summary.json`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_REPAIR_CYCLE_03_AUDIT.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-PG-04_PHASE_15_FINAL_BOUNDED_CLOSEOUT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_USER_VERDICT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_CLOSEOUT_SUMMARY.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/AGIFCORE_BOUNDED_INTELLIGENCE_CLAIM_BOUNDARY.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/bounded_intelligence_benchmark.json`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/BOUNDED_INTELLIGENCE_GATE_SPEC.md`
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/` except read-only verification

## Branch And Worktree

- Branch Name: `codex/tc-p15-pg-04-final-bounded-closeout`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `not_created`

## Objective

- Goal:
  - verify the bounded-closeout preconditions directly and, only if they remain clean, finalize Phase 15 as bounded-intelligence proof with truthful claim boundaries and closure records
- Expected Outputs:
  - final bounded-intelligence closeout summary
  - refreshed Governor verification record
  - Phase 15 user verdict record based on the explicit user close-if-clean instruction
  - updated phase-truth files and project logs
- Non-Goals:
  - no runtime tuning except a tiny truth-preserving fix if absolutely required
  - no benchmark edits
  - no threshold edits
  - no broad-chat claim revival
  - no post-Phase-16 work
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 -m compileall /Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime`
  - `python3 -m compileall /Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit`
  - `python3 /Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
  - `python3 /Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_shadow_benchmark.py`
- Required Build Commands:
  - `none`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_shadow_benchmark.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_failure_summary.json`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle/REVIEW_FIRST.md`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-AUDIT-02_PHASE_15_BOUNDED_CLOSEOUT_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_REPAIR_CYCLE_03_AUDIT.md`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_VALIDATION_REQUEST.md`
- User Verdict Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path:
  - `not_applicable`

## Approval Chain

- Auditor: `anti_shortcut_auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `ahsadin`

## Completion Checklist

- closeout preconditions were reverified directly
- bounded claim language stayed truthful
- broad-chat claim stayed unproven/deferred
- required audit, verification, validation, and verdict records exist
- phase-truth files were updated only after the closeout chain was complete
- rollback path is defined

## No Approval Implied

This task card governs final bounded closeout preparation and proof verification only.
It does not by itself approve or close Phase 15.
