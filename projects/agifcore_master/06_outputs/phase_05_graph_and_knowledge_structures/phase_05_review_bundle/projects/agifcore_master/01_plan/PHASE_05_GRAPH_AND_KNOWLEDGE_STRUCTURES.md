# Phase 5: Graph and Knowledge Structures

## 1. Phase identity

- Phase number: `5`
- Canonical phase name: `Graph and Knowledge Structures`
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
  - approved Phase 2, 3, and 4 surfaces under:
    - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/`
    - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/`
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/`
    - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/`
    - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/`
    - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/`
    - `projects/agifcore_master/04_execution/phase_04_memory_planes/`
    - `projects/agifcore_master/05_testing/phase_04_memory_planes/`
    - `projects/agifcore_master/06_outputs/phase_04_memory_planes/`
  - admin controls:
    - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
    - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
    - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
    - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
    - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`

## 2. Phase mission

- Phase 5 exists to define and later build the governed graph layer above approved memory planes and below world-model and conversation behavior.
- Phase 5 must later build:
  - descriptor graph
  - skill graph
  - concept graph
  - transfer graph
  - provenance links
  - conflict rules
  - supersession rules
  - reusable support selection
- Phase 5 must not:
  - implement Phase 6 world-model or simulator logic
  - implement Phase 7 conversation behavior
  - rework Phase 2 kernel or Phase 3 structure boundaries
  - move graph persistence into Phase 4 memory planes
  - treat historical v1 or v2 code as already-valid AGIFCore completion
  - imply approval, freeze, commit, or closure

## 3. Scope and non-goals

- In-scope artifacts:
  - the canonical Phase 5 plan
  - the Phase 5 planning task-card set
  - graph-layer boundary rules
  - reuse and provenance decisions for all major Phase 5 subsystems
  - future execution, testing, outputs, and handoff family targets
  - later demo and closure planning
- Out-of-scope work:
  - any Phase 5 runtime code
  - any Phase 5 verifier code
  - any Phase 5 demo or evidence generation
  - any Phase 6 planning
  - any Phase 7 planning
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
- Explicit untouched-later-phase statement:
  - Phase 6 and all later phases remain untouched by this plan.

## 4. Phase 4 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 4 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` both show Phase 4 `approved` | Phase 5 planning may proceed |
| Explicit user approval record exists | `pass` | `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_USER_VERDICT.md` records verdict `approved` | no silent approval assumption |
| Required Phase 1 artifacts relied on exist | `pass` | provenance package, trace contract, validation and demo protocol, requirement pack, design pack | planning has required governance inputs |
| Required Phase 2 artifacts relied on exist | `pass` | approved plan plus runtime, verifier, evidence, and demo surfaces are present | kernel/workspace seams are inspectable |
| Required Phase 3 artifacts relied on exist | `pass` | approved plan plus runtime, verifier, evidence, and demo surfaces are present | cell/tissue/bundle seams are inspectable |
| Required Phase 4 artifacts relied on exist | `pass` | approved plan plus runtime, verifier, evidence, demo, validation, and user verdict surfaces are present | memory-plane seams are inspectable |
| Dependency gap: canonical Phase 5 plan file currently absent | `non-blocker` | `projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md` does not exist yet | this draft is the first canonical target |
| Dependency gap: Phase 5 planning task folder currently absent | `non-blocker` | no `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/` folder exists yet | expected pre-authoring condition |
| Blockers vs non-blockers | `planning not blocked` | no missing prerequisite artifact blocks this planning run | readiness may be `ready_for_user_review` |

## 5. Active team map for Phase 5

| Role | Model tier | Active/inactive | Why | Exact responsibility this phase | Must never do this phase |
| --- | --- | --- | --- | --- | --- |
| User | none | active | final human approver | later review or reject the Phase 5 plan package | delegate final approval |
| Program Governor | `gpt-5.4` | active | top planning authority and phase control | own prerequisite truth, scope, role activation, reuse decisions, task-card map, closure map, and final plan integration | implement runtime code, self-approve, broaden into Phase 6 |
| Constitution Keeper | `gpt-5.4 mini` | active | Phase 5 can drift into hidden autonomy, world-model logic, or conversation logic | guard constitution, non-negotiables, approval honesty, and phase boundaries | author canonical runtime design alone, approve the phase |
| Source Cartographer | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | inherited graph substrate must be mapped before planning execution | map each Phase 5 subsystem to inherited source basis, disposition, and reuse limits | invent a fifth disposition, treat historical code as already earned AGIFCore runtime, approve the phase |
| Architecture & Contract Lead | `gpt-5.4` | active | graph boundaries and contracts must be explicit before execution | own graph-layer separation, provenance/conflict/supersession boundaries, memory and kernel interface limits | redesign the team, leak Phase 6/7 behavior, approve the phase |
| Kernel Pod Lead | `gpt-5.3-codex` | inactive by default | Phase 5 should consume Phase 2 seams, not reopen them | consult only if Phase 2 workspace, replay, rollback, or quarantine seams become ambiguous | author the plan, implement code, or expand Phase 2 scope |
| Memory & Graph Pod Lead | `gpt-5.3-codex` | active | future execution owner for Phase 5 | provide planning consultation on module breakdown, graph-local runtime targets, and one-pod execution order | author canonical plan truth alone, implement Phase 5 code in this run, approve the phase |
| World & Conversation Pod Lead | `gpt-5.3-codex` | inactive by default | Phase 5 must stay below world-model and conversation behavior | consult only if Phase 5 planning risks importing Phase 6/7 behavior | author the plan, absorb Phase 6 or 7 behavior |
| Meta & Growth Pod Lead | `gpt-5.3-codex` | inactive | danger zone and not needed | none | activate casually or leak self-improvement logic into Phase 5 |
| Product & Sandbox Pod Lead | `gpt-5.3-codex` | inactive unless narrowly needed | product-runtime and bundle shell are not primary Phase 5 work | consult only if a bundle/runtime-shell seam blocks graph packaging assumptions | author the plan, absorb Phase 13+ scope |
| Test & Replay Lead | `gpt-5.4 mini` | active | Phase 5 needs verifier, evidence, and demo planning from the start | plan graph, provenance, conflict, supersession, support-selection, and transfer verifiers plus evidence expectations | implement runtime behavior, approve the phase |
| Anti-Shortcut Auditor | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | high risk of fake completeness or blind greenfield recreation | detect one-big-graph shortcuts, missing provenance enforcement, silent phase drift, and unsupported completion claims | author canonical plan content, downgrade blockers, approve the phase |
| Merge Arbiter | `gpt-5.3-codex` | inactive | planning-only run | none unless later execution integration is needed | author planning content or approve the phase |
| Validation Agent | `gpt-5.4` | active | final machine-side review of the plan package is required | validate the Phase 5 planning package before user review | author plan content, implement code, or approve the phase |
| Release & Evidence Lead | `gpt-5.4 mini` | active | Phase 5 demos must be inspectable later | define demo bundle shape and evidence packaging only | perform release execution or public-claim packaging |

## 6. Reuse and provenance strategy

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance artifact justification |
| --- | --- | --- | --- | --- |
| descriptor graph | v1 `intelligence/fabric/descriptors/graph.py` descriptor-node and retired-visibility substrate; Phase 4 `graph_refs` anchor pattern | `port_with_provenance` | port the auditable descriptor node/edge substrate and retired-source visibility, but split transfer behavior back out into a dedicated transfer graph | `CC-008`, `CC-009`, `CC-040`, `CC-048`, `SIM-012` |
| skill graph | v2 Phase 4 typed-lineage skill-graph contracts and builder; v1 governed skill-graph acceptance tests as proof target only | `rebuild_clean` | keep typed provenance bundles, semantic-to-procedural grounding, and rejected-mechanism comparison as design input, but do not port rejected old execution packages or a mixed descriptor-skill snapshot verbatim | `CC-086`, `CC-089`, `SIM-050`, `SIM-053` |
| concept graph | v1 `theory_fragment` plus approved Phase 4 semantic memory exports and concept-ready `graph_refs` | `rebuild_clean` | no canonical concept-graph runtime exists; AGIFCore must build a distinct concept graph around reviewed abstractions instead of leaving them buried in semantic memory | `CC-021`, `CC-044`, `SIM-008` |
| transfer graph | v1 explicit transfer approval and materialized provenance path in `descriptors/graph.py`; v1 skill-graph transfer tests | `port_with_provenance` | port the explicit approval, deny, abstain, and provenance-log substrate, but keep later world/simulator-heavy transfer path logic out of Phase 5 | `CC-008`, `CC-009`, `CC-040`, `CC-049`, `SIM-013` |
| provenance links | Phase 2 lineage, replay, rollback, and workspace anchors plus Phase 4 `provenance_refs`, `review_ref`, and `graph_refs`; v2 `GraphProvenanceBundle` as research input | `rebuild_clean` | anchor types are portable, but the enforced AGIFCore provenance-link contract across four graph layers does not exist yet and must be built explicitly | `CC-040`, `CC-042`, `CC-044`, `SIM-004`, `SIM-006` |
| conflict rules | v1 trust-weighted defer and veto patterns in routing and memory review; later v2 transfer-conflict work for research only | `rebuild_clean` | there is no Phase 5-safe conflict engine ready to port; conflict resolution must be explicit, bounded, and graph-local without importing Phase 6 simulation machinery | `CC-045`, `CC-049`, `SIM-009`, `SIM-013` |
| supersession rules | approved Phase 4 supersession markers in semantic and continuity memory; v1 descriptor supersession tests and lifecycle signals | `rebuild_clean` | AGIFCore must build explicit graph-level supersession chains, but those chains must be grounded in existing reviewed-memory and correction markers instead of invented anew | `CC-045`, `CC-044`, `SIM-009` |
| reusable support selection | v1 `routing.py` plus `utility.py` and descriptor-use authority gates; later v2 Phase 9 support graph kept research-only | `port_with_provenance` | routing with utility scoring is the strongest portable selection substrate; Phase 9 support-graph activation hooks are later-runtime behavior and must not be imported into Phase 5 | `CC-048`, `CC-049`, `SIM-012`, `SIM-013`, `RRM-004` |

## 7. Graph boundary rules

### What belongs in descriptor graph only

- reviewed typed descriptors that anchor reusable support
- descriptor-to-descriptor relations such as shared typed pattern or reviewed alias overlap
- retired and superseded descriptor visibility
- descriptor-side trust band, policy requirements, and bounded selection metadata
- explicit links back to reviewed memory entries and provenance anchors

### What belongs in skill graph only

- reusable procedures and callable skill records
- preconditions, postconditions, constraints, and invocation limits
- skill-to-descriptor grounding edges
- allowed target-domain and governance-relevant reuse limits
- explicit non-automatic-execution status

### What belongs in concept graph only

- semantic abstractions and theory fragments
- concept-to-concept relations and typed abstraction tags
- compression-aware conceptual summaries
- semantic supersession chains between reviewed abstractions
- reusable conceptual structure that is not procedural and not transfer approval

### What belongs in transfer graph only

- governed transfer candidates between source and target graph entities
- explicit approval, denial, abstain, and blocked states
- transfer provenance bundles and approval references
- read-only transfer-path records kept below Phase 6 simulator logic
- transfer-specific policy requirements and boundary checks

### What provenance links must represent

- source memory ids, descriptor ids, skill ids, concept ids, and transfer ids when applicable
- review ids and review decisions
- compression, forgetting, and retirement ids when those events shape graph state
- artifact refs, source refs, rollback refs, replay refs, and workspace refs where applicable
- graph-construction lineage and stable provenance hashes
- explicit inherited-versus-constructed origin, not a plain string label

### What conflict rules must represent

- incompatible reuse targets
- lower-trust or lower-provenance candidates losing to higher-trust reviewed candidates
- blocked transfer because explicit approval or policy gate is missing
- reuse blocked by retired or superseded source state
- incompatible skill constraints or target-domain restrictions
- explicit machine-checkable status and reason codes

### What supersession rules must represent

- old-to-new replacement links for descriptors, skills, concepts, and transfer records
- preserved predecessor visibility after replacement
- replayable and reversible replacement history
- bounded chain depth and no silent overwrite
- query-time preference for active reviewed nodes over superseded nodes

### What is explicitly forbidden to leak in from Phase 6 world-model logic

- world relations
- future, fault, or pressure scenario state
- overload or instrumentation simulation results
- world-cell or world-relation prediction outputs
- domain-proof route-of-custody step bodies
- transfer execution enablement, simulator verdicts, or world-model conflict scoring

### What is explicitly forbidden to leak in from Phase 7 conversation behavior

- discourse-mode selection behavior
- clarification and self-knowledge dialogue policy
- response composition or answer rendering
- question-shape activation hooks
- live current-information dependency hooks
- any user-facing language behavior used as a graph shortcut

### How Phase 5 stays separate from Phase 4 memory-plane implementation except through allowed interfaces

- Allowed inputs from Phase 4:
  - semantic, procedural, and continuity export state
  - memory-review export state and `review_ref`
  - approved `provenance_refs`
  - explicit `graph_refs`
  - correction and supersession outputs
  - rollback-safe update history and rollback refs
- Allowed inputs from Phase 2:
  - workspace `memory_review_export`
  - replay refs
  - rollback refs
  - quarantine refs
- Forbidden:
  - direct mutation of Phase 4 stores by graph logic
  - graph persistence inside memory-plane modules
  - raw working-memory or raw episodic state being treated as graph state
  - graph writes occurring during unreviewed capture instead of after reviewed interfaces

## 8. Phase 5 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Phase 5 planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max descriptor-node count before review/escalation | `<= 768` | stop and escalate if the later execution target exceeds `768` descriptor nodes |
| max skill-node count before review/escalation | `<= 256` | stop and reopen planning if the later skill graph exceeds `256` nodes |
| max concept-node count before review/escalation | `<= 512` | stop and review concept retention and grouping if the later concept graph exceeds `512` nodes |
| max transfer-link count before review/escalation | `<= 128` | stop and review transfer boundedness if the later transfer graph exceeds `128` active links |
| max provenance-link fanout | `<= 16` refs per node or edge | stop if any node or edge needs more than `16` provenance refs |
| max conflict set size | `<= 8` competing items per decision | stop and escalate if any conflict group exceeds `8` items |
| max supersession chain length | `<= 4` hops | stop and reopen supersession design if any chain grows beyond `4` |
| max reusable-support candidate set size per query | `<= 24` | stop and tighten selection filters if any query examines more than `24` candidates |
| max Phase 5 evidence/demo bundle size | `<= 64 MiB` | stop and reorganize outputs if the bundle exceeds `64 MiB` |

Budget rules:

- these are laptop-oriented planning ceilings only
- later execution must measure against them directly
- if any ceiling is exceeded, stop and escalate to Program Governor instead of widening silently
- if later execution needs higher ceilings, reopen planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md` | Program Governor | Architecture & Contract Lead | Anti-Shortcut Auditor | Validation Agent | Phase 1 provenance package, approved Phase 2/3/4 baselines, requirements, design pack, admin controls | all later Phase 5 work | section-complete Phase 5 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/` | Program Governor | Constitution Keeper | Anti-Shortcut Auditor | Validation Agent | task-card template, model manifest, tool matrix, this plan | all later valid Phase 5 work | one task card per active role with disjoint planning scope |
| `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/` | Memory & Graph Pod Lead | Architecture & Contract Lead | Anti-Shortcut Auditor | Validation Agent | Phase 5 plan, approved Phase 2/3/4 surfaces, provenance package, trace contract | Phase 5 runtime delivery | later runtime family exists and matches plan |
| `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/` | Memory & Graph Pod Lead | Architecture & Contract Lead | Anti-Shortcut Auditor | Validation Agent | same as above plus exact module breakdown from this plan | Phase 5 runtime delivery | descriptor, skill, concept, transfer, provenance, conflict, supersession, and support-selection modules exist |
| `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/` | Test & Replay Lead | Program Governor | Anti-Shortcut Auditor | Validation Agent | Phase 5 plan, execution family, validation protocol | Phase 5 verification and closeout | verifier family exists and runs |
| `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/` | Test & Replay Lead | Release & Evidence Lead | Anti-Shortcut Auditor | Validation Agent | verifiers, graph exports, provenance reports, transfer reports | audit, governor verification, validation, user demos | machine-readable evidence bundle is inspectable |
| `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/` | Release & Evidence Lead | Program Governor | Anti-Shortcut Auditor | Validation Agent | evidence package, demo protocol, validation protocol | user review | demo bundle exists for graph reuse and transfer |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_EXECUTION_START_BRIEF.md` | Program Governor | Constitution Keeper | Anti-Shortcut Auditor | Validation Agent | approved Phase 5 plan, admin controls | later execution start | execution scope, file families, and no-approval status are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_GOVERNOR_VERIFICATION_RECORD.md` | Program Governor | `n/a` | Anti-Shortcut Auditor | Validation Agent | audited files, rerun verifiers, demo bundle, evidence bundle | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_VALIDATION_REQUEST.md` | Validation Agent | Program Governor | Anti-Shortcut Auditor | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdicts are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_USER_VERDICT.md` | User | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| phase control and prerequisite reconciliation | freeze scope, role activation, task-card map, and closure chain | Program Governor | Constitution Keeper | main Phase 5 plan and task-card map | Phase 4 approved in live phase-truth files | active and inactive roles are fixed and Phase 5 stays inside scope |
| reuse and provenance mapping | map every major Phase 5 subsystem to inherited source basis and one allowed disposition | Source Cartographer | Program Governor, Anti-Shortcut Auditor | reuse table and source-basis notes | provenance package and inspected legacy sources reviewed | each subsystem has explicit source basis, disposition, and rationale |
| graph boundary framing | freeze descriptor, skill, concept, and transfer graph boundaries and allowed interfaces | Architecture & Contract Lead | Program Governor, Source Cartographer, Memory & Graph Pod Lead | graph-boundary rules and future module targets | approved Phase 2/3/4 seams reviewed | no one-big-graph shortcut remains |
| provenance, conflict, and supersession planning | define explicit provenance-link meaning, conflict statuses, and supersession-chain behavior | Architecture & Contract Lead | Constitution Keeper, Source Cartographer, Memory & Graph Pod Lead | provenance/conflict/supersession rule set | graph boundary framing stable | these rules are machine-checkable and not prose-only |
| reusable support selection planning | define bounded graph-assisted support selection grounded in reviewed provenance, trust, and utility | Memory & Graph Pod Lead | Source Cartographer, Architecture & Contract Lead, Constitution Keeper | support-selection plan and later runtime-family targets | reuse decisions and graph boundaries stable | selection stays bounded, review-linked, and Phase 6/7-free |
| graph budget and boundedness planning | freeze laptop-oriented ceilings and stop rules for later execution | Program Governor | Memory & Graph Pod Lead, Test & Replay Lead | budget envelope and escalation map | future runtime-family targets stable | every ceiling and escalation point is explicit |
| test, demo, validation, and evidence planning | define verifier family, evidence family, demo family, and review path | Test & Replay Lead | Release & Evidence Lead, Program Governor, Validation Agent, Anti-Shortcut Auditor | test plan, demo plan, evidence plan, validation surface | runtime-family targets and boundaries stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. Program Governor verifies Phase 4 approval truth and opens the Phase 5 task-card set.
2. Source Cartographer maps all eight major Phase 5 subsystems to source basis and one allowed disposition.
3. Architecture & Contract Lead drafts graph boundary rules in parallel with step 2.
4. Memory & Graph Pod Lead decomposes future execution targets only after first-pass reuse and boundary outputs exist.
5. Constitution Keeper reviews steps 2 through 4 for constitution drift, greenfield recreation, and Phase 6/7 leakage.
6. If a Phase 2 seam is ambiguous after step 5, Kernel Pod Lead is consulted narrowly and remains non-authoring.
7. If a bundle/runtime-shell seam is ambiguous after step 5, Product & Sandbox Pod Lead is consulted narrowly and remains non-authoring.
8. If world-model or conversation logic is trying to leak into the plan, World & Conversation Pod Lead is consulted only to reject that drift, not to broaden scope.
9. Program Governor consolidates the Phase 5 plan, budget envelope, artifact matrix, workstreams, and closure map.
10. Test & Replay Lead and Release & Evidence Lead define verifier, evidence, and demo families after the graph boundaries and runtime-family targets are stable.
11. Anti-Shortcut Auditor audits the complete Phase 5 planning package.
12. Program Governor independently verifies the audited planning package.
13. Validation Agent prepares the later review request.
14. User review happens only after the validated planning package exists.

Safe parallelism:

- Source Cartographer and Architecture & Contract Lead may work in parallel on disjoint planning outputs.
- Memory & Graph Pod Lead waits for first-pass reuse and boundary outputs before locking execution decomposition.
- Test & Replay Lead and Release & Evidence Lead wait for stable runtime-family targets.
- Merge Arbiter remains inactive in planning-only work.
- One active build pod remains the default later execution rule, and that pod is `Memory & Graph Pod Lead`.

## 12. Detailed task cards

User is approval-only and does not receive a task card. Inactive roles receive no Phase 5 task card unless separately reopened by Program Governor.

### `P5-TC-PG-01`

- task card ID: `P5-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, the Phase 5 plan, task-card map, artifact matrix, budget envelope, and closure chain
- exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-PG-01_PHASE_5_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
  - earlier phase-truth files except to report a prerequisite mismatch
- required reads first:
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2, 3, and 4 plans and surfaces
  - graph, memory, workspace, governance, and skill-graph design files
  - admin control stack
- step-by-step work method:
  1. verify Phase 4 approval truth
  2. lock active and inactive roles
  3. consolidate reuse, boundary, budget, verifier, and demo outputs
  4. lock future artifact families and closure mapping
- required cross-checks:
  - no Phase 6 planning
  - no Phase 7 planning
  - no one-big-graph shortcut
  - no approval language
- exit criteria:
  - the plan is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation or approval
- explicit proof that no approval is implied: the task ends at plan readiness only; Phase 5 remains `open`

### `P5-TC-CK-01`

- task card ID: `P5-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4 mini`
- objective: guard constitution, non-negotiables, and Phase 5 boundary discipline
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-CK-01_PHASE_5_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/PHASE_APPROVAL_RULES.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - Phase 5 draft
- step-by-step work method:
  1. check that Phase 5 stays below world-model and conversation logic
  2. check that transfer remains governed and read-only
  3. check that graph support is not hidden autonomy
  4. report any drift to Program Governor
- required cross-checks:
  - no hidden-model loophole
  - no Phase 6 world-state logic
  - no Phase 7 dialogue behavior
  - no approval language
- exit criteria:
  - all constitutional objections are resolved or explicitly blocked
- handoff target: `Program Governor`
- anti-drift rule: do not author architecture or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P5-TC-SC-01`

- task card ID: `P5-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- objective: map every major Phase 5 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-SC-01_PHASE_5_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 2, 3, and 4 plans
  - inspected legacy graph, routing, utility, and transfer files
- step-by-step work method:
  1. map descriptor, skill, concept, transfer, provenance, conflict, supersession, and selection subsystems
  2. assign one allowed disposition to each
  3. flag where v2 remains research-only or rejected
  4. pass unresolved seam notes to ACL and PG
- required cross-checks:
  - no fifth disposition
  - no silent omission
  - no direct carry of rejected v2 execution packages
- exit criteria:
  - each subsystem has source basis, disposition, and rationale
- handoff target: `Architecture & Contract Lead` then `Program Governor`
- anti-drift rule: do not claim inspected historical code is already valid AGIFCore runtime
- explicit proof that no approval is implied: provenance mapping does not earn the phase

### `P5-TC-ACL-01`

- task card ID: `P5-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own graph boundary framing plus provenance, conflict, and supersession contract limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-ACL-01_PHASE_5_GRAPH_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- required reads first:
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/SKILL_GRAPH_MODEL.md`
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - approved Phase 2, 3, and 4 plans
  - Source Cartographer output
- step-by-step work method:
  1. define what belongs in each graph only
  2. define allowed Phase 2/4 interfaces and forbidden leaks
  3. define provenance-link, conflict, and supersession meaning
  4. hand off runtime-family implications to PG and MGP
- required cross-checks:
  - no one mixed graph
  - no world-model state
  - no conversation behavior
  - no direct mutation of memory planes
- exit criteria:
  - graph boundaries and rule meanings are explicit enough to verify later
- handoff target: `Program Governor` then `Memory & Graph Pod Lead`
- anti-drift rule: do not redesign kernel, memory planes, or the team
- explicit proof that no approval is implied: architecture framing is planning truth only

### `P5-TC-MGP-01`

- task card ID: `P5-TC-MGP-01`
- role owner: `Memory & Graph Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 5 execution package and one-pod build order
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-MGP-01_PHASE_5_EXECUTION_DECOMPOSITION.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- required reads first:
  - approved Phase 2, 3, and 4 runtime and plan surfaces
  - Phase 5 draft
  - Source Cartographer output
  - ACL boundary output
- step-by-step work method:
  1. define future runtime family layout under `04_execution/phase_05_graph_and_knowledge_structures/`
  2. order module implementation to preserve one active build pod
  3. identify where Phase 2 and Phase 4 interfaces must be consumed read-only
  4. flag any seam that would require a narrow consultation
- required cross-checks:
  - no runtime code written now
  - no Phase 6/7 module creep
  - no second build pod
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: execution decomposition does not earn the phase

### `P5-TC-TRL-01`

- task card ID: `P5-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4 mini`
- objective: define the Phase 5 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-TRL-01_PHASE_5_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 2, 3, and 4 verifier families
  - Phase 5 draft
- step-by-step work method:
  1. define one verifier per major subsystem group
  2. define evidence reports and manifest contents
  3. define budget-bound and anti-shortcut checks
  4. define failure signatures for each closure requirement
- required cross-checks:
  - tests must verify graph separation
  - provenance must have enforcement meaning
  - transfer must include deny and abstain cases
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P5-TC-ASA-01`

- task card ID: `P5-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- objective: audit the Phase 5 planning package for fake completeness, greenfield recreation, and phase drift
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-ASA-01_PHASE_5_PLAN_AUDIT.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- required reads first:
  - full Phase 5 draft
  - Source Cartographer output
  - ACL boundary output
  - TRL evidence-plan output
  - relevant approved Phase 2/3/4 plans
- step-by-step work method:
  1. check that all required sections exist
  2. check that each major subsystem has a source basis and disposition
  3. check that no one mixed graph or prose-only rule set is being passed off as design
  4. check that no approval or completion claim is implied
- required cross-checks:
  - no blind rewrite where a plausible substrate exists
  - no silent omission of provenance/conflict/supersession/support selection
  - no Phase 6 or 7 behavior smuggled in
- exit criteria:
  - all blockers are either cleared or explicitly raised
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P5-TC-VA-01`

- task card ID: `P5-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 5 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-VA-01_PHASE_5_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - the canonical plan file
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- required reads first:
  - full Phase 5 draft
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

### `P5-TC-REL-01`

- task card ID: `P5-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4 mini`
- objective: define later Phase 5 demo-bundle shape and review packet surfaces
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-REL-01_PHASE_5_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 6+ artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 2, 3, and 4 demo bundles
  - TRL verifier/evidence plan
  - Phase 5 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the graph reuse demo surface
  3. define the transfer demo surface
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

| Closure requirement | Artifact(s) that will satisfy it later | Responsible role | How it will be checked | Failure would look like |
| --- | --- | --- | --- | --- |
| descriptor graph exists | `04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/descriptor_graph.py`, `verify_phase_05_descriptor_graph.py`, descriptor report | Memory & Graph Pod Lead | verifier confirms typed descriptor nodes, retired/superseded visibility, and bounded relations | only Phase 4 `graph_refs` exist; no real descriptor graph runtime |
| skill graph exists | `skill_graph.py`, `verify_phase_05_skill_graph.py`, skill report | Memory & Graph Pod Lead | verifier confirms procedures, constraints, and skill grounding edges | loose tool list or procedural memory dump with no skill graph |
| concept graph exists | `concept_graph.py`, `verify_phase_05_concept_graph.py`, concept report | Memory & Graph Pod Lead | verifier confirms concept nodes and concept-only relations | semantic memory still acts as the only concept structure |
| transfer graph exists | `transfer_graph.py`, `verify_phase_05_transfer_graph.py`, transfer report | Memory & Graph Pod Lead | verifier confirms explicit approve/deny/abstain states and read-only transfer behavior | direct cross-domain copy or hidden Phase 6 transfer path |
| provenance links exist | `provenance_links.py`, `verify_phase_05_provenance_links.py`, provenance report | Memory & Graph Pod Lead | verifier confirms source ids, review ids, rollback/workspace anchors, and provenance hashes are enforced | provenance is only free-text labels with no machine-checkable link meaning |
| conflict rules exist | `conflict_rules.py`, `verify_phase_05_conflict_and_supersession.py` | Memory & Graph Pod Lead | verifier confirms blocked/defer/clear outcomes and reason codes | conflict stays prose-only or always resolves silently |
| supersession rules exist | `supersession_rules.py`, `verify_phase_05_conflict_and_supersession.py` | Memory & Graph Pod Lead | verifier confirms explicit predecessor visibility and bounded supersession chains | silent overwrite or unbounded hidden replacement |
| reusable support selection exists | `support_selection.py`, `verify_phase_05_support_selection.py`, selection report | Memory & Graph Pod Lead | verifier confirms bounded candidate set, trust/provenance/utility use, and no Phase 6/7 behavior | selection ignores graph evidence or just reuses Phase 9 support graph hooks |
| demo path exists | `06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/phase_05_demo_index.md`, `phase_05_graph_reuse_demo.md`, `phase_05_transfer_demo.md` | Release & Evidence Lead | direct demo-bundle inspection | no inspectable demo or demo claims unsupported by evidence |
| tests and evidence path exists | verifier family under `05_testing/...` and evidence manifest under `06_outputs/.../phase_05_evidence/phase_05_evidence_manifest.json` | Test & Replay Lead | governor rerun plus validation request | no machine-readable evidence or missing verifier coverage |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| graph reuse demo | descriptor, skill, and concept graphs; provenance links; support-selection report; demo index; evidence manifest | Release & Evidence Lead from outputs produced by Test & Replay Lead and Memory & Graph Pod Lead | Anti-Shortcut Auditor | graph node and edge examples, provenance anchors, supersession visibility, selection result, and the backing evidence reports |
| transfer demo | transfer graph; provenance links; conflict and supersession reports; explicit approve, deny, and abstain cases; demo index; evidence manifest | Release & Evidence Lead from outputs produced by Test & Replay Lead and Memory & Graph Pod Lead | Anti-Shortcut Auditor | transfer candidate, approval requirement, denial path, abstain path, provenance bundle, and proof that transfer stays read-only and below Phase 6 |

Validation rules for both demos:

- Validation Agent prepares the review request only after audit and governor verification exist.
- Program Governor is the only role that asks the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable graph substrate | compare subsystem plan against mapped v1/v2 sources and approved Phase 4 interfaces | Source Cartographer | any subsystem has no mapped source basis despite plausible legacy substrate | stop and reopen reuse mapping before execution |
| one giant undifferentiated graph pretending to be four graphs | boundary-rule audit and verifier-plan audit | Architecture & Contract Lead | any plan or later code collapses descriptor, skill, concept, and transfer into one unverifiable store | reject the design and split by graph layer before continuing |
| provenance links exist only as labels with no enforcement meaning | provenance-link verifier design review | Architecture & Contract Lead | no machine-checkable source/review/rollback requirements are defined | stop and define enforced provenance-link contract |
| conflict and supersession rules exist only as prose | closure-gate and verifier audit | Test & Replay Lead | no dedicated verifier or runtime family exists for these rules | block closure until explicit runtime and verifier paths exist |
| reusable support selection bypasses graph evidence | selection-plan audit against v1 routing/utility substrate and graph-boundary rules | Memory & Graph Pod Lead | selection result can be produced without provenance, trust, or bounded candidate review | stop and force graph-evidence and utility-bound checks |
| Phase 5 accidentally absorbs Phase 4 memory implementation | interface audit against approved Phase 4 exports | Constitution Keeper | graph layer reaches into raw memory stores or adds graph persistence inside Phase 4 modules | reject the seam and limit access to approved exports only |
| Phase 5 accidentally absorbs Phase 6 world-model behavior | boundary audit against Phase 6-forbidden list | Architecture & Contract Lead | world relations, simulation outputs, or transfer-path world proofs appear in Phase 5 | stop and remove the world-model dependency |
| Phase 5 accidentally absorbs Phase 7 conversation behavior | boundary audit against Phase 7-forbidden list | Constitution Keeper | clarification, self-knowledge, discourse mode, or answer-composition logic appears in Phase 5 | stop and remove the conversation dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 5 plan artifacts
- after user approval, any future change to the Phase 5 plan requires explicit reopen instruction and a supersession note
- Merge Arbiter remains inactive in this planning-only work and may not be activated to imply closure

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 4 is explicitly `approved` in current phase-truth files and in the explicit user verdict record.
- Phase 5 remains `open`.
- The required Phase 1 provenance package, approved Phase 2/3/4 baselines, requirement pack, design pack, admin controls, and legacy source candidates were all reviewed.
- No prerequisite blocker was found.
- Defaults locked by this draft:
  - later execution keeps one active build pod by default: `Memory & Graph Pod Lead`
  - v1 routing-and-utility remains the default support-selection substrate
  - v2 phase 4 skill-graph work, v2 phase 6a transfer path work, and v2 phase 9 support-graph work remain research input only unless a later explicit port decision is justified
  - any shared storage choice later is acceptable only if graph-layer boundaries, budgets, and verifiers remain separate
