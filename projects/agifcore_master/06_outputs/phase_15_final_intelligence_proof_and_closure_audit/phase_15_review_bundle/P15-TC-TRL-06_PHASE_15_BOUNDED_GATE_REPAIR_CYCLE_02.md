# Task Card

## Header

- Task Card ID: `P15-TC-TRL-06`
- Phase: `15`
- Title: `Bounded-intelligence gate repair cycle 02`
- Status: `complete`
- Issued By: `Program Governor`
- Issued On: `2026-04-03`

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
  - `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md`
  - `projects/agifcore_master/01_plan/AGIFCORE_BOUNDED_INTELLIGENCE_CLAIM_BOUNDARY.md`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/BOUNDED_INTELLIGENCE_GATE_SPEC.md`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/bounded_intelligence_benchmark.json`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_FAILURE_SUMMARY.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/interactive_turn.py`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_report.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_failure_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/interactive_turn_records/`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle/REVIEW_FIRST.md`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle.zip`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_FAILURE_SUMMARY.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/bounded_intelligence_benchmark.json`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/BOUNDED_INTELLIGENCE_GATE_SPEC.md`
  - all `projects/agifcore_master/01_plan/PHASE_16*`
  - all unrelated earlier-phase runtime modules unless direct live-turn repair is required
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Forbidden Folders:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/phase_16*`
  - `.codex/`

## Branch And Worktree

- Branch Name: `current-thread`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `not_created`

## Objective

- Goal:
  - repair the remaining bounded-intelligence gate blockers by strengthening real follow-up memory binding, removing benchmark-shaped behavior, and replacing synthetic Phase 15 proof signaling with runtime-derived turn evidence
- Expected Outputs:
  - improved follow-up binding across the frozen benchmark follow-up cases
  - runtime-derived per-turn Phase 15 evidence records with explicit follow-up integrity fields
  - rerun frozen bounded-intelligence gate outputs
  - rerun anti-shortcut audit outcome
  - updated standalone review bundle
- Non-Goals:
  - Phase 16 work
  - benchmark edits
  - threshold edits
  - hardcoded prompt answers
  - broad answer-quality polishing
  - phase closure
  - commit or freeze
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 -m compileall projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime`
  - `python3 -m compileall projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit`
  - `python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
- Required Build Commands:
  - `none`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_report.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_failure_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/interactive_turn_records/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle/REVIEW_FIRST.md`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_FAILURE_SUMMARY.md`
- Extra Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_REPAIR_CYCLE_02_AUDIT.md`
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
- follow-up binding uses stored prior-turn state instead of shallow previous-response replay
- Phase 15 evidence is runtime-derived and machine-readable
- required compile checks ran
- frozen gate reran
- anti-shortcut audit reran
- updated evidence was produced
- standalone review bundle was refreshed
- rollback path is defined

## No Approval Implied

This task card governs bounded-intelligence repair cycle 02 only.
It does not approve or close Phase 15.
It does not start or close Phase 16.
