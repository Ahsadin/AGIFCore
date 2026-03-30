# Cognitive Priors

## Purpose

This file defines the first-pass cognitive priors that AGIFCore design should preserve before later world-awareness and science phases deepen them.

These priors are design constraints, not claims of trained or embedded knowledge.

## First-pass priors

- support must be stronger than fluency
- uncertainty must stay visible instead of being polished away
- governance and policy checks are part of cognition, not post-processing
- memory review is selective and governed, not unlimited retention
- simulation and critique should happen before confident answer finalization when the task demands it
- transfer and reuse must stay provenance-aware
- rollback and quarantine are normal control paths, not exceptional admissions of failure

## Design implications

- The planner, simulator, critic, governance, and language layers must remain separable in the design.
- Trace references must survive across planning, simulation, critique, governance, and memory review.
- Weak-support states must have a real representational path through the conversation and runtime models.
- Compression, retirement, and correction behavior must remain part of the memory design instead of later patches.

## Dependency notes

- Later science, world-model, and self-improvement phases may enrich these priors but should not contradict them.
- This file stays intentionally abstract enough to avoid hard-coding implementation heuristics in Phase 1.
- The formal models and simulator model should remain aligned to these priors.

## Cross-References

- `projects/agifcore_master/01_plan/HUMAN_THINKING_TARGET.md`
- `projects/agifcore_master/03_design/FORMAL_MODELS.md`
- `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
- `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
