# AGIFCore Results

## Final Outcome

AGIFCore is supported and closed as a bounded intelligence baseline.

## Evaluation Set

The final claim relies on three checks:

1. a frozen bounded-intelligence gate with `50` prompts across `10` question classes
2. a paraphrased shadow benchmark with the same class coverage
3. an anti-shortcut audit that checks for benchmark-shaped behavior and synthetic proof signaling

## Frozen Gate Result

- overall: `49/50`
- pass rate: `98%`
- hard fails: `0`
- final gate result: `pass`

### Frozen Gate Class Results

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

### Threshold Status

- overall threshold `44/50`: passed
- identity + project + local-runtime combined `14/15` (`93.3%`): passed
- math / logic threshold: passed
- comparison / planning threshold: passed
- current-world threshold: passed
- contradiction / inconsistency threshold: passed
- follow-up threshold: passed
- underspecified threshold: passed
- unsupported honest fail-closed threshold: passed
- phase-chain integrity threshold: passed

### One Remaining Frozen-Gate Miss

The only frozen-gate failure was a class-label mismatch on the prompt `what phase are you on`.

- expected class: `local_truth_evidence`
- detected class: `project_phase_capability`
- recorded failure type: `interpretation_failure`

The response itself stayed grounded and safe, but the case still counted as a failure because the verifier expected a different allowed class family.

## Shadow Benchmark Result

- overall: `50/50`
- pass rate: `100%`
- hard fails: `0`
- final shadow result: `pass`

All ten shadow-benchmark classes passed at `5/5`.

## Audit Result

The anti-shortcut audit cleared the bounded claim.

That audit confirmed:

- the frozen gate still passed after the final integrity repair
- the paraphrased shadow benchmark also passed
- benchmark-shaped branching was removed from the live runtime path
- the recorded evidence remained runtime-derived rather than synthetic

## What The Results Support

The results support these claims:

- supported local truth handling
- bounded reasoning and simple math
- follow-up binding
- contradiction and ambiguity handling
- bounded current-world estimates
- honest unsupported-question fail-closed behavior
- bounded generalization beyond the exact frozen wording

## What The Results Do Not Support

The results do not support:

- broad open-ended non-neural chat intelligence
- unrestricted conversational intelligence
- general AGI

Those claims remain unproven and deferred.

## Evidence Locations

- `projects/agifcore_master/06_outputs/final_publication/closeout_records/bounded_intelligence_gate_summary.json`
- `projects/agifcore_master/06_outputs/final_publication/closeout_records/bounded_intelligence_shadow_summary.json`
- `projects/agifcore_master/06_outputs/final_publication/PUBLICATION_AUDIT_REPORT.md`
- `projects/agifcore_master/06_outputs/final_publication/final_public_review_bundle/REVIEW_FIRST.md`

## Status Language

Use this wording only:

- supported and closed: bounded intelligence baseline
- failed / unproven / deferred: broad open-ended non-neural chat
- not claimed: AGI
