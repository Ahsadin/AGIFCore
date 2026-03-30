# Architecture Overview

## Purpose

This file gives the first-pass architecture framing for AGIFCore Phase 1.

It freezes the major system boundaries that later phases must respect without claiming that runtime implementation already exists.

## Top-level architecture lanes

| Lane | First-pass role | What it owns | What it must not do |
| --- | --- | --- | --- |
| product surface | local desktop UI | human-facing interaction and inspectable evidence surfaces | own correctness or hidden cognition |
| local gateway/API | local gateway | contract transport, validation, and local control surface | become the cognition core |
| runner core | local runner | turn execution, trace production, memory-review handoff, and governed orchestration | bypass governance or contract validation |
| governed cognition substrate | later Phase 2-12 runtime layers | fabric, cells, memory, graph, simulator, critique, and governance logic | leak around the runner/gateway/UI contract |
| evidence and release lane | later Phase 15-16 packaging | traces, exports, evidence bundles, release packaging, and public proof | redefine runtime truth after the fact |

## Frozen split to preserve

- `runner core`
- `local gateway/API`
- `local desktop UI`

The split above must remain explicit in all later design and runtime work.

## Architectural rules

- AGIFCore remains local-first and may not depend on hidden external models or cloud correctness.
- Build-machine roles stay outside runtime truth.
- The conversation surface is the expression layer, not the cognition core.
- Shared workspace coordination, operator family behavior, trace export, bundle integrity, and sandbox enforcement must stay inspectable.
- Release and publication flows are downstream architecture lanes, not add-on afterthoughts.

## Dependency notes

- This first-pass overview is already aligned to the current constitution and inheritance mapping.
- Final detail for cell families, memory planes, graph stack, and simulator boundaries still depends on the rest of the design pack becoming substantive.
- No architecture wording here should be treated as implementation-complete until the later audited design pack exists.

## Cross-References

- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
- `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
