# Phase 9 Rich Expression Demo

Phase 9 remains `open`. This page is for inspection only.

What to inspect:

- [phase_09_teaching_report.json](/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_teaching_report.json)
- [phase_09_comparison_report.json](/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_comparison_report.json)
- [phase_09_planning_report.json](/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_planning_report.json)
- [phase_09_synthesis_report.json](/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_synthesis_report.json)
- [phase_09_analogy_report.json](/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_analogy_report.json)
- [phase_09_concept_composition_report.json](/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_concept_composition_report.json)
- [phase_09_cross_domain_composition_report.json](/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/phase_09_cross_domain_composition_report.json)

Evidence-backed summary:

- Teaching is bounded and keeps uncertainty visible. The verifier asserts `teaching-sections-bounded` and `teaching-honesty-boundary-emitted`.
- Comparison is axis-based and keeps asymmetry explicit. The verifier asserts `comparison-axes-bounded` and `comparison-intent-respected`.
- Planning stays in bounded steps and stops when evidence is missing. The verifier asserts `planning-steps-bounded`, `stop-if-unsure-preserved`, and `fresh-measurement-step-added`.
- Synthesis preserves declared uncertainty instead of smoothing it away. The verifier asserts `synthesis-inputs-bounded`, `support-honesty-preserved`, and `uncertainty-surfaced`.
- Analogy is illustrative only, with explicit `analogy_trace_ref`, break limits, and support refs. The verifier asserts `analogy-count-bounded`, `analogy-trace-ref-present`, and `break-limits-and-support-refs-present`.
- Concept composition stays bounded and carries its own `concept_composition_ref`. The verifier asserts `concept-elements-bounded`, `concept-composition-ref-present`, and `fail-closed-on-weak-support`.
- Cross-domain composition defaults to exactly two domains and fail-closes on under-support. The verifier asserts `exactly-two-domains-kept`, `over-limit-domains-bounded`, and `concept-composition-ref-preserved`.

Truth note:

- this is a summary of real verifier outputs
- no approval language is used
