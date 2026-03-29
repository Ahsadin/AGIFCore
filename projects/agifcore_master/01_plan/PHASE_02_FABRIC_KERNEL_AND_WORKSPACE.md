# Phase 2: Fabric Kernel and Workspace

## Summary

Phase 2 is the first runtime-building phase, but it is not a blank-slate rewrite. The execution default is:

- reuse the strongest fabric and workspace substrate from `agif_fabric_v1`
- reuse the strongest contract and fail-closed discipline from `agif-tasklet-cell`
- keep `root v2 lineage` and `agif_v2_master` as historical reference only unless the frozen provenance package explicitly justifies a carry decision
- keep one active build pod by default in later execution: `Kernel Pod Lead`

This phase plans the later build of:

- typed event fabric
- event bus
- shared workspace state
- cell registry
- lifecycle engine
- scheduler
- replay ledger
- rollback
- quarantine
- fail-closed kernel behavior

This file is planning-only and does not create runtime code, testing code, or execution scaffolds by itself.

## 1. Phase identity

- Phase number: `2`
- Canonical phase name: `Fabric Kernel and Workspace`
- Status: `planning_draft`
- Canonical artifact path: `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
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
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/01_plan/HUMAN_THINKING_TARGET.md`
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - all files in `projects/agifcore_master/02_requirements/`
  - all files in `projects/agifcore_master/03_design/`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`

## 2. Phase mission

- Phase 2 exists to define and later build the governed kernel substrate that later cells, memory, graph, simulator, and conversation phases depend on.
- Phase 2 must build later:
  - typed event fabric
  - event bus
  - shared workspace state
  - cell registry
  - lifecycle engine
  - scheduler
  - replay ledger
  - rollback
  - quarantine
  - fail-closed kernel behavior
- Phase 2 must not:
  - implement Phase 3 cell contracts, tissue manifests, or bundle structure
  - implement Phase 4 memory planes
  - implement Phase 5 graph persistence
  - implement conversation behavior beyond contract-safe kernel hooks
  - weaken Phase 1 trace, governance, or approval rules
  - claim inherited code is already valid AGIFCore runtime
  - approve itself

## 3. Scope and non-goals

### In scope

- this Phase 2 planning artifact
- the Phase 2 task-card map
- per-subsystem reuse and provenance strategy
- the future execution-family plan for `04_execution/phase_02_fabric_kernel_and_workspace/`
- the future testing-family plan for `05_testing/phase_02_fabric_kernel_and_workspace/`
- the future outputs, evidence, and demo family plan for `06_outputs/phase_02_fabric_kernel_and_workspace/`
- the later audit, governor-verification, validation-request, and user-review path

### Out of scope

- any runtime implementation in this planning artifact
- any file under `04_execution/` as part of plan authoring alone
- Phase 3 cell and tissue planning
- Phase 4 memory implementation
- Phase 5 graph implementation
- product shell, gateway, sandbox, installer, or release execution
- any commit, freeze, tag, merge, or approval action by this file alone

### Phase 2 memory-hook surface

Phase 2 may expose only a bounded kernel-facing memory-hook surface.

Allowed at most:

- workspace-safe state anchors
- replay and rollback state references
- kernel-safe retention or review hook points that hand later work to memory-review surfaces
- retention-candidate or review-needed references that do not themselves implement memory policy

Explicitly forbidden in Phase 2:

- semantic memory
- procedural memory
- reviewed long-term memory
- promotion logic
- compression logic
- forgetting logic
- retirement logic
- graph persistence
- long-term memory storage policy
- memory-plane-specific algorithms from Phase 4

### Phase 2 budget envelope

These are planning ceilings for later Phase 2 execution on the primary laptop-oriented reference profile. They are not achieved measurements.

| Budget item | Planning ceiling | Use |
| --- | --- | --- |
| max resident RAM for Phase 2 runtime | `<= 2 GiB` | stop and escalate if exceeded |
| max shared-workspace state size before pruning or escalation | `<= 256 MiB` | keep workspace bounded and inspectable |
| max replay-ledger growth before rotation or export | `<= 512 MiB` | keep replay local and reviewable |
| max rollback snapshot budget | `<= 8 snapshots` and `<= 1 GiB` total | preserve bounded rollback control |
| max event size | `<= 256 KiB` | prevent oversized payload drift |
| max event queue depth | `<= 1024` | prevent silent backlog growth |
| max scheduler latency target | `<= 50 ms` planning target | subject to later measurement |
| max quarantine response-time target | `<= 250 ms` planning target | subject to later measurement |
| max demo and evidence bundle size | `<= 250 MiB` | keep review packet inspectable on laptop |

Budget rule:

- these are Phase 2 planning ceilings only
- later execution must measure against them
- if a ceiling is exceeded, stop and escalate to Program Governor instead of silently widening the envelope

### Explicit statement

Phase 3 and later phases remain untouched by this plan.

## 4. Phase 1 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 1 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` both show Phase 1 `approved` | Phase 2 planning may proceed |
| Required Phase 1 artifacts relied on exist | `pass` | provenance package, trace contract, validation and demo protocol, requirement pack, and design pack exist | planning has the required inputs |
| Dependency gaps that block planning | `none` | no missing prerequisite artifact blocks planning | no prerequisite stop |
| Non-blocker note | `present` | `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md` still contains historical in-document `Status: open` text | treat `PHASE_INDEX.md` and `PHASE_GATE_CHECKLIST.md` as authoritative gate truth |
| Blockers vs non-blockers | `planning not blocked` | current gaps are only expected missing Phase 2 artifacts, not Phase 1 prerequisites | readiness is `ready_for_user_review` |

## 5. Active team map for Phase 2

| Role | Model tier | Status | Why | Exact responsibility this phase | Must never do this phase |
| --- | --- | --- | --- | --- | --- |
| User | none | active | final human approver | later approve or reject the Phase 2 plan | delegate final approval |
| Program Governor | `gpt-5.4` | active | top phase authority | own prerequisite truth, plan integration, work order, artifact matrix, and gate alignment | implement runtime code, self-approve, broaden into Phase 3 |
| Constitution Keeper | `gpt-5.4 mini` | active | drift control | guard non-negotiables, fail-closed honesty, memory-hook boundary, and Phase 2 scope | author runtime design on its own, approve phase |
| Source Cartographer | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | inherited substrate is central | map each Phase 2 subsystem to source basis, disposition, and provenance expectations | port code as already done, invent a fifth disposition, approve phase |
| Architecture & Contract Lead | `gpt-5.4` | active | kernel and workspace boundary owner | own event model framing, workspace boundary, registry, lifecycle, and scheduler boundaries, and trace alignment | drift into Phase 3 or 4 implementation, weaken Phase 1 contracts, approve phase |
| Kernel Pod Lead | `gpt-5.3-codex` | active for build decomposition planning only | later execution owner for Phase 2 | decompose future execution slices, file targets, rollback boundaries, and one-pod build order | implement runtime code in this planning run, activate extra build pods casually, approve phase |
| Memory & Graph Pod Lead | `gpt-5.3-codex` | inactive | Phase 2 must not absorb Phase 4 or 5 | none unless a narrow boundary ambiguity blocks planning | absorb memory or graph scope |
| World & Conversation Pod Lead | `gpt-5.3-codex` | inactive | not needed for kernel planning | none | absorb Phase 6 through 9 scope |
| Meta & Growth Pod Lead | `gpt-5.3-codex` | inactive | danger zone and unnecessary here | none | activate casually or leak self-improvement into Phase 2 |
| Product & Sandbox Pod Lead | `gpt-5.3-codex` | inactive | runner, gateway, and UI split is already frozen in Phase 1 | none unless a narrow shell seam becomes unclear | absorb Phase 13 through 16 scope |
| Test & Replay Lead | `gpt-5.4 mini` | active | replay and rollback are first-class | define tests, replay checks, rollback checks, quarantine checks, fail-closed checks, and evidence expectations | implement runtime behavior, approve phase |
| Anti-Shortcut Auditor | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | high risk of fake kernel completeness or blind rewrite | detect omission, greenfield drift, unsupported closure claims, and scope leakage | author canonical content, downgrade blockers, approve phase |
| Merge Arbiter | `gpt-5.3-codex` | inactive | planning-only run | none until later execution integration is needed | author plan content or approve phase |
| Validation Agent | `gpt-5.4` | active | final machine-side plan review | validate the Phase 2 plan package and prepare the later review request | author the plan or approve phase |
| Release & Evidence Lead | `gpt-5.4 mini` | active | later demos must be inspectable | define demo bundle shape and evidence grouping only | perform release execution or public-claim packaging |

## 6. Reuse and provenance strategy

Only the frozen four disposition categories are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

Where a row below refers to a reusable substrate or architectural pattern rather than one literal historical module, that clarification appears in rationale only and does not create a new disposition type.

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance justification |
| --- | --- | --- | --- | --- |
| typed event fabric | `SRC-001 agif_fabric_v1` exact names `EventType`, `Event`, `CellContract`; `SRC-002` contract discipline | `port_with_provenance` | the typed fabric substrate already exists and should be ported with AGIFCore verification rather than reinvented | `COMPONENT_CATALOG.md` `CC-001` to `CC-003`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-027` |
| event bus | `SRC-001` shared workspace coordination and `runner/cell fabric` operator family; `SRC-002` schema-enforced contracts | `port_with_provenance` | this is a substrate-pattern carry decision, not a claim that one literal historical `event_bus.py` already exists | `COMPONENT_CATALOG.md` `CC-037`, `CC-038`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-001`, `SIM-002`, `SIM-027` |
| shared workspace state | `SRC-001 agif_fabric_v1` shared workspace coordination | `port_with_provenance` | workspace is one of the strongest v1 carry surfaces and is explicitly named in the master plan | `COMPONENT_CATALOG.md` `CC-037`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-001`; `WORKSPACE_MODEL.md` |
| cell registry | `SRC-001` exact names `LogicalCell` and `CellRegistry` | `port_with_provenance` | registry surface already exists and should be ported before later Phase 3 cell and tissue expansion | `COMPONENT_CATALOG.md` `CC-004`, `CC-005` |
| lifecycle engine | `SRC-001` exact `LifecycleEngine` and explicit lifecycle verbs | `port_with_provenance` | lifecycle control already exists as a strong v1 substrate and should be ported with AGIFCore checks | `COMPONENT_CATALOG.md` `CC-006`, `CC-039`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-003` |
| scheduler | `SRC-001` exact `Scheduler` plus need signals and routing with utility scoring | `port_with_provenance` | scheduler and resource control is already a v1 substrate and aligns to the locked scheduler or resource cell-family role | `COMPONENT_CATALOG.md` `CC-007`, `CC-047`, `CC-048`; `CELL_FAMILIES.md` |
| replay ledger | `SRC-001` lineage ledger and audit or replay support; `SRC-002` deterministic trace verification patterns | `port_with_provenance` | ledger structure should port from v1 while determinism verification patterns are rebuilt around it | `COMPONENT_CATALOG.md` `CC-016`, `CC-040`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-004`, `SIM-033` |
| rollback | `SRC-001` rollback snapshots and rollback references | `port_with_provenance` | rollback is already an explicit v1 control surface and should not be redesigned from zero | `COMPONENT_CATALOG.md` `CC-042`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-006` |
| quarantine | `SRC-001` quarantine and containment plus quarantined lifecycle posture | `port_with_provenance` | quarantine is a strong v1 safety substrate and must remain first-class in AGIFCore | `COMPONENT_CATALOG.md` `CC-043`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-007` |
| fail-closed kernel behavior | `SRC-001` authority approvals or vetoes and quarantine posture; `SRC-002` strict policy checks, contracts, and fail-closed discipline | `rebuild_clean` | the policy and integrity ingredients are portable, but the kernel's fail-closed semantics must be rebuilt explicitly for AGIFCore | `COMPONENT_CATALOG.md` `CC-049`, `CC-063`, `CC-065`, `CC-066`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-013`, `SIM-027`, `SIM-029`, `SIM-030`; `TRACE_CONTRACT.md` |

## 7. Artifact ownership matrix

### Artifact ownership matrix

| Artifact path | Primary author | Reviewer | Auditor | Validator | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 truth, provenance, contracts, requirements, design pack, admin controls | all later Phase 2 work | section-complete Phase 2 plan |
| `00_admin/codex_threads/tasks/phase_02/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, this plan | all later Phase 2 work | one task card per active role with disjoint scope |
| `04_execution/phase_02_fabric_kernel_and_workspace/` | `Kernel Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 2 plan, provenance package, trace contract | Phase 2 runtime delivery | later runtime files exist and match scoped targets |
| `05_testing/phase_02_fabric_kernel_and_workspace/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 2 plan, execution family, validation protocol | Phase 2 verification and closeout | later verifier family exists and runs |
| `06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | tests, trace exports, replay logs, demo protocol | audit, governor verification, validation, user demos | later machine-readable evidence bundle is inspectable |
| `06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, validation protocol | user review | later demo bundle exists for kernel trace, replay, rollback and quarantine, and shared workspace |
| `00_admin/codex_threads/handoffs/PHASE_02_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, tests, demos, evidence | validation request | direct verification record exists |
| `00_admin/codex_threads/handoffs/PHASE_02_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdicts are explicit |
| `00_admin/codex_threads/handoffs/PHASE_02_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

### Future family note

- naming future `04_execution/`, `05_testing/`, and `06_outputs/` families in this plan does not create them
- directory or scaffold creation for those families is deferred to the first Phase 2 execution run
- this planning run only freezes names, ownership, and expectations

### First-pass planned future runtime files

Planned execution root:

- `04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/`

Planned first-pass files:

| Planned file | Planned purpose |
| --- | --- |
| `event_types.py` | typed event definitions and allowed kernel event envelopes |
| `event_bus.py` | event dispatch and governed event flow |
| `workspace_state.py` | shared workspace state surface and state anchors |
| `cell_registry.py` | registry of logical cells and kernel-visible identity and state references |
| `lifecycle_engine.py` | activate, split, merge, hibernate, reactivate, retire, and quarantine transitions |
| `scheduler.py` | kernel scheduling and budget control |
| `replay_ledger.py` | replay ledger and trace-linked replay records |
| `rollback_controller.py` | bounded rollback control and restore paths |
| `quarantine_controller.py` | containment and quarantine transitions |
| `kernel_fail_closed.py` | kernel fail-closed decisions, stop states, and refusal paths |

### First-pass planned future testing files

Planned testing root:

- `05_testing/phase_02_fabric_kernel_and_workspace/`

Planned first-pass files:

| Planned file | Planned purpose |
| --- | --- |
| `verify_phase_02_kernel_trace.py` | event flow and kernel trace verification |
| `verify_phase_02_workspace_state.py` | shared workspace state verification |
| `verify_phase_02_lifecycle.py` | lifecycle transition verification |
| `verify_phase_02_scheduler.py` | scheduler and budget verification |
| `verify_phase_02_replay.py` | replay determinism and replay-ledger verification |
| `verify_phase_02_rollback_quarantine.py` | rollback and quarantine verification |
| `verify_phase_02_fail_closed.py` | fail-closed negative-case verification |

### First-pass planned future outputs and evidence files

Planned outputs root:

- `06_outputs/phase_02_fabric_kernel_and_workspace/`

Planned first-pass files:

| Planned file | Planned purpose |
| --- | --- |
| `phase_02_evidence_manifest.json` | machine-readable Phase 2 evidence index |
| `phase_02_kernel_trace_demo.md` | kernel trace demo surface |
| `phase_02_replay_report.json` | replay results and anchors |
| `phase_02_rollback_quarantine_report.json` | rollback and quarantine evidence |
| `phase_02_workspace_state_report.json` | shared workspace inspection report |
| `phase_02_fail_closed_report.json` | fail-closed negative-case evidence |

## 8. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| phase control and prerequisite reconciliation | freeze scope, active roles, task-card map, and closure chain | `Program Governor` | `Constitution Keeper` | main Phase 2 plan and task-card map | Phase 1 approved in live phase-truth files | active and inactive roles are fixed and Phase 2 stays inside scope |
| kernel boundary and architecture framing | freeze kernel, event, workspace, registry, lifecycle, scheduler, replay, rollback, quarantine, and fail-closed boundaries | `Architecture & Contract Lead` | `Program Governor`, `Constitution Keeper` | kernel boundary framing and execution-family structure | provenance package and Phase 1 design pack reviewed | every Phase 2 subsystem has an explicit boundary |
| typed event fabric and event bus planning | define typed event admission, event flow, and governed dispatch rules | `Architecture & Contract Lead` | `Source Cartographer`, `Kernel Pod Lead` | event-model and event-bus plan | kernel boundary framing started | typed event and dispatch path are explicit and trace-safe |
| shared workspace and registry planning | define shared state, registry role, replay anchors, and the bounded memory-hook surface | `Architecture & Contract Lead` | `Source Cartographer`, `Kernel Pod Lead`, `Constitution Keeper` | workspace and registry plan | workspace model and provenance reviewed | workspace-safe anchors are explicit and memory overreach is blocked |
| lifecycle, scheduler, and budget-control planning | freeze lifecycle verbs, scheduler responsibilities, and budget-envelope enforcement points | `Kernel Pod Lead` | `Architecture & Contract Lead`, `Constitution Keeper`, `Source Cartographer` | execution decomposition for lifecycle, scheduler, and budget control | workspace and registry framing stable | later execution order is rollback-safe and one-pod by default |
| replay, rollback, quarantine, and fail-closed planning | define recovery, containment, and stop-state proofs | `Architecture & Contract Lead` | `Kernel Pod Lead`, `Test & Replay Lead` | replay, rollback, quarantine, and fail-closed plan | event, workspace, lifecycle boundaries stable | all recovery and refusal paths have later verify and demo expectations |
| test, demo, validation, and evidence planning | define verifier family, evidence family, demo family, and review path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | test plan, evidence plan, demo plan, validation surface | subsystem boundaries stable | later review path is inspectable and machine-readable |

## 9. Ordered execution sequence

1. `Program Governor` verifies Phase 1 approval truth and opens the Phase 2 task-card set.
2. `Source Cartographer` maps every Phase 2 subsystem to source basis and disposition.
3. `Architecture & Contract Lead` drafts kernel, event, workspace, registry, lifecycle, scheduler, replay, rollback, quarantine, and fail-closed boundaries in parallel with step 2.
4. `Constitution Keeper` reviews steps 2 and 3 for constitution drift, hidden-autonomy wording, and memory-hook overreach.
5. `Kernel Pod Lead` decomposes the future execution slices only after steps 2 through 4 stabilize reuse and boundary choices.
6. `Test & Replay Lead` and `Release & Evidence Lead` define verifier, evidence, and demo families after execution decomposition exists.
7. `Program Governor` consolidates the Phase 2 plan, ownership matrix, closure map, budget envelope, and execution-governance rules.
8. `Anti-Shortcut Auditor` audits the full Phase 2 plan package.
9. `Program Governor` independently verifies the audited planning package.
10. `Validation Agent` prepares the later user review request.
11. User review happens only after the validated planning package exists.

Safe parallelism:

- `Source Cartographer` and `Architecture & Contract Lead` may work in parallel
- `Kernel Pod Lead` waits for stable reuse and boundary outputs
- `Test & Replay Lead` and `Release & Evidence Lead` wait for stable execution decomposition
- `Merge Arbiter` stays inactive in planning-only work

Execution-governance stop rules for the later execution run:

- if later Phase 2 execution expands active roles beyond one build pod without explicit Program Governor approval, stop
- if later Phase 2 execution needs stronger machines or wider resource budgets than the primary laptop-oriented profile supports, stop and escalate
- if later Phase 2 execution evidence or log volume grows beyond the planned Phase 2 bundle ceilings, stop and reopen planning
- if later Phase 2 execution tries to widen the memory-hook surface beyond kernel anchors, stop and reopen planning
- if later execution needs new provenance disposition vocabulary, stop and reject the change

## 10. Detailed task cards

User is active approval-only and does not receive a task card.

### `P2-TC-PG-01`

- Role owner: `Program Governor`
- Model tier: `gpt-5.4`
- Objective: own the Phase 2 plan, prerequisite truth, task-card map, budget envelope, and closure chain
- Exact files allowed to touch:
  - `01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `00_admin/codex_threads/tasks/phase_02/P2-TC-PG-01_PHASE_2_GOVERNOR_CONTROL.md`
- Files forbidden to touch:
  - `01_plan/MASTER_PLAN.md`
  - all `04_execution/*`
  - all Phase 3+ artifacts
  - Phase 1 truth files except prerequisite-mismatch note if needed
- Required reads first:
  - repo and project truth files
  - live phase-truth files
  - Phase 1 provenance package
  - Phase 1 contract, requirement, and design packs
  - admin control stack
- Step-by-step work method:
  1. verify Phase 1 approval in live phase-truth files
  2. define active and inactive roles for Phase 2 planning
  3. define reuse strategy, workstreams, future artifact families, and closure map
  4. add budget envelope and stop-and-escalate rules
  5. reconcile all role outputs into one plan
- Required cross-checks:
  - no Phase 3 scope
  - no fifth disposition category
  - no implementation claims
- Exit criteria:
  - Phase 2 plan is section-complete and decision-complete
- Handoff target: `Anti-Shortcut Auditor`
- Anti-drift rule: do not let planning language imply implementation or approval
- Explicit proof that no approval is implied: task ends at planning readiness only; Phase 2 stays `open`

### `P2-TC-CK-01`

- Role owner: `Constitution Keeper`
- Model tier: `gpt-5.4 mini`
- Objective: guard non-negotiables, fail-closed honesty, and memory-hook boundary discipline
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_02/P2-TC-CK-01_PHASE_2_CONSTITUTION_GUARD.md`
- Files forbidden to touch:
  - all `04_execution/*`
  - all `03_design/*`
  - all provenance files as author
- Required reads first:
  - `01_plan/SYSTEM_CONSTITUTION.md`
  - `02_requirements/NON_NEGOTIABLES.md`
  - `02_requirements/PHASE_APPROVAL_RULES.md`
  - `01_plan/TRACE_CONTRACT.md`
  - `03_design/WORKSPACE_MODEL.md`
  - the Phase 2 plan draft
- Step-by-step work method:
  1. check that workspace is not described as hidden autonomy
  2. check that rollback, quarantine, replay, and fail-closed paths remain explicit
  3. check that memory hooks stay inside the bounded surface
  4. flag any Phase 3 or Phase 4 drift
- Required cross-checks:
  - no hidden-model or cloud-correctness loopholes
  - no long-term memory logic in Phase 2
  - no self-approval path
- Exit criteria:
  - all constitutional objections are resolved or explicitly blocked
- Handoff target: `Program Governor`
- Anti-drift rule: do not author architecture or implementation
- Explicit proof that no approval is implied: constitutional review is not phase approval

### `P2-TC-SC-01`

- Role owner: `Source Cartographer`
- Model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- Objective: map each Phase 2 subsystem to source basis, disposition, and provenance expectations
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_02/P2-TC-SC-01_PHASE_2_KERNEL_PROVENANCE_AND_REUSE.md`
- Files forbidden to touch:
  - all `04_execution/*`
  - all `02_requirements/*`
  - all `03_design/*`
- Required reads first:
  - `01_plan/COMPONENT_CATALOG.md`
  - `01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `01_plan/RUNTIME_REBUILD_MAP.md`
  - Phase 0 source-freeze artifacts
  - historical source roots when needed
- Step-by-step work method:
  1. map each Phase 2 subsystem to the strongest source basis
  2. select one frozen disposition only
  3. clarify in notes when the carry decision is substrate-level rather than a literal module carry
  4. flag any subsystem with weak or ambiguous provenance
- Required cross-checks:
  - no silent omission of a subsystem
  - no fifth disposition category
  - no v2 runtime treated as portable truth
- Exit criteria:
  - every required Phase 2 subsystem has explicit provenance and rationale
- Handoff target: `Architecture & Contract Lead` then `Program Governor`
- Anti-drift rule: do not claim mapped historical code is already valid AGIFCore runtime
- Explicit proof that no approval is implied: provenance mapping does not earn the phase

### `P2-TC-ACL-01`

- Role owner: `Architecture & Contract Lead`
- Model tier: `gpt-5.4`
- Objective: freeze kernel, workspace, event, and state boundaries below later phases and above bare storage
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_02/P2-TC-ACL-01_PHASE_2_KERNEL_AND_WORKSPACE_ARCHITECTURE.md`
- Files forbidden to touch:
  - all `04_execution/*`
  - all Phase 3+ plan artifacts
  - Phase 1 canonical design files as edits
- Required reads first:
  - `01_plan/TRACE_CONTRACT.md`
  - `03_design/ARCHITECTURE_OVERVIEW.md`
  - `03_design/WORKSPACE_MODEL.md`
  - `03_design/GOVERNANCE_MODEL.md`
  - `03_design/PRODUCT_RUNTIME_MODEL.md`
  - `03_design/FORMAL_MODELS.md`
  - provenance outputs from `SC`
- Step-by-step work method:
  1. define typed event admission and event-bus boundaries
  2. define shared workspace state and registry boundaries
  3. define lifecycle, scheduler, replay, rollback, quarantine, and fail-closed boundaries
  4. define the bounded memory-hook surface
  5. align all boundaries to trace and export surfaces
- Required cross-checks:
  - runner, gateway, and UI split remains intact
  - no Phase 3 cell or bundle behavior
  - no Phase 4 memory implementation
- Exit criteria:
  - every kernel subsystem has an explicit boundary and later proof path
- Handoff target: `Kernel Pod Lead` then `Program Governor`
- Anti-drift rule: do not redesign the product runtime stack above the kernel
- Explicit proof that no approval is implied: architecture framing is planning truth only

### `P2-TC-KPL-01`

- Role owner: `Kernel Pod Lead`
- Model tier: `gpt-5.3-codex`
- Objective: decompose the later Phase 2 implementation into one-pod, rollback-safe execution slices
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_02/P2-TC-KPL-01_PHASE_2_KERNEL_EXECUTION_DECOMPOSITION.md`
- Files forbidden to touch:
  - all `04_execution/*` in this planning run
  - all Phase 3+ plan artifacts
  - all test and output families as edits
- Required reads first:
  - the Phase 2 plan draft
  - Phase 1 provenance package
  - Phase 1 workspace, governance, and product-runtime models
- Step-by-step work method:
  1. split later execution into kernel-core, workspace-state, and recovery-control slices
  2. keep one active build pod as the default
  3. define rollback boundaries between slices
  4. define which verifier family must pass before the next slice starts
- Required cross-checks:
  - no runtime code is written in this planning run
  - no extra build pod is activated
  - no Phase 3 scope is pulled forward
- Exit criteria:
  - later execution order is decision-complete and rollback-safe
- Handoff target: `Test & Replay Lead` and `Program Governor`
- Anti-drift rule: do not turn decomposition into hidden implementation
- Explicit proof that no approval is implied: decomposition defines later work only

### `P2-TC-TRL-01`

- Role owner: `Test & Replay Lead`
- Model tier: `gpt-5.4 mini`
- Objective: define the Phase 2 verifier family, replay checks, rollback checks, quarantine checks, fail-closed checks, and evidence outputs
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_02/P2-TC-TRL-01_PHASE_2_TEST_AND_REPLAY_PLAN.md`
- Files forbidden to touch:
  - all `04_execution/*`
  - all Phase 1 canonical content
- Required reads first:
  - `01_plan/VALIDATION_PROTOCOL.md`
  - `01_plan/DEMO_PROTOCOL.md`
  - `01_plan/TRACE_CONTRACT.md`
  - `01_plan/PROOF_DOMAIN_MATRIX.md`
  - the Phase 2 plan draft
- Step-by-step work method:
  1. define the `verify_phase_02_*` family
  2. define replay determinism checks
  3. define rollback restoration and quarantine containment checks
  4. define fail-closed negative cases
  5. define machine-readable evidence outputs
- Required cross-checks:
  - every required subsystem has a planned verifier
  - replay and rollback are not prose-only promises
  - fail-closed behavior is tested negatively
- Exit criteria:
  - later test and evidence paths are exact enough to implement without new decisions
- Handoff target: `Release & Evidence Lead` then `Program Governor`
- Anti-drift rule: do not implement runtime behavior through test planning
- Explicit proof that no approval is implied: verification planning does not earn the phase

### `P2-TC-REL-01`

- Role owner: `Release & Evidence Lead`
- Model tier: `gpt-5.4 mini`
- Objective: define the later user-facing Phase 2 demo and evidence bundle
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_02/P2-TC-REL-01_PHASE_2_DEMO_AND_EVIDENCE_PLAN.md`
- Files forbidden to touch:
  - all `04_execution/*`
  - all public release artifacts
- Required reads first:
  - `01_plan/DEMO_PROTOCOL.md`
  - `01_plan/VALIDATION_PROTOCOL.md`
  - the Phase 2 plan draft
  - `TRL` outputs when available
- Step-by-step work method:
  1. define the demo bundle shape for kernel trace, replay, rollback or quarantine, and shared workspace
  2. define which evidence is machine-readable and which is human-facing
  3. define the later review packet order
- Required cross-checks:
  - no release or publication drift
  - no missing demo surface
  - no evidence summary without real underlying files
- Exit criteria:
  - later user review packet is exact and inspectable
- Handoff target: `Program Governor` then `Validation Agent`
- Anti-drift rule: do not expand into Phase 16 release work
- Explicit proof that no approval is implied: demo-package planning is not demo acceptance

### `P2-TC-ASA-01`

- Role owner: `Anti-Shortcut Auditor`
- Model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- Objective: audit the Phase 2 plan package for drift, omission, and fake completeness
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_02/P2-TC-ASA-01_PHASE_2_PLAN_AUDIT.md`
  - `00_admin/codex_threads/tasks/phase_02/P2-AUDIT-01_PHASE_2_PLAN_AUDIT_REPORT.md`
- Files forbidden to touch:
  - canonical plan content
  - all `04_execution/*`
- Required reads first:
  - the complete Phase 2 planning package
  - task-card template
  - validation protocol
  - Phase 1 provenance package
- Step-by-step work method:
  1. check every required subsystem is represented
  2. check reuse decisions against the provenance package
  3. check that memory hooks stay bounded
  4. check that budget envelope and stop rules exist
  5. check that no Phase 3 scope leaked in
  6. write explicit blockers or pass results
- Required cross-checks:
  - no greenfield rewrite where v1 or tasklet substrate exists
  - no fifth disposition category
  - no implementation claims
- Exit criteria:
  - audit report explicitly states pass or blockers with file-backed reasons
- Handoff target: `Program Governor`
- Anti-drift rule: do not rewrite the plan instead of auditing it
- Explicit proof that no approval is implied: audit pass is not phase approval

### `P2-TC-VA-01`

- Role owner: `Validation Agent`
- Model tier: `gpt-5.4`
- Objective: validate the Phase 2 planning package and prepare the user review request
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_02/P2-TC-VA-01_PHASE_2_VALIDATION_REQUEST.md`
  - later `00_admin/codex_threads/handoffs/PHASE_02_VALIDATION_REQUEST.md`
- Files forbidden to touch:
  - canonical plan content
  - any runtime code or test code
  - user verdict files
- Required reads first:
  - audited Phase 2 plan package
  - governor verification record when it exists
  - validation protocol
- Step-by-step work method:
  1. read the audited Phase 2 plan package
  2. identify exact review surfaces and what the user must inspect
  3. state pass, fail, blockers, and allowed verdicts
  4. hand the review request back to `Program Governor`
- Required cross-checks:
  - no self-validation by an authoring role
  - every requested review surface points to a real planned artifact
  - no approval language before user verdict
- Exit criteria:
  - validation request is exact enough for user review with no missing surface
- Handoff target: `Program Governor`
- Anti-drift rule: do not author plan content or runtime behavior
- Explicit proof that no approval is implied: validation request asks for review; it does not mark the phase earned

## 11. Closure-gate mapping

| Phase 2 closure requirement | Artifact(s) that must satisfy it later | Responsible role | How it will be checked | What failure looks like |
| --- | --- | --- | --- | --- |
| typed event fabric exists | `04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_types.py`, `event_bus.py`, `verify_phase_02_kernel_trace.py` | `Kernel Pod Lead` | typed events and event flow exist and are trace-backed | ad hoc event payloads or no trace anchors |
| event bus exists | `event_bus.py` and kernel trace demo | `Kernel Pod Lead` | dispatch path is explicit and inspectable | hidden dispatch inside unrelated state code |
| shared workspace state exists | `workspace_state.py` and `verify_phase_02_workspace_state.py` | `Kernel Pod Lead` | shared state and state anchors are explicit | workspace is missing or behaves like hidden memory |
| registry exists | `cell_registry.py` and lifecycle tests | `Kernel Pod Lead` | registry records and identity or state linkage are present | cell references are ad hoc or opaque |
| lifecycle exists | `lifecycle_engine.py` and `verify_phase_02_lifecycle.py` | `Kernel Pod Lead` | lifecycle verbs exist and are bounded | incomplete or untestable transitions |
| scheduler exists | `scheduler.py` and `verify_phase_02_scheduler.py` | `Kernel Pod Lead` | scheduling and budget behavior are explicit | implicit scheduling or ignored budgets |
| replay exists | `replay_ledger.py` and `verify_phase_02_replay.py` | `Test & Replay Lead` | replay determinism and ledger anchors pass | replay cannot reproduce prior state |
| rollback exists | `rollback_controller.py` and `verify_phase_02_rollback_quarantine.py` | `Test & Replay Lead` | restoration from a known-good point works | rollback is descriptive only |
| quarantine exists | `quarantine_controller.py` and `verify_phase_02_rollback_quarantine.py` | `Test & Replay Lead` | unsafe state is contained and prevented from proceeding | quarantine has no real containment effect |
| fail-closed kernel behavior exists | `kernel_fail_closed.py` and `verify_phase_02_fail_closed.py` | `Test & Replay Lead` | negative cases reject or halt safely with inspectable reason | unsafe continuation or silent downgrade |
| demo path exists | `06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/` | `Release & Evidence Lead` | all four required demos exist and point to real evidence | missing or narrative-only demo surface |
| tests and evidence path exists | `05_testing/phase_02_fabric_kernel_and_workspace/` and `06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/` | `Test & Replay Lead` | verifier family runs and outputs are machine-readable | no verifier family or no evidence package |

## 12. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| kernel trace demo | typed event fabric, event bus, registry or lifecycle interaction, trace export, `verify_phase_02_kernel_trace.py` output | `Test & Replay Lead` with `Kernel Pod Lead` support | `Anti-Shortcut Auditor` | event admission, dispatch, lifecycle touchpoints, trace anchors, and fail-closed refusal path |
| replay demo | replay ledger, deterministic replay verifier, replay evidence manifest | `Test & Replay Lead` | `Anti-Shortcut Auditor` | one recorded run, one replayed run, and matching anchors |
| rollback or quarantine demo | rollback point, failed-state injection, quarantine trigger, restoration evidence, `verify_phase_02_rollback_quarantine.py` output | `Test & Replay Lead` with `Kernel Pod Lead` support | `Anti-Shortcut Auditor` | unsafe path is quarantined, restoration occurs, and the reason is inspectable |
| shared-workspace demo | shared workspace state, registry references, workspace export, `verify_phase_02_workspace_state.py` output | `Release & Evidence Lead` with `Test & Replay Lead` support | `Anti-Shortcut Auditor` | cross-subsystem state is visible and clearly separate from long-term memory |

Validation package rules:

- later validation must point to the four demos above
- later review must include audit, governor verification, demo bundle, validation request, and user verdict path
- demos do not imply approval; only explicit user `approved` earns the phase

## 13. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield rebuild of already-existing substrate | compare subsystem plan against the provenance package | `Source Cartographer` | a core subsystem is planned as greenfield without justification | reopen provenance mapping and block execution start |
| event model drift from Phase 1 contracts | cross-check event boundaries against `TRACE_CONTRACT.md` and `FORMAL_MODELS.md` | `Architecture & Contract Lead` | event plan bypasses trace or support-state honesty | reopen architecture lane before execution |
| workspace overreach into later phases | compare workspace surface against `WORKSPACE_MODEL.md`, `MEMORY_MODEL.md`, and `GRAPH_STACK_MODEL.md` | `Constitution Keeper` | workspace is used to smuggle memory, graph, or cell behavior into Phase 2 | reject the drift and keep the plan kernel-only |
| registry and lifecycle coupling becomes vague | inspect whether registry, lifecycle verbs, and transitions are explicit and separately testable | `Kernel Pod Lead` | registry exists only in narrative text or lifecycle verbs are partial | reopen execution decomposition |
| replay and rollback promised but not structured | verify the plan names ledger, rollback points, verifiers, and evidence outputs | `Test & Replay Lead` | replay or rollback exists only in prose | block validation readiness and reopen verification planning |
| fail-closed kernel semantics underdefined | inspect negative-case rules against governance, contract, and policy inputs | `Architecture & Contract Lead` | fail-closed appears only as UI or UX language | rebuild the boundary section and block execution start |
| memory hooks expand beyond contract-safe anchors | compare planned memory-hook surface against the bounded list in Section 3 | `Constitution Keeper` | long-term memory, semantic or procedural memory, or graph persistence appears in Phase 2 scope | quarantine the expansion and reopen planning |
| Phase 2 execution cost grows beyond the planning envelope | compare later execution evidence against the Phase 2 budget envelope | `Program Governor` | RAM, workspace size, replay growth, snapshot budget, queue depth, or evidence bundle exceeds ceiling | stop execution, escalate, and reopen planning |
| more than one build pod becomes "necessary" without approval | compare later execution task cards against the one-active-build-pod rule | `Program Governor` | a second pod is activated without explicit approval | stop and reject the expansion |
| Phase 2 accidentally absorbs Phase 3 scope | compare planned outputs against the Phase 3 title and cell or tissue responsibilities | `Program Governor` | cell contracts, tissue manifests, or bundle structure appear as Phase 2 deliverables | reject the drift and keep Phase 3 untouched |
| `SRC-003` or `SRC-004` runtime history is treated as trusted runtime | compare any carry choice against `rebuild_clean` rows in the provenance package | `Anti-Shortcut Auditor` | v2 runtime or contract components are treated as portable truth | freeze for rework and escalate to `Program Governor` |

## 14. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says `approved` in a later separate run may the Phase 2 plan artifacts be committed and frozen
- Phase 2 remains `open` until later execution, tests, demos, audit, governor verification, validation request, and explicit user approval all exist
- after user approval, any future change to the Phase 2 plan requires explicit reopen instruction and a supersession note naming the replaced artifact

## 15. Final readiness judgment

`ready_for_user_review`

Phase 1 approval is explicit in the live phase-truth files, the Phase 1 provenance and design package are present, the reuse-versus-rebuild defaults for all required Phase 2 subsystems are explicit, the bounded memory-hook surface is now defined, the execution-governance stop rules and budget envelope are explicit, and the future execution, testing, and output targets are named precisely enough to prevent later blind drift.
