# Phase 4: Memory Planes

## 1. Phase identity

- Phase number: `4`
- Canonical phase name: `Memory Planes`
- Status: `planning_draft`
- Canonical artifact path: `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
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
  - approved Phase 2 execution surfaces under `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/`
  - approved Phase 2 testing surfaces under `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/`
  - approved Phase 2 evidence and demo surfaces under `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/`
  - approved Phase 3 execution surfaces under `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/`
  - approved Phase 3 testing surfaces under `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/`
  - approved Phase 3 evidence and demo surfaces under `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`

## 2. Phase mission

- Phase 4 exists to define and later build the governed memory layer above the approved Phase 2 kernel and the approved Phase 3 cell, tissue, and bundle layer.
- Phase 4 must build later:
  - working memory
  - episodic memory
  - semantic memory
  - procedural memory
  - continuity memory
  - correction handling
  - promotion
  - compression
  - forgetting
  - retirement
  - memory review
  - rollback-safe updates
- Phase 4 must not:
  - re-implement Phase 2 kernel, replay, rollback, quarantine, or fail-closed logic
  - re-implement Phase 3 cell, tissue, trust, split/merge, or bundle structure
  - implement Phase 5 graph persistence, graph schemas, or graph traversal policy
  - implement Phase 6 world-model or simulator behavior
  - implement Phase 7 conversation behavior
  - weaken the trace contract, review chain, or user approval rules
  - treat inherited code as earned AGIFCore runtime without rebuild, tests, demos, evidence, audit, and later user approval
  - approve itself

## 3. Scope and non-goals

### In scope

- the Phase 4 planning artifact
- the Phase 4 task-card map
- the memory-plane boundary rules
- the reuse and provenance strategy for each memory subsystem
- the future execution-family plan for `04_execution/phase_04_memory_planes/`
- the future testing-family plan for `05_testing/phase_04_memory_planes/`
- the future outputs, evidence, and demo family plan for `06_outputs/phase_04_memory_planes/`
- the later audit, governor-verification, validation-request, and user-review path

### Out of scope

- any runtime implementation in this run
- any file under `04_execution/` as part of this planning run
- Phase 5 graph implementation
- Phase 6 world-model or simulator implementation
- Phase 7 conversation implementation
- product-runtime, gateway, sandbox, installer, or release execution work
- any commit, freeze, tag, merge, or approval action

### Phase 4 scope rules

- Phase 4 must use the approved Phase 2 kernel rollback, replay, quarantine, and workspace anchors instead of inventing a separate memory-control substrate.
- Phase 4 must use the approved Phase 3 cell, tissue, and bundle boundaries instead of hiding memory responsibilities inside one giant untyped store.
- Phase 4 may define graph-ready references only. It may not define Phase 5 graph schemas or persistence.
- Phase 4 may define conversation-safe memory interfaces only. It may not define Phase 7 language behavior.

### Explicit statement

Phase 5 and later phases remain untouched by this plan.

## 4. Phase 3 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 3 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` both show Phase 3 `approved` | Phase 4 planning may proceed |
| Required Phase 1 artifacts relied on exist | `pass` | provenance package, trace contract, validation and demo protocol, requirement pack, and design pack exist | planning has the required Phase 1 inputs |
| Required Phase 2 artifacts relied on exist | `pass` | approved Phase 2 plan, runtime, verifier family, evidence bundle, demos, and closeout records exist on disk | planning has the required kernel and workspace baseline |
| Required Phase 3 artifacts relied on exist | `pass` | approved Phase 3 plan, runtime, verifier family, evidence bundle, demos, and closeout records exist on disk | planning has the required cell, tissue, and bundle baseline |
| Dependency gaps that block planning | `none` | no missing prerequisite artifact blocks planning | no prerequisite stop |
| Non-blocker note: current Phase 4 plan artifact does not exist yet | `present` | this planning run is the first canonical Phase 4 plan draft | expected planning target, not a blocker |
| Non-blocker note: no direct frozen semantic-memory, procedural-memory, or correction-handling module rows exist | `present` | provenance package provides partial substrate but not final AGIFCore-ready modules | requires controlled rebuild decisions, not a planning stop |
| Blockers vs non-blockers | `planning not blocked` | current gaps are expected Phase 4 outputs, not unmet prerequisites | readiness is `ready_for_user_review` |

## 5. Active team map for Phase 4

Later Phase 4 execution default build pod: `Memory & Graph Pod Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | Must never do this phase |
| --- | --- | --- | --- | --- | --- |
| User | none | active | final human approver remains required | later approve or reject the Phase 4 plan | delegate final approval |
| Program Governor | `gpt-5.4` | active | top planning authority and phase control remain central | own prerequisite truth, active-role map, reuse strategy, work order, artifact matrix, and closure chain | implement runtime code, self-approve, broaden into Phase 5 |
| Constitution Keeper | `gpt-5.4 mini` | active | Phase 4 can drift into hidden autonomy, Phase 5 graph scope, or Phase 7 conversation scope | guard constitution, non-negotiables, review honesty, correction safety, and phase boundaries | author runtime design on its own, approve the phase |
| Source Cartographer | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | anti-rebuild discipline is central to memory work | map each memory subsystem to inherited source basis, disposition, and provenance expectations | invent a fifth disposition, treat historical code as already valid runtime, approve the phase |
| Architecture & Contract Lead | `gpt-5.4` | active | Phase 4 needs precise plane boundaries and correction/review seams | own memory-plane boundaries, plane-to-plane leak rules, correction boundaries, review boundaries, and alignment to kernel and cell/tissue contracts | drift into Phase 5 graph logic, Phase 7 conversation logic, or self-approve |
| Kernel Pod Lead | `gpt-5.3-codex` | inactive by default, consult only if needed | Phase 4 must respect approved Phase 2 rollback, replay, quarantine, and workspace seams | consult only if a Phase 2 seam becomes ambiguous | author the plan, implement Phase 4 code in this run, approve the phase |
| Memory & Graph Pod Lead | `gpt-5.3-codex` | active | future execution owner for Phase 4 and default later build pod | provide planning consultation on execution decomposition, plane-local module boundaries, and memory-lifecycle sequencing | author the canonical plan alone, drift into Phase 5 graph build work, approve the phase |
| World & Conversation Pod Lead | `gpt-5.3-codex` | inactive | Phase 4 must stay below world-model and conversation phases | none | absorb Phase 6 or 7 scope |
| Meta & Growth Pod Lead | `gpt-5.3-codex` | inactive | danger zone and not needed for memory planning | none | activate casually or leak self-improvement into Phase 4 |
| Product & Sandbox Pod Lead | `gpt-5.3-codex` | inactive unless narrow consultation is required | memory review export and bundle/runtime-shell seams may need narrow consultation later | consult only if a product-runtime or bundle shell seam blocks planning | author the plan, absorb later product or sandbox execution scope |
| Test & Replay Lead | `gpt-5.4 mini` | active | memory carry-forward, correction, forgetting, compression, and rollback-safe behavior must be test-planned from the start | define verifier family, evidence expectations, and later demo checks | implement runtime behavior, approve the phase |
| Anti-Shortcut Auditor | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | high risk of fake memory completeness or giant-store shortcuts | detect silent omission, unsupported completeness, greenfield drift, and plane-collapsing shortcuts | author canonical plan content, downgrade blockers, approve the phase |
| Merge Arbiter | `gpt-5.3-codex` | inactive | planning-only run | none until later execution integration is needed | author plan content or approve the phase |
| Validation Agent | `gpt-5.4` | active | final machine-side review of the plan package is required before user review | validate the Phase 4 planning package and later prepare the review request | author the plan or approve the phase |
| Release & Evidence Lead | `gpt-5.4 mini` | active | demos must be inspectable and self-contained later | define evidence grouping and demo bundle shape only | perform release execution or public-claim packaging |

## 6. Reuse and provenance strategy

Only the frozen four disposition categories are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance justification |
| --- | --- | --- | --- | --- |
| working memory | `SRC-002 agif-tasklet-cell` local session memory plus the approved Phase 2 workspace and trace anchors | `port_with_provenance` | bounded session-local state already exists and should be ported into AGIFCore rather than replaced with a blank-slate catch-all store | `CC-067`, `SIM-031`, `MEMORY_MODEL.md`, `TRACE_CONTRACT.md` |
| episodic memory | `SRC-002 agif-tasklet-cell` episodic memory plus approved Phase 2 replay and rollback anchors | `port_with_provenance` | tasklet provides a direct episodic substrate and Phase 2 already provides replay, rollback, and lineage anchors that episodic memory must respect | `CC-068`, `SIM-032`, `CC-040`, `CC-042` |
| semantic memory | `SRC-001 agif_fabric_v1` theory fragments plus reviewed-memory tiers, with concept-graph alignment kept for later | `rebuild_clean` | no direct frozen semantic-memory module exists, so AGIFCore must rebuild a distinct semantic plane around portable theory-fragment and reviewed-memory substrate without sneaking in Phase 5 graph storage | `CC-021`, `CC-044`, `MEMORY_MODEL.md`, `GRAPH_STACK_MODEL.md` |
| procedural memory | `SRC-001` strategy journal substrate plus reviewed-memory tiers, with skill-graph alignment kept for later | `rebuild_clean` | no direct frozen procedural-memory module exists, so AGIFCore must rebuild a distinct procedural plane instead of confusing reusable procedures with semantic facts or task scripts | `CC-013`, `CC-044`, `SKILL_GRAPH_MODEL.md`, `CELL_FAMILIES.md` |
| continuity memory | `SRC-001` `SelfModelRecord` plus continuity/self-history cell-family anchors | `port_with_provenance` | self-history and continuity anchors are explicitly frozen and should port into AGIFCore rather than be reinvented | `CC-011`, `CC-013`, `MEMORY_MODEL.md`, `CELL_FAMILIES.md` |
| correction handling | approved Phase 2 rollback/quarantine/replay substrate plus continuity anchors from `SelfModelRecord` | `rebuild_clean` | no direct frozen correction-handling module exists; AGIFCore must build explicit before/after correction flow, supersession markers, and rollback-safe updates on top of portable rollback and continuity substrate | `CC-011`, `CC-040`, `CC-042`, `CC-043`, `TRACE_CONTRACT.md` |
| promotion | `SRC-001` promotion, deduplication, supersession, compression, retirement, and memory GC substrate | `rebuild_clean` | the provenance package explicitly marks the memory lifecycle substrate as rebuild-clean rather than direct carry-over | `CC-045`, `SIM-009` |
| compression | `SRC-001` memory lifecycle substrate plus reviewed-memory tiers | `rebuild_clean` | compression is a named memory responsibility, but the exact AGIFCore execution behavior must be rebuilt, not assumed | `CC-045`, `SIM-009`, `CC-044` |
| forgetting | `SRC-001` memory lifecycle substrate plus `memory_pressure` signal | `rebuild_clean` | forgetting must be explicit, reviewable, and pressure-aware; there is no direct frozen AGIFCore-ready forgetting module | `CC-045`, `CC-046`, `MEMORY_MODEL.md` |
| retirement | `SRC-001` memory lifecycle substrate plus reviewed-memory tiers | `rebuild_clean` | retirement is a required lifecycle state transition, but not a ready AGIFCore module | `CC-045`, `SIM-009`, `CC-044` |
| memory review | `SRC-001` reviewed memory with hot, warm, cold, and ephemeral tiers plus tasklet session and episodic substrate | `port_with_provenance` | reviewed-memory and tiering policy are explicit carry candidates; AGIFCore should port that substrate and rebuild its exact review flow around it, not invent review from zero | `CC-044`, `CC-067`, `CC-068`, `MEMORY_MODEL.md` |
| rollback-safe updates | approved Phase 2 rollback, quarantine, replay, and workspace substrate plus approved Phase 3 structure and bundle boundaries | `port_with_provenance` | rollback control already exists and should be reused rather than rebuilt; Phase 4 must layer memory-plane-safe batching and review rules on top of it | `CC-040`, `CC-042`, `CC-043`, `SIM-006`, `WORKSPACE_MODEL.md` |

## 7. Memory-plane boundary rules

### Working memory only

- active turn or task state
- currently active support fragments, context refs, and trace-linked temporary reasoning state
- current cell, tissue, and bundle-local memory candidates that have not yet passed promotion or review
- current memory-pressure counters and bounded current-run review queues

### Episodic memory only

- replayable event-style history
- reviewable turn history with provenance and trace anchors
- before-and-after correction events as time-ordered records
- carry-forward records that preserve when something happened, not what timelessly remains true

### Semantic memory only

- reviewed and promoted abstractions
- generalized concepts, theories, and stable descriptors
- semantic records that stay compatible with later concept or descriptor graph references
- no raw turn transcript, no current scratchpad, and no executable procedure body

### Procedural memory only

- reviewed reusable procedures and skills
- preconditions, postconditions, constraints, and provenance for governed reuse
- procedural records that stay compatible with later skill-graph references
- no generic fact storage, no raw episodic timeline, and no automatic execution authority

### Continuity memory only

- self-history anchors
- approved continuity facts that preserve honest self-reference and durable continuity state
- correction and supersession markers that affect long-lived continuity truth
- no raw conversation transcript and no catch-all personal profile store

### Cross-plane leak rules

- raw working-memory state may not enter semantic, procedural, or continuity memory without governed promotion and memory review
- episodic records may not become semantic, procedural, or continuity records without explicit provenance, correction status, and review approval
- semantic memory may not silently overwrite episodic history
- procedural memory may not silently rewrite semantic memory or continuity memory
- correction handling may not directly mutate long-term planes without a rollback-safe update record
- compression, forgetting, and retirement may not delete the last surviving provenance anchor for a retained long-term record

### Phase 5 separation rule

- Phase 4 may produce graph-ready references only
- Phase 4 may not define descriptor, skill, concept, or transfer graph schemas
- Phase 4 may not define graph persistence, traversal, edge ranking, or graph conflict rules
- Phase 5 remains the only graph-implementation phase

### Phase 7 separation rule

- Phase 4 may expose retrieval hooks, carry-forward exports, correction refs, and memory-review refs
- Phase 4 may not implement user-turn interpretation, discourse-mode selection, answer planning, language realization, or self-knowledge dialogue behavior
- conversation remains a later surface above memory, not part of memory itself

## 8. Phase 4 budget envelope

No explicit master-plan numeric memory ceilings are frozen for Phase 4. The ceilings below are planning ceilings for later Phase 4 execution on the laptop profile. They are not achieved measurements.

| Budget item | Phase 4 planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max working-memory resident size | `<= 512 KiB` serialized bounded state | stop and escalate if exceeded |
| max episodic-memory recent-window size | `<= 512` records and `<= 2 MiB` serialized | stop and review rollover or carry-forward strategy if exceeded |
| max semantic-memory retained size before compression or review | `<= 2048` entries or `<= 8 MiB` serialized | stop and reopen compression or review policy if exceeded |
| max procedural-memory retained size before review | `<= 512` entries or `<= 2 MiB` serialized | stop and review procedural retention policy if exceeded |
| max continuity-memory retained size before retirement or review | `<= 256` entries or `<= 1 MiB` serialized | stop and escalate if exceeded |
| max correction queue size | `<= 64` pending items | stop and review correction backlog handling if exceeded |
| max promotion batch size | `<= 32` candidate items per batch | stop and split the batch if exceeded |
| max rollback-safe update batch size | `<= 16` records per batch | stop and split the update if exceeded |
| max memory review report size | `<= 512 KiB` | stop and summarize or split review scopes if exceeded |
| max Phase 4 evidence and demo bundle size | `<= 64 MiB` | stop and reorganize outputs if exceeded |

Budget rules:

- these are Phase 4 planning ceilings only
- later execution must measure against them
- if any ceiling is exceeded, stop and escalate to Program Governor instead of silently widening the envelope
- if later execution needs these ceilings raised, reopen planning before continuing

## 9. Artifact ownership matrix

### Artifact ownership matrix

| Artifact path | Primary author | Reviewer | Auditor | Validator | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `01_plan/PHASE_04_MEMORY_PLANES.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2 and 3 baselines, requirements, design pack, admin controls | all later Phase 4 work | section-complete Phase 4 plan |
| `00_admin/codex_threads/tasks/phase_04/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, this plan | all later valid Phase 4 work | one task card per active role with disjoint scope |
| `04_execution/phase_04_memory_planes/` | `Memory & Graph Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 4 plan, Phase 1 provenance package, approved Phase 2 kernel, approved Phase 3 structure, trace contract, memory model | Phase 4 runtime delivery | later runtime files exist and match scoped targets |
| `05_testing/phase_04_memory_planes/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 4 plan, execution family, validation protocol | Phase 4 verification and closeout | later verifier family exists and runs |
| `06_outputs/phase_04_memory_planes/phase_04_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifiers, trace-linked exports, memory reports | audit, governor verification, validation, user demos | later machine-readable evidence bundle is inspectable |
| `06_outputs/phase_04_memory_planes/phase_04_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, validation protocol | user review | later demo bundle exists for memory carry-forward, correction, and forgetting/compression |
| `00_admin/codex_threads/handoffs/PHASE_04_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, verifiers, demos, evidence | validation request | direct verification record exists |
| `00_admin/codex_threads/handoffs/PHASE_04_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdicts are explicit |
| `00_admin/codex_threads/handoffs/PHASE_04_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

### Future family note

- naming future `04_execution/`, `05_testing/`, and `06_outputs/` families in this plan does not create them
- directory or scaffold creation for those families is deferred to the first Phase 4 execution run
- this planning run only freezes names, ownership, and expectations

### First-pass planned future runtime files

Planned execution root:

- `04_execution/phase_04_memory_planes/agifcore_phase4_memory/`

Planned first-pass files:

| Planned file | Planned purpose |
| --- | --- |
| `working_memory.py` | bounded active turn or task memory surface |
| `episodic_memory.py` | replayable event-style memory surface |
| `semantic_memory.py` | reviewed abstraction and concept memory surface |
| `procedural_memory.py` | reviewed reusable procedure and skill memory surface |
| `continuity_memory.py` | self-history and continuity anchor surface |
| `correction_handling.py` | explicit correction, supersession, and before/after update flow |
| `promotion_pipeline.py` | governed promotion of reviewed candidates between planes |
| `compression_pipeline.py` | explicit compression and memory-pressure handling |
| `forgetting_retirement.py` | forgetting, retirement, and retirement-safe provenance rules |
| `memory_review.py` | review queues, review outputs, and tiered review decisions |
| `rollback_safe_updates.py` | memory-plane-safe batched updates with rollback and replay anchors |

### First-pass planned future testing files

Planned testing root:

- `05_testing/phase_04_memory_planes/`

Planned first-pass files:

| Planned file | Planned purpose |
| --- | --- |
| `verify_phase_04_working_memory.py` | bounded current-state and carry-forward checks |
| `verify_phase_04_episodic_memory.py` | episodic replayability and event-history checks |
| `verify_phase_04_semantic_memory.py` | semantic retention and provenance checks |
| `verify_phase_04_procedural_memory.py` | procedural retention and governed reuse checks |
| `verify_phase_04_continuity_memory.py` | continuity and correction-anchor checks |
| `verify_phase_04_corrections_and_promotion.py` | correction, supersession, and promotion checks |
| `verify_phase_04_forgetting_and_compression.py` | compression, forgetting, retirement, and memory-pressure checks |
| `verify_phase_04_rollback_safe_updates.py` | rollback-safe batch update and restore checks |
| `verify_phase_04_memory_review.py` | memory-review gate, tiering, and enforcement checks |

### First-pass planned future outputs and evidence files

Planned outputs root:

- `06_outputs/phase_04_memory_planes/`

Planned first-pass files:

- `phase_04_evidence_manifest.json`
- `phase_04_working_memory_report.json`
- `phase_04_episodic_memory_report.json`
- `phase_04_semantic_memory_report.json`
- `phase_04_procedural_memory_report.json`
- `phase_04_continuity_memory_report.json`
- `phase_04_corrections_and_promotion_report.json`
- `phase_04_forgetting_and_compression_report.json`
- `phase_04_rollback_safe_updates_report.json`
- `phase_04_memory_review_report.json`
- `phase_04_demo_index.md`
- `phase_04_memory_carry_forward_demo.md`
- `phase_04_correction_demo.md`
- `phase_04_forgetting_compression_demo.md`

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| phase control and prerequisite reconciliation | freeze scope, active roles, task-card map, default build pod, and closure chain | `Program Governor` | `Constitution Keeper` | main Phase 4 plan and task-card map | Phase 3 approved in live phase-truth files | active and inactive roles are fixed and Phase 4 stays inside scope |
| memory plane boundary framing | define the five memory planes as distinct governed surfaces above the approved Phase 2 and 3 baselines | `Architecture & Contract Lead` | `Source Cartographer`, `Memory & Graph Pod Lead`, `Program Governor` | plane-boundary plan and runtime-family targets | approved Phase 2 and 3 seams reviewed | no plane collapses into a giant catch-all store |
| correction and memory review planning | define correction flow, supersession, review queues, and enforcement points | `Architecture & Contract Lead` | `Constitution Keeper`, `Test & Replay Lead`, `Memory & Graph Pod Lead` | correction and review plan | memory-plane boundaries stable | correction is explicit and review has real enforcement meaning |
| promotion, compression, forgetting, and retirement planning | define lifecycle transitions between review, retention, compression, forgetting, and retirement | `Memory & Graph Pod Lead` | `Source Cartographer`, `Architecture & Contract Lead`, `Test & Replay Lead` | lifecycle pipeline plan | reviewed-memory substrate and plane boundaries reviewed | lifecycle transitions are explicit, bounded, and verifiable |
| rollback-safe update planning | define how memory updates remain replayable, reversible, and quarantine-safe | `Memory & Graph Pod Lead` | `Architecture & Contract Lead`, `Program Governor`, `Kernel Pod Lead` if consulted | rollback-safe update plan | Phase 2 rollback, replay, and quarantine surfaces reviewed | no silent mutation path remains |
| profile and budget enforcement planning | freeze laptop-oriented ceilings and stop rules for later execution | `Program Governor` | `Memory & Graph Pod Lead`, `Test & Replay Lead`, `Constitution Keeper` | budget envelope and stop-rule map | deployment profiles reviewed | budget ceilings and escalation points are explicit |
| test, demo, validation, and evidence planning | define verifiers, reports, demo bundle, and review path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | verifier family plan, evidence plan, demo plan, validation surface | execution targets stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. `Program Governor` verifies Phase 3 approval truth and opens the Phase 4 task-card set.
2. `Source Cartographer` maps each Phase 4 subsystem to source basis and disposition.
3. `Architecture & Contract Lead` and `Memory & Graph Pod Lead` draft plane boundaries, memory-lifecycle boundaries, and later execution decomposition in parallel with step 2.
4. `Constitution Keeper` reviews steps 2 and 3 for constitution drift, hidden-memory shortcuts, Phase 5 graph leakage, and Phase 7 conversation leakage.
5. If a Phase 2 rollback, replay, or workspace seam is still unclear after step 4, `Kernel Pod Lead` is activated only for narrow consultation.
6. If a product-runtime or bundle shell seam is still unclear after step 4, `Product & Sandbox Pod Lead` is activated only for narrow consultation.
7. `Program Governor` consolidates the core Phase 4 plan, future artifact families, budget envelope, and closure map after steps 2 through 6 stabilize.
8. `Test & Replay Lead` and `Release & Evidence Lead` define verifiers, evidence, and demos after the memory boundaries and lifecycle boundaries are stable.
9. `Anti-Shortcut Auditor` audits the full Phase 4 planning package.
10. `Program Governor` independently verifies the audited planning package.
11. `Validation Agent` prepares the later user review request.
12. User review happens only after the validated planning package exists.

Safe parallelism:

- `Source Cartographer`, `Architecture & Contract Lead`, and `Memory & Graph Pod Lead` may work in parallel on disjoint planning artifacts
- `Constitution Keeper` may begin once first-pass outputs exist
- `Kernel Pod Lead` remains inactive unless a real kernel seam blocks planning
- `Merge Arbiter` stays inactive in planning-only work
- one active build pod remains the default for later execution, and that build pod is `Memory & Graph Pod Lead`

## 12. Detailed task cards

User is active approval-only and does not receive a task card.

### `P4-TC-PG-01`

- task card ID: `P4-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, the Phase 4 plan, task-card map, artifact matrix, and closure chain
- exact files allowed to touch:
  - `01_plan/PHASE_04_MEMORY_PLANES.md`
  - `00_admin/codex_threads/tasks/phase_04/P4-TC-PG-01_PHASE_4_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `01_plan/MASTER_PLAN.md`
  - all `04_execution/*`
  - all Phase 5+ artifacts
  - earlier phase-truth files except to report a prerequisite mismatch
- required reads first:
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 and Phase 3 plans and execution surfaces
  - memory model, graph stack model, product runtime model, workspace model
  - task-card template, model manifest, tool matrix, branch/worktree policy, escalation rules
- step-by-step work method:
  1. verify Phase 3 approval in live phase-truth files
  2. define active and inactive roles for Phase 4 planning
  3. freeze the later default build pod as `Memory & Graph Pod Lead`
  4. reconcile provenance, boundary, verification, budget, and demo outputs into one plan
- required cross-checks:
  - no Phase 5 graph implementation is planned in Phase 4
  - no Phase 7 conversation behavior is planned in Phase 4
  - no implementation claims appear in planning language
- exit criteria:
  - the Phase 4 plan is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply runtime implementation or approval
- explicit proof that no approval is implied: the task ends at plan readiness only; Phase 4 remains `open`

### `P4-TC-CK-01`

- task card ID: `P4-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4 mini`
- objective: guard constitution, correction safety, review honesty, and phase boundaries
- exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_04/P4-TC-CK-01_PHASE_4_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - all `04_execution/*`
  - all `05_testing/*`
  - all `06_outputs/*`
  - all Phase 5+ artifacts
- required reads first:
  - `01_plan/SYSTEM_CONSTITUTION.md`
  - `01_plan/TRACE_CONTRACT.md`
  - `02_requirements/NON_NEGOTIABLES.md`
  - `02_requirements/PHASE_APPROVAL_RULES.md`
  - `03_design/MEMORY_MODEL.md`
  - `03_design/GRAPH_STACK_MODEL.md`
  - `03_design/CONVERSATION_MODEL.md`
  - the Phase 4 plan draft
- step-by-step work method:
  1. check that memory planes stay governed and auditable
  2. check that correction handling cannot silently rewrite long-term state
  3. check that review is enforceable, not decorative
  4. check that Phase 4 does not absorb Phase 5 graph logic or Phase 7 conversation behavior
- required cross-checks:
  - no hidden autonomy wording
  - no no-LLM or no-cloud rule drift
  - no approval language
- exit criteria:
  - all constitutional objections are resolved or explicitly blocked
- handoff target: `Program Governor`
- anti-drift rule: do not author runtime design or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P4-TC-SC-01`

- task card ID: `P4-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- objective: map each Phase 4 subsystem to source basis, disposition, and provenance expectations
- exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_04/P4-TC-SC-01_PHASE_4_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - all `04_execution/*`
  - all `05_testing/*`
  - all `06_outputs/*`
  - all Phase 5+ artifacts
- required reads first:
  - `01_plan/COMPONENT_CATALOG.md`
  - `01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 2 and Phase 3 plans and execution baselines
  - historical source roots when needed
- step-by-step work method:
  1. map each Phase 4 subsystem to the strongest source basis
  2. select exactly one frozen disposition per subsystem
  3. flag where the carry decision is substrate-level rather than a literal module carry
  4. flag any direct provenance gap
- required cross-checks:
  - no subsystem is silently omitted
  - no fifth disposition category appears
  - no historical code is treated as already valid runtime
- exit criteria:
  - every required Phase 4 subsystem has explicit provenance and rationale
- handoff target: `Architecture & Contract Lead` then `Program Governor`
- anti-drift rule: do not claim mapped historical code is already valid AGIFCore runtime
- explicit proof that no approval is implied: provenance mapping does not earn the phase

### `P4-TC-ACL-01`

- task card ID: `P4-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: freeze the memory-plane, correction, and review boundary layer above the approved Phase 2 kernel and Phase 3 structure
- exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_04/P4-TC-ACL-01_PHASE_4_MEMORY_PLANE_BOUNDARIES.md`
- files forbidden to touch:
  - all `04_execution/*`
  - all Phase 5+ artifacts
  - earlier canonical design files as edits
- required reads first:
  - `01_plan/TRACE_CONTRACT.md`
  - `01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - approved Phase 2 runtime files for workspace, replay, rollback, quarantine, lifecycle, and scheduler
  - approved Phase 3 runtime files for cell contracts, tissue manifests, active or dormant control, split/merge, and bundle validation
  - `03_design/MEMORY_MODEL.md`
  - `03_design/GRAPH_STACK_MODEL.md`
  - `03_design/WORKSPACE_MODEL.md`
  - `03_design/CONVERSATION_MODEL.md`
  - provenance outputs from `SC`
- step-by-step work method:
  1. define the five memory planes as distinct governed surfaces
  2. define correction, promotion, compression, forgetting, retirement, and review boundaries
  3. define allowed plane-to-plane transitions and forbidden leak paths
  4. align all boundaries to approved kernel and structure seams
- required cross-checks:
  - no giant untyped store pretending to be multiple planes
  - no Phase 5 graph implementation
  - no Phase 7 conversation implementation
- exit criteria:
  - every Phase 4 subsystem has an explicit boundary and later proof path
- handoff target: `Program Governor` then `Test & Replay Lead`
- anti-drift rule: do not redesign the kernel, structure layer, or conversation layer
- explicit proof that no approval is implied: architecture framing is planning truth only

### `P4-TC-MGPL-01`

- task card ID: `P4-TC-MGPL-01`
- role owner: `Memory & Graph Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: own future execution decomposition for Phase 4 and freeze the later one-build-pod default execution lane
- exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_04/P4-TC-MGPL-01_PHASE_4_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - all `04_execution/*`
  - all `05_testing/*`
  - all `06_outputs/*`
  - all Phase 5+ artifacts
- required reads first:
  - approved Phase 2 and Phase 3 plans and execution baselines
  - `03_design/MEMORY_MODEL.md`
  - `03_design/GRAPH_STACK_MODEL.md`
  - `03_design/WORKSPACE_MODEL.md`
  - provenance outputs from `SC`
  - boundary outputs from `ACL`
- step-by-step work method:
  1. define the future runtime-file decomposition for each plane and lifecycle surface
  2. define the likely internal execution slices without changing the approved scope
  3. keep one build pod as the default for later execution
  4. define where rollback-safe updates depend on approved Phase 2 rollback substrate
- required cross-checks:
  - no Phase 5 graph build work is pulled into Phase 4
  - no one-store shortcut is proposed
  - no extra build pod is proposed without evidence
- exit criteria:
  - later execution can proceed without new decomposition decisions
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement runtime code in this planning run
- explicit proof that no approval is implied: execution decomposition does not approve or earn the phase

### `P4-TC-TRL-01`

- task card ID: `P4-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4 mini`
- objective: define the Phase 4 verifier family, evidence outputs, and demo-proof surfaces
- exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_04/P4-TC-TRL-01_PHASE_4_MEMORY_VERIFICATION_PLAN.md`
- files forbidden to touch:
  - all `04_execution/*`
  - all earlier canonical content
  - all Phase 5+ artifacts
- required reads first:
  - `01_plan/VALIDATION_PROTOCOL.md`
  - `01_plan/DEMO_PROTOCOL.md`
  - `01_plan/TRACE_CONTRACT.md`
  - approved Phase 2 and 3 verifier and evidence surfaces
  - the Phase 4 plan draft
- step-by-step work method:
  1. define the `verify_phase_04_*` family
  2. define carry-forward, correction, compression, forgetting, retirement, review, and rollback-safe update checks
  3. define negative fail-closed cases
  4. define machine-readable evidence outputs
- required cross-checks:
  - every required Phase 4 subsystem has a planned verifier
  - report text does not stand in for behavior proof
  - demos point to real evidence files
- exit criteria:
  - later test and evidence paths are exact enough to implement without new decisions
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P4-TC-ASA-01`

- task card ID: `P4-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- objective: audit the Phase 4 plan package for drift, omission, giant-store shortcuts, and fake completeness
- exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_04/P4-TC-ASA-01_PHASE_4_PLAN_AUDIT.md`
  - `00_admin/codex_threads/tasks/phase_04/P4-AUDIT-01_PHASE_4_PLAN_AUDIT_REPORT.md`
- files forbidden to touch:
  - canonical plan content
  - all `04_execution/*`
  - all Phase 5+ artifacts
- required reads first:
  - the complete Phase 4 planning package
  - the Phase 1 provenance package
  - the approved Phase 2 and Phase 3 baselines
  - validation protocol
- step-by-step work method:
  1. check every required subsystem is represented
  2. check carry decisions against the provenance package
  3. check that Phase 2 and Phase 3 seams are preserved
  4. check that correction, compression, forgetting, and retirement are enforceable and not just labels
  5. write explicit blockers or pass results
- required cross-checks:
  - no greenfield recreation where v1 or tasklet substrate exists
  - no one giant untyped store
  - no Phase 5 or Phase 7 scope leakage
- exit criteria:
  - audit report explicitly states pass or blockers with file-backed reasons
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P4-TC-VA-01`

- task card ID: `P4-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the Phase 4 planning package and prepare the later user review request
- exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_04/P4-TC-VA-01_PHASE_4_VALIDATION_REQUEST.md`
  - later `00_admin/codex_threads/handoffs/PHASE_04_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - canonical plan content
  - any runtime code or test code
  - any user verdict file
- required reads first:
  - audited Phase 4 plan package
  - governor verification record when it exists
  - validation protocol
- step-by-step work method:
  1. read the audited Phase 4 plan package
  2. identify exact review surfaces and what the user must inspect
  3. state pass, fail, blockers, and allowed verdicts
  4. hand the review request back to `Program Governor`
- required cross-checks:
  - no self-validation by an authoring role
  - every requested review surface points to a real planned artifact
  - no approval language before user verdict
- exit criteria:
  - validation request is exact enough for user review with no missing surface
- handoff target: `Program Governor`
- anti-drift rule: do not author plan content or runtime behavior
- explicit proof that no approval is implied: validation asks for review and does not mark the phase earned

### `P4-TC-REL-01`

- task card ID: `P4-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4 mini`
- objective: define the later user-facing Phase 4 demo and evidence bundle
- exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_04/P4-TC-REL-01_PHASE_4_DEMO_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - all `04_execution/*`
  - all public release artifacts
  - all Phase 5+ artifacts
- required reads first:
  - `01_plan/DEMO_PROTOCOL.md`
  - `01_plan/VALIDATION_PROTOCOL.md`
  - the Phase 4 plan draft
  - `TRL` outputs when available
- step-by-step work method:
  1. define the demo bundle shape for memory carry-forward, correction, and forgetting/compression
  2. define which evidence is machine-readable and which is human-facing
  3. define the later review packet order
- required cross-checks:
  - no release or publication drift
  - no missing demo surface
  - no evidence summary without real underlying files
- exit criteria:
  - later user review packet is exact and inspectable
- handoff target: `Program Governor` then `Validation Agent`
- anti-drift rule: do not expand into later release work
- explicit proof that no approval is implied: demo-package planning is not demo acceptance

## 13. Closure-gate mapping

| Phase 4 closure requirement | Artifact(s) that must satisfy it later | Responsible role | How it will be checked | What failure looks like |
| --- | --- | --- | --- | --- |
| working memory exists | `working_memory.py`, `verify_phase_04_working_memory.py`, `phase_04_working_memory_report.json` | `Memory & Graph Pod Lead` | bounded current-state behavior, current-turn carry-forward, and trace-linked review refs are explicit and test-backed | a vague scratchpad or unbounded catch-all store |
| episodic memory exists | `episodic_memory.py`, `verify_phase_04_episodic_memory.py`, `phase_04_episodic_memory_report.json` | `Memory & Graph Pod Lead` | replayable, reviewable event-style records exist with provenance and continuity anchors | episodic records are missing, unreplayable, or merged into another plane |
| semantic memory exists | `semantic_memory.py`, `verify_phase_04_semantic_memory.py`, `phase_04_semantic_memory_report.json` | `Memory & Graph Pod Lead` | reviewed abstractions and concepts exist with promotion provenance and no raw transcript leakage | semantic memory is only a label or holds raw history |
| procedural memory exists | `procedural_memory.py`, `verify_phase_04_procedural_memory.py`, `phase_04_procedural_memory_report.json` | `Memory & Graph Pod Lead` | reusable procedures exist with constraints, provenance, and no semantic-plane collapse | procedural memory is only a renamed semantic store or auto-execution shortcut |
| continuity memory exists | `continuity_memory.py`, `verify_phase_04_continuity_memory.py`, `phase_04_continuity_memory_report.json` | `Memory & Graph Pod Lead` | self-history and continuity anchors exist with correction-safe updates | continuity is unsupported narration or a raw transcript dump |
| correction handling exists | `correction_handling.py`, `verify_phase_04_corrections_and_promotion.py`, `phase_04_corrections_and_promotion_report.json` | `Architecture & Contract Lead` | before-and-after correction path, supersession markers, and review linkage are explicit | correction is claimed without visible mutation path or provenance |
| promotion exists | `promotion_pipeline.py`, `verify_phase_04_corrections_and_promotion.py`, `phase_04_corrections_and_promotion_report.json` | `Memory & Graph Pod Lead` | promotion batches move reviewed candidates across planes with provenance | promotion is only a label with no gated transition |
| compression exists | `compression_pipeline.py`, `verify_phase_04_forgetting_and_compression.py`, `phase_04_forgetting_and_compression_report.json` | `Memory & Graph Pod Lead` | compression changes retained state in a visible, reviewable way while preserving required anchors | compression is descriptive only or loses required provenance |
| forgetting exists | `forgetting_retirement.py`, `verify_phase_04_forgetting_and_compression.py`, `phase_04_forgetting_and_compression_report.json` | `Memory & Graph Pod Lead` | forgetting rules are explicit, policy-bounded, and verifier-visible | silent deletion or no governed forgetting path |
| retirement exists | `forgetting_retirement.py`, `verify_phase_04_forgetting_and_compression.py`, `phase_04_forgetting_and_compression_report.json` | `Memory & Graph Pod Lead` | retirement transitions are explicit and preserve the required review trail | retirement is named but has no state transition or evidence trail |
| memory review exists | `memory_review.py`, `verify_phase_04_memory_review.py`, `phase_04_memory_review_report.json` | `Test & Replay Lead` | review gates affect promotion, compression, forgetting, and retirement behavior | memory review is a report-only ritual with no enforcement meaning |
| rollback-safe updates exist | `rollback_safe_updates.py`, `verify_phase_04_rollback_safe_updates.py`, `phase_04_rollback_safe_updates_report.json` | `Memory & Graph Pod Lead` | update batches are replayable, reversible, and quarantine-safe | updates mutate state with no rollback or restore path |
| demo path exists | `06_outputs/phase_04_memory_planes/phase_04_demo_bundle/` | `Release & Evidence Lead` | all three required demos exist and point to real evidence | narrative-only demos or missing demo files |
| tests and evidence path exists | `05_testing/phase_04_memory_planes/` and `06_outputs/phase_04_memory_planes/phase_04_evidence/` | `Test & Replay Lead` | verifier family runs and outputs are machine-readable | no verifier family, no evidence manifest, or empty reports |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| memory carry-forward demo | working memory, episodic memory, continuity memory, promotion or review linkage, carry-forward verifier output, and evidence manifest | `Release & Evidence Lead` with `Test & Replay Lead` support | `Anti-Shortcut Auditor` | before-and-after state across at least one governed carry-forward step, with replay and review refs |
| correction demo | correction handling, continuity memory, semantic or episodic supersession behavior, rollback-safe update verifier output, and correction evidence | `Release & Evidence Lead` with `Test & Replay Lead` support | `Anti-Shortcut Auditor` | a clear incorrect state, a governed correction path, the corrected state, and the preserved supersession or rollback trail |
| forgetting or compression demo | compression pipeline, forgetting or retirement behavior, memory review output, forgetting/compression verifier output, and evidence manifest | `Release & Evidence Lead` with `Test & Replay Lead` support | `Anti-Shortcut Auditor` | pre- and post-review memory state, the governed action taken, preserved provenance anchors, and visible boundedness effect |

Validation package rules:

- later validation must point the user to the three demos above plus the audited evidence bundle
- later review must include the audit report, governor verification record, demo bundle, validation request, and user verdict path
- demos do not imply approval; only an explicit user `approved` verdict earns the phase

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable memory substrate | compare each subsystem plan against `COMPONENT_CATALOG.md`, `SOURCE_INHERITANCE_MATRIX.md`, and `RUNTIME_REBUILD_MAP.md` | `Source Cartographer` | a subsystem is planned greenfield without provenance justification | reopen provenance mapping and block execution start |
| one giant untyped store pretending to be multiple memory planes | compare planned runtime family against the memory-plane boundary rules and verifier plan | `Architecture & Contract Lead` | one module or one data store is proposed as the only memory truth without distinct plane contracts | reject the shortcut and split plane responsibilities before execution |
| correction handling mutating long-term state unsafely | inspect whether correction flow has before/after state, supersession markers, rollback refs, and review gates | `Architecture & Contract Lead` | correction path lacks rollback-safe update evidence or direct plane-specific update rules | reopen correction planning and block execution start |
| promotion, compression, forgetting, and retirement existing only as labels | compare lifecycle plan to verifier outputs and required state transitions | `Test & Replay Lead` | lifecycle names exist without verifier-visible effects | reopen lifecycle planning before execution continues |
| memory review becoming a report-only ritual with no enforcement | inspect whether review outcomes actually gate promotion, compression, forgetting, or retirement | `Program Governor` | review output does not change behavior or retention decisions | reopen review planning and block validation readiness |
| rollback-safe updates not actually rollback-safe | compare planned update path against approved Phase 2 rollback, replay, quarantine, and workspace surfaces | `Memory & Graph Pod Lead` | updates can mutate long-term state without restore or reject path | reopen rollback-safe update planning and consult `Kernel Pod Lead` if needed |
| Phase 4 accidentally absorbing Phase 5 graph logic | compare planned outputs against `GRAPH_STACK_MODEL.md` and the Phase 5 scope | `Constitution Keeper` | graph schemas, persistence, or traversal behavior appears in Phase 4 deliverables | reject the drift and keep Phase 5 untouched |
| Phase 4 accidentally absorbing conversation behavior | compare planned outputs against `CONVERSATION_MODEL.md` and the Phase 7 scope | `Constitution Keeper` | discourse selection, answer planning, or language realization appears in Phase 4 deliverables | reject the drift and keep Phase 7 untouched |
| semantic and procedural memory collapse into one vague long-term store | compare plane boundaries, runtime-family plan, and verifier plan | `Architecture & Contract Lead` | semantic and procedural memories share one interface with no distinct behaviors | split the plane contracts before execution starts |
| continuity memory becomes unsupported self-narration | inspect continuity rules against `SelfModelRecord`, correction rules, and trace requirements | `Constitution Keeper` | continuity stores fluent claims with no provenance or correction path | block execution start until continuity rules are explicit |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says `approved` in a later separate run may the Phase 4 plan artifacts be committed and frozen
- Phase 4 remains `open` until later execution, verifiers, demos, audit, governor verification, validation request, and explicit user approval all exist
- after user approval, any future change to the Phase 4 plan requires explicit reopen instruction and a supersession note naming the replaced artifact

## 17. Final readiness judgment

`ready_for_user_review`

Phase 3 approval is explicit in the live phase-truth files, the full Phase 1 provenance and design package is present, the approved Phase 2 kernel and workspace baseline is available, the approved Phase 3 cell, tissue, and bundle baseline is available, and the port-versus-rebuild defaults for all required Phase 4 subsystems are explicit. The remaining gaps are expected Phase 4 outputs rather than prerequisite blockers.
