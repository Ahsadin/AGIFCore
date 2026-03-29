# Graph Stack Model

## Purpose

This file defines the first-pass graph stack for AGIFCore Phase 1.

It freezes the stack vocabulary that later graph and knowledge-structure work must obey.

## Locked graph layers

| Graph layer | First-pass role | Notes |
| --- | --- | --- |
| descriptor graph | holds stable descriptors and typed references | anchors reusable structured support |
| skill graph | holds procedures, callable skills, and their preconditions | stays distinct from generic concept relations |
| concept graph | holds abstractions, theories, and reusable conceptual structure | later semantic abstraction work should land here |
| transfer graph | holds governed transfer relations across domains, cells, or structures | transfer remains explicit and provenance-aware |

## Stack rules

- The graph stack must remain layered even if implementation chooses shared storage.
- Transfer edges require stronger governance than ordinary conceptual association.
- Graph layers are support structures for thinking and replay, not hidden shortcuts around governance.
- Graph references must remain compatible with trace, memory, and simulator surfaces.

## Relationship to other models

- The skill graph is where reusable procedures and tool-like policies should later be anchored.
- The concept graph is where semantic abstraction and theory fragments should later accumulate.
- The descriptor graph is the lowest reusable structure layer for typed support.
- The transfer graph is the explicit home for governed cross-domain or cross-structure movement.

## Dependency notes

- Exact node/edge schemas remain later Phase 5 work.
- Current inheritance and component mappings identify likely graph-facing artifacts but do not complete this stack.
- This file freezes stack boundaries so later graph work is auditable rather than improvised.

## Cross-References

- `projects/agifcore_master/03_design/SKILL_GRAPH_MODEL.md`
- `projects/agifcore_master/03_design/MEMORY_MODEL.md`
- `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
- `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
