# Phase 13: Product Runtime and UX

Brief summary:

Phase 13 plans the governed product shell that sits above approved Phase 2 through 12 runtime truth and below Phase 14 sandbox/profile/scale behavior and Phase 16 release/publication behavior. It must later deliver a local-first product runtime with a typed host API, explicit runner/gateway/UI separation, inspectable exports, safe shutdown, fail-closed UX, and local installer/distribution flow without turning the product shell into a hidden cognition lane or public-release lane.

Planned interface additions for later execution:

- a new runtime family under `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/`
- a thin shell snapshot `agifcore.phase_13.product_runtime_shell.v1`
- a thin gateway contract `agifcore.phase_13.gateway_envelope.v1`
- a thin embeddable API contract `agifcore.phase_13.embeddable_runtime_api.v1`
- export contracts:
  - `agifcore.phase_13.state_export.v1`
  - `agifcore.phase_13.trace_export.v1`
  - `agifcore.phase_13.memory_review_export.v1`
  - `agifcore.phase_13.safe_shutdown.v1`
- default public surface set for the first execution slice:
  - `session_open`
  - `conversation_turn`
  - `state_export`
  - `trace_export`
  - `memory_review_export`
  - `safe_shutdown`
- reserved but default-fail-closed host control surfaces:
  - `task_submit`
  - `policy_update`

Planning defaults chosen:

- later execution keeps one active build pod by default: `Product & Sandbox Pod Lead`
- later execution must keep runner, gateway, and desktop UI as three explicit surfaces
- later execution must preserve `task_submit` and `policy_update` as replay-only or fail-closed unless an approved later gate explicitly widens them
- the existing project-scoped `.codex` setup is reusable now, and `phase_builder` explicitly names `Product & Sandbox Pod Lead`

## 1. Phase identity

- Phase number: `13`
- Canonical phase name: `Product Runtime and UX`
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
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md` through `projects/agifcore_master/01_plan/PHASE_12_STRUCTURAL_GROWTH.md`
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
  - approved Phase 2 through Phase 12 execution, testing, and output surfaces under `projects/agifcore_master/04_execution/`, `projects/agifcore_master/05_testing/`, and `projects/agifcore_master/06_outputs/`
  - admin control files under `projects/agifcore_master/00_admin/`
  - project-scoped custom-agent setup under `.codex/config.toml` and `.codex/agents/`
  - direct donor inspection from `agif_fabric_v1`, `agif-tasklet-cell`, and `agif_fabric_v2/projects/agif_v2_master`, with direct focus on old runner/operator substrate, old gateway envelopes and no-bypass rules, old desktop fail-closed UX surfaces, old installer/distribution folders, and old v2 typed embedding/export/shutdown surfaces

## 2. Phase mission

- Phase 13 exists to define and later build the governed local product shell that can host approved AGIFCore runtime truth inside a real product boundary without changing that truth.
- Phase 13 must later build:
  - embeddable runtime API
  - local runner
  - local gateway
  - local desktop UI
  - state export
  - trace export
  - memory review export
  - safe shutdown
  - fail-closed UX
  - installer/distribution flow
- Phase 13 must not:
  - implement Phase 14 sandbox/profile/scale behavior
  - implement Phase 16 release/publication behavior
  - re-implement Phase 2 through 12 runtime logic as a second cognition system
  - let the local gateway become a hidden second runtime
  - let the local desktop UI own correctness or rewrite trace truth
  - let exports become summary-only claims instead of governed evidence surfaces
  - let installer or packaging logic become a substitute for correctness
  - bypass trace-contract honesty, support-state honesty, or fail-closed behavior
  - claim historical donor shells as earned AGIFCore completion
  - imply commit, freeze, approval, or closure

## 3. Scope and non-goals

- In-scope artifacts:
  - the canonical Phase 13 plan
  - Phase 13 planning task cards
  - product-runtime and UX boundary rules
  - reuse and provenance decisions for each major subsystem
  - future execution, testing, output, and handoff targets
  - later demo, validation, and closure planning
- Out-of-scope work:
  - any Phase 13 runtime code
  - any Phase 13 verifier code
  - any Phase 13 evidence generation
  - any Phase 14 planning
  - any Phase 15 planning
  - any Phase 16 planning
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
- Explicit untouched-later-phase statement:
  - Phase 14 and all later phases remain untouched by this plan.

## 4. Phase 12 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 12 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` show Phase 12 `approved` and Phase 13 `open` | Phase 13 planning may proceed |
| Explicit Phase 12 closeout truth exists outside index tables | `pass` | `projects/agifcore_master/DECISIONS.md` and `projects/agifcore_master/CHANGELOG.md` confirm Phase 12 approval and that Phase 13 has not started | no silent approval assumption |
| Required Phase 1 provenance artifacts relied on exist | `pass` | `SYSTEM_CONSTITUTION.md`, `HUMAN_THINKING_TARGET.md`, `COMPONENT_CATALOG.md`, `SOURCE_INHERITANCE_MATRIX.md`, `RUNTIME_REBUILD_MAP.md`, `TRACE_CONTRACT.md`, `VALIDATION_PROTOCOL.md`, and `DEMO_PROTOCOL.md` are present | provenance and closure framing exist |
| Required Phase 2 through 12 artifacts relied on exist | `pass` | approved plans and approved execution/testing/output families for Phases 2 through 12 are present | runtime seams and product inputs are inspectable |
| Dependency gap: canonical Phase 13 plan file is not present yet | `non-blocker` | `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md` is missing and is the target of this planning run | expected planning target |
| Dependency gap: Phase 13 planning task folder is not present yet | `non-blocker` | `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/` is missing | expected planning target |
| Reusable builder package explicitly names `Product & Sandbox Pod Lead` | `pass` | `.codex/agents/phase_builder.toml` now names Product & Sandbox alongside the other build-pod roles | reusable setup is aligned for a later execution run |
| Compatibility seam: AGIFCore has no approved Phase 13 product shell contract yet | `non-blocker` | approved Phase 2 through 12 surfaces exist, but no approved product-runtime shell contract exists yet | Phase 13 must define a new shell above existing runtime truth instead of mutating it |
| Compatibility seam: donor desktop UI substrate contains research/demo-specific product behavior | `non-blocker` | old tasklet `desktop_ui_server.py` contains useful fail-closed and evidence patterns plus unrelated research-specific views and controls | Phase 13 should adapt UI patterns, not direct-port the whole shell |
| Compatibility seam: donor release/publication substrate exists but belongs later | `non-blocker` | tasklet `public_release/` and AGIFCore `PUBLIC_RELEASE_MODEL.md` show a later release lane | Phase 13 must stop at local installer/distribution flow |
| Blockers vs non-blockers | `planning not blocked` | all prerequisite approvals and planning inputs exist | readiness may be `ready_for_user_review` |

Required Phase 1 through 12 artifacts relied on:

- Phase 1 provenance package and admin control stack
- approved Phase 2 kernel/workspace baseline
- approved Phase 3 structure baseline
- approved Phase 4 memory baseline
- approved Phase 5 graph baseline
- approved Phase 6 world-model/simulator baseline
- approved Phase 7 conversation baseline
- approved Phase 8 science/world-awareness baseline
- approved Phase 9 rich-expression baseline
- approved Phase 10 meta-cognition baseline
- approved Phase 11 self-improvement baseline
- approved Phase 12 structural-growth baseline
- existing project-scoped `.codex` agent package

## 5. Active team map for Phase 13

Later Phase 13 execution default build pod: `Product & Sandbox Pod Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | What it must never do this phase |
| --- | --- | --- | --- | --- | --- |
| `Program Governor` | `gpt-5.4` | active | prerequisite truth, product-boundary control, and final integration are required | own prerequisite truth, `.codex` setup verification, role activation, plan integration, artifact matrix, closure map, and final readiness judgment | implement runtime code, validate its own authored artifacts, or broaden into Phase 14 or 16 |
| `Constitution Keeper` | `gpt-5.4-mini` | active | product shells can hide unsafe behavior behind UX polish | guard constitution, honesty, fail-closed discipline, no-hidden-model rules, and product-shell boundaries | author runtime design alone, approve the phase, or allow Phase 14 or 16 leakage |
| `Source Cartographer` | `gpt-5.4-mini` | active | donor product/runtime substrate is real and must not be recreated blindly | map each Phase 13 subsystem to donor basis, disposition, and reuse limits | invent a fifth disposition, treat donor shells as earned AGIFCore runtime, or approve the phase |
| `Architecture & Contract Lead` | `gpt-5.4` | active | Phase 13 needs strict runner/gateway/UI/export boundaries above approved runtime truth | own subsystem boundaries, allowed lower-phase interfaces, forbidden Phase 14 and 16 leaks, and the Phase 13 shell-contract strategy | redesign earlier phases, collapse product surfaces into one giant app shell, or approve the phase |
| `Kernel Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 2 runner or operator-family seam becomes ambiguous | consult on runner lifecycle, workspace operator commands, rollback, and shutdown seams only if ambiguity appears | author the plan, implement code, or broaden Phase 2 |
| `Memory & Graph Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 4 or 5 export seam becomes ambiguous | consult on memory-review export, graph-backed export refs, and export persistence only if ambiguity appears | author the plan, implement code, or pull Phase 13 down into memory or graph layers |
| `World & Conversation Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 7, 8, or 9 surface seam becomes ambiguous | consult on conversation-turn host surfaces and rich-expression presentation seams only if ambiguity appears | author the plan, implement code, or absorb Phase 13 into lower phases |
| `Meta & Growth Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 10, 11, or 12 seam becomes ambiguous | consult on how product surfaces may expose critique, self-improvement, or structural-growth outputs without owning them | author the plan, implement code, or widen product scope into meta/runtime policy |
| `Product & Sandbox Pod Lead` | `gpt-5.3-codex` | active | later execution owner and default build pod for Phase 13 | decompose the future product-runtime family for host API, runner, gateway, desktop UI, exports, shutdown, fail-closed UX, and installer/distribution | author canonical plan truth alone, implement code in this run, or absorb Phase 14 or 16 scope |
| `Test & Replay Lead` | `gpt-5.4-mini` | active | product-runtime claims must be verifier-planned from the start | define verifier family, replay checks, export checks, fail-closed checks, installer checks, and closure failure signatures | implement runtime logic, fabricate reports, or approve the phase |
| `Anti-Shortcut Auditor` | `gpt-5.4-mini` | active | product work can look complete in screenshots while being weak in evidence | audit for giant-shell collapse, fake exports, fake fail-closed UX, fake installer claims, and phase-leak drift | rewrite the plan instead of auditing it, downgrade blockers casually, or approve the phase |
| `Merge Arbiter` | `gpt-5.3-codex` | inactive | planning-only run | none | imply closure or perform merge work |
| `Validation Agent` | `gpt-5.4` | active | final machine-side review of the planning package is required before user review | validate the planning package after audit and Governor verification exist | author the plan, implement runtime, or approve the phase |
| `Release & Evidence Lead` | `gpt-5.4-mini` | active | later product demos must be inspectable and evidence-linked | define demo-bundle shape, review packet order, and later demo sequencing | implement runtime behavior, publish release material, or imply acceptance |

## 6. Reuse and provenance strategy

Only the frozen four disposition categories are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance artifact justification |
| --- | --- | --- | --- | --- |
| embeddable runtime API | old v2 `session_open`, `conversation_turn`, `memory_review_export`, `trace_export`, and `safe_shutdown` surface set in `agif_v2_master` Phase 8 embedding, plus tasklet envelope discipline, plus current AGIFCore trace contract | `port_with_provenance` | the typed host-surface set is already real, replay-oriented, and fail-closed where needed; AGIFCore should port that surface discipline while aligning names to current AGIFCore export truth | `TRACE_CONTRACT.md`; `COMPONENT_CATALOG.md` rows `CC-062`, `CC-063`, and `CC-073` |
| local runner | `agif_fabric_v1` `runner/cell`, tasklet `local_runner_service.py`, and approved AGIFCore Phase 2 through 12 runtime surfaces | `port_with_provenance` | there is clear runner/operator lineage plus current AGIFCore lower-phase runtime truth; AGIFCore should port orchestration patterns, not invent a new second runtime | `COMPONENT_CATALOG.md` rows `CC-038` and `CC-061`; `SOURCE_INHERITANCE_MATRIX.md` row `SIM-025` |
| local gateway | tasklet `trigger_gateway_orchestrator.py`, `gateway_envelope_schema_v1.json`, `12_GATEWAY_PROFILE.md`, and v2 host-contract surface rules | `port_with_provenance` | the gateway envelope, policy-hash, allowlist, and no-bypass pattern is concrete and machine-checkable; AGIFCore should port that mediation layer with current contract names | `COMPONENT_CATALOG.md` rows `CC-062` and `CC-063`; `SOURCE_INHERITANCE_MATRIX.md` rows `SIM-026` and `SIM-027` |
| local desktop UI | tasklet `desktop_ui_server.py`, tasklet demo shell patterns, and AGIFCore product-runtime model | `adapt_for_research_only` | the donor UI contains strong fail-closed and evidence-view patterns but also research/demo-specific views and controls that would over-expand Phase 13; AGIFCore should adapt the offline desktop-first shell style and explicit fail-closed states, then rebuild the actual UI around approved AGIFCore truth | `COMPONENT_CATALOG.md` row `CC-060`; `RUNTIME_REBUILD_MAP.md` row `RRM-009` |
| state export | approved AGIFCore Phase 2 `state_export()` behavior, v2 `state_snapshot` surface, tasklet export lanes, and workspace/export boundary rules | `port_with_provenance` | the export semantics already exist locally and donor-side; AGIFCore should port the host-facing surface shape while preserving the repo’s current `state_export` naming | `TRACE_CONTRACT.md`; `WORKSPACE_MODEL.md` |
| trace export | approved AGIFCore Phase 2 `trace_export()` behavior, v2 `trace_export` surface, and tasklet evidence/trace presentation | `port_with_provenance` | the export surface is portable even though the underlying AGIFCore trace generators were rebuilt earlier; Phase 13 should expose the trace truth, not redefine it | `TRACE_CONTRACT.md`; `COMPONENT_CATALOG.md` row `CC-069` |
| memory review export | approved AGIFCore Phase 2 `memory_review_export()` behavior and v2 `memory_review_export` surface | `port_with_provenance` | the lower-phase export already exists and the v2 host contract already names the right surface family; Phase 13 should port the host-facing wrapper and preserve the memory-review anchors | `TRACE_CONTRACT.md`; `COMPONENT_CATALOG.md` row `CC-067` |
| safe shutdown | v2 `safe_shutdown` surface, tasklet runner lifecycle patterns, and AGIFCore Phase 2 rollback/snapshot concepts | `port_with_provenance` | the donor shutdown receipt and state-hash pattern is concrete, and AGIFCore already has snapshot/rollback semantics underneath it | `TRACE_CONTRACT.md`; `WORKSPACE_MODEL.md` |
| fail-closed UX | tasklet `desktop_ui_server.py` fail-closed help and explicit denial states, v2 `policy_update` fail-closed host surface, and AGIFCore bundle-integrity rules | `port_with_provenance` | explicit fail-closed states, next-step guidance, and deterministic denial reasons already exist donor-side and are required by current AGIFCore design truth | `COMPONENT_CATALOG.md` row `CC-066`; `SOURCE_INHERITANCE_MATRIX.md` row `SIM-030` |
| installer/distribution flow | tasklet `macos_installer/`, `windows_installer/`, local packaging folders, and current AGIFCore deployment/product-runtime design | `port_with_provenance` | reusable local installer/distribution substrate exists, but AGIFCore must stop before public release/publication work; Phase 13 should port local packaging flow only | `COMPONENT_CATALOG.md` row `CC-070`; `SOURCE_INHERITANCE_MATRIX.md` row `SIM-034` |

## 7. Product-runtime and UX boundary rules

### What belongs in embeddable runtime API only

- expose the minimum typed host-facing local surfaces needed to open a session, submit a governed conversation turn, request governed exports, and request safe shutdown
- preserve stable surface names, request fields, response fields, and fail-closed semantics
- keep `task_submit` and `policy_update` reserved but default-fail-closed unless a later approved gate widens them
- never own transport enforcement, UI presentation, or cognition logic

### What belongs in local runner only

- execute approved Phase 2 through 12 runtime surfaces
- produce trace refs and hand off memory-review refs
- coordinate runtime lifecycle and safe-shutdown internals
- never bypass governance, never own gateway validation, and never present itself as the product UI

### What belongs in local gateway only

- validate local request envelopes
- enforce schema, policy-hash, allowlist, size, and rate rules before runner invocation
- expose local control endpoints for the approved host surface set only
- never become a hidden second runtime or bypass runner enforcement

### What belongs in local desktop UI only

- present conversation, status, traces, exports, fail-closed explanations, and installer/distribution status to the user
- show inspectable evidence refs and explicit blocked/paused states
- never own correctness, mutate trace truth, or silently widen blocked behavior

### What belongs in state export only

- expose a governed runtime snapshot suitable for inspection, replay anchoring, and shutdown handoff
- preserve provenance, snapshot hashes, and state lineage refs
- never become a hidden general-purpose storage dump

### What belongs in trace export only

- expose governed turn, replay, and evidence trace outputs
- preserve trace-contract field integrity and replay anchors
- never summarize away support state, knowledge-gap reasons, or blocked outcomes

### What belongs in memory review export only

- expose retention, revision, compression, rejection, and memory-review refs that the approved lower runtime already emits
- preserve memory-review anchors and continuity refs
- never write new memory truth by itself

### What belongs in safe shutdown only

- expose a governed stop request and receipt surface
- coordinate snapshot/export flush and shutdown receipts through approved runner surfaces
- never hide dropped work, silent truncation, or unsafe state mutation

### What belongs in fail-closed UX only

- make denials, pauses, missing evidence, integrity failures, and blocked surfaces explicit to the user
- preserve deterministic reason codes, evidence refs, and next-step guidance
- never downgrade a blocked state into a friendly-looking success path

### What belongs in installer/distribution flow only

- package the local runner, local gateway, local desktop UI, contracts, and integrity metadata for local install and local distribution
- preserve integrity evidence, artifact inventory, and local install instructions
- never turn into public-release notes, publication packaging, or claims matrices

### What is explicitly forbidden to leak in from Phase 14 sandbox/profile/scale behavior

- sandbox engine implementation
- WASM or runtime-isolation wiring
- profile manifest authoring
- laptop/mobile/builder budget tuning
- scale-realization control loops
- soak-profile privilege claims
- profile-specific correctness divergence

### What is explicitly forbidden to leak in from Phase 16 release/publication behavior

- release notes
- claims matrix authoring
- public evidence index
- GitHub/public release asset flow
- tag/release flow
- paper/publication package
- public release claim language standing in for local product proof

### How Phase 13 stays separate from the intelligence/runtime phases below except through allowed interfaces

Allowed lower-phase inputs:

- approved runner-executable runtime truth from Phases 2 through 12
- approved `state_export`, `trace_export`, and `memory_review_export` lower-phase surfaces
- approved conversation-turn entry surfaces from the conversation/runtime stack
- approved rollback, replay, and snapshot refs

Rules for those inputs:

- they are inputs and presentation/export sources only
- Phase 13 may host them, route them, validate transport to them, present them, or export them
- Phase 13 may not rewrite lower-phase truth, invent new cognition, or bypass lower-phase governance
- the desktop UI and gateway may not reach directly into lower-phase internals outside approved runner/export interfaces

Forbidden lower-phase interactions:

- direct UI mutation of cell, tissue, memory, graph, simulator, critique, self-improvement, or structural-growth state
- direct gateway calls that skip runner enforcement
- product-shell code inventing a second trace or second support-state story
- installer logic changing runtime truth after packaging

## 8. Phase 13 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max embeddable API surface count | `<= 8` surfaces | stop and reopen shell-contract planning if later execution needs more than `8` top-level surfaces |
| max local gateway route count | `<= 10` routes | stop and reduce gateway breadth if later execution exceeds `10` routes |
| max desktop UI screen/view count | `<= 7` views | stop and simplify the product shell if later execution exceeds `7` views |
| max `state_export` payload size | `<= 8 MiB` | stop and tighten export scope if later execution exceeds `8 MiB` |
| max `trace_export` payload size | `<= 16 MiB` | stop and tighten trace packaging if later execution exceeds `16 MiB` |
| max `memory_review_export` payload size | `<= 8 MiB` | stop and tighten memory-review packaging if later execution exceeds `8 MiB` |
| max fail-closed UX state count | `<= 10` explicit states | stop and consolidate UX states if later execution exceeds `10` states |
| max installer/distribution artifact count | `<= 6` artifacts per platform bundle | stop and simplify packaging if later execution exceeds `6` artifacts per platform |
| max Phase 13 evidence and demo bundle size | `<= 192 MiB` | stop and reorganize outputs if the bundle exceeds `192 MiB` |

Budget rules:

- these are laptop-profile planning ceilings only
- later execution must measure against them directly
- any ceiling breach must stop and escalate instead of widening silently
- any later need for higher ceilings requires reopening planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2 through 12 baselines, admin controls, and donor inspection | all later Phase 13 work | section-complete Phase 13 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, and the Phase 13 plan | all later valid Phase 13 work | one planning task card per active role |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_PLAN_FREEZE_HANDOFF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 13 plan and admin controls | later execution start | frozen scope and no-approval status are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_EXECUTION_START_BRIEF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 13 plan and admin controls | later execution start | execution scope, shell boundaries, and file families are explicit |
| `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/` | `Product & Sandbox Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 2 through 12 surfaces, Phase 13 plan, provenance package, trace contract, and product boundary rules | later Phase 13 runtime delivery | runtime family exists and matches the plan |
| `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/` | `Product & Sandbox Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | same as above plus exact module breakdown from this plan | later Phase 13 runtime delivery | API, runner, gateway, desktop UI, export, shutdown, fail-closed UX, and installer modules exist |
| `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 13 plan, execution family, validation protocol, and demo protocol | later verification and closeout | verifier family exists and runs |
| `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifier outputs, runtime snapshots, export captures, install logs, and demo traces | audit, Governor verification, and validation | machine-readable evidence bundle is inspectable |
| `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, validation protocol, and demo scripts | user review | end-to-end, fail-closed, and installer/distribution demos exist |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-AUDIT-01_PHASE_13_FINAL_PACKAGE_AUDIT_REPORT.md` | `Anti-Shortcut Auditor` | `Program Governor` | `n/a` | `Validation Agent` | runtime, tests, evidence, demos, and planning truth | Governor verification | standard final audit exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, rerun verifiers, demo bundle, evidence bundle, and install logs | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdict request are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| runtime API and runner planning | define the typed host API and runner shell above approved Phase 2 through 12 truth | `Product & Sandbox Pod Lead` | `Architecture & Contract Lead`, `Constitution Keeper`, `Kernel Pod Lead` consult-only | future `contracts.py`, `embeddable_runtime_api.py`, `local_runner.py`, and `product_runtime_shell.py` | prerequisite truth and reuse map exist | API and runner boundaries are explicit and separate from gateway, UI, and sandbox |
| gateway and desktop UI planning | define the local gateway and desktop UI without turning either into a second runtime | `Product & Sandbox Pod Lead` | `Architecture & Contract Lead`, `Source Cartographer`, `World & Conversation Pod Lead` consult-only | future `local_gateway.py`, `desktop_ui.py`, and `fail_closed_ux.py` | API and runner boundaries are stable | gateway no-bypass rules and UI presentation-only rules are explicit |
| export surface planning | define state, trace, and memory-review export surfaces that preserve lower-phase truth | `Architecture & Contract Lead` | `Product & Sandbox Pod Lead`, `Memory & Graph Pod Lead` consult-only, `Test & Replay Lead` | future `state_export.py`, `trace_export.py`, and `memory_review_export.py` | runner/gateway/UI boundaries are stable | export rules preserve provenance, replay anchors, and trace honesty |
| safe shutdown and fail-closed UX planning | define stop-state behavior and explicit blocked-state UX | `Architecture & Contract Lead` | `Constitution Keeper`, `Product & Sandbox Pod Lead` | future `safe_shutdown.py` and fail-closed UX rules | runner and export rules are stable | shutdown is receipt-based and fail-closed states are explicit and inspectable |
| installer/distribution planning | define local packaging and installer/distribution flow without entering public release | `Product & Sandbox Pod Lead` | `Source Cartographer`, `Architecture & Contract Lead`, `Release & Evidence Lead` | future `installer_distribution.py`, packaging manifest rules, and install verification path | gateway/UI/export boundaries are stable | local packaging flow is explicit and Phase 16 leakage is blocked |
| test, demo, validation, and evidence planning | define verifier family, evidence manifest, demo bundle, and validation path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | verifier plan, evidence plan, demo plan, and validation surfaces | runtime-family targets are stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. `Program Governor` verifies Phase 12 approval truth and confirms Phase 13 remains `open`.
2. `Program Governor` verifies the project-scoped `.codex` package and records the non-blocking `phase_builder` wording gap.
3. `Program Governor` locks active, consult-only, and inactive roles for Phase 13 planning.
4. `Source Cartographer` maps all required Phase 13 subsystems to donor basis and one allowed disposition.
5. `Architecture & Contract Lead` drafts subsystem boundaries, allowed lower-phase interfaces, and forbidden Phase 14 and 16 leaks.
6. `Product & Sandbox Pod Lead` drafts the future runtime-family decomposition after the first-pass reuse map and boundary rules exist.
7. `Constitution Keeper` reviews the first-pass shell boundaries for hidden-model drift, silent degradation, and fail-closed weakness.
8. If a Phase 2 seam is ambiguous, `Kernel Pod Lead` is consulted narrowly and remains non-authoring.
9. If a Phase 4 or 5 seam is ambiguous, `Memory & Graph Pod Lead` is consulted narrowly and remains non-authoring.
10. If a Phase 7, 8, or 9 seam is ambiguous, `World & Conversation Pod Lead` is consulted narrowly and remains non-authoring.
11. If a Phase 10, 11, or 12 seam is ambiguous, `Meta & Growth Pod Lead` is consulted narrowly and remains non-authoring.
12. `Test & Replay Lead` and `Release & Evidence Lead` define verifier, evidence, demo, and review-packet families after the runtime-family targets are stable.
13. `Program Governor` consolidates the plan, task-card set, artifact matrix, budget envelope, and closure map.
14. `Anti-Shortcut Auditor` audits the full planning package.
15. `Program Governor` independently re-reads the cited files directly and verifies the package.
16. `Validation Agent` prepares the later review request only after audit and Governor verification exist.
17. User review happens only after the validated planning package exists.

Safe parallelism:

- `Source Cartographer` and `Architecture & Contract Lead` may work in parallel on disjoint planning outputs.
- `Product & Sandbox Pod Lead` waits for first-pass reuse and boundary outputs before locking the runtime family.
- `Test & Replay Lead` and `Release & Evidence Lead` wait for stable runtime-family targets.
- `Merge Arbiter` remains inactive in planning-only work.

## 12. Detailed task cards

### `P13-TC-PG-01`

- task card ID: `P13-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, `.codex` setup verification, the canonical Phase 13 plan, role activation, artifact matrix, budget envelope, closure map, and final readiness judgment
- exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-PG-01_PHASE_13_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 14 and later artifacts
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - `.codex/agents/*` unless a separate maintenance run is explicitly authorized
- required reads first:
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 through 12 plans and execution surfaces
  - relevant requirement and design files
  - existing `.codex` setup files
- step-by-step work method:
  1. verify Phase 12 approval truth
  2. verify `.codex` setup contents and record any drift
  3. lock active, consult-only, and inactive roles
  4. consolidate reuse, boundary, runtime-family, verifier, and demo outputs
  5. lock future artifact families and closure mapping
  6. prepare the final planning package for audit
- required cross-checks:
  - no Phase 14 planning
  - no Phase 16 planning
  - no runtime implementation
  - no approval language
- exit criteria: the Phase 13 planning package is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation, closure, or approval
- explicit proof that no approval is implied: this task ends at plan readiness only; Phase 13 remains `open`

### `P13-TC-CK-01`

- task card ID: `P13-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4-mini`
- objective: guard constitution, fail-closed discipline, and Phase 13 product-shell boundaries
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-CK-01_PHASE_13_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md`
  - `projects/agifcore_master/02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - the Phase 13 draft
- step-by-step work method:
  1. check that product surfaces stay evidence-bound and fail-closed
  2. check that gateway and UI do not become hidden cognition lanes
  3. check that Phase 13 stays below Phase 14 and Phase 16
  4. report any boundary drift to `Program Governor`
- required cross-checks:
  - no hidden-model loophole
  - no silent degrade path
  - no unsafe installer magic
  - no Phase 14 or 16 behavior
  - no approval language
- exit criteria: constitutional objections are resolved or explicitly raised as blockers
- handoff target: `Program Governor`
- anti-drift rule: do not author runtime design or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P13-TC-SC-01`

- task card ID: `P13-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4-mini`
- objective: map every major Phase 13 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-SC-01_PHASE_13_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 2 through 12 plans and execution surfaces
  - inspected donor product-runtime and installer files
- step-by-step work method:
  1. map all ten Phase 13 subsystems
  2. assign one allowed disposition to each subsystem
  3. flag where exact contract inheritance is stronger than whole-shell portability
  4. pass unresolved seam notes to `Architecture & Contract Lead` and `Program Governor`
- required cross-checks:
  - no fifth disposition
  - no silent omission
  - no treating donor shells as earned AGIFCore runtime
- exit criteria: each subsystem has source basis, disposition, and rationale
- handoff target: `Architecture & Contract Lead` then `Program Governor`
- anti-drift rule: do not claim inspected donor code is already valid AGIFCore runtime
- explicit proof that no approval is implied: provenance mapping does not earn the phase

### `P13-TC-ACL-01`

- task card ID: `P13-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 13 boundaries, allowed interfaces, forbidden leaks, and the Phase 13 shell-contract strategy
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-ACL-01_PHASE_13_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- required reads first:
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/03_design/ARCHITECTURE_OVERVIEW.md`
  - `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
  - `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
  - `projects/agifcore_master/03_design/PUBLIC_RELEASE_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 12 plan and runtime surfaces
  - `Source Cartographer` output
- step-by-step work method:
  1. define what belongs in each Phase 13 subsystem only
  2. define allowed lower-phase interfaces
  3. define the supplemental Phase 13 shell-contract strategy
  4. define forbidden Phase 14 and Phase 16 leaks
  5. pass runtime-family implications to `Program Governor` and `Product & Sandbox Pod Lead`
- required cross-checks:
  - no one mixed app shell
  - no direct UI ownership of correctness
  - no gateway bypass path
  - no Phase 14 or 16 semantics
- exit criteria: boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `Product & Sandbox Pod Lead`
- anti-drift rule: do not redesign kernel, memory, graph, simulator, conversation, meta-runtime, or the team
- explicit proof that no approval is implied: boundary framing is planning truth only

### `P13-TC-PSPL-01`

- task card ID: `P13-TC-PSPL-01`
- role owner: `Product & Sandbox Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 13 product-runtime family without crossing into Phase 14 or Phase 16
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-PSPL-01_PHASE_13_PRODUCT_RUNTIME_DECOMPOSITION.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- required reads first:
  - approved Phase 2 through 12 plans and execution surfaces
  - the Phase 13 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
  - `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
- step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/`
  2. keep the module set explicit:
     - `contracts.py`
     - `embeddable_runtime_api.py`
     - `local_runner.py`
     - `local_gateway.py`
     - `desktop_ui.py`
     - `state_export.py`
     - `trace_export.py`
     - `memory_review_export.py`
     - `safe_shutdown.py`
     - `fail_closed_ux.py`
     - `installer_distribution.py`
     - `product_runtime_shell.py`
  3. order implementation so contracts come first, then runner and API, then gateway, then exports, then shutdown, then fail-closed UX, then desktop UI, then installer/distribution, and the thin shell last
  4. identify where lower-phase exports and runner inputs must be consumed without mutation
- required cross-checks:
  - no runtime code written now
  - no Phase 14 behavior
  - no Phase 16 behavior
  - no hidden autonomy or hidden correctness path
- exit criteria: future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase

### `P13-TC-TRL-01`

- task card ID: `P13-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4-mini`
- objective: define the Phase 13 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-TRL-01_PHASE_13_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 12 verifier and evidence families
  - the Phase 13 draft
- step-by-step work method:
  1. define one verifier per major Phase 13 subsystem
  2. define cross-cutting gateway no-bypass, fail-closed, export-integrity, shutdown, and installer checks
  3. define evidence reports and manifest contents
  4. define end-to-end, fail-closed UX, and installer/distribution demo verification hooks
- required cross-checks:
  - tests must verify separation between API, runner, gateway, UI, exports, shutdown, and installer
  - fail-closed paths must be machine-checkable and visible
  - exports must be trace-contract aligned
  - installer flow must prove local installability without public-release claims
- exit criteria: later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P13-TC-ASA-01`

- task card ID: `P13-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4-mini`
- objective: audit the Phase 13 planning package for fake completeness, giant-shell collapse, fake exports, fake fail-closed UX, fake installer flow, and phase-leak drift
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-ASA-01_PHASE_13_PLAN_AUDIT.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- required reads first:
  - full Phase 13 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` boundary output
  - `Test & Replay Lead` evidence-plan output
  - relevant approved Phase 2 through 12 plan and runtime surfaces
- step-by-step work method:
  1. check that all required sections exist
  2. check that each major subsystem has a source basis and disposition
  3. check that no one giant app shell is being passed off as design
  4. check that no approval or completion claim is implied
- required cross-checks:
  - no blind rewrite where a plausible substrate exists
  - no silent omission of any required subsystem
  - no Phase 14 or 16 behavior smuggled in
  - no empty export, fail-closed, or installer proof path
- exit criteria: all blockers are either cleared or explicitly raised
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P13-TC-VA-01`

- task card ID: `P13-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 13 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-VA-01_PHASE_13_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- required reads first:
  - full Phase 13 draft
  - audit output
  - Governor verification output
  - validation protocol
- step-by-step work method:
  1. confirm the plan is decision-complete
  2. confirm every closure requirement has a later artifact path
  3. confirm the later demos are inspectable and truthful
  4. confirm role separation and review-surface completeness
- required cross-checks:
  - no author and validator role collision
  - no missing review surface
  - no implied approval
- exit criteria: review request scope is exact and inspectable
- handoff target: `Program Governor`
- anti-drift rule: do not author plan content or runtime behavior
- explicit proof that no approval is implied: validation asks for review and does not mark the phase earned

### `P13-TC-REL-01`

- task card ID: `P13-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4-mini`
- objective: define the later Phase 13 demo-bundle shape and review packet order
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/P13-TC-REL-01_PHASE_13_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 14 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 12 demo bundle
  - `Test & Replay Lead` verifier and evidence plan
  - the Phase 13 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the end-to-end product demo surface
  3. define the fail-closed UX demo surface
  4. define the installer/distribution demo surface
  5. define the user-review packet order
- required cross-checks:
  - demos must stay inspectable from files alone
  - no demo may imply acceptance or phase completion
  - no public-release or publication packaging creep
- exit criteria: later review packet is exact, ordered, and bounded
- handoff target: `Program Governor` then `Validation Agent`
- anti-drift rule: do not expand into release execution or public claims
- explicit proof that no approval is implied: demo-package planning is not demo acceptance

## 13. Closure-gate mapping

| Closure requirement | Artifact(s) that will satisfy it later | Role responsible | How it will be checked | What failure would look like |
| --- | --- | --- | --- | --- |
| embeddable runtime API exists | `embeddable_runtime_api.py`, `verify_phase_13_runtime_api.py`, `phase_13_runtime_api_report.json` | `Product & Sandbox Pod Lead` | verifier confirms typed local surfaces, surface ceilings, and blocked/fail-closed control surfaces | host API claims with no typed surface set or no blocked-surface proof |
| local runner exists | `local_runner.py`, `verify_phase_13_local_runner.py`, `phase_13_local_runner_report.json` | `Product & Sandbox Pod Lead` | verifier confirms governed turn execution, trace refs, memory-review handoff, and lifecycle receipts | second runtime behavior, missing trace refs, or no lifecycle evidence |
| local gateway exists | `local_gateway.py`, `verify_phase_13_local_gateway.py`, `phase_13_local_gateway_report.json` | `Product & Sandbox Pod Lead` | verifier confirms schema validation, policy-hash enforcement, no-bypass order, and deterministic denial reasons | direct runner bypass, missing policy-hash checks, or opaque allow/deny results |
| local desktop UI exists | `desktop_ui.py`, `verify_phase_13_desktop_ui.py`, `phase_13_desktop_ui_report.json` | `Product & Sandbox Pod Lead` | verifier confirms presentation-only behavior, evidence visibility, and explicit blocked states | UI owning correctness or hiding blocked states behind fluent success text |
| state export exists | `state_export.py`, `verify_phase_13_state_export.py`, `phase_13_state_export_report.json` | `Product & Sandbox Pod Lead` | verifier confirms provenance-preserving export shape and bounded payload size | unlabeled state dump or export with no replay anchors |
| trace export exists | `trace_export.py`, `verify_phase_13_trace_export.py`, `phase_13_trace_export_report.json` | `Product & Sandbox Pod Lead` | verifier confirms trace-contract fields remain visible and replay anchors persist | trace summary with missing support-state or knowledge-gap fields |
| memory review export exists | `memory_review_export.py`, `verify_phase_13_memory_review_export.py`, `phase_13_memory_review_export_report.json` | `Product & Sandbox Pod Lead` | verifier confirms memory-review refs, continuity refs, and bounded payload size | memory export claims with no memory-review anchors or over-broad dumps |
| safe shutdown exists | `safe_shutdown.py`, `verify_phase_13_safe_shutdown.py`, `phase_13_safe_shutdown_report.json` | `Product & Sandbox Pod Lead` | verifier confirms receipt, snapshot/export handoff, and deterministic safe stop | silent stop path, no receipt, or dropped state with no evidence |
| fail-closed UX exists | `fail_closed_ux.py`, `verify_phase_13_fail_closed_ux.py`, `phase_13_fail_closed_ux_report.json` | `Product & Sandbox Pod Lead` | verifier confirms explicit blocked states, reason codes, and next-step help | labels only, hidden denials, or success-looking UX on blocked actions |
| installer/distribution flow exists | `installer_distribution.py`, `verify_phase_13_installer_distribution.py`, `phase_13_installer_distribution_report.json` | `Product & Sandbox Pod Lead` | verifier confirms local artifact inventory, integrity checks, and reproducible install path | installer notes with no real artifacts, no install proof, or public-release leakage |
| demo path exists | `phase_13_demo_index.md`, `phase_13_end_to_end_product_demo.md`, `phase_13_fail_closed_ux_demo.md`, `phase_13_installer_distribution_demo.md` plus matching `.json` outputs | `Release & Evidence Lead` | direct demo-bundle inspection and rerunnable demo scripts | no inspectable demo or demo claims unsupported by evidence |
| tests/evidence path exists | full verifier family under `05_testing/phase_13_product_runtime_and_ux/` and `phase_13_evidence_manifest.json` | `Test & Replay Lead` | Governor rerun plus validation request | missing verifier coverage, missing manifest, or non-machine-readable evidence |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| end-to-end product demo | `embeddable_runtime_api.py`, `local_runner.py`, `local_gateway.py`, `desktop_ui.py`, all three export modules, `safe_shutdown.py`, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Product & Sandbox Pod Lead` | `Anti-Shortcut Auditor` | session open, one governed conversation turn, gateway decision path, UI presentation, state export, trace export, memory-review export, and safe-shutdown receipt with backing evidence |
| fail-closed UX demo | `local_gateway.py`, `desktop_ui.py`, `fail_closed_ux.py`, bundle-integrity check path, runnable demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Product & Sandbox Pod Lead` | `Anti-Shortcut Auditor` | denied or blocked request, deterministic reason code, fail-closed help surface, proof that runner was not bypassed, and backing evidence refs |
| installer/distribution demo | `installer_distribution.py`, packaged local artifacts, integrity manifest, install verification script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Product & Sandbox Pod Lead` | `Anti-Shortcut Auditor` | artifact inventory, install flow, integrity checks, local run proof, and proof that no Phase 16 public-release behavior was required |

Validation rules for all demos:

- `Validation Agent` prepares the review request only after the standard audit and the Governor verification record exist.
- `Program Governor` is the only role that asks the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.
- If any Phase 14 or Phase 16 behavior appears during Phase 13 execution, the correct action is to stop and escalate boundary drift, not to widen the demo scope.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable product-runtime substrate | compare subsystem plans and later runtime against mapped donor files and exact inherited records | `Source Cartographer` | a subsystem is rebuilt from zero despite a clear donor basis or exact inherited contract surface | stop and reopen reuse mapping before execution |
| one giant app shell pretending to do runner, gateway, UI, exports, shutdown, and installer | boundary audit and verifier-plan audit | `Architecture & Contract Lead` | one opaque module is asked to own most Phase 13 behavior | reject the design and split the lanes before continuing |
| fail-closed UX existing only as labels | fail-closed verifier and demo audit | `Constitution Keeper` | blocked states appear without deterministic reason codes, help surface, or no-bypass proof | stop and require real fail-closed behavior |
| exports existing only as claims | export verifiers and evidence audit | `Test & Replay Lead` | export language appears without machine-readable payloads, bounded sizes, or replay anchors | stop and require real export outputs |
| installer/distribution flow existing only as notes | installer verifier and installer demo audit | `Anti-Shortcut Auditor` | install flow is described without actual artifact inventory, integrity checks, or local run proof | block closure until installer/distribution behavior is real |
| local gateway becoming a hidden second runtime | gateway verifier and boundary audit | `Architecture & Contract Lead` | gateway starts owning cognition, correctness, or lower-phase mutation | stop and remove the gateway overreach |
| local desktop UI owning correctness instead of presentation | UI verifier and demo audit | `Constitution Keeper` | UI text diverges from trace truth or invents success states | stop and re-separate presentation from correctness |
| Phase 13 accidentally absorbing Phase 14 sandbox/profile/scale behavior | boundary audit against the forbidden Phase 14 list | `Architecture & Contract Lead` | sandbox engine wiring, profile manifests, or scale control loops appear in Phase 13 | stop and remove the sandbox/profile dependency |
| Phase 13 accidentally absorbing Phase 16 release/publication behavior | boundary audit against the forbidden Phase 16 list | `Release & Evidence Lead` | release notes, claims matrix, GitHub/public release, or publication packaging appear in Phase 13 | stop and remove the release/publication dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 13 plan artifacts
- after user approval, any future change to the Phase 13 plan requires explicit reopen instruction and a supersession note

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 12 is explicitly `approved` in the live phase-truth files and corroborated by the decision and changelog records.
- Phase 13 remains `open`.
- The required provenance stack, approved Phase 2 through 12 baselines, requirements pack, design pack, admin controls, and donor product-runtime substrate were all reviewed directly.
- No prerequisite blocker was found.
- The main non-blocker seams are:
  - Phase 13 has no AGIFCore shell contract yet and must layer above approved Phase 2 through 12 truth rather than mutate it.
  - the strongest product-runtime substrate is donor-side in tasklet and v2 embedding surfaces, so AGIFCore must port contract and packaging discipline without inheriting unrelated donor-specific product behavior.
  - the donor desktop UI is useful but too mixed to direct-port cleanly, so UI patterns stay adaptation-first by default.
  - the reusable `phase_builder` setup is now aligned to explicitly name `Product & Sandbox Pod Lead`.
- Defaults locked by this draft:
  - later execution keeps one active build pod by default: `Product & Sandbox Pod Lead`
  - embeddable runtime API, local runner, local gateway, state export, trace export, memory review export, safe shutdown, fail-closed UX, and installer/distribution default toward `port_with_provenance`
  - local desktop UI defaults toward `adapt_for_research_only`
  - `task_submit` and `policy_update` stay replay-only or fail-closed by default unless a later approved gate widens them
  - Phase 13 remains a governed product-runtime layer above approved Phase 2 through 12 outputs and below Phase 14 and Phase 16 behavior
