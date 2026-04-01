# Phase 14: Sandbox, Profiles, and Scale Realization

Brief summary:

Phase 14 plans the governed sandbox, profile, and scale layer that sits above approved Phase 13 product runtime and below Phase 15 final proof/closure-audit work and Phase 16 release/publication work. It must later deliver explicit sandbox enforcement, explicit Wasmtime limits, literal final cell/tissue manifests, explicit mobile/laptop/builder profile manifests, active-cell budget enforcement, and dormant-cell survival proofs without turning deployment control into hidden correctness privilege or final-proof theater.

Planned interface additions for later execution:

- runtime family under `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/`
- thin snapshot `agifcore.phase_14.sandbox_profile_runtime.v1`
- thin sandbox contract `agifcore.phase_14.sandbox_policy.v1`
- thin manifest contracts:
  - `agifcore.phase_14.cell_manifest.v1`
  - `agifcore.phase_14.tissue_manifest.v1`
  - `agifcore.phase_14.profile_manifest.v1`
- thin enforcement/proof contracts:
  - `agifcore.phase_14.wasmtime_fuel_limits.v1`
  - `agifcore.phase_14.wasmtime_memory_limits.v1`
  - `agifcore.phase_14.wasmtime_wall_time_limits.v1`
  - `agifcore.phase_14.active_cell_budget.v1`
  - `agifcore.phase_14.dormant_survival_proof.v1`

Planning defaults chosen:

- later execution keeps one active build pod by default: `Product & Sandbox Pod Lead`
- later execution must preserve the Phase 13 public runtime contract across mobile, laptop, and builder
- later execution must keep soak harness, closure audit, blind packs, hidden packs, and public release work out of Phase 14
- the existing project-scoped `.codex` setup is reusable as-is; no maintenance change is required before Phase 14 planning or later execution start

## 1. Phase identity

- Phase number: `14`
- Canonical phase name: `Sandbox, Profiles, and Scale Realization`
- Status: `planning_draft`
- Source-of-truth references reviewed:
  - repo policy stack: `AGENTS.md`, `projects/agifcore_master/AGENTS.override.md`, `PROJECT_README.md`, `DECISIONS.md`, `CHANGELOG.md`
  - master truth and gates: `MASTER_PLAN.md`, `PHASE_INDEX.md`, `PHASE_GATE_CHECKLIST.md`
  - phase plans: `PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md` through `PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
  - Phase 1 provenance and closure stack: `SYSTEM_CONSTITUTION.md`, `HUMAN_THINKING_TARGET.md`, `COMPONENT_CATALOG.md`, `SOURCE_INHERITANCE_MATRIX.md`, `RUNTIME_REBUILD_MAP.md`, `TRACE_CONTRACT.md`, `VALIDATION_PROTOCOL.md`, `DEMO_PROTOCOL.md`
  - all files under `projects/agifcore_master/02_requirements/`
  - all files under `projects/agifcore_master/03_design/`
  - approved Phase 2 through Phase 13 execution/testing/output families under `04_execution/`, `05_testing/`, and `06_outputs/`
  - admin controls under `projects/agifcore_master/00_admin/`
  - `.codex/config.toml` and `.codex/agents/*.toml`
  - direct donor inspection focused on wasm hardening, deployment profiles, mobile profile verification, and lifecycle/dormant semantics from `agif-tasklet-cell`, `agif_fabric_v1`, and `agif_fabric_v2/projects/agif_v2_master`

## 2. Phase mission

- Phase 14 exists to define and later build the explicit enforcement and scale-realization layer that governs isolated packaged execution and profile-constrained runtime scale above approved Phase 13 product-runtime truth.
- Phase 14 must later build:
  - WASM sandbox for isolated packaged execution where needed
  - Wasmtime fuel limits
  - Wasmtime memory limits
  - Wasmtime wall-time limits
  - literal `1024`-cell manifest
  - literal `24-40` tissue manifest
  - mobile profile manifest
  - laptop profile manifest
  - builder profile manifest
  - active-cell budget enforcement
  - dormant-cell survival proofs
- Phase 14 must not:
  - redesign or replace Phase 13 runner/gateway/UI contracts
  - change correctness rules between mobile, laptop, and builder
  - implement Phase 15 final proof, soak harness, or closure audit
  - implement Phase 16 release/publication behavior
  - treat sandboxing as a substitute for bundle integrity
  - treat builder or soak as correctness privilege
  - let manifests become decorative labels instead of enforced boundaries
  - imply commit, freeze, approval, or closure

## 3. Scope and non-goals

- In-scope artifacts:
  - canonical Phase 14 plan
  - Phase 14 planning task cards
  - sandbox/profile/scale boundary rules
  - reuse and provenance decisions
  - future execution/testing/output/handoff targets
  - later demo, validation, and closure mapping
- Out-of-scope work:
  - any Phase 14 runtime code
  - any Phase 14 verifier code
  - any Phase 14 evidence generation
  - any Phase 15 planning or execution
  - any Phase 16 planning or execution
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
- Explicit untouched-later-phase statement:
  - Phase 15 and all later phases remain untouched by this plan.

## 4. Phase 13 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 13 explicitly approved in current phase-truth files | `pass` | `PHASE_INDEX.md` and `PHASE_GATE_CHECKLIST.md` show Phase 13 `approved`, Phase 14 `open` | Phase 14 planning may proceed |
| Explicit Phase 13 closeout truth exists outside index tables | `pass` | `DECISIONS.md` and `CHANGELOG.md` record Phase 13 approval | no silent approval assumption |
| Required Phase 1 provenance artifacts relied on exist | `pass` | constitution, provenance, validation, and demo files are present | provenance and closure framing exist |
| Required Phase 2 through 13 artifacts relied on exist | `pass` | approved plans and execution/testing/output families exist | downstream seams are inspectable |
| Custom-agent setup is reusable | `pass` | `.codex/config.toml` and `.codex/agents/*.toml` parse cleanly; `phase_builder` already names `Product & Sandbox Pod Lead` | no setup blocker |
| Canonical Phase 14 plan file not present yet | `non-blocker` | expected planning target | normal planning target |
| Phase 14 planning task folder not present yet | `non-blocker` | expected planning target | normal planning target |
| Phase 14 contract family does not exist yet | `non-blocker` | no approved sandbox/profile/scale runtime family exists yet | Phase 14 must define it cleanly above approved Phase 13 truth |
| Literal manifests do not exist yet | `non-blocker` | cell/tissue/profile manifests are frozen targets, not current files | Phase 14 must materialize them from AGIFCore truth |
| Dormant survival proof family does not exist yet | `non-blocker` | lifecycle semantics exist but proof family does not | Phase 14 must define a real proof path |
| Blockers vs non-blockers | `planning not blocked` | prerequisites are satisfied | readiness may be `ready_for_user_review` |

Required Phase 1 through 13 artifacts relied on:

- Phase 1 provenance and admin-control package
- approved Phase 2 kernel/workspace baseline
- approved Phase 3 structure/bundle/profile-budget baseline
- approved Phase 4 memory baseline
- approved Phase 5 graph baseline
- approved Phase 6 world-model baseline
- approved Phase 7 conversation baseline
- approved Phase 8 science/world-awareness baseline
- approved Phase 9 expression/composition baseline
- approved Phase 10 meta-cognition baseline
- approved Phase 11 self-improvement baseline
- approved Phase 12 structural-growth baseline
- approved Phase 13 product-runtime baseline
- existing project-scoped `.codex` agent package

## 5. Active team map for Phase 14

Later Phase 14 execution default build pod: `Product & Sandbox Pod Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | What it must never do this phase |
| --- | --- | --- | --- | --- | --- |
| `Program Governor` | `gpt-5.4` | active | prerequisite truth, phase boundary control, and final integration are required | own prerequisite truth, `.codex` verification, role activation, plan integration, artifact matrix, closure map, and final readiness judgment | implement runtime code, validate its own authored artifacts, or broaden into Phase 15 or 16 |
| `Constitution Keeper` | `gpt-5.4-mini` | active | sandbox/profile work can quietly create hidden privilege or hidden autonomy | guard fail-closed discipline, same-truth-across-profiles rule, no hidden privilege, and no phase-leak drift | author runtime design alone, approve the phase, or allow proof/release leakage |
| `Source Cartographer` | `gpt-5.4-mini` | active | donor sandbox/profile substrate is real and must not be recreated blindly | map each Phase 14 subsystem to donor basis, disposition, and reuse limits | invent a fifth disposition, treat donor proof bundles as earned AGIFCore proof, or approve the phase |
| `Architecture & Contract Lead` | `gpt-5.4` | active | Phase 14 needs strict sandbox/profile/manifest boundaries above Phase 13 | own subsystem boundaries, allowed Phase 13 interfaces, forbidden Phase 15 and 16 leaks, and the Phase 14 contract strategy | redesign earlier phases, collapse all Phase 14 behavior into one opaque deployment shell, or approve the phase |
| `Kernel Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if lifecycle/runner seams become ambiguous | consult on activation, dormancy, rollback, quarantine, and runner interaction only if ambiguity appears | author the plan, implement code, or broaden Phase 2 |
| `Memory & Graph Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if dormant-survival or persistence seams become ambiguous | consult on dormant-state persistence, memory refs, graph anchors, and continuity refs only if ambiguity appears | author the plan, implement code, or pull Phase 14 into memory/graph work |
| `World & Conversation Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if profile effects on public surface seams become ambiguous | consult on preserving same public contract and abstain behavior across profiles | author the plan, implement code, or absorb Phase 14 into lower phases |
| `Meta & Growth Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if structural-growth runtime exposure becomes ambiguous under budgets | consult on how Phase 12 outputs stay visible without escaping profile budgets | author the plan, implement code, or widen scope into meta/runtime redesign |
| `Product & Sandbox Pod Lead` | `gpt-5.3-codex` | active | later execution owner and default build pod for Phase 14 | decompose future sandbox/profile/manifest/budget/proof family | author canonical plan truth alone, implement code in this run, or absorb Phase 15/16 scope |
| `Test & Replay Lead` | `gpt-5.4-mini` | active | claims about sandbox and scale must be verifier-planned from the start | define verifier family, manifest audits, profile checks, budget checks, dormant-survival checks, and closure failure signatures | implement runtime logic, fabricate reports, or approve the phase |
| `Anti-Shortcut Auditor` | `gpt-5.4-mini` | active | sandbox/profile work can look complete in notes while lacking enforcement | audit for fake sandbox policies, fake manifests, fake budgets, fake dormant proofs, and phase-leak drift | rewrite the plan instead of auditing it, downgrade blockers casually, or approve the phase |
| `Merge Arbiter` | `gpt-5.3-codex` | inactive | planning-only run | none | imply closure or perform merge work |
| `Validation Agent` | `gpt-5.4` | active | machine-side review of the planning package is required before user review | validate the planning package after audit and Governor verification exist | author the plan, implement runtime, or approve the phase |
| `Release & Evidence Lead` | `gpt-5.4-mini` | active | later demos must be inspectable and evidence-linked | define demo bundle shape, manifest-audit presentation, and review packet order | implement runtime behavior, publish release material, or imply acceptance |

## 6. Reuse and provenance strategy

Only the frozen four dispositions are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance artifact justification |
| --- | --- | --- | --- | --- |
| WASM sandbox | `agif-tasklet-cell` wasm bundle/runtime substrate plus `V6_WASM_HARDENING_CONTRACT.md` | `port_with_provenance` | donor-side isolated wasm execution and fail-closed enforcement are concrete and machine-checkable | `COMPONENT_CATALOG.md` `CC-074`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-038`; `SANDBOX_MODEL.md` |
| Wasmtime fuel limits | tasklet v6 hardening contract limit records and failure codes | `port_with_provenance` | fuel-limit contract and fail codes already exist as explicit lineage | `COMPONENT_CATALOG.md` `CC-075`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-039` |
| Wasmtime memory limits | tasklet v6 hardening contract max-memory records and limit hits | `port_with_provenance` | explicit memory cap lineage already exists | `COMPONENT_CATALOG.md` `CC-076`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-040` |
| Wasmtime wall-time limits | tasklet v6 hardening contract wall-time cap and timeout semantics | `port_with_provenance` | explicit timeout lineage already exists | `COMPONENT_CATALOG.md` `CC-077`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-041` |
| literal `1024`-cell manifest | AGIFCore `MASTER_PLAN.md`, approved Phase 3 structural-budget truth, donor v2 locked scale target | `rebuild_clean` | the frozen count is inherited, but the final AGIFCore manifest must be authored from approved AGIFCore cell/tissue truth, not copied from donor inventories | `MASTER_PLAN.md`; `CELL_FAMILIES.md`; approved Phase 3 structural budget lines |
| literal `24-40` tissue manifest | AGIFCore `MASTER_PLAN.md`, approved Phase 3 tissue structure truth, donor v2 locked tissue band | `rebuild_clean` | the band is inherited, but the final tissue manifest must reflect AGIFCore-approved tissue structure and cross-tissue boundaries | `MASTER_PLAN.md`; `CELL_FAMILIES.md`; approved Phase 3 structure plan |
| mobile profile manifest | AGIFCore `DEPLOYMENT_PROFILES.md`, AGIFCore `DEPLOYMENT_MODEL.md`, v2 deployment profiles, v2 mobile profile verification | `port_with_provenance` | the same-architecture mobile constraint and `8-24` band are already frozen and verifier-backed donor-side | `DEPLOYMENT_PROFILES.md`; `DEPLOYMENT_MODEL.md`; `PHASE_8A_MOBILE_PROFILE_VERIFICATION.md` |
| laptop profile manifest | AGIFCore `DEPLOYMENT_PROFILES.md`, AGIFCore `DEPLOYMENT_MODEL.md`, v2 deployment profiles | `port_with_provenance` | laptop as reference profile and same-contract rule are already explicit and portable | `DEPLOYMENT_PROFILES.md`; `DEPLOYMENT_MODEL.md` |
| builder profile manifest | AGIFCore `DEPLOYMENT_PROFILES.md`, AGIFCore `DEPLOYMENT_MODEL.md`, v2 deployment profiles | `port_with_provenance` | builder-as-diagnostic-only and no-correctness-privilege rule are already explicit and portable | `DEPLOYMENT_PROFILES.md`; `DEPLOYMENT_MODEL.md` |
| active-cell budget enforcement | approved Phase 3 active/dormant control plus profile-budget rules, v1 lifecycle model, v2 profile verification patterns | `port_with_provenance` | activation/dormancy semantics and profile-bounded runtime already exist conceptually and structurally | `COMPONENT_CATALOG.md` `CC-039`; Phase 3 profile-budget and active/dormant planning truth |
| dormant-cell survival proofs | v1 lifecycle model, AGIFCore Phase 3 active/dormant control, AGIFCore Phase 13 safe shutdown/export lineage | `rebuild_clean` | dormant semantics are inherited, but AGIFCore needs a new proof family tied to its own manifests, profile budgets, and shutdown/restart evidence | `COMPONENT_CATALOG.md` `CC-039` to `CC-043`; `LIFECYCLE_MODEL.md`; approved Phase 3 and Phase 13 baselines |

## 7. Sandbox/profile/scale boundary rules

### What belongs in WASM sandbox only

- isolated packaged execution boundary
- sandbox-policy loading and deny/allow routing
- enforcement receipts for sandbox decisions
- no public UX, no gateway ownership, no cognition logic

### What belongs in Wasmtime fuel limits only

- explicit execution-step budget classes
- limit-hit detection and receipts
- deterministic fail-closed response when fuel is exceeded
- no memory or wall-time tuning logic beyond its own class tables

### What belongs in Wasmtime memory limits only

- explicit memory-cap classes
- memory-peak measurement and limit-hit receipts
- deterministic fail-closed memory denial path
- no fuel or wall-time ownership

### What belongs in Wasmtime wall-time limits only

- explicit elapsed-time classes
- timeout detection and timeout receipts
- deterministic fail-closed timeout path
- no fuel or memory ownership

### What belongs in the literal cell manifest only

- exact `1024` logical cell identities
- family assignment, lineage anchors, activation eligibility, and profile eligibility
- no live runtime state, no proof claims, no product UX ownership

### What belongs in the literal tissue manifest only

- exact `24-40` tissue identities
- cell-to-tissue placement and tissue-boundary structure
- tissue-level active-cap and coordination metadata
- no final proof or release claims

### What belongs in profile manifests only

- mobile, laptop, and builder profile definitions only
- same-contract, same-architecture, same-truth rules
- profile-specific active-cell bands and diagnostics allowances
- no soak harness, no correctness privilege, no final-proof claims

### What belongs in active-cell budget enforcement only

- live enforcement that activation stays within profile bands
- deterministic block/hibernate/deny receipts when budgets would be exceeded
- no silent widening and no cell-family rewrites

### What belongs in dormant-cell survival proofs only

- verifier-backed cases showing dormant cells retain identity, lineage, policy envelope, and memory/continuity refs under profile pressure and shutdown/restart
- no final proof/closure audit language and no public-release summaries

### What is explicitly forbidden to leak in from Phase 15 final proof/closure-audit behavior

- blind packs
- hidden packs
- live-demo pack
- soak harness
- hardening package
- reproducibility package
- closure audit
- soak summary or closure-audit summary framing

### What is explicitly forbidden to leak in from Phase 16 release/publication behavior

- release notes
- claims matrix authoring
- public evidence index
- GitHub/public release asset flow
- tag/release flow
- paper/publication package
- public reproducibility package
- support/handoff publication materials

### How Phase 14 stays separate from Phase 13 product-runtime behavior except through allowed interfaces

Allowed Phase 13 inputs:

- approved Phase 13 runner/gateway/API surfaces
- approved Phase 13 exports and safe-shutdown receipts
- approved Phase 13 installer/distribution truth only where packaging boundaries need profile metadata
- approved bundle-integrity rules from earlier design truth

Rules for those inputs:

- Phase 14 may constrain packaged execution and runtime scale through explicit policies, manifests, and budget receipts
- Phase 14 may not redesign the Phase 13 public runtime contract or turn gateway/UI into profile-specific truth owners
- Phase 14 may not create profile-specific correctness divergence
- sandbox/profile enforcement must remain inspectable through approved runtime/export lanes

## 8. Phase 14 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max sandbox policy count | `<= 12` policies | stop and reopen boundary planning if later execution needs more than `12` policy records |
| max Wasmtime fuel classes | `<= 4` classes | stop and simplify limit taxonomy if more than `4` fuel classes are proposed |
| max Wasmtime memory classes | `<= 4` classes | stop and simplify limit taxonomy if more than `4` memory classes are proposed |
| max Wasmtime wall-time classes | `<= 4` classes | stop and simplify limit taxonomy if more than `4` wall-time classes are proposed |
| max profile manifest count | `<= 3` manifests | stop if soak or extra profile manifests appear in Phase 14 |
| max active-cell budget states | `<= 5` states | stop and consolidate if enforcement requires more than `5` public budget states |
| max dormant-cell survival proof cases | `<= 12` cases | stop and refactor proof family if more than `12` cases are needed |
| max Phase 14 evidence/demo bundle size | `<= 224 MiB` | stop and reorganize outputs if the bundle exceeds `224 MiB` |

Budget rules:

- these are planning ceilings only
- they are laptop-profile oriented where relevant
- later execution must measure against them directly
- any ceiling breach must stop and escalate instead of widening silently
- any later higher ceiling requires reopened planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2-13 baselines, admin controls, donor inspection | all later Phase 14 work | section-complete Phase 14 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, plan | all later valid Phase 14 work | one planning task card per active role |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_PLAN_FREEZE_HANDOFF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 14 plan and admin controls | later execution start | frozen scope and no-approval status explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_EXECUTION_START_BRIEF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 14 plan and admin controls | later execution start | execution scope and boundary rules explicit |
| `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/` | `Product & Sandbox Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 13 runtime, Phase 14 plan, provenance package, sandbox and deployment models | later Phase 14 runtime delivery | runtime family exists and matches the plan |
| `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/` | `Product & Sandbox Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | same plus exact module breakdown from this plan | later Phase 14 runtime delivery | sandbox, limits, manifests, budgets, and dormant-proof modules exist |
| `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 14 plan, execution family, validation protocol, demo protocol | later verification and closeout | verifier family exists and runs |
| `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifier outputs, manifest captures, sandbox receipts, budget reports, demo traces | audit and Governor verification | machine-readable evidence bundle is inspectable |
| `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, validation protocol, demo scripts | user review | sandbox, laptop, mobile, and manifest-audit demos exist |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-AUDIT-01_PHASE_14_FINAL_PACKAGE_AUDIT_REPORT.md` | `Anti-Shortcut Auditor` | `Program Governor` | `n/a` | `Validation Agent` | runtime, tests, evidence, demos, planning truth | Governor verification | standard final audit exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, rerun verifiers, demo bundle, evidence bundle | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdict request explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| sandbox and limit-policy planning | define isolated wasm execution, policy boundary, and explicit Wasmtime limit families | `Product & Sandbox Pod Lead` | `Architecture & Contract Lead`, `Constitution Keeper`, `Kernel Pod Lead` consult-only | future `sandbox_policy.py`, `wasmtime_fuel_limits.py`, `wasmtime_memory_limits.py`, `wasmtime_wall_time_limits.py`, `sandbox_profile_shell.py` | prerequisite truth and reuse map exist | sandbox and limits are explicit and separate from profile/manifest/proof work |
| manifest and profile planning | define final literal cell/tissue manifests and mobile/laptop/builder profile manifests | `Product & Sandbox Pod Lead` | `Source Cartographer`, `Architecture & Contract Lead`, `Kernel Pod Lead` consult-only | future `cell_manifest.py`, `tissue_manifest.py`, `profile_manifests.py` | reuse map and scale targets are stable | manifest/profile boundaries are explicit and same-truth rule is preserved |
| active-cell budget and dormant-survival planning | define budget enforcement and real dormant-survival proof family | `Architecture & Contract Lead` | `Product & Sandbox Pod Lead`, `Constitution Keeper`, `Memory & Graph Pod Lead` consult-only | future `active_cell_budget.py`, `dormant_cell_survival.py` | manifest/profile rules are stable | budget receipts and dormant proofs are explicit and inspectable |
| test, demo, validation, and evidence planning | define verifier family, evidence manifest, demo bundle, and review path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | verifier plan, evidence plan, demo plan, validation surfaces | runtime-family targets are stable | later review path is inspectable and machine-readable |

## 11. Ordered execution sequence

1. `Program Governor` verifies Phase 13 approval truth and confirms Phase 14 remains `open`.
2. `Program Governor` verifies the reusable `.codex` package and records that no maintenance change is required.
3. `Program Governor` locks active, consult-only, and inactive roles for Phase 14 planning.
4. `Source Cartographer` maps all Phase 14 subsystems to donor basis and one allowed disposition.
5. `Architecture & Contract Lead` drafts subsystem boundaries, allowed Phase 13 interfaces, and forbidden Phase 15/16 leaks.
6. `Product & Sandbox Pod Lead` drafts the future runtime-family decomposition after first-pass reuse and boundary outputs exist.
7. `Constitution Keeper` reviews the first-pass sandbox/profile plan for hidden privilege, hidden autonomy, and fail-closed weakness.
8. `Kernel Pod Lead` is consulted only if lifecycle/runner seams are ambiguous.
9. `Memory & Graph Pod Lead` is consulted only if dormant-survival persistence seams are ambiguous.
10. `World & Conversation Pod Lead` is consulted only if same-contract public-surface seams are ambiguous.
11. `Meta & Growth Pod Lead` is consulted only if Phase 12 outputs under profile budgets become ambiguous.
12. `Test & Replay Lead` and `Release & Evidence Lead` define verifier, evidence, demo, and review-packet families after runtime-family targets stabilize.
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

### `P14-TC-PG-01`

- task card ID: `P14-TC-PG-01`
- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, `.codex` verification, canonical Phase 14 plan, role activation, artifact matrix, budget envelope, closure map, and readiness judgment
- exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-PG-01_PHASE_14_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 15 and later artifacts
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - `.codex/agents/*`
- required reads first:
  - `ROLE_AUTHORITY_RULES.md`
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 through 13 plans and execution surfaces
  - requirement and design files relevant to sandbox/deployment/lifecycle
  - `.codex` setup files
- step-by-step work method:
  1. verify prerequisite truth
  2. verify `.codex` setup contents
  3. lock role activation
  4. consolidate reuse, boundary, decomposition, verifier, and demo outputs
  5. lock artifact families and closure mapping
  6. prepare the package for audit
- required cross-checks:
  - no Phase 15 planning
  - no Phase 16 planning
  - no runtime implementation
  - no approval language
- exit criteria:
  - the Phase 14 planning package is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation or approval
- explicit proof that no approval is implied: Phase 14 remains `open`

### `P14-TC-CK-01`

- task card ID: `P14-TC-CK-01`
- role owner: `Constitution Keeper`
- model tier: `gpt-5.4-mini`
- objective: guard fail-closed, same-truth-across-profiles, and no hidden-privilege rules
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-CK-01_PHASE_14_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 15 and later artifacts
- required reads first:
  - `SYSTEM_CONSTITUTION.md`
  - `NON_NEGOTIABLES.md`
  - `FALSIFICATION_THRESHOLDS.md`
  - `SCIENTIFIC_METHOD.md`
  - `DEPLOYMENT_PROFILES.md`
  - the Phase 14 draft
- step-by-step work method:
  1. check fail-closed sandbox behavior
  2. check that profile budgets do not become correctness privilege
  3. check that manifests and proofs stay evidence-bound
  4. report any boundary drift to `Program Governor`
- required cross-checks:
  - no hidden privilege
  - no hidden-model loophole
  - no silent degrade path
  - no Phase 15 or 16 behavior
  - no approval language
- exit criteria:
  - constitutional objections are resolved or raised explicitly
- handoff target: `Program Governor`
- anti-drift rule: do not author runtime design or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P14-TC-SC-01`

- task card ID: `P14-TC-SC-01`
- role owner: `Source Cartographer`
- model tier: `gpt-5.4-mini`
- objective: map each Phase 14 subsystem to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-SC-01_PHASE_14_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - `.codex/`
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 15 and later artifacts
- required reads first:
  - `COMPONENT_CATALOG.md`
  - `SOURCE_INHERITANCE_MATRIX.md`
  - `RUNTIME_REBUILD_MAP.md`
  - approved Phase 2 through 13 plans and execution surfaces
  - donor wasm/profile/lifecycle files
- step-by-step work method:
  1. map all eleven Phase 14 subsystems
  2. assign one allowed disposition to each
  3. flag where inherited contract is stronger than whole-module portability
  4. pass unresolved seams to `Architecture & Contract Lead` and `Program Governor`
- required cross-checks:
  - no fifth disposition
  - no silent omission
  - no donor proof treated as earned AGIFCore proof
- exit criteria:
  - each subsystem has source basis, disposition, and rationale
- handoff target: `Architecture & Contract Lead` then `Program Governor`
- anti-drift rule: do not claim donor code is already valid AGIFCore runtime
- explicit proof that no approval is implied: provenance mapping does not earn the phase

### `P14-TC-ACL-01`

- task card ID: `P14-TC-ACL-01`
- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 14 boundaries, allowed Phase 13 interfaces, forbidden leaks, and the Phase 14 contract strategy
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-ACL-01_PHASE_14_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 15 and later artifacts
- required reads first:
  - `SANDBOX_MODEL.md`
  - `DEPLOYMENT_MODEL.md`
  - `BUNDLE_INTEGRITY_MODEL.md`
  - `PRODUCT_RUNTIME_MODEL.md`
  - `TRACE_CONTRACT.md`
  - approved Phase 13 plan and runtime surfaces
  - `Source Cartographer` output
- step-by-step work method:
  1. define what belongs in each Phase 14 subsystem only
  2. define allowed Phase 13 interfaces
  3. define manifest/profile/budget/proof contract strategy
  4. define forbidden Phase 15 and 16 leaks
  5. pass runtime-family implications to `Program Governor` and `Product & Sandbox Pod Lead`
- required cross-checks:
  - no giant deployment shell
  - no profile-specific correctness divergence
  - no sandbox-as-integrity-substitute
  - no Phase 15 or 16 semantics
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `Product & Sandbox Pod Lead`
- anti-drift rule: do not redesign earlier phases or the team
- explicit proof that no approval is implied: boundary framing is planning truth only

### `P14-TC-PSPL-01`

- task card ID: `P14-TC-PSPL-01`
- role owner: `Product & Sandbox Pod Lead`
- model tier: `gpt-5.3-codex`
- objective: decompose the future Phase 14 sandbox/profile/scale family without crossing into Phase 15 or 16
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-PSPL-01_PHASE_14_SANDBOX_PROFILE_SCALE_DECOMPOSITION.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 15 and later artifacts
- required reads first:
  - approved Phase 2 through 13 plans and execution surfaces
  - the Phase 14 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` output
  - `SANDBOX_MODEL.md`
  - `DEPLOYMENT_MODEL.md`
  - `BUNDLE_INTEGRITY_MODEL.md`
- step-by-step work method:
  1. define the future runtime family under `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/`
  2. keep the module set explicit:
     - `contracts.py`
     - `sandbox_policy.py`
     - `wasmtime_fuel_limits.py`
     - `wasmtime_memory_limits.py`
     - `wasmtime_wall_time_limits.py`
     - `cell_manifest.py`
     - `tissue_manifest.py`
     - `profile_manifests.py`
     - `active_cell_budget.py`
     - `dormant_cell_survival.py`
     - `sandbox_profile_shell.py`
  3. order implementation so contracts come first, then sandbox and limit families, then manifests and profiles, then budget enforcement, then dormant proofs, then the thin shell last
  4. identify where Phase 13 runtime interfaces are consumed without mutation
- required cross-checks:
  - no runtime code written now
  - no Phase 15 behavior
  - no Phase 16 behavior
  - no hidden correctness privilege
- exit criteria:
  - future module family, execution order, and stop points are explicit
- handoff target: `Program Governor`
- anti-drift rule: do not author canonical plan truth alone and do not implement code in this run
- explicit proof that no approval is implied: decomposition does not earn the phase

### `P14-TC-TRL-01`

- task card ID: `P14-TC-TRL-01`
- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4-mini`
- objective: define the Phase 14 verifier, evidence, and closure-check family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-TRL-01_PHASE_14_TEST_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 15 and later artifacts
- required reads first:
  - `VALIDATION_PROTOCOL.md`
  - `DEMO_PROTOCOL.md`
  - approved Phase 13 verifier and evidence families
  - the Phase 14 draft
- step-by-step work method:
  1. define one verifier per major Phase 14 subsystem
  2. define cross-cutting manifest-audit, profile-same-truth, budget-enforcement, and dormant-survival checks
  3. define evidence reports and manifest contents
  4. define sandbox, laptop, mobile, and manifest-audit demo verification hooks
- required cross-checks:
  - tests must verify explicit separation between sandbox, limits, manifests, profiles, budgets, and dormant proofs
  - profile equality of public contract must be machine-checkable
  - dormant proofs must be evidence-backed, not prose
  - no soak/final-proof/public-release creep
- exit criteria:
  - later test and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P14-TC-ASA-01`

- task card ID: `P14-TC-ASA-01`
- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4-mini`
- objective: audit the Phase 14 planning package for fake sandboxing, fake manifests, fake budgets, fake dormant proofs, and phase-leak drift
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-ASA-01_PHASE_14_PLAN_AUDIT.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 15 and later artifacts
- required reads first:
  - full Phase 14 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` output
  - `Test & Replay Lead` output
  - relevant approved Phase 3 and Phase 13 truth
- step-by-step work method:
  1. check that all required sections exist
  2. check that each subsystem has source basis and disposition
  3. check that no giant deployment shell is being passed off as design
  4. check that no approval or completion claim is implied
- required cross-checks:
  - no blind rewrite where plausible substrate exists
  - no silent omission of required subsystems
  - no Phase 15 or 16 behavior smuggled in
  - no empty manifest, budget, or proof path
- exit criteria:
  - all blockers are cleared or raised explicitly
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P14-TC-VA-01`

- task card ID: `P14-TC-VA-01`
- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 14 planning package before user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-VA-01_PHASE_14_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 15 and later artifacts
- required reads first:
  - full Phase 14 draft
  - audit output
  - Governor verification output
  - validation protocol
- step-by-step work method:
  1. confirm the plan is decision-complete
  2. confirm every closure requirement has a later artifact path
  3. confirm later demos are inspectable and truthful
  4. confirm role separation and review-surface completeness
- required cross-checks:
  - no author/validator collision
  - no missing review surface
  - no implied approval
- exit criteria:
  - review request scope is exact and inspectable
- handoff target: `Program Governor`
- anti-drift rule: do not author plan content or runtime behavior
- explicit proof that no approval is implied: validation asks for review and does not mark the phase earned

### `P14-TC-REL-01`

- task card ID: `P14-TC-REL-01`
- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4-mini`
- objective: define the later Phase 14 demo-bundle shape and review packet order
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-REL-01_PHASE_14_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 15 and later artifacts
- required reads first:
  - `DEMO_PROTOCOL.md`
  - approved Phase 13 demo bundle
  - `Test & Replay Lead` verifier/evidence plan
  - the Phase 14 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the sandbox enforcement demo surface
  3. define the laptop and mobile constrained demo surfaces
  4. define the manifest audit demo surface
  5. define the user-review packet order
- required cross-checks:
  - demos must stay inspectable from files alone
  - no demo may imply acceptance or phase completion
  - no Phase 15 or 16 packaging creep
- exit criteria:
  - later review packet is exact, ordered, and bounded
- handoff target: `Program Governor` then `Validation Agent`
- anti-drift rule: do not expand into release execution or public claims
- explicit proof that no approval is implied: demo-package planning is not demo acceptance

## 13. Closure-gate mapping

| Closure requirement | Artifact(s) that will satisfy it later | Role responsible | How it will be checked | What failure would look like |
| --- | --- | --- | --- | --- |
| sandbox exists | `sandbox_policy.py`, `verify_phase_14_sandbox.py`, `phase_14_sandbox_report.json` | `Product & Sandbox Pod Lead` | verifier confirms isolated packaged execution, fail-closed denies, and evidence receipts | sandbox claims with no real policy engine or no deny receipts |
| Wasmtime fuel limits exist | `wasmtime_fuel_limits.py`, `verify_phase_14_wasmtime_fuel.py`, `phase_14_wasmtime_fuel_report.json` | `Product & Sandbox Pod Lead` | verifier confirms explicit fuel classes and deterministic limit-hit receipts | labels only, missing classes, or silent overrun |
| Wasmtime memory limits exist | `wasmtime_memory_limits.py`, `verify_phase_14_wasmtime_memory.py`, `phase_14_wasmtime_memory_report.json` | `Product & Sandbox Pod Lead` | verifier confirms explicit memory classes and deterministic memory-limit receipts | labels only or silent overuse |
| Wasmtime wall-time limits exist | `wasmtime_wall_time_limits.py`, `verify_phase_14_wasmtime_wall_time.py`, `phase_14_wasmtime_wall_time_report.json` | `Product & Sandbox Pod Lead` | verifier confirms explicit timeout classes and deterministic timeout receipts | labels only or silent timeout escape |
| literal cell manifest exists | `cell_manifest.py`, `verify_phase_14_cell_manifest.py`, `phase_14_cell_manifest_report.json` | `Product & Sandbox Pod Lead` | verifier confirms literal `1024` logical-cell inventory and manifest integrity | approximate count, missing lineage anchors, or placeholder manifest |
| literal tissue manifest exists | `tissue_manifest.py`, `verify_phase_14_tissue_manifest.py`, `phase_14_tissue_manifest_report.json` | `Product & Sandbox Pod Lead` | verifier confirms literal `24-40` tissue inventory and tissue-boundary integrity | placeholder tissue list or out-of-band tissue count |
| profile manifests exist | `profile_manifests.py`, `verify_phase_14_profile_manifests.py`, `phase_14_profile_manifest_report.json` | `Product & Sandbox Pod Lead` | verifier confirms mobile/laptop/builder manifests preserve same contract and profile-specific budgets only | notes-only profiles, extra profiles, or correctness divergence |
| active-cell budget enforcement exists | `active_cell_budget.py`, `verify_phase_14_active_cell_budget.py`, `phase_14_active_cell_budget_report.json` | `Product & Sandbox Pod Lead` | verifier confirms profile bands are enforced with deterministic block/hibernate receipts | budget claims with no live enforcement or silent widening |
| dormant-cell survival proofs exist | `dormant_cell_survival.py`, `verify_phase_14_dormant_cell_survival.py`, `phase_14_dormant_survival_report.json` | `Product & Sandbox Pod Lead` | verifier confirms dormant identity, lineage, refs, and restart continuity across proof cases | prose-only proof or loss of dormant continuity |
| demo path exists | `phase_14_demo_index.md`, `run_phase_14_sandbox_enforcement_demo.py`, `run_phase_14_laptop_profile_demo.py`, `run_phase_14_mobile_constrained_demo.py`, `run_phase_14_manifest_audit_demo.py` | `Release & Evidence Lead` | direct demo-bundle inspection and rerunnable demo scripts | no inspectable demo or unsupported demo claims |
| tests/evidence path exists | full verifier family under `05_testing/phase_14_sandbox_profiles_and_scale_realization/` and `phase_14_evidence_manifest.json` | `Test & Replay Lead` | Governor rerun plus validation request | missing verifier coverage, missing manifest, or non-machine-readable evidence |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| sandbox enforcement demo | sandbox policy runtime, all three Wasmtime limit families, deny receipts, demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Product & Sandbox Pod Lead` | `Anti-Shortcut Auditor` | allowed run, denied run, limit-hit receipts, and proof that execution stayed fail-closed |
| laptop demo | laptop profile manifest, active-cell budget enforcement, same Phase 13 public contract, demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Product & Sandbox Pod Lead` | `Anti-Shortcut Auditor` | laptop profile manifest, reference-band behavior, same runtime contract, and budget receipts |
| mobile constrained demo | mobile profile manifest, constrained active-cell band, same public contract, abstain/fail-closed behavior, demo script, and evidence manifest | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Product & Sandbox Pod Lead` | `Anti-Shortcut Auditor` | mobile profile manifest, `8-24` band evidence, same-contract proof, and constrained but truthful behavior |
| manifest audit demo | literal cell manifest, literal tissue manifest, profile manifests, budget bindings, manifest verifier outputs, and demo guide | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Product & Sandbox Pod Lead` | `Anti-Shortcut Auditor` | exact `1024`-cell manifest, exact `24-40` tissue manifest, profile manifests, hashes, and manifest audit results |

Validation rules:

- `Validation Agent` prepares the review request only after standard audit and Governor verification exist.
- `Program Governor` is the only role that asks the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.
- If Phase 15 or Phase 16 behavior appears during later Phase 14 execution, the correct action is to stop and escalate boundary drift.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable sandbox/profile substrate | compare planned/runtime artifacts against mapped donor files and exact inherited contracts | `Source Cartographer` | a subsystem is rebuilt from zero despite clear donor basis | stop and reopen reuse mapping before execution |
| one giant deployment shell pretending to do sandbox, profiles, manifests, and budget enforcement | boundary audit and verifier-plan audit | `Architecture & Contract Lead` | one opaque module is asked to own most Phase 14 behavior | reject the design and split the lanes before continuing |
| sandbox policies existing only as labels | sandbox verifier and demo audit | `Constitution Keeper` | policies appear without real deny/allow enforcement and receipts | stop and require real sandbox behavior |
| profile manifests existing only as notes | manifest verifier and manifest-audit demo | `Source Cartographer` | profiles are described without machine-readable manifests and counts | stop and require real manifests |
| active-cell budget enforcement existing only as claims | budget verifier and cross-profile runs | `Test & Replay Lead` | profile bands exist in prose without real block/hibernate receipts | stop and require real enforcement |
| dormant-cell survival proofs existing only as prose | dormant-survival verifier and restart-case audit | `Test & Replay Lead` | dormant continuity is asserted without proof cases and receipts | stop and require real proof cases |
| Phase 14 accidentally absorbing Phase 15 final-proof behavior | boundary audit against the forbidden Phase 15 list | `Program Governor` | soak harness, blind packs, hidden packs, hardening package, reproducibility package, or closure audit appear in Phase 14 | stop and remove final-proof dependency |
| Phase 14 accidentally absorbing Phase 16 release/publication behavior | boundary audit against the forbidden Phase 16 list | `Release & Evidence Lead` | release notes, claims matrix, public evidence index, or release asset flow appear in Phase 14 | stop and remove release/publication dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 14 plan artifacts
- after user approval, any future change to the Phase 14 plan requires explicit reopen instruction and a supersession note

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 13 is explicitly `approved` in the live phase-truth files and corroborated by decision and changelog records.
- Phase 14 remains `open`.
- The required provenance stack, approved Phase 2 through 13 baselines, requirements pack, design pack, admin controls, and donor sandbox/profile substrate were reviewed directly.
- No prerequisite blocker was found.
- The main non-blocker seams are:
  - Phase 14 has no AGIFCore sandbox/profile contract family yet and must layer above approved Phase 13 truth instead of mutating it.
  - the strongest wasm/limit lineage is donor-side in tasklet hardening contract surfaces, so AGIFCore should port that enforcement discipline with provenance rather than recreate it.
  - literal cell/tissue manifests and dormant-survival proof cases are AGIFCore-specific artifacts and should be rebuilt cleanly from approved AGIFCore structural truth.
  - mobile/laptop/builder profile truth is already frozen in AGIFCore and strongly corroborated by donor v2 profile verification, so profile manifests should package that truth rather than invent new profile semantics.
- Defaults locked by this draft:
  - later execution keeps one active build pod by default: `Product & Sandbox Pod Lead`
  - wasm sandbox and Wasmtime limit families default toward `port_with_provenance`
  - literal cell/tissue manifests and dormant-cell survival proofs default toward `rebuild_clean`
  - mobile/laptop/builder profile manifests and active-cell budget enforcement default toward `port_with_provenance`
  - Phase 14 remains a governed sandbox/profile/scale layer above approved Phase 13 outputs and below Phase 15 and Phase 16 behavior
