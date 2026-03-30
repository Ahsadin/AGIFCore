# Source Inheritance Matrix

## Purpose

This file is the row-by-row Phase 1 inheritance map for AGIFCore.

If a relevant inherited item is not listed here, it is still missing.

## Source pools

- `SRC-001` `agif_fabric_v1`
- `SRC-002` `agif-tasklet-cell`
- `SRC-003` `root v2 lineage`
- `SRC-004` `agif_v2_master`

## Mapping rules

- Every row must pick exactly one disposition:
  - `rebuild_clean`
  - `port_with_provenance`
  - `adapt_for_research_only`
  - `reject`
- Rows below are first-pass mappings, not final inheritance approval.
- Anything not represented here remains missing.

## Row-by-row inheritance matrix

| ID | Source pool | Inherited item | First-pass disposition | AGIFCore follow-through | Notes |
| --- | --- | --- | --- | --- | --- |
| SIM-001 | `SRC-001` `agif_fabric_v1` | shared workspace coordination | `port_with_provenance` | workspace fabric | direct master-plan coverage |
| SIM-002 | `SRC-001` `agif_fabric_v1` | `runner/cell fabric` operator family | `port_with_provenance` | operator family | direct master-plan coverage |
| SIM-003 | `SRC-001` `agif_fabric_v1` | lifecycle control: activate, split, merge, hibernate, reactivate, retire | `port_with_provenance` | lifecycle engine | direct master-plan coverage |
| SIM-004 | `SRC-001` `agif_fabric_v1` | lineage ledger | `port_with_provenance` | provenance ledger | direct master-plan coverage |
| SIM-005 | `SRC-001` `agif_fabric_v1` | veto log | `port_with_provenance` | authority history | direct master-plan coverage |
| SIM-006 | `SRC-001` `agif_fabric_v1` | rollback snapshots | `port_with_provenance` | rollback support | direct master-plan coverage |
| SIM-007 | `SRC-001` `agif_fabric_v1` | quarantine and containment | `port_with_provenance` | safety boundary | direct master-plan coverage |
| SIM-008 | `SRC-001` `agif_fabric_v1` | reviewed memory with hot, warm, cold, ephemeral tiers | `port_with_provenance` | memory policy | direct master-plan coverage |
| SIM-009 | `SRC-001` `agif_fabric_v1` | promotion, deduplication, supersession, compression, retirement, memory GC | `rebuild_clean` | memory lifecycle | exact behavior must be rebuilt, not assumed |
| SIM-010 | `SRC-001` `agif_fabric_v1` | `memory_pressure` | `rebuild_clean` | memory pressure signal | exact behavior must be rebuilt, not assumed |
| SIM-011 | `SRC-001` `agif_fabric_v1` | need signals | `rebuild_clean` | need signaling | exact behavior must be rebuilt, not assumed |
| SIM-012 | `SRC-001` `agif_fabric_v1` | routing with utility scoring | `port_with_provenance` | routing policy | direct master-plan coverage |
| SIM-013 | `SRC-001` `agif_fabric_v1` | authority approvals and vetoes | `port_with_provenance` | governance policy | direct master-plan coverage |
| SIM-014 | `SRC-001` `agif_fabric_v1` | finance tissue system | `adapt_for_research_only` | research-only unless later justified | direct master-plan coverage |
| SIM-015 | `SRC-001` `agif_fabric_v1` | benchmark and evidence machinery | `port_with_provenance` | evidence support | direct master-plan coverage |
| SIM-016 | `SRC-001` `agif_fabric_v1` | soak harness | `port_with_provenance` | soak / verification | direct master-plan coverage |
| SIM-017 | `SRC-001` `agif_fabric_v1` | machine-role policy | `port_with_provenance` | role policy | direct master-plan coverage |
| SIM-018 | `SRC-001` `agif_fabric_v1` | post-closure extensions: organic split/merge, governed descriptor transfer, POS proof | `adapt_for_research_only` | research-only extension note | direct master-plan coverage |
| SIM-019 | `SRC-001` `agif_fabric_v1` | release note | `port_with_provenance` | release support | direct master-plan coverage |
| SIM-020 | `SRC-001` `agif_fabric_v1` | claims-to-evidence matrix | `port_with_provenance` | evidence support | direct master-plan coverage |
| SIM-021 | `SRC-001` `agif_fabric_v1` | reproducibility package | `port_with_provenance` | evidence packaging | direct master-plan coverage |
| SIM-022 | `SRC-001` `agif_fabric_v1` | final evidence index | `port_with_provenance` | evidence packaging | direct master-plan coverage |
| SIM-023 | `SRC-001` `agif_fabric_v1` | paper-draft status note | `adapt_for_research_only` | research note | direct master-plan coverage |
| SIM-024 | `SRC-002` `agif-tasklet-cell` | offline desktop-first shell and UI | `port_with_provenance` | product shell | direct master-plan coverage |
| SIM-025 | `SRC-002` `agif-tasklet-cell` | local runner | `port_with_provenance` | local runtime entrypoint | direct master-plan coverage |
| SIM-026 | `SRC-002` `agif-tasklet-cell` | gateway/service layer | `port_with_provenance` | local gateway | direct master-plan coverage |
| SIM-027 | `SRC-002` `agif-tasklet-cell` | schema-enforced contracts | `port_with_provenance` | contract layer | direct master-plan coverage |
| SIM-028 | `SRC-002` `agif-tasklet-cell` | bundle integrity checks | `port_with_provenance` | integrity checks | direct master-plan coverage |
| SIM-029 | `SRC-002` `agif-tasklet-cell` | strict policy checks | `port_with_provenance` | policy checks | direct master-plan coverage |
| SIM-030 | `SRC-002` `agif-tasklet-cell` | fail-closed UX | `port_with_provenance` | UX policy | direct master-plan coverage |
| SIM-031 | `SRC-002` `agif-tasklet-cell` | local session memory | `port_with_provenance` | session memory | direct master-plan coverage |
| SIM-032 | `SRC-002` `agif-tasklet-cell` | episodic memory | `port_with_provenance` | memory plane | direct master-plan coverage |
| SIM-033 | `SRC-002` `agif-tasklet-cell` | deterministic reasoning traces | `rebuild_clean` | trace support | the trace behavior must be verified, not copied blindly |
| SIM-034 | `SRC-002` `agif-tasklet-cell` | installer/distribution flow | `port_with_provenance` | installer/distribution | direct master-plan coverage |
| SIM-035 | `SRC-002` `agif-tasklet-cell` | release-readiness flow | `port_with_provenance` | release readiness | direct master-plan coverage |
| SIM-036 | `SRC-002` `agif-tasklet-cell` | evidence packaging | `port_with_provenance` | evidence packaging | direct master-plan coverage |
| SIM-037 | `SRC-002` `agif-tasklet-cell` | SDK and bundle loading | `port_with_provenance` | bundle loading | direct master-plan coverage |
| SIM-038 | `SRC-002` `agif-tasklet-cell` | WASM sandbox | `port_with_provenance` | sandbox boundary | direct master-plan coverage |
| SIM-039 | `SRC-002` `agif-tasklet-cell` | Wasmtime fuel limits | `port_with_provenance` | sandbox budget | direct master-plan coverage |
| SIM-040 | `SRC-002` `agif-tasklet-cell` | Wasmtime memory limits | `port_with_provenance` | sandbox budget | direct master-plan coverage |
| SIM-041 | `SRC-002` `agif-tasklet-cell` | Wasmtime wall-time limits | `port_with_provenance` | sandbox budget | direct master-plan coverage |
| SIM-042 | `SRC-002` `agif-tasklet-cell` | proactive/background agent lane | `adapt_for_research_only` | research-only lane unless later redesign says otherwise | direct master-plan coverage |
| SIM-043 | `SRC-002` `agif-tasklet-cell` | tiny-transformer inference lane | `reject` | hidden cognition path is not Phase 1 baseline material | direct master-plan coverage |
| SIM-044 | `SRC-002` `agif-tasklet-cell` | public release and paper-evidence packaging | `port_with_provenance` | release packaging | direct master-plan coverage |
| SIM-045 | `SRC-002` `agif-tasklet-cell` | tag and public release asset flow | `port_with_provenance` | release flow | direct master-plan coverage |
| SIM-046 | `SRC-003` `root v2 lineage` | root master-plan rewrite logic | `adapt_for_research_only` | historical rewrite rule only | exact supporting path: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/AGIF v2- AGIF Core Unified Master Plan Finalization.md` |
| SIM-047 | `SRC-003` `root v2 lineage` | North-Star addendum logic | `adapt_for_research_only` | historical rewrite rule only | exact supporting path: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/AGIF v2 Phase 7A North-Star Addendum.md` |
| SIM-048 | `SRC-003` `root v2 lineage` | all requirement docs | `adapt_for_research_only` | historical documentation only | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/AGIF_V3_CONCEPT.md` and requirement-docs root `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/02_requirements/` |
| SIM-049 | `SRC-003` `root v2 lineage` | all design docs | `adapt_for_research_only` | historical documentation only | exact supporting path set: design-docs root `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/03_design/` and verified runtime file-set root `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/` |
| SIM-050 | `SRC-003` `root v2 lineage` | all reusable execution packages from phases 2 through 10 | `reject` | old execution artifacts do not count as AGIFCore completion | exact supporting path set: execution-packages root `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/`, plus phase 8/8b/8c/9 directories `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8_embedding/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8c_governed_structural_growth/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/`, and the phase 10 plan file `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/PHASE_10_MSI_SOAK_RELEASE_HARDENING_AND_PUBLICATION_PLAN.md` |
| SIM-051 | `SRC-003` `root v2 lineage` | `AGIF_V3_CONCEPT.md` | `adapt_for_research_only` | historical concept note only | exact supporting path: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/AGIF_V3_CONCEPT.md` |
| SIM-052 | `SRC-003` `root v2 lineage` | all `8A`, `8B`, `8C`, `9`, and `10` logic | `adapt_for_research_only` | historical phase logic only | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8_embedding/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8c_governed_structural_growth/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/`, and `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/PHASE_10_MSI_SOAK_RELEASE_HARDENING_AND_PUBLICATION_PLAN.md` |
| SIM-053 | `SRC-003` `root v2 lineage` | all concrete runtime and contract components already identified in code | `rebuild_clean` | runtime and contract rebuild | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/runtime.py`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/orchestrator.py`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/question_analyzer.py`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/answer_composer.py`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/whole_stack_activation.py` |
| SIM-054 | `SRC-003` `root v2 lineage` | publication, hardening, and public release flow from the Phase 10 lane | `adapt_for_research_only` | historical release flow only | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/PHASE_10_MSI_SOAK_RELEASE_HARDENING_AND_PUBLICATION_PLAN.md`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/06_outputs/publication_notes/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/06_outputs/releases/` |
| SIM-055 | `SRC-004` `agif_v2_master` | root master-plan rewrite logic | `adapt_for_research_only` | historical rewrite rule only | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2` and `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/AGIF v2- AGIF Core Unified Master Plan Finalization.md` |
| SIM-056 | `SRC-004` `agif_v2_master` | North-Star addendum logic | `adapt_for_research_only` | historical rewrite rule only | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2` and `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/AGIF v2 Phase 7A North-Star Addendum.md` |
| SIM-057 | `SRC-004` `agif_v2_master` | all requirement docs | `adapt_for_research_only` | historical documentation only | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/AGIF_V3_CONCEPT.md`, and `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/02_requirements/` |
| SIM-058 | `SRC-004` `agif_v2_master` | all design docs | `adapt_for_research_only` | historical documentation only | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/03_design/`, and `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/` |
| SIM-059 | `SRC-004` `agif_v2_master` | all reusable execution packages from phases 2 through 10 | `reject` | old execution artifacts do not count as AGIFCore completion | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8_embedding/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8c_governed_structural_growth/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/`, and `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/PHASE_10_MSI_SOAK_RELEASE_HARDENING_AND_PUBLICATION_PLAN.md` |
| SIM-060 | `SRC-004` `agif_v2_master` | `AGIF_V3_CONCEPT.md` | `adapt_for_research_only` | historical concept note only | exact supporting path: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/AGIF_V3_CONCEPT.md` |
| SIM-061 | `SRC-004` `agif_v2_master` | all `8A`, `8B`, `8C`, `9`, and `10` logic | `adapt_for_research_only` | historical phase logic only | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8_embedding/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8c_governed_structural_growth/`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/`, and `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/PHASE_10_MSI_SOAK_RELEASE_HARDENING_AND_PUBLICATION_PLAN.md` |
| SIM-062 | `SRC-004` `agif_v2_master` | all concrete runtime and contract components already identified in code | `rebuild_clean` | runtime and contract rebuild | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/runtime.py`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/orchestrator.py`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/question_analyzer.py`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/answer_composer.py`, and `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/whole_stack_activation.py` |
| SIM-063 | `SRC-004` `agif_v2_master` | publication, hardening, and public release flow from the Phase 10 lane | `adapt_for_research_only` | historical release flow only | exact supporting path set: `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/01_plan/PHASE_10_MSI_SOAK_RELEASE_HARDENING_AND_PUBLICATION_PLAN.md`, `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/06_outputs/publication_notes/`, and `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/06_outputs/releases/` |

## Unresolved lineage items

- The SRC-003 and SRC-004 rows now carry exact supporting path evidence for each row, with exact path or path-set references attached to every row.
- Row-by-row path confirmation is now established at the level of exact historical file paths or exact directory path sets.
- Semantic inheritance approval is still not claimed here; the matrix remains a first-pass mapping and later code-level confirmation is still required before any final inheritance approval.
