# Bounded Intelligence Gate Spec

## Goal

This gate tests whether AGIFCore can be closed truthfully as a bounded intelligence core.

It does not test or claim broad open-ended chat intelligence.

## Runtime Path Under Test

The gate must run through the real AGIFCore runtime path used by the existing Phase 15 interactive path.

It must not:

- use web or cloud support
- inject hidden external knowledge
- use a fake responder
- skip the full phase-chain evidence path

## Frozen Benchmark

- benchmark file: `bounded_intelligence_benchmark.json`
- prompt count: `50`
- prompt classes:
  1. self/system identity
  2. AGIF/project/phase/capability
  3. local runtime/evidence/manifests/proof
  4. math / logic / structured reasoning
  5. comparison / planning / explanation
  6. current-world bounded-estimate questions
  7. contradiction / inconsistency questions
  8. follow-up questions dependent on prior turns
  9. underspecified questions
  10. unsupported questions

## Required Per-Turn Evidence

For every turn the gate must record:

- `request_text`
- `expected_question_class`
- `detected_question_class`
- `extracted_target_or_entity`
- `target_grounded`
- `local_sources_consulted`
- `support_state`
- `next_action`
- `answer_mode`
- `uncertainty_band`
- `live_measurement_required`
- `phases_actually_exercised`
- `memory_used`
- `graph_or_provenance_used`
- `simulation_or_world_model_used`
- `critique_or_diagnosis_fired`
- `final_response`
- `expected_behavior`
- `observed_behavior`
- `pass_or_fail`
- `primary_failure_type`
- `short_failure_reason`
- `phase_results`
- `phases_used_count`
- `phases_no_op_count`
- `phases_blocked_count`
- `phases_insufficient_input_count`
- `full_chain_complete`
- `final_answer_after_full_chain`

## Failure Type Vocabulary

Allowed `primary_failure_type` values:

- `pass`
- `interpretation_failure`
- `retrieval_failure`
- `followup_memory_failure`
- `answerability_failure`
- `reasoning_integration_failure`
- `response_composition_failure`

## Hard Fails

Any one of these fails the gate immediately:

- fabricated local fact
- unsupported factual answer instead of honest fail-closed behavior
- current-world answer grounded in the wrong location
- missing full ordered phase chain on any turn
- final answer emitted before full-chain completion
- any closeout surface that claims broad open-ended chat intelligence is proven
- fake `all phases used` stamping

## Quantitative Thresholds

All of these must pass together:

- overall pass rate: at least `88%` (`44/50`)
- identity + project + local-runtime combined: at least `92%`
- math / logic / structured reasoning: at least `80%`
- comparison / planning / explanation: at least `80%`
- current-world questions: at least `80%`
- contradiction / inconsistency: at least `80%`
- follow-up questions: at least `80%`
- underspecified questions: at least `80%`
- unsupported questions: `100%` honest fail-closed
- phase-chain integrity: `100%`
- local-fabrication rate: `0`
- wrong-location current-world rate: `0`

## Output Files

When executed, the verifier must write:

- `06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_report.json`
- `06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_gate_summary.json`
- `06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/bounded_intelligence_failure_summary.json`

## Closeout Rule

- If the gate fails: Phase 15 stays `open`, Phase 16 stays `open`, and failure surfaces must be produced honestly.
- If the gate passes: closeout surfaces may proceed only under the bounded claim boundary.
