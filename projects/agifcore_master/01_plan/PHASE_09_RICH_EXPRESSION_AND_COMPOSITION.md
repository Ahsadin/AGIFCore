# Phase 9: Rich Expression and Composition

## 1. Phase identity

- Phase number: `9`
- Canonical phase name: `Rich Expression and Composition`
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
  - approved Phase 2 through Phase 8 execution, testing, and output surfaces under `projects/agifcore_master/04_execution/`, `projects/agifcore_master/05_testing/`, and `projects/agifcore_master/06_outputs/`
  - direct local donor inspection from the approved provenance pools, with direct focus on the v2 Phase 9 contracts/composer/analyzer surfaces and the v2 Phase 7A rich-expression, analogy, and composition evaluation substrate

## 2. Phase mission

- Phase 9 exists to define and later build the governed rich-expression and composition layer that turns already-bounded support into clearer, more useful, less generic user-facing structure.
- Phase 9 must later build:
  - teaching
  - comparison
  - planning
  - synthesis
  - analogy
  - concept composition
  - cross-domain composition
  - audience-aware explanation quality
- Phase 9 must not:
  - implement Phase 10 meta-cognition behavior
  - implement Phase 11 self-improvement behavior
  - re-implement Phase 2 fabric control, Phase 4 memory policy, Phase 5 graph policy, Phase 6 simulator logic, Phase 7 conversation honesty routing, or Phase 8 science/world reasoning
  - turn fluent wording into fake proof
  - execute live external search
  - bypass support-state honesty
  - claim historical v1, tasklet, root v2, or v2 packages as earned AGIFCore completion
  - imply commit, freeze, approval, or closure

## 3. Scope and non-goals

- In-scope artifacts:
  - the canonical Phase 9 plan
  - Phase 9 planning task cards
  - rich-expression and composition boundary rules
  - reuse and provenance decisions for each major subsystem
  - future execution, testing, output, and handoff targets
  - later demo, validation, and closure planning
- Out-of-scope work:
  - any Phase 9 runtime code
  - any Phase 9 verifier code
  - any Phase 9 evidence generation
  - any Phase 10 planning
  - any Phase 11 planning
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
- Explicit untouched-later-phase statement:
  - Phase 10 and all later phases remain untouched by this plan.

## 4. Phase 8 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 8 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` show Phase 8 `approved` and Phase 9 `open` | Phase 9 planning may proceed |
| Explicit Phase 8 closeout truth exists outside index tables | `pass` | `projects/agifcore_master/DECISIONS.md` and `projects/agifcore_master/CHANGELOG.md` confirm Phase 8 approval and that Phase 9 has not started | no silent approval assumption |
| Required Phase 1 provenance artifacts relied on exist | `pass` | `HUMAN_THINKING_TARGET.md`, `COMPONENT_CATALOG.md`, `SOURCE_INHERITANCE_MATRIX.md`, `RUNTIME_REBUILD_MAP.md`, `TRACE_CONTRACT.md`, `VALIDATION_PROTOCOL.md`, and `DEMO_PROTOCOL.md` are present | provenance and closure framing exist |
| Required Phase 2 to 8 artifacts relied on exist | `pass` | approved plans and approved execution/testing/output families for Phases 2 through 8 are present | runtime seams and honesty seams are inspectable |
| Dependency gap: canonical Phase 9 plan file is not present yet | `non-blocker` | `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md` did not exist before this planning run and is the target of this planning package | expected planning target |
| Dependency gap: Phase 9 planning task folder is not present yet | `non-blocker` | `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/` did not exist before this planning run | expected planning target |
| Dependency gap: project-scoped `.codex/` custom-agent setup is not present yet | `non-blocker` | repo-local `.codex/config.toml` and `.codex/agents/` did not exist before this planning run | expected setup target |
| Compatibility seam: live Phase 7 runtime does not yet visibly expose inherited Phase 9 trace refs | `non-blocker` | the Phase 1 provenance package keeps `concept_composition_ref`, `analogy_trace_ref`, `revision_trace_ref`, `consolidation_trace_ref`, and `reorganization_trace_ref` visible, but the approved Phase 7 runtime surface does not yet expose them as active contract fields | Phase 9 must define a supplemental overlay contract instead of silently assuming those fields already exist |
| Blockers vs non-blockers | `planning not blocked` | all prerequisite approvals and planning inputs exist | readiness may be `ready_for_user_review` |

## 5. Active team map for Phase 9

Later Phase 9 execution default build pod: `World & Conversation Pod Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | What it must never do this phase |
| --- | --- | --- | --- | --- | --- |
| `Program Governor` | `gpt-5.4` | active | planning authority, prerequisite truth, custom-agent setup ownership, and final integration are required | own prerequisite truth, role activation, setup-package spec, plan integration, artifact matrix, closure map, and final readiness judgment | implement runtime code, validate its own authored artifacts, or broaden into Phase 10 |
| `Constitution Keeper` | `gpt-5.4 mini` | active | Phase 9 can drift into persuasion, hidden support laundering, or early meta-cognition | guard constitution, honesty, non-negotiables, and phase boundaries | author runtime design alone, approve the phase, or leak Phase 10/11 behavior |
| `Source Cartographer` | `gpt-5.4 mini` | active | Phase 9 has strong donor substrate and must not be rebuilt blindly | map each subsystem to donor basis, disposition, and reuse limits | invent a fifth disposition, treat historical code as earned completion, or approve the phase |
| `Architecture & Contract Lead` | `gpt-5.4` | active | Phase 9 must define narrow interfaces above Phase 8 and beside Phase 7 | own subsystem boundaries, allowed interfaces, forbidden leaks, and the Phase 9 overlay contract strategy | redesign earlier phases, collapse all rich expression into one style engine, or approve the phase |
| `Kernel Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 2 seam becomes ambiguous | consult on workspace, turn, replay, or trace-export seams only if ambiguity appears | author the plan, implement code, or broaden Phase 2 |
| `Memory & Graph Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 4 or Phase 5 seam becomes ambiguous | consult on reviewed memory, concept graph, or support-selection seams only if ambiguity appears | author the plan, implement code, or pull Phase 9 down into memory or graph layers |
| `World & Conversation Pod Lead` | `gpt-5.3-codex` | active | later execution owner and default build pod for rich-expression work | decompose the future runtime family for teaching, comparison, planning, synthesis, analogy, composition, and audience-aware explanation | author canonical plan truth alone, implement code in this run, or absorb Phase 10/11 scope |
| `Meta & Growth Pod Lead` | `gpt-5.3-codex` | inactive | unrelated to Phase 9 planning and dangerous for boundary drift | none | activate casually or leak self-improvement into Phase 9 |
| `Product & Sandbox Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if runtime-shell or export-format seams become ambiguous | consult on runner-shell, bundle-output, or packaging seams only if ambiguity appears | author the plan, implement product work, or broaden scope |
| `Test & Replay Lead` | `gpt-5.4 mini` | active | rich-expression quality must be test-planned from the start | define the verifier family, evidence expectations, demo checks, and closure failure signatures | implement runtime logic, fake reports, or approve the phase |
| `Anti-Shortcut Auditor` | `gpt-5.4 mini` | active | Phase 9 has high risk of fake style quality and giant-engine collapse | audit for fake completeness, support laundering, unsupported analogy, and unverifiable demos | rewrite the plan instead of auditing it, downgrade blockers casually, or approve the phase |
| `Merge Arbiter` | `gpt-5.3-codex` | inactive | planning-only run | none | imply closure or perform merge work |
| `Validation Agent` | `gpt-5.4` | active | final machine-side review of the planning package is required before user review | validate the plan package after audit and governor verification exist | author the plan, implement runtime, or approve the phase |
| `Release & Evidence Lead` | `gpt-5.4 mini` | active | later demos must be inspectable and non-generic | define demo-bundle shape, review packet surfaces, and later demo ordering | implement runtime behavior, publish release material, or imply acceptance |

## 6. Reuse and provenance strategy

Only the frozen four disposition categories are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance artifact justification |
| --- | --- | --- | --- | --- |
| teaching | v2 Phase 7A rich-expression routing and v2 Phase 9 explanation scaffolds, plus approved Phase 7 `TEACH` discourse mode and Phase 8 visible-support surfaces | `rebuild_clean` | donor routing and phrasing heuristics are real but tightly coupled to older conversation runtime and mixed support logic. AGIFCore should rebuild a typed teaching lane above approved Phase 7 and 8 outputs while preserving bounded scaffolding ideas | `HUMAN_THINKING_TARGET.md`; `RUNTIME_REBUILD_MAP.md` row `RRM-006`; `COMPONENT_CATALOG.md` rows `CC-023` and `CC-024` |
| comparison | v2 rich-expression compare mode, v2 Phase 9 comparison wording paths, and approved Phase 7 `COMPARE` discourse mode | `rebuild_clean` | comparison is clearly a real substrate, but donor logic is heuristic and not safely separable from older answer-composer behavior. AGIFCore should rebuild a typed axis-based comparison layer that preserves honesty and traceability | `HUMAN_THINKING_TARGET.md`; `RUNTIME_REBUILD_MAP.md` row `RRM-006`; `TRACE_CONTRACT.md` |
| planning | v2 rich-expression plan mode, v2 activation-plan lineage, and the inherited `planner` tissue role | `rebuild_clean` | the donor proves there is a planning-facing expression substrate, but old activation-plan logic is coupled to runtime orchestration. AGIFCore should rebuild user-facing bounded planning expression without importing runtime activation semantics or later strategy journals | `COMPONENT_CATALOG.md` row `CC-032`; `HUMAN_THINKING_TARGET.md`; `TRACE_CONTRACT.md` |
| synthesis | v2 open-question composer paths and rich-expression explain routes, plus approved Phase 8 visible reasoning and science-world snapshots | `rebuild_clean` | synthesis exists in the donor, but the old runtime mixes expression, current-world routing, and support decisions. AGIFCore should rebuild bounded multi-input synthesis that never upgrades support or hides uncertainty | `HUMAN_THINKING_TARGET.md`; `RUNTIME_REBUILD_MAP.md` row `RRM-006`; `TRACE_CONTRACT.md` |
| analogy | exact inherited `analogy_trace_ref` contract item, the v2 analogy gap substrate, and donor analogy-facing wording paths | `port_with_provenance` | this subsystem has a stronger exact inherited surface than the other rich-expression lanes because the trace carrier is already frozen in Phase 1. AGIFCore should port the analogy trace contract and bounded analogy-policy expectations with provenance, then rebind the runtime logic to approved Phase 7 and 8 inputs | `COMPONENT_CATALOG.md` row `CC-027`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-053` and `SIM-062`; `TRACE_CONTRACT.md` |
| concept composition | exact inherited `concept_composition_ref` contract item, the v2 compositional-insight substrate, and NS6 composition evaluation policies | `port_with_provenance` | concept composition has exact inherited trace support plus a strong bounded two-domain policy substrate. AGIFCore should port the trace carrier and bounded composition-policy surface with provenance, while rebuilding execution logic against approved Phase 5, 6, 7, and 8 exports | `COMPONENT_CATALOG.md` row `CC-025`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-053` and `SIM-062`; `TRACE_CONTRACT.md` |
| cross-domain composition | v2 compositional-insight substrate and NS6 composition boundary policy, especially the guarded two-domain-only precedent | `rebuild_clean` | donor material provides strong boundary cues, but the runtime logic remains experimental and entangled with older conversation machinery. AGIFCore should rebuild a stricter typed cross-domain layer that preserves the bounded two-domain policy and fail-closed routing | `COMPONENT_CATALOG.md` row `CC-025`; `HUMAN_THINKING_TARGET.md`; `TRACE_CONTRACT.md` |
| audience-aware explanation quality | `NORTH_STAR_LANGUAGE_TARGET.md`, approved Phase 7 anti-generic-filler surface, and v2 answer-composer adaptation heuristics | `rebuild_clean` | the donor has useful tone and adaptation cues, but AGIFCore needs a stricter, typed audience profile layer that stays clear, bounded, honest, and non-persuasive. This should be rebuilt on top of approved Phase 7 and 8 outputs | `HUMAN_THINKING_TARGET.md`; `TRACE_CONTRACT.md`; `RUNTIME_REBUILD_MAP.md` row `RRM-006` |

## 7. Rich-expression boundary rules

### What belongs in teaching only

- structure already-supported material into a bounded lesson shape
- expose prerequisites, ordered steps, likely misconceptions, and what to inspect next
- keep language simpler when the audience profile calls for it
- no new evidence acquisition, no support-state upgrade, and no hidden analogy generation

### What belongs in comparison only

- choose bounded comparison axes
- state shared structure, differences, limits of the comparison, and where the support is asymmetric
- keep axis count bounded and trace-linked
- no action checklist, no composition trace generation, and no unsupported scoring theater

### What belongs in planning only

- turn already-supported information into a bounded step list, checklist, or sequence
- preserve stop points, dependencies, verification steps, and rollback or caution markers when supported
- keep step counts bounded and inspectable
- no runtime activation orchestration, no strategy-journal writing, and no task execution

### What belongs in synthesis only

- combine multiple already-supported inputs into one bounded reading
- preserve input refs, missing support, and unresolved conflicts
- remain faithful to support-state honesty and Phase 8 uncertainty
- no hidden evidence laundering, no fresh causal claim generation, and no support upgrade

### What belongs in analogy only

- build explicit source-to-target mapping records
- state where the analogy helps, where it breaks, and what it does not prove
- preserve an inspectable analogy trace
- no analogy as decoration, no correctness-by-metaphor, and no unsupported emotional framing

### What belongs in concept composition only

- combine a small bounded set of concepts into one composite explanation or view
- preserve explicit composition inputs and one visible composition trace
- enforce element-count ceilings and fail closed when the composition is unsupported
- no unbounded concept chaining and no invisible composition logic

### What belongs in cross-domain composition only

- relate exactly two supported domains through one bounded shared pattern unless a later re-plan explicitly widens the policy
- preserve domain refs, shared pattern, boundary notes, and fail-closed reasons
- keep the composition honest when one domain is under-supported
- no three-domain expansion by default and no pretending the shared pattern is broader than the evidence allows

### What belongs in audience-aware explanation quality only

- choose terminology density, section ordering, brevity, and cueing based on an explicit bounded audience profile
- keep responses clear, concise, honest, bounded, and free of filler
- preserve uncertainty statements instead of smoothing them away
- no persuasion engine, no rhetoric optimization for compliance, and no suppression of caveats

### What is explicitly forbidden to leak in from Phase 10 meta-cognition behavior

- self-model runtime records
- meta-cognition observer logic
- skeptic or counterexample loops
- thinker tissue outputs
- surprise-engine control loops
- strategy journal entries
- attention redirect loops
- any hidden critique loop that evaluates or rewrites the answer outside the declared Phase 9 surfaces

### What is explicitly forbidden to leak in from Phase 11 self-improvement behavior

- proposal generation or proposal adoption loops
- automatic self-editing of phase boundaries or policies
- autonomous benchmark-driven model or prompt evolution
- automatic structural growth or runtime self-reconfiguration
- autonomous phase advancement or closure behavior
- any closed-loop improvement path that changes AGIFCore behavior without separate governed approval

### How Phase 9 stays separate from Phase 7 conversation execution except through allowed interfaces

Allowed Phase 7 inputs:

- `agifcore.phase_07.raw_text_intake.v1`
- `agifcore.phase_07.question_interpretation.v1`
- `agifcore.phase_07.support_state_logic.v1`
- `agifcore.phase_07.utterance_plan.v1`
- `agifcore.phase_07.answer_contract.v1`
- `agifcore.phase_07.anti_generic_filler.v1` for bounded anti-filler compatibility only

Rules for those inputs:

- they are read-only inputs only
- Phase 9 may use them to understand discourse intent, support-state honesty, utterance shape, and baseline anti-generic expectations
- Phase 9 may not mutate support state, next action, discourse mode, or final answer mode
- Phase 9 may not own the final Phase 7 answer envelope

Forbidden Phase 7 interactions:

- direct mutation of Phase 7 runtime state
- rewriting the answer contract as if Phase 7 had already changed
- upgrading `search_needed`, `unknown`, or `abstain` without new bounded support from approved lower layers
- collapsing Phase 9 and Phase 7 into one opaque response engine

### How Phase 9 stays separate from Phase 8 science/world-awareness execution except through allowed interfaces

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
- Phase 9 may express, compare, teach, plan from, synthesize, or analogize over them
- Phase 9 may not rerun priors, region selection, causal-chain reasoning, current-world honesty, or science reflection
- Phase 9 may not reinterpret Phase 8 uncertainty as stronger support than Phase 8 declared

Forbidden Phase 8 interactions:

- direct mutation of Phase 8 runtime state
- rerunning or replacing science/world-awareness logic inside Phase 9
- using language polish to erase bounded current-world limits
- treating visible reasoning summaries as hidden chain-of-thought input rather than public evidence-linked summary

### Phase 9 compatibility decision for inherited trace refs

- Because Phase 1 keeps `concept_composition_ref`, `analogy_trace_ref`, `revision_trace_ref`, `consolidation_trace_ref`, and `reorganization_trace_ref` visible while the live Phase 7 runtime does not yet expose them as active fields, Phase 9 should later define a supplemental Phase 9 overlay contract rather than silently mutating earlier phase truth.
- The later default envelope should therefore be a new Phase 9 turn record layered above approved Phase 7 and Phase 8 snapshots and carrying Phase 9 trace refs explicitly.

## 8. Phase 9 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max teaching-structure section count | `<= 6` sections | stop and tighten teaching structure if later execution needs more than `6` sections |
| max comparison axis count | `<= 5` axes | stop and tighten comparison if later execution needs more than `5` axes |
| max planning-step count | `<= 10` steps | stop and split the plan or reopen planning if later execution needs more than `10` steps |
| max synthesis input set size | `<= 12` inputs | stop and tighten synthesis input selection if later execution needs more than `12` bounded inputs |
| max analogy count per response | `<= 2` analogies | stop and reduce analogy fan-out if later execution needs more than `2` analogies |
| max concept-composition element count | `<= 6` elements | stop and reduce composition breadth if later execution needs more than `6` elements |
| max cross-domain composition element count | `<= 4` elements | stop and reopen composition policy if later execution needs broader multi-domain blending |
| max audience-profile branch count | `<= 4` branches | stop and reduce audience branching if later execution exceeds `4` profiles in one turn |
| max Phase 9 evidence and demo bundle size | `<= 96 MiB` | stop and reorganize outputs if the bundle exceeds `96 MiB` |

Budget rules:

- these are laptop-profile planning ceilings only
- later execution must measure against them directly
- any ceiling breach must stop and escalate instead of widening silently
- any later need for higher ceilings requires reopening planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `.codex/config.toml` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | admin control files and this setup spec | future governed multi-agent runs | project-scoped agent routing exists |
| `.codex/agents/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | model manifest, tool matrix, and this setup spec | future role-separated runs | one narrow agent file per required role |
| `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2 to 8 baselines, requirements pack, design pack, admin controls, and donor inspection | all later Phase 9 work | section-complete Phase 9 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, and the Phase 9 plan | all later valid Phase 9 work | one planning task card per active role |
| `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/` | `World & Conversation Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 2 to 8 surfaces, Phase 9 plan, provenance package, and trace contract | later Phase 9 runtime delivery | runtime family exists and matches the plan |
| `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/` | `World & Conversation Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | same as above plus the exact module breakdown from this plan | later Phase 9 runtime delivery | teaching, comparison, planning, synthesis, analogy, composition, audience-quality, and turn modules exist |
| `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 9 plan, execution family, validation protocol, and demo protocol | later verification and closeout | verifier family exists and runs |
| `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifier outputs, runtime snapshots, and demo traces | audit, governor verification, and validation | machine-readable evidence bundle is inspectable |
| `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, and validation protocol | user review | rich-expression and non-generic chat-quality demo bundle exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_EXECUTION_START_BRIEF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 9 plan and admin controls | later execution start | execution scope, file families, and no-approval status are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, rerun verifiers, demo bundle, and evidence bundle | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdict request are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| custom-agent setup | define the reusable project-scoped agent package for future phases | `Program Governor` | `Constitution Keeper`, `Validation Agent` | `.codex/config.toml` spec and eight agent-file specs | admin control stack reviewed | setup package is decision-complete and role-safe |
| phase control and prerequisite reconciliation | lock phase truth, role activation, and closure chain | `Program Governor` | `Constitution Keeper` | prerequisite record and integrated Phase 9 plan | Phase 8 is explicitly approved | roles are fixed and scope is locked |
| teaching and comparison boundary framing | define the teaching and comparison lanes separately | `Architecture & Contract Lead` | `Source Cartographer`, `Constitution Keeper` | boundary rules and future module targets for `teaching.py` and `comparison.py` | reuse map exists | teaching and comparison are explicit, bounded, and non-generic |
| planning and synthesis planning | define bounded step-structure and bounded multi-input synthesis | `World & Conversation Pod Lead` | `Architecture & Contract Lead`, `Source Cartographer` | future module targets for `planning.py` and `synthesis.py` | boundary rules are stable | planning and synthesis stay separate and trace-linked |
| analogy and composition planning | define analogy, concept composition, and cross-domain composition with bounded trace surfaces | `World & Conversation Pod Lead` | `Architecture & Contract Lead`, `Source Cartographer`, `Memory & Graph Pod Lead` consult-only | future module targets for `analogy.py`, `concept_composition.py`, and `cross_domain_composition.py` | reuse map and boundaries are stable | analogy and composition are explicit, bounded, and fail closed |
| audience-aware explanation planning | define bounded audience adaptation without persuasion drift | `Architecture & Contract Lead` | `Constitution Keeper`, `World & Conversation Pod Lead` | future module target for `audience_aware_explanation_quality.py` | baseline expression boundaries are stable | audience adaptation is explicit, honest, and non-persuasive |
| test, demo, validation, and evidence planning | define verifier family, evidence reports, demo bundle, audit path, and validation path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | verifier plan, evidence plan, demo plan, and validation surfaces | runtime-family targets are stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. `Program Governor` verifies Phase 8 approval truth and confirms Phase 9 remains `open`.
2. `Program Governor` defines the custom-agent setup package but does not use those agents in the same planning run.
3. `Source Cartographer` maps all required Phase 9 subsystems to source basis and one allowed disposition.
4. `Architecture & Contract Lead` drafts subsystem boundaries, allowed Phase 7 and 8 interfaces, and forbidden Phase 10 and 11 leaks.
5. `World & Conversation Pod Lead` drafts teaching, comparison, planning, synthesis, analogy, composition, and audience-quality runtime-family decomposition after the first-pass reuse map and boundary rules exist.
6. `Constitution Keeper` reviews the first-pass reuse map and boundary rules for persuasion drift, support laundering, and Phase 10 or 11 leakage.
7. If a Phase 2 seam is ambiguous, `Kernel Pod Lead` is consulted narrowly and remains non-authoring.
8. If a Phase 4 or Phase 5 seam is ambiguous, `Memory & Graph Pod Lead` is consulted narrowly and remains non-authoring.
9. If a runtime-shell or output-format seam is ambiguous, `Product & Sandbox Pod Lead` is consulted narrowly and remains non-authoring.
10. `Test & Replay Lead` and `Release & Evidence Lead` define verifier, evidence, and demo families after the runtime-family targets are stable.
11. `Program Governor` consolidates the plan, task-card set, artifact matrix, budget envelope, and closure map.
12. `Anti-Shortcut Auditor` audits the full planning package.
13. `Program Governor` independently re-reads the cited files directly and verifies the package.
14. `Validation Agent` prepares the later review request only after audit and governor verification exist.
15. User review happens only after the validated planning package exists.

Safe parallelism:

- `Source Cartographer` and `Architecture & Contract Lead` may work in parallel on disjoint planning outputs.
- `World & Conversation Pod Lead` waits for the first-pass reuse and boundary outputs before locking the runtime family.
- `Test & Replay Lead` and `Release & Evidence Lead` wait for stable runtime-family targets.
- `Merge Arbiter` remains inactive in planning-only work.

## 12. Detailed task cards

### `P9-TC-PG-01`

- task card ID: `P9-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, custom-agent setup spec, the Phase 9 plan, task-card map, artifact matrix, budget envelope, and closure chain
- exact files allowed to touch:
  - `.codex/config.toml`
  - `.codex/agents/constitution_guard.toml`
  - `.codex/agents/source_cartographer.toml`
  - `.codex/agents/architecture_contract.toml`
  - `.codex/agents/phase_builder.toml`
  - `.codex/agents/test_replay.toml`
  - `.codex/agents/anti_shortcut_auditor.toml`
  - `.codex/agents/validation_agent.toml`
  - `.codex/agents/release_evidence.toml`
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-PG-01_PHASE_9_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 10 and later artifacts
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - earlier phase-truth files except to report a prerequisite mismatch
- required reads first:
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 to 8 plans and execution surfaces
  - relevant requirement and design files
  - admin control stack
- step-by-step work method:
  1. verify Phase 8 approval truth
  2. lock active, consult-only, and inactive roles
  3. define the custom-agent setup package without using those agents yet
  4. consolidate reuse, boundary, runtime-family, verifier, and demo outputs
  5. lock future artifact families and closure mapping
- required cross-checks:
  - no Phase 10 planning
  - no Phase 11 planning
  - no live external search execution
  - no approval language
  - do not use the custom agents in this planning run
- exit criteria:
  - the setup package and the plan are section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation, closure, or approval
- explicit proof that no approval is implied: this task ends at plan readiness only; Phase 9 remains `open`

### `P9-TC-CK-01`

- task card ID: `P9-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4 mini`
- objective: guard constitution, falsification honesty, and Phase 9 boundary discipline
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-CK-01_PHASE_9_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md`
  - `projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - Phase 9 draft
- step-by-step work method:
  1. check that Phase 9 stays below Phase 10 and Phase 11
  2. check that audience adaptation stays clarity-oriented rather than persuasive
  3. check that synthesis and comparison preserve support-state honesty
  4. report any drift to `Program Governor`
- required cross-checks:
  - no hidden-model loophole
  - no fake support strength
  - no persuasion engine
  - no Phase 10 or 11 behavior
  - no approval language
- exit criteria:
  - constitutional objections are resolved or explicitly raised as blockers
- handoff target: `Program Governor`
- anti-drift rule: do not author architecture or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P9-TC-SC-01`

- task card ID: `P9-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4 mini`
- objective: map every major Phase 9 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-SC-01_PHASE_9_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 7 and Phase 8 plans and execution surfaces
  - inspected donor Phase 9 and rich-expression source files
- step-by-step work method:
  1. map teaching, comparison, planning, synthesis, analogy, concept composition, cross-domain composition, and audience-aware explanation quality
  2. assign one allowed disposition to each subsystem
  3. flag where exact trace-carrier inheritance is stronger than runtime-code portability
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

### `P9-TC-ACL-01`

- task card ID: `P9-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 9 boundaries, allowed interfaces, forbidden leaks, and the Phase 9 overlay-contract strategy
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-ACL-01_PHASE_9_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 7 and Phase 8 plans
  - `Source Cartographer` output
- step-by-step work method:
  1. define what belongs in each Phase 9 subsystem only
  2. define allowed Phase 7 and Phase 8 interfaces
  3. define the supplemental Phase 9 overlay-contract strategy for inherited trace refs
  4. define forbidden Phase 10 and 11 leaks
  5. pass runtime-family implications to `Program Governor` and `World & Conversation Pod Lead`
- required cross-checks:
  - no one mixed style engine
  - no final response-envelope ownership inside Phase 9
  - no direct mutation of Phase 7 or Phase 8 state
  - no persuasion theater disguised as audience adaptation
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `World & Conversation Pod Lead`
- anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, or the team
- explicit proof that no approval is implied: boundary framing is planning truth only

### `P9-TC-WCPL-01`

- task card ID: `P9-TC-WCPL-01`
- role owner: `World & Conversation Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 9 runtime family without crossing into Phase 10 or 11
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-WCPL-01_PHASE_9_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - approved Phase 2 to 8 plans and execution surfaces
  - Phase 9 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
- step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/agifcore_phase9_rich_expression/`
  2. keep the module set explicit:
     - `contracts.py`
     - `teaching.py`
     - `comparison.py`
     - `planning.py`
     - `synthesis.py`
     - `analogy.py`
     - `concept_composition.py`
     - `cross_domain_composition.py`
     - `audience_aware_explanation_quality.py`
     - `rich_expression_turn.py`
  3. order module implementation so contracts come first, then teaching/comparison, then planning/synthesis, then analogy/composition, then audience-quality, and the thin coordinator last
  4. identify where Phase 7 and Phase 8 exports must be consumed read-only
- required cross-checks:
  - no runtime code written now
  - no Phase 10 behavior
  - no Phase 11 behavior
  - no live search execution
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase

### `P9-TC-TRL-01`

- task card ID: `P9-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4 mini`
- objective: define the Phase 9 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-TRL-01_PHASE_9_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 8 verifier and evidence families
  - Phase 9 draft
- step-by-step work method:
  1. define one verifier per major Phase 9 subsystem
  2. define cross-cutting anti-shortcut and non-generic quality checks
  3. define evidence reports and manifest contents
  4. define failure signatures for each closure requirement
- required cross-checks:
  - tests must verify separation between teaching, comparison, planning, synthesis, analogy, composition, and audience-quality
  - analogy and composition outputs must have machine-checkable trace refs
  - synthesis must preserve support-state honesty
  - audience-aware explanation quality must stay clarity-oriented rather than persuasive
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P9-TC-ASA-01`

- task card ID: `P9-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4 mini`
- objective: audit the Phase 9 planning package for fake completeness, greenfield recreation, and style-engine collapse
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-ASA-01_PHASE_9_PLAN_AUDIT.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - full Phase 9 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `Test & Replay Lead` evidence-plan output
  - relevant approved Phase 7 and Phase 8 plans
- step-by-step work method:
  1. check that all required sections exist
  2. check that each major subsystem has a source basis and disposition
  3. check that no one giant style engine is being passed off as design
  4. check that no approval or completion claim is implied
- required cross-checks:
  - no blind rewrite where a plausible substrate exists
  - no silent omission of analogy, concept composition, cross-domain composition, or audience-quality
  - no Phase 10 or Phase 11 behavior smuggled in
  - no empty report path or unverifiable demo plan
- exit criteria:
  - all blockers are either cleared or explicitly raised
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P9-TC-VA-01`

- task card ID: `P9-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 9 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-VA-01_PHASE_9_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - full Phase 9 draft
  - audit output
  - governor verification output
  - validation protocol
- step-by-step work method:
  1. confirm the plan is decision-complete
  2. confirm every closure requirement has a later artifact path
  3. confirm the later demos are inspectable and truthful
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

### `P9-TC-REL-01`

- task card ID: `P9-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4 mini`
- objective: define the later Phase 9 demo-bundle shape and review packet surfaces
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-REL-01_PHASE_9_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 10 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 8 demo bundle
  - `Test & Replay Lead` verifier and evidence plan
  - Phase 9 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the rich-expression demo surface
  3. define the non-generic chat-quality demo surface
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
| teaching exists | `teaching.py`, `verify_phase_09_teaching.py`, `phase_09_teaching_report.json` | `World & Conversation Pod Lead` | verifier confirms bounded sectioning, prerequisite markers, and support-linked teaching structure | generic explanation text with no typed teaching structure |
| comparison exists | `comparison.py`, `verify_phase_09_comparison.py`, `phase_09_comparison_report.json` | `World & Conversation Pod Lead` | verifier confirms explicit axes, asymmetry handling, and trace-linked comparison notes | vague “X and Y are different” text with no axes |
| planning exists | `planning.py`, `verify_phase_09_planning.py`, `phase_09_planning_report.json` | `World & Conversation Pod Lead` | verifier confirms bounded step lists, stop points, and verification cues | free-form advice with no typed steps or checks |
| synthesis exists | `synthesis.py`, `verify_phase_09_synthesis.py`, `phase_09_synthesis_report.json` | `World & Conversation Pod Lead` | verifier confirms multi-input trace preservation and unresolved-conflict surfacing | a fluent summary that hides input gaps or conflicts |
| analogy exists | `analogy.py`, `verify_phase_09_analogy.py`, `phase_09_analogy_report.json` | `World & Conversation Pod Lead` | verifier confirms explicit source-target mapping, break limits, and visible `analogy_trace_ref` support | decorative metaphor with no mapping or no trace |
| concept composition exists | `concept_composition.py`, `verify_phase_09_concept_composition.py`, `phase_09_concept_composition_report.json` | `World & Conversation Pod Lead` | verifier confirms bounded element counts, composition trace, and fail-closed behavior | concept blending with no visible `concept_composition_ref` or boundary rules |
| cross-domain composition exists | `cross_domain_composition.py`, `verify_phase_09_cross_domain_composition.py`, `phase_09_cross_domain_composition_report.json` | `World & Conversation Pod Lead` | verifier confirms exactly-two-domain default policy, shared pattern visibility, and honest fail-closed routing | unsupported three-domain blending or fake shared-pattern claims |
| audience-aware explanation quality exists | `audience_aware_explanation_quality.py`, `verify_phase_09_audience_aware_explanation_quality.py`, `phase_09_audience_aware_explanation_quality_report.json` | `World & Conversation Pod Lead` | verifier confirms bounded audience profiles, anti-filler behavior, and no persuasion drift | style-only rewriting that suppresses uncertainty or pushes compliance |
| demo path exists | `phase_09_demo_index.md`, `phase_09_rich_expression_demo.md`, `phase_09_non_generic_chat_quality_demo.md` plus matching `.json` outputs | `Release & Evidence Lead` | direct demo-bundle inspection and rerunnable demo scripts | no inspectable demo or demo claims unsupported by evidence |
| tests/evidence path exists | full verifier family under `05_testing/phase_09_rich_expression_and_composition/` and `phase_09_evidence_manifest.json` | `Test & Replay Lead` | governor rerun plus validation request | missing verifier coverage, missing manifest, or non-machine-readable evidence |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| rich-expression demo | teaching, comparison, planning, synthesis, analogy, concept composition, cross-domain composition, audience-quality modules, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `World & Conversation Pod Lead` | `Anti-Shortcut Auditor` | original prompt, selected Phase 7 and 8 input states, active expression lane, trace refs, public result text, and backing evidence reports |
| non-generic chat-quality demo | audience-aware explanation quality, anti-generic quality verifier, synthesis or teaching lane as appropriate, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `World & Conversation Pod Lead` | `Anti-Shortcut Auditor` | the raw prompt, support-state honesty, audience profile chosen, anti-filler checks, non-generic text evidence, and proof that no unsupported fluency replaced support |

Validation rules for both demos:

- `Validation Agent` prepares the review request only after audit and governor verification exist.
- `Program Governor` is the only role that asks the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable rich-expression substrate | compare subsystem plans and later runtime against mapped donor files and exact trace-carrier inheritance | `Source Cartographer` | a subsystem is rebuilt from zero despite a clear donor basis or exact inherited trace surface | stop and reopen reuse mapping before execution |
| one giant style engine pretending to do teaching, comparison, planning, synthesis, analogy, and composition | boundary audit and verifier-plan audit | `Architecture & Contract Lead` | a single opaque module is asked to own most Phase 9 behavior | reject the design and split the lanes before continuing |
| audience-aware explanation quality becoming persuasion instead of clarity | constitution review and later verifier checks | `Constitution Keeper` | language adaptation smooths away uncertainty, pushes agreement, or hides weak support | stop and tighten audience-quality rules |
| analogy becoming unsupported decoration | analogy verifier and demo audit | `Anti-Shortcut Auditor` | analogy text appears without explicit source-target mapping or trace | block closure until analogy trace behavior is real |
| synthesis bypassing evidence and support-state honesty | synthesis verifier and governor rerun | `Constitution Keeper` | synthesis output is stronger than the incoming support state or hides conflicts | stop and force honest synthesis rules |
| Phase 9 accidentally absorbing Phase 10 meta-cognition behavior | boundary audit against the forbidden Phase 10 list | `Constitution Keeper` | self-model, skeptic loop, thinker tissue, or meta-observer behavior appears in Phase 9 | stop and remove the meta-cognition dependency |
| Phase 9 accidentally absorbing Phase 11 self-improvement behavior | boundary audit against the forbidden Phase 11 list | `Constitution Keeper` | proposal generation, self-editing loops, or autonomous improvement behavior appears in Phase 9 | stop and remove the self-improvement dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 9 plan artifacts
- after user approval, any future change to the Phase 9 plan requires explicit reopen instruction and a supersession note

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 8 is explicitly `approved` in the live phase-truth files and corroborated by the decision and changelog records.
- Phase 9 remains `open`.
- The required provenance stack, approved Phase 2 through 8 baselines, requirements pack, design pack, admin controls, and donor substrate were all reviewed directly.
- No prerequisite blocker was found.
- The main non-blocker seam is the inherited Phase 9 trace-carrier compatibility gap in the live Phase 7 runtime, and this plan addresses it through a Phase 9 overlay-contract strategy rather than by silently rewriting earlier phase truth.
- Defaults locked by this draft:
  - later execution keeps one active build pod by default: `World & Conversation Pod Lead`
  - teaching, comparison, planning, synthesis, cross-domain composition, and audience-aware explanation quality default toward `rebuild_clean`
  - analogy and concept composition default toward `port_with_provenance` for exact trace and policy substrate, with AGIFCore-specific runtime rebinding
  - Phase 9 remains a read-only rich-expression layer above approved Phase 7 and Phase 8 outputs and below Phase 10 and Phase 11 behavior
