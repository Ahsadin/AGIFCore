# Phase 11: Governed Self-Improvement

Brief summary:

Phase 11 plans the governed self-improvement layer that sits above approved Phase 10 meta-cognition and critique outputs and below Phase 12 structural growth and Phase 13 product runtime. It must later produce inspectable reflection, proposal, experiment, measurement, adoption, monitoring, rollback, and bounded self-initiated inquiry surfaces without leaking into structural growth or product-runtime behavior.

Planned interface additions for later execution:

- a new runtime family under `projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/`
- a thin coordinator snapshot `agifcore.phase_11.self_improvement_cycle.v1`
- per-subsystem schemas:
  - `agifcore.phase_11.offline_reflection_and_consolidation.v1`
  - `agifcore.phase_11.idle_reflection.v1`
  - `agifcore.phase_11.proposal_generation.v1`
  - `agifcore.phase_11.self_experiment_lab.v1`
  - `agifcore.phase_11.shadow_evaluation.v1`
  - `agifcore.phase_11.before_after_measurement.v1`
  - `agifcore.phase_11.adoption_or_rejection_pipeline.v1`
  - `agifcore.phase_11.post_adoption_monitoring.v1`
  - `agifcore.phase_11.rollback_proof.v1`
  - `agifcore.phase_11.thought_episodes.v1`
  - `agifcore.phase_11.self_initiated_inquiry_engine.v1`

Planning defaults chosen:

- later execution keeps one active build pod by default: `Meta & Growth Pod Lead`
- later execution must include one extra audit pass, stronger Governor review, and one additional human demo checkpoint because self-improvement and self-initiated inquiry behavior are inside the Meta & Growth danger zone
- the existing project-scoped `.codex` setup is reusable; the only setup tightening applied in this planning pass is that `phase_builder` now explicitly names `Meta & Growth Pod Lead` in `developer_instructions`

## 1. Phase identity

- Phase number: `11`
- Canonical phase name: `Governed Self-Improvement`
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
  - `projects/agifcore_master/01_plan/PHASE_10_META_COGNITION_AND_CRITIQUE.md`
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
  - approved Phase 2 through Phase 10 execution, testing, and output surfaces under `projects/agifcore_master/04_execution/`, `projects/agifcore_master/05_testing/`, and `projects/agifcore_master/06_outputs/`
  - admin control files under `projects/agifcore_master/00_admin/`
  - project-scoped custom agent setup under `.codex/config.toml` and `.codex/agents/`
  - direct donor inspection from `agif_fabric_v1`, `agif-tasklet-cell`, root v2 lineage, and `agif_v2_master`, with direct focus on old Phase 9 idle reflection, old Phase 8B shadow-evaluation and adoption rules, old Phase 8C governed structural-growth contracts/runtime, and current AGIFCore Phase 10 runtime surfaces

## 2. Phase mission

- Phase 11 exists to define and later build the governed self-improvement layer that can review past failures, generate bounded proposals, test them safely, measure them honestly, adopt or reject them under governance, monitor them after adoption, prove rollback, and run bounded self-initiated inquiry without becoming uncontrolled autonomy.
- Phase 11 must later build:
  - offline reflection and consolidation
  - idle reflection
  - proposal generation
  - self-experiment lab
  - shadow evaluation
  - before/after measurement
  - adoption or rejection pipeline
  - post-adoption monitoring
  - rollback proof
  - thought episodes
  - self-initiated inquiry engine
- Phase 11 must not:
  - implement Phase 12 structural growth behavior
  - implement Phase 13 product-runtime behavior
  - re-implement Phase 2 fabric control, Phase 4 memory policy, Phase 5 graph policy, Phase 6 simulator logic, Phase 7 conversation execution, Phase 8 science/world reasoning, Phase 9 rich expression, or Phase 10 critique itself
  - turn proposals into hidden self-approval
  - turn measurement into prose-only claims
  - turn rollback into a promise with no proved roundtrip
  - execute live external search
  - bypass support-state honesty
  - claim historical v1, tasklet, root v2, or v2 packages as earned AGIFCore completion
  - imply commit, freeze, approval, or closure

## 3. Scope and non-goals

- In-scope artifacts:
  - the canonical Phase 11 plan
  - Phase 11 planning task cards
  - self-improvement boundary rules
  - reuse and provenance decisions for each major subsystem
  - future execution, testing, output, and handoff targets
  - later demo, validation, and closure planning
- Out-of-scope work:
  - any Phase 11 runtime code
  - any Phase 11 verifier code
  - any Phase 11 evidence generation
  - any Phase 12 planning
  - any Phase 13 planning
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
- Explicit untouched-later-phase statement:
  - Phase 12 and all later phases remain untouched by this plan.

## 4. Phase 10 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 10 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` show Phase 10 `approved` and Phase 11 `open` | Phase 11 planning may proceed |
| Explicit Phase 10 closeout truth exists outside index tables | `pass` | `projects/agifcore_master/DECISIONS.md` and `projects/agifcore_master/CHANGELOG.md` confirm Phase 10 approval and that Phase 11 has not started | no silent approval assumption |
| Required Phase 1 provenance artifacts relied on exist | `pass` | `HUMAN_THINKING_TARGET.md`, `COMPONENT_CATALOG.md`, `SOURCE_INHERITANCE_MATRIX.md`, `RUNTIME_REBUILD_MAP.md`, `TRACE_CONTRACT.md`, `VALIDATION_PROTOCOL.md`, and `DEMO_PROTOCOL.md` are present | provenance and closure framing exist |
| Required Phase 2 through 10 artifacts relied on exist | `pass` | approved plans and approved execution/testing/output families for Phases 2 through 10 are present | runtime seams and honesty seams are inspectable |
| Dependency gap: canonical Phase 11 plan file is not present yet | `non-blocker` | `projects/agifcore_master/01_plan/PHASE_11_GOVERNED_SELF_IMPROVEMENT.md` was missing and is the target of this planning run | expected planning target |
| Dependency gap: Phase 11 planning task folder is not present yet | `non-blocker` | `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/` was missing and is the target of this planning run | expected planning target |
| Compatibility seam: AGIFCore has no Phase 11 overlay contract yet | `non-blocker` | approved Phase 10 exposes an overlay contract and typed self-model, observer, journal, thinker-tissue, theory-fragment, and diagnosis refs, but no approved Phase 11 cycle schema exists yet | Phase 11 must define a new overlay above Phase 10 instead of mutating lower-phase truth |
| Compatibility seam: strongest idle-reflection and adoption substrate is donor-side only | `non-blocker` | the strongest substrate is in old Phase 9 idle-reflection and old 8B/8C adoption work, not in approved AGIFCore runtime | Phase 11 must separate reusable record logic from old mixed runtime orchestration |
| Blockers vs non-blockers | `planning not blocked` | all prerequisite approvals and planning inputs exist | readiness may be `ready_for_user_review` |

## 5. Active team map for Phase 11

Later Phase 11 execution default build pod: `Meta & Growth Pod Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | What it must never do this phase |
| --- | --- | --- | --- | --- | --- |
| `Program Governor` | `gpt-5.4` | active | prerequisite truth, danger-zone control, and final integration are required | own prerequisite truth, custom-agent setup verification, role activation, plan integration, artifact matrix, closure map, and final readiness judgment | implement runtime code, validate its own authored artifacts, or broaden into Phase 12 or 13 |
| `Constitution Keeper` | `gpt-5.4-mini` | active | Phase 11 can drift into uncontrolled autonomy, hidden self-approval, or product/runtime leakage | guard constitution, honesty, weak-support visibility, no-hidden-model rules, and phase boundaries | author runtime design alone, approve the phase, or allow Phase 12 or 13 leakage |
| `Source Cartographer` | `gpt-5.4-mini` | active | donor self-improvement substrate is real but uneven and must not be rebuilt blindly | map each subsystem to donor basis, disposition, and reuse limits | invent a fifth disposition, treat historical code as earned completion, or approve the phase |
| `Architecture & Contract Lead` | `gpt-5.4` | active | Phase 11 needs strict self-improvement boundaries above approved Phase 10 surfaces | own subsystem boundaries, allowed interfaces, forbidden leaks, and the Phase 11 overlay-contract strategy | redesign earlier phases, collapse all self-improvement into one giant engine, or approve the phase |
| `Kernel Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 2 seam becomes ambiguous | consult on workspace, replay-anchor, scheduler, rollback, or quarantine seams only if ambiguity appears | author the plan, implement code, or broaden Phase 2 |
| `Memory & Graph Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if Phase 4 or 5 persistence seams become ambiguous | consult on continuity memory, theory-fragment persistence, graph provenance, or retention seams only if ambiguity appears | author the plan, implement code, or pull Phase 11 down into memory or graph layers |
| `World & Conversation Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 7, 8, 9, or 10 seam becomes ambiguous | consult on conversation, science-world, rich-expression, or critique input seams only if ambiguity appears | author the plan, implement code, or absorb Phase 11 into lower phases |
| `Meta & Growth Pod Lead` | `gpt-5.3-codex` | active | later execution owner and danger-zone build pod for Phase 11 | decompose the future runtime family for reflection, proposals, experiments, measurement, adoption, monitoring, rollback proof, thought episodes, and bounded inquiry | author canonical plan truth alone, implement code in this run, or absorb Phase 12 or 13 scope |
| `Product & Sandbox Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if runtime-shell or export seams become ambiguous | consult on runner-shell, packaging, or export-format seams only if ambiguity appears | author the plan, implement product work, or broaden scope |
| `Test & Replay Lead` | `gpt-5.4-mini` | active | self-improvement must be test-planned from the start | define verifier family, evidence expectations, danger-zone audit hooks, and closure failure signatures | implement runtime logic, fake reports, or approve the phase |
| `Anti-Shortcut Auditor` | `gpt-5.4-mini` | active | Phase 11 has the highest risk of fake autonomy, fake measurement, and fake rollback | audit for fake completeness, giant-engine collapse, unsupported proposals, prose-only measurement, fake rollback, and unverifiable demos | rewrite the plan instead of auditing it, downgrade blockers casually, or approve the phase |
| `Merge Arbiter` | `gpt-5.3-codex` | inactive | planning-only run | none | imply closure or perform merge work |
| `Validation Agent` | `gpt-5.4` | active | final machine-side review of the planning package is required before user review | validate the plan package after audit and Governor verification exist | author the plan, implement runtime, or approve the phase |
| `Release & Evidence Lead` | `gpt-5.4-mini` | active | later self-improvement demos must be inspectable and evidence-linked | define demo-bundle shape, review packet surfaces, and later demo ordering | implement runtime behavior, publish release material, or imply acceptance |

## 6. Reuse and provenance strategy

Only the frozen four disposition categories are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance artifact justification |
| --- | --- | --- | --- | --- |
| offline reflection and consolidation | old Phase 9 `ReflectionCycleReport` / `idle_reflection.py`, `ReflectionControlLoopRecord`, and approved Phase 10 `strategy_journal`, `theory_fragments`, and `meta_cognition_turn` surfaces | `adapt_for_research_only` | the donor cycle is real, but it is tightly coupled to old answer-composer flags and bounded historical review packs; AGIFCore should adapt the cycle semantics and rebuild the actual Phase 11 coordinator above approved Phase 10 traces | `COMPONENT_CATALOG.md` row `CC-018`; `RUNTIME_REBUILD_MAP.md` row `RRM-007`; `TRACE_CONTRACT.md` |
| idle reflection | old Phase 9 explicit idle entrypoint and normal-turn idle-audit split, `ReflectionControlLoopRecord`, and approved Phase 10 overlay refs | `adapt_for_research_only` | the explicit idle-entrypoint pattern is strong donor substrate, but it remains research-only in the provenance package and must not be treated as direct drop-in runtime logic | `COMPONENT_CATALOG.md` row `CC-018`; `RUNTIME_REBUILD_MAP.md` row `RRM-007`; `TRACE_CONTRACT.md` |
| proposal generation | `proposal_generator`, old Phase 8B allowed proposal-kind freeze, and approved Phase 10 thinker-tissue bounded proposals | `rebuild_clean` | proposal generation is a real named donor surface, but Phase 11 needs typed, governance-bound proposal records above approved Phase 10 outputs rather than a direct carry of old mixed proposal logic | `COMPONENT_CATALOG.md` row `CC-019`; `HUMAN_THINKING_TARGET.md`; `COGNITIVE_PRIORS.md` |
| self-experiment lab | old Phase 8B shadow-evaluation rules, old Phase 9 governed review packs, and v1 benchmark/evidence machinery | `rebuild_clean` | there is strong experiment substrate, but no AGIFCore-ready self-experiment module exists; AGIFCore should rebuild a held-out, deterministic, sandboxed experiment lab above approved Phase 10 outputs | `COMPONENT_CATALOG.md` rows `CC-051`, `CC-056`, and `CC-057`; `SCIENTIFIC_METHOD.md` |
| shadow evaluation | old Phase 8B `shadow_eval_report` and `held_out_delta` rules plus old Phase 8C held-out improvement reports | `adapt_for_research_only` | the donor evaluation surface is concrete and useful, but it remains proof-oriented and historical; AGIFCore should adapt the evaluation semantics while rebuilding the actual Phase 11 execution path | `SCIENTIFIC_METHOD.md`; `COMPONENT_CATALOG.md` rows `CC-051` and `CC-056` |
| before/after measurement | old Phase 9 baseline -> adopted -> rollback triplets plus v1 claims-to-evidence and reproducibility surfaces | `port_with_provenance` | the measurement carrier pattern is concrete, replayable, and audit-friendly; AGIFCore should port the measurement shape and evidence linkage with provenance and rebind it to approved Phase 10 inputs | `COMPONENT_CATALOG.md` rows `CC-051`, `CC-056`, and `CC-057`; `TRACE_CONTRACT.md` |
| adoption or rejection pipeline | old Phase 8C `AdoptionRecord`, v1 authority approvals and vetoes, and approved Phase 10 overlay refs | `port_with_provenance` | the decision-record substrate is strong enough to port, but the actual Phase 11 execution pipeline still needs AGIFCore-specific runtime rebinding and audit gates | `COMPONENT_CATALOG.md` rows `CC-049` and `CC-042`; `GOVERNANCE_MODEL.md` |
| post-adoption monitoring | old Phase 8C monitoring-plan surface, v1 soak harness and evidence machinery, and old Phase 9 repeated governed-window proof | `rebuild_clean` | the donor shows what must be monitored, but AGIFCore needs a fresh, bounded monitoring lane that is tied to approved evidence and rollback thresholds rather than historical experiment scripts | `COMPONENT_CATALOG.md` rows `CC-052` and `CC-051`; `GOVERNANCE_MODEL.md` |
| rollback proof | v1 rollback snapshots and lineage support, old Phase 9 rollback roundtrip proof, and old Phase 8C rollback-proof fields | `port_with_provenance` | rollback proof is one of the strongest portable substrates; AGIFCore should port the roundtrip-proof shape and rollback-link discipline with provenance | `COMPONENT_CATALOG.md` row `CC-042`; `SOURCE_INHERITANCE_MATRIX.md` row `SIM-006`; `TRACE_CONTRACT.md` |
| thought episodes | old Phase 8B thought episodes about reasoning quality plus approved Phase 10 strategy-journal and self-model surfaces | `adapt_for_research_only` | the donor concept is real but under-specified as a runtime module; AGIFCore should adapt the note shape and bind it to approved Phase 10 traces instead of copying historical usage | `COMPONENT_CATALOG.md` rows `CC-011`, `CC-013`, and `CC-022`; `HUMAN_THINKING_TARGET.md` |
| self-initiated inquiry engine | tasklet proactive/background agent lane, old explicit idle entrypoint rules, and approved Phase 10 thinker-tissue plus attention-redirect outputs | `adapt_for_research_only` | there is historical substrate for bounded background work, but it is explicitly research-only and too risky to port directly; AGIFCore should adapt the gating semantics and rebuild a tightly bounded inquiry engine above approved Phase 10 signals | `SOURCE_INHERITANCE_MATRIX.md` row `SIM-042`; `COMPONENT_CATALOG.md` rows `CC-047` and `CC-016`; `COGNITIVE_PRIORS.md` |

## 7. Self-improvement boundary rules

### What belongs in offline reflection and consolidation only

- batch review of completed Phase 10 traces and accepted evidence bundles
- consolidate repeated weak patterns into bounded proposal candidates
- carry forward only typed reflection outputs, not live behavior changes
- no ordinary-turn execution and no silent runtime mutation

### What belongs in idle reflection only

- explicit idle-entrypoint review of a bounded pending queue
- preserve the distinction between `idle cycle ran` and `idle cycle did not run`
- produce one bounded reflection-cycle output per governed cycle
- no always-on autonomous background learning

### What belongs in proposal generation only

- emit typed proposals with target, rationale, expected gain, falsifier, evidence needed, and rollback target
- keep proposal count bounded per cycle
- stay recommendation-only until later stages clear adoption
- no direct adoption and no runtime code authoring

### What belongs in self-experiment lab only

- run sandboxed, deterministic, held-out experiments on bounded proposals
- use replayable packs and explicit evaluation fixtures
- preserve experiment provenance and exact candidate/baseline separation
- no live adoption, no external-search dependency, and no silent data mutation

### What belongs in shadow evaluation only

- compare baseline versus candidate in isolated form before adoption
- record delta, regressions, and uncertainty honestly
- remain non-public and non-user-facing except through evidence surfaces
- no live turn rewriting and no covert promotion to runtime truth

### What belongs in before/after measurement only

- preserve same-pack baseline, adopted, and rollback triplets
- store metrics, regressions, and pass/fail deltas in machine-readable form
- tie measurement directly to one candidate and one bounded review pack
- no decision authority and no prose-only measurement claims

### What belongs in adoption or rejection pipeline only

- take proposal, experiment, measurement, audit, and Governor gates as inputs
- record one explicit state per candidate: `adopted`, `rejected`, `held`, or `rolled_back`
- require rollback readiness before adoption
- no self-approval, no missing-evidence adoption, and no implicit fast path

### What belongs in post-adoption monitoring only

- observe adopted changes over bounded follow-up windows
- watch for regressions, rollback triggers, and stale measurement drift
- preserve a typed monitoring record and escalation path
- no new proposal invention and no silent widening of adopted scope

### What belongs in rollback proof only

- prove the candidate can roundtrip from baseline to adopted to restored baseline
- preserve rollback refs, replayability, and same-pack comparison
- fail closed if rollback cannot be demonstrated
- no “trust me” rollback claims

### What belongs in thought episodes only

- preserve compact self-improvement notes about repeated failures, attempted ideas, and falsifiers
- tie notes to real trace refs and candidate ids
- stay subordinate to strategy journal and reflection outputs
- no hidden diary, no identity narrative, and no unreviewed memory promotion

### What belongs in self-initiated inquiry engine only

- create one bounded inquiry from explicit missing-need, contradiction, or unresolved-monitoring signals
- require governance gating, budget checks, and a typed inquiry goal
- stay local, replayable, and evidence-linked
- no uncontrolled autonomy, no live external search, and no user-facing answer ownership

### What is explicitly forbidden to leak in from Phase 12 structural growth behavior

- self-model feedback-loop execution that rewrites structural state
- reflection-control-loop execution that changes tissues or manifests
- cell-family creation or deletion
- tissue creation, removal, or reorganization
- domain genesis
- theory formation beyond bounded candidate proposals
- transfer-structure growth
- runtime-substrate or manifest self-rewrite

### What is explicitly forbidden to leak in from Phase 13 product-runtime behavior

- runner/gateway/UI split changes
- local gateway endpoint design
- desktop UI behavior and presentation ownership
- installer and distribution work
- product-shell background-service behavior
- public release packaging
- product-runtime UX claims standing in for self-improvement evidence

### How Phase 11 stays separate from Phase 10 meta-cognition and critique execution except through allowed interfaces

Allowed Phase 10 inputs:

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
- `agifcore.phase_10.meta_cognition_turn.v1`
- `agifcore.phase_10.overlay_contract.v1`

Rules for those inputs:

- they are read-only inputs only
- Phase 11 may consume them to discover repeated weak patterns, candidate improvements, measurement targets, and bounded inquiry triggers
- Phase 11 may not mutate Phase 10 runtime state or pretend that critique itself adopted a change
- Phase 11 may not own direct user-facing response text or ordinary-turn answer envelopes

Forbidden Phase 10 interactions:

- direct mutation of Phase 10 runtime state
- using Phase 11 to smuggle structural growth or product-runtime work into Phase 10
- collapsing critique, proposal, experiment, adoption, and monitoring into one opaque engine
- treating self-improvement as a replacement for ordinary-turn critique honesty

## 8. Phase 11 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max offline reflection items per cycle | `<= 12` items | stop and tighten reflection intake if later execution needs more than `12` items |
| max idle reflection items per cycle | `<= 6` items | stop and reduce idle-cycle breadth if later execution exceeds `6` items |
| max proposal count per cycle | `<= 3` proposals | stop and reopen proposal policy if later execution needs more than `3` proposals |
| max self-experiment count per cycle | `<= 2` experiments | stop and reduce experiment fan-out if later execution exceeds `2` experiments |
| max shadow-evaluation count per cycle | `<= 3` evaluations | stop and tighten evaluation scope if later execution exceeds `3` evaluations |
| max before/after measurement pair count per cycle | `<= 3` pairs | stop and simplify measurement families if later execution exceeds `3` pairs |
| max adoption or rejection decisions per cycle | `<= 2` decisions | stop and reopen adoption policy if later execution needs more than `2` decisions |
| max post-adoption monitoring items per cycle | `<= 4` items | stop and tighten monitoring entry rules if later execution exceeds `4` items |
| max rollback-proof events per cycle | `<= 2` events | stop and reduce rollback fan-out if later execution exceeds `2` proof events |
| max thought-episode count per cycle | `<= 6` episodes | stop and tighten episode creation if later execution exceeds `6` notes |
| max self-initiated inquiry count per cycle | `<= 1` inquiry | stop and escalate if later execution needs more than one inquiry in the same cycle |
| max Phase 11 evidence and demo bundle size | `<= 144 MiB` | stop and reorganize outputs if the bundle exceeds `144 MiB` |

Budget rules:

- these are laptop-profile planning ceilings only
- later execution must measure against them directly
- any ceiling breach must stop and escalate instead of widening silently
- any later need for higher ceilings requires reopening planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_11_GOVERNED_SELF_IMPROVEMENT.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2 through 10 baselines, admin controls, and donor inspection | all later Phase 11 work | section-complete Phase 11 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, and the Phase 11 plan | all later valid Phase 11 work | one planning task card per active role |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_11_PLAN_FREEZE_HANDOFF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 11 plan and admin controls | later execution start | frozen scope and no-approval status are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_11_EXECUTION_START_BRIEF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 11 plan and admin controls | later execution start | execution scope, danger-zone controls, and file families are explicit |
| `projects/agifcore_master/04_execution/phase_11_governed_self_improvement/` | `Meta & Growth Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 10 surfaces, Phase 11 plan, provenance package, and trace contract | later Phase 11 runtime delivery | runtime family exists and matches the plan |
| `projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/` | `Meta & Growth Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | same as above plus exact module breakdown from this plan | later Phase 11 runtime delivery | reflection, proposal, experiment, evaluation, adoption, monitoring, rollback, episode, inquiry, and coordinator modules exist |
| `projects/agifcore_master/05_testing/phase_11_governed_self_improvement/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 11 plan, execution family, validation protocol, and demo protocol | later verification and closeout | verifier family exists and runs |
| `projects/agifcore_master/06_outputs/phase_11_governed_self_improvement/phase_11_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifier outputs, runtime snapshots, and demo traces | audit, Governor verification, and validation | machine-readable evidence bundle is inspectable |
| `projects/agifcore_master/06_outputs/phase_11_governed_self_improvement/phase_11_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, validation protocol, and additional-human-checkpoint material | user review | self-improvement, rollback, and bounded inquiry demos exist |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-AUDIT-01_PHASE_11_FINAL_PACKAGE_AUDIT_REPORT.md` | `Anti-Shortcut Auditor` | `Program Governor` | `n/a` | `Validation Agent` | runtime, tests, evidence, demos, and planning truth | Governor verification | standard final audit exists |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-AUDIT-02_PHASE_11_DANGER_ZONE_AUDIT_REPORT.md` | `Anti-Shortcut Auditor` | `Constitution Keeper` | `n/a` | `Validation Agent` | runtime, tests, evidence, demos, and Meta & Growth danger-zone controls | Governor verification | extra danger-zone audit exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_11_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, rerun verifiers, demo bundle, evidence bundle, and additional-human-checkpoint record | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_11_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdict request are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_11_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| reflection and consolidation planning | define the bounded reflection cycle and consolidation lane above Phase 10 | `Architecture & Contract Lead` | `Source Cartographer`, `Constitution Keeper`, `Meta & Growth Pod Lead` | future `contracts.py`, `offline_reflection_and_consolidation.py`, `idle_reflection.py`, and `self_improvement_cycle.py` | prerequisite truth and reuse map exist | reflection boundaries are explicit and separate from Phase 12 and 13 |
| proposal and experiment planning | define proposal-generation and sandboxed experiment behavior | `Meta & Growth Pod Lead` | `Architecture & Contract Lead`, `Source Cartographer`, `Constitution Keeper` | future `proposal_generation.py` and `self_experiment_lab.py` | reflection boundaries are stable | proposal and experiment behavior are typed, bounded, and governance-linked |
| evaluation and measurement planning | define shadow evaluation and before/after measurement behavior | `Test & Replay Lead` | `Meta & Growth Pod Lead`, `Architecture & Contract Lead`, `Source Cartographer` | future `shadow_evaluation.py` and `before_after_measurement.py` | proposal and experiment targets are stable | evaluation and measurement are machine-checkable, honest, and rollback-linked |
| adoption or rejection and monitoring planning | define governed adoption, rejection, hold, and monitoring behavior | `Architecture & Contract Lead` | `Constitution Keeper`, `Meta & Growth Pod Lead`, `Test & Replay Lead` | future `adoption_or_rejection_pipeline.py` and `post_adoption_monitoring.py` | evaluation and measurement boundaries are stable | decision states, evidence requirements, and monitoring triggers are explicit |
| rollback-proof and thought-episode planning | define rollback roundtrip proof and bounded self-improvement notes | `Meta & Growth Pod Lead` | `Architecture & Contract Lead`, `Constitution Keeper`, `Test & Replay Lead` | future `rollback_proof.py` and `thought_episodes.py` | adoption pipeline is stable | rollback proof and thought episodes are explicit, bounded, and non-theatrical |
| self-initiated inquiry planning | define bounded inquiry triggers, budgets, and allowed inquiry scope | `Architecture & Contract Lead` | `Constitution Keeper`, `Meta & Growth Pod Lead`, `World & Conversation Pod Lead` consult-only | future `self_initiated_inquiry_engine.py` | reflection and monitoring boundaries are stable | inquiry behavior is bounded, typed, and clearly separate from product runtime or structural growth |
| test, demo, validation, and evidence planning | define verifier family, evidence manifests, extra danger-zone audit path, additional human checkpoint, demo bundle, and validation path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | verifier plan, evidence plan, demo plan, extra-audit plan, checkpoint plan, and validation surfaces | runtime-family targets are stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. `Program Governor` verifies Phase 10 approval truth and confirms Phase 11 remains `open`.
2. `Program Governor` verifies the project-scoped `.codex` package and records the one setup tightening for `phase_builder`.
3. `Program Governor` locks active, consult-only, and inactive roles for Phase 11 planning.
4. `Source Cartographer` maps all required Phase 11 subsystems to donor basis and one allowed disposition.
5. `Architecture & Contract Lead` drafts subsystem boundaries, allowed Phase 10 interfaces, and forbidden Phase 12 and 13 leaks.
6. `Meta & Growth Pod Lead` drafts the future runtime-family decomposition after the first-pass reuse map and boundary rules exist.
7. `Constitution Keeper` reviews the first-pass reuse map and boundary rules for autonomy drift, support laundering, self-approval drift, and later-phase leakage.
8. If a Phase 2 seam is ambiguous, `Kernel Pod Lead` is consulted narrowly and remains non-authoring.
9. If a Phase 4 or 5 seam is ambiguous, `Memory & Graph Pod Lead` is consulted narrowly and remains non-authoring.
10. If a Phase 7, 8, 9, or 10 seam is ambiguous, `World & Conversation Pod Lead` is consulted narrowly and remains non-authoring.
11. If a runtime-shell or output-format seam is ambiguous, `Product & Sandbox Pod Lead` is consulted narrowly and remains non-authoring.
12. `Test & Replay Lead` and `Release & Evidence Lead` define verifier, evidence, demo, additional-human-checkpoint, and danger-zone audit families after the runtime-family targets are stable.
13. `Program Governor` consolidates the plan, task-card set, artifact matrix, budget envelope, and closure map.
14. `Anti-Shortcut Auditor` audits the full planning package.
15. `Program Governor` independently re-reads the cited files directly and verifies the package.
16. `Validation Agent` prepares the later review request only after audit and Governor verification exist.
17. User review happens only after the validated planning package exists.

Safe parallelism:

- `Source Cartographer` and `Architecture & Contract Lead` may work in parallel on disjoint planning outputs.
- `Meta & Growth Pod Lead` waits for first-pass reuse and boundary outputs before locking the runtime family.
- `Test & Replay Lead` and `Release & Evidence Lead` wait for stable runtime-family targets.
- `Merge Arbiter` remains inactive in planning-only work.

## 12. Detailed task cards

### `P11-TC-PG-01`

- task card ID: `P11-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, `.codex` setup verification, the canonical Phase 11 plan, role activation, artifact matrix, budget envelope, closure map, and final readiness judgment
- exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_11_GOVERNED_SELF_IMPROVEMENT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-PG-01_PHASE_11_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 12 and later artifacts
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - `.codex/agents/*` unless the run is explicitly write-enabled
- required reads first:
  - the frozen read-before-work stack from `ROLE_AUTHORITY_RULES.md`
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 through 10 plans and execution surfaces
  - relevant requirement and design files
  - existing `.codex` setup files
- step-by-step work method:
  1. verify Phase 10 approval truth
  2. verify `.codex` setup contents and record any drift
  3. lock active, consult-only, and inactive roles
  4. consolidate reuse, boundary, runtime-family, verifier, and demo outputs
  5. lock future artifact families and closure mapping
  6. prepare the final planning package for audit
- required cross-checks:
  - no Phase 12 planning
  - no Phase 13 planning
  - no runtime implementation
  - no approval language
- exit criteria:
  - the Phase 11 planning package is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation, closure, or approval
- explicit proof that no approval is implied: this task ends at plan readiness only; Phase 11 remains `open`

### `P11-TC-CK-01`

- task card ID: `P11-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4-mini`
- objective: guard constitution, falsification honesty, and Phase 11 autonomy boundaries
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-CK-01_PHASE_11_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_11_GOVERNED_SELF_IMPROVEMENT.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 12 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - the Phase 11 draft
- step-by-step work method:
  1. check that self-improvement stays evidence-bound and rollback-bound
  2. check that self-initiated inquiry stays bounded and local
  3. check that Phase 11 stays below Phase 12 and Phase 13
  4. report any boundary drift to `Program Governor`
- required cross-checks:
  - no hidden-model loophole
  - no self-approval path
  - no uncontrolled autonomy
  - no Phase 12 or 13 behavior
  - no approval language
- exit criteria:
  - constitutional objections are resolved or explicitly raised as blockers
- handoff target: `Program Governor`
- anti-drift rule: do not author runtime design or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P11-TC-SC-01`

- task card ID: `P11-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4-mini`
- objective: map every major Phase 11 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-SC-01_PHASE_11_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 12 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 10 plan and execution surfaces
  - inspected donor idle-reflection and governed-adoption files
- step-by-step work method:
  1. map all eleven Phase 11 subsystems
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

### `P11-TC-ACL-01`

- task card ID: `P11-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 11 boundaries, allowed interfaces, forbidden leaks, and the Phase 11 overlay-contract strategy
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-ACL-01_PHASE_11_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 12 and later artifacts
- required reads first:
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 10 plan and runtime surfaces
  - `Source Cartographer` output
- step-by-step work method:
  1. define what belongs in each Phase 11 subsystem only
  2. define allowed Phase 10 interfaces
  3. define the supplemental Phase 11 overlay-contract strategy
  4. define forbidden Phase 12 and Phase 13 leaks
  5. pass runtime-family implications to `Program Governor` and `Meta & Growth Pod Lead`
- required cross-checks:
  - no one mixed self-improvement engine
  - no direct user-facing answer ownership inside Phase 11
  - no direct mutation of Phase 10 state
  - no structural-growth or product-runtime semantics
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `Meta & Growth Pod Lead`
- anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, science-world, rich-expression, critique, or the team
- explicit proof that no approval is implied: boundary framing is planning truth only

### `P11-TC-MGPL-01`

- task card ID: `P11-TC-MGPL-01`
- role owner: `Meta & Growth Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 11 runtime family without crossing into Phase 12 or Phase 13
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-MGPL-01_PHASE_11_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 12 and later artifacts
- required reads first:
  - approved Phase 2 through 10 plans and execution surfaces
  - the Phase 11 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
- step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_11_governed_self_improvement/agifcore_phase11_self_improvement/`
  2. keep the module set explicit:
     - `contracts.py`
     - `offline_reflection_and_consolidation.py`
     - `idle_reflection.py`
     - `proposal_generation.py`
     - `self_experiment_lab.py`
     - `shadow_evaluation.py`
     - `before_after_measurement.py`
     - `adoption_or_rejection_pipeline.py`
     - `post_adoption_monitoring.py`
     - `rollback_proof.py`
     - `thought_episodes.py`
     - `self_initiated_inquiry_engine.py`
     - `self_improvement_cycle.py`
  3. order implementation so contracts and reflection come first, then proposals and experiment lab, then evaluation and measurement, then adoption and monitoring, then rollback proof and thought episodes, and the inquiry engine last
  4. identify where Phase 10 exports must be consumed read-only
- required cross-checks:
  - no runtime code written now
  - no Phase 12 behavior
  - no Phase 13 behavior
  - no hidden autonomy path
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase

### `P11-TC-TRL-01`

- task card ID: `P11-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4-mini`
- objective: define the Phase 11 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-TRL-01_PHASE_11_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 12 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 10 verifier and evidence families
  - the Phase 11 draft
- step-by-step work method:
  1. define one verifier per major Phase 11 subsystem
  2. define cross-cutting adoption, rollback, inquiry, and honesty checks
  3. define evidence reports and manifest contents
  4. define the extra Meta & Growth danger-zone audit hook surfaces and the additional human checkpoint evidence
- required cross-checks:
  - tests must verify separation between all eleven Phase 11 subsystems
  - measurement must be machine-checkable and not prose-only
  - rollback proof must be real and evidence-linked
  - self-initiated inquiry must stay bounded and local
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P11-TC-ASA-01`

- task card ID: `P11-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4-mini`
- objective: audit the Phase 11 planning package for fake completeness, giant-engine collapse, fake measurement, fake rollback, and danger-zone drift
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-ASA-01_PHASE_11_PLAN_AUDIT.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 12 and later artifacts
- required reads first:
  - full Phase 11 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `Test & Replay Lead` evidence-plan output
  - relevant approved Phase 10 plan and runtime surfaces
- step-by-step work method:
  1. check that all required sections exist
  2. check that each major subsystem has a source basis and disposition
  3. check that no one giant self-improvement engine is being passed off as design
  4. check that no approval or completion claim is implied
- required cross-checks:
  - no blind rewrite where a plausible substrate exists
  - no silent omission of any required subsystem
  - no Phase 12 or 13 behavior smuggled in
  - no empty report path or unverifiable demo plan
- exit criteria:
  - all blockers are either cleared or explicitly raised
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P11-TC-VA-01`

- task card ID: `P11-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 11 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-VA-01_PHASE_11_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_11_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 12 and later artifacts
- required reads first:
  - full Phase 11 draft
  - audit output
  - Governor verification output
  - validation protocol
- step-by-step work method:
  1. confirm the plan is decision-complete
  2. confirm every closure requirement has a later artifact path
  3. confirm the later demos are inspectable and truthful
  4. confirm the extra danger-zone audit and additional-human-checkpoint paths exist in the closure chain
- required cross-checks:
  - no author and validator role collision
  - no missing review surface
  - no implied approval
- exit criteria:
  - review request scope is exact and inspectable
- handoff target: `Program Governor`
- anti-drift rule: do not author plan content or runtime behavior
- explicit proof that no approval is implied: validation asks for review and does not mark the phase earned

### `P11-TC-REL-01`

- task card ID: `P11-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4-mini`
- objective: define the later Phase 11 demo-bundle shape and review packet surfaces
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_11/P11-TC-REL-01_PHASE_11_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 12 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 10 demo bundle
  - `Test & Replay Lead` verifier and evidence plan
  - the Phase 11 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the self-improvement demo surface
  3. define the rollback demo surface
  4. define the bounded self-initiated inquiry demo surface
  5. define the user-review packet order
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
| offline reflection and consolidation exists | `offline_reflection_and_consolidation.py`, `verify_phase_11_offline_reflection_and_consolidation.py`, `phase_11_offline_reflection_and_consolidation_report.json` | `Meta & Growth Pod Lead` | verifier confirms bounded reflection items, typed consolidation output, and no live-turn mutation | one opaque reflection dump with no typed consolidation surface |
| idle reflection exists | `idle_reflection.py`, `verify_phase_11_idle_reflection.py`, `phase_11_idle_reflection_report.json` | `Meta & Growth Pod Lead` | verifier confirms explicit idle entrypoint, bounded cycle, and normal-turn separation | idle reflection silently running on ordinary turns or having no explicit cycle output |
| proposal generation exists | `proposal_generation.py`, `verify_phase_11_proposal_generation.py`, `phase_11_proposal_generation_report.json` | `Meta & Growth Pod Lead` | verifier confirms typed proposals, falsifiers, rollback target, and bounded proposal counts | “proposal” labels with no typed proposal record |
| self-experiment lab exists | `self_experiment_lab.py`, `verify_phase_11_self_experiment_lab.py`, `phase_11_self_experiment_lab_report.json` | `Meta & Growth Pod Lead` | verifier confirms sandboxed held-out experiments and candidate/baseline separation | live-adoption behavior passed off as experiment lab |
| shadow evaluation exists | `shadow_evaluation.py`, `verify_phase_11_shadow_evaluation.py`, `phase_11_shadow_evaluation_report.json` | `Meta & Growth Pod Lead` | verifier confirms held-out delta, regression capture, and non-adopting evaluation state | evaluation prose with no isolated comparison record |
| before/after measurement exists | `before_after_measurement.py`, `verify_phase_11_before_after_measurement.py`, `phase_11_before_after_measurement_report.json` | `Meta & Growth Pod Lead` | verifier confirms baseline/adopted/rollback triplets and machine-readable metrics | “improved” claims with no triplet or no metric surface |
| adoption or rejection pipeline exists | `adoption_or_rejection_pipeline.py`, `verify_phase_11_adoption_or_rejection_pipeline.py`, `phase_11_adoption_or_rejection_pipeline_report.json` | `Meta & Growth Pod Lead` | verifier confirms typed states, evidence preconditions, and no self-approval path | adoption happening with missing evidence or no explicit state |
| post-adoption monitoring exists | `post_adoption_monitoring.py`, `verify_phase_11_post_adoption_monitoring.py`, `phase_11_post_adoption_monitoring_report.json` | `Meta & Growth Pod Lead` | verifier confirms bounded monitoring windows, regression triggers, and rollback escalation | monitoring described in prose with no typed monitoring records |
| rollback proof exists | `rollback_proof.py`, `verify_phase_11_rollback_proof.py`, `phase_11_rollback_proof_report.json` | `Meta & Growth Pod Lead` | verifier confirms adopted-to-rollback roundtrip restores baseline on the same pack | rollback claimed but not demonstrated or not same-pack |
| thought episodes exists | `thought_episodes.py`, `verify_phase_11_thought_episodes.py`, `phase_11_thought_episodes_report.json` | `Meta & Growth Pod Lead` | verifier confirms bounded episode notes tied to real refs and proposal ids | diary-like notes with no trace linkage or governance bounds |
| self-initiated inquiry engine exists | `self_initiated_inquiry_engine.py`, `verify_phase_11_self_initiated_inquiry_engine.py`, `phase_11_self_initiated_inquiry_engine_report.json` | `Meta & Growth Pod Lead` | verifier confirms one bounded inquiry path, budget enforcement, and no external-search dependence | uncontrolled inquiry fan-out or product-runtime takeover |
| demo path exists | `phase_11_demo_index.md`, `phase_11_self_improvement_demo.md`, `phase_11_rollback_demo.md`, `phase_11_bounded_self_initiated_inquiry_demo.md` plus matching `.json` outputs | `Release & Evidence Lead` | direct demo-bundle inspection and rerunnable demo scripts | no inspectable demo or demo claims unsupported by evidence |
| tests and evidence path exists | full verifier family under `05_testing/phase_11_governed_self_improvement/` and `phase_11_evidence_manifest.json` | `Test & Replay Lead` | Governor rerun plus validation request | missing verifier coverage, missing manifest, or non-machine-readable evidence |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| self-improvement demo | `offline_reflection_and_consolidation.py`, `proposal_generation.py`, `self_experiment_lab.py`, `shadow_evaluation.py`, `before_after_measurement.py`, `adoption_or_rejection_pipeline.py`, `post_adoption_monitoring.py`, runnable demo script, evidence manifest, and additional-human-checkpoint record | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Meta & Growth Pod Lead` | `Anti-Shortcut Auditor` | original baseline pack, candidate proposal, experiment conditions, evaluation delta, before/after metrics, adoption decision, monitoring output, rollback target, and backing evidence reports |
| rollback demo | `rollback_proof.py`, `before_after_measurement.py`, `adoption_or_rejection_pipeline.py`, runnable demo script, evidence manifest, and additional-human-checkpoint record | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Meta & Growth Pod Lead` | `Anti-Shortcut Auditor` | baseline state, adopted state, rollback state, same-pack roundtrip evidence, rollback ref, and proof that the restored result matches the baseline profile |
| bounded self-initiated inquiry demo | `self_initiated_inquiry_engine.py`, `idle_reflection.py`, `offline_reflection_and_consolidation.py`, runnable demo script, evidence manifest, and additional-human-checkpoint record | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Meta & Growth Pod Lead` | `Anti-Shortcut Auditor` | inquiry trigger, budget gate, inquiry goal, allowed local data sources, produced inquiry trace, stop condition, and proof that no uncontrolled autonomy or external-search path was used |

Validation rules for all demos:

- `Validation Agent` prepares the review request only after the standard audit, the extra danger-zone audit, the Governor verification record, and the additional human checkpoint record exist.
- `Program Governor` is the only role that asks the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.
- If any structural-growth or product-runtime behavior appears during Phase 11 execution, the correct action is to stop and escalate boundary drift, not to widen the demo scope.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable self-improvement substrate | compare subsystem plans and later runtime against mapped donor files and exact inherited records | `Source Cartographer` | a subsystem is rebuilt from zero despite a clear donor basis or exact inherited record surface | stop and reopen reuse mapping before execution |
| one giant improvement engine pretending to do reflection, proposal, evaluation, adoption, rollback, and inquiry | boundary audit and verifier-plan audit | `Architecture & Contract Lead` | one opaque module is asked to own most Phase 11 behavior | reject the design and split the lanes before continuing |
| proposal generation existing only as labels | proposal verifier and self-improvement demo audit | `Anti-Shortcut Auditor` | proposal language appears without typed proposal records, falsifiers, or rollback targets | block closure until proposal behavior is real |
| measurement existing only as prose | measurement verifier and self-improvement demo audit | `Test & Replay Lead` | measurement claims appear without same-pack triplets or machine-readable metrics | stop and require typed measurement outputs |
| rollback proof existing only as claims | rollback verifier and rollback-demo audit | `Constitution Keeper` | rollback is claimed without same-pack roundtrip proof | stop and require real rollback proof before continuing |
| self-initiated inquiry becoming uncontrolled autonomy | inquiry verifier, budget checks, and danger-zone audit | `Constitution Keeper` | more than one ungated inquiry appears, or inquiry escapes local bounded inputs | stop and remove the uncontrolled inquiry path |
| Phase 11 accidentally absorbing Phase 12 structural growth behavior | boundary audit against the forbidden Phase 12 list | `Constitution Keeper` | self-reorganization, tissue change, domain genesis, or structural-growth control loops appear in Phase 11 | stop and remove the structural-growth dependency |
| Phase 11 accidentally absorbing Phase 13 product-runtime behavior | boundary audit against the forbidden Phase 13 list | `Architecture & Contract Lead` | runner/gateway/UI changes, product UX ownership, or installer/public-release work appears in Phase 11 | stop and remove the product-runtime dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 11 plan artifacts
- after user approval, any future change to the Phase 11 plan requires explicit reopen instruction and a supersession note

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 10 is explicitly `approved` in the live phase-truth files and corroborated by the decision and changelog records.
- Phase 11 remains `open`.
- The required provenance stack, approved Phase 2 through 10 baselines, requirements pack, design pack, admin controls, and donor substrate were all reviewed directly.
- No prerequisite blocker was found.
- The main non-blocker seams are:
  - Phase 11 has no AGIFCore overlay contract yet and must layer above approved Phase 10 truth rather than mutate it.
  - the strongest idle-reflection and adoption substrate is donor-side only and must be disentangled from old mixed runtime behavior.
  - self-initiated inquiry has useful research substrate but remains too risky to port directly and therefore stays bounded and research-adapted by default.
- Defaults locked by this draft:
  - later execution keeps one active build pod by default: `Meta & Growth Pod Lead`
  - offline reflection and consolidation, idle reflection, shadow evaluation, thought episodes, and self-initiated inquiry default toward `adapt_for_research_only`
  - proposal generation, self-experiment lab, and post-adoption monitoring default toward `rebuild_clean`
  - before/after measurement, adoption or rejection pipeline, and rollback proof default toward `port_with_provenance`
  - Phase 11 remains a governed self-improvement layer above approved Phase 10 outputs and below Phase 12 and Phase 13 behavior
