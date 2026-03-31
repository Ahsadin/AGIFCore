# Phase 9 Validation Request

Phase 9 is ready for user review, but it remains open until the explicit user verdict is recorded. No approval is implied by this request.

Please inspect these files in this order:

1. Review context and rules
   - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-VA-02_PHASE_9_FINAL_VALIDATION.md`
   - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
   - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`

2. Independent checks already completed
   - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-AUDIT-01_PHASE_9_FINAL_PACKAGE_AUDIT_REPORT.md`
   - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_GOVERNOR_VERIFICATION_RECORD.md`

3. User-facing demo bundle
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/phase_09_demo_index.md`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/phase_09_demo_index.json`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/phase_09_rich_expression_demo.md`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/phase_09_rich_expression_demo.json`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/phase_09_non_generic_chat_quality_demo.md`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/phase_09_non_generic_chat_quality_demo.json`

4. Evidence package behind the demos
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_evidence_manifest.json`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_teaching_report.json`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_comparison_report.json`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_planning_report.json`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_synthesis_report.json`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_analogy_report.json`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_concept_composition_report.json`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_cross_domain_composition_report.json`
   - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_audience_aware_explanation_quality_report.json`

5. Optional deep inspection surfaces
   - runtime: `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/`
   - testing: `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/`

What good looks like:

- the Governor verification record says the full Phase 9 verifier family was rerun directly, the full demo bundle was checked, and the overlay coordinator smoke test passed
- the demo bundle opens cleanly and stays review-only
- the evidence manifest lists all eight required reports with `status: phase_9_verifier_family_pass`
- the rich-expression demo shows bounded teaching, comparison, planning, synthesis, analogy, concept composition, and cross-domain composition surfaces tied back to evidence files
- the non-generic chat-quality demo shows audience-aware quality with at least novice and technical cases while preserving uncertainty and avoiding persuasion drift
- analogy stays trace-backed and bounded
- concept composition and cross-domain composition stay bounded and fail closed where required
- the audience-quality lane derives profile from real Phase 7 intake text rather than hashes or abstract labels
- no file implies approval, closure, or Phase 10 start before the explicit verdict is recorded

What failure looks like:

- a listed file is missing or points to the wrong surface
- the demos and evidence manifest do not agree
- the runtime, evidence, or demos collapse into one mixed style engine
- wording upgrades support strength or hides uncertainty
- analogy or composition claims are unsupported or not trace-linked
- audience-aware quality becomes persuasion instead of clarity
- the overlay coordinator is missing, broken, or not evidence-compatible
- any file implies approval, closure, or Phase 10 start before the explicit verdict is recorded
- you find a blocker that makes the Phase 9 package unfit for review approval

Please reply with exactly one of these verdicts:

- `approved`
- `rejected`
- `approved_with_blockers`

If you choose `approved_with_blockers` or `rejected`, include the blockers you want corrected. Until the explicit user verdict is recorded, Phase 9 remains open.
