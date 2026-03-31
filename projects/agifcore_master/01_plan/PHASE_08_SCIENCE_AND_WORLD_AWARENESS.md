# Phase 8: Science and World Awareness

## 1. Phase identity

- Phase number: `8`
- Canonical phase name: `Science and World Awareness`
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
  - `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
  - `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md`
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
  - approved Phase 2, 3, 4, 5, 6, and 7 execution, testing, and output surfaces under:
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
    - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/`
    - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/`
    - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/`
    - `projects/agifcore_master/04_execution/phase_07_conversation_core/`
    - `projects/agifcore_master/05_testing/phase_07_conversation_core/`
    - `projects/agifcore_master/06_outputs/phase_07_conversation_core/`
  - admin control files:
    - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
    - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
    - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
    - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
    - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`
  - direct inherited-source inspection:
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/README.md`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/agif_phase8b_world_awareness/contracts.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/agif_phase8b_world_awareness/answer_contract.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/agif_phase8b_world_awareness/world_awareness_curriculum.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/agif_phase8b_world_awareness/derived_science_runtime.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/agif_phase8b_world_awareness/grounded_fact_runtime.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8c_governed_structural_growth/agif_phase8c_governed_structural_growth/contracts.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8c_governed_structural_growth/agif_phase8c_governed_structural_growth/runtime.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/contracts.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/question_analyzer.py`

## 2. Phase mission

- Phase 8 exists to define and later build the governed science and world-awareness layer that sits above approved Phase 6 simulator outputs and Phase 7 conversation baselines without collapsing into live-search execution or later meta-cognition.
- Phase 8 must later build:
  - scientific priors
  - entity/request inference
  - world-region selection
  - causal-chain reasoning
  - bounded current-world reasoning
  - visible reasoning summaries
  - science reflection
- Phase 8 must not:
  - implement Phase 9 rich-expression behavior
  - implement Phase 10 meta-cognition behavior
  - re-implement Phase 2 kernel or workspace control surfaces
  - re-implement Phase 4 memory storage, Phase 5 graph storage, Phase 6 simulator logic, or Phase 7 conversation execution
  - execute live external search inside the Phase 8 layer
  - treat visible reasoning summaries as hidden chain-of-thought disclosure
  - treat historical v1, tasklet, or v2 packages as earned AGIFCore completion
  - imply commit, freeze, approval, or closure

## 3. Scope and non-goals

- In-scope artifacts:
  - the canonical Phase 8 plan
  - Phase 8 planning task cards
  - science/world-awareness boundary rules
  - reuse and provenance decisions for each major Phase 8 subsystem
  - future execution, testing, output, and handoff targets
  - later demo, validation, and closure planning
- Out-of-scope work:
  - any Phase 8 runtime code
  - any Phase 8 verifier code
  - any Phase 8 evidence generation
  - any Phase 9 planning
  - any Phase 10 planning
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
- Explicit untouched-later-phase statement:
  - Phase 9 and all later phases remain untouched by this plan.

## 4. Phase 7 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 7 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` show Phase 7 `approved` and Phase 8 `open` | Phase 8 planning may proceed |
| Explicit Phase 7 closeout truth exists outside index tables | `pass` | `projects/agifcore_master/DECISIONS.md` and `projects/agifcore_master/CHANGELOG.md` record Phase 7 approval and closeout on `2026-03-31` | no silent approval assumption |
| Required Phase 1 artifacts relied on exist | `pass` | provenance package, trace contract, validation protocol, demo protocol, requirements pack, design pack, and admin controls are present | planning has required governance inputs |
| Required Phase 2 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | workspace, turn, replay, and trace seams are inspectable |
| Required Phase 3 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | structural cell, tissue, and bundle seams are inspectable |
| Required Phase 4 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | reviewed memory and continuity export seams are inspectable |
| Required Phase 5 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | support-selection, provenance, trust, and policy seams are inspectable |
| Required Phase 6 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | target-domain, world-model, simulation, lane, instrumentation, and usefulness seams are inspectable |
| Required Phase 7 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | intake, interpretation, support-state, and answer-contract seams are inspectable |
| Dependency gap: canonical Phase 8 plan file did not exist before this drafting pass | `non-blocker` | `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md` is the product of this planning run | expected planning target, not a prerequisite failure |
| Dependency gap: Phase 8 planning task folder was opened during this drafting pass | `non-blocker` | `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/` now exists to hold the planning task-card set | expected planning support surface, not a prerequisite failure |
| Dependency gap: no AGIFCore Phase 8 runtime, testing, evidence, or demo families exist yet | `non-blocker` | there is no `phase_08_*` execution family yet | expected future execution output, not a planning blocker |
| Blockers vs non-blockers | `planning not blocked` | all prerequisite approvals and source inputs exist | readiness may be `ready_for_user_review` |

## 5. Active team map for Phase 8

Later Phase 8 execution default build pod: `World & Conversation Pod Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | What it must never do this phase |
| --- | --- | --- | --- | --- | --- |
| `Program Governor` | `gpt-5.4` | active | top planning authority and phase-truth control are required | own prerequisite truth, scope lock, active-role map, reuse decisions, workstream order, artifact matrix, closure map, and final plan integration | implement runtime code, self-approve, or broaden into Phase 9 |
| `Constitution Keeper` | `gpt-5.4 mini` | active | Phase 8 can drift into fake science certainty, live-world overclaim, or later-phase meta leakage | guard constitution, non-negotiables, falsification honesty, no-hidden-model rules, and phase boundaries | author runtime design alone, approve the phase, or smuggle Phase 9 or Phase 10 behavior into Phase 8 |
| `Source Cartographer` | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | inherited science and world-awareness substrate must be mapped before execution is planned | map each Phase 8 subsystem to inherited source basis, disposition, and reuse limits | invent a fifth disposition, treat historical packages as already earned AGIFCore runtime, or approve the phase |
| `Architecture & Contract Lead` | `gpt-5.4` | active | science/world-awareness boundaries and visible reasoning interfaces must be explicit before execution | own subsystem boundaries, allowed interfaces, forbidden leaks, and alignment to Phase 6 and Phase 7 contracts | redesign the team, collapse science into conversation or simulator logic, or approve the phase |
| `Kernel Pod Lead` | `gpt-5.3-codex` | consult-only | Phase 8 should consume Phase 2 session, trace, and replay seams without reopening them | consult only if workspace, replay, rollback, trace-export, or session-turn seams become ambiguous | author the plan, implement code, or expand Phase 2 scope |
| `Memory & Graph Pod Lead` | `gpt-5.3-codex` | consult-only | Phase 8 must stay above reviewed memory, concept graph, and support-selection exports without rewriting them | consult only if Phase 4 or Phase 5 export seams become ambiguous | author the plan, implement code, or pull Phase 8 logic down into memory or graph layers |
| `World & Conversation Pod Lead` | `gpt-5.3-codex` | active | later execution owner for Phase 8 and default build pod | provide planning consultation on runtime decomposition, scientific-prior usage, current-world honesty routing, visible reasoning outputs, and hard stops below Phase 9 and Phase 10 | author canonical plan truth alone, implement Phase 8 code in this run, absorb Phase 9 or Phase 10 scope, or approve the phase |
| `Meta & Growth Pod Lead` | `gpt-5.3-codex` | inactive | danger-zone work is unrelated to Phase 8 planning and would blur Phase 10 and 11 boundaries | none | activate casually or leak self-improvement behavior into Phase 8 |
| `Product & Sandbox Pod Lead` | `gpt-5.3-codex` | consult-only | Phase 8 may later need narrow runner, demo-shell, or export-format clarification | consult only if runtime-shell or bundle-output seams become ambiguous | author the plan, implement Phase 13 or 14 work, or broaden product scope |
| `Test & Replay Lead` | `gpt-5.4 mini` | active | science/world-awareness truthfulness and boundedness must be test-planned from the start | define verifier family, evidence expectations, closure checks, demo checks, and failure signatures | implement runtime behavior, fake reports, or approve the phase |
| `Anti-Shortcut Auditor` | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | Phase 8 has high risk of fake causal reasoning, live-fact bluffing, and summary theater | detect silent omission, greenfield recreation, prose-only causal chains, fake visible reasoning, and unverifiable world-facing claims | author canonical plan content, downgrade blockers, or approve the phase |
| `Merge Arbiter` | `gpt-5.3-codex` | inactive | planning-only run | none unless later execution integration is needed | author planning content or imply closure |
| `Validation Agent` | `gpt-5.4` | active | final machine-side review of the plan package is required before user review | validate the Phase 8 planning package and later prepare the review request | author plan content, implement code, or approve the phase |
| `Release & Evidence Lead` | `gpt-5.4 mini` | active | later demos must be inspectable, runnable, and bounded | define evidence grouping, demo bundle shape, and review packet surfaces only | perform release execution, public-claim packaging, or imply acceptance |

Author, audit, and validation remain separate identities even when model tiers overlap.

## 6. Reuse and provenance strategy

Only the frozen four disposition categories are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance artifact justification |
| --- | --- | --- | --- | --- |
| scientific priors | `agif_phase8c_governed_structural_growth/contracts.py` `ScientificPriorCell` plus the bounded seed-prior material in `runtime.py`; Phase 1 component catalog entries for `ScientificPriorCell` and `theory_fragment` | `port_with_provenance` | the typed prior-cell structure, principle ids, variable lists, causal mechanisms, scope limits, and worked examples are concrete reusable substrate. AGIFCore should port the bounded prior-cell contract and seed-prior framing with provenance, while stripping structural-growth adoption machinery and rebinding to AGIFCore Phase 6 and Phase 7 inputs. | `COMPONENT_CATALOG.md` rows `CC-010` and `CC-021`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-052` and `SIM-061`; `SCIENTIFIC_METHOD.md` |
| entity/request inference | `agif_phase9_real_runtime/question_analyzer.py` and `contracts.py` `UnifiedQuestionAnalysis` lineage, plus the `E1_STEP_LADDER` in `agif_phase8c_governed_structural_growth/runtime.py` | `rebuild_clean` | the donor analyzer has useful messy-question, live-current, and science-cue signals, but it is entangled with later runtime and open support-graph behavior. AGIFCore should rebuild a narrower Phase 8 inference layer against approved Phase 7 intake and interpretation outputs while preserving the donor’s concrete signal vocabulary. | `RUNTIME_REBUILD_MAP.md` row `RRM-003`; `TRACE_CONTRACT.md`; `CONVERSATION_MODEL.md` |
| world-region selection | `agif_phase8c_governed_structural_growth/runtime.py` `REGION_MARKERS`, `SEED_TOPICS`, and Phase 8B curriculum topic-group structure, plus approved Phase 6 target-domain and world-model exports | `rebuild_clean` | the donor region hints are useful substrate but remain heuristic and phase-8C-specific. AGIFCore should rebuild an explicit, typed world-region selector that consumes approved Phase 6 domain and world-model exports rather than carrying over string-marker tables as runtime truth. | `COMPONENT_CATALOG.md` rows `CC-009` and `CC-021`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-052` and `SIM-061`; `SIMULATOR_MODEL.md` |
| causal-chain reasoning | `agif_phase8b_world_awareness/derived_science_runtime.py`, `grounded_fact_runtime.py`, and `agif_phase8c_governed_structural_growth/runtime.py` step ladder and causal-prior usage | `rebuild_clean` | the donor files prove there is a real causal path concept, but most of the runtime today stores only `causal_chain_ref` strings or folds reasoning into runtime-specific answer builders. AGIFCore should rebuild explicit typed causal-chain steps, evidence links, and missing-variable markers against Phase 6 and Phase 7 exports. | `COMPONENT_CATALOG.md` rows `CC-010` and `CC-021`; `TRACE_CONTRACT.md`; `SIMULATOR_MODEL.md` |
| bounded current-world reasoning | `agif_phase8b_world_awareness/grounded_fact_runtime.py` and `derived_science_runtime.py` live-fact fail-closed lanes, plus Phase 7 `live_current_requested` and `search_needed` honesty semantics | `port_with_provenance` | the donor already contains concrete `search_needed`, `unknown`, `abstain`, `live_measurement_required`, and fresh-search guardrails. AGIFCore should port that honesty boundary with provenance, rebind it to approved Phase 7 interpretation outputs and approved local evidence only, and keep external search execution outside Phase 8. | `SCIENTIFIC_METHOD.md`; `FALSIFICATION_THRESHOLDS.md`; `TRACE_CONTRACT.md`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-052` and `SIM-061` |
| visible reasoning summaries | `agif_phase8b_world_awareness/contracts.py` `PublicReasoningSummary`, `PublicReasoningSummaryField`, and governed answer-record fields | `port_with_provenance` | the donor public-summary shape is concrete and already designed to show what is known, inferred, uncertain, and still needs verification. AGIFCore should port that public summary contract with provenance and keep it strictly public-summary-only rather than hidden-thought disclosure. | `TRACE_CONTRACT.md`; `NORTH_STAR_LANGUAGE_TARGET.md`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-052` and `SIM-061` |
| science reflection | Phase 1 `science_reflection` lineage, `agif_phase8b_world_awareness/idle_reflection_runtime.py`, and `agif_phase8c_governed_structural_growth/contracts.py` reflection and surprise records | `rebuild_clean` | donor reflection surfaces exist, but they are entangled with idle reflection, proposal generation, structural growth, and later meta-cognition. AGIFCore should rebuild a much narrower Phase 8 science-reflection layer that records falsifiers, missing variables, and next verification steps without crossing into Phase 10 meta structures or Phase 11 improvement loops. | `COMPONENT_CATALOG.md` row `CC-020`; `SCIENTIFIC_METHOD.md`; `FALSIFICATION_THRESHOLDS.md` |

## 7. Science/world-awareness boundary rules

### What belongs in scientific priors only

- maintain the typed, bounded prior registry for plain-language laws, variables, causal mechanisms, scope limits, failure cases, worked examples, transfer hints, cue terms, and hidden-variable hints
- select which scientific priors are relevant for a reasoning run
- preserve provenance for every selected prior
- no entity parsing, no world-region selection, no causal-chain construction, and no response text

### What belongs in entity/request inference only

- infer the likely entity, entity class, request type, live-current flag, science-topic cues, hidden-variable cues, and ambiguity markers from approved Phase 7 intake and interpretation outputs
- turn a messy question into a bounded, typed request-analysis state
- make uncertainty explicit when multiple entity or request interpretations remain plausible
- no final answer mode, no world-region selection, no causal chain, and no visible reasoning summary

### What belongs in world-region selection only

- choose bounded world-region or context candidates from the inferred request, approved Phase 6 target-domain and world-model exports, and available local context refs
- record why each region candidate is plausible or why no safe region could be chosen
- keep candidate counts bounded and trace-linked
- no current-fact claim, no causal explanation text, and no answer-mode selection

### What belongs in causal-chain reasoning only

- build typed, machine-checkable causal-chain steps from selected priors, region/context candidates, approved Phase 6 evidence, and missing-variable markers
- surface weak links, unsupported jumps, and fail-closed states directly in the chain record
- preserve explicit refs to priors, regions, world-model entities, simulation traces, and usefulness inputs
- no prose-only “because” answer, no answer contract, and no Phase 9 expression logic

### What belongs in bounded current-world reasoning only

- decide whether a question can be answered from bounded local world-awareness support or whether fresher information is required
- emit explicit freshness and honesty outputs such as `live_measurement_required`, `needs_fresh_information`, bounded-local support refs, and fail-closed reason codes
- preserve the distinction between locally bounded world support and truly current outside facts
- no live web call, no external search execution, no silent timestamp laundering, and no exact current-fact claim beyond the bounded local evidence

### What belongs in visible reasoning summaries only

- emit the public reasoning summary fields only:
  - `what_is_known`
  - `what_is_inferred`
  - `uncertainty`
  - `what_would_verify`
- include explicit `principle_refs`, `causal_chain_ref`, `uncertainty_band`, and `live_measurement_required` style outputs as public-facing reasoning metadata
- keep the summary bounded, inspectable, and evidence-linked
- no hidden chain-of-thought dump, no private scratchpad leakage, and no rhetorical polish engine

### What belongs in science reflection only

- record bounded post-reasoning review outputs such as weak-prior choice, missing variable, falsifier, next verification step, and whether uncertainty should be increased
- keep reflection tied to one completed Phase 8 reasoning run
- remain note-like and verification-oriented rather than self-improvement-oriented
- no self-model writing, no strategy journal, no thinker tissue, no theory-fragment storage, and no proposal-adoption loop

### What is explicitly forbidden to leak in from Phase 9 rich-expression behavior

- teaching-quality rewrite engines
- comparison, planning, synthesis, or analogy engines used as the correctness path
- audience-aware explanation optimization
- multi-draft composition loops
- persuasive or stylistic polish systems
- cross-domain composition or concept-composition logic used to hide weak support
- any behavior that makes Phase 8 depend on Phase 9 to explain science or world-facing support honestly

### What is explicitly forbidden to leak in from Phase 10 meta-cognition behavior

- self-model runtime records
- meta-cognition observer logic
- attention redirect loops
- skeptic or counterexample runtime loops
- strategy journal entries
- thinker tissue outputs
- surprise-engine control loops
- theory-fragment creation or integration
- weak-answer diagnosis loops that belong to the later critique phase
- any behavior that makes Phase 8 a hidden Phase 10 preview

### How Phase 8 stays separate from Phase 7 conversation execution except through allowed interfaces

Allowed Phase 7 inputs:

- `RawTextIntakeRecord`
- `agifcore.phase_07.question_interpretation.v1`
- `agifcore.phase_07.support_state_logic.v1`
- `agifcore.phase_07.answer_contract.v1` for validation and demo linkage only

Rules for those inputs:

- they are read-only inputs only
- Phase 8 may use intake and interpretation to infer entity and request shape
- Phase 8 may use support-state outputs to preserve honesty and avoid upgrading weak-support states silently
- Phase 8 may use the Phase 7 answer-contract shape only to align later demo and validation surfaces, not as the source of science truth

Forbidden Phase 7 interactions:

- direct mutation of any Phase 7 runtime state
- generating the final `response_text` inside Phase 8
- choosing `discourse_mode` or replacing the Phase 7 utterance planner
- upgrading `search_needed`, `unknown`, or `abstain` into a stronger answer without new bounded evidence

### How Phase 8 stays separate from Phase 6 world-model/simulator execution except through allowed interfaces

Allowed Phase 6 inputs:

- `agifcore.phase_06.target_domains.v1`
- `agifcore.phase_06.world_model.v1`
- `agifcore.phase_06.candidate_futures.v1`
- `agifcore.phase_06.what_if_simulation.v1`
- `agifcore.phase_06.fault_lanes.v1`
- `agifcore.phase_06.pressure_lanes.v1`
- `agifcore.phase_06.conflict_lanes.v1`
- `agifcore.phase_06.overload_lanes.v1`
- `agifcore.phase_06.instrumentation.v1`
- `agifcore.phase_06.usefulness_scoring.v1`
- associated trace refs, provenance hashes, fail-closed markers, domain ids, and reason codes

Rules for those inputs:

- they are read-only evidence inputs only
- Phase 8 may use them to ground prior selection, world-region selection, causal-chain steps, and current-world honesty boundaries
- Phase 8 may not rerun, mutate, or reinterpret them as raw graph or memory truth

Forbidden Phase 6 interactions:

- direct mutation of any Phase 6 snapshot or runtime state
- rerunning simulation inside visible reasoning summary generation
- storing reasoning-summary text back into Phase 6 packages
- using usefulness or instrumentation outputs as a replacement for explicit causal-chain reasoning

Additional read-only dependency rule:

- Phase 8 may also consume approved Phase 4 reviewed-memory and continuity exports and approved Phase 5 support-selection, concept, provenance, and trust exports only through approved read-only interfaces
- Phase 8 may not directly mutate Phase 4 or Phase 5 stores

## 8. Phase 8 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Phase 8 planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max scientific-prior set size per run | `<= 12` prior cells | stop and reopen prior-selection rules if later execution needs more than `12` priors without explicit re-plan |
| max entity/request inference candidate set size | `<= 16` candidates | stop and tighten inference fan-out if later execution exceeds `16` entity/request candidates |
| max world-region candidate count | `<= 8` candidates | stop and tighten region selection if later execution exceeds `8` candidate regions |
| max causal-chain step count | `<= 10` steps | stop and split or reduce the chain if later execution needs more than `10` causal steps |
| max current-world evidence input set size | `<= 24` inputs | stop and tighten current-world evidence filters if later execution needs more than `24` bounded evidence inputs |
| max visible reasoning summary size | `<= 1200` characters total across the public reasoning summary fields | stop and tighten the summary surface if later execution exceeds `1200` characters |
| max science-reflection record count per run | `<= 6` records | stop and reduce reflection fan-out if later execution produces more than `6` reflection records |
| max Phase 8 evidence and demo bundle size | `<= 96 MiB` | stop and reorganize outputs if the combined evidence and demo bundle exceeds `96 MiB` |

Budget rules:

- these are laptop-profile planning ceilings only
- later execution must measure against them directly
- if any ceiling is exceeded, stop and escalate to `Program Governor` instead of widening silently
- if later execution needs higher ceilings, reopen planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2 to 7 baselines, requirements pack, design pack, admin controls, and direct legacy-source inspection | all later Phase 8 work | section-complete Phase 8 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, and this plan | all later valid Phase 8 work | one planning task card per active role with disjoint scope |
| `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/` | `World & Conversation Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 8 plan, approved Phase 2 to 7 surfaces, provenance package, and trace contract | later Phase 8 runtime delivery | runtime family exists and matches plan |
| `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/` | `World & Conversation Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | same as above plus exact module breakdown from this plan | later Phase 8 runtime delivery | priors, inference, region, causal-chain, current-world, visible-summary, and reflection modules exist |
| `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 8 plan, execution family, validation protocol, and demo protocol | later Phase 8 verification and closeout | verifier family exists and runs |
| `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifier outputs, Phase 8 snapshots, and demo traces | audit, governor verification, validation, and demos | machine-readable evidence bundle is inspectable |
| `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, and validation protocol | user review | demo bundle exists for science explanation and bounded live-fact inspection |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_EXECUTION_START_BRIEF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 8 plan and admin controls | later execution start | execution scope, file families, and no-approval status are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, rerun verifiers, demo bundle, and evidence bundle | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdict request are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| phase control and prerequisite reconciliation | lock phase truth, role activation, task-card scope, and closure chain | `Program Governor` | `Constitution Keeper` | canonical Phase 8 plan and task-card map | Phase 7 is explicitly approved in live phase-truth files | active and consult-only roles are fixed and Phase 8 stays inside scope |
| reuse and provenance mapping | map each Phase 8 subsystem to a donor basis and one allowed disposition | `Source Cartographer` | `Program Governor`, `Constitution Keeper` | reuse table and source-basis notes | Phase 1 provenance package and legacy source files reviewed | every subsystem has source basis, disposition, and rationale |
| scientific-prior and boundary framing | define scientific-prior boundaries, public-summary boundaries, and hard phase leaks | `Architecture & Contract Lead` | `Source Cartographer`, `Constitution Keeper` | boundary rules and future module targets for `scientific_priors.py` and `visible_reasoning_summaries.py` | approved Phase 6 and 7 seams reviewed and reuse map exists | scientific priors and visible reasoning boundaries are explicit, bounded, and trace-linked |
| entity/request inference planning | define inference contracts and request-shape boundaries above Phase 7 and below causal reasoning | `World & Conversation Pod Lead` | `Architecture & Contract Lead`, `Source Cartographer` | future module targets for `entity_request_inference.py` | boundary rules and reuse map are stable | inference is explicit, bounded, and not collapsed into conversation or causal reasoning |
| world-region selection and causal-chain planning | define region/context selection and typed causal-chain construction | `World & Conversation Pod Lead` | `Architecture & Contract Lead`, `Source Cartographer`, `Memory & Graph Pod Lead` consult-only | future module targets for `world_region_selection.py` and `causal_chain_reasoning.py` | inference planning is stable | world-region selection and causal-chain outputs are separate, typed, and verifiable |
| bounded current-world reasoning planning | define freshness honesty, bounded local evidence rules, and fail-closed live-fact handling | `World & Conversation Pod Lead` | `Constitution Keeper`, `Architecture & Contract Lead`, `Product & Sandbox Pod Lead` consult-only | future module target for `bounded_current_world_reasoning.py` | causal-chain planning is stable | current-world reasoning remains bounded, honest, and external-search-free |
| visible reasoning summary and science-reflection planning | define the public reasoning surface and bounded science-reflection outputs | `Architecture & Contract Lead` | `World & Conversation Pod Lead`, `Test & Replay Lead`, `Constitution Keeper` | future module targets for `visible_reasoning_summaries.py` and `science_reflection.py` | current-world reasoning constraints are stable | public reasoning stays inspectable and reflection stays below Phase 10 |
| test, demo, validation, and evidence planning | define verifier family, evidence reports, demo bundle, audit path, and validation path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | test plan, evidence plan, demo plan, and validation surfaces | runtime-family targets and boundaries are stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. `Program Governor` verifies Phase 7 approval truth and opens the Phase 8 task-card set.
2. `Source Cartographer` maps all required Phase 8 subsystems to source basis and one allowed disposition.
3. `Architecture & Contract Lead` drafts scientific-prior boundaries, visible reasoning-summary boundaries, and forbidden Phase 9 and Phase 10 leaks.
4. `World & Conversation Pod Lead` drafts entity/request inference, world-region selection, causal-chain reasoning, bounded current-world reasoning, and science-reflection decomposition after the first-pass reuse map exists.
5. `Constitution Keeper` reviews the first-pass reuse map and boundary rules for no-hidden-model drift, no fake current-world certainty, and no Phase 9 or Phase 10 leakage.
6. If a Phase 2 seam is ambiguous after step 5, `Kernel Pod Lead` is consulted narrowly and remains non-authoring.
7. If a Phase 4 or Phase 5 seam is ambiguous after step 5, `Memory & Graph Pod Lead` is consulted narrowly and remains non-authoring.
8. If a runner, bundle, or output-format seam is ambiguous after step 5, `Product & Sandbox Pod Lead` is consulted narrowly and remains non-authoring.
9. `World & Conversation Pod Lead` locks the future runtime family only after reuse and boundary outputs are stable.
10. `Test & Replay Lead` and `Release & Evidence Lead` define verifier, evidence, and demo families after the runtime-family targets are stable.
11. `Program Governor` consolidates the full Phase 8 plan, budget envelope, artifact matrix, workstreams, task-card set, and closure map.
12. `Anti-Shortcut Auditor` audits the full Phase 8 planning package.
13. `Program Governor` independently verifies the audited planning package by re-reading the cited files directly.
14. `Validation Agent` prepares the later review request only after audit and governor verification exist.
15. User review happens only after the validated planning package exists.

Safe parallelism:

- `Source Cartographer` and `Architecture & Contract Lead` may work in parallel on disjoint planning outputs.
- `World & Conversation Pod Lead` waits for first-pass reuse and boundary outputs before locking runtime-family targets.
- `Test & Replay Lead` and `Release & Evidence Lead` wait for stable runtime-family targets.
- `Merge Arbiter` remains inactive in planning-only work.
- One active build pod remains the default later execution rule, and that pod is `World & Conversation Pod Lead`.

## 12. Detailed task cards

Consult-only roles receive no Phase 8 task card unless separately reopened by `Program Governor`.

### `P8-TC-PG-01`

- task card ID: `P8-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, the Phase 8 plan, task-card map, artifact matrix, budget envelope, and closure chain
- exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-PG-01_PHASE_8_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
  - earlier phase-truth files except to report a prerequisite mismatch
- required reads first:
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 to 7 plans and execution surfaces
  - relevant requirement and design files
  - admin control stack
- step-by-step work method:
  1. verify Phase 7 approval truth
  2. lock active, consult-only, and inactive roles
  3. consolidate reuse, boundary, runtime-family, verifier, and demo outputs
  4. lock future artifact families and closure mapping
- required cross-checks:
  - no Phase 9 planning
  - no Phase 10 planning
  - no live external search execution
  - no approval language
- exit criteria:
  - the plan is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation, closure, or approval
- explicit proof that no approval is implied: this task ends at plan readiness only; Phase 8 remains `open`

### `P8-TC-CK-01`

- task card ID: `P8-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4 mini`
- objective: guard constitution, falsification honesty, and Phase 8 boundary discipline
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-CK-01_PHASE_8_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md`
  - `projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - Phase 8 draft
- step-by-step work method:
  1. check that Phase 8 stays below Phase 9 rich expression and Phase 10 meta-cognition
  2. check that bounded current-world reasoning stays fail-closed and honesty-bound
  3. check that visible reasoning summaries remain public-summary-only rather than hidden-thought theater
  4. report any drift to `Program Governor`
- required cross-checks:
  - no hidden-model loophole
  - no fake live-world certainty
  - no Phase 9 behavior
  - no Phase 10 behavior
  - no approval language
- exit criteria:
  - constitutional objections are resolved or explicitly raised as blockers
- handoff target: `Program Governor`
- anti-drift rule: do not author architecture or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P8-TC-SC-01`

- task card ID: `P8-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- objective: map every major Phase 8 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-SC-01_PHASE_8_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 6 and Phase 7 plans
  - inspected legacy Phase 8B, Phase 8C, and Phase 9 source files
- step-by-step work method:
  1. map scientific priors, entity/request inference, world-region selection, causal-chain reasoning, bounded current-world reasoning, visible reasoning summaries, and science reflection
  2. assign one allowed disposition to each subsystem
  3. flag where v2 remains a strong substrate and where v1 remains research-only lineage rather than runtime donor
  4. pass unresolved seam notes to `Architecture & Contract Lead` and `Program Governor`
- required cross-checks:
  - no fifth disposition
  - no silent omission
  - no treating old packages as earned AGIFCore runtime
- exit criteria:
  - each subsystem has source basis, disposition, and rationale
- handoff target: `Architecture & Contract Lead` then `Program Governor`
- anti-drift rule: do not claim inspected historical code is already valid AGIFCore runtime
- explicit proof that no approval is implied: provenance mapping does not earn the phase

### `P8-TC-ACL-01`

- task card ID: `P8-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 8 boundaries, allowed interfaces, forbidden leaks, and public reasoning-summary scope
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-01_PHASE_8_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- required reads first:
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 6 and Phase 7 plans
  - `Source Cartographer` output
- step-by-step work method:
  1. define what belongs in each Phase 8 subsystem only
  2. define allowed Phase 6 and Phase 7 interfaces
  3. define forbidden Phase 9 and Phase 10 leaks
  4. pass runtime-family implications to `Program Governor` and `World & Conversation Pod Lead`
- required cross-checks:
  - no one mixed reasoning function
  - no final response generation inside Phase 8
  - no direct mutation of Phase 6 or Phase 7 state
  - no chain-of-thought theater disguised as visible reasoning
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `World & Conversation Pod Lead`
- anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, or the team
- explicit proof that no approval is implied: boundary framing is planning truth only

### `P8-TC-WCPL-01`

- task card ID: `P8-TC-WCPL-01`
- role owner: `World & Conversation Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 8 runtime family without crossing into Phase 9 or Phase 10
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-WCPL-01_PHASE_8_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- required reads first:
  - approved Phase 2 to 7 plans and execution surfaces
  - Phase 8 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
- step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/`
  2. keep the module set explicit: `contracts.py`, `scientific_priors.py`, `entity_request_inference.py`, `world_region_selection.py`, `causal_chain_reasoning.py`, `bounded_current_world_reasoning.py`, `visible_reasoning_summaries.py`, `science_reflection.py`, `science_world_turn.py`
  3. order module implementation so contracts and scientific priors come first, then entity/request inference, then world-region selection, then causal-chain reasoning, then bounded current-world reasoning, then visible reasoning summaries, then science reflection, and the thin coordinator last
  4. identify where Phase 4, Phase 5, Phase 6, and Phase 7 exports must be consumed read-only
- required cross-checks:
  - no runtime code written now
  - no Phase 9 rich-expression behavior
  - no Phase 10 meta-cognition behavior
  - no live search execution
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase

### `P8-TC-TRL-01`

- task card ID: `P8-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4 mini`
- objective: define the Phase 8 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-TRL-01_PHASE_8_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 6 and Phase 7 verifier families and evidence bundles
  - Phase 8 draft
- step-by-step work method:
  1. define one verifier per major Phase 8 subsystem group
  2. define evidence reports and manifest contents
  3. define budget-bound, anti-bluff, anti-theater, and anti-live-fact-guessing checks
  4. define failure signatures for each closure requirement
- required cross-checks:
  - tests must verify separation between priors, inference, region selection, causal chains, current-world reasoning, visible summaries, and reflection
  - causal-chain outputs must be machine-checkable
  - bounded current-world reasoning must enforce freshness honesty
  - visible reasoning summaries must stay public-summary-only
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P8-TC-ASA-01`

- task card ID: `P8-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- objective: audit the Phase 8 planning package for fake completeness, greenfield recreation, and fake-science risk
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ASA-01_PHASE_8_PLAN_AUDIT.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- required reads first:
  - full Phase 8 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `Test & Replay Lead` evidence-plan output
  - relevant approved Phase 6 and Phase 7 plans
- step-by-step work method:
  1. check that all required sections exist
  2. check that each major subsystem has a source basis and disposition
  3. check that no one mixed reasoning function or prose-only causal chain is being passed off as design
  4. check that no approval or completion claim is implied
- required cross-checks:
  - no blind rewrite where a plausible substrate exists
  - no silent omission of bounded current-world reasoning, visible reasoning summaries, or science reflection
  - no Phase 9 or Phase 10 behavior smuggled in
  - no empty report path or unverifiable demo plan
- exit criteria:
  - all blockers are either cleared or explicitly raised
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P8-TC-VA-01`

- task card ID: `P8-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 8 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-VA-01_PHASE_8_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- required reads first:
  - full Phase 8 draft
  - audit output
  - governor verification output
  - validation protocol
- step-by-step work method:
  1. confirm the plan is decision-complete
  2. confirm every required closure requirement has a later artifact path
  3. confirm the user-review demos are inspectable and truthful
  4. prepare the later review request only after audit and governor verification exist
- required cross-checks:
  - no author and validator role collision
  - no missing review surface
  - no implied approval
- exit criteria:
  - review request scope is exact and inspectable
- handoff target: `Program Governor`
- anti-drift rule: do not author plan content or runtime behavior
- explicit proof that no approval is implied: validation asks for review and does not mark the phase earned

### `P8-TC-REL-01`

- task card ID: `P8-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4 mini`
- objective: define the later Phase 8 demo-bundle shape and review packet surfaces
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-REL-01_PHASE_8_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 9 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 6 and Phase 7 demo bundles
  - `Test & Replay Lead` verifier and evidence plan
  - Phase 8 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the science explanation demo surface
  3. define the bounded live-fact demo surface
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
| scientific priors exist | `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/scientific_priors.py`, `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/verify_phase_08_scientific_priors.py`, `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_scientific_priors_report.json` | `World & Conversation Pod Lead` | verifier confirms typed prior cells, scope limits, failure cases, and provenance-linked selection | one flat keyword list or undocumented heuristics with no typed prior contract |
| entity/request inference exists | `entity_request_inference.py`, `verify_phase_08_entity_request_inference.py`, `phase_08_entity_request_inference_report.json` | `World & Conversation Pod Lead` | verifier confirms typed entity/request candidates, live-current flags, and hidden-variable cues | copied Phase 7 interpretation with no distinct entity/request inference structure |
| world-region selection exists | `world_region_selection.py`, `verify_phase_08_world_region_selection.py`, `phase_08_world_region_selection_report.json` | `World & Conversation Pod Lead` | verifier confirms bounded candidate regions, reason codes, and trace-linked selection | always one default region or ad hoc strings with no candidate set |
| causal-chain reasoning exists | `causal_chain_reasoning.py`, `verify_phase_08_causal_chain_reasoning.py`, `phase_08_causal_chain_reasoning_report.json` | `World & Conversation Pod Lead` | verifier confirms typed causal-chain steps, evidence refs, missing-variable markers, and fail-closed behavior | causal reasoning exists only as prose or `causal_chain_ref` labels with no step records |
| bounded current-world reasoning exists | `bounded_current_world_reasoning.py`, `verify_phase_08_bounded_current_world_reasoning.py`, `phase_08_bounded_current_world_reasoning_report.json` | `World & Conversation Pod Lead` | verifier confirms freshness boundaries, `live_measurement_required` behavior, and no search execution | exact current answers are emitted without freshness guards or external execution is hidden inside Phase 8 |
| visible reasoning summaries exist | `visible_reasoning_summaries.py`, `verify_phase_08_visible_reasoning_summaries.py`, `phase_08_visible_reasoning_summaries_report.json` | `World & Conversation Pod Lead` | verifier confirms public reasoning summary fields, bounded size, evidence refs, and no hidden-thought leakage | summary is an unstructured monologue, chain-of-thought dump, or unsupported filler |
| science reflection exists | `science_reflection.py`, `verify_phase_08_science_reflection.py`, `phase_08_science_reflection_report.json` | `World & Conversation Pod Lead` | verifier confirms falsifier, missing-variable, and next-verification outputs tied to one reasoning run | reflection exists only as labels or comments with no bounded effect on uncertainty or verification |
| demo path exists | `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_demo_index.md`, `phase_08_science_explanation_demo.md`, `phase_08_bounded_live_fact_demo.md` plus matching `.json` demo outputs | `Release & Evidence Lead` | direct demo-bundle inspection and rerunnable demo scripts | no inspectable demo or demo claims unsupported by evidence |
| tests/evidence path exists | verifier family under `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/` and evidence manifest `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_evidence_manifest.json` | `Test & Replay Lead` | governor rerun plus validation request | missing verifier coverage, missing manifest, or non-machine-readable evidence |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| science explanation demo | scientific priors, entity/request inference, world-region selection, causal-chain reasoning, visible reasoning summaries, science reflection, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `World & Conversation Pod Lead` | `Anti-Shortcut Auditor` | the original prompt, inferred entity/request shape, selected priors, selected region/context, typed causal chain, public reasoning summary fields, reflection note, and the backing evidence reports |
| bounded live-fact demo | entity/request inference, world-region selection when applicable, bounded current-world reasoning, visible reasoning summaries, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `World & Conversation Pod Lead` | `Anti-Shortcut Auditor` | the live-current cue detection, bounded local evidence set, freshness boundary, `live_measurement_required` or equivalent honesty output, public reasoning summary, and proof that no unsupported exact current answer was emitted |

Validation rules for both demos:

- `Validation Agent` prepares the review request only after audit and governor verification exist.
- `Program Governor` is the only role that asks the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable science/world-awareness substrate | compare subsystem plan and later runtime against mapped v2 Phase 8B, v2 Phase 8C, and v2 Phase 9 donor files | `Source Cartographer` | any subsystem is rebuilt from zero despite a clear typed donor basis | stop and reopen reuse mapping before execution proceeds |
| one giant reasoning function pretending to do priors, inference, causal chains, and reflection | boundary-rule audit and verifier-plan audit | `Architecture & Contract Lead` | any plan or later code collapses priors, inference, region selection, causal chains, current-world reasoning, and reflection into one unverifiable unit | reject the design and split the layers before continuing |
| causal-chain reasoning existing only as prose | causal-chain verifier design and later rerun | `World & Conversation Pod Lead` | no typed step records or evidence refs can be verified | block closure until real causal-chain records exist |
| bounded current-world reasoning bypassing the honesty boundary | live-fact verifier design and demo rerun | `Constitution Keeper` | exact current-fact output appears without a freshness gate or external execution is hidden inside Phase 8 | stop and force fail-closed current-world rules |
| visible reasoning summaries becoming fake chain-of-thought theater | summary verifier design and demo audit | `Constitution Keeper` | the summary exposes opaque hidden-thought text or no evidence-linked public fields exist | stop and reduce the surface to bounded public summary fields only |
| science reflection existing only as labels with no effect | science-reflection verifier design and evidence audit | `World & Conversation Pod Lead` | a reflection record can be produced without a falsifier, missing-variable note, or next verification step | stop and require effect-bound science-reflection rules |
| Phase 8 accidentally absorbing Phase 9 rich-expression behavior | boundary audit against forbidden Phase 9 list | `Constitution Keeper` | teaching, analogy, synthesis, style optimization, or multi-draft composition appears in Phase 8 | stop and remove the rich-expression dependency |
| Phase 8 accidentally absorbing Phase 10 meta-cognition behavior | boundary audit against forbidden Phase 10 list | `Constitution Keeper` | self-model, skeptic, strategy journal, thinker tissue, theory fragments, or weak-answer diagnosis loops appear in Phase 8 | stop and remove the meta-cognition dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 8 plan artifacts
- after user approval, any future change to the Phase 8 plan requires explicit reopen instruction and a supersession note
- `Merge Arbiter` remains inactive in this planning-only work and may not be activated to imply closure

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 7 is explicitly `approved` in the current phase-truth files and in the closeout records reviewed directly.
- Phase 8 remains `open`.
- The required Phase 1 provenance package, approved Phase 2 to 7 baselines, requirement pack, design pack, admin controls, and legacy science/world-awareness source candidates were all reviewed directly.
- No prerequisite blocker was found.
- Defaults locked by this draft:
  - later execution keeps one active build pod by default: `World & Conversation Pod Lead`
  - v2 Phase 8B world-awareness contracts and Phase 8C scientific-prior contracts are the main bounded reuse substrate, but they must be rebound to AGIFCore Phase 6 and Phase 7 interfaces and re-verified inside AGIFCore
  - scientific priors, bounded current-world reasoning, and visible reasoning summaries default toward `port_with_provenance`
  - entity/request inference, world-region selection, causal-chain reasoning, and science reflection default toward `rebuild_clean`
  - Phase 8 remains a read-only science/world-awareness layer above approved simulator and conversation exports and below Phase 9 and Phase 10 behavior
