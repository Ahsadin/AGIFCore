# Phase 10: Meta-Cognition and Critique

Brief summary:

Phase 10 plans the bounded meta-cognition and critique layer that sits above approved Phase 7 conversation, Phase 8 science/world-awareness, and Phase 9 rich-expression outputs. It must produce inspectable self-model, critique, surprise, contradiction, and weak-answer diagnosis surfaces without leaking into Phase 11 self-improvement or Phase 12 structural growth.

Planned interface additions for later execution:

- a new runtime family under `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/`
- a thin coordinator snapshot `agifcore.phase_10.meta_cognition_turn.v1`
- per-subsystem schemas:
  - `agifcore.phase_10.self_model.v1`
  - `agifcore.phase_10.meta_cognition_layer.v1`
  - `agifcore.phase_10.attention_redirect.v1`
  - `agifcore.phase_10.meta_cognition_observer.v1`
  - `agifcore.phase_10.skeptic_counterexample.v1`
  - `agifcore.phase_10.strategy_journal.v1`
  - `agifcore.phase_10.thinker_tissue.v1`
  - `agifcore.phase_10.surprise_engine.v1`
  - `agifcore.phase_10.theory_fragments.v1`
  - `agifcore.phase_10.weak_answer_diagnosis.v1`

Planning defaults chosen:

- later execution keeps one active build pod by default: `Meta & Growth Pod Lead`
- later execution must include one extra audit pass and stronger Governor review because the active build pod is the Meta & Growth pod
- no additional human checkpoint is planned by default because Phase 10 must not land self-improvement, self-initiated inquiry, or structural-growth behavior at all; if any such behavior appears, execution stops as boundary drift instead of folding it into Phase 10
- planning-support task cards will be materialized under `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/`

## 1. Phase identity

- Phase number: `10`
- Canonical phase name: `Meta-Cognition and Critique`
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
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
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
  - approved Phase 2 through Phase 9 execution, testing, and output surfaces under `projects/agifcore_master/04_execution/`, `projects/agifcore_master/05_testing/`, and `projects/agifcore_master/06_outputs/`
  - admin control files under `projects/agifcore_master/00_admin/`
  - project-scoped custom agent setup under `.codex/config.toml` and `.codex/agents/`
  - direct local donor inspection from the approved provenance pools, with direct focus on the v2 `CELL_FAMILIES` surface, Phase 8C governed structural growth plan/contracts/runtime/verifier, and Phase 9 real-runtime contracts/question-analyzer/answer-composer/open-question reasoning verifier

## 2. Phase mission

- Phase 10 exists to define and later build the governed meta-cognition and critique layer that can explain weakness, detect contradiction, track bounded self-state, and propose bounded redirect or fallback without pretending to be self-improvement.
- Phase 10 must later build:
  - self model
  - meta-cognition layer
  - attention redirect
  - meta-cognition observer
  - skeptic/counterexample
  - strategy journal
  - thinker tissue
  - surprise engine
  - theory fragments
  - weak-answer diagnosis
- Phase 10 must not:
  - implement Phase 11 self-improvement behavior
  - implement Phase 12 structural growth behavior
  - re-implement Phase 2 fabric control, Phase 4 memory policy, Phase 5 graph policy, Phase 6 simulator logic, Phase 7 conversation execution, Phase 8 science/world reasoning, or Phase 9 rich-expression realization
  - turn self-model language into unsupported self-assertion
  - turn critique into hidden chain-of-thought theater
  - turn diagnosis into exact fault claims without support
  - execute live external search
  - bypass support-state honesty
  - claim historical v1, tasklet, root v2, or v2 packages as earned AGIFCore completion
  - imply commit, freeze, approval, or closure

## 3. Scope and non-goals

- In-scope artifacts:
  - the canonical Phase 10 plan
  - Phase 10 planning task cards
  - meta-cognition and critique boundary rules
  - reuse and provenance decisions for each major subsystem
  - future execution, testing, output, and handoff targets
  - later demo, validation, and closure planning
- Out-of-scope work:
  - any Phase 10 runtime code
  - any Phase 10 verifier code
  - any Phase 10 evidence generation
  - any Phase 11 planning
  - any Phase 12 planning
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
- Explicit untouched-later-phase statement:
  - Phase 11 and all later phases remain untouched by this plan.

## 4. Phase 9 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 9 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` show Phase 9 `approved` and Phase 10 `open` | Phase 10 planning may proceed |
| Explicit Phase 9 closeout truth exists outside index tables | `pass` | `projects/agifcore_master/DECISIONS.md` and `projects/agifcore_master/CHANGELOG.md` confirm Phase 9 approval and that Phase 10 has not started | no silent approval assumption |
| Required Phase 1 provenance artifacts relied on exist | `pass` | `HUMAN_THINKING_TARGET.md`, `COMPONENT_CATALOG.md`, `SOURCE_INHERITANCE_MATRIX.md`, `RUNTIME_REBUILD_MAP.md`, `TRACE_CONTRACT.md`, `VALIDATION_PROTOCOL.md`, and `DEMO_PROTOCOL.md` are present | provenance and closure framing exist |
| Required Phase 2 through 9 artifacts relied on exist | `pass` | approved plans and approved execution/testing/output families for Phases 2 through 9 are present | runtime seams and honesty seams are inspectable |
| Dependency gap: canonical Phase 10 plan file is not present yet | `non-blocker` | `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md` did not exist before this planning run and is the target of this planning package | expected planning target |
| Dependency gap: Phase 10 planning task folder is not present yet | `non-blocker` | `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/` did not exist before this planning run | expected planning target |
| Compatibility seam: AGIFCore has no Phase 10 overlay contract yet | `non-blocker` | approved Phase 9 already exposes `revision_trace_ref`, `consolidation_trace_ref`, and `reorganization_trace_ref` as reserved overlay fields, but there is no approved Phase 10 coordinator schema yet | Phase 10 must define a new overlay contract above Phase 9 rather than mutate lower-phase truth |
| Compatibility seam: donor observer and counterexample records are research-only | `non-blocker` | `COMPONENT_CATALOG.md` marks `MetaCognitionObserverRecord` and `SkepticCounterexampleRecord` as `adapt_for_research_only` | Phase 10 must not treat those donor records as direct drop-in runtime logic |
| Blockers vs non-blockers | `planning not blocked` | all prerequisite approvals and planning inputs exist | readiness may be `ready_for_user_review` |

## 5. Active team map for Phase 10

Later Phase 10 execution default build pod: `Meta & Growth Pod Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | What it must never do this phase |
| --- | --- | --- | --- | --- | --- |
| `Program Governor` | `gpt-5.4` | active | prerequisite truth, danger-zone control, and final integration are required | own prerequisite truth, role activation, plan integration, artifact matrix, closure map, and final readiness judgment | implement runtime code, validate its own authored artifacts, or broaden into Phase 11 or 12 |
| `Constitution Keeper` | `gpt-5.4-mini` | active | Phase 10 can drift into unsupported self-assertion or early self-improvement | guard constitution, honesty, weak-support visibility, and phase boundaries | author runtime design alone, approve the phase, or allow Phase 11 or 12 leakage |
| `Source Cartographer` | `gpt-5.4-mini` | active | Phase 10 donor substrate is real but uneven and must not be rebuilt blindly | map each subsystem to donor basis, disposition, and reuse limits | invent a fifth disposition, treat historical code as earned completion, or approve the phase |
| `Architecture & Contract Lead` | `gpt-5.4` | active | Phase 10 needs a new critique overlay above approved Phase 9 surfaces | own subsystem boundaries, allowed interfaces, forbidden leaks, and the Phase 10 overlay-contract strategy | redesign earlier phases, collapse all critique into one giant introspection engine, or approve the phase |
| `Kernel Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 2 seam becomes ambiguous | consult on workspace, replay-anchor, or scheduler seams only if ambiguity appears | author the plan, implement code, or broaden Phase 2 |
| `Memory & Graph Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 4 or 5 seam becomes ambiguous | consult on continuity-memory, concept-graph, or theory-fragment persistence seams only if ambiguity appears | author the plan, implement code, or pull Phase 10 down into memory or graph layers |
| `World & Conversation Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 7, 8, or 9 seam becomes ambiguous | consult on conversation, science-world, or rich-expression input seams only if ambiguity appears | author the plan, implement code, or absorb Phase 10 into lower phases |
| `Meta & Growth Pod Lead` | `gpt-5.3-codex` | active | later execution owner and danger-zone build pod for Phase 10 | decompose the future runtime family for self-model, critique, redirect, observer, skeptic, strategy journal, thinker tissue, surprise, theory fragments, and weak-answer diagnosis | author canonical plan truth alone, implement code in this run, or absorb Phase 11 or 12 scope |
| `Product & Sandbox Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if runtime-shell or export seams become ambiguous | consult on runner-shell, packaging, or export-format seams only if ambiguity appears | author the plan, implement product work, or broaden scope |
| `Test & Replay Lead` | `gpt-5.4-mini` | active | critique quality must be test-planned from the start | define the verifier family, evidence expectations, danger-zone audit hooks, and closure failure signatures | implement runtime logic, fake reports, or approve the phase |
| `Anti-Shortcut Auditor` | `gpt-5.4-mini` | active | Phase 10 has high risk of fake introspection and unsupported self-claims | audit for fake completeness, giant-engine collapse, self-assertion theater, unsupported diagnosis, and unverifiable demos | rewrite the plan instead of auditing it, downgrade blockers casually, or approve the phase |
| `Merge Arbiter` | `gpt-5.3-codex` | inactive | planning-only run | none | imply closure or perform merge work |
| `Validation Agent` | `gpt-5.4` | active | final machine-side review of the planning package is required before user review | validate the plan package after audit and Governor verification exist | author the plan, implement runtime, or approve the phase |
| `Release & Evidence Lead` | `gpt-5.4-mini` | active | later critique demos must be inspectable and evidence-linked | define demo-bundle shape, review packet surfaces, and later demo ordering | implement runtime behavior, publish release material, or imply acceptance |

## 6. Reuse and provenance strategy

Only the frozen four disposition categories are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance artifact justification |
| --- | --- | --- | --- | --- |
| self model | `SelfModelRecord` in `COMPONENT_CATALOG.md`, v2 Phase 8C `SelfModelRecord` contracts/runtime, approved Phase 4 continuity memory, and approved Phase 7 self-knowledge surface | `port_with_provenance` | the record shape and bounded continuity semantics are strong inherited substrate; AGIFCore should port the record contract and rebind runtime logic to approved Phase 4 and 7 surfaces instead of inventing a new self-state format | `COMPONENT_CATALOG.md` row `CC-011`; `MEMORY_MODEL.md`; `TRACE_CONTRACT.md` |
| meta-cognition layer | v2 Phase 8C structural-growth runtime bundle, v2 Phase 9 real-runtime `ReasoningAttempt` and critic-check patterns, and critic tissue lineage | `rebuild_clean` | donor logic exists, but it is spread across proof-time structural-growth code and v2 answer-composer behavior; AGIFCore should rebuild a strict coordinator above approved Phase 7, 8, and 9 outputs rather than port a mixed orchestration layer | `COMPONENT_CATALOG.md` row `CC-034`; `RUNTIME_REBUILD_MAP.md` rows `RRM-003` and `RRM-006`; `FORMAL_MODELS.md` |
| attention redirect | v2 thinker-tissue `missing_needs` and `bounded_proposals`, v2 surprise-engine `triggered_action`, and v2 real-runtime question triage | `rebuild_clean` | there is useful donor behavior, but no exact stable Phase 1 component record for redirect control; AGIFCore should rebuild a bounded redirect layer that chooses what to re-check without importing v2 orchestration behavior wholesale | `COGNITIVE_PRIORS.md`; `TRACE_CONTRACT.md`; `FORMAL_MODELS.md` |
| meta-cognition observer | `MetaCognitionObserverRecord` in `COMPONENT_CATALOG.md` and v2 Phase 8C observer contracts/runtime | `adapt_for_research_only` | the inherited record is real and useful, but the component catalog already freezes it as research-only; AGIFCore may adapt its record ideas, but should not treat donor observer logic as direct runtime truth | `COMPONENT_CATALOG.md` row `CC-012`; `HUMAN_THINKING_TARGET.md`; `SCIENTIFIC_METHOD.md` |
| skeptic/counterexample | `SkepticCounterexampleRecord` in `COMPONENT_CATALOG.md`, v2 Phase 8C skeptic records, and v2 real-runtime skeptic-check patterns | `adapt_for_research_only` | the donor counterexample path is strong enough to shape AGIFCore boundaries, but the inherited runtime is proof-oriented and research-facing; AGIFCore should adapt the semantics and rebuild the actual execution path later | `COMPONENT_CATALOG.md` row `CC-014`; `HUMAN_THINKING_TARGET.md`; `TRACE_CONTRACT.md` |
| strategy journal | `StrategyJournalEntry` and `strategy_journal` in `COMPONENT_CATALOG.md`, plus v2 Phase 8C journal contracts/runtime | `port_with_provenance` | the journal record and bounded `worked`, `failed`, and `monitor` shape are exact inherited substrate; AGIFCore should port the contract surface and rebind it to approved lower-phase traces | `COMPONENT_CATALOG.md` rows `CC-013` and `CC-022`; `MEMORY_MODEL.md`; `TRACE_CONTRACT.md` |
| thinker tissue | `ThinkerTissueRecord` in `COMPONENT_CATALOG.md`, v2 `CELL_FAMILIES.md`, and v2 Phase 8C thinker-tissue runtime | `port_with_provenance` | the deeper-structure name, role, and bounded-governance framing are strongly inherited; AGIFCore should port the tissue contract and record shape while rebuilding runtime behavior against approved AGIFCore exports | `COMPONENT_CATALOG.md` row `CC-016`; `ROLE_AUTHORITY_RULES.md`; `ARCHITECTURE_OVERVIEW.md` |
| surprise engine | `SurpriseEngineRecord` in `COMPONENT_CATALOG.md` and v2 Phase 8C surprise-engine runtime | `rebuild_clean` | the component catalog already marks the surprise engine as a rebuild target; the donor proves the detection categories, but AGIFCore should rebuild strict contradiction and anomaly detection above approved lower-phase outputs | `COMPONENT_CATALOG.md` row `CC-015`; `COGNITIVE_PRIORS.md`; `GOVERNANCE_MODEL.md` |
| theory fragments | `theory_fragment` in `COMPONENT_CATALOG.md`, v2 Phase 8C `TheoryFragmentRecord`, and the approved Phase 5 concept-graph boundary | `port_with_provenance` | the fragment record, falsifier, and next-step shape are strong inherited substrate; AGIFCore should port the bounded candidate-record semantics and bind them to Phase 5 concept-graph persistence rules later | `COMPONENT_CATALOG.md` row `CC-021`; `GRAPH_STACK_MODEL.md`; `TRACE_CONTRACT.md` |
| weak-answer diagnosis | v2 Phase 9 real-runtime `bounded_answer_quality_diagnosis` and `bounded_diagnosis_triage` verifier pack, plus v2 answer-composer/question-analyzer behavior | `rebuild_clean` | the donor behavior is concrete, but it lives inside the v2 answer-composer lane, which `RUNTIME_REBUILD_MAP.md` already marks as a clean rebuild target; AGIFCore should rebuild a typed diagnosis lane that preserves honesty and boundedness | `RUNTIME_REBUILD_MAP.md` row `RRM-006`; `COMPONENT_CATALOG.md` row `CC-034`; `NORTH_STAR_LANGUAGE_TARGET.md` |

## 7. Meta-cognition and critique boundary rules

### What belongs in self model only

- represent bounded current-run self-state as typed `knows`, `infers`, `unknowns`, confidence band, and what would verify
- derive self-state from approved Phase 4 continuity, Phase 7 self-knowledge, and lower-phase support traces
- preserve self-history as bounded operational state, not a diary or identity narrative
- no unsupported self-assertion, no anthropomorphic claims, and no autonomous self-directed goals

### What belongs in meta-cognition layer only

- coordinate self-model, observer, redirect, skeptic, surprise, thinker tissue, theory fragments, and weak-answer diagnosis into one bounded critique pass
- preserve a typed meta-cognition turn record above approved Phase 9 output
- route only bounded critique outcomes such as `recheck_support`, `reframe_explanation`, `clarify`, `abstain`, or `no_redirect`
- no language-realization ownership, no direct answer-envelope ownership, and no implicit Phase 11 proposal pipeline

### What belongs in attention redirect only

- choose which weak link, contradiction, or missing variable deserves the next bounded look
- emit redirect targets tied to existing lower-phase refs
- stop after the bounded redirect ceiling and fail closed when the redirect path is underspecified
- no open-ended looping, no hidden rerun storm, and no direct mutation of lower-phase records

### What belongs in meta-cognition observer only

- record observed failures, repeated uncertainty, missing needs, and critique triggers
- preserve inspectable observer refs for replay and evidence
- remain observational unless the meta-cognition layer explicitly consumes the record
- no direct answer rewriting, no self-improvement proposal generation, and no hidden scoring theater

### What belongs in skeptic/counterexample only

- ask what could make the current answer or explanation wrong
- identify one bounded counterexample or one bounded variable flip that would weaken the claim
- record whether skepticism changed the output, kept it the same, or forced honest fallback
- no endless debate loop, no unsupported exact counterexample claims, and no rhetoric-only `skeptic` labels

### What belongs in strategy journal only

- record which reasoning path worked, which failed, which priors or patterns were used, and what should be monitored next
- preserve bounded operational notes for later replay and review
- stay grounded in actual trace refs and real failure or success evidence
- no action execution, no rule adoption, and no silent carryover into Phase 11 improvement

### What belongs in thinker tissue only

- aggregate weak-answer, contradiction, and repeated-uncertainty signals into bounded `what is missing` or `what should be checked` proposals
- preserve governance mode and bounded proposal refs
- stay explicitly separate from the build-machine Program Governor and from any human-review role
- no unrestricted self-modification, no global rewrite authority, and no hidden off-contract deliberation

### What belongs in surprise engine only

- detect contradiction, missing variable, boundary failure, wrong-prior choice, or weak causal chain
- trigger one bounded follow-up: re-check, concept refinement candidate, theory-fragment candidate, clarify, or honest fallback
- preserve typed trigger reason and typed triggered action
- no silent auto-fix and no unrestricted retry loop

### What belongs in theory fragments only

- store bounded candidate fragments with statement, source ref, falsifier, and next verification step
- remain provisional and explicitly weaker than accepted concept-graph truth
- align later persistence to approved Phase 5 concept-graph boundaries
- no theory adoption, no graph-wide propagation, and no autonomous theory formation

### What belongs in weak-answer diagnosis only

- explain why the answer was weak, vague, contradictory, underspecified, or support-thin
- surface the exact missing support, contradiction cue, or clarification need that made it weak
- propose the next bounded check or clarification without pretending the diagnosis is exact when it is not
- no support laundering, no exact blame claims without support, and no `diagnosis` prose with no typed diagnosis items

### What is explicitly forbidden to leak in from Phase 11 self-improvement behavior

- proposal generation or proposal adoption loops
- offline reflection and consolidation
- idle reflection as an autonomous improvement path
- self-experiment lab behavior
- shadow evaluation, before/after measurement, adoption or rejection pipeline, or post-adoption monitoring
- rollback-safe adoption machinery
- self-initiated inquiry engine behavior
- any closed-loop mechanism that changes AGIFCore behavior without separate governed approval

### What is explicitly forbidden to leak in from Phase 12 structural growth behavior

- self-model feedback-loop execution
- reflection-control-loop execution
- self-reorganization
- domain genesis
- theory formation beyond bounded candidate fragments
- procedure or tool invention
- curiosity or gap-selection autonomy
- structural growth of tissues, transfer structures, or runtime substrate

### How Phase 10 stays separate from Phase 7 execution except through allowed interfaces

Allowed Phase 7 inputs:

- `agifcore.phase_07.raw_text_intake.v1`
- `agifcore.phase_07.question_interpretation.v1`
- `agifcore.phase_07.support_state_logic.v1`
- `agifcore.phase_07.self_knowledge_surface.v1`
- `agifcore.phase_07.utterance_plan.v1`
- `agifcore.phase_07.answer_contract.v1`
- `agifcore.phase_07.conversation_turn.v1`

Rules for those inputs:

- they are read-only inputs only
- Phase 10 may use them to understand discourse mode, support-state honesty, self-knowledge bounds, answer mode, and current trace anchors
- Phase 10 may not mutate support state, next action, final answer mode, or the Phase 7 answer contract
- Phase 10 may not own user-facing response text directly

Forbidden Phase 7 interactions:

- direct mutation of Phase 7 runtime state
- laundering `search_needed`, `unknown`, or `abstain` into stronger support
- treating runtime critique as a replacement for the Program Governor or human review
- collapsing Phase 10 and Phase 7 into one opaque answer engine

### How Phase 10 stays separate from Phase 8 execution except through allowed interfaces

Allowed Phase 8 inputs:

- `agifcore.phase_08.scientific_priors.v1`
- `agifcore.phase_08.entity_request_inference.v1`
- `agifcore.phase_08.world_region_selection.v1`
- `agifcore.phase_08.causal_chain_reasoning.v1`
- `agifcore.phase_08.bounded_current_world_reasoning.v1`
- `agifcore.phase_08.visible_reasoning_summaries.v1`
- `agifcore.phase_08.science_reflection.v1`
- `agifcore.phase_08.science_world_turn.v1`

Rules for those inputs:

- they are read-only inputs only
- Phase 10 may critique, detect contradiction in, or diagnose weakness across those outputs
- Phase 10 may not rerun science priors, causal-chain reasoning, current-world reasoning, or science reflection
- Phase 10 may not reinterpret Phase 8 uncertainty as stronger support than Phase 8 declared

Forbidden Phase 8 interactions:

- direct mutation of Phase 8 runtime state
- hidden re-execution of science/world-awareness logic inside critique
- using critique wording to erase bounded current-world limits
- treating public reasoning summaries as hidden chain-of-thought

### How Phase 10 stays separate from Phase 9 execution except through allowed interfaces

Allowed Phase 9 inputs:

- `agifcore.phase_09.teaching.v1`
- `agifcore.phase_09.comparison.v1`
- `agifcore.phase_09.planning.v1`
- `agifcore.phase_09.synthesis.v1`
- `agifcore.phase_09.analogy.v1`
- `agifcore.phase_09.concept_composition.v1`
- `agifcore.phase_09.cross_domain_composition.v1`
- `agifcore.phase_09.audience_aware_explanation_quality.v1`
- `agifcore.phase_09.rich_expression_turn.v1`

Rules for those inputs:

- they are read-only inputs only
- Phase 10 may critique rich-expression choices, diagnose weakness, detect contradiction, and request bounded redirect or honest fallback
- Phase 10 may not own direct language realization
- Phase 10 may not silently rewrite the Phase 9 overlay contract or mutate Phase 9 snapshot truth

Forbidden Phase 9 interactions:

- direct mutation of Phase 9 runtime state
- treating meta-cognition as a replacement for the rich-expression layer
- using critique to smuggle in self-improvement or structural-growth behavior
- collapsing diagnosis, critique, redirect, and rewrite into one opaque `introspection` engine

### Phase 10 compatibility decision for inherited trace refs

- Phase 9 already exposes `revision_trace_ref`, `consolidation_trace_ref`, and `reorganization_trace_ref` as reserved optional overlay fields.
- Phase 10 should therefore define a new `agifcore.phase_10.meta_cognition_turn.v1` overlay above approved Phase 9 snapshots and carry explicit Phase 10 refs such as self-model, observer, strategy-journal, skeptic, surprise, theory-fragment, and diagnosis refs there.
- Phase 10 must not retroactively mutate Phase 7, 8, or 9 truth to pretend those fields already existed earlier.

## 8. Phase 10 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max self-model record count per run | `<= 4` records | stop and tighten self-state scope if later execution needs more than `4` records |
| max meta-cognition observation count per run | `<= 8` observations | stop and reduce observer fan-out if later execution exceeds `8` observations |
| max attention redirect count per run | `<= 2` redirects | stop and reopen redirect policy if later execution needs more than `2` redirects |
| max skeptic/counterexample branch count | `<= 3` branches | stop and reduce skeptic branching if later execution needs more than `3` counterexample branches |
| max strategy-journal entry count per run | `<= 2` entries | stop and tighten journal write conditions if later execution needs more than `2` entries |
| max thinker-tissue item count per run | `<= 6` items | stop and reduce thinker-tissue breadth if later execution exceeds `6` items |
| max surprise-event count per run | `<= 4` events | stop and reopen surprise policy if later execution exceeds `4` surprise events |
| max theory-fragment count per run | `<= 3` fragments | stop and tighten fragment creation if later execution exceeds `3` fragments |
| max weak-answer diagnosis item count per run | `<= 5` items | stop and reduce diagnosis granularity if later execution exceeds `5` diagnosis items |
| max Phase 10 evidence and demo bundle size | `<= 112 MiB` | stop and reorganize outputs if the bundle exceeds `112 MiB` |

Budget rules:

- these are laptop-profile planning ceilings only
- later execution must measure against them directly
- any ceiling breach must stop and escalate instead of widening silently
- any later need for higher ceilings requires reopening planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2 through 9 baselines, requirements pack, design pack, admin controls, and donor inspection | all later Phase 10 work | section-complete Phase 10 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, and the Phase 10 plan | all later valid Phase 10 work | one planning task card per active role |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_PLAN_FREEZE_HANDOFF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 10 plan and admin controls | later execution start | frozen scope, active roles, blocked actions, and no-approval status are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_EXECUTION_START_BRIEF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 10 plan and admin controls | later execution start | execution scope, danger-zone controls, and file families are explicit |
| `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/` | `Meta & Growth Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 2 through 9 surfaces, Phase 10 plan, provenance package, and trace contract | later Phase 10 runtime delivery | runtime family exists and matches the plan |
| `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/` | `Meta & Growth Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | same as above plus the exact module breakdown from this plan | later Phase 10 runtime delivery | self-model, layer, redirect, observer, skeptic, journal, thinker tissue, surprise, theory-fragment, diagnosis, and coordinator modules exist |
| `projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 10 plan, execution family, validation protocol, and demo protocol | later verification and closeout | verifier family exists and runs |
| `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifier outputs, runtime snapshots, and demo traces | audit, Governor verification, and validation | machine-readable evidence bundle is inspectable |
| `projects/agifcore_master/06_outputs/phase_10_meta_cognition_and_critique/phase_10_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, and validation protocol | user review | `why was this weak` and contradiction demo bundle exists |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-01_PHASE_10_FINAL_PACKAGE_AUDIT_REPORT.md` | `Anti-Shortcut Auditor` | `Program Governor` | `n/a` | `Validation Agent` | runtime, tests, evidence, demos, and planning truth | Governor verification | standard final audit exists |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-AUDIT-02_PHASE_10_DANGER_ZONE_AUDIT_REPORT.md` | `Anti-Shortcut Auditor` | `Constitution Keeper` | `n/a` | `Validation Agent` | runtime, tests, evidence, demos, and Meta & Growth danger-zone controls | Governor verification | extra danger-zone audit exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, rerun verifiers, demo bundle, evidence bundle | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdict request are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| self-model, meta-cognition layer, and observer planning | define the bounded self-state, critique coordinator, and observer lane | `Architecture & Contract Lead` | `Source Cartographer`, `Constitution Keeper`, `Meta & Growth Pod Lead` | future `contracts.py`, `self_model.py`, `meta_cognition_layer.py`, `meta_cognition_observer.py`, `meta_cognition_turn.py` | prerequisite truth and reuse map exist | self-state, observer, and coordinator boundaries are explicit and separate from Phase 11 and 12 |
| attention redirect and skeptic planning | define bounded redirect policy and counterexample behavior | `Meta & Growth Pod Lead` | `Architecture & Contract Lead`, `Source Cartographer`, `World & Conversation Pod Lead` consult-only | future `attention_redirect.py` and `skeptic_counterexample.py` | boundary rules are stable | redirect and skeptic behavior are typed, bounded, and fail closed |
| strategy journal and thinker tissue planning | define replayable strategy learning records and thinker-tissue aggregation | `Meta & Growth Pod Lead` | `Architecture & Contract Lead`, `Source Cartographer`, `Memory & Graph Pod Lead` consult-only | future `strategy_journal.py` and `thinker_tissue.py` | reuse map is stable | journal and thinker-tissue surfaces are explicit, bounded, and non-autonomous |
| surprise engine and theory-fragment planning | define contradiction and anomaly detection and provisional theory-fragment handling | `Meta & Growth Pod Lead` | `Architecture & Contract Lead`, `Source Cartographer`, `Memory & Graph Pod Lead` consult-only | future `surprise_engine.py` and `theory_fragments.py` | boundary rules are stable | surprise and fragment behavior are explicit, falsifiable, and do not become structural growth |
| weak-answer diagnosis planning | define the bounded `why was this weak` lane and contradiction-diagnosis rules | `Architecture & Contract Lead` | `Constitution Keeper`, `Meta & Growth Pod Lead`, `World & Conversation Pod Lead` consult-only | future `weak_answer_diagnosis.py` | approved Phase 7, 8, and 9 interfaces are clear | diagnosis behavior is explicit, support-honest, and non-theatrical |
| test, demo, validation, and evidence planning | define verifier family, evidence reports, extra danger-zone audit path, demo bundle, and validation path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | verifier plan, evidence plan, demo plan, extra-audit plan, and validation surfaces | runtime-family targets are stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. `Program Governor` verifies Phase 9 approval truth and confirms Phase 10 remains `open`.
2. `Program Governor` locks active, consult-only, and inactive roles for Phase 10 planning.
3. `Source Cartographer` maps all required Phase 10 subsystems to donor basis and one allowed disposition.
4. `Architecture & Contract Lead` drafts subsystem boundaries, allowed Phase 7, 8, and 9 interfaces, and forbidden Phase 11 and 12 leaks.
5. `Meta & Growth Pod Lead` drafts the future runtime-family decomposition after the first-pass reuse map and boundary rules exist.
6. `Constitution Keeper` reviews the first-pass reuse map and boundary rules for unsupported self-assertion, support laundering, and Phase 11 or 12 leakage.
7. If a Phase 2 seam is ambiguous, `Kernel Pod Lead` is consulted narrowly and remains non-authoring.
8. If a Phase 4 or Phase 5 seam is ambiguous, `Memory & Graph Pod Lead` is consulted narrowly and remains non-authoring.
9. If a Phase 7, 8, or 9 seam is ambiguous, `World & Conversation Pod Lead` is consulted narrowly and remains non-authoring.
10. If a runtime-shell or output-format seam is ambiguous, `Product & Sandbox Pod Lead` is consulted narrowly and remains non-authoring.
11. `Test & Replay Lead` and `Release & Evidence Lead` define verifier, evidence, demo, and danger-zone audit families after the runtime-family targets are stable.
12. `Program Governor` consolidates the plan, task-card set, artifact matrix, budget envelope, and closure map.
13. `Anti-Shortcut Auditor` audits the full planning package.
14. `Program Governor` independently re-reads the cited files directly and verifies the package.
15. `Validation Agent` prepares the later review request only after audit and Governor verification exist.
16. User review happens only after the validated planning package exists.

Safe parallelism:

- `Source Cartographer` and `Architecture & Contract Lead` may work in parallel on disjoint planning outputs.
- `Meta & Growth Pod Lead` waits for first-pass reuse and boundary outputs before locking the runtime family.
- `Test & Replay Lead` and `Release & Evidence Lead` wait for stable runtime-family targets.
- `Merge Arbiter` remains inactive in planning-only work.

## 12. Detailed task cards

### `P10-TC-PG-01`

- task card ID: `P10-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, the canonical Phase 10 plan, role activation, artifact matrix, budget envelope, closure map, and final readiness judgment
- exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-PG-01_PHASE_10_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 11 and later artifacts
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - `.codex/`
- required reads first:
  - the frozen read-before-work stack from `ROLE_AUTHORITY_RULES.md`
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 through 9 plans and execution surfaces
  - relevant requirement and design files
- step-by-step work method:
  1. verify Phase 9 approval truth
  2. lock active, consult-only, and inactive roles
  3. consolidate reuse, boundary, runtime-family, verifier, and demo outputs
  4. lock future artifact families and closure mapping
  5. prepare the final planning package for audit
- required cross-checks:
  - no Phase 11 planning
  - no Phase 12 planning
  - no runtime implementation
  - no approval language
- exit criteria:
  - the Phase 10 planning package is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation, closure, or approval
- explicit proof that no approval is implied: this task ends at plan readiness only; Phase 10 remains `open`

### `P10-TC-CK-01`

- task card ID: `P10-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4-mini`
- objective: guard constitution, falsification honesty, and Phase 10 boundary discipline
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-CK-01_PHASE_10_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - the Phase 10 draft
- step-by-step work method:
  1. check that self model stays evidence-bound
  2. check that weak-answer diagnosis preserves weak-support honesty
  3. check that Phase 10 stays below Phase 11 and Phase 12
  4. report any boundary drift to `Program Governor`
- required cross-checks:
  - no hidden-model loophole
  - no self-assertion theater
  - no support laundering
  - no Phase 11 or 12 behavior
  - no approval language
- exit criteria:
  - constitutional objections are resolved or explicitly raised as blockers
- handoff target: `Program Governor`
- anti-drift rule: do not author runtime design or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P10-TC-SC-01`

- task card ID: `P10-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4-mini`
- objective: map every major Phase 10 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-SC-01_PHASE_10_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 7, 8, and 9 plans and execution surfaces
  - inspected donor Phase 8C and Phase 9 real-runtime files
- step-by-step work method:
  1. map all ten Phase 10 subsystems
  2. assign one allowed disposition to each subsystem
  3. flag where exact record inheritance is stronger than runtime portability
  4. pass unresolved seam notes to `Architecture & Contract Lead` and `Program Governor`
- required cross-checks:
  - no fifth disposition
  - no silent omission
  - no treating historical packages as earned AGIFCore runtime
- exit criteria:
  - each subsystem has source basis, disposition, and rationale
- handoff target: `Architecture & Contract Lead` then `Program Governor`
- anti-drift rule: do not claim inspected historical code is already valid AGIFCore runtime
- explicit proof that no approval is implied: provenance mapping does not earn the phase

### `P10-TC-ACL-01`

- task card ID: `P10-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 10 boundaries, allowed interfaces, forbidden leaks, and the Phase 10 overlay-contract strategy
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-ACL-01_PHASE_10_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 7, 8, and 9 plans
  - `Source Cartographer` output
- step-by-step work method:
  1. define what belongs in each Phase 10 subsystem only
  2. define allowed Phase 7, 8, and 9 interfaces
  3. define the supplemental Phase 10 overlay-contract strategy
  4. define forbidden Phase 11 and 12 leaks
  5. pass runtime-family implications to `Program Governor` and `Meta & Growth Pod Lead`
- required cross-checks:
  - no one mixed introspection engine
  - no final response-envelope ownership inside Phase 10
  - no direct mutation of Phase 7, 8, or 9 state
  - no self-improvement or structural-growth semantics
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `Meta & Growth Pod Lead`
- anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, science-world, rich-expression, or the team
- explicit proof that no approval is implied: boundary framing is planning truth only

### `P10-TC-MGPL-01`

- task card ID: `P10-TC-MGPL-01`
- role owner: `Meta & Growth Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 10 runtime family without crossing into Phase 11 or 12
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-MGPL-01_PHASE_10_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - approved Phase 2 through 9 plans and execution surfaces
  - the Phase 10 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
- step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_10_meta_cognition_and_critique/agifcore_phase10_meta_cognition/`
  2. keep the module set explicit:
     - `contracts.py`
     - `self_model.py`
     - `meta_cognition_layer.py`
     - `attention_redirect.py`
     - `meta_cognition_observer.py`
     - `skeptic_counterexample.py`
     - `strategy_journal.py`
     - `thinker_tissue.py`
     - `surprise_engine.py`
     - `theory_fragments.py`
     - `weak_answer_diagnosis.py`
     - `meta_cognition_turn.py`
  3. order implementation so contracts come first, then self-model/layer/observer, then redirect/skeptic, then journal/thinker tissue, then surprise/theory fragments, then diagnosis, and the thin coordinator last
  4. identify where Phase 7, 8, and 9 exports must be consumed read-only
- required cross-checks:
  - no runtime code written now
  - no Phase 11 behavior
  - no Phase 12 behavior
  - no hidden self-improvement path
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase

### `P10-TC-TRL-01`

- task card ID: `P10-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4-mini`
- objective: define the Phase 10 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-TRL-01_PHASE_10_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 9 verifier and evidence families
  - the Phase 10 draft
- step-by-step work method:
  1. define one verifier per major Phase 10 subsystem
  2. define cross-cutting contradiction, weak-answer diagnosis, and honesty checks
  3. define evidence reports and manifest contents
  4. define the extra Meta & Growth danger-zone audit hook surfaces
- required cross-checks:
  - tests must verify separation between all ten Phase 10 subsystems
  - weak-answer diagnosis must preserve support-state honesty
  - contradiction handling must be typed and evidence-linked
  - no verifier may accept prose-only introspection as success
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P10-TC-ASA-01`

- task card ID: `P10-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4-mini`
- objective: audit the Phase 10 planning package for fake completeness, greenfield recreation, giant-engine collapse, and danger-zone drift
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-ASA-01_PHASE_10_PLAN_AUDIT.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - full Phase 10 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `Test & Replay Lead` evidence-plan output
  - relevant approved Phase 7, 8, and 9 plans
- step-by-step work method:
  1. check that all required sections exist
  2. check that each major subsystem has a source basis and disposition
  3. check that no one giant introspection engine is being passed off as design
  4. check that no approval or completion claim is implied
- required cross-checks:
  - no blind rewrite where a plausible substrate exists
  - no silent omission of any required subsystem
  - no Phase 11 or 12 behavior smuggled in
  - no empty report path or unverifiable demo plan
- exit criteria:
  - all blockers are either cleared or explicitly raised
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P10-TC-VA-01`

- task card ID: `P10-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 10 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-VA-01_PHASE_10_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_10_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - full Phase 10 draft
  - audit output
  - Governor verification output
  - validation protocol
- step-by-step work method:
  1. confirm the plan is decision-complete
  2. confirm every closure requirement has a later artifact path
  3. confirm the later demos are inspectable and truthful
  4. confirm the extra danger-zone audit path exists in the closure chain
- required cross-checks:
  - no author and validator role collision
  - no missing review surface
  - no implied approval
- exit criteria:
  - review request scope is exact and inspectable
- handoff target: `Program Governor`
- anti-drift rule: do not author plan content or runtime behavior
- explicit proof that no approval is implied: validation asks for review and does not mark the phase earned

### `P10-TC-REL-01`

- task card ID: `P10-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4-mini`
- objective: define the later Phase 10 demo-bundle shape and review packet surfaces
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_10/P10-TC-REL-01_PHASE_10_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 11 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 9 demo bundle
  - `Test & Replay Lead` verifier and evidence plan
  - the Phase 10 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the `why was this weak` demo surface
  3. define the contradiction demo surface
  4. define the user-review packet order
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
| self model exists | `self_model.py`, `verify_phase_10_self_model.py`, `phase_10_self_model_report.json` | `Meta & Growth Pod Lead` | verifier confirms bounded `knows/infers/unknowns`, confidence band, and verification cues | free-form self-description with no typed self-state |
| meta-cognition layer exists | `meta_cognition_layer.py`, `verify_phase_10_meta_cognition_layer.py`, `phase_10_meta_cognition_layer_report.json` | `Meta & Growth Pod Lead` | verifier confirms typed coordination over lower-phase snapshots and bounded redirect outputs | one opaque introspection module with no inspectable coordination record |
| attention redirect exists | `attention_redirect.py`, `verify_phase_10_attention_redirect.py`, `phase_10_attention_redirect_report.json` | `Meta & Growth Pod Lead` | verifier confirms bounded redirect targets, ceilings, and fail-closed behavior | open-ended rerun looping or undocumented redirect outcomes |
| meta-cognition observer exists | `meta_cognition_observer.py`, `verify_phase_10_meta_cognition_observer.py`, `phase_10_meta_cognition_observer_report.json` | `Meta & Growth Pod Lead` | verifier confirms typed observations tied to lower-phase trace refs | prose-only `observer notes` with no typed observation surface |
| skeptic/counterexample exists | `skeptic_counterexample.py`, `verify_phase_10_skeptic_counterexample.py`, `phase_10_skeptic_counterexample_report.json` | `Meta & Growth Pod Lead` | verifier confirms bounded counterexample generation, variable-flip logic, and changed-answer reporting | a skeptic label with no counterexample record or no impact accounting |
| strategy journal exists | `strategy_journal.py`, `verify_phase_10_strategy_journal.py`, `phase_10_strategy_journal_report.json` | `Meta & Growth Pod Lead` | verifier confirms typed worked/failed/monitor fields and trace-linked entries | diary-like notes or unsupported journal summaries |
| thinker tissue exists | `thinker_tissue.py`, `verify_phase_10_thinker_tissue.py`, `phase_10_thinker_tissue_report.json` | `Meta & Growth Pod Lead` | verifier confirms bounded missing-needs and bounded-proposal aggregation under governance | thinker tissue as a hidden free-form deliberation engine |
| surprise engine exists | `surprise_engine.py`, `verify_phase_10_surprise_engine.py`, `phase_10_surprise_engine_report.json` | `Meta & Growth Pod Lead` | verifier confirms contradiction and anomaly detection plus typed triggered action | contradiction claims with no typed trigger reason or no bounded action |
| theory fragments exist | `theory_fragments.py`, `verify_phase_10_theory_fragments.py`, `phase_10_theory_fragments_report.json` | `Meta & Growth Pod Lead` | verifier confirms fragment statement, falsifier, next step, and bounded persistence rules | fragment notes with no falsifier, no next step, or implicit theory adoption |
| weak-answer diagnosis exists | `weak_answer_diagnosis.py`, `verify_phase_10_weak_answer_diagnosis.py`, `phase_10_weak_answer_diagnosis_report.json` | `Meta & Growth Pod Lead` | verifier confirms typed diagnosis items, missing-support cues, and honest next-step guidance | vague `answer was weak` prose with no typed diagnosis or support linkage |
| demo path exists | `phase_10_demo_index.md`, `phase_10_why_was_this_weak_demo.md`, `phase_10_contradiction_demo.md` plus matching `.json` outputs | `Release & Evidence Lead` | direct demo-bundle inspection and rerunnable demo scripts | no inspectable demo or demo claims unsupported by evidence |
| tests/evidence path exists | full verifier family under `05_testing/phase_10_meta_cognition_and_critique/` and `phase_10_evidence_manifest.json` | `Test & Replay Lead` | Governor rerun plus validation request | missing verifier coverage, missing manifest, or non-machine-readable evidence |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| `why was this weak` demo | `meta_cognition_turn.py`, `self_model.py`, `meta_cognition_observer.py`, `weak_answer_diagnosis.py`, `strategy_journal.py`, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Meta & Growth Pod Lead` | `Anti-Shortcut Auditor` | the original prompt, lower-phase input snapshots used, self-model fields, weakness signals, diagnosis items, redirect outcome, journal entry, and the backing evidence reports |
| contradiction demo | `meta_cognition_turn.py`, `surprise_engine.py`, `skeptic_counterexample.py`, `thinker_tissue.py`, `theory_fragments.py`, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Meta & Growth Pod Lead` | `Anti-Shortcut Auditor` | the original prompt or state, contradiction trigger, counterexample record, whether the answer changed, triggered action, theory-fragment candidate or honest fallback, and the backing evidence reports |

Validation rules for both demos:

- `Validation Agent` prepares the review request only after the standard audit, the extra danger-zone audit, and the Governor verification record exist.
- `Program Governor` is the only role that asks the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.
- If any self-improvement, self-initiated inquiry, or structural-growth behavior appears during Phase 10 execution, the correct action is to stop and escalate boundary drift, not to widen the demo scope.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable critique substrate | compare subsystem plans and later runtime against mapped donor files and exact inherited records | `Source Cartographer` | a subsystem is rebuilt from zero despite a clear donor basis or exact inherited record surface | stop and reopen reuse mapping before execution |
| one giant introspection engine pretending to do all meta-cognition functions | boundary audit and verifier-plan audit | `Architecture & Contract Lead` | one opaque module is asked to own most Phase 10 behavior | reject the design and split the lanes before continuing |
| self model becoming unsupported self-assertion | constitution review and later self-model verifier | `Constitution Keeper` | self-model fields are not derived from lower-phase traces or they make unsupported identity claims | stop and tighten self-model rules |
| skeptic/counterexample existing only as labels | skeptic verifier and contradiction-demo audit | `Anti-Shortcut Auditor` | counterexample language appears without typed counterexample records or changed-answer accounting | block closure until skeptic behavior is real |
| theory fragments existing only as notes with no effect | fragment verifier and evidence audit | `Meta & Growth Pod Lead` | fragments can be produced without falsifier, next-step, or bounded persistence rules | stop and require effect-bound fragment rules |
| weak-answer diagnosis existing only as prose | diagnosis verifier and `why was this weak` demo audit | `Constitution Keeper` | a diagnosis explanation is present without typed diagnosis items or support linkage | stop and require typed diagnosis outputs |
| Phase 10 accidentally absorbing Phase 11 self-improvement behavior | boundary audit against the forbidden Phase 11 list | `Constitution Keeper` | proposal generation, adoption logic, self-experiment behavior, or self-initiated inquiry appears in Phase 10 | stop and remove the self-improvement dependency |
| Phase 10 accidentally absorbing Phase 12 structural growth behavior | boundary audit against the forbidden Phase 12 list | `Constitution Keeper` | self-reorganization, domain genesis, theory formation, or structural-growth control loops appear in Phase 10 | stop and remove the structural-growth dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 10 plan artifacts
- after user approval, any future change to the Phase 10 plan requires explicit reopen instruction and a supersession note

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 9 is explicitly `approved` in the live phase-truth files and corroborated by the decision and changelog records.
- Phase 10 remains `open`.
- The required provenance stack, approved Phase 2 through 9 baselines, requirements pack, design pack, admin controls, and donor substrate were all reviewed directly.
- No prerequisite blocker was found.
- The main non-blocker seams are:
  - Phase 10 has no AGIFCore overlay contract yet and must layer above approved Phase 9 truth rather than mutate it.
  - `MetaCognitionObserverRecord` and `SkepticCounterexampleRecord` are useful donor substrate but remain research-only in the component catalog.
  - weak-answer diagnosis has strong donor behavior but is entangled with the v2 answer-composer lane and therefore stays a clean rebuild target.
- Defaults locked by this draft:
  - later execution keeps one active build pod by default: `Meta & Growth Pod Lead`
  - self model, strategy journal, thinker tissue, and theory fragments default toward `port_with_provenance`
  - meta-cognition observer and skeptic/counterexample default toward `adapt_for_research_only`
  - meta-cognition layer, attention redirect, surprise engine, and weak-answer diagnosis default toward `rebuild_clean`
  - Phase 10 remains a read-only critique and meta-cognition layer above approved Phase 7, 8, and 9 outputs and below Phase 11 and Phase 12 behavior
