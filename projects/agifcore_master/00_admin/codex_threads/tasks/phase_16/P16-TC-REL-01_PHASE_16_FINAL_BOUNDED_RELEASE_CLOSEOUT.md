# Task Card

## Header

- Task Card ID: `P16-TC-REL-01`
- Phase: `16`
- Title: `Final bounded release and publication closeout`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-04-05`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `architecture_contract`, `anti_shortcut_auditor`, `validation_agent`, `phase_builder`
- Allowed Models: `gpt-5.4-mini`, `gpt-5.4`
- Build Pod Agent Session ID: `role-separated release lane`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `role-separated validation lane`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/AGIFCORE_BOUNDED_INTELLIGENCE_CLAIM_BOUNDARY.md`
  - `projects/agifcore_master/01_plan/PHASE_16_BOUNDED_RELEASE_AND_PUBLICATION.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_summary.json`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_REPAIR_CYCLE_03_AUDIT.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_16/P16-TC-REL-01_PHASE_16_FINAL_BOUNDED_RELEASE_CLOSEOUT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_16_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_16_USER_VERDICT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/AGIFCORE_BOUNDED_BASELINE_HANDOFF.md`
  - `projects/agifcore_master/01_plan/PHASE_16_BOUNDED_RELEASE_AND_PUBLICATION.md`
  - `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle/`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle.zip`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/bounded_intelligence_benchmark.json`
  - all future mission project files
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_16/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`
  - `projects/agifcore_master/01_plan/`
  - `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/`
  - `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/` except read-only verification

## Branch And Worktree

- Branch Name: `codex/tc-p15-pg-04-final-bounded-closeout`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `not_created`

## Objective

- Goal:
  - materialize the bounded release/publication package and close Phase 16 only if bounded closeout truth remains fully supported
- Expected Outputs:
  - bounded claims matrix
  - bounded publication summary
  - final bounded review bundle and zip
  - bounded baseline handoff note
  - final Governor verification and user-verdict records for Phase 16
- Non-Goals:
  - no new runtime capability work
  - no broad-chat claims
  - no post-Phase-16 mission work
  - no benchmark edits
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
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
  - `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/CLAIMS_MATRIX.md`
  - `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/BOUND_PUBLICATION_SUMMARY.md`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/phase_16_bounded_review_bundle/REVIEW_FIRST.md`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_16/P16-AUDIT-01_PHASE_16_BOUNDED_RELEASE_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_REPAIR_CYCLE_03_AUDIT.md`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_16_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_16_VALIDATION_REQUEST.md`
- User Verdict Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_16_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path:
  - `not_applicable`

## Approval Chain

- Auditor: `anti_shortcut_auditor`
- Merge Arbiter: `inactive`
- Program Governor: `Program Governor`
- User: `ahsadin`

## Completion Checklist

- bounded release package exists and is internally consistent
- claims matrix and publication summary stay inside the bounded claim boundary
- final standalone review bundle exists and is inspectable
- bounded baseline handoff note exists
- phase-truth files are updated only if the full closeout chain is complete
- rollback path is defined

## No Approval Implied

This task card governs final bounded release and publication closeout preparation only.
It does not by itself approve or close Phase 16.
