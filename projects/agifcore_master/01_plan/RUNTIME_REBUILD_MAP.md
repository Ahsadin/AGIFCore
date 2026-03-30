# Runtime Rebuild Map

## Purpose

This file maps the runtime modules named by the frozen master plan to AGIFCore first-pass ownership and rebuild paths.

It is a cartography artifact, not an implementation artifact.

## Module map

| ID | Runtime module | Source basis | First-pass disposition | AGIFCore target | Notes |
| --- | --- | --- | --- | --- | --- |
| RRM-001 | `runtime.py` | `SRC-004 agif_v2_master` | `rebuild_clean` | AGIFCore runtime entrypoint | exact module name from the master plan |
| RRM-002 | `orchestrator.py` | `SRC-004 agif_v2_master` | `rebuild_clean` | AGIFCore orchestrator | exact module name from the master plan |
| RRM-003 | `question_analyzer.py` | `SRC-003 root v2 lineage` | `rebuild_clean` | question / intake analysis lane | exact module name from the master plan |
| RRM-004 | `support_graph.py` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | support graph / routing substrate | exact module name from the master plan |
| RRM-005 | `memory_runtime.py` | `SRC-001 agif_fabric_v1` | `rebuild_clean` | memory runtime | exact module name from the master plan |
| RRM-006 | `answer_composer.py` | `SRC-003 root v2 lineage` | `rebuild_clean` | answer composition / language realization | exact module name from the master plan |
| RRM-007 | `idle_reflection.py` | `SRC-001 agif_fabric_v1` | `adapt_for_research_only` | idle reflection / self-history lane | exact module name from the master plan |
| RRM-008 | `whole_stack_activation.py` | `SRC-004 agif_v2_master` | `rebuild_clean` | whole-stack activation controller | exact module name from the master plan |
| RRM-009 | `demo_shell.py` | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | demo shell / user review surface | exact module name from the master plan |
| RRM-010 | `contracts.py` | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | schema-enforced contracts | exact module name from the master plan |

## Rebuild notes

- `runtime.py` and `orchestrator.py` are treated as clean AGIFCore rebuilds because the frozen master plan names them as runtime control surfaces, not as trusted final implementation.
- `question_analyzer.py`, `answer_composer.py`, and `whole_stack_activation.py` are kept explicit because they describe later runtime behavior that must not be smuggled in silently.
- `support_graph.py`, `memory_runtime.py`, `demo_shell.py`, and `contracts.py` are the most obvious carry/port candidates, but they still require direct Phase 1 verification before they can be called complete.
- `idle_reflection.py` is only a research-adjacent first-pass mapping until the later phase proves the intended self-history behavior.

## Unresolved runtime-module items

- Verified historical root paths exist at `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2` and `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master`.
- Sample file-level verification has been performed against representative sources, including `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/AGIF_V3_CONCEPT.md` and the Phase 9 runtime files under `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/`.
- Exact row-by-row supporting paths for the broader `SRC-003` and `SRC-004` historical surfaces are recorded in `SOURCE_INHERITANCE_MATRIX.md`.
- This map is still first-pass lineage cartography, not final runtime approval.
- This file does not claim that any runtime module is already implemented in AGIFCore.
- This file does not claim that any runtime module is safe to execute.
