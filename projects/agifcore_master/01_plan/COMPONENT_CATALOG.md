# Component Catalog

## Purpose

This file is the Phase 1 component inventory for AGIFCore.

It is intentionally row-based. If a component is not listed here, it is still missing for Phase 1 planning purposes.

## Scope

- Source basis is the frozen Phase 0 inventory plus the frozen Phase 1 master plan.
- This file does not port code.
- This file does not claim that any inherited component is complete.
- This file records exact names, current source basis, and the first-pass AGIFCore disposition.
- Exact row-by-row historical path coverage for `SRC-003` and `SRC-004` lives in `SOURCE_INHERITANCE_MATRIX.md`.

## Exact inherited component names

| ID | Component name | Source basis | First-pass disposition | AGIFCore target | Notes |
| --- | --- | --- | --- | --- | --- |
| CC-001 | `EventType` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | event fabric typing | exact inherited concrete name from the master plan |
| CC-002 | `Event` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | event fabric payload | exact inherited concrete name from the master plan |
| CC-003 | `CellContract` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | common cell contract | exact inherited concrete name from the master plan |
| CC-004 | `LogicalCell` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | logical cell runtime surface | exact inherited concrete name from the master plan |
| CC-005 | `CellRegistry` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | cell registry | exact inherited concrete name from the master plan |
| CC-006 | `LifecycleEngine` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | lifecycle engine | exact inherited concrete name from the master plan |
| CC-007 | `Scheduler` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | scheduling / budget control | exact inherited concrete name from the master plan |
| CC-008 | `transfer_descriptor` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | transfer contract | exact inherited concrete name from the master plan |
| CC-009 | `target_domain` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | routing target contract | exact inherited concrete name from the master plan |
| CC-010 | `ScientificPriorCell` | `SRC-001 agif_fabric_v1` | `adapt_for_research_only` | research prior / scientific lane | exact inherited concrete name from the master plan |
| CC-011 | `SelfModelRecord` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | self-history / continuity | exact inherited concrete name from the master plan |
| CC-012 | `MetaCognitionObserverRecord` | `SRC-001 agif_fabric_v1` | `adapt_for_research_only` | meta-cognition / critique | exact inherited concrete name from the master plan |
| CC-013 | `StrategyJournalEntry` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | planner / strategy journal | exact inherited concrete name from the master plan |
| CC-014 | `SkepticCounterexampleRecord` | `SRC-001 agif_fabric_v1` | `adapt_for_research_only` | critic / counterexample tracking | exact inherited concrete name from the master plan |
| CC-015 | `SurpriseEngineRecord` | `SRC-001 agif_fabric_v1` | `rebuild_clean` | surprise and anomaly handling | exact inherited concrete name from the master plan |
| CC-016 | `ThinkerTissueRecord` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | thinker tissue / audit-replay support | exact inherited concrete name from the master plan |
| CC-017 | `SelfModelFeedbackLoopRecord` | `SRC-001 agif_fabric_v1` | `adapt_for_research_only` | feedback loop / self-history | exact inherited concrete name from the master plan |
| CC-018 | `ReflectionControlLoopRecord` | `SRC-001 agif_fabric_v1` | `adapt_for_research_only` | reflection / idle reflection support | exact inherited concrete name from the master plan |
| CC-019 | `proposal_generator` | `SRC-001 agif_fabric_v1` | `rebuild_clean` | proposal generation | exact inherited concrete name from the master plan |
| CC-020 | `science_reflection` | `SRC-001 agif_fabric_v1` | `adapt_for_research_only` | science / falsification support | exact inherited concrete name from the master plan |
| CC-021 | `theory_fragment` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | theory storage | exact inherited concrete name from the master plan |
| CC-022 | `strategy_journal` | `SRC-001 agif_fabric_v1` | `port_with_provenance` | strategy journal | exact inherited concrete name from the master plan |
| CC-023 | `ConversationTurnRecord` | `SRC-003 root v2 lineage` | `port_with_provenance` | conversation trace | exact inherited contract item from the master plan |
| CC-024 | `ConversationSnapshot` | `SRC-003 root v2 lineage` | `port_with_provenance` | conversation trace | exact inherited contract item from the master plan |
| CC-025 | `concept_composition_ref` | `SRC-003 root v2 lineage` | `port_with_provenance` | composition trace reference | exact inherited contract item from the master plan |
| CC-026 | `revision_trace_ref` | `SRC-003 root v2 lineage` | `port_with_provenance` | revision trace reference | exact inherited contract item from the master plan |
| CC-027 | `analogy_trace_ref` | `SRC-003 root v2 lineage` | `port_with_provenance` | analogy trace reference | exact inherited contract item from the master plan |
| CC-028 | `consolidation_trace_ref` | `SRC-003 root v2 lineage` | `port_with_provenance` | consolidation trace reference | exact inherited contract item from the master plan |
| CC-029 | `reorganization_trace_ref` | `SRC-003 root v2 lineage` | `port_with_provenance` | reorganization trace reference | exact inherited contract item from the master plan |
| CC-030 | `proof-intake` | `SRC-003 root v2 lineage` | `rebuild_clean` | proof intake tissue role | exact inherited tissue-role name from the master plan |
| CC-031 | `world-model-review` | `SRC-003 root v2 lineage` | `rebuild_clean` | world model review tissue role | exact inherited tissue-role name from the master plan |
| CC-032 | `planner` | `SRC-003 root v2 lineage` | `port_with_provenance` | planner tissue role | exact inherited tissue-role name from the master plan |
| CC-033 | `simulator` | `SRC-003 root v2 lineage` | `rebuild_clean` | simulator tissue role | exact inherited tissue-role name from the master plan |
| CC-034 | `critic` | `SRC-003 root v2 lineage` | `port_with_provenance` | critic tissue role | exact inherited tissue-role name from the master plan |
| CC-035 | `governance` | `SRC-003 root v2 lineage` | `port_with_provenance` | governance tissue role | exact inherited tissue-role name from the master plan |
| CC-036 | `audit` | `SRC-003 root v2 lineage` | `port_with_provenance` | audit tissue role | exact inherited tissue-role name from the master plan |

## AGIFCore subsystem surfaces to keep visible

| ID | Subsystem surface | Source basis | First-pass disposition | AGIFCore target | Notes |
| --- | --- | --- | --- | --- | --- |
| CC-037 | shared workspace coordination | `SRC-001 agif_fabric_v1` | `port_with_provenance` | workspace fabric | explicitly named in the master plan |
| CC-038 | `runner/cell fabric` operator family | `SRC-001 agif_fabric_v1` | `port_with_provenance` | operator family | explicitly named in the master plan |
| CC-039 | lifecycle control: activate, split, merge, hibernate, reactivate, retire | `SRC-001 agif_fabric_v1` | `port_with_provenance` | lifecycle engine | exact control verbs must stay explicit |
| CC-040 | lineage ledger | `SRC-001 agif_fabric_v1` | `port_with_provenance` | provenance ledger | exact source-of-truth support surface |
| CC-041 | veto log | `SRC-001 agif_fabric_v1` | `port_with_provenance` | authority history | exact source-of-truth support surface |
| CC-042 | rollback snapshots | `SRC-001 agif_fabric_v1` | `port_with_provenance` | rollback support | exact source-of-truth support surface |
| CC-043 | quarantine and containment | `SRC-001 agif_fabric_v1` | `port_with_provenance` | safety boundary | exact source-of-truth support surface |
| CC-044 | reviewed memory with hot, warm, cold, ephemeral tiers | `SRC-001 agif_fabric_v1` | `port_with_provenance` | memory policy | exact source-of-truth support surface |
| CC-045 | promotion, deduplication, supersession, compression, retirement, memory GC | `SRC-001 agif_fabric_v1` | `rebuild_clean` | memory lifecycle | exact source-of-truth support surface |
| CC-046 | `memory_pressure` | `SRC-001 agif_fabric_v1` | `rebuild_clean` | memory pressure signal | exact source-of-truth support surface |
| CC-047 | need signals | `SRC-001 agif_fabric_v1` | `rebuild_clean` | need signaling | exact source-of-truth support surface |
| CC-048 | routing with utility scoring | `SRC-001 agif_fabric_v1` | `port_with_provenance` | routing policy | exact source-of-truth support surface |
| CC-049 | authority approvals and vetoes | `SRC-001 agif_fabric_v1` | `port_with_provenance` | governance policy | exact source-of-truth support surface |
| CC-050 | finance tissue system | `SRC-001 agif_fabric_v1` | `adapt_for_research_only` | finance tissue | exact source-of-truth support surface |
| CC-051 | benchmark and evidence machinery | `SRC-001 agif_fabric_v1` | `port_with_provenance` | evidence policy | exact source-of-truth support surface |
| CC-052 | soak harness | `SRC-001 agif_fabric_v1` | `port_with_provenance` | soak / verification | exact source-of-truth support surface |
| CC-053 | machine-role policy | `SRC-001 agif_fabric_v1` | `port_with_provenance` | role policy | exact source-of-truth support surface |
| CC-054 | post-closure extensions: organic split/merge, governed descriptor transfer, POS proof | `SRC-001 agif_fabric_v1` | `adapt_for_research_only` | extension boundary | exact source-of-truth support surface |
| CC-055 | release note | `SRC-001 agif_fabric_v1` | `port_with_provenance` | release support | exact source-of-truth support surface |
| CC-056 | claims-to-evidence matrix | `SRC-001 agif_fabric_v1` | `port_with_provenance` | evidence support | exact source-of-truth support surface |
| CC-057 | reproducibility package | `SRC-001 agif_fabric_v1` | `port_with_provenance` | evidence packaging | exact source-of-truth support surface |
| CC-058 | final evidence index | `SRC-001 agif_fabric_v1` | `port_with_provenance` | evidence packaging | exact source-of-truth support surface |
| CC-059 | paper-draft status note | `SRC-001 agif_fabric_v1` | `adapt_for_research_only` | research/status note | exact source-of-truth support surface |
| CC-060 | offline desktop-first shell and UI | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | product shell | explicitly named in the master plan |
| CC-061 | local runner | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | local runtime entrypoint | explicitly named in the master plan |
| CC-062 | gateway/service layer | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | local gateway | explicitly named in the master plan |
| CC-063 | schema-enforced contracts | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | contract layer | explicitly named in the master plan |
| CC-064 | bundle integrity checks | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | integrity checks | explicitly named in the master plan |
| CC-065 | strict policy checks | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | policy checks | explicitly named in the master plan |
| CC-066 | fail-closed UX | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | UX policy | explicitly named in the master plan |
| CC-067 | local session memory | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | session memory | explicitly named in the master plan |
| CC-068 | episodic memory | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | memory plane | explicitly named in the master plan |
| CC-069 | deterministic reasoning traces | `SRC-002 agif-tasklet-cell` | `rebuild_clean` | trace support | explicitly named in the master plan |
| CC-070 | installer/distribution flow | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | installer/distribution | explicitly named in the master plan |
| CC-071 | release-readiness flow | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | release readiness | explicitly named in the master plan |
| CC-072 | evidence packaging | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | evidence packaging | explicitly named in the master plan |
| CC-073 | SDK and bundle loading | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | bundle loading | explicitly named in the master plan |
| CC-074 | WASM sandbox | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | sandbox boundary | explicitly named in the master plan |
| CC-075 | Wasmtime fuel limits | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | sandbox budget | explicitly named in the master plan |
| CC-076 | Wasmtime memory limits | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | sandbox budget | explicitly named in the master plan |
| CC-077 | Wasmtime wall-time limits | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | sandbox budget | explicitly named in the master plan |
| CC-078 | proactive/background agent lane | `SRC-002 agif-tasklet-cell` | `adapt_for_research_only` | research lane only | explicitly named in the master plan |
| CC-079 | tiny-transformer inference lane | `SRC-002 agif-tasklet-cell` | `reject` | do not inherit as AGIFCore baseline | explicitly named in the master plan |
| CC-080 | public release and paper-evidence packaging | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | release packaging | explicitly named in the master plan |
| CC-081 | tag and public release asset flow | `SRC-002 agif-tasklet-cell` | `port_with_provenance` | release flow | explicitly named in the master plan |
| CC-082 | root master-plan rewrite logic | `SRC-003 root v2 lineage` | `adapt_for_research_only` | rewrite governance | explicit v2 lineage only |
| CC-083 | North-Star addendum logic | `SRC-003 root v2 lineage` | `adapt_for_research_only` | target-setting note | explicit v2 lineage only |
| CC-084 | all requirement docs | `SRC-004 agif_v2_master` | `adapt_for_research_only` | historical documentation | explicit v2 lineage only |
| CC-085 | all design docs | `SRC-004 agif_v2_master` | `adapt_for_research_only` | historical documentation | explicit v2 lineage only |
| CC-086 | reusable execution packages from phases 2 through 10 | `SRC-004 agif_v2_master` | `reject` | do not inherit old execution as completion | explicit v2 lineage only |
| CC-087 | `AGIF_V3_CONCEPT.md` | `SRC-004 agif_v2_master` | `adapt_for_research_only` | historical concept note | explicit v2 lineage only |
| CC-088 | all `8A`, `8B`, `8C`, `9`, and `10` logic | `SRC-004 agif_v2_master` | `adapt_for_research_only` | historical phase logic | explicit v2 lineage only |
| CC-089 | all concrete runtime and contract components already identified in code | `SRC-004 agif_v2_master` | `rebuild_clean` | runtime/contract rebuild | representative runtime-module paths are verified in `SOURCE_INHERITANCE_MATRIX.md` and `RUNTIME_REBUILD_MAP.md` |
| CC-090 | publication, hardening, and public release flow from the Phase 10 lane | `SRC-004 agif_v2_master` | `adapt_for_research_only` | release history only | explicit v2 lineage only |

## Unresolved lineage items

- Verified historical roots exist at `<historical_local_source>/agif_fabric_v2` and `<historical_local_source>/agif_fabric_v2/projects/agif_v2_master`.
- Exact row-by-row path evidence for `SRC-003` and `SRC-004` is recorded in `SOURCE_INHERITANCE_MATRIX.md`, and representative runtime-module verification is recorded in `RUNTIME_REBUILD_MAP.md`.
- Where `SRC-003` and `SRC-004` overlap, this catalog keeps the historical surface visible at the component level while `SOURCE_INHERITANCE_MATRIX.md` carries the exact path-set coverage.
- This catalog remains first-pass lineage cartography only. It does not claim final semantic inheritance approval.
- No code-level component ownership or runtime approval can be claimed from this catalog alone.
