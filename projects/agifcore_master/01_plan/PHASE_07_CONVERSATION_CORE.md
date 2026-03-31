# Phase 7: Conversation Core

## 1. Phase identity

- Phase number: `7`
- Canonical phase name: `Conversation Core`
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
  - approved Phase 2, 3, 4, 5, and 6 execution, testing, and output surfaces under:
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
  - admin control files:
    - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
    - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
    - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
    - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
    - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`
  - direct inherited-source inspection:
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_7a_north_star/agif_phase7a_e0_interpreter/interpreter.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_7a_north_star/agif_phase7a_e1_support_state/support_state.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_7_conversation/agif_phase7_conversation/contracts.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_7_conversation/agif_phase7_conversation/conversation.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_8b_world_awareness/agif_phase8b_world_awareness/answer_contract.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/contracts.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/question_analyzer.py`
    - `agif_fabric_v2/projects/agif_v2_master/04_execution/phase_9_real_runtime/agif_phase9_real_runtime/answer_composer.py`
    - `agif_fabric_v2/projects/agif_v2_master/05_testing/phase_9_real_runtime/verify_phase9_open_question_reasoning.py`
    - `agif-tasklet-cell/projects/agif_full_product_v1/04_execution/desktop_shell/local_runner_service.py`
    - `agif-tasklet-cell/projects/agif_full_product_v1/04_execution/desktop_shell/trigger_gateway_orchestrator.py`
    - `agif-tasklet-cell/projects/agif_final_review_hardening/02_requirements/ABSTAIN_FIRST_POLICY_CONTRACT.md`

## 2. Phase mission

- Phase 7 exists to define and later build the governed conversation layer that turns approved Phase 4, Phase 5, and Phase 6 evidence into honest user-facing turns.
- Phase 7 must later build:
  - raw text intake
  - question interpretation
  - support-state logic
  - self-knowledge surface
  - clarification
  - utterance planner
  - surface realizer
  - answer contract
  - anti-generic filler guardrails
- Phase 7 must not:
  - implement Phase 8 science or world-awareness behavior
  - implement Phase 9 rich-expression behavior
  - re-implement Phase 2 kernel or workspace control surfaces
  - re-implement Phase 4 memory storage, Phase 5 graph storage, or Phase 6 simulator logic
  - perform live external search execution inside the conversation layer
  - turn language generation into a hidden correctness path
  - treat historical v1, tasklet, or v2 packages as earned AGIFCore completion
  - imply commit, freeze, approval, or closure

## 3. Scope and non-goals

- In-scope artifacts:
  - the canonical Phase 7 plan
  - Phase 7 planning task cards
  - conversation boundary rules
  - reuse and provenance decisions for each major Phase 7 subsystem
  - future execution, testing, output, and handoff targets
  - later demo, validation, and closure planning
- Out-of-scope work:
  - any Phase 7 runtime code
  - any Phase 7 verifier code
  - any Phase 7 evidence generation
  - any Phase 8 planning
  - any Phase 9 planning
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
- Explicit untouched-later-phase statement:
  - Phase 8 and all later phases remain untouched by this plan.

## 4. Phase 6 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 6 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` show Phase 6 `approved` and Phase 7 `open` | Phase 7 planning may proceed |
| Explicit Phase 6 closeout truth exists outside index tables | `pass` | `projects/agifcore_master/DECISIONS.md` and `projects/agifcore_master/CHANGELOG.md` record Phase 6 approval and closeout on `2026-03-31` | no silent approval assumption |
| Required Phase 1 artifacts relied on exist | `pass` | provenance package, trace contract, validation protocol, demo protocol, requirements pack, design pack, and admin controls are present | planning has required governance inputs |
| Required Phase 2 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | session, turn, replay, and trace seams are inspectable |
| Required Phase 3 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | structural cell, tissue, and bundle seams are inspectable |
| Required Phase 4 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | reviewed memory export seams are inspectable |
| Required Phase 5 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | support-selection, provenance, trust, and policy seams are inspectable |
| Required Phase 6 artifacts relied on exist | `pass` | approved plan plus runtime, testing, and output surfaces are present | world-model, simulation, lane, instrumentation, and usefulness seams are inspectable |
| Dependency gap: canonical Phase 7 plan file is not present yet | `non-blocker` | `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md` is the target of this draft | expected planning target, not a prerequisite failure |
| Dependency gap: Phase 7 planning task folder is not present yet | `non-blocker` | no `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/` folder is required yet | expected pre-authoring condition |
| Dependency gap: no AGIFCore Phase 7 runtime, testing, evidence, or demo families exist yet | `non-blocker` | there is no `phase_07_*` execution family yet | expected future execution output, not a planning blocker |
| Blockers vs non-blockers | `planning not blocked` | all prerequisite approvals and source inputs exist | readiness may be `ready_for_user_review` |

## 5. Active team map for Phase 7

Later Phase 7 execution default build pod: `World & Conversation Pod Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | What it must never do this phase |
| --- | --- | --- | --- | --- | --- |
| `Program Governor` | `gpt-5.4` | active | top planning authority and phase-truth control are required | own prerequisite truth, scope lock, active-role map, reuse decisions, workstream order, artifact matrix, closure map, and final plan integration | implement runtime code, self-approve, or broaden into Phase 8 |
| `Constitution Keeper` | `gpt-5.4 mini` | active | Phase 7 can drift into hidden-model behavior, unsupported self-knowledge, or world-awareness leakage | guard constitution, non-negotiables, approval honesty, fail-closed conversation behavior, and phase boundaries | author runtime design alone, approve the phase, or smuggle Phase 8 or Phase 9 behavior into Phase 7 |
| `Source Cartographer` | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | inherited conversation substrate must be mapped before execution is planned | map each Phase 7 subsystem to inherited source basis, disposition, and reuse limits | invent a fifth disposition, treat historical packages as already earned AGIFCore runtime, or approve the phase |
| `Architecture & Contract Lead` | `gpt-5.4` | active | conversation boundaries and answer-contract seams must be explicit before execution | own subsystem boundaries, allowed interfaces, forbidden leaks, and alignment to Phase 2, 4, 5, and 6 contracts | redesign the team, collapse conversation into memory or simulator logic, or approve the phase |
| `Kernel Pod Lead` | `gpt-5.3-codex` | consult-only | Phase 7 should consume Phase 2 session and trace seams without reopening them | consult only if workspace, replay, rollback, trace-export, or session-turn seams become ambiguous | author the plan, implement code, or expand Phase 2 scope |
| `Memory & Graph Pod Lead` | `gpt-5.3-codex` | consult-only | Phase 7 must stay above reviewed memory, support selection, and graph trust surfaces | consult only if Phase 4 or Phase 5 export seams become ambiguous | author the plan, implement code, or pull Phase 7 logic down into memory or graph layers |
| `World & Conversation Pod Lead` | `gpt-5.3-codex` | active | later execution owner for Phase 7 and default build pod | provide planning consultation on runtime decomposition, support-state routing, utterance planning, answer-contract targets, and hard stops below Phase 8 and Phase 9 | author canonical plan truth alone, implement Phase 7 code in this run, absorb Phase 8 or Phase 9 scope, or approve the phase |
| `Meta & Growth Pod Lead` | `gpt-5.3-codex` | inactive | danger-zone work is unrelated to Phase 7 planning | none | activate casually or leak self-modification behavior into Phase 7 |
| `Product & Sandbox Pod Lead` | `gpt-5.3-codex` | consult-only | Phase 7 may later need narrow shell, runner, or export-format clarification | consult only if runtime-shell or bundle-output seams become ambiguous | author the plan, implement Phase 13 or 14 work, or broaden product scope |
| `Test & Replay Lead` | `gpt-5.4 mini` | active | conversation truthfulness must be test-planned from the start | define verifier family, evidence expectations, closure checks, demo checks, and failure signatures | implement runtime behavior, fake reports, or approve the phase |
| `Anti-Shortcut Auditor` | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | Phase 7 has high risk of one-big-function shortcuts and polished bluffing | detect silent omission, greenfield recreation, unsupported self-knowledge, prose-only answer contracts, and unverifiable output claims | author canonical plan content, downgrade blockers, or approve the phase |
| `Merge Arbiter` | `gpt-5.3-codex` | inactive | planning-only run | none unless later execution integration is needed | author planning content or imply closure |
| `Validation Agent` | `gpt-5.4` | active | final machine-side review of the plan package is required before user review | validate the Phase 7 planning package and later prepare the review request | author plan content, implement code, or approve the phase |
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
| raw text intake | `agif_phase7a_e0_interpreter/interpreter.py`, tasklet shell gateway intake surfaces, and Phase 2 turn/session seams | `rebuild_clean` | the historical intake experiments show useful shape, but AGIFCore must rebuild intake around the frozen turn contract, local-only turn handling, and Phase 2 session APIs rather than old graph-matching intake logic | `TRACE_CONTRACT.md`; `COMPONENT_CATALOG.md` conversation shell and turn-record entries; `SOURCE_INHERITANCE_MATRIX.md` tasklet shell and gateway inheritance rows |
| question interpretation | `agif_phase9_real_runtime/question_analyzer.py` and `agif_phase9_real_runtime/contracts.py` `UnifiedQuestionAnalysis` lineage | `rebuild_clean` | the old analyzer has strong messy-question cues and freshness markers, but it is entangled with later rich runtime behavior and must be rebuilt against approved Phase 4, 5, and 6 exports plus the frozen trace fields | `RUNTIME_REBUILD_MAP.md` entry around `question_analyzer.py`; `TRACE_CONTRACT.md`; `CONVERSATION_MODEL.md` |
| support-state logic | `agif_phase7a_e1_support_state/support_state.py`, `agif_phase7_conversation/contracts.py`, and tasklet abstain-first policy surfaces | `port_with_provenance` | support-state routing, knowledge-gap reasons, and next-action logic already align well with AGIFCore fail-closed requirements and the frozen trace contract, so the logic should be ported with provenance after rebinding to AGIFCore inputs | `TRACE_CONTRACT.md`; `COMPONENT_CATALOG.md` conversation-contract items; `SOURCE_INHERITANCE_MATRIX.md` fail-closed UX and gateway rows |
| self-knowledge surface | `agif_phase7_conversation/conversation.py` self-knowledge routes, `agif_phase7a_e1_support_state/support_state.py`, and approved Phase 4 continuity memory exports | `rebuild_clean` | the donor surfaces prove the behavior existed, but historical self-facts cannot be inherited literally; AGIFCore must rebuild this layer so every self-knowledge statement is anchored to continuity memory, replay-safe self-history, and explicit support refs | `TRACE_CONTRACT.md`; `HUMAN_THINKING_TARGET.md`; `MEMORY_MODEL.md` |
| clarification | `agif_phase7a_e1_support_state/support_state.py` clarification routing and `agif_phase7_conversation/contracts.py` request and next-action surfaces | `port_with_provenance` | clarification routing and failure reasons are already concrete substrate and should be ported with provenance, while AGIFCore keeps the behavior bounded, specific, and non-filler | `TRACE_CONTRACT.md`; `CONVERSATION_MODEL.md`; `NON_NEGOTIABLES.md` |
| utterance planner | `agif_phase7_conversation/contracts.py` `ConversationUtterancePlan` lineage and `agif_phase7_conversation/conversation.py` response-act structure | `port_with_provenance` | the historical plan layer is reusable if rebound to AGIFCore support-state and answer-contract fields; it must remain a thin structural planner and must stop before Phase 9 expressive behavior | `COMPONENT_CATALOG.md` conversation turn and contract items; `CONVERSATION_MODEL.md`; `TRACE_CONTRACT.md` |
| surface realizer | `agif_phase7_conversation/conversation.py` final response assembly steps and `agif_phase9_real_runtime/answer_composer.py` heuristics | `rebuild_clean` | the old surface layer mixes later expressive logic and richer style behavior; AGIFCore needs a simpler realizer that is constrained by support-state, utterance plan, and answer contract | `RUNTIME_REBUILD_MAP.md` entry around `answer_composer.py`; `NORTH_STAR_LANGUAGE_TARGET.md`; `NON_NEGOTIABLES.md` |
| answer contract | `agif_phase8b_world_awareness/answer_contract.py`, tasklet public answer envelope and abstain-first policy, and `agif_phase9_real_runtime/contracts.py` `PublicAnswerEnvelope` lineage | `rebuild_clean` | strong donor contract surfaces exist, but the phase 8B answer contract is contaminated by world-awareness fields and cannot be ported directly; AGIFCore must rebuild a Phase 7-native contract around frozen trace fields, support state, and evidence refs | `TRACE_CONTRACT.md`; `COMPONENT_CATALOG.md` conversation-contract items; `SOURCE_INHERITANCE_MATRIX.md` public-envelope and shell inheritance rows |
| anti-generic filler guardrails | `agif_phase9_real_runtime/answer_composer.py` heuristic guards, `verify_phase9_open_question_reasoning.py`, and AGIFCore north-star language rules | `port_with_provenance` | the historical heuristics and regression cases are direct reusable substrate; they should become explicit machine-checkable guardrails over planning and realization instead of remaining informal style advice | `NORTH_STAR_LANGUAGE_TARGET.md`; `NON_NEGOTIABLES.md`; `RUNTIME_REBUILD_MAP.md` answer-composer rebuild notes |

## 7. Conversation boundary rules

### What belongs in raw text intake only

- accept raw user text, Phase 2 session identifiers, turn identifiers, and any approved local attachment or metadata refs exported by the runtime shell
- normalize whitespace, preserve quoting and code-block boundaries, calculate bounded length metrics, and create replay-safe raw text hashes
- emit a read-only intake record that can be traced and replayed
- no question interpretation, no support-state judgment, no clarification wording, and no final response text

### What belongs in question interpretation only

- transform intake records into a structured question representation with request kind, ambiguity markers, freshness markers, self-knowledge markers, requested output shape, and domain cues
- map interpretation output onto frozen turn fields such as `user_intent`, `discourse_mode` candidates, and candidate `knowledge_gap_reason`
- preserve explicit uncertainty markers when the question is messy or under-specified
- no support ranking, no simulator recomputation, no response drafting, and no answer-contract emission

### What belongs in support-state logic only

- combine question interpretation with approved Phase 4 memory-review outputs, approved Phase 5 support-selection outputs, and approved Phase 6 simulation and lane outputs
- produce machine-checkable `support_state`, `knowledge_gap_reason`, `next_action`, and answer-vs-clarify-vs-search-needed routing
- enforce fail-closed behavior when support is weak, conflicting, stale, or policy-blocked
- no self-knowledge phrasing, no clarification wording, no utterance text, and no answer composition

### What belongs in self-knowledge surface only

- convert approved continuity-memory, self-history, and trace-backed local-runtime facts into inspectable self-knowledge statements
- require an evidence ref for every self-knowledge claim
- state limits, capabilities, missing context, or local state only when supported by memory or trace anchors
- no unsupported self-assertion, no emotional narration, no hidden-model claims, and no fabricated “I know” language

### What belongs in clarification only

- generate the smallest necessary clarification question when ambiguity, missing parameters, or blocked local evidence prevents a truthful answer
- tie each clarification request to a specific missing variable or ambiguity reason
- remain bounded to at most two specific questions in one turn
- no generic filler, no teaching detours, no search execution, and no replacement of `abstain` or `search_needed` when clarification cannot resolve the problem

### What belongs in utterance planner only

- choose the response path implied by support-state logic and map it onto a bounded utterance plan
- select or confirm the turn’s `discourse_mode`, response sections, cited evidence refs, and realization constraints
- keep structural intent separate from final wording
- no new facts, no new evidence lookup, no simulator reruns, and no rich-expression styling

### What belongs in surface realizer only

- turn the utterance plan into plain response text that matches the answer contract and respects anti-filler guardrails
- keep wording simple, explicit, and bounded
- preserve abstain, clarify, and search-needed honesty rather than smoothing it away
- no hidden reasoning path, no support-state overrides, no world-awareness behavior, and no ornamental rich-expression logic

### What belongs in answer contract only

- emit the machine-checkable turn envelope for the user-facing answer
- include frozen or directly aligned fields such as `response_text`, `abstain_or_answer`, `support_state`, `knowledge_gap_reason`, `next_action`, `discourse_mode`, `memory_review_ref`, `planner_trace_ref`, `simulation_trace_ref`, `critic_trace_ref`, `governance_trace_ref`, and relevant evidence refs
- bind the final text to the chosen response mode and support classification
- no prose-only summaries, no hidden free-form fields, and no Phase 8 freshness-resolution payloads

### What anti-generic filler guardrails must represent

- explicit machine-checkable rules that detect and block empty framing, generic hedging, unsupported politeness padding, and vague summary text with no evidence anchor
- a bounded violation result with reason codes and fallback action such as `clarify`, `search_needed`, `unknown`, or `abstain`
- regression targets that prove the guardrails constrain actual output behavior
- no soft guidelines only, no style-preference drift, and no unlogged silent rewriting

### What is explicitly forbidden to leak in from Phase 8 science/world-awareness behavior

- scientific priors execution
- falsification or science-reflection loops
- live current-world lookup
- freshness resolution beyond choosing `search_needed` or `needs_fresh_information`
- world-region selection
- live entity discovery from external sources
- world-awareness curriculum logic
- Phase 8 answer-contract fields that require live-world reasoning

### What is explicitly forbidden to leak in from Phase 9 rich-expression behavior

- expressive rewrite or rhetoric engines
- analogy-generation systems as a correctness path
- multi-draft composition loops
- rich support-graph activation or orchestration as a language-generation shortcut
- critique-rewrite pipelines that alter support-state decisions
- public-release style optimization or persuasive polish systems
- any behavior that makes Phase 7 depend on Phase 9 for honest answering

### How Phase 7 stays separate from Phase 6 world-model and simulator logic except through allowed interfaces

Allowed Phase 6 inputs:

- `WorldModelSnapshot`
- `CandidateFutureSnapshot`
- `WhatIfSimulationSnapshot`
- `FaultLaneSnapshot`
- `PressureLaneSnapshot`
- `ConflictLaneSnapshot`
- `OverloadLaneSnapshot`
- `InstrumentationSnapshot`
- `UsefulnessEvaluationSnapshot`
- associated trace refs, provenance hashes, reason codes, and review-safe status markers

Rules for those inputs:

- they are read-only evidence inputs only
- Phase 7 may translate them into support-state and answer-contract decisions
- Phase 7 may not rerun, mutate, or reinterpret them as graph or memory truth

Forbidden Phase 6 interactions:

- direct mutation of any Phase 6 snapshot or runtime state
- rerunning simulation inside realization
- storing response text or clarification text inside Phase 6 packages
- using Phase 6 usefulness or instrumentation outputs as a replacement for support-state logic

### How Phase 7 stays separate from Phase 4 memory and Phase 5 graph logic except through allowed interfaces

Allowed Phase 4 inputs:

- semantic, procedural, working-memory turn anchors, and continuity export state when exported through approved interfaces
- memory-review export outputs and refs
- correction, supersession, rollback, and replay refs
- approved continuity self-history anchors used by self-knowledge surface

Allowed Phase 5 inputs:

- support-selection results and ranked support candidates
- graph export state, provenance bundles, provenance hashes, trust bands, policy requirements, transfer decisions, conflict outputs, and supersession outputs

Forbidden Phase 4 and Phase 5 interactions:

- direct mutation of memory stores or graph stores
- importing raw internal helper state instead of approved exports
- hiding conversation state inside Phase 4 or Phase 5 packages
- promoting language output back into memory or graph truth during Phase 7 runtime

## 8. Phase 7 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Phase 7 planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max raw-input length | `<= 4000` characters | stop and reopen intake rules if later execution accepts turns above `4000` characters without explicit re-plan |
| max parsed-question structure size | `<= 64` normalized signals or fields | stop and tighten interpretation structure if later execution exceeds `64` parsed items per turn |
| max support-state candidate set size | `<= 24` evidence candidates | stop and reduce candidate fan-in if support-state logic needs more than `24` candidate refs |
| max clarification question count per turn | `<= 2` questions | stop and escalate if a turn needs more than `2` clarification questions |
| max utterance-plan branch count | `<= 6` branches | stop and tighten planner branching if later execution produces more than `6` plan branches |
| max response-plan size | `<= 3200` characters of user-facing text | stop and tighten realization scope if response text exceeds `3200` characters without explicit justification |
| max answer-contract field count | `<= 20` top-level fields | stop and simplify the contract if later execution requires more than `20` top-level fields |
| max Phase 7 evidence and demo bundle size | `<= 96 MiB` | stop and reorganize outputs if the combined evidence and demo bundle exceeds `96 MiB` |

Budget rules:

- these are laptop-profile planning ceilings only
- later execution must measure against them directly
- if any ceiling is exceeded, stop and escalate to `Program Governor` instead of widening silently
- if later execution needs higher ceilings, reopen planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2 to 6 baselines, requirements pack, design pack, admin controls, and direct legacy-source inspection | all later Phase 7 work | section-complete Phase 7 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, and this plan | all later valid Phase 7 work | one planning task card per active role with disjoint scope |
| `projects/agifcore_master/04_execution/phase_07_conversation_core/` | `World & Conversation Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 7 plan, approved Phase 2 to 6 surfaces, provenance package, and trace contract | later Phase 7 runtime delivery | runtime family exists and matches plan |
| `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/` | `World & Conversation Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | same as above plus exact module breakdown from this plan | later Phase 7 runtime delivery | intake, interpretation, support-state, self-knowledge, clarification, planner, realizer, contract, and guardrail modules exist |
| `projects/agifcore_master/05_testing/phase_07_conversation_core/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 7 plan, execution family, validation protocol, and demo protocol | later Phase 7 verification and closeout | verifier family exists and runs |
| `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifier outputs, answer-contract outputs, support-state outputs, and demo traces | audit, governor verification, validation, and demos | machine-readable evidence bundle is inspectable |
| `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, validation protocol | user review | demo bundle exists for messy-question, self-knowledge, and honest abstain/search-needed inspection |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_EXECUTION_START_BRIEF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 7 plan and admin controls | later execution start | execution scope, file families, and no-approval status are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, rerun verifiers, demo bundle, and evidence bundle | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdict request are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| phase control and prerequisite reconciliation | lock phase truth, role activation, task-card scope, and closure chain | `Program Governor` | `Constitution Keeper` | canonical Phase 7 plan and task-card map | Phase 6 is explicitly approved in live phase-truth files | active and consult-only roles are fixed and Phase 7 stays inside scope |
| reuse and provenance mapping | map each Phase 7 subsystem to a donor basis and one allowed disposition | `Source Cartographer` | `Program Governor`, `Constitution Keeper` | reuse table and source-basis notes | Phase 1 provenance package and legacy source files reviewed | every subsystem has source basis, disposition, and rationale |
| intake and interpretation planning | define intake and interpretation boundaries, contracts, and runtime-family targets | `Architecture & Contract Lead` | `World & Conversation Pod Lead`, `Source Cartographer` | boundary rules and future module targets for `raw_text_intake.py` and `question_interpretation.py` | approved Phase 2 to 6 seams reviewed and reuse map exists | intake and interpretation are explicit, bounded, and trace-linked |
| support-state and self-knowledge planning | define support-state enforcement, evidence routing, and self-knowledge constraints | `World & Conversation Pod Lead` | `Architecture & Contract Lead`, `Memory & Graph Pod Lead` consult-only | future module targets for `support_state_logic.py` and `self_knowledge_surface.py` | intake and interpretation rules are stable | support-state logic and self-knowledge remain evidence-bound and fail-closed |
| clarification and abstain/search-needed planning | define clarification behavior, abstain behavior, and search-needed routing | `World & Conversation Pod Lead` | `Constitution Keeper`, `Architecture & Contract Lead` | future module targets for `clarification.py` and abstain-search-needed routing inside `support_state_logic.py` | support-state planning is stable | clarification is specific, non-filler, and distinct from abstain and search-needed |
| utterance planning and surface realization planning | define structural planning and truthful response assembly | `World & Conversation Pod Lead` | `Architecture & Contract Lead`, `Source Cartographer` | future module targets for `utterance_planner.py` and `surface_realizer.py` | support-state routing is stable | planner and realizer are separate, bounded, and below Phase 9 |
| answer-contract and anti-filler planning | define the machine-checkable answer envelope and output guardrails | `Architecture & Contract Lead` | `World & Conversation Pod Lead`, `Test & Replay Lead` | future module targets for `answer_contract.py` and `anti_generic_filler.py` | planner and realizer constraints are stable | answer contract and guardrails are explicit enough to verify later |
| test, demo, validation, and evidence planning | define verifier family, evidence reports, demo bundle, audit path, and validation path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | test plan, evidence plan, demo plan, and validation surfaces | runtime-family targets and boundaries are stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. `Program Governor` verifies Phase 6 approval truth and opens the Phase 7 task-card set.
2. `Source Cartographer` maps all required Phase 7 subsystems to source basis and one allowed disposition.
3. `Architecture & Contract Lead` drafts intake, interpretation, answer-contract, and anti-filler boundaries.
4. `World & Conversation Pod Lead` drafts support-state, self-knowledge, clarification, planner, and realizer decomposition after the first-pass reuse map exists.
5. `Constitution Keeper` reviews the first-pass reuse map and boundary rules for no-hidden-model drift, no unsupported self-knowledge, and no Phase 8 or Phase 9 leakage.
6. If a Phase 2 seam is ambiguous after step 5, `Kernel Pod Lead` is consulted narrowly and remains non-authoring.
7. If a Phase 4 or Phase 5 seam is ambiguous after step 5, `Memory & Graph Pod Lead` is consulted narrowly and remains non-authoring.
8. If a runner, bundle, or output-format seam is ambiguous after step 5, `Product & Sandbox Pod Lead` is consulted narrowly and remains non-authoring.
9. `World & Conversation Pod Lead` locks the future runtime family only after reuse and boundary outputs are stable.
10. `Test & Replay Lead` and `Release & Evidence Lead` define verifier, evidence, and demo families after the runtime-family targets are stable.
11. `Program Governor` consolidates the full Phase 7 plan, budget envelope, artifact matrix, workstreams, task-card set, and closure map.
12. `Anti-Shortcut Auditor` audits the full Phase 7 planning package.
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

Consult-only roles receive no Phase 7 task card unless separately reopened by `Program Governor`.

### `P7-TC-PG-01`

- task card ID: `P7-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, the Phase 7 plan, task-card map, artifact matrix, budget envelope, and closure chain
- exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-PG-01_PHASE_7_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 8 and later artifacts
  - earlier phase-truth files except to report a prerequisite mismatch
- required reads first:
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 to 6 plans and execution surfaces
  - relevant requirement and design files
  - admin control stack
- step-by-step work method:
  1. verify Phase 6 approval truth
  2. lock active, consult-only, and inactive roles
  3. consolidate reuse, boundary, runtime-family, verifier, and demo outputs
  4. lock future artifact families and closure mapping
- required cross-checks:
  - no Phase 8 planning
  - no Phase 9 planning
  - no live external search execution
  - no approval language
- exit criteria:
  - the plan is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation, closure, or approval
- explicit proof that no approval is implied: this task ends at plan readiness only; Phase 7 remains `open`

### `P7-TC-CK-01`

- task card ID: `P7-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4 mini`
- objective: guard constitution, fail-closed conversation behavior, and Phase 7 boundary discipline
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-CK-01_PHASE_7_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 8 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/PHASE_APPROVAL_RULES.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - Phase 7 draft
- step-by-step work method:
  1. check that Phase 7 stays below science/world-awareness and rich-expression behavior
  2. check that self-knowledge stays evidence-bound
  3. check that clarification and abstain behavior remain fail-closed and non-generic
  4. report any drift to `Program Governor`
- required cross-checks:
  - no hidden-model loophole
  - no unsupported self-assertion
  - no Phase 8 behavior
  - no Phase 9 behavior
  - no approval language
- exit criteria:
  - constitutional objections are resolved or explicitly raised as blockers
- handoff target: `Program Governor`
- anti-drift rule: do not author architecture or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P7-TC-SC-01`

- task card ID: `P7-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- objective: map every major Phase 7 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-SC-01_PHASE_7_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 8 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 4, 5, and 6 plans
  - inspected legacy conversation, answer-contract, and tasklet source files
- step-by-step work method:
  1. map intake, interpretation, support-state, self-knowledge, clarification, planner, realizer, contract, and anti-filler subsystems
  2. assign one allowed disposition to each
  3. flag where v2 remains a strong substrate and where tasklet remains only envelope provenance
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

### `P7-TC-ACL-01`

- task card ID: `P7-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 7 boundaries, allowed interfaces, forbidden leaks, and answer-contract scope
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-ACL-01_PHASE_7_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 8 and later artifacts
- required reads first:
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 2 to 6 plans
  - `Source Cartographer` output
- step-by-step work method:
  1. define what belongs in each Phase 7 subsystem only
  2. define allowed Phase 4, Phase 5, and Phase 6 interfaces
  3. define forbidden Phase 8 and Phase 9 leaks
  4. pass runtime-family implications to `Program Governor` and `World & Conversation Pod Lead`
- required cross-checks:
  - no one mixed conversation function
  - no unsupported self-knowledge
  - no user-facing language behavior inside support-state logic
  - no direct mutation of memory, graph, or simulator state
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `World & Conversation Pod Lead`
- anti-drift rule: do not redesign kernel, memory, graph, simulator, or the team
- explicit proof that no approval is implied: boundary framing is planning truth only

### `P7-TC-WCPL-01`

- task card ID: `P7-TC-WCPL-01`
- role owner: `World & Conversation Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 7 runtime family without crossing into Phase 8 or Phase 9
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-WCPL-01_PHASE_7_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 8 and later artifacts
- required reads first:
  - approved Phase 2 to 6 plans and execution surfaces
  - Phase 7 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
- step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/`
  2. keep the module set explicit: `contracts.py`, `raw_text_intake.py`, `question_interpretation.py`, `support_state_logic.py`, `self_knowledge_surface.py`, `clarification.py`, `utterance_planner.py`, `surface_realizer.py`, `answer_contract.py`, `anti_generic_filler.py`, `conversation_turn.py`
  3. order module implementation so intake comes before interpretation, interpretation before support-state, support-state before clarification and self-knowledge, then planner, realizer, contract, and guardrails
  4. identify where Phase 4, Phase 5, and Phase 6 exports must be consumed read-only
- required cross-checks:
  - no runtime code written now
  - no Phase 8 world-awareness behavior
  - no Phase 9 rich-expression behavior
  - no live search execution
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase

### `P7-TC-TRL-01`

- task card ID: `P7-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4 mini`
- objective: define the Phase 7 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-TRL-01_PHASE_7_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 8 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 2 to 6 verifier families and evidence bundles
  - Phase 7 draft
- step-by-step work method:
  1. define one verifier per major Phase 7 subsystem group
  2. define evidence reports and manifest contents
  3. define budget-bound, anti-bluff, and anti-filler checks
  4. define failure signatures for each closure requirement
- required cross-checks:
  - tests must verify separation between intake, interpretation, support-state, planning, and realization
  - self-knowledge must require continuity or trace anchors
  - answer contract must be machine-checkable
  - anti-filler guardrails must constrain actual output
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P7-TC-ASA-01`

- task card ID: `P7-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- objective: audit the Phase 7 planning package for fake completeness, greenfield recreation, and polished bluffing risk
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-ASA-01_PHASE_7_PLAN_AUDIT.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 8 and later artifacts
- required reads first:
  - full Phase 7 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `Test & Replay Lead` evidence-plan output
  - relevant approved Phase 2 to 6 plans
- step-by-step work method:
  1. check that all required sections exist
  2. check that each major subsystem has a source basis and disposition
  3. check that no one mixed conversation function or prose-only contract is being passed off as design
  4. check that no approval or completion claim is implied
- required cross-checks:
  - no blind rewrite where a plausible substrate exists
  - no silent omission of self-knowledge, answer contract, or anti-filler guardrails
  - no Phase 8 or Phase 9 behavior smuggled in
  - no empty report path or unverifiable demo plan
- exit criteria:
  - all blockers are either cleared or explicitly raised
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P7-TC-VA-01`

- task card ID: `P7-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 7 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-VA-01_PHASE_7_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 8 and later artifacts
- required reads first:
  - full Phase 7 draft
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

### `P7-TC-REL-01`

- task card ID: `P7-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4 mini`
- objective: define the later Phase 7 demo-bundle shape and review packet surfaces
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-REL-01_PHASE_7_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 8 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 2 to 6 demo bundles
  - `Test & Replay Lead` verifier and evidence plan
  - Phase 7 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the messy-question demo surface
  3. define the self-knowledge demo surface
  4. define the honest abstain and search-needed demo surface
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
| raw text intake exists | `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/raw_text_intake.py`, `projects/agifcore_master/05_testing/phase_07_conversation_core/verify_phase_07_raw_text_intake.py`, `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_evidence/phase_07_raw_text_intake_report.json` | `World & Conversation Pod Lead` | verifier confirms replay-safe intake record, raw-text hash, length bounds, and no interpretation leakage | intake is merged into interpretation or outputs only raw strings with no trace-safe record |
| question interpretation exists | `question_interpretation.py`, `verify_phase_07_question_interpretation.py`, `phase_07_question_interpretation_report.json` | `World & Conversation Pod Lead` | verifier confirms structured question representation, ambiguity markers, and freshness/self-knowledge cues | interpretation is just prose notes or directly returns final answer text |
| support-state logic exists | `support_state_logic.py`, `verify_phase_07_support_state_logic.py`, `phase_07_support_state_logic_report.json` | `World & Conversation Pod Lead` | verifier confirms `support_state`, `knowledge_gap_reason`, `next_action`, evidence refs, and fail-closed routing | support-state is a label with no enforcement meaning or no evidence linkage |
| self-knowledge surface exists | `self_knowledge_surface.py`, `verify_phase_07_self_knowledge_surface.py`, `phase_07_self_knowledge_surface_report.json` | `World & Conversation Pod Lead` | verifier confirms every self-knowledge statement has continuity or trace anchors | self-knowledge makes unsupported claims about capability, memory, or local state |
| clarification exists | `clarification.py`, `verify_phase_07_clarification.py`, `phase_07_clarification_report.json` | `World & Conversation Pod Lead` | verifier confirms specific missing-variable questions, bounded count, and no filler | clarification is generic padding or appears when an answer should have been given directly |
| utterance planner exists | `utterance_planner.py`, `verify_phase_07_utterance_planner_and_surface_realizer.py`, `phase_07_utterance_planner_and_surface_realizer_report.json` | `World & Conversation Pod Lead` | verifier confirms bounded plan branches, discourse-mode choice, and section structure | planner is missing or collapsed into final text generation |
| surface realizer exists | `surface_realizer.py`, `verify_phase_07_utterance_planner_and_surface_realizer.py`, `phase_07_utterance_planner_and_surface_realizer_report.json` | `World & Conversation Pod Lead` | verifier confirms final text matches plan, support-state, and answer contract | realized answer contradicts contract, hides abstain, or invents unsupported facts |
| answer contract exists | `answer_contract.py`, `verify_phase_07_answer_contract.py`, `phase_07_answer_contract_report.json` | `World & Conversation Pod Lead` | verifier confirms machine-checkable fields, trace refs, and alignment with response text | contract exists only as prose or disagrees with the emitted response |
| anti-generic filler guardrails exist | `anti_generic_filler.py`, `verify_phase_07_anti_generic_filler.py`, `phase_07_anti_generic_filler_report.json` | `World & Conversation Pod Lead` | verifier confirms guardrail violations are detected and constrain output behavior | filler rules are advisory only and do not change any output decision |
| demo path exists | `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_demo_bundle/phase_07_demo_index.md`, `phase_07_messy_question_demo.md`, `phase_07_self_knowledge_demo.md`, `phase_07_honest_abstain_search_needed_demo.md` plus matching `.json` demo outputs | `Release & Evidence Lead` | direct demo-bundle inspection and rerunnable demo scripts | no inspectable demo or demo claims unsupported by evidence |
| tests and evidence path exists | verifier family under `projects/agifcore_master/05_testing/phase_07_conversation_core/` and evidence manifest `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_evidence/phase_07_evidence_manifest.json` | `Test & Replay Lead` | governor rerun plus validation request | missing verifier coverage, missing manifest, or non-machine-readable evidence |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| messy-question live demo | raw text intake, question interpretation, support-state logic, clarification path, utterance planner, surface realizer, answer contract, anti-filler guardrails, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `World & Conversation Pod Lead` | `Anti-Shortcut Auditor` | the original messy prompt, intake record, interpreted structure, chosen support state, clarification or answer decision, answer contract, realized text, and guardrail result |
| self-knowledge demo | support-state logic, self-knowledge surface, continuity-memory anchors, utterance planner, surface realizer, answer contract, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `World & Conversation Pod Lead` | `Anti-Shortcut Auditor` | the continuity or self-history anchors, exact self-knowledge statements, contract fields, realized text, and proof that unsupported claims were blocked |
| honest abstain and search-needed demo | question interpretation, support-state logic, clarification or abstain routing, answer contract, anti-filler guardrails, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `World & Conversation Pod Lead` | `Anti-Shortcut Auditor` | the evidence gap or freshness gap, chosen `support_state`, `knowledge_gap_reason`, `next_action`, abstain or search-needed text, and proof that no unsupported grounded answer was emitted |

Validation rules for all three demos:

- `Validation Agent` prepares the review request only after audit and governor verification exist.
- `Program Governor` is the only role that asks the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable conversation substrate | compare subsystem plan and later runtime against mapped v2 and tasklet sources | `Source Cartographer` | any subsystem is rebuilt from zero despite a clear typed donor basis | stop and reopen reuse mapping before execution proceeds |
| one giant conversation function pretending to be intake, support-state, planning, and realization | boundary-rule audit and verifier-plan audit | `Architecture & Contract Lead` | any plan or later code collapses intake, interpretation, support-state, planner, and realizer into one unverifiable unit | reject the design and split the layers before continuing |
| support-state logic existing only as labels with no enforcement meaning | support-state verifier design and later rerun | `World & Conversation Pod Lead` | a support-state can be set without changing next action, answer mode, or contract behavior | block closure until support-state drives real routing |
| self-knowledge becoming unsupported self-assertion | self-knowledge verifier design and continuity-anchor audit | `Constitution Keeper` | any self-knowledge statement lacks continuity or trace refs | stop and force evidence-bound self-knowledge rules |
| clarification becoming generic filler | clarification verifier design and anti-filler audit | `World & Conversation Pod Lead` | clarification text does not identify a concrete missing variable or is used where direct answer should occur | block closure until clarification is specific and bounded |
| answer contract existing only as prose | answer-contract verifier design and evidence audit | `Test & Replay Lead` | no machine-checkable contract file or response-to-contract alignment can be verified | stop and force a typed answer-contract surface |
| anti-generic filler guardrails not actually constraining output | anti-filler verifier design and regression reruns | `Test & Replay Lead` | generic filler is detected in demos but does not alter planner or realization output | stop and require guardrail-enforced fallback behavior |
| Phase 7 accidentally absorbing Phase 8 science and world-awareness behavior | boundary audit against forbidden Phase 8 list | `Constitution Keeper` | scientific priors, live lookup, or freshness-resolution behavior appears in Phase 7 | stop and remove the science or world-awareness dependency |
| Phase 7 accidentally absorbing Phase 9 rich-expression behavior | boundary audit against forbidden Phase 9 list | `Constitution Keeper` | expressive rewrite, multi-draft composition, or rhetorical generation appears in Phase 7 | stop and remove the rich-expression dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 7 plan artifacts
- after user approval, any future change to the Phase 7 plan requires explicit reopen instruction and a supersession note
- `Merge Arbiter` remains inactive in this planning-only work and may not be activated to imply closure

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 6 is explicitly `approved` in the current phase-truth files and in the closeout records reviewed directly.
- Phase 7 remains `open`.
- The required Phase 1 provenance package, approved Phase 2 to 6 baselines, requirement pack, design pack, admin controls, and legacy conversation-source candidates were all reviewed directly.
- No prerequisite blocker was found.
- Defaults locked by this draft:
  - later execution keeps one active build pod by default: `World & Conversation Pod Lead`
  - v2 Phase 7 and 7A are the main bounded conversation substrate, with tasklet shell and abstain-first surfaces used as envelope and fail-closed provenance rather than main cognition substrate
  - support-state logic, clarification, utterance planner, and anti-generic filler guardrails default toward `port_with_provenance`
  - raw text intake, question interpretation, self-knowledge surface, surface realizer, and answer contract default toward `rebuild_clean`
  - Phase 7 remains a read-only conversation layer above approved memory, graph, and simulator exports and below Phase 8 and Phase 9 behavior
