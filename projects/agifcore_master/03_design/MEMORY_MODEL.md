# Memory Model

## Purpose

This file defines the first-pass memory framing for AGIFCore.

It freezes the memory planes and lifecycle expectations that later phases must implement and verify.

## Memory planes

| Plane | First-pass role | Notes |
| --- | --- | --- |
| working memory | hold active turn/task state | must remain bounded and tied to current support construction |
| episodic memory | store event-style history and continuity | must remain replayable and reviewable |
| semantic memory | store stabilized abstractions and concepts | should later align to concept and descriptor graph layers |
| procedural memory | store reusable procedures and skills | should later align to skill graph and governed reuse |
| continuity memory | store self-history and continuity anchors | must support correction and honest self-reference |

## Reviewed memory policy

- reviewed memory with hot, warm, cold, and ephemeral tiers remains a locked design input.
- memory review is a required step, not a best-effort extra.
- promotion, deduplication, supersession, compression, retirement, and memory GC must stay explicit memory responsibilities.
- `memory_pressure` remains a first-class signal for later implementation.

## Hard rules

- Memory is selective, governed, and auditable.
- No memory path may silently bypass review.
- Long-lived memory must preserve provenance and correction ability.
- Memory behavior must support rollback, quarantine, and replay rather than hide them.

## Dependency notes

- Exact storage layout, retention thresholds, and review algorithms remain later implementation work.
- This first-pass design already depends on the trace contract, workspace model, and graph-stack framing.
- Future execution must prove real correction memory and continuity behavior, not just long retention.

## Cross-References

- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
- `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
- `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
