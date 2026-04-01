# Phase 12: Structural Growth

Brief summary:

Phase 12 plans the governed structural-growth layer that sits above approved Phase 11 self-improvement outputs and below Phase 13 product runtime and Phase 14 sandbox/profile/scale behavior. It must later produce inspectable self-model feedback, reflection control, self-reorganization, domain genesis, theory formation, procedure/tool invention, and curiosity/gap-selection surfaces without turning structural change into hidden autonomy or leaking into product-runtime or deployment-profile behavior.

Planned interface additions for later execution:

- a new runtime family under `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/`
- a thin coordinator snapshot `agifcore.phase_12.structural_growth_cycle.v1`
- a thin overlay contract `agifcore.phase_12.overlay_contract.v1`
- per-subsystem schemas:
  - `agifcore.phase_12.self_model_feedback.v1`
  - `agifcore.phase_12.reflection_control.v1`
  - `agifcore.phase_12.self_reorganization.v1`
  - `agifcore.phase_12.domain_genesis.v1`
  - `agifcore.phase_12.theory_formation.v1`
  - `agifcore.phase_12.procedure_tool_invention.v1`
  - `agifcore.phase_12.curiosity_gap_selection.v1`

Planning defaults chosen:

- later execution keeps one active build pod by default: `Meta & Growth Pod Lead`
- later execution must include one extra audit pass, stronger Governor review, and one additional human demo checkpoint because structural growth behavior is inside the Meta & Growth danger zone
- the existing project-scoped `.codex` setup is reusable as-is; no blocking maintenance change is needed before Phase 12 planning

## 1. Phase identity

- Phase number: `12`
- Canonical phase name: `Structural Growth`
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
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md` through `projects/agifcore_master/01_plan/PHASE_11_GOVERNED_SELF_IMPROVEMENT.md`
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
  - approved Phase 2 through Phase 11 execution, testing, and output surfaces under `projects/agifcore_master/04_execution/`, `projects/agifcore_master/05_testing/`, and `projects/agifcore_master/06_outputs/`
  - admin control files under `projects/agifcore_master/00_admin/`
  - project-scoped custom-agent setup under `.codex/config.toml` and `.codex/agents/`
  - direct donor inspection from `agif_fabric_v1`, `agif-tasklet-cell`, root v2 lineage, and `agif_v2_master`, with direct focus on old `8C-E2` theory-growth freezes, old `8C-E3` governed structural-growth plan/contracts/runtime/proof, old `7A-E6` reorganization runtime, old `CELL_FAMILIES` structural target set, and current AGIFCore Phase 10 and Phase 11 runtime surfaces

## 2. Phase mission

- Phase 12 exists to define and later build the governed structural-growth layer that can take bounded structural evidence, turn it into typed structural candidates, test those candidates safely, and expose traceable growth decisions without becoming uncontrolled self-modification.
- Phase 12 must later build:
  - self-model feedback
  - reflection control
  - self-reorganization
  - domain genesis
  - theory formation
  - procedure/tool invention
  - curiosity/gap selection
- Phase 12 must not:
  - implement Phase 13 product-runtime behavior
  - implement Phase 14 sandbox/profile/scale behavior
  - re-implement Phase 2 kernel/workspace control, Phase 3 structure truth, Phase 4 memory policy, Phase 5 graph policy, Phase 6 simulator logic, Phase 7 conversation execution, Phase 8 science/world reasoning, Phase 9 rich expression, Phase 10 critique, or Phase 11 self-improvement itself
  - turn structural candidates into hidden self-approval
  - turn reorganization into silent runtime mutation
  - turn theory formation into prose-only notes
  - turn procedure/tool invention into unreviewed executable behavior
  - turn curiosity into uncontrolled autonomy
  - execute live external search
  - bypass support-state honesty or rollback discipline
  - claim historical v1, tasklet, root v2, or v2 packages as earned AGIFCore completion
  - imply commit, freeze, approval, or closure

## 3. Scope and non-goals

- In-scope artifacts:
  - the canonical Phase 12 plan
  - Phase 12 planning task cards
  - structural-growth boundary rules
  - reuse and provenance decisions for each major subsystem
  - future execution, testing, output, and handoff targets
  - later demo, validation, and closure planning
- Out-of-scope work:
  - any Phase 12 runtime code
  - any Phase 12 verifier code
  - any Phase 12 evidence generation
  - any Phase 13 planning
  - any Phase 14 planning
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
- Explicit untouched-later-phase statement:
  - Phase 13 and all later phases remain untouched by this plan.

## 4. Phase 11 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 11 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` show Phase 11 `approved` and Phase 12 `open` | Phase 12 planning may proceed |
| Explicit Phase 11 closeout truth exists outside index tables | `pass` | `projects/agifcore_master/DECISIONS.md` and `projects/agifcore_master/CHANGELOG.md` confirm Phase 11 approval and that Phase 12 has not started | no silent approval assumption |
| Required Phase 1 provenance artifacts relied on exist | `pass` | `HUMAN_THINKING_TARGET.md`, `COMPONENT_CATALOG.md`, `SOURCE_INHERITANCE_MATRIX.md`, `RUNTIME_REBUILD_MAP.md`, `TRACE_CONTRACT.md`, `VALIDATION_PROTOCOL.md`, and `DEMO_PROTOCOL.md` are present | provenance and closure framing exist |
| Required Phase 2 through 11 artifacts relied on exist | `pass` | approved plans and approved execution/testing/output families for Phases 2 through 11 are present | boundary seams and runtime inputs are inspectable |
| Dependency gap: canonical Phase 12 plan file is not present yet | `non-blocker` | `projects/agifcore_master/01_plan/PHASE_12_STRUCTURAL_GROWTH.md` is missing and is the target of this planning run | expected planning target |
| Dependency gap: Phase 12 planning task folder is not present yet | `non-blocker` | `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/` is missing | expected planning target |
| Compatibility seam: AGIFCore has no Phase 12 overlay contract yet | `non-blocker` | approved Phase 11 exposes a self-improvement cycle schema and Phase 11 overlay contract, but no approved Phase 12 coordinator schema exists yet | Phase 12 must define a new overlay above Phase 11 instead of mutating lower-phase truth |
| Compatibility seam: strongest structural-growth substrate is donor-side only | `non-blocker` | the strongest substrate is in old `8C-E2`, old `8C-E3`, and old `7A-E6`, not in approved AGIFCore runtime | Phase 12 must split reusable record semantics from historical runtime orchestration |
| Compatibility seam: donor domain genesis is mostly label-level or explicitly out of scope | `non-blocker` | old `8B` shows `domain_genesis` as a label and old `8C-E3` proof keeps domain genesis out of scope | Phase 12 must rebuild domain genesis cleanly from approved AGIFCore boundaries |
| Blockers vs non-blockers | `planning not blocked` | all prerequisite approvals and planning inputs exist | readiness may be `ready_for_user_review` |

Required Phase 1 through 11 artifacts relied on:

- Phase 1 provenance package and admin control stack
- approved Phase 2 kernel/workspace baseline
- approved Phase 3 cells/tissues/structure baseline
- approved Phase 4 memory baseline
- approved Phase 5 graph baseline
- approved Phase 6 world-model/simulator baseline
- approved Phase 7 conversation baseline
- approved Phase 8 science/world-awareness baseline
- approved Phase 9 rich-expression baseline
- approved Phase 10 meta-cognition baseline
- approved Phase 11 self-improvement baseline
- existing project-scoped `.codex` agent package

## 5. Active team map for Phase 12

Later Phase 12 execution default build pod: `Meta & Growth Pod Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | What it must never do this phase |
| --- | --- | --- | --- | --- | --- |
| `Program Governor` | `gpt-5.4` | active | prerequisite truth, danger-zone control, and final integration are required | own prerequisite truth, `.codex` setup verification, role activation, plan integration, artifact matrix, closure map, and final readiness judgment | implement runtime code, validate its own authored artifacts, or broaden into Phase 13 or 14 |
| `Constitution Keeper` | `gpt-5.4-mini` | active | Phase 12 can drift into uncontrolled mutation, hidden self-approval, or later-phase leakage | guard constitution, honesty, rollback discipline, no-hidden-model rules, and structural-growth boundaries | author runtime design alone, approve the phase, or allow Phase 13 or 14 leakage |
| `Source Cartographer` | `gpt-5.4-mini` | active | donor structural-growth substrate is real but uneven and must not be rebuilt blindly | map each subsystem to donor basis, disposition, and reuse limits | invent a fifth disposition, treat historical code as earned completion, or approve the phase |
| `Architecture & Contract Lead` | `gpt-5.4` | active | Phase 12 needs strict structural-growth boundaries above approved Phase 11 surfaces | own subsystem boundaries, allowed Phase 11 interfaces, forbidden Phase 13 and 14 leaks, and the Phase 12 overlay-contract strategy | redesign earlier phases, collapse all structural growth into one giant engine, or approve the phase |
| `Kernel Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 2 seam becomes ambiguous | consult on split/merge lifecycle, scheduler, rollback/quarantine, or workspace mutation seams only if ambiguity appears | author the plan, implement code, or broaden Phase 2 |
| `Memory & Graph Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if Phase 4 or 5 persistence seams become ambiguous | consult on memory carry-forward, concept/skill/transfer graph anchoring, retention, or rollback persistence only if ambiguity appears | author the plan, implement code, or pull Phase 12 down into memory or graph layers |
| `World & Conversation Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 7, 8, 9, 10, or 11 seam becomes ambiguous | consult on conversation, science-world, critique, or self-improvement input seams only if ambiguity appears | author the plan, implement code, or absorb Phase 12 into lower phases |
| `Meta & Growth Pod Lead` | `gpt-5.3-codex` | active | later execution owner and danger-zone build pod for Phase 12 | decompose the future runtime family for feedback, reflection control, reorganization, domain genesis, theory formation, procedure/tool invention, and bounded curiosity/gap selection | author canonical plan truth alone, implement code in this run, or absorb Phase 13 or 14 scope |
| `Product & Sandbox Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if runtime-shell or export seams become ambiguous | consult on runner-shell or export-format seams only if ambiguity appears | author the plan, implement product/sandbox work, or broaden scope |
| `Test & Replay Lead` | `gpt-5.4-mini` | active | structural growth must be test-planned from the start | define verifier family, replay checks, evidence expectations, extra danger-zone audit hooks, and closure failure signatures | implement runtime logic, fabricate reports, or approve the phase |
| `Anti-Shortcut Auditor` | `gpt-5.4-mini` | active | Phase 12 has the highest risk of fake structural change and fake rollback | audit for fake completeness, giant-engine collapse, uncontrolled mutation, label-only domain growth, note-only theory growth, and unverifiable demos | rewrite the plan instead of auditing it, downgrade blockers casually, or approve the phase |
| `Merge Arbiter` | `gpt-5.3-codex` | inactive | planning-only run | none | imply closure or perform merge work |
| `Validation Agent` | `gpt-5.4` | active | final machine-side review of the planning package is required before user review | validate the planning package after audit and Governor verification exist | author the plan, implement runtime, or approve the phase |
| `Release & Evidence Lead` | `gpt-5.4-mini` | active | later structural-growth demos must be inspectable and evidence-linked | define demo-bundle shape, additional human checkpoint surface, review packet order, and later demo sequencing | implement runtime behavior, publish release material, or imply acceptance |

## 6. Reuse and provenance strategy

Only the frozen four disposition categories are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance artifact justification |
| --- | --- | --- | --- | --- |
| self-model feedback | old `SelfModelFeedbackLoopRecord` in `8C-E3` contracts/runtime, approved Phase 10 `self_model` and `strategy_journal`, and approved Phase 11 measurement/monitoring/thought-episode outputs | `adapt_for_research_only` | the donor feedback loop is real and typed, but it is tightly coupled to old science-solver and reuse-rule updates; AGIFCore should adapt the loop semantics and rebuild the actual Phase 12 coordinator above approved Phase 10 and 11 traces | `COMPONENT_CATALOG.md` rows `CC-011` and `CC-017`; `TRACE_CONTRACT.md` |
| reflection control | old `ReflectionControlLoopRecord`, old `8C-E3` reflection path, old idle-reflection lineage, and approved Phase 11 offline/idle reflection surfaces | `adapt_for_research_only` | the donor reflection-control record is concrete, but the historical runtime is bound to old reflection orchestration; AGIFCore should adapt the record shape and rebuild the execution path above approved Phase 11 outputs | `COMPONENT_CATALOG.md` row `CC-018`; `RUNTIME_REBUILD_MAP.md` row `RRM-007`; `TRACE_CONTRACT.md` |
| self-reorganization | old `7A-E6` reorganization trace/proposal runtime, old `8C-E3` structural-growth proof, v1 lifecycle control and rollback substrate, and approved Phase 3 structure truth | `rebuild_clean` | donor reorganization traces and lifecycle verbs are useful, but the old runtime is an experiment-specific pressure lane that cannot be ported directly as AGIFCore structural mutation; AGIFCore should rebuild a governed reorganization lane while preserving trace, rollback, and lifecycle semantics | `COMPONENT_CATALOG.md` row `CC-029`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-003`, `SIM-006`, and `SIM-018` |
| domain genesis | old `8B` `domain_genesis` label, old `8C-E3` proof note that domain genesis stays out of scope, approved Domain Matrix, and approved Phase 5 transfer/concept graph boundaries | `rebuild_clean` | there is no donor runtime that proves governed domain genesis; only labels and boundary notes exist, so AGIFCore must rebuild a tightly bounded domain-genesis lane from current graph, world-model, and self-improvement evidence | `SOURCE_INHERITANCE_MATRIX.md` row `SIM-018`; `COMPONENT_CATALOG.md` rows `CC-008` and `CC-047` |
| theory formation | old `8C-E2` theory-growth record freeze, old `TheoryFragmentRecord`, approved Phase 10 theory fragments, approved Phase 11 experiment/evaluation outputs, and approved Phase 5 concept-graph boundary | `port_with_provenance` | the theory-growth output contract, falsifier discipline, and fragment-to-theory evidence chain are concrete and machine-checkable; AGIFCore should port that typed theory-growth shape with provenance and bind it above approved Phase 10 and 11 inputs | `COMPONENT_CATALOG.md` row `CC-021`; `TRACE_CONTRACT.md` |
| procedure/tool invention | approved Phase 4 procedural-memory boundary, approved Phase 5 skill-graph boundary, old donor `procedural skill` cell-family language, and transfer-descriptor substrate | `rebuild_clean` | storage and graph anchors already exist, but the donor line does not provide a safe AGIFCore-ready invention lane; AGIFCore should rebuild bounded invention candidates above failures, skill graph anchors, and governance rules | `COMPONENT_CATALOG.md` rows `CC-008` and `CC-044`; `SOURCE_INHERITANCE_MATRIX.md` row `SIM-008` |
| curiosity/gap selection | v1 need signals, old tasklet proactive/background lane, approved Phase 10 observer missing-needs, and approved Phase 11 inquiry triggers and monitoring regressions | `adapt_for_research_only` | there is real substrate for need signaling and bounded inquiry triggers, but direct port would reintroduce uncontrolled autonomy; AGIFCore should adapt the gating semantics and rebuild a bounded selector above approved Phase 10 and 11 traces | `COMPONENT_CATALOG.md` row `CC-047`; `SOURCE_INHERITANCE_MATRIX.md` row `SIM-042`; `TRACE_CONTRACT.md` |

## 7. Structural-growth boundary rules

### What belongs in self-model feedback only

- batch review of completed Phase 10 and Phase 11 traces to identify repeated structural failure patterns
- produce typed feedback items about knowledge boundaries, reuse limits, missing structures, and refinement pressure
- carry forward only typed feedback outputs, not structural mutations
- no direct reorganization, no domain creation, and no automatic theory adoption

### What belongs in reflection control only

- govern which structural candidate lanes may run in the current cycle
- cap candidate counts and stop reasons
- decide which feedback items defer, advance, or halt
- no direct mutation, no product-runtime decisions, and no sandbox/profile tuning

### What belongs in self-reorganization only

- propose bounded changes to existing AGIFCore structural arrangements
- preserve before/after state, rollback target, rejected alternative, and reorganization trace
- allow only governed split, merge, transfer, routing, or structure-shape candidates tied to approved Phase 3 and Phase 5 truth
- no silent mutation, no unlimited rewrite, and no domain genesis by side effect

### What belongs in domain genesis only

- propose one bounded new domain candidate when repeated evidence shows the current domain map is insufficient
- require explicit boundary statement, parent/peer domain refs, activation signals, and rejection path
- keep the domain candidate in a governed state until later adoption rules clear it
- no automatic proof-domain expansion and no uncontrolled domain sprawl

### What belongs in theory formation only

- turn approved Phase 10 theory fragments and approved Phase 11 experiment/evaluation evidence into typed theory candidates
- require assumptions, mechanism steps, predicted observables, falsifiers, and one next verification step
- preserve candidate, refine, hold, reject, or retire states explicitly
- no prose-only theory notes and no automatic graph-wide propagation

### What belongs in procedure/tool invention only

- create bounded reusable procedure or tool-policy candidates tied to procedural memory and the skill graph
- require skill-graph anchors, preconditions, limits, sandbox-compatibility note, and non-auto-execute rule
- keep invention as candidate-only until later governance clears it
- no external connector enablement, no live code authoring, and no automatic tool execution

### What belongs in curiosity/gap selection only

- rank repeated unmet needs, contradictions, regressions, and structural blind spots from approved evidence
- emit typed gap-selection records and one bounded downstream target choice per cycle
- preserve why the target was chosen, why others were deferred, and what would stop the cycle
- no uncontrolled background work and no user-facing answer ownership

### What is explicitly forbidden to leak in from Phase 13 product-runtime behavior

- runner/gateway/UI split changes
- local gateway endpoint design
- desktop UI behavior and presentation ownership
- installer and distribution work
- product-shell orchestration or background-service behavior
- public release packaging
- product-runtime UX claims standing in for structural-growth evidence

### What is explicitly forbidden to leak in from Phase 14 sandbox/profile/scale behavior

- sandbox engine implementation
- WASM or runtime-isolation policy changes
- laptop/mobile/builder profile tuning
- profile manifest or budget enforcement changes
- scale-realization control loops
- soak/profile packaging or scaling claims
- deployment-profile optimization passed off as structural growth

### How Phase 12 stays separate from Phase 11 self-improvement execution except through allowed interfaces

Allowed Phase 11 inputs:

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
- `agifcore.phase_11.self_improvement_cycle.v1`
- `agifcore.phase_11.overlay_contract.v1`

Rules for those inputs:

- they are read-only inputs only
- Phase 12 may consume them to discover structural failure patterns, structural candidate pressure, theory-upgrade opportunities, procedure gaps, domain-boundary failures, and bounded curiosity targets
- Phase 12 may not mutate Phase 11 runtime state or reinterpret held or rejected Phase 11 proposals as adopted structural change
- Phase 12 may not own direct user-facing response text or ordinary-turn answer envelopes

Forbidden Phase 11 interactions:

- direct mutation of Phase 11 runtime state
- using Phase 12 to smuggle product-runtime or sandbox/profile work into Phase 11
- collapsing feedback, reflection control, reorganization, domain genesis, theory formation, procedure invention, and curiosity into one opaque engine
- treating structural growth as a replacement for Phase 11 honesty, rollback, or monitoring discipline

## 8. Phase 12 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max self-model feedback items per cycle | `<= 6` items | stop and tighten feedback intake if later execution needs more than `6` items |
| max reflection-control actions per cycle | `<= 3` actions | stop and reduce control breadth if later execution exceeds `3` actions |
| max self-reorganization actions per cycle | `<= 1` action | stop and escalate if later execution needs more than one reorganization action in the same cycle |
| max domain-genesis items per cycle | `<= 1` item | stop and reopen domain-genesis policy if later execution needs more than one domain candidate in the same cycle |
| max theory-formation candidates per cycle | `<= 2` candidates | stop and tighten theory-growth scope if later execution exceeds `2` candidates |
| max procedure/tool invention candidates per cycle | `<= 1` candidate | stop and reduce invention fan-out if later execution exceeds `1` candidate |
| max curiosity/gap-selection items per cycle | `<= 2` items | stop and tighten curiosity selection if later execution exceeds `2` items |
| max Phase 12 evidence and demo bundle size | `<= 144 MiB` | stop and reorganize outputs if the bundle exceeds `144 MiB` |

Budget rules:

- these are laptop-profile planning ceilings only
- later execution must measure against them directly
- any ceiling breach must stop and escalate instead of widening silently
- any later need for higher ceilings requires reopening planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_12_STRUCTURAL_GROWTH.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2 through 11 baselines, admin controls, and donor inspection | all later Phase 12 work | section-complete Phase 12 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, and the Phase 12 plan | all later valid Phase 12 work | one planning task card per active role |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_PLAN_FREEZE_HANDOFF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 12 plan and admin controls | later execution start | frozen scope and no-approval status are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_EXECUTION_START_BRIEF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 12 plan and admin controls | later execution start | execution scope, danger-zone controls, and file families are explicit |
| `projects/agifcore_master/04_execution/phase_12_structural_growth/` | `Meta & Growth Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 10 and 11 surfaces, Phase 12 plan, provenance package, trace contract, and structural-boundary rules | later Phase 12 runtime delivery | runtime family exists and matches the plan |
| `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/` | `Meta & Growth Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | same as above plus exact module breakdown from this plan | later Phase 12 runtime delivery | feedback, reflection control, reorganization, domain genesis, theory formation, procedure/tool invention, curiosity/gap, and coordinator modules exist |
| `projects/agifcore_master/05_testing/phase_12_structural_growth/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 12 plan, execution family, validation protocol, and demo protocol | later verification and closeout | verifier family exists and runs |
| `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifier outputs, runtime snapshots, demo traces, and additional human checkpoint inputs | audit, Governor verification, and validation | machine-readable evidence bundle is inspectable |
| `projects/agifcore_master/06_outputs/phase_12_structural_growth/phase_12_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, validation protocol, and additional human checkpoint material | user review | structural-growth and theory-growth demos exist |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-AUDIT-01_PHASE_12_FINAL_PACKAGE_AUDIT_REPORT.md` | `Anti-Shortcut Auditor` | `Program Governor` | `n/a` | `Validation Agent` | runtime, tests, evidence, demos, and planning truth | Governor verification | standard final audit exists |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-AUDIT-02_PHASE_12_DANGER_ZONE_AUDIT_REPORT.md` | `Anti-Shortcut Auditor` | `Constitution Keeper` | `n/a` | `Validation Agent` | runtime, tests, evidence, demos, and Meta & Growth danger-zone controls | Governor verification | extra danger-zone audit exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, rerun verifiers, demo bundle, evidence bundle, and additional human checkpoint record | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_ADDITIONAL_HUMAN_DEMO_CHECKPOINT.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | demo bundle, evidence bundle, structural diff summaries, and rollback proof refs | validation request | required extra human checkpoint is explicit and inspectable |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdict request are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| self-model feedback and reflection-control planning | define the bounded structural-feedback and control lanes above approved Phase 11 | `Architecture & Contract Lead` | `Source Cartographer`, `Constitution Keeper`, `Meta & Growth Pod Lead` | future `contracts.py`, `self_model_feedback.py`, `reflection_control.py`, and `structural_growth_cycle.py` | prerequisite truth and reuse map exist | feedback and control boundaries are explicit and separate from mutation, Phase 13, and Phase 14 |
| self-reorganization planning | define governed reorganization behavior using approved Phase 3 structure truth and rollback discipline | `Meta & Growth Pod Lead` | `Architecture & Contract Lead`, `Constitution Keeper`, `Kernel Pod Lead` consult-only, `Memory & Graph Pod Lead` consult-only | future `self_reorganization.py` | feedback/control boundaries are stable | reorganization behavior is typed, rollback-bound, and not a free-form rewrite system |
| domain genesis and theory-formation planning | define governed domain-candidate creation and theory-growth behavior | `Architecture & Contract Lead` | `Source Cartographer`, `Meta & Growth Pod Lead`, `Memory & Graph Pod Lead` consult-only | future `domain_genesis.py` and `theory_formation.py` | feedback/control and reuse map are stable | domain and theory behavior are typed, falsifiable, graph-aware, and separately bounded |
| procedure/tool invention planning | define bounded procedure and tool-policy invention anchored to procedural memory and the skill graph | `Meta & Growth Pod Lead` | `Architecture & Contract Lead`, `Constitution Keeper`, `Memory & Graph Pod Lead` consult-only | future `procedure_tool_invention.py` | theory/domain boundaries are stable | invention stays candidate-only, graph-anchored, and non-auto-executing |
| curiosity/gap-selection planning | define bounded gap selection, ranking, and downstream structural-target choice | `Architecture & Contract Lead` | `Constitution Keeper`, `Meta & Growth Pod Lead`, `World & Conversation Pod Lead` consult-only | future `curiosity_gap_selection.py` | feedback/control boundaries are stable | curiosity stays local, bounded, and non-autonomous |
| test, demo, validation, and evidence planning | define verifier family, evidence manifests, extra danger-zone audit path, additional human checkpoint, demo bundle, and validation path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | verifier plan, evidence plan, demo plan, extra-audit plan, checkpoint plan, and validation surfaces | runtime-family targets are stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. `Program Governor` verifies Phase 11 approval truth and confirms Phase 12 remains `open`.
2. `Program Governor` verifies the project-scoped `.codex` package and records that no maintenance change is needed.
3. `Program Governor` locks active, consult-only, and inactive roles for Phase 12 planning.
4. `Source Cartographer` maps all required Phase 12 subsystems to donor basis and one allowed disposition.
5. `Architecture & Contract Lead` drafts subsystem boundaries, allowed Phase 11 interfaces, and forbidden Phase 13 and 14 leaks.
6. `Meta & Growth Pod Lead` drafts the future runtime-family decomposition after the first-pass reuse map and boundary rules exist.
7. `Constitution Keeper` reviews the first-pass reuse map and boundary rules for uncontrolled mutation, hidden self-approval, support laundering, and later-phase leakage.
8. If a Phase 2 seam is ambiguous, `Kernel Pod Lead` is consulted narrowly and remains non-authoring.
9. If a Phase 4 or 5 seam is ambiguous, `Memory & Graph Pod Lead` is consulted narrowly and remains non-authoring.
10. If a Phase 7, 8, 9, 10, or 11 seam is ambiguous, `World & Conversation Pod Lead` is consulted narrowly and remains non-authoring.
11. If a runtime-shell or export-format seam is ambiguous, `Product & Sandbox Pod Lead` is consulted narrowly and remains non-authoring.
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

### `P12-TC-PG-01`

- task card ID: `P12-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, `.codex` setup verification, the canonical Phase 12 plan, role activation, artifact matrix, budget envelope, closure map, and final readiness judgment
- exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_12_STRUCTURAL_GROWTH.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-PG-01_PHASE_12_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 13 and later artifacts
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - `.codex/agents/*` unless a separate maintenance run is explicitly authorized
- required reads first:
  - the frozen read-before-work stack from `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 through 11 plans and execution surfaces
  - relevant requirement and design files
  - existing `.codex` setup files
- step-by-step work method:
  1. verify Phase 11 approval truth
  2. verify `.codex` setup contents and record any drift
  3. lock active, consult-only, and inactive roles
  4. consolidate reuse, boundary, runtime-family, verifier, and demo outputs
  5. lock future artifact families and closure mapping
  6. prepare the final planning package for audit
- required cross-checks:
  - no Phase 13 planning
  - no Phase 14 planning
  - no runtime implementation
  - no approval language
- exit criteria:
  - the Phase 12 planning package is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation, closure, or approval
- explicit proof that no approval is implied: this task ends at plan readiness only; Phase 12 remains `open`

### `P12-TC-CK-01`

- task card ID: `P12-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4-mini`
- objective: guard constitution, rollback discipline, and Phase 12 mutation boundaries
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-CK-01_PHASE_12_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_12_STRUCTURAL_GROWTH.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - the Phase 12 draft
- step-by-step work method:
  1. check that structural mutation stays evidence-bound and rollback-bound
  2. check that curiosity and gap selection stay bounded and local
  3. check that Phase 12 stays below Phase 13 and Phase 14
  4. report any boundary drift to `Program Governor`
- required cross-checks:
  - no hidden-model loophole
  - no self-approval path
  - no uncontrolled autonomy
  - no Phase 13 or 14 behavior
  - no approval language
- exit criteria:
  - constitutional objections are resolved or explicitly raised as blockers
- handoff target: `Program Governor`
- anti-drift rule: do not author runtime design or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P12-TC-SC-01`

- task card ID: `P12-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4-mini`
- objective: map every major Phase 12 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-SC-01_PHASE_12_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 10 and Phase 11 plans and execution surfaces
  - inspected donor structural-growth, theory-growth, and reorganization files
- step-by-step work method:
  1. map all seven Phase 12 subsystems
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

### `P12-TC-ACL-01`

- task card ID: `P12-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 12 boundaries, allowed interfaces, forbidden leaks, and the Phase 12 overlay-contract strategy
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-ACL-01_PHASE_12_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- required reads first:
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/SKILL_GRAPH_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 11 plan and runtime surfaces
  - `Source Cartographer` output
- step-by-step work method:
  1. define what belongs in each Phase 12 subsystem only
  2. define allowed Phase 11 interfaces
  3. define the supplemental Phase 12 overlay-contract strategy
  4. define forbidden Phase 13 and Phase 14 leaks
  5. pass runtime-family implications to `Program Governor` and `Meta & Growth Pod Lead`
- required cross-checks:
  - no one mixed structural-growth engine
  - no direct user-facing answer ownership inside Phase 12
  - no direct mutation of Phase 11 state
  - no product-runtime or sandbox/profile semantics
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `Meta & Growth Pod Lead`
- anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, science-world, rich-expression, critique, self-improvement, or the team
- explicit proof that no approval is implied: boundary framing is planning truth only

### `P12-TC-MGPL-01`

- task card ID: `P12-TC-MGPL-01`
- role owner: `Meta & Growth Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 12 runtime family without crossing into Phase 13 or Phase 14
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-MGPL-01_PHASE_12_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- required reads first:
  - approved Phase 2 through 11 plans and execution surfaces
  - the Phase 12 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `projects/agifcore_master/03_design/CELL_FAMILIES.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/SKILL_GRAPH_MODEL.md`
- step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_12_structural_growth/agifcore_phase12_structural_growth/`
  2. keep the module set explicit:
     - `contracts.py`
     - `self_model_feedback.py`
     - `reflection_control.py`
     - `curiosity_gap_selection.py`
     - `theory_formation.py`
     - `procedure_tool_invention.py`
     - `self_reorganization.py`
     - `domain_genesis.py`
     - `structural_growth_cycle.py`
  3. order implementation so contracts and interface adapters come first, then self-model feedback and reflection control, then curiosity/gap selection, then theory formation, then procedure/tool invention, then self-reorganization, then domain genesis, and the thin coordinator last
  4. identify where Phase 11 exports must be consumed read-only
- required cross-checks:
  - no runtime code written now
  - no Phase 13 behavior
  - no Phase 14 behavior
  - no hidden autonomy path
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase

### `P12-TC-TRL-01`

- task card ID: `P12-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4-mini`
- objective: define the Phase 12 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-TRL-01_PHASE_12_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 11 verifier and evidence families
  - the Phase 12 draft
- step-by-step work method:
  1. define one verifier per major Phase 12 subsystem
  2. define cross-cutting reorganization, domain-genesis, theory-growth, procedure-invention, curiosity, rollback, and honesty checks
  3. define evidence reports and manifest contents
  4. define the extra Meta & Growth danger-zone audit hook surfaces and the additional human checkpoint evidence
- required cross-checks:
  - tests must verify separation between all seven Phase 12 subsystems
  - reorganization must be machine-checkable and rollback-linked
  - domain genesis must stay candidate-bound and non-sprawling
  - theory formation must be falsifiable and evidence-linked
  - curiosity/gap selection must stay bounded and local
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P12-TC-ASA-01`

- task card ID: `P12-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4-mini`
- objective: audit the Phase 12 planning package for fake completeness, giant-engine collapse, uncontrolled mutation, fake theory growth, fake invention, and danger-zone drift
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-ASA-01_PHASE_12_PLAN_AUDIT.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- required reads first:
  - full Phase 12 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `Test & Replay Lead` evidence-plan output
  - relevant approved Phase 10 and Phase 11 plan and runtime surfaces
- step-by-step work method:
  1. check that all required sections exist
  2. check that each major subsystem has a source basis and disposition
  3. check that no one giant growth engine is being passed off as design
  4. check that no approval or completion claim is implied
- required cross-checks:
  - no blind rewrite where a plausible substrate exists
  - no silent omission of any required subsystem
  - no Phase 13 or 14 behavior smuggled in
  - no empty report path or unverifiable demo plan
- exit criteria:
  - all blockers are either cleared or explicitly raised
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P12-TC-VA-01`

- task card ID: `P12-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 12 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-VA-01_PHASE_12_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_12_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- required reads first:
  - full Phase 12 draft
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

### `P12-TC-REL-01`

- task card ID: `P12-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4-mini`
- objective: define the later Phase 12 demo-bundle shape, additional human checkpoint surface, and review packet order
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_12/P12-TC-REL-01_PHASE_12_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 13 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 11 demo bundle
  - `Test & Replay Lead` verifier and evidence plan
  - the Phase 12 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the structural-growth demo surface
  3. define the theory-growth demo surface
  4. define the additional human checkpoint record surface
  5. define the user-review packet order
- required cross-checks:
  - demos must stay inspectable from files alone
  - no demo may imply acceptance or phase completion
  - no product-runtime or public-release packaging creep
- exit criteria:
  - later review packet is exact, ordered, and bounded
- handoff target: `Program Governor` then `Validation Agent`
- anti-drift rule: do not expand into release execution or public claims
- explicit proof that no approval is implied: demo-package planning is not demo acceptance

## 13. Closure-gate mapping

| Closure requirement | Artifact(s) that will satisfy it later | Role responsible | How it will be checked | What failure would look like |
| --- | --- | --- | --- | --- |
| self-model feedback exists | `self_model_feedback.py`, `verify_phase_12_self_model_feedback.py`, `phase_12_self_model_feedback_report.json` | `Meta & Growth Pod Lead` | verifier confirms typed feedback items, Phase 10/11 refs, and no direct mutation | opaque complaint list with no typed feedback record or support refs |
| reflection control exists | `reflection_control.py`, `verify_phase_12_reflection_control.py`, `phase_12_reflection_control_report.json` | `Meta & Growth Pod Lead` | verifier confirms capped control actions, stop reasons, and downstream gating | uncontrolled queue or direct mutation path with no control record |
| self-reorganization exists | `self_reorganization.py`, `verify_phase_12_self_reorganization.py`, `phase_12_self_reorganization_report.json` | `Meta & Growth Pod Lead` | verifier confirms before/after state, rejected alternative, rollback target, and reorganization trace | structural change claims with no before/after evidence, no rejected alternative, or no rollback proof |
| domain genesis exists | `domain_genesis.py`, `verify_phase_12_domain_genesis.py`, `phase_12_domain_genesis_report.json` | `Meta & Growth Pod Lead` | verifier confirms typed domain candidates, boundary rules, parent/peer refs, and candidate-only state | new domain names appearing with no typed candidate record or no boundary evidence |
| theory formation exists | `theory_formation.py`, `verify_phase_12_theory_formation.py`, `phase_12_theory_formation_report.json` | `Meta & Growth Pod Lead` | verifier confirms theory-growth status, mechanism steps, falsifiers, predicted observables, and next verification step | theory notes with no mechanism, no falsifier, or no candidate state |
| procedure/tool invention exists | `procedure_tool_invention.py`, `verify_phase_12_procedure_tool_invention.py`, `phase_12_procedure_tool_invention_report.json` | `Meta & Growth Pod Lead` | verifier confirms skill-graph anchors, preconditions, non-auto-execute rule, and bounded candidate state | “new tool/procedure” claims with no skill anchor, no limits, or hidden execution path |
| curiosity/gap selection exists | `curiosity_gap_selection.py`, `verify_phase_12_curiosity_gap_selection.py`, `phase_12_curiosity_gap_selection_report.json` | `Meta & Growth Pod Lead` | verifier confirms bounded gap counts, ranked choices, stop conditions, and no uncontrolled autonomy | uncontrolled background selection or more than budgeted items per cycle |
| demo path exists | `phase_12_demo_index.md`, `phase_12_structural_growth_demo.md`, `phase_12_theory_growth_demo.md` plus matching `.json` outputs | `Release & Evidence Lead` | direct demo-bundle inspection and rerunnable demo scripts | no inspectable demo or demo claims unsupported by evidence |
| tests/evidence path exists | full verifier family under `05_testing/phase_12_structural_growth/` and `phase_12_evidence_manifest.json` | `Test & Replay Lead` | Governor rerun plus validation request | missing verifier coverage, missing manifest, or non-machine-readable evidence |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| structural-growth demo | `self_model_feedback.py`, `reflection_control.py`, `self_reorganization.py`, `curiosity_gap_selection.py`, `structural_growth_cycle.py`, runnable demo script, evidence manifest, rollback proof, monitoring refs, and additional-human-checkpoint record | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Meta & Growth Pod Lead` | `Anti-Shortcut Auditor` | baseline structural snapshot, selected structural gap, accepted reorganization candidate, rejected alternative, before/after metrics, rollback proof, monitoring refs, and backing evidence reports |
| theory-growth demo | `theory_formation.py`, `self_model_feedback.py`, `reflection_control.py`, `curiosity_gap_selection.py`, runnable demo script, evidence manifest, and additional-human-checkpoint record | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Meta & Growth Pod Lead` | `Anti-Shortcut Auditor` | source theory fragments, theory candidate record, assumption refs, mechanism-step refs, predicted-observable refs, falsifier refs, next verification step, whether the candidate stayed held or advanced, and backing evidence reports |

Validation rules for all demos:

- `Validation Agent` prepares the review request only after the standard audit, the extra danger-zone audit, the Governor verification record, and the additional human checkpoint record exist.
- `Program Governor` is the only role that asks the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.
- If any product-runtime or sandbox/profile/scale behavior appears during Phase 12 execution, the correct action is to stop and escalate boundary drift, not to widen the demo scope.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable structural-growth substrate | compare subsystem plans and later runtime against mapped donor files and exact inherited records | `Source Cartographer` | a subsystem is rebuilt from zero despite a clear donor basis or exact inherited record surface | stop and reopen reuse mapping before execution |
| one giant growth engine pretending to do all structural growth | boundary audit and verifier-plan audit | `Architecture & Contract Lead` | one opaque module is asked to own most Phase 12 behavior | reject the design and split the lanes before continuing |
| self-reorganization becoming uncontrolled system mutation | reorganization verifier, rollback checks, and structural-growth demo audit | `Constitution Keeper` | structural state changes appear without before/after evidence, rollback proof, or rejected alternatives | stop and remove the uncontrolled mutation path |
| domain genesis existing only as labels | domain-genesis verifier and structural-growth demo audit | `Anti-Shortcut Auditor` | domain names appear without typed candidate records, boundary evidence, or rejection path | block closure until domain-genesis behavior is real |
| theory formation existing only as notes | theory verifier and theory-growth demo audit | `Test & Replay Lead` | a theory explanation appears without mechanism, falsifier, predicted observables, or next-step fields | stop and require typed theory outputs |
| procedure/tool invention existing only as claims | procedure/tool verifier and evidence audit | `Architecture & Contract Lead` | invention language appears without skill-graph anchors, preconditions, or bounded candidate state | stop and require real invention records |
| curiosity/gap selection becoming uncontrolled autonomy | curiosity verifier, budget checks, and danger-zone audit | `Constitution Keeper` | more than the budgeted gap-selection items appear, or selection escapes local evidence inputs | stop and remove the uncontrolled curiosity path |
| Phase 12 accidentally absorbing Phase 13 product-runtime behavior | boundary audit against the forbidden Phase 13 list | `Architecture & Contract Lead` | runner/gateway/UI changes, product UX ownership, or installer/public-release work appears in Phase 12 | stop and remove the product-runtime dependency |
| Phase 12 accidentally absorbing Phase 14 sandbox/profile/scale behavior | boundary audit against the forbidden Phase 14 list | `Constitution Keeper` | sandbox enforcement changes, profile-budget tuning, or scale-realization control loops appear in Phase 12 | stop and remove the sandbox/profile dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 12 plan artifacts
- after user approval, any future change to the Phase 12 plan requires explicit reopen instruction and a supersession note

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 11 is explicitly `approved` in the live phase-truth files and corroborated by the decision and changelog records.
- Phase 12 remains `open`.
- The required provenance stack, approved Phase 2 through 11 baselines, requirements pack, design pack, admin controls, and donor structural-growth substrate were all reviewed directly.
- No prerequisite blocker was found.
- The main non-blocker seams are:
  - Phase 12 has no AGIFCore overlay contract yet and must layer above approved Phase 11 truth rather than mutate it.
  - the strongest structural-growth substrate is donor-side only in old `8C-E2`, old `8C-E3`, and old `7A-E6`, so AGIFCore must split portable record shapes from historical runtime orchestration.
  - domain genesis has only label-level or out-of-scope donor support and therefore stays a clean rebuild target by default.
- Defaults locked by this draft:
  - later execution keeps one active build pod by default: `Meta & Growth Pod Lead`
  - self-model feedback, reflection control, and curiosity/gap selection default toward `adapt_for_research_only`
  - self-reorganization, domain genesis, and procedure/tool invention default toward `rebuild_clean`
  - theory formation defaults toward `port_with_provenance`
  - Phase 12 remains a governed structural-growth layer above approved Phase 11 outputs and below Phase 13 and Phase 14 behavior
