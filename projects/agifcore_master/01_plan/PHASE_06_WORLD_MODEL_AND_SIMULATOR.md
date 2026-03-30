# Phase 6: World Model and Simulator

## 1. Phase identity

- Phase number: `6`
- Canonical phase name: `World Model and Simulator`
- Status: `planning_draft`
- Source-of-truth references reviewed:
  - `AGENTS.md`
  - `projects/agifcore_master/AGENTS.override.md`
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_INDEX.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
  - `projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md`
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/01_plan/HUMAN_THINKING_TARGET.md`
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - all files under `projects/agifcore_master/02_requirements/`
  - all files under `projects/agifcore_master/03_design/`
  - approved Phase 2, 3, 4, and 5 surfaces under:
    - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/`
    - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/`
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/`
    - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/`
    - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/`
    - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/`
    - `projects/agifcore_master/04_execution/phase_04_memory_planes/`
    - `projects/agifcore_master/05_testing/phase_04_memory_planes/`
    - `projects/agifcore_master/06_outputs/phase_04_memory_planes/`
    - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/`
    - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/`
    - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/`
  - admin controls:
    - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
    - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
    - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
    - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
    - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`
  - direct inherited-source inspection:
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v1/intelligence/fabric/utility.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v1/intelligence/fabric/domain/finance.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v1/intelligence/fabric/domain/pos_operations.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_5_simulator/agif_phase5_simulator/contracts.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_5_simulator/agif_phase5_simulator/world_model.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_5_simulator/agif_phase5_simulator/simulation.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_5_simulator/agif_phase5_simulator/fault_injection.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_5_simulator/agif_phase5_simulator/pressure.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_5_simulator/agif_phase5_simulator/transfer_conflict.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_5_simulator/agif_phase5_simulator/overload.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_5_simulator/agif_phase5_simulator/instrumentation.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_5_simulator/agif_phase5_simulator/usefulness.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_6a_domain_proofs/agif_phase6a_domain_proofs/contracts.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_6a_domain_proofs/agif_phase6a_domain_proofs/transfer_path.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/README.md`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/agif_phase8b_world_awareness/answer_contract.py`
    - `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/support_graph.py`

## 2. Phase mission

- Phase 6 exists to define and later build the governed world-model and simulator layer above approved memory and graph baselines and below conversation and science/world-awareness behavior.
- Phase 6 must later build:
  - world-model representation
  - entity classes
  - target-domain structures
  - candidate futures
  - what-if simulation
  - fault lanes
  - pressure lanes
  - overload lanes
  - conflict lanes
  - instrumentation
  - usefulness scoring
- Phase 6 must not:
  - implement Phase 7 conversation behavior
  - implement Phase 8 science or world-awareness behavior
  - re-implement Phase 2 kernel or workspace control surfaces
  - re-implement Phase 4 memory storage or Phase 5 graph storage
  - turn simulation into live action or live transfer execution
  - treat historical v1, tasklet, or v2 execution packages as earned AGIFCore completion
  - imply commit, freeze, approval, or closure

## 3. Scope and non-goals

- In-scope artifacts:
  - the canonical Phase 6 plan
  - the Phase 6 planning task-card set
  - world-model and simulator boundary rules
  - reuse and provenance decisions for each major Phase 6 subsystem
  - future execution, testing, outputs, and handoff family targets
  - later demo and closure planning
- Out-of-scope work:
  - any Phase 6 runtime code
  - any Phase 6 verifier code
  - any Phase 6 evidence generation
  - any Phase 7 planning
  - any Phase 8 planning
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
- Explicit untouched-later-phase statement:
  - Phase 7 and all later phases remain untouched by this plan.

## 4. Phase 5 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 5 explicitly approved in current phase-truth files | `pass` | `01_plan/PHASE_INDEX.md` and `01_plan/PHASE_GATE_CHECKLIST.md` both show Phase 5 `approved` and Phase 6 `open` | Phase 6 planning may proceed |
| Explicit user approval record exists | `pass` | `00_admin/codex_threads/handoffs/PHASE_05_USER_VERDICT.md` records verdict `approved` | no silent approval assumption |
| Required Phase 1 artifacts relied on exist | `pass` | provenance package, trace contract, validation protocol, demo protocol, requirements pack, design pack, and admin controls are present | planning has the required governance inputs |
| Required Phase 2 artifacts relied on exist | `pass` | approved plan plus runtime, verifier, evidence, and demo surfaces are present | kernel and workspace seams are inspectable |
| Required Phase 3 artifacts relied on exist | `pass` | approved plan plus runtime, verifier, evidence, and demo surfaces are present | cell, tissue, and bundle seams are inspectable |
| Required Phase 4 artifacts relied on exist | `pass` | approved plan plus runtime, verifier, evidence, demo, validation, and user verdict surfaces are present | reviewed-memory seams are inspectable |
| Required Phase 5 artifacts relied on exist | `pass` | approved plan plus runtime, verifier, evidence, demo, validation, and user verdict surfaces are present | graph, provenance, transfer, and support-selection seams are inspectable |
| Dependency gap: canonical Phase 6 plan file is not present yet | `non-blocker` | `01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md` is the target of this draft | expected planning target, not a prerequisite failure |
| Dependency gap: Phase 6 planning task folder is not present yet | `non-blocker` | no `00_admin/codex_threads/tasks/phase_06/` folder exists yet | expected pre-authoring condition |
| Dependency gap: no AGIFCore Phase 6 runtime, verifier, evidence, or demo families exist yet | `non-blocker` | there is no `04_execution/phase_06_*`, `05_testing/phase_06_*`, or `06_outputs/phase_06_*` family yet | expected future execution output, not a planning blocker |
| Blockers vs non-blockers | `planning not blocked` | all prerequisite approvals and source inputs exist | readiness may be `ready_for_user_review` |

## 5. Active team map for Phase 6

Later Phase 6 execution default build pod: `World & Conversation Pod Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | Must never do this phase |
| --- | --- | --- | --- | --- | --- |
| Program Governor | `gpt-5.4` | active | top planning authority and phase truth control are required | own prerequisite truth, scope lock, active-role map, reuse decisions, workstream order, artifact matrix, closure map, and final plan integration | implement runtime code, self-approve, broaden into Phase 7 |
| Constitution Keeper | `gpt-5.4 mini` | active | Phase 6 can drift into hidden autonomy, live-world reasoning, or conversation behavior | guard constitution, non-negotiables, approval honesty, no-hidden-model rules, and phase boundaries | author runtime design alone, approve the phase, or smuggle Phase 8 science behavior into Phase 6 |
| Source Cartographer | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | inherited simulator substrate must be mapped before execution is planned | map each Phase 6 subsystem to inherited source basis, disposition, and reuse limits | invent a fifth disposition, treat historical packages as already earned AGIFCore runtime, approve the phase |
| Architecture & Contract Lead | `gpt-5.4` | active | world-model and simulator boundaries must be explicit before execution | own Phase 6 subsystem boundaries, allowed interfaces, leak-prevention rules, and alignment to Phase 2/4/5 contracts | redesign the team, collapse simulation into conversation or science behavior, approve the phase |
| Kernel Pod Lead | `gpt-5.3-codex` | consult-only | Phase 6 should consume Phase 2 seams without reopening them | consult only if workspace, replay, rollback, quarantine, or trace-export seams become ambiguous | author the plan, implement code, or expand Phase 2 scope |
| Memory & Graph Pod Lead | `gpt-5.3-codex` | consult-only | Phase 6 must stay above reviewed memory and graph exports without rewriting them | consult only if Phase 4 reviewed-memory exports or Phase 5 graph, transfer, or provenance seams become ambiguous | author the plan, implement code, or pull Phase 6 logic down into Phase 4 or Phase 5 |
| World & Conversation Pod Lead | `gpt-5.3-codex` | active | later execution owner for Phase 6 and default future build pod | provide planning consultation on module breakdown, lane ordering, world-model/runtime-family targets, and the hard stop below Phase 7 | author canonical plan truth alone, implement Phase 6 code in this run, absorb Phase 7 or 8 scope, or approve the phase |
| Meta & Growth Pod Lead | `gpt-5.3-codex` | inactive | danger-zone work is unrelated to Phase 6 planning | none | activate casually or leak self-improvement behavior into Phase 6 |
| Product & Sandbox Pod Lead | `gpt-5.3-codex` | consult-only | Phase 6 may need narrow runtime-shell or bundle-output clarification later | consult only if a runner, bundle, sandbox, or output-surface seam becomes ambiguous | author the plan, implement Phase 13 or 14 work, or broaden product scope |
| Test & Replay Lead | `gpt-5.4 mini` | active | simulation, lane, and scoring behavior must be test-planned from the start | define verifier family, evidence expectations, closure checks, and failure signatures | implement runtime behavior, fake reports, or approve the phase |
| Anti-Shortcut Auditor | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | Phase 6 has high risk of one-big-state shortcuts and fake simulation claims | detect silent omission, greenfield recreation where substrate exists, placeholder evidence, phase drift, and unverifiable claims | author canonical plan content, downgrade blockers, or approve the phase |
| Merge Arbiter | `gpt-5.3-codex` | inactive | planning-only run | none unless later execution integration is needed | author planning content or imply closure |
| Validation Agent | `gpt-5.4` | active | final machine-side review of the plan package is required before user review | validate the Phase 6 planning package and later prepare the review request | author plan content, implement code, or approve the phase |
| Release & Evidence Lead | `gpt-5.4 mini` | active | demos must be inspectable and self-contained later | define evidence grouping, demo bundle shape, and review packet surfaces only | perform release execution, public-claim packaging, or imply acceptance |

## 6. Reuse and provenance strategy

Only the frozen four disposition categories are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance artifact justification |
| --- | --- | --- | --- | --- |
| world-model representation | v2 `04_execution/phase_5_simulator/agif_phase5_simulator/contracts.py` `WorldModel*` contract family and `world_model.py`; approved Phase 5 transfer, provenance, and support-selection outputs | `rebuild_clean` | the typed cell, relation, operator, and provenance shape is the strongest substrate, but the old builder is wired to historical v2 graph contracts and cannot be ported verbatim into AGIFCore. Rebuild the representation against approved AGIFCore Phase 4 and Phase 5 exports while preserving the bounded, execution-disabled, provenance-linked design. | `COMPONENT_CATALOG.md` rows `CC-031`, `CC-033`, `CC-040`, `CC-049`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-050`, `SIM-059` |
| entity classes | v2 `contracts.py` world-model enums and typed state/value/operator classes; v1 `target_domain` contract vocabulary | `rebuild_clean` | AGIFCore needs explicit world-entity, relation, operator, and status types, but those types must bind to approved AGIFCore graph node kinds and memory exports rather than historical `agif_phase4_skill_graph` symbols. | `COMPONENT_CATALOG.md` rows `CC-009`, `CC-031`, `CC-033`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-050`, `SIM-059` |
| target-domain structures | v1 `target_domain` contract, v1 bounded domain fixtures, v2 world-model target projection fields, and Phase 6A proof target-domain prefixes | `port_with_provenance` | `target_domain` is already an explicit inherited contract surface, and Phase 6 should port and normalize it rather than invent a new domain-target vocabulary. Historical domain fixtures remain bounded examples, not proof of runtime completion. | `COMPONENT_CATALOG.md` rows `CC-009`, `CC-048`; `SOURCE_INHERITANCE_MATRIX.md` row `SIM-012` |
| candidate futures | v2 `WhatIfCandidateFuture`, `WhatIfSimulationEntry`, and relation-grounded future expansion in `simulation.py` | `port_with_provenance` | the old future-shape and bounded read-only branch expansion are concrete, inspectable substrate and should be ported with provenance rather than reinvented. The AGIFCore port must stay execution-disabled and must consume approved Phase 6 world-model outputs only. | `COMPONENT_CATALOG.md` row `CC-033`; `TRACE_CONTRACT.md`; `SIMULATOR_MODEL.md` |
| what-if simulation | v2 `simulation.py` relation-grounded what-if builder plus `WhatIfSimulationSnapshot` contract | `port_with_provenance` | the deterministic, fail-closed what-if layer is already close to the target Phase 6 behavior and should be ported with provenance after rebinding to AGIFCore interfaces. It must remain below governance and above world-model representation. | `COMPONENT_CATALOG.md` row `CC-033`; `SIMULATOR_MODEL.md`; `TRACE_CONTRACT.md` |
| fault lanes | v2 `fault_injection.py` and `FaultInjectionSnapshot` contract family | `port_with_provenance` | the old fault overlay is already bounded, read-only, and provenance-linked. Port the lane mechanics with provenance, but keep AGIFCore-specific thresholds and phase boundaries explicit in the new implementation. | `COMPONENT_CATALOG.md` rows `CC-015`, `CC-033`, `CC-040`; `SIMULATOR_MODEL.md` |
| pressure lanes | v1 `memory_pressure` and need-signal substrate plus v2 `pressure.py` scenario cascade structure | `rebuild_clean` | Phase 6 pressure lanes must combine AGIFCore Phase 4 pressure signals, approved world-model outputs, and fail-closed simulation results. The v1 signal vocabulary and v2 lane pattern are useful inputs, but the integrated Phase 6 pressure lane must be rebuilt clean against AGIFCore exports. | `COMPONENT_CATALOG.md` rows `CC-046`, `CC-047`, `CC-033`; `SOURCE_INHERITANCE_MATRIX.md` row `SIM-010` |
| overload lanes | v1 need-signal and overload control vocabulary plus v2 `overload.py` result structure and Phase 6A overload path references | `rebuild_clean` | overload handling depends on AGIFCore-specific lane composition, conflict weighting, and runner-profile ceilings. The historical overload builders are strong research input, but the AGIFCore overload lane must be rebuilt against approved Phase 6 lane outputs and laptop-profile budgets. | `COMPONENT_CATALOG.md` rows `CC-047`, `CC-033`, `CC-051`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-010`, `SIM-050` |
| conflict lanes | approved Phase 5 `conflict_rules.py` and `transfer_graph.py` outputs plus v2 `transfer_conflict.py` and Phase 6A transfer-path conflict records | `rebuild_clean` | Phase 6 conflict lanes must consume AGIFCore Phase 5 governed transfer and conflict state rather than replay historical v2 transfer-conflict snapshots. Rebuild the lane clean while preserving the bounded, read-only, conflict-result structure from the historical substrate. | `COMPONENT_CATALOG.md` rows `CC-008`, `CC-041`, `CC-049`, `CC-033`; `SOURCE_INHERITANCE_MATRIX.md` row `SIM-013` |
| instrumentation | v2 `instrumentation.py`, `InstrumentationSnapshot` contracts, and Phase 6A route-of-custody instrumentation records | `port_with_provenance` | the audit-record, summary, and metric surfaces are already strongly typed and provenance-linked. Port them with provenance so Phase 6 evidence does not regress to prose-only reports. | `COMPONENT_CATALOG.md` rows `CC-040`, `CC-051`, `CC-052`; `TRACE_CONTRACT.md` |
| usefulness scoring | v1 `utility.py` plus v2 `usefulness.py` and Phase 6A proof-domain usefulness measurements | `rebuild_clean` | Phase 6 usefulness scoring must use AGIFCore world-model, lane, and instrumentation outputs plus the approved proof-domain matrix. Reuse the scoring intuition from v1 and the measurement structure from v2, but rebuild the evaluation layer clean so thresholds and inputs are AGIFCore-native and evidence-bound. | `COMPONENT_CATALOG.md` rows `CC-048`, `CC-051`; `SOURCE_INHERITANCE_MATRIX.md` row `SIM-012` |

## 7. World-model and simulator boundary rules

### What belongs in world-model representation only

- read-only modeled world cells derived from approved Phase 5 graph outputs and approved Phase 4 reviewed-memory exports
- typed world relations between modeled entities
- operator slots that record review readiness, hold, blocked, or execution-disabled state
- stable provenance hashes linking each modeled cell or relation back to graph, memory, review, rollback, replay, and governance anchors
- bounded state values, relation strengths, and modeled confidence values
- no user-facing language, no live world fetch, and no live action execution

### What belongs in entity classes only

- typed class and enum definitions for world entities, relation kinds, operator kinds, statuses, state-value types, lane outcomes, and simulator result categories
- shared serialization and schema-facing class structure for Phase 6 runtime, verifier, and evidence surfaces
- no domain fixtures, no candidate-future instances, no live simulation branches, and no instrumentation results

### What belongs in target-domain structures only

- canonical target-domain identifiers, prefixes, typed target-domain objects, and domain-structure metadata
- fixed domain-shape references that later simulation can project onto without inventing new domain labels
- domain-specific object templates and domain matching rules
- no world-model relations, no candidate futures, no what-if expansion, and no conversation-layer intent inference

### What belongs in candidate futures only

- read-only projected future branches derived from current world-model cells, relations, and operator states
- branch identifiers, projected outcomes, branch confidence, and state codes
- bounded branch fanout and branch-depth metadata
- no lane overlays, no instrumentation summaries, and no live transfer or world execution

### What belongs in what-if simulation only

- deterministic evaluation of candidate futures over bounded branch depth
- fail-closed abstain paths when evidence, relation coverage, or operator coverage is insufficient
- simulation entry records, considered relation ids, and replay-safe provenance to world-model inputs
- simulation trace linkage and machine-checkable outcome reasons
- no fault injection, no pressure cascade, no overload scoring, no conversation answer shaping, and no live execution

### What fault, pressure, overload, and conflict lanes must represent

- `fault lanes` must represent explicit fault overlays or degraded scenarios applied to prior what-if branches
- `pressure lanes` must represent bounded stress propagation or pressure accumulation grounded in prior world-model, what-if, and fault outputs
- `overload lanes` must represent bounded overload and unsafe-load evaluation grounded in prior pressure and conflict outputs plus profile budgets
- `conflict lanes` must represent explicit incompatible or blocked simulator paths, including governed transfer-world conflicts and mutually incompatible projected outcomes
- every lane must have machine-checkable outcome types, reason codes, provenance hashes, and replay-safe status
- lane outputs must remain read-only and execution-disabled in Phase 6

### What instrumentation must represent

- per-run records, summaries, and metrics over world-model, what-if, fault, pressure, overload, and conflict outputs
- event counts, fail-closed counts, audited record counts, and explicit lane coverage summaries
- trace-linked and provenance-linked evidence for verifier and demo surfaces
- no release prose, no public claims, and no hand-written `all pass` summaries

### What usefulness scoring must represent

- bounded evaluation of whether Phase 6 world-model and simulator outputs provide domain-specific useful support
- inputs from world-model coverage, candidate futures, lane outputs, and instrumentation records
- explicit thresholds, reason codes, and unsafe-regression checks
- no direct answer selection, no conversation-mode selection, and no bypass around governance or later conversation logic

### What is explicitly forbidden to leak in from Phase 7 conversation behavior

- raw text intake
- question interpretation
- discourse-mode selection
- support-state or knowledge-gap final user-surface decisions
- clarification behavior
- self-knowledge narration
- utterance planning
- response composition
- answer contract generation
- any `response_text` or user-facing language behavior used as a simulator shortcut

### What is explicitly forbidden to leak in from Phase 8 science/world-awareness behavior

- scientific priors execution
- falsification or science-reflection loops
- live current-world lookup
- world-region selection
- entity or request inference from raw user text
- bounded live-fact reasoning or freshness-resolution behavior
- world-awareness curriculum or answer-contract logic
- any behavior that turns Phase 6 local simulation into live world-awareness or live science behavior

### How Phase 6 stays separate from Phase 5 graph implementation except through allowed interfaces

Allowed Phase 5 inputs:

- descriptor, skill, concept, and transfer graph export state
- transfer decisions, decision reasons, target-domain limits, and authority review refs
- provenance bundles and provenance hashes
- conflict-rule outputs and supersession outputs
- support-selection results as read-only optional inputs for building world-model candidates
- graph-layer trust bands, policy requirements, and status markers

Forbidden Phase 5 interactions:

- direct mutation of Phase 5 graph stores
- storing world-model state inside Phase 5 graph modules
- importing raw Phase 5 internal helper state instead of exported store state
- promoting simulator lane results back into graph truth during Phase 6 runtime

### How Phase 6 stays separate from Phase 4 memory implementation except through allowed interfaces

Allowed Phase 4 inputs:

- semantic, procedural, and continuity export state
- approved provenance refs, review refs, and graph refs
- correction and supersession outputs
- rollback-safe update records and rollback refs
- memory-review export references and approved review decisions
- pressure-related reviewed signals only when exported through approved interfaces

Forbidden Phase 4 interactions:

- direct mutation of memory-plane stores by simulator logic
- raw working-memory or episodic buffers being treated as Phase 6 world-model state
- hidden persistence of simulator structures inside Phase 4 memory modules
- bypassing review or correction boundaries to fabricate world-model support

## 8. Phase 6 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Phase 6 planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max entity count before review/escalation | `<= 256` | stop and reopen planning if the later world-model export exceeds `256` entities |
| max target-domain object count before review/escalation | `<= 128` | stop and tighten domain-shape scope if the later target-domain structure exceeds `128` objects |
| max candidate-futures count per simulation | `<= 24` | stop and reduce branch fanout if any simulation entry evaluates more than `24` futures |
| max simulation branch depth | `<= 4` | stop and reopen branch rules if any simulation path goes deeper than `4` hops |
| max fault/pressure/overload/conflict lane count | `<= 32` combined lane result groups per run | stop and escalate if a run requires more than `32` combined lane groups |
| max instrumentation-event count per run | `<= 160` combined records, summaries, and metrics | stop and reorganize instrumentation if a run exceeds `160` instrumentation events |
| max usefulness-score input set size | `<= 64` evidence-linked inputs per scored run | stop and tighten input filters if usefulness scoring needs more than `64` inputs |
| max Phase 6 evidence/demo bundle size | `<= 96 MiB` | stop and reorganize outputs if the Phase 6 evidence plus demo bundle exceeds `96 MiB` |

Budget rules:

- these are laptop-profile planning ceilings only
- later execution must measure against them directly
- if any ceiling is exceeded, stop and escalate to Program Governor instead of widening silently
- if later execution needs higher ceilings, reopen planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md` | Program Governor | Architecture & Contract Lead | Anti-Shortcut Auditor | Validation Agent | Phase 1 provenance package, approved Phase 2-5 baselines, requirements pack, design pack, admin controls, direct legacy-source inspection | all later Phase 6 work | section-complete Phase 6 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/` | Program Governor | Constitution Keeper | Anti-Shortcut Auditor | Validation Agent | task-card template, model manifest, tool matrix, this plan | all later valid Phase 6 work | one planning task card per active role with disjoint scope |
| `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/` | World & Conversation Pod Lead | Architecture & Contract Lead | Anti-Shortcut Auditor | Validation Agent | Phase 6 plan, approved Phase 2-5 surfaces, provenance package, trace contract | later Phase 6 runtime delivery | runtime family exists and matches plan |
| `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/` | World & Conversation Pod Lead | Architecture & Contract Lead | Anti-Shortcut Auditor | Validation Agent | same as above plus exact module breakdown from this plan | later Phase 6 runtime delivery | world model, entities, target domains, candidate futures, what-if, lanes, instrumentation, and usefulness modules exist |
| `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/` | Test & Replay Lead | Program Governor | Anti-Shortcut Auditor | Validation Agent | Phase 6 plan, execution family, validation protocol | later Phase 6 verification and closeout | verifier family exists and runs |
| `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/` | Test & Replay Lead | Release & Evidence Lead | Anti-Shortcut Auditor | Validation Agent | verifier outputs, world-model exports, lane exports, instrumentation exports, usefulness exports | audit, governor verification, validation, demos | machine-readable evidence bundle is inspectable |
| `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/` | Release & Evidence Lead | Program Governor | Anti-Shortcut Auditor | Validation Agent | evidence package, demo protocol, validation protocol | user review | demo bundle exists for causal simulation and stress/conflict inspection |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_EXECUTION_START_BRIEF.md` | Program Governor | Constitution Keeper | Anti-Shortcut Auditor | Validation Agent | approved Phase 6 plan, admin controls | later execution start | execution scope, file families, and no-approval status are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_GOVERNOR_VERIFICATION_RECORD.md` | Program Governor | `n/a` | Anti-Shortcut Auditor | Validation Agent | audited files, rerun verifiers, demo bundle, evidence bundle | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_VALIDATION_REQUEST.md` | Validation Agent | Program Governor | Anti-Shortcut Auditor | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdicts are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_USER_VERDICT.md` | User | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| phase control and prerequisite reconciliation | lock phase truth, active-role map, task-card plan, and closure chain | Program Governor | Constitution Keeper | canonical Phase 6 plan and task-card map | Phase 5 is explicitly approved in live phase-truth files | active and consult-only roles are fixed and Phase 6 stays inside scope |
| reuse and provenance mapping | map each Phase 6 subsystem to legacy source basis and one allowed disposition | Source Cartographer | Program Governor, Constitution Keeper | reuse table and source-basis notes | Phase 1 provenance package and legacy source files reviewed | every subsystem has source basis, disposition, and rationale |
| world-model boundary framing | freeze world-model, entity-class, and allowed-interface rules | Architecture & Contract Lead | Program Governor, World & Conversation Pod Lead | world-model boundary rules and interface limits | approved Phase 2-5 seams reviewed | no one-big-state shortcut remains and Phase 7/8 leaks are explicitly blocked |
| entity and target-domain modeling planning | define world entities, operator/state classes, and target-domain structures | World & Conversation Pod Lead | Source Cartographer, Architecture & Contract Lead | future runtime family layout for `entity_classes.py` and `target_domains.py` | first-pass reuse map and boundary rules exist | entity and target-domain structures are explicit, typed, and bounded |
| candidate-futures and simulation planning | define future branching, branch-depth ceilings, what-if behavior, and simulation trace expectations | World & Conversation Pod Lead | Architecture & Contract Lead, Memory & Graph Pod Lead consult-only | future runtime family layout for `candidate_futures.py` and `what_if_simulation.py` | world-model boundaries and target-domain structures are stable | candidate futures and what-if simulation are explicit, bounded, and replay-safe |
| fault, pressure, overload, and conflict lane planning | define lane order, lane meanings, and lane-specific failure behavior | World & Conversation Pod Lead | Architecture & Contract Lead, Source Cartographer, Memory & Graph Pod Lead consult-only | future runtime family layout for `fault_lanes.py`, `pressure_lanes.py`, `overload_lanes.py`, and `conflict_lanes.py` | candidate-future and simulation planning is stable | every lane has machine-checkable outputs and no prose-only placeholder remains |
| instrumentation and usefulness scoring planning | define the audit-event layer and evidence-bound usefulness evaluation | World & Conversation Pod Lead | Test & Replay Lead, Source Cartographer, Architecture & Contract Lead | future runtime family layout for `instrumentation.py` and `usefulness_scoring.py` | lane planning is stable | usefulness scoring is evidence-bound and instrumentation is not prose-only |
| test, demo, validation, and evidence planning | define verifier family, evidence reports, demo bundle, audit path, and validation path | Test & Replay Lead | Release & Evidence Lead, Program Governor, Validation Agent, Anti-Shortcut Auditor | test plan, evidence plan, demo plan, validation surface | runtime-family targets and boundaries are stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. Program Governor verifies Phase 5 approval truth and opens the Phase 6 task-card set.
2. Source Cartographer maps all required Phase 6 subsystems to source basis and one allowed disposition.
3. Architecture & Contract Lead and World & Conversation Pod Lead draft boundary rules in parallel on disjoint planning outputs.
4. Constitution Keeper reviews the first-pass reuse map and boundary rules for no-hidden-model, no Phase 7 leakage, and no Phase 8 leakage.
5. If a Phase 2 seam is ambiguous after step 4, Kernel Pod Lead is consulted narrowly and remains non-authoring.
6. If a Phase 4 or Phase 5 seam is ambiguous after step 4, Memory & Graph Pod Lead is consulted narrowly and remains non-authoring.
7. If a runner, bundle, sandbox, or output-surface seam is ambiguous after step 4, Product & Sandbox Pod Lead is consulted narrowly and remains non-authoring.
8. World & Conversation Pod Lead decomposes the later Phase 6 runtime family only after first-pass reuse and boundary outputs exist.
9. Test & Replay Lead and Release & Evidence Lead define verifier, evidence, and demo families after the runtime-family targets are stable.
10. Program Governor consolidates the full Phase 6 plan, budget envelope, artifact matrix, workstreams, task-card set, and closure map.
11. Anti-Shortcut Auditor audits the full Phase 6 planning package.
12. Program Governor independently verifies the audited planning package by re-reading the cited files directly.
13. Validation Agent prepares the later review request only after audit and governor verification exist.
14. User review happens only after the validated planning package exists.

Safe parallelism:

- Source Cartographer and Architecture & Contract Lead may work in parallel on disjoint planning outputs.
- World & Conversation Pod Lead waits for first-pass reuse and boundary outputs before locking runtime-family targets.
- Test & Replay Lead and Release & Evidence Lead wait for stable runtime-family targets.
- Merge Arbiter remains inactive in planning-only work.
- One active build pod remains the default later execution rule, and that pod is `World & Conversation Pod Lead`.

## 12. Detailed task cards

Consult-only roles receive no Phase 6 task card unless separately reopened by Program Governor.

### `P6-TC-PG-01`

- task card ID: `P6-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, the Phase 6 plan, task-card map, artifact matrix, budget envelope, and closure chain
- exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-PG-01_PHASE_6_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
  - earlier phase-truth files except to report a prerequisite mismatch
- required reads first:
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2, 3, 4, and 5 plans and execution surfaces
  - relevant requirement and design files
  - admin control stack
- step-by-step work method:
  1. verify Phase 5 approval truth
  2. lock active, consult-only, and inactive roles
  3. consolidate reuse, boundary, runtime-family, verifier, and demo outputs
  4. lock future artifact families and closure mapping
- required cross-checks:
  - no Phase 7 planning
  - no Phase 8 planning
  - no live transfer execution
  - no approval language
- exit criteria:
  - the plan is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation, closure, or approval
- explicit proof that no approval is implied: this task ends at plan readiness only; Phase 6 remains `open`

### `P6-TC-CK-01`

- task card ID: `P6-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4 mini`
- objective: guard constitution, non-negotiables, and Phase 6 boundary discipline
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-CK-01_PHASE_6_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/PHASE_APPROVAL_RULES.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - Phase 6 draft
- step-by-step work method:
  1. check that Phase 6 stays below conversation and science/world-awareness behavior
  2. check that world-model and simulator logic remain local-first, bounded, and trace-linked
  3. check that live world execution and hidden-model loopholes are absent
  4. report any drift to Program Governor
- required cross-checks:
  - no hidden-model loophole
  - no conversation behavior
  - no science/world-awareness behavior
  - no approval language
- exit criteria:
  - constitutional objections are resolved or explicitly raised as blockers
- handoff target: `Program Governor`
- anti-drift rule: do not author architecture or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P6-TC-SC-01`

- task card ID: `P6-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- objective: map every major Phase 6 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-SC-01_PHASE_6_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 4 and Phase 5 plans
  - inspected legacy simulator and domain-proof source files
- step-by-step work method:
  1. map world model, entities, target domains, futures, simulation, lanes, instrumentation, and usefulness
  2. assign one allowed disposition to each
  3. flag where v1 remains a contract source, where v2 remains a bounded substrate, and where research-only boundaries apply
  4. pass unresolved seam notes to ACL and PG
- required cross-checks:
  - no fifth disposition
  - no silent omission
  - no treating old packages as earned AGIFCore runtime
- exit criteria:
  - each subsystem has source basis, disposition, and rationale
- handoff target: `Architecture & Contract Lead` then `Program Governor`
- anti-drift rule: do not claim inspected historical code is already valid AGIFCore runtime
- explicit proof that no approval is implied: provenance mapping does not earn the phase

### `P6-TC-ACL-01`

- task card ID: `P6-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 6 boundaries, allowed interfaces, and forbidden leaks
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-ACL-01_PHASE_6_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
- required reads first:
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 2-5 plans
  - Source Cartographer output
- step-by-step work method:
  1. define what belongs in each Phase 6 subsystem only
  2. define allowed Phase 4 and Phase 5 interfaces
  3. define forbidden Phase 7 and Phase 8 leaks
  4. pass runtime-family implications to PG and WCPL
- required cross-checks:
  - no one mixed state object
  - no user-facing language behavior
  - no live-world or science behavior
  - no direct mutation of graph or memory stores
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `World & Conversation Pod Lead`
- anti-drift rule: do not redesign kernel, memory, graph, or the team
- explicit proof that no approval is implied: boundary framing is planning truth only

### `P6-TC-WCPL-01`

- task card ID: `P6-TC-WCPL-01`
- role owner: `World & Conversation Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 6 runtime family without crossing into Phase 7
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-WCPL-01_PHASE_6_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
- required reads first:
  - approved Phase 2-5 plans and execution surfaces
  - Phase 6 draft
  - Source Cartographer output
  - ACL boundary output
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
- step-by-step work method:
  1. define the future runtime family under `04_execution/phase_06_world_model_and_simulator/`
  2. order module implementation so world model comes before futures, futures before lanes, lanes before instrumentation, and instrumentation before usefulness
  3. identify where Phase 4 and Phase 5 exports must be consumed read-only
  4. flag any seam that would require consult-only role input
- required cross-checks:
  - no runtime code written now
  - no Phase 7 conversation behavior
  - no Phase 8 science/world-awareness behavior
  - no live transfer execution
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase

### `P6-TC-TRL-01`

- task card ID: `P6-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4 mini`
- objective: define the Phase 6 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-TRL-01_PHASE_6_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 2-5 verifier families and evidence bundles
  - Phase 6 draft
- step-by-step work method:
  1. define one verifier per major Phase 6 subsystem group
  2. define evidence reports and manifest contents
  3. define budget-bound and anti-shortcut checks
  4. define failure signatures for each closure requirement
- required cross-checks:
  - tests must verify world/entities/futures/simulation separation
  - candidate futures must show real branching behavior
  - lane outputs must be machine-checkable
  - usefulness scoring must consume evidence-linked inputs
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P6-TC-ASA-01`

- task card ID: `P6-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- objective: audit the Phase 6 planning package for fake completeness, greenfield recreation, and phase drift
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-ASA-01_PHASE_6_PLAN_AUDIT.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
- required reads first:
  - full Phase 6 draft
  - Source Cartographer output
  - ACL boundary output
  - TRL evidence-plan output
  - relevant approved Phase 2-5 plans
- step-by-step work method:
  1. check that all required sections exist
  2. check that each major subsystem has a source basis and disposition
  3. check that no one mixed state object or prose-only lane set is being passed off as design
  4. check that no approval or completion claim is implied
- required cross-checks:
  - no blind rewrite where a plausible substrate exists
  - no silent omission of futures, lanes, instrumentation, or usefulness scoring
  - no Phase 7 or 8 behavior smuggled in
  - no empty report path or unverifiable demo plan
- exit criteria:
  - all blockers are either cleared or explicitly raised
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P6-TC-VA-01`

- task card ID: `P6-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 6 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-VA-01_PHASE_6_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
- required reads first:
  - full Phase 6 draft
  - audit output
  - governor verification output
  - validation protocol
- step-by-step work method:
  1. confirm the plan is decision-complete
  2. confirm every required closure requirement has a later artifact path
  3. confirm the user-review demos are inspectable and truthful
  4. prepare the later review request only after audit and governor verification exist
- required cross-checks:
  - no author/validator role collision
  - no missing review surface
  - no implied approval
- exit criteria:
  - review request scope is exact and inspectable
- handoff target: `Program Governor`
- anti-drift rule: do not author plan content or runtime behavior
- explicit proof that no approval is implied: validation asks for review and does not mark the phase earned

### `P6-TC-REL-01`

- task card ID: `P6-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4 mini`
- objective: define the later Phase 6 demo-bundle shape and review packet surfaces
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-TC-REL-01_PHASE_6_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 2-5 demo bundles
  - TRL verifier/evidence plan
  - Phase 6 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the causal simulation demo surface
  3. define the stress/conflict demo surface
  4. define the review packet order for the user
- required cross-checks:
  - demos must stay inspectable from files alone
  - no demo may imply acceptance or phase completion
  - no public-release packaging creep
- exit criteria:
  - later review packet is exact, ordered, and bounded
- handoff target: `Program Governor` then `Validation Agent`
- anti-drift rule: do not expand into release execution or public claims
- explicit proof that no approval is implied: demo-package planning is not demo acceptance

## 13. Closure-gate mapping

| Closure requirement | Artifact(s) that will satisfy it later | Role responsible | How it will be checked | What failure would look like |
| --- | --- | --- | --- | --- |
| world-model representation exists | `04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/world_model.py`, `05_testing/phase_06_world_model_and_simulator/verify_phase_06_world_model_representation.py`, `06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_world_model_representation_report.json` | World & Conversation Pod Lead | verifier confirms world cells, relations, operators, provenance, and read-only execution-disabled status | one flat mixed state object or no explicit world-model runtime |
| entity classes exist | `entity_classes.py`, `verify_phase_06_entity_classes.py`, `phase_06_entity_classes_report.json` | World & Conversation Pod Lead | verifier confirms typed enums, state classes, lane statuses, and serialization boundaries | lane or entity types are implicit dicts with no typed contract surface |
| target-domain structures exist | `target_domains.py`, `verify_phase_06_target_domain_structures.py`, `phase_06_target_domain_structures_report.json` | World & Conversation Pod Lead | verifier confirms canonical target-domain objects, prefixes, and domain-match rules | domain labels are ad hoc strings or copied directly from user text |
| candidate futures exist | `candidate_futures.py`, `verify_phase_06_candidate_futures.py`, `phase_06_candidate_futures_report.json` | World & Conversation Pod Lead | verifier confirms real branch records, projected outcomes, and bounded future count | candidate futures are labels only or summaries with no branch structure |
| what-if simulation exists | `what_if_simulation.py`, `verify_phase_06_what_if_simulation.py`, `phase_06_what_if_simulation_report.json` | World & Conversation Pod Lead | verifier confirms simulation entries, causal branch evaluation, fail-closed abstain behavior, and trace linkage | simulation returns conclusions without branch records or trace-linked causal steps |
| fault lanes exist | `fault_lanes.py`, `verify_phase_06_fault_pressure_overload_conflict_lanes.py`, `phase_06_fault_pressure_overload_conflict_report.json` | World & Conversation Pod Lead | verifier confirms fault overlays, fault outcomes, fail-closed behavior, and provenance | fault lane exists only as prose or comments |
| pressure lanes exist | `pressure_lanes.py`, `verify_phase_06_fault_pressure_overload_conflict_lanes.py`, `phase_06_fault_pressure_overload_conflict_report.json` | World & Conversation Pod Lead | verifier confirms bounded pressure scenarios, pressure outcomes, and provenance to prior layers | pressure lane has no scenario records or bypasses world-model and what-if inputs |
| overload lanes exist | `overload_lanes.py`, `verify_phase_06_fault_pressure_overload_conflict_lanes.py`, `phase_06_fault_pressure_overload_conflict_report.json` | World & Conversation Pod Lead | verifier confirms overload results, threshold reasoning, and replay-safe outputs | overload lane is a plain threshold note or unverified metric |
| conflict lanes exist | `conflict_lanes.py`, `verify_phase_06_fault_pressure_overload_conflict_lanes.py`, `phase_06_fault_pressure_overload_conflict_report.json` | World & Conversation Pod Lead | verifier confirms blocked, hold, abstain, or clear outcomes with machine-checkable reason codes | conflict lane duplicates Phase 5 graph conflict prose without real simulator results |
| instrumentation exists | `instrumentation.py`, `verify_phase_06_instrumentation.py`, `phase_06_instrumentation_report.json` | World & Conversation Pod Lead | verifier confirms records, summaries, metrics, and coverage checks over all Phase 6 lanes | instrumentation is hand-written markdown or empty summaries with no records |
| usefulness scoring exists | `usefulness_scoring.py`, `verify_phase_06_usefulness_scoring.py`, `phase_06_usefulness_scoring_report.json` | World & Conversation Pod Lead | verifier confirms evidence-linked inputs, thresholds, unsafe-regression checks, and domain-specific scoring | usefulness scoring bypasses instrumentation or ignores provenance |
| demo path exists | `06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/phase_06_demo_index.md`, `phase_06_causal_simulation_demo.md`, `phase_06_stress_conflict_demo.md` | Release & Evidence Lead | direct demo-bundle inspection | no inspectable demo or demo claims unsupported by evidence |
| tests/evidence path exists | verifier family under `05_testing/phase_06_world_model_and_simulator/` and evidence manifest under `06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_evidence_manifest.json` | Test & Replay Lead | governor rerun plus validation request | no machine-readable evidence or missing verifier coverage |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| causal simulation demo | world-model representation, entity classes, target-domain structures, candidate futures, what-if simulation, instrumentation, usefulness scoring, demo index, evidence manifest | Release & Evidence Lead from outputs produced by Test & Replay Lead and World & Conversation Pod Lead | Anti-Shortcut Auditor | world cells and relations, target-domain mapping, candidate branch expansion, causal what-if outcome, simulation trace references, instrumentation record coverage, and the backing evidence reports |
| stress/conflict demo | fault lanes, pressure lanes, overload lanes, conflict lanes, instrumentation, usefulness scoring, demo index, evidence manifest | Release & Evidence Lead from outputs produced by Test & Replay Lead and World & Conversation Pod Lead | Anti-Shortcut Auditor | fault overlays, pressure cascade, overload result, conflict result, hold or abstain behavior, transfer-execution-disabled proof, instrumentation summaries, and the backing evidence reports |

Validation rules for both demos:

- Validation Agent prepares the review request only after audit and governor verification exist.
- Program Governor is the only role that asks the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable simulator substrate | compare subsystem plan and later runtime against mapped v1 and v2 sources | Source Cartographer | any subsystem is rebuilt from zero despite a clear typed historical substrate | stop and reopen reuse mapping before execution proceeds |
| one giant undifferentiated state object pretending to be world model, entities, futures, and simulation | boundary-rule audit and verifier-plan audit | Architecture & Contract Lead | any plan or later code collapses world model, entities, futures, and simulation into one unverifiable store | reject the design and split the layers before continuing |
| candidate futures existing only as labels with no branching behavior | candidate-futures verifier design and later rerun | World & Conversation Pod Lead | no bounded branch structure or branch-depth limit can be verified | block closure until real future-branch records exist |
| fault, pressure, overload, and conflict lanes existing only as prose | closure-gate and verifier audit | Test & Replay Lead | no dedicated runtime family or verifier coverage exists for the lanes | block closure until machine-checkable lane outputs exist |
| usefulness scoring bypassing evidence and instrumentation | usefulness verifier design and evidence audit | Test & Replay Lead | a score can be produced without instrumentation or provenance-linked inputs | stop and force evidence-bound input checks |
| Phase 6 accidentally absorbing Phase 5 graph implementation | interface audit against approved Phase 5 exports | Architecture & Contract Lead | world-model or lane logic reaches into raw graph internals or writes simulator state back into graph modules | reject the seam and limit access to approved exports only |
| Phase 6 accidentally absorbing Phase 7 conversation behavior | boundary audit against Phase 7-forbidden list | Constitution Keeper | discourse mode, clarification, self-knowledge, or answer-composition logic appears in Phase 6 | stop and remove the conversation dependency |
| Phase 6 accidentally absorbing Phase 8 science/world-awareness behavior | boundary audit against Phase 8-forbidden list | Constitution Keeper | scientific priors, live world lookup, falsification, or world-awareness contract logic appears in Phase 6 | stop and remove the science/world-awareness dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 6 plan artifacts
- after user approval, any future change to the Phase 6 plan requires explicit reopen instruction and a supersession note
- Merge Arbiter remains inactive in this planning-only work and may not be activated to imply closure

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 5 is explicitly `approved` in the current phase-truth files and in the explicit user verdict record.
- Phase 6 remains `open`.
- The required Phase 1 provenance package, approved Phase 2-5 baselines, requirement pack, design pack, admin controls, and legacy source candidates were all reviewed directly.
- No prerequisite blocker was found.
- Defaults locked by this draft:
  - later execution keeps one active build pod by default: `World & Conversation Pod Lead`
  - the v2 simulator spine is the main bounded reuse substrate, but it must be rebound to AGIFCore Phase 4 and Phase 5 exports and re-verified inside AGIFCore
  - `target_domain`, candidate futures, what-if simulation, fault lanes, and instrumentation default toward `port_with_provenance`
  - world-model representation, entity classes, pressure, overload, conflict, and usefulness scoring default toward `rebuild_clean`
  - any shared storage choice later is acceptable only if world-model, entities, futures, simulation, lanes, instrumentation, and usefulness scoring remain separately verifiable
