# Cell Families

## Purpose

This file freezes the first-pass AGIFCore cell-family framing from the master plan.

It is a design boundary for later runtime work, not a claim that any cell family is already implemented.

## Locked cell families

| Cell family | First-pass role in cognition flow | Notes for later phases |
| --- | --- | --- |
| intake or router | capture input or need and route it into governed handling | must stay aligned to workspace and operator family boundaries |
| attention | select what deserves active processing | later budgeting and salience logic still need implementation |
| working-memory | hold the active working state for the current turn or task | must align to the memory model and trace contract |
| episodic memory | retain event-style continuity and reviewable turn history | must stay replayable and auditable |
| semantic abstraction | hold generalized concepts and stable abstractions | must later align to descriptor/concept graph structures |
| procedural skill | hold reusable procedures and skills | must later align to skill graph and governed transfer logic |
| world-model or simulator | test hypotheses, scenarios, and world-facing support before final output | later simulator details still need separate design and execution work |
| planner | propose plans or next actions under support constraints | must stay trace-linked and governance-aware |
| critic or error-monitor | detect contradiction, weak support, or failure modes | must support abstain, revise, and escalation behavior |
| governance or authority | enforce policy, approvals, vetoes, and boundary discipline | may not be bypassed by product/runtime convenience |
| transfer-broker | manage governed transfer and reuse across domains or structures | transfer logic stays governed, not automatic |
| scheduler or resource | allocate work, budget, and active capacity | must later align to laptop/mobile/builder profile budgets |
| continuity or self-history | preserve self-knowledge and continuity references | stays separate from unsupported self-narration |
| language realizer | turn governed support into user-facing language | language remains the surface, not the cognition core |
| compression or retirement | manage selective retention, compression, and retirement | must align to reviewed memory and memory-pressure behavior |
| audit or replay | preserve inspectable evidence, replay, and closure support | remains a first-class family, not a later add-on |

## Family-level rules

- The cell-family list may not be renamed, merged away, or reduced casually.
- A family name does not imply a one-to-one runtime process or class.
- Build-time role names and runtime cell families are different concepts and must not be confused.
- Later implementation may refine the structure, but it may not silently remove a locked family responsibility.

## Dependency notes

- Final family manifests and active-cell allocations depend on later phase execution.
- Memory, graph, simulator, and transfer details still require their own deeper design artifacts.
- This first-pass file freezes responsibilities and vocabulary so later phases do not invent incompatible families.

## Cross-References

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- `projects/agifcore_master/03_design/MEMORY_MODEL.md`
- `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
- `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
