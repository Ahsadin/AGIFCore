# Public Vs Internal Evidence Map

This map separates canonical public evidence from internal raw evidence and archive candidates.

## Canonical Public Evidence

These are the files that should remain public-facing or be mirrored into the final public publication package:

- `README.md`
- `CLAIM_BOUNDARY.md`
- `ARCHITECTURE.md`
- `RESULTS.md`
- `REPRODUCIBILITY.md`
- `NEXT_STEPS.md`
- `paper/AGIFCore_Bounded_Intelligence_Final_Report.md`
- `projects/agifcore_master/06_outputs/final_publication/closeout_records/`
- `projects/agifcore_master/06_outputs/final_publication/public_evidence/public_evidence_manifest.json`
- `projects/agifcore_master/06_outputs/final_publication/final_public_review_bundle/REVIEW_FIRST.md`
- `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/CLAIMS_MATRIX.md`
- `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/BOUND_PUBLICATION_SUMMARY.md`

## Internal Raw Evidence

These are raw or mechanically generated evidence files that are not part of the canonical public package.
They may remain as sanitized internal provenance if the publication-safety scan stays clean.
If any future scan flags them, they should move to local non-public storage:

- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/interactive_turn_records/`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_report.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_shadow_report.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/phase_15_evidence_manifest.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/phase_15_reproducibility_report.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/phase_15_real_desktop_chat_demo_report.json`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/phase_15_interactive_chat_report.json`
- `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/bounded_intelligence_gate_report.json`
- `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/bounded_intelligence_shadow_report.json`

## Archive Or Move To Non-Public Storage

These are duplicated review-bundle or repair-cycle artifacts that should be archived rather than deleted when practical:

- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle/`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_review_bundle.zip`
- `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_demo_bundle/`
- `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/phase_16_bounded_review_bundle/`
- `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/phase_16_bounded_review_bundle.zip`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_16/`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_CLOSEOUT_SUMMARY.md`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_FAILURE_SUMMARY.md`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_BOUNDED_INTELLIGENCE_GATE_REPAIR_CYCLE_02_AUDIT.md`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_EXECUTION_START_BRIEF.md`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_PLAN_FREEZE_HANDOFF.md`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_USER_VERDICT.md`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_16_USER_VERDICT.md`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_16_VALIDATION_REQUEST.md`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_16_GOVERNOR_VERIFICATION_RECORD.md`

## Cleanup Guidance

- Keep the canonical public evidence in the final publication lane.
- Keep sanitized internal provenance only if the publication-safety scan stays clean.
- Archive duplicate review bundles and repair-cycle artifacts when they no longer serve the public package.
- Avoid deletion unless the canonical copy and the public-safe copy both survive elsewhere.
