# Phase 8 Validation Request

Phase 8 is ready for user review, but it remains open until the explicit user verdict is recorded. No approval is implied by this request.

Please inspect these files in this order:

1. Review context and rules
   - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-VA-02_PHASE_8_FINAL_VALIDATION.md`
   - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
   - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`

2. Independent checks already completed
   - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-AUDIT-01_PHASE_8_FINAL_PACKAGE_AUDIT_REPORT.md`
   - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_GOVERNOR_VERIFICATION_RECORD.md`

3. User-facing demo bundle
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_demo_index.md`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_demo_index.json`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_science_explanation_demo.md`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_science_explanation_demo.json`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_bounded_live_fact_demo.md`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_bounded_live_fact_demo.json`

4. Evidence package behind the demos
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_evidence_manifest.json`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_scientific_priors_report.json`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_entity_request_inference_report.json`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_world_region_selection_report.json`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_causal_chain_reasoning_report.json`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_bounded_current_world_reasoning_report.json`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_visible_reasoning_summaries_report.json`
   - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_science_reflection_report.json`

5. Optional deep inspection surfaces
   - runtime: `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/`
   - testing: `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`

What good looks like:

- the Governor verification record says the full Phase 8 verifier family was rerun directly and the full demo bundle was checked
- the demo bundle opens cleanly and stays review-only
- the evidence manifest lists all seven required reports with `status: phase_8_verifier_family_pass`
- the science explanation demo shows bounded scientific priors, typed inference, bounded region choice, causal-chain reasoning, public summaries, and science reflection
- the bounded live-fact demo shows freshness limits and `live_measurement_required` instead of a fabricated exact current answer
- the visible reasoning summary stays public-summary-only and bounded
- the science reflection surface stays below Phase 10 and records concrete falsifier, missing-variable, and next-step outputs
- no file implies approval, closure, or Phase 9 start before the explicit verdict is recorded

What failure looks like:

- a listed file is missing or points to the wrong surface
- the demos and evidence manifest do not agree
- the runtime, evidence, or demos collapse into one mixed reasoning shortcut
- current-world boundedness is violated or exact live answers are fabricated
- visible reasoning summaries act like hidden-thought disclosure
- science reflection becomes generic, unsupported, or meta-cognitive beyond Phase 8
- any file implies approval, closure, or Phase 9 start before the explicit verdict is recorded
- you find a blocker that makes the Phase 8 package unfit for review approval

Please reply with exactly one of these verdicts:

- `approved`
- `rejected`
- `approved_with_blockers`

If you choose `approved_with_blockers` or `rejected`, include the blockers you want corrected. Until the explicit user verdict is recorded, Phase 8 remains open.
