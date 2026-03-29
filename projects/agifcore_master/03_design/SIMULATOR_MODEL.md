# Simulator Model

## Purpose

This file defines the first-pass simulator and world-model boundary for AGIFCore.

The simulator is a governed checking layer, not a hidden autonomous actor.

## First-pass responsibilities

- evaluate planner proposals before final response when scenario checking is needed
- provide world-model or simulator review support
- surface contradiction, risk, and likely failure paths back to the critic and governance layers
- preserve replayable links to simulation traces

## Boundary rules

- The simulator does not get to overrule governance on its own.
- The simulator is distinct from the planner, critic, and language realizer even if later implementations share infrastructure.
- Simulation outputs must remain inspectable and trace-linked.
- Bounded current-world support must stay honest when world-state support is incomplete.

## Relationship to cognition flow

- planner proposal comes before simulator check
- simulator/world-model check informs critic and governance
- governance decides whether the result may reach language realization

This ordering is frozen from the master plan and should not be collapsed away later.

## Dependency notes

- Exact world representation, search strategy, and simulator internals remain later design and implementation work.
- This first-pass file freezes the simulator as a required layer in the cognition flow.
- The conversation model and formal models should remain aligned to the trace and accountability of simulator outputs.

## Cross-References

- `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
- `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
- `projects/agifcore_master/03_design/FORMAL_MODELS.md`
- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
