# AGIFCore Master Plan

## Summary

Build **AGIFCore** as the new canonical system in `/Users/ahsadin/Documents/AGIFCore`. AGIF v2 is archived as a failed historical attempt for the intended end goal. AGIFCore mines `agif_fabric_v1`, `agif-tasklet-cell`, the root v2 lineage, and `agif_v2_master`, but no old code or old proof counts as done until it is rebuilt or ported into AGIFCore, verified, demoed, and approved by you.

AGIFCore’s end goal is **human-like functional thinking under AGIF rules**:
- understand messy language
- reason through support, planning, simulation, critique, and governance
- remember, correct, and compress memory
- form concepts, strategies, and theories
- run governed self-improvement
- initiate bounded internal inquiry without waiting for a user prompt
- reorganize parts of itself under governance
- stay honest with `clarify`, `search_needed`, `unknown`, or `abstain` when support is weak
- never rely on LLMs, hidden models, or cloud correctness

No phase is earned until:
1. implementation is complete
2. tests and verifiers pass
3. a phase demo is built for you
4. a validation agent asks for your review
5. you explicitly approve it

## Canonical Package And Source-Of-Truth Files

Create these root files:
- `/Users/ahsadin/Documents/AGIFCore/AGENTS.md`
- `/Users/ahsadin/Documents/AGIFCore/README.md`
- `/Users/ahsadin/Documents/AGIFCore/PROJECT_README.md`
- `/Users/ahsadin/Documents/AGIFCore/DECISIONS.md`
- `/Users/ahsadin/Documents/AGIFCore/CHANGELOG.md`

Create this canonical project:
- `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/`

Create these required project-level truth files:
- `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/AGENTS.override.md`
- `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/PROJECT_README.md`
- `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/DECISIONS.md`
- `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/CHANGELOG.md`

Required structure:
- `00_admin/`
- `01_plan/`
- `02_requirements/`
- `03_design/`
- `04_execution/`
- `05_testing/`
- `06_outputs/`
- `07_assets/`
- `08_logs/`

Required planning files:
- `01_plan/MASTER_PLAN.md`
- `01_plan/PHASE_INDEX.md`
- `01_plan/PHASE_GATE_CHECKLIST.md`
- `01_plan/COMPONENT_CATALOG.md`
- `01_plan/SOURCE_INHERITANCE_MATRIX.md`
- `01_plan/RUNTIME_REBUILD_MAP.md`
- `01_plan/TRACE_CONTRACT.md`
- `01_plan/PROOF_DOMAIN_MATRIX.md`
- `01_plan/VALIDATION_PROTOCOL.md`
- `01_plan/DEMO_PROTOCOL.md`
- `01_plan/HUMAN_THINKING_TARGET.md`
- `01_plan/SYSTEM_CONSTITUTION.md`

Required AGIFCore requirement pack:
- `NON_NEGOTIABLES.md`
- `INNOVATION_RULES.md`
- `SCIENTIFIC_METHOD.md`
- `FALSIFICATION_THRESHOLDS.md`
- `BOTTLENECK_ESCALATION_RULES.md`
- `DEPLOYMENT_PROFILES.md`
- `DOMAIN_MATRIX.md`
- `CONVERSATION_SCOPE.md`
- `NORTH_STAR_LANGUAGE_TARGET.md`
- `MACHINE_ROLE_POLICY.md`
- `PHASE_APPROVAL_RULES.md`

Required AGIFCore design pack:
- `ARCHITECTURE_OVERVIEW.md`
- `CELL_FAMILIES.md`
- `COGNITIVE_PRIORS.md`
- `FORMAL_MODELS.md`
- `MEMORY_MODEL.md`
- `SIMULATOR_MODEL.md`
- `GOVERNANCE_MODEL.md`
- `CONVERSATION_MODEL.md`
- `DEPLOYMENT_MODEL.md`
- `SKILL_GRAPH_MODEL.md`
- `GRAPH_STACK_MODEL.md`
- `WORKSPACE_MODEL.md`
- `PRODUCT_RUNTIME_MODEL.md`
- `BUNDLE_INTEGRITY_MODEL.md`
- `SANDBOX_MODEL.md`
- `PUBLIC_RELEASE_MODEL.md`

Before implementation starts for any phase, create the detailed phase plan file for that phase in `01_plan/PHASE_XX_*.md`.

## Frozen Rules, Targets, And Complete Source Coverage

### Core rules
- local-first
- no LLM
- no hidden external model
- no cloud correctness dependency
- language is the surface, not the cognition core
- replayable
- reversible
- auditable
- governed
- fail-closed
- no benchmark-id routing
- no generic filler accepted as intelligence
- no copied old code counts as done without AGIFCore re-verification

### Three-track AGIF definition
- fabric backbone
- mind cells
- conversational surface

### Locked cognition flow
1. input or need capture
2. attention selection
3. working-state build
4. episodic, semantic, and procedural retrieval
5. planner proposal
6. simulator or world-model check
7. critic or error-monitor pass
8. governance or policy pass
9. language realization
10. memory review and selective retention

### Locked scale and profiles
- `1024` logical cells
- `24-40` tissues
- laptop `64-128` active cells
- mobile `8-24` active cells
- builder above laptop
- one literal final cell manifest
- one literal final tissue manifest
- one literal final profile manifest for mobile, laptop, and builder

### Locked proof domains
- `finance_document_workflows`
- `pos_store_operations`
- `procurement_work_order_processing`
- `claims_case_handling`
- `maintenance_diagnostics`
- `building_home_infrastructure_events`
- `planning_coordination_workflows`
- `compliance_support_triage`

Each proof domain must eventually include:
- local baseline
- fabric run without transfer
- fabric run with transfer
- governed conversation layer
- replayable traces
- laptop and mobile profile checks

### Locked cell families
- intake or router
- attention
- working-memory
- episodic memory
- semantic abstraction
- procedural skill
- world-model or simulator
- planner
- critic or error-monitor
- governance or authority
- transfer-broker
- scheduler or resource
- continuity or self-history
- language realizer
- compression or retirement
- audit or replay

### Mandatory row-by-row inheritance matrix
`SOURCE_INHERITANCE_MATRIX.md` must inventory all relevant source logic and truth from:
- `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v1`
- `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif-tasklet-cell`
- `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2`
- `/Users/ahsadin/Documents/Projects/ENF/AGIF/agif_fabric_v2/projects/agif_v2_master`

Every inherited item must be marked exactly one way:
- `rebuild_clean`
- `port_with_provenance`
- `adapt_for_research_only`
- `reject`

Nothing may be silently omitted. Anything not represented in the inheritance matrix or component catalog counts as missing and blocks Phase 1 close.

### Minimum row-by-row coverage from v1
- shared workspace coordination
- `runner/cell fabric` operator family
- lifecycle control: activate, split, merge, hibernate, reactivate, retire
- lineage ledger
- veto log
- rollback snapshots
- quarantine and containment
- reviewed memory with hot, warm, cold, ephemeral tiers
- promotion, deduplication, supersession, compression, retirement, memory GC
- `memory_pressure`
- need signals
- routing with utility scoring
- authority approvals and vetoes
- finance tissue system
- benchmark and evidence machinery
- soak harness
- machine-role policy
- post-closure extensions: organic split/merge, governed descriptor transfer, POS proof
- release note
- claims-to-evidence matrix
- reproducibility package
- final evidence index
- paper-draft status note

### Minimum row-by-row coverage from tasklet
- offline desktop-first shell and UI
- local runner
- gateway/service layer
- schema-enforced contracts
- bundle integrity checks
- strict policy checks
- fail-closed UX
- local session memory
- episodic memory
- deterministic reasoning traces
- installer/distribution flow
- release-readiness flow
- evidence packaging
- SDK and bundle loading
- WASM sandbox
- Wasmtime fuel limits
- Wasmtime memory limits
- Wasmtime wall-time limits
- proactive/background agent lane
- tiny-transformer inference lane
- public release and paper-evidence packaging
- tag and public release asset flow

Default disposition:
- keep or port: offline product discipline, runner/gateway/UI split, fail-closed UX, schema validation, bundle integrity, installer/distribution, release/publication packaging, evidence packaging, sandbox hardening
- research-only or reject by default: tiny-transformer cognition path, proactive-agent cognition path, any hidden model dependence

### Minimum row-by-row coverage from v2 lineage
- root master-plan rewrite logic
- North-Star addendum logic
- all requirement docs
- all design docs
- all reusable execution packages from phases 2 through 10
- `AGIF_V3_CONCEPT.md`
- all `8A`, `8B`, `8C`, `9`, and `10` logic
- all concrete runtime and contract components already identified in code
- publication, hardening, and public release flow from the Phase 10 lane

## Complete Component Catalog And Frozen Contracts

### Exact inherited concrete names that must be cataloged
- `EventType`
- `Event`
- `CellContract`
- `LogicalCell`
- `CellRegistry`
- `LifecycleEngine`
- `Scheduler`
- `transfer_descriptor`
- `target_domain`
- `ScientificPriorCell`
- `SelfModelRecord`
- `MetaCognitionObserverRecord`
- `StrategyJournalEntry`
- `SkepticCounterexampleRecord`
- `SurpriseEngineRecord`
- `ThinkerTissueRecord`
- `SelfModelFeedbackLoopRecord`
- `ReflectionControlLoopRecord`
- `proposal_generator`
- `science_reflection`
- `theory_fragment`
- `strategy_journal`

### Exact inherited conversation-contract items that must be carried or explicitly replaced
- `ConversationTurnRecord`
- `ConversationSnapshot`
- `concept_composition_ref`
- `revision_trace_ref`
- `analogy_trace_ref`
- `consolidation_trace_ref`
- `reorganization_trace_ref`

### Exact inherited tissue-role names
- `proof-intake`
- `world-model-review`
- `planner`
- `simulator`
- `critic`
- `governance`
- `audit`

### Exact Phase 9 runtime modules that must be mapped in `RUNTIME_REBUILD_MAP.md`
- `runtime.py`
- `orchestrator.py`
- `question_analyzer.py`
- `support_graph.py`
- `memory_runtime.py`
- `answer_composer.py`
- `idle_reflection.py`
- `whole_stack_activation.py`
- `demo_shell.py`
- `contracts.py`

### Full AGIFCore subsystem list
- typed event fabric
- event bus
- shared workspace state
- cell registry
- lifecycle engine
- scheduler
- active/dormant budgets
- replay ledger
- rollback and quarantine
- fail-closed governance
- common cell contracts
- tissue manifests and routing
- split/merge behavior
- trust bands
- activation rules
- working memory
- episodic memory
- semantic memory
- procedural memory
- continuity/self-history
- promotion, compression, forgetting, retirement
- descriptor graph
- skill graph
- concept graph
- transfer graph
- provenance and conflict links
- world model
- simulator
- candidate futures
- fault, pressure, overload, and conflict simulation
- instrumentation and usefulness scoring
- raw text intake
- intent grounding
- messy-language handling
- support-state model
- self-knowledge surface
- clarification behavior
- audience model
- discourse planning
- utterance planning
- surface realization
- scientific priors
- entity and request inference
- world-region selection
- causal-chain construction
- current-world honesty boundary
- self model
- meta-cognition layer
- attention redirect
- meta-cognition observer
- skeptic/counterexample
- strategy journal
- thinker tissue
- surprise engine
- theory fragments
- science reflection
- offline reflection and consolidation
- idle reflection
- proposal generation
- self-experiment lab
- shadow evaluation
- before/after measurement
- adoption or rejection pipeline
- post-adoption monitoring
- rollback-safe adoption or rejection
- thought episodes
- self-initiated inquiry engine
- self-model feedback loop
- reflection control loop
- self-reorganization
- domain genesis
- theory formation
- procedure/tool invention
- curiosity and gap selection
- embeddable runtime API
- local runner
- local gateway
- local desktop UI
- operator command family
- state export
- trace export
- memory review export
- safe shutdown
- bundle integrity
- schema validation
- installer/distribution flow
- release notes
- claims matrix
- paper-draft status note
- final evidence index
- public release package
- GitHub/public release asset flow
- tag/release flow
- paper/publication package
- public evidence-bundle alignment
- evidence bundles
- blind packs
- live demo packs
- soak and closure-audit machinery

### Frozen conversation and operator contract
Create `TRACE_CONTRACT.md` and freeze these turn fields:
- `conversation_id`
- `turn_id`
- `user_intent`
- `active_context_refs`
- `planner_trace_ref`
- `simulation_trace_ref`
- `critic_trace_ref`
- `governance_trace_ref`
- `response_text`
- `abstain_or_answer`
- `memory_review_ref`

Freeze these richer conversation fields:
- `discourse_mode`
- `support_state`
- `knowledge_gap_reason`
- `next_action`

Allowed `discourse_mode` values:
- `status`
- `explain`
- `compare`
- `teach`
- `analogy`
- `plan`
- `synthesize`
- `critique_rewrite`
- `clarify`
- `self_knowledge`
- `abstain`

Allowed `support_state` values:
- `grounded`
- `inferred`
- `search_needed`
- `unknown`

Allowed `knowledge_gap_reason` values:
- `none`
- `ambiguous_request`
- `missing_local_evidence`
- `conflicting_state`
- `blocked_by_policy`
- `needs_fresh_information`
- `out_of_scope`

Allowed `next_action` values:
- `answer`
- `clarify`
- `search_local`
- `search_external`
- `abstain`

Final answer modes:
- `grounded_fact`
- `derived_estimate`
- `derived_explanation`
- `hypothesis`
- `clarify`
- `search_needed`
- `unknown`
- `abstain`

Freeze the operator command family:
- `agifcore fabric init`
- `agifcore fabric run`
- `agifcore fabric status`
- `agifcore fabric replay`
- `agifcore fabric evidence`

Freeze the product runtime split:
- runner core
- local gateway/API
- local desktop UI

Freeze the machine-role policy:
- laptop is the primary reference product machine
- builder is for diagnostics and deeper instrumentation, not correctness privilege
- optional soak machine may exist for endurance evidence only
- correctness may never depend on a separate soak machine
- imported soak artifacts require provenance and may not replace primary-machine reproducibility

## Phase Ladder

### Phase 0: AGIFCore reset and source freeze
Build:
- repo scaffold
- archival note marking AGIF v2 as failed for the intended end goal
- source-freeze inventory rules
- planning file skeletons

User validation:
- project structure
- archival statement
- source-freeze method

### Phase 1: constitution and full-system blueprint
Build:
- constitution
- human-thinking target
- full requirement pack
- full design pack
- component catalog
- source inheritance matrix
- runtime rebuild map
- proof-domain matrix
- trace contract
- phase index and checklist

Phase 1 cannot close until:
- every source pool has row-by-row inheritance coverage
- all required AGIFCore project-level truth files exist
- all required requirement files exist
- all required design files exist
- all 8 proof domains are frozen explicitly
- all exact inherited component names above are cataloged
- all exact runtime modules above are mapped
- operator command family is frozen
- machine-role policy is frozen
- runner/gateway/UI split is frozen
- bundle integrity and sandbox rules are frozen
- release/publication lane is frozen explicitly

User validation:
- full architecture demo
- inheritance matrix demo
- requirement pack demo
- design pack demo

### Phase 2: fabric kernel and workspace
Build:
- typed event fabric
- event bus
- shared workspace state
- registry
- lifecycle
- scheduler
- replay
- rollback
- quarantine
- fail-closed kernel behavior

User validation:
- kernel trace demo
- replay demo
- rollback/quarantine demo
- shared-workspace demo

### Phase 3: cells, tissues, structure, and bundles
Build:
- cell contracts
- tissue manifests
- activation policies
- trust bands
- split/merge rules
- active/dormant control
- profile budget rules
- bundle schema validation
- bundle integrity checks

User validation:
- tissue orchestration demo
- split/merge demo
- bundle validation demo

### Phase 4: memory planes
Build:
- working, episodic, semantic, procedural, continuity memory
- correction handling
- promotion
- compression
- forgetting
- retirement
- memory review
- rollback-safe updates

User validation:
- memory carry-forward demo
- correction demo
- forgetting/compression demo

### Phase 5: graph and knowledge structures
Build:
- descriptor, skill, concept, transfer graphs
- provenance
- conflict/supersession rules
- reusable support selection

User validation:
- graph reuse demo
- transfer demo

### Phase 6: world model and simulator
Build:
- world-model representation
- entity classes
- target-domain structures
- candidate futures
- what-if simulation
- fault, pressure, overload, and conflict lanes
- instrumentation and usefulness scoring

User validation:
- causal simulation demo
- stress/conflict demo

### Phase 7: conversation core
Build:
- raw text intake
- question interpretation
- support-state logic
- self-knowledge surface
- clarification
- utterance planner
- surface realizer
- answer contract
- anti-generic filler guardrails

User validation:
- messy-question live demo
- self-knowledge demo
- honest abstain/search-needed demo

### Phase 8: science and world awareness
Build:
- scientific priors
- entity/request inference
- world-region selection
- causal-chain reasoning
- bounded current-world reasoning
- visible reasoning summaries
- science reflection

User validation:
- science explanation demo
- bounded live-fact demo

### Phase 9: rich expression and composition
Build:
- teaching
- comparison
- planning
- synthesis
- analogy
- concept composition
- cross-domain composition
- audience-aware explanation quality

User validation:
- rich-expression demo
- non-generic chat-quality demo

### Phase 10: meta-cognition and critique
Build:
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

User validation:
- “why was this weak” demo
- contradiction demo

### Phase 11: governed self-improvement
Build:
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

User validation:
- self-improvement demo
- rollback demo
- bounded self-initiated inquiry demo

### Phase 12: structural growth
Build:
- self-model feedback
- reflection control
- self-reorganization
- domain genesis
- theory formation
- procedure/tool invention
- curiosity/gap selection

User validation:
- structural-growth demo
- theory-growth demo

### Phase 13: product runtime and UX
Build:
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

User validation:
- end-to-end product demo
- fail-closed UX demo
- installer/distribution demo

### Phase 14: sandbox, profiles, and scale realization
Build:
- WASM sandbox for isolated packaged execution where needed
- Wasmtime fuel limits
- Wasmtime memory limits
- Wasmtime wall-time limits
- literal `1024`-cell manifest
- literal `24-40` tissue manifest
- mobile/laptop/builder profile manifests
- active-cell budget enforcement
- dormant-cell survival proofs

User validation:
- sandbox enforcement demo
- laptop demo
- mobile constrained demo
- manifest audit demo

### Phase 15: final intelligence proof and closure audit
Build:
- blind packs
- hidden packs
- live-demo pack
- soak harness
- hardening package
- reproducibility package
- closure audit

User validation:
- final AGIFCore demo
- soak summary
- closure audit summary

### Phase 16: release, publication, and public evidence package
Build:
- release notes
- claims matrix
- paper-draft status note
- final evidence index
- public release package
- GitHub/public release asset flow
- tag/release flow
- paper/publication package
- public evidence-bundle alignment
- public reproducibility package
- support and handoff material

User validation:
- release package review
- publication/evidence review

## Important Interfaces And Validation

Standardize these early and keep them stable:
- `CellManifest`
- `TissueManifest`
- `EventRecord`
- `WorkspaceState`
- `ConversationTurnRecord`
- `ConversationSnapshot`
- `TurnRecord`
- `StateSnapshot`
- `EpisodeRecord`
- `ConceptRecord`
- `TheoryRecord`
- `StrategyRecord`
- `ProposalRecord`
- `AdoptionRecord`
- `ThoughtEpisodeRecord`
- `BundleManifest`
- `SandboxPolicy`
- `DemoSessionRecord`
- `VerifierResultBundle`

Minimum runtime API:
- `session_open`
- `conversation_turn`
- `state_snapshot`
- `idle_cycle`
- `trace_export`
- `memory_review_export`
- `policy_update`
- `safe_shutdown`

Every phase must ship:
- unit tests
- integration tests
- replay determinism checks
- rollback checks
- anti-shortcut checks
- machine-readable evidence
- demo guide for you
- validation-agent handoff
- your recorded verdict

Required artifacts per phase:
- `05_testing/.../verify_*.py`
- `06_outputs/.../*_evidence.json`
- `00_admin/codex_threads/handoffs/*_validation_request.md`
- `00_admin/codex_threads/handoffs/*_user_verdict.md`

Allowed user verdicts:
- `approved`
- `rejected`
- `approved_with_blockers`

Only `approved` earns the phase.

Required test families across the program:
- all 8 proof domains
- messy wording and vague questions
- correction memory and continuity
- self-knowledge questions
- science explanation
- bounded current-world questions
- teaching, comparison, planning, synthesis, analogy
- contradiction and weak-answer diagnosis
- self-improvement before/after proof
- rollback and quarantine
- split/merge and structural pressure
- shared-workspace coordination
- bundle integrity and schema validation
- runner/gateway/UI contract checks
- sandbox fuel, memory, and wall-time limits
- laptop/mobile/builder profile behavior
- long-run soak and recovery
- release/publication package integrity
- final live demo by you

Final AGIFCore acceptance must prove:
- no hidden LLM or cloud correctness path
- no benchmark routing tricks
- no generic filler accepted as intelligence
- real memory and correction behavior
- real graph, world-model, and simulator use
- real support-state honesty
- real critique and revision
- real governed self-improvement
- real self-initiated inquiry in bounded governed form
- real structural adaptation
- real product runtime
- real scale/profile behavior
- real public evidence/release package
- your explicit final approval

## Assumptions And Defaults

- AGIFCore is a new canonical build in `/Users/ahsadin/Documents/AGIFCore`.
- AGIF v2 remains archived as historical failure for the intended end goal.
- Old repos are mined aggressively, but nothing is trusted without AGIFCore re-verification.
- v1 supplies the strongest fabric, shared workspace, reviewed memory, routing, authority, tissue, rollback, quarantine, operator command, and soak foundations.
- tasklet supplies the strongest offline product, runner/gateway/UI split, fail-closed UX, schema contract, bundle integrity, installer/distribution, release/publication discipline, evidence packaging, and sandbox patterns.
- tasklet tiny-transformer and proactive-agent cognition paths are not part of the AGIFCore default intelligence core.
- “think like a human” means human-like functional cognition under AGIF rules, proven by behavior, not by style alone.

