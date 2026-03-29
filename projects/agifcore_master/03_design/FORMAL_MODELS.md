# Formal Models

## Purpose

This file captures the first-pass formal framing AGIFCore needs so later runtime work stays structurally coherent.

Phase 1 uses this file to name the kinds of models the architecture depends on, not to finalize implementation math.

## First-pass formal surfaces

| Surface | What it formalizes | Why it matters now |
| --- | --- | --- |
| turn contract model | the required fields and trace references for governed turns | keeps conversation, runtime, and evidence aligned |
| state-transition model | how a turn or internal action moves between admitted, planned, simulated, critiqued, governed, realized, and reviewed states | prevents hidden transition jumps |
| policy-decision model | how governance determines allow, block, clarify, abstain, or escalate outcomes | keeps governance explicit instead of implicit |
| memory-lifecycle model | how memory is reviewed, retained, compressed, superseded, or retired | prevents memory sprawl and hidden retention |
| graph-reference model | how descriptors, skills, concepts, and transfer relations refer to one another | keeps graph design composable |
| profile-budget model | how laptop, mobile, builder, and optional soak limits constrain work | keeps deployment differences governed and explicit |

## Formal-model rules

- A formal surface must clarify structure, not hide it behind generic prose.
- Formal framing may remain implementation-neutral in Phase 1, but the boundaries must be explicit enough to audit.
- No formal framing may introduce a hidden-model or cloud-correctness loophole.
- Any later implementation that violates the state-transition or contract model should be treated as architectural drift.

## Dependency notes

- Exact schemas, state machines, and algebraic representations remain later implementation/design work.
- The trace contract, governance model, memory model, and graph stack model should be read as concrete projections of the surfaces named here.
- This first-pass file exists to stabilize the shape of the problem before deeper formalization later.

## Cross-References

- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
- `projects/agifcore_master/03_design/MEMORY_MODEL.md`
- `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
