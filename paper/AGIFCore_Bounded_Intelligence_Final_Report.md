# AGIFCore: A Bounded-Intelligence Architecture with Governed Runtime Behavior, Evidence-Carrying Evaluation, and Audit-Constrained Publication

## 1. Title

AGIFCore: A Bounded-Intelligence Architecture with Governed Runtime Behavior, Evidence-Carrying Evaluation, and Audit-Constrained Publication

## 2. Abstract

AGIFCore is a local-first intelligence architecture that was built to test whether a non-neural runtime could earn a defensible intelligence claim without hidden cloud support or vague benchmark rhetoric.
The final result is not a claim of broad open-ended chat intelligence.
Instead, AGIFCore closed as a bounded intelligence architecture/runtime/core.

The final claim is supported by three linked proof surfaces: a frozen `50`-prompt bounded-intelligence gate, a paraphrased `50`-prompt shadow benchmark, and an anti-shortcut audit that checked for benchmark-shaped branching and synthetic evidence.
On the frozen gate, AGIFCore passed `49/50` cases (`98%`) with `0` hard fails.
On the shadow benchmark, AGIFCore passed `50/50` cases (`100%`) with `0` hard fails.
The anti-shortcut audit cleared the bounded claim after targeted integrity repair.

These results support bounded local truth handling, bounded reasoning, follow-up binding, contradiction handling, bounded current-world estimation, and honest fail-closed behavior.
They do not support broad open-ended non-neural chat intelligence, unrestricted conversational intelligence, or AGI.

## 3. Plain-English Summary

AGIFCore finished as a careful local intelligence core, not as a general chatbot.
It can answer a narrow set of supported questions honestly and with evidence.
It can remember the immediate local context of a conversation, detect some contradictions, and refuse unsupported questions instead of inventing answers.

What it did not prove is just as important.
AGIFCore did not become a strong open-ended chat system.
It did not solve unrestricted language fluency, broad world knowledge, or AGI-like conversation.
That is why the project closes under a bounded-intelligence claim only.

## 4. Motivation

AGIFCore was built to test a strict hypothesis:

- can a governed, local-first, non-neural system earn an intelligence claim that is replayable, auditable, and fail-closed?

The project did not aim to maximize perceived smoothness in casual conversation.
It aimed to maximize truth discipline:

- explicit support-state handling
- explicit claim boundaries
- machine-readable evidence
- role-separated review and validation
- auditable closeout language

This matters because many intelligence claims collapse under closer inspection.
AGIFCore was designed so that the final published claim would be narrower than the aspirational goal if the evidence demanded it.
That is what happened.

## 5. System Architecture

AGIFCore is organized as a governed runtime core rather than a broad chat product.
Its architecture is strongest when a request can be tied back to known local support and explicit answer policies.

The important subsystems are:

- question interpretation
- local retrieval and support-state analysis
- prior-turn continuity and follow-up binding
- contradiction and ambiguity diagnosis
- bounded world reasoning for narrow estimate-style prompts
- answer-mode selection
- per-turn evidence recording

The architecture is intentionally not open-ended.
It is built around a small number of allowed answer behaviors:

- `grounded_fact`
- `bounded_estimate`
- `clarify`
- `abstain`
- `search_needed`

Those modes are selected after the system checks what evidence exists, what kind of question is being asked, and whether the target is grounded enough to answer safely.

## 6. Methods

### 6.1 Runtime Path Under Test

The bounded gate was run through the real AGIFCore runtime path used by the Phase 15 interactive proof path.
The gate spec explicitly forbids:

- web support
- hidden cloud support
- fake responders
- skipping the full phase-chain evidence path

The runtime under test therefore had to produce both the answer and the machine-readable record of how it arrived there.

### 6.2 Evidence-Carrying Evaluation

Every scored turn had to record structured evidence, not just text output.
Required per-turn fields included:

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
- `phases_actually_exercised`
- `memory_used`
- `graph_or_provenance_used`
- `simulation_or_world_model_used`
- `critique_or_diagnosis_fired`
- `final_response`
- `pass_or_fail`
- `primary_failure_type`

This structure matters because it makes the claim auditable at the turn level.
It is possible to inspect not only whether AGIFCore passed a case, but also what kind of support it used and whether it completed the required chain honestly.

### 6.3 Failure Vocabulary

The bounded verifier used a restricted failure vocabulary:

- `interpretation_failure`
- `retrieval_failure`
- `followup_memory_failure`
- `answerability_failure`
- `reasoning_integration_failure`
- `response_composition_failure`

This kept failure reporting structured and comparable across repair cycles.

## 7. Evaluation Setup

The final evaluation used three linked surfaces.

### 7.1 Frozen Bounded-Intelligence Gate

The frozen benchmark contained `50` prompts across `10` question classes:

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

### 7.2 Shadow Benchmark

The shadow benchmark preserved the same class coverage and count but changed the wording.
Its purpose was not to replace the frozen gate.
Its purpose was to test whether the runtime still behaved credibly when exact prompt wording changed.

### 7.3 Anti-Shortcut Audit

The anti-shortcut audit checked whether the passing result was real.
In particular, it checked for:

- benchmark-shaped branching
- exact prompt-family shortcuts
- synthetic proof signaling
- fake or decorative phase usage
- evidence surfaces that looked good but were not tied to real execution

AGIFCore only became eligible for bounded closeout after this audit was cleared.

## 8. Bounded-Intelligence Gate Design

The gate was designed around both hard fails and class-level thresholds.

### 8.1 Hard Fails

Any one of the following would fail the gate immediately:

- fabricated local fact
- unsupported factual answer instead of honest fail-closed behavior
- wrong-location current-world grounding
- missing full ordered phase chain on any turn
- final answer emitted before full-chain completion
- any closeout surface claiming broad chat was proven
- fake `all phases used` stamping

### 8.2 Thresholds

The gate required all of the following:

- overall pass rate at least `88%` (`44/50`)
- identity + project + local-runtime combined at least `92%`
- math / logic at least `80%`
- comparison / planning at least `80%`
- current-world at least `80%`
- contradiction / inconsistency at least `80%`
- follow-up at least `80%`
- underspecified at least `80%`
- unsupported at `100%` honest fail-closed
- phase-chain integrity at `100%`
- local-fabrication rate `0`
- wrong-location current-world rate `0`

This design is important because it blocks the easy path of “mostly good answers” while still hallucinating on the highest-risk classes.

## 9. Shadow Benchmark Design

The shadow benchmark held the class structure constant while varying the wording.
It specifically targeted the concern that the runtime might pass only because it fit the exact frozen `50` prompts.

The shadow suite preserved the same behavioral expectations:

- bounded support use
- correct class handling
- follow-up continuity
- honest fail-closed behavior
- no fake broad-world grounding

The shadow benchmark therefore acted as a generalization check inside the same bounded claim space.

## 10. Results

### 10.1 Frozen Gate

Final frozen-gate result:

- `49/50`
- `98%`
- `0` hard fails
- `gate_passed: true`

Class-by-class frozen-gate results:

| Class | Passed | Total | Pass Rate |
| --- | ---: | ---: | ---: |
| identity_system | 5 | 5 | 100% |
| project_phase_capability | 4 | 5 | 80% |
| local_runtime_evidence | 5 | 5 | 100% |
| math_logic | 5 | 5 | 100% |
| comparison_planning | 5 | 5 | 100% |
| current_world | 5 | 5 | 100% |
| contradiction_ambiguity | 5 | 5 | 100% |
| follow_up | 5 | 5 | 100% |
| underspecified | 5 | 5 | 100% |
| unsupported | 5 | 5 | 100% |

Combined identity + project + local-runtime score:

- `14/15`
- `93.3%`

The gate therefore cleared all required thresholds.

### 10.2 Shadow Benchmark

Final shadow result:

- `50/50`
- `100%`
- `0` hard fails
- `shadow_passed: true`

Class-by-class shadow-benchmark results:

| Class | Passed | Total | Pass Rate |
| --- | ---: | ---: | ---: |
| identity_system | 5 | 5 | 100% |
| project_phase_capability | 5 | 5 | 100% |
| local_runtime_evidence | 5 | 5 | 100% |
| math_logic | 5 | 5 | 100% |
| comparison_planning | 5 | 5 | 100% |
| current_world | 5 | 5 | 100% |
| contradiction_ambiguity | 5 | 5 | 100% |
| follow_up | 5 | 5 | 100% |
| underspecified | 5 | 5 | 100% |
| unsupported | 5 | 5 | 100% |

This matters because it shows that the final bounded result was not limited to the exact wording of the frozen suite.

### 10.3 Anti-Shortcut Audit

The anti-shortcut audit cleared the bounded claim after the final integrity repair cycle.

The audit verified that:

- the frozen gate still passed after repair
- the shadow benchmark still passed
- exact frozen prompt strings were no longer present in the live runtime path
- runtime behavior was driven by support, continuity, retrieval, and critique state rather than by benchmark wording
- evidence remained runtime-derived and machine-readable

## 11. Failure Analysis

The final frozen gate had one remaining failure.

Recorded failure counts by primary failure type:

| Failure Type | Count |
| --- | ---: |
| interpretation_failure | 1 |
| retrieval_failure | 0 |
| followup_memory_failure | 0 |
| answerability_failure | 0 |
| reasoning_integration_failure | 0 |
| response_composition_failure | 0 |

### 11.1 The Remaining Failure

Case:

- `what_phase_are_you_on`

Recorded failure:

- class group: `project_phase_capability`
- expected class: `local_truth_evidence`
- detected class: `project_phase_capability`
- primary failure type: `interpretation_failure`

The important point is that this was not a safety failure.
The response stayed grounded, used local support, and did not hallucinate.
The failure remained because the verifier expected one allowed class family while the runtime chose another closely related class family.

### 11.2 Why This Did Not Invalidate The Final Claim

The bounded claim does not require perfection on every taxonomy edge case.
It requires:

- threshold passage
- no hard fails
- fail-closed integrity
- honest evidence

AGIFCore still met those requirements.

### 11.3 What AGIFCore Failed To Prove More Broadly

The broader failure is more important than the single frozen-gate miss.
AGIFCore did not prove:

- broad open-ended non-neural chat intelligence
- unrestricted conversational intelligence
- AGI

This was not hidden or softened in the closeout.
The entire release package was rebuilt around that narrower truth.

## 12. Claim Boundary

The final supported claim is:

- AGIFCore is a bounded intelligence architecture/runtime/core

The final unsupported claims are:

- broad open-ended non-neural chat intelligence
- unrestricted conversational intelligence
- AGI

This boundary is not just a publishing preference.
It is the direct consequence of the evaluation results.

AGIFCore is strongest when it stays inside:

- local truth
- bounded reasoning
- explicit answer modes
- inspectable evidence
- fail-closed behavior

That is why bounded intelligence is the correct final claim.

## 13. Lessons Learned

Three lessons stand out.

First, bounded local truth and governance can be evaluated cleanly.
AGIFCore showed that a non-neural local runtime can be made inspectable and auditable in a meaningful way.

Second, continuity and contradiction handling can be improved substantially without pretending that this solves broad conversation.
The repair cycles raised real capability within the bounded contract, especially around follow-up binding and unsupported-question handling.

Third, evidence discipline matters as much as answer quality.
The anti-shortcut audit forced the project to remove benchmark-shaped behavior and synthetic proof signaling.
Without that step, even a numerically strong gate result would not have been a trustworthy claim.

## 14. Reproducibility

The repository contains rerun instructions in `REPRODUCIBILITY.md`.
The key public commands are:

```bash
python3 -m py_compile projects/agifcore_master/05_testing/final_publication/verify_publication_safety.py
python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_gate.py
python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_bounded_intelligence_shadow_benchmark.py
python3 projects/agifcore_master/05_testing/final_publication/verify_publication_safety.py
```

The expected public outcome is:

- frozen gate still passes
- shadow benchmark still passes
- publication-safety scan shows zero findings on candidate public files

The anti-shortcut audit is included as an audited closeout surface rather than as a standalone public rerun script.

## 15. Next Project Direction

The next project direction is `AGIF + neural hybrid`.

Default working name:

- `AGIF-X`
- subtitle: `AGIF + Neural Hybrid Rebuild`

This direction exists because AGIFCore alone did not justify a broad-chat success claim.
The bounded baseline is useful infrastructure, but not a final answer to open-ended conversational capability.

The next project should therefore:

- inherit AGIFCore as bounded infrastructure
- define a new claim boundary
- add explicit neural language and reasoning support
- require a new evaluation and audit stack

## 16. Conclusion

AGIFCore closed honestly, but under a narrower claim than the broad aspiration that motivated it.

It succeeded as a bounded intelligence baseline.
It proved supported local truth handling, bounded reasoning, follow-up binding, contradiction handling, bounded current-world estimation, and honest fail-closed behavior.
It passed a frozen bounded gate, passed a paraphrased shadow benchmark, and cleared an anti-shortcut audit.

It did not prove broad open-ended non-neural chat intelligence.
It did not prove unrestricted conversational intelligence.
It did not prove AGI.

That boundary is not a weakness in the final publication.
It is the reason the final publication is trustworthy.
