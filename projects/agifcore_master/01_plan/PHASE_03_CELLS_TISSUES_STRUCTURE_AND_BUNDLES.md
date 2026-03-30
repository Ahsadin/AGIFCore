# Phase 3: Cells, Tissues, Structure, and Bundles

## Summary

Phase 3 plans the later build of the structural layer that sits on top of the approved Phase 2 kernel and workspace. It is not a greenfield rewrite. The default posture is:

- port the strongest cell, tissue, lifecycle, and lineage substrate from `agif_fabric_v1`
- port the strongest schema-contract and bundle-integrity substrate from `agif-tasklet-cell`
- keep `root v2 lineage` and `agif_v2_master` as research context only unless the frozen provenance package already authorizes carry-over
- keep one primary authoring lane in planning and one build pod by default in later execution

Planned later interface surfaces in the Phase 3 execution family:

- `CellContract`
- `TissueManifest`
- `ActivationPolicy`
- `TrustBand`
- `SplitProposal`
- `MergeProposal`
- `ProfileBudgetRule`
- `BundleManifest`

Planning defaults chosen here:

- trust bands are a controlled AGIFCore rebuild because no direct frozen trust-band module exists in the provenance package
- profile budget rules are a controlled AGIFCore rebuild on top of frozen deployment profiles and the approved Phase 2 scheduler constraints
- tissue manifests are port-with-provenance at the substrate level, not a claim that one literal final AGIFCore tissue-manifest module already exists
- later Phase 3 execution default build pod is `Kernel Pod Lead`
- Phase 3 stays above the Phase 2 kernel and below Phase 4 memory and Phase 5 graph work

## 1. Phase identity

- Phase number: `3`
- Canonical phase name: `Cells, Tissues, Structure, and Bundles`
- Status: `planning_draft`
- Canonical artifact path: `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
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
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`

## 2. Phase mission

- Phase 3 exists to define and later build the governed structural layer that turns the Phase 2 kernel into explicit cells, tissues, and bundle-ready composition units.
- Phase 3 must build later:
  - cell contracts
  - tissue manifests
  - activation policies
  - trust bands
  - split and merge rules
  - active and dormant control
  - profile budget rules
  - bundle schema validation
  - bundle integrity checks
- Phase 3 must not:
  - re-implement the Phase 2 kernel, scheduler, replay, rollback, quarantine, or fail-closed surfaces
  - implement Phase 4 memory planes
  - implement Phase 5 graph persistence or graph policies
  - implement Phase 6 world-model or simulator behavior
  - implement Phase 7 conversation behavior
  - weaken the frozen trace contract, approval chain, or anti-shortcut rules
  - claim runtime completion from historical repos alone
  - approve itself

## 3. Scope and non-goals

### In scope

- this Phase 3 planning artifact
- the Phase 3 task-card map
- the reuse and provenance strategy for each structural subsystem
- the future execution-family plan for `04_execution/phase_03_cells_tissues_structure_and_bundles/`
- the future testing-family plan for `05_testing/phase_03_cells_tissues_structure_and_bundles/`
- the future outputs, evidence, and demo family plan for `06_outputs/phase_03_cells_tissues_structure_and_bundles/`
- the later audit, governor-verification, validation-request, and user-review path

### Out of scope

- any runtime implementation in this run
- any file under `04_execution/` as part of this planning run
- Phase 4 memory implementation
- Phase 5 graph implementation
- simulator, world-model, or conversation behavior
- product-runtime or sandbox execution work beyond the structural bundle seam Phase 3 must plan
- any commit, freeze, tag, merge, or approval action

### Phase 3 boundary rules

- Cell contracts must align to the approved Phase 2 identity and state substrate in `cell_registry.py`, `lifecycle_engine.py`, `event_types.py`, and `workspace_state.py`.
- Tissue manifests may coordinate cells and routing boundaries, but they may not smuggle in Phase 4 memory logic, Phase 5 graph logic, or product-runtime logic.
- Split and merge rules must reuse the already approved Phase 2 lifecycle states and transitions instead of inventing a second structural state machine.
- Bundle schema validation and bundle integrity checks must stay fail-closed and must remain separate from later sandbox isolation. Sandbox is not a substitute for integrity.

### Phase 3 structural budget envelope

These are planning ceilings for later Phase 3 execution. They are not achieved measurements.

Master-plan hard ceilings:

| Budget item | Master-plan hard ceiling | Source |
| --- | --- | --- |
| logical cells | `1024` | `MASTER_PLAN.md` |
| laptop active cells | `64-128` | `MASTER_PLAN.md` |
| mobile active cells | `8-24` | `MASTER_PLAN.md` |
| tissues | `24-40` | `MASTER_PLAN.md` |

Stricter Phase 3 implementation ceilings:

| Budget item | Phase 3 implementation ceiling | Why |
| --- | --- | --- |
| laptop active cells during Phase 3 execution | `<= 32` | keep the structural layer bounded and below the master-plan hard ceiling |
| mobile active cells during Phase 3 execution | `<= 8` | keep the constrained profile honest during first structural execution |
| tissues during Phase 3 execution | `<= 12` | hold orchestration and evidence volume inside a first-pass reviewable range |
| cells per tissue before split pressure or review | `<= 8` | force explicit structural review before tissues become oversized |
| dormant blueprint count before review or escalation | `<= 128` | prevent silent dormant-structure buildup |
| manifest size | `<= 64 KiB` | keep structure files small, inspectable, and local-first |
| bundle payload size | `<= 8 MiB` | keep bundle review and local verification practical on laptop profile |
| tissue membership fanout per tissue | `<= 16` direct cell members | bound complexity and orchestration load |
| routing targets per tissue manifest | `<= 8` | keep routing complexity reviewable in Phase 3 |

Budget rules:

- these are Phase 3 planning ceilings only
- later execution must measure against them
- if any Phase 3 ceiling is exceeded, stop and escalate to Program Governor
- do not silently widen Phase 3 ceilings
- if work needs the master-plan hard ceilings to be approached, reopen planning before continuing

### Explicit statement

Phase 4 and later phases remain untouched by this plan.

## 4. Phase 2 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 2 explicitly approved in current phase-truth files | `pass` | `projects/agifcore_master/01_plan/PHASE_INDEX.md` and `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` both show Phase 2 `approved` | Phase 3 planning may proceed |
| Required Phase 1 artifacts relied on exist | `pass` | provenance package, trace contract, validation and demo protocol, requirement pack, and design pack exist | planning has the required Phase 1 inputs |
| Required Phase 2 artifacts relied on exist | `pass` | approved plan, runtime, verifier, evidence, demo, audit, governor verification, validation request, and user verdict all exist on disk | planning has the required kernel and workspace baseline |
| Dependency gaps that block planning | `none` | no missing prerequisite artifact blocks planning | no prerequisite stop |
| Non-blocker note: trust-band substrate | `present` | no direct frozen trust-band component row exists in the Phase 1 provenance package | requires controlled rebuild, not a planning stop |
| Non-blocker note: future Phase 3 artifact families | `present` | no Phase 3 execution, testing, or output families exist yet | expected starting condition, not a blocker |
| Blockers vs non-blockers | `planning not blocked` | current gaps are expected Phase 3 outputs, not unmet prerequisites | readiness is `ready_for_user_review` |

## 5. Active team map for Phase 3

| Role | Model tier | Status | Why | Exact responsibility this phase | Must never do this phase |
| --- | --- | --- | --- | --- | --- |
| User | none | active | final human approver remains required | later approve or reject the Phase 3 plan | delegate final approval |
| Program Governor | `gpt-5.4` | active | phase control, dependency truth, and sequencing remain central | own the Phase 3 plan, task-card map, work order, artifact matrix, and closure chain | implement Phase 3 runtime code, self-approve, broaden into Phase 4 |
| Constitution Keeper | `gpt-5.4 mini` | active | Phase 3 can drift into hidden autonomy, Phase 4 memory, or Phase 5 graph scope | guard constitution, non-negotiables, trust-band honesty, and scope boundaries | author runtime design on its own, approve phase |
| Source Cartographer | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | reuse discipline is central to Phase 3 | map each subsystem to source basis, disposition, and provenance expectations | invent a fifth disposition, treat v2 runtime as already valid, approve phase |
| Architecture & Contract Lead | `gpt-5.4` | active | Phase 3 needs precise cell, tissue, bundle, and kernel seam framing | own cell contract framing, tissue-manifest framing, structural-governance seams, and contract alignment to Phase 2 | drift into Phase 4 or 5 implementation, weaken Phase 2 constraints, approve phase |
| Kernel Pod Lead | `gpt-5.3-codex` | inactive by default for planning-only work; later Phase 3 execution default build pod | Phase 3 must respect the approved Phase 2 substrate and later needs one build pod owner | consult only if registry, lifecycle, scheduler, or workspace seam becomes ambiguous in planning; own later Phase 3 execution by default | author the Phase 3 plan, implement runtime code in this planning run, approve phase |
| Memory & Graph Pod Lead | `gpt-5.3-codex` | inactive | Phase 3 must not absorb Phase 4 or 5 | none unless a narrow drift question requires a boundary clarification | absorb memory or graph scope |
| World & Conversation Pod Lead | `gpt-5.3-codex` | inactive | not needed for structural planning | none | absorb Phase 6 through 9 scope |
| Meta & Growth Pod Lead | `gpt-5.3-codex` | inactive | danger zone and unnecessary here | none | activate casually or leak self-improvement into Phase 3 |
| Product & Sandbox Pod Lead | `gpt-5.3-codex` | inactive by default, consult only if needed | bundle and integrity planning may later need a narrow runtime-shell seam check | consult only if bundle-validation boundaries cannot be resolved from the current design and provenance pack | author the Phase 3 plan, absorb Phase 13 through 16 scope |
| Test & Replay Lead | `gpt-5.4 mini` | active | structural checks, bundle validation, and demos must be planned from the start | define verifiers, structure checks, bundle-validation checks, integrity checks, and evidence expectations | implement runtime behavior, approve phase |
| Anti-Shortcut Auditor | `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only | active | high risk of greenfield drift or fake structure completeness | detect silent omission, unsupported carry claims, and phase drift | author canonical content, downgrade blockers, approve phase |
| Merge Arbiter | `gpt-5.3-codex` | inactive | planning-only run | none until later execution integration is needed | author plan content or approve phase |
| Validation Agent | `gpt-5.4` | active | final machine-side review of the plan package is required before user review | validate the Phase 3 plan package and prepare the later review request | author the plan or approve phase |
| Release & Evidence Lead | `gpt-5.4 mini` | active | later demos must be inspectable and self-contained | define demo bundle shape and evidence grouping only | perform release execution or public-claim packaging |

## 6. Reuse and provenance strategy

Only the frozen four disposition categories are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

Where a row below refers to a reusable substrate or structural pattern rather than one literal historical AGIFCore-ready module, that clarification appears in rationale only and does not create a new disposition type.

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Phase 1 provenance justification |
| --- | --- | --- | --- | --- |
| cell contracts | `SRC-001 agif_fabric_v1` exact `CellContract` name and cell identity substrate; `SRC-002` schema-enforced contract discipline | `port_with_provenance` | the common contract surface already exists and should port with AGIFCore verification rather than be recreated from zero; Phase 3 should align it to the approved Phase 2 registry, lifecycle, and event substrate | `COMPONENT_CATALOG.md` `CC-003`, `CC-004`, `CC-005`, `CC-063`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-027` |
| tissue manifests | `SRC-001` `ThinkerTissueRecord`, logical-cell and registry substrate, tissue foundations; `SRC-003` tissue role vocabulary only as research context | `port_with_provenance` | the tissue substrate and record vocabulary are real carry candidates, but AGIFCore still needs its own canonical manifest schema and routing fields; v2 tissue-role refinements stay non-default and research-only | `COMPONENT_CATALOG.md` `CC-016`, `CC-004`, `CC-005`, `CC-032`, `CC-034`, `CC-035`, `CC-036`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-001` |
| activation policies | `SRC-001` lifecycle control, need-signal framing, scheduler/resource substrate; approved Phase 2 `lifecycle_engine.py` and `scheduler.py` | `port_with_provenance` | activation already has bounded triggers, lifecycle transitions, and budget-aware scheduling substrate; Phase 3 should layer explicit cell and tissue activation policy on top of that approved kernel behavior | `COMPONENT_CATALOG.md` `CC-006`, `CC-007`, `CC-039`, `CC-047`, `CC-048`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-003` |
| trust bands | `SRC-001` trust ancestry, `trust_risk` signal, policy-envelope cues; `SRC-002` fail-closed policy discipline | `rebuild_clean` | no direct frozen trust-band component exists in the provenance package, so AGIFCore must define a clean trust-band surface while staying bounded to inherited trust ancestry, policy envelope, and fail-closed governance substrate | no direct trust-band row exists; controlled rebuild is justified by that gap plus adjacent anchors `CC-003`, `CC-039`, `CC-063` and `SIM-027` |
| split and merge rules | `SRC-001` lifecycle control plus frozen split/merge rules and lineage rules; approved Phase 2 `lifecycle_engine.py` | `port_with_provenance` | split and merge are already strongly frozen in v1 and partially realized in the approved Phase 2 lifecycle engine; Phase 3 should port the structural rules and govern them through explicit policies rather than inventing a new model | `COMPONENT_CATALOG.md` `CC-039`, `CC-054`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-003`, `SIM-018` |
| active and dormant control | `SRC-001` dormant/active lifecycle semantics and Phase 2 lifecycle plus scheduler substrate | `port_with_provenance` | active and dormant control already exists conceptually and operationally in the approved kernel; Phase 3 should formalize the structural rules, not redefine the state machine | `COMPONENT_CATALOG.md` `CC-007`, `CC-039`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-003` |
| profile budget rules | `SRC-001` scheduler/resource substrate plus frozen deployment profiles and Phase 2 budget envelope | `rebuild_clean` | the supporting budget substrate exists, but the Phase 3 cross-profile structural policy is not a direct inherited module; AGIFCore should define clean profile-budget rules that bind cells and tissues to laptop, mobile, and builder profiles | controlled rebuild justified by adjacent anchors `CC-007`, `CC-047`, `CC-048` plus `DEPLOYMENT_PROFILES.md` and the approved Phase 2 budget envelope |
| bundle schema validation | `SRC-002 agif-tasklet-cell` schema contracts, manifest validation, and bundle loading discipline | `port_with_provenance` | tasklet carries the strongest validated schema and manifest discipline; Phase 3 should port those rules into AGIFCore’s cell and bundle structure without copying the old runtime wholesale | `COMPONENT_CATALOG.md` `CC-063`, `CC-073`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-027`, `SIM-037` |
| bundle integrity checks | `SRC-002 agif-tasklet-cell` bundle integrity checks and fail-closed validation cases | `port_with_provenance` | integrity checking is directly named in the provenance pack and should port with re-verification instead of a greenfield rebuild | `COMPONENT_CATALOG.md` `CC-064`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-028` |

## 7. Artifact ownership matrix

### Artifact ownership matrix

| Artifact path | Primary author | Reviewer | Auditor | Validator | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2 plan and execution surfaces, requirements, design pack, admin controls | all later Phase 3 work | section-complete Phase 3 plan |
| `00_admin/codex_threads/tasks/phase_03/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, this plan | all later valid Phase 3 work | one task card per active role with disjoint scope |
| `04_execution/phase_03_cells_tissues_structure_and_bundles/` | `Kernel Pod Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 3 plan, Phase 1 provenance package, approved Phase 2 kernel, trace contract, bundle design surfaces | Phase 3 runtime delivery | later runtime files exist and match scoped targets |
| `05_testing/phase_03_cells_tissues_structure_and_bundles/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 3 plan, execution family, validation protocol | Phase 3 verification and closeout | later verifier family exists and runs |
| `06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifiers, trace-linked exports, structural reports | audit, governor verification, validation, user demos | later machine-readable evidence bundle is inspectable |
| `06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, validation protocol | user review | later demo bundle exists for tissue orchestration, split and merge, and bundle validation |
| `00_admin/codex_threads/handoffs/PHASE_03_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, verifiers, demos, evidence | validation request | direct verification record exists |
| `00_admin/codex_threads/handoffs/PHASE_03_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited plan or later audited execution package | user review | exact review surfaces and verdicts are explicit |
| `00_admin/codex_threads/handoffs/PHASE_03_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

### Future family note

- naming future `04_execution/`, `05_testing/`, and `06_outputs/` families in this plan does not create them
- directory or scaffold creation for those families is deferred to the first Phase 3 execution run
- this planning run only freezes names, ownership, and expectations

### First-pass planned future runtime files

Planned execution root:

- `04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/`

Planned first-pass files:

- `cell_contracts.py`
- `tissue_manifests.py`
- `activation_policies.py`
- `trust_bands.py`
- `split_merge_rules.py`
- `active_dormant_control.py`
- `profile_budget_rules.py`
- `bundle_manifest.py`
- `bundle_schema_validation.py`
- `bundle_integrity_checks.py`
- `schemas/phase_03_cell_contract.schema.json`
- `schemas/phase_03_tissue_manifest.schema.json`
- `schemas/phase_03_bundle_manifest.schema.json`

### First-pass planned future testing files

Planned testing root:

- `05_testing/phase_03_cells_tissues_structure_and_bundles/`

Planned first-pass files:

- `verify_phase_03_cell_contracts.py`
- `verify_phase_03_tissue_orchestration.py`
- `verify_phase_03_activation_and_trust.py`
- `verify_phase_03_split_merge.py`
- `verify_phase_03_profile_budgets.py`
- `verify_phase_03_bundle_validation.py`
- `verify_phase_03_bundle_integrity.py`

### First-pass planned future outputs and evidence files

Planned outputs root:

- `06_outputs/phase_03_cells_tissues_structure_and_bundles/`

Planned first-pass files:

- `phase_03_evidence_manifest.json`
- `phase_03_cell_contracts_report.json`
- `phase_03_tissue_orchestration_report.json`
- `phase_03_activation_and_trust_report.json`
- `phase_03_split_merge_report.json`
- `phase_03_profile_budget_report.json`
- `phase_03_bundle_validation_report.json`
- `phase_03_bundle_integrity_report.json`
- `phase_03_demo_index.md`
- `phase_03_tissue_orchestration_demo.md`
- `phase_03_split_merge_demo.md`
- `phase_03_bundle_validation_demo.md`

## 8. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| phase control and prerequisite reconciliation | freeze scope, active roles, task-card map, and closure chain | `Program Governor` | `Constitution Keeper` | main Phase 3 plan and task-card map | Phase 2 approved in live phase-truth files | active and inactive roles are fixed and Phase 3 stays inside scope |
| cell contract and boundary framing | define the contract surface that every Phase 3 cell must obey without conflicting with the approved Phase 2 kernel | `Architecture & Contract Lead` | `Source Cartographer`, `Program Governor` | cell-contract plan and schema targets | approved Phase 2 registry, lifecycle, event, and workspace surfaces reviewed | contract fields, kernel dependencies, and structural boundaries are explicit |
| tissue manifest and coordination planning | define tissue manifest shape, membership rules, routing boundaries, and orchestration surfaces | `Architecture & Contract Lead` | `Source Cartographer`, `Constitution Keeper` | tissue-manifest plan and orchestration targets | cell-contract framing started and tissue design surfaces reviewed | tissue responsibilities, membership rules, and routing boundaries are explicit |
| activation, trust-band, and active/dormant-control planning | define activation rules, trust-band meaning, dormant and active policies, and enforcement points | `Architecture & Contract Lead` | `Program Governor`, `Constitution Keeper`, `Test & Replay Lead` | activation, trust, and active/dormant policy plan | Phase 2 lifecycle and scheduler constraints reviewed | trust is enforceable, not decorative, and active/dormant control stays profile-aware |
| split/merge and structural-governance planning | define proposals, approvals, lineage preservation, and conflict-aware consolidation rules | `Architecture & Contract Lead` | `Source Cartographer`, `Test & Replay Lead` | split/merge rule plan and lineage expectations | activation and tissue boundaries stable | structural changes are explicit, replayable, reversible, and policy-bounded |
| bundle schema and integrity planning | define bundle manifest schema, validation path, integrity checks, and fail-closed refusal rules | `Architecture & Contract Lead` | `Source Cartographer`, `Test & Replay Lead` | bundle schema and integrity plan | bundle and sandbox design surfaces reviewed | schema validation and integrity checks are explicit and testable |
| test, demo, validation, and evidence planning | define verifiers, reports, demo bundle, and review path | `Test & Replay Lead` | `Release & Evidence Lead`, `Program Governor`, `Validation Agent`, `Anti-Shortcut Auditor` | verifier family plan, evidence plan, demo plan, validation surface | structural boundaries stable | later review path is inspectable and machine-readable |

## 9. Ordered execution sequence

1. `Program Governor` verifies Phase 2 approval truth and opens the Phase 3 task-card set.
2. `Source Cartographer` maps each Phase 3 subsystem to source basis and disposition.
3. `Architecture & Contract Lead` drafts cell, tissue, split/merge, trust-band, and bundle boundaries in parallel with step 2.
4. `Constitution Keeper` reviews steps 2 and 3 for constitution drift, hidden-autonomy wording, and Phase 4 or 5 leakage.
5. If a Phase 2 kernel seam is still unclear after step 4, `Kernel Pod Lead` is activated only for narrow consultation.
6. If a bundle/runtime-shell seam is still unclear after step 4, `Product & Sandbox Pod Lead` is activated only for narrow consultation.
7. `Program Governor` consolidates the core Phase 3 plan, future artifact families, and closure map after steps 2 through 6 stabilize.
8. `Test & Replay Lead` and `Release & Evidence Lead` define verifiers, evidence, and demos after the structural boundaries are stable.
9. `Anti-Shortcut Auditor` audits the full Phase 3 plan package.
10. `Program Governor` independently verifies the audited planning package.
11. `Validation Agent` prepares the later user review request.
12. User review happens only after the validated planning package exists.

Safe parallelism:

- `Source Cartographer` and `Architecture & Contract Lead` may work in parallel
- `Constitution Keeper` may begin once first-pass outputs exist
- `Test & Replay Lead` and `Release & Evidence Lead` wait for stable structural boundaries
- `Kernel Pod Lead` and `Product & Sandbox Pod Lead` remain inactive unless a narrow seam genuinely blocks planning
- one active build pod is the default in later Phase 3 execution, and that build pod is `Kernel Pod Lead`
- `Merge Arbiter` stays inactive in planning-only work

## 10. Detailed task cards

User is active approval-only and does not receive a task card.

### `P3-TC-PG-01`

- Role owner: `Program Governor`
- Model tier: `gpt-5.4`
- Objective: own the Phase 3 plan, prerequisite truth, task-card map, artifact matrix, and closure chain
- Exact files allowed to touch:
  - `01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `00_admin/codex_threads/tasks/phase_03/P3-TC-PG-01_PHASE_3_GOVERNOR_CONTROL.md`
- Files forbidden to touch:
  - `01_plan/MASTER_PLAN.md`
  - all `04_execution/*`
  - all Phase 4+ artifacts
  - earlier phase-truth files except to report a prerequisite mismatch if one is found
- Required reads first:
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 plan, runtime, verifier, and evidence surfaces
  - requirements, design pack, and admin controls
- Step-by-step work method:
  1. verify Phase 2 approval in live phase-truth files
  2. define active and inactive roles for Phase 3 planning
  3. define reuse strategy, workstreams, future artifact families, and closure chain
  4. reconcile all role outputs into one plan
- Required cross-checks:
  - no Phase 4 or 5 scope drift
  - no fifth disposition category
  - no implementation claims
- Exit criteria:
  - the Phase 3 plan is section-complete and decision-complete
- Handoff target: `Anti-Shortcut Auditor`
- Anti-drift rule: do not let planning language imply runtime implementation or approval
- Explicit proof that no approval is implied: the task ends at plan readiness only; Phase 3 remains `open`

### `P3-TC-CK-01`

- Role owner: `Constitution Keeper`
- Model tier: `gpt-5.4 mini`
- Objective: guard constitution, non-negotiables, trust-band honesty, and phase boundaries
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_03/P3-TC-CK-01_PHASE_3_CONSTITUTION_GUARD.md`
- Files forbidden to touch:
  - all `04_execution/*`
  - all `05_testing/*`
  - all `06_outputs/*`
  - all Phase 4+ artifacts
- Required reads first:
  - `01_plan/SYSTEM_CONSTITUTION.md`
  - `01_plan/TRACE_CONTRACT.md`
  - `02_requirements/NON_NEGOTIABLES.md`
  - `02_requirements/PHASE_APPROVAL_RULES.md`
  - `03_design/CELL_FAMILIES.md`
  - `03_design/GOVERNANCE_MODEL.md`
  - the Phase 3 plan draft
- Step-by-step work method:
  1. check that Phase 3 stays structural and not cognitive in a Phase 4 or 5 sense
  2. check that trust bands do not become vague labels
  3. check that bundle validation and integrity stay fail-closed
  4. report any drift to `Program Governor`
- Required cross-checks:
  - no hidden-autonomy language
  - no long-term memory or graph logic in Phase 3
  - no approval language
- Exit criteria:
  - all constitutional objections are resolved or explicitly blocked
- Handoff target: `Program Governor`
- Anti-drift rule: do not author architecture or implementation
- Explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P3-TC-SC-01`

- Role owner: `Source Cartographer`
- Model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- Objective: map each Phase 3 subsystem to source basis, disposition, and provenance expectations
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_03/P3-TC-SC-01_PHASE_3_PROVENANCE_AND_REUSE.md`
- Files forbidden to touch:
  - all `04_execution/*`
  - all `05_testing/*`
  - all `06_outputs/*`
  - all Phase 4+ artifacts
- Required reads first:
  - `01_plan/COMPONENT_CATALOG.md`
  - `01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 2 plan and structural kernel surfaces
  - historical source roots when needed
- Step-by-step work method:
  1. map each Phase 3 subsystem to the strongest source basis
  2. select only one frozen disposition per subsystem
  3. note when the carry decision is substrate-level rather than a literal module carry
  4. flag any direct provenance gap
- Required cross-checks:
  - no silent omission of a subsystem
  - no fifth disposition category
  - no v2 runtime treated as already-portable truth
- Exit criteria:
  - every required Phase 3 subsystem has explicit provenance and rationale
- Handoff target: `Architecture & Contract Lead` then `Program Governor`
- Anti-drift rule: do not claim mapped historical code is already valid AGIFCore runtime
- Explicit proof that no approval is implied: provenance mapping does not earn the phase

### `P3-TC-ACL-01`

- Role owner: `Architecture & Contract Lead`
- Model tier: `gpt-5.4`
- Objective: freeze the cell, tissue, structural, and bundle boundary layer above the approved Phase 2 kernel
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_03/P3-TC-ACL-01_PHASE_3_CELL_TISSUE_BUNDLE_ARCHITECTURE.md`
- Files forbidden to touch:
  - all `04_execution/*`
  - all Phase 4+ artifacts
  - earlier canonical design files as edits
- Required reads first:
  - `01_plan/TRACE_CONTRACT.md`
  - `01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - approved Phase 2 runtime files for registry, lifecycle, scheduler, workspace, and event bus
  - `03_design/CELL_FAMILIES.md`
  - `03_design/BUNDLE_INTEGRITY_MODEL.md`
  - `03_design/GOVERNANCE_MODEL.md`
  - `03_design/PRODUCT_RUNTIME_MODEL.md`
  - provenance outputs from `SC`
- Step-by-step work method:
  1. define `CellContract` and `TissueManifest` boundaries
  2. define activation, trust-band, and active/dormant-control boundaries
  3. define split/merge proposal, approval, and lineage boundaries
  4. define `BundleManifest`, bundle schema-validation, and integrity boundaries
  5. align all boundaries to the approved Phase 2 kernel and trace surfaces
- Required cross-checks:
  - no second lifecycle state machine
  - no Phase 4 memory or Phase 5 graph implementation
  - no product-runtime or sandbox overreach
- Exit criteria:
  - every Phase 3 subsystem has an explicit boundary and later proof path
- Handoff target: `Program Governor` then `Test & Replay Lead`
- Anti-drift rule: do not redesign the kernel or product runtime
- Explicit proof that no approval is implied: architecture framing is planning truth only

### `P3-TC-TRL-01`

- Role owner: `Test & Replay Lead`
- Model tier: `gpt-5.4 mini`
- Objective: define the Phase 3 verifier family, structure checks, bundle-validation checks, and evidence outputs
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_03/P3-TC-TRL-01_PHASE_3_TEST_AND_STRUCTURE_VALIDATION_PLAN.md`
- Files forbidden to touch:
  - all `04_execution/*`
  - all earlier canonical content
  - all Phase 4+ artifacts
- Required reads first:
  - `01_plan/VALIDATION_PROTOCOL.md`
  - `01_plan/DEMO_PROTOCOL.md`
  - `01_plan/TRACE_CONTRACT.md`
  - approved Phase 2 verifier and evidence surfaces
  - the Phase 3 plan draft
- Step-by-step work method:
  1. define the `verify_phase_03_*` family
  2. define cell-contract, tissue-orchestration, activation/trust, split/merge, profile-budget, schema-validation, and integrity checks
  3. define negative fail-closed cases for invalid bundles and invalid structure
  4. define machine-readable evidence outputs
- Required cross-checks:
  - every required Phase 3 subsystem has a planned verifier
  - bundle validation and integrity are not prose-only promises
  - demos point to real evidence files
- Exit criteria:
  - later test and evidence paths are exact enough to implement without new decisions
- Handoff target: `Release & Evidence Lead` then `Program Governor`
- Anti-drift rule: do not implement runtime behavior through test planning
- Explicit proof that no approval is implied: verification planning does not earn the phase

### `P3-TC-ASA-01`

- Role owner: `Anti-Shortcut Auditor`
- Model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- Objective: audit the Phase 3 plan package for drift, omission, and fake completeness
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_03/P3-TC-ASA-01_PHASE_3_PLAN_AUDIT.md`
  - `00_admin/codex_threads/tasks/phase_03/P3-AUDIT-01_PHASE_3_PLAN_AUDIT_REPORT.md`
- Files forbidden to touch:
  - canonical plan content
  - all `04_execution/*`
  - all Phase 4+ artifacts
- Required reads first:
  - the complete Phase 3 planning package
  - the Phase 1 provenance package
  - the approved Phase 2 plan and execution baseline
  - validation protocol
- Step-by-step work method:
  1. check every required subsystem is represented
  2. check carry decisions against the provenance package
  3. check that Phase 2 kernel constraints are preserved
  4. check that trust bands and bundle validation are enforceable, not narrative-only
  5. write explicit blockers or pass results
- Required cross-checks:
  - no greenfield recreation where v1 or tasklet substrate exists
  - no v2 runtime treated as default truth
  - no Phase 4 or 5 scope leakage
- Exit criteria:
  - audit report explicitly states pass or blockers with file-backed reasons
- Handoff target: `Program Governor`
- Anti-drift rule: do not rewrite the plan instead of auditing it
- Explicit proof that no approval is implied: audit pass is not phase approval

### `P3-TC-VA-01`

- Role owner: `Validation Agent`
- Model tier: `gpt-5.4`
- Objective: validate the Phase 3 planning package and prepare the user review request
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_03/P3-TC-VA-01_PHASE_3_VALIDATION_REQUEST.md`
  - later `00_admin/codex_threads/handoffs/PHASE_03_VALIDATION_REQUEST.md`
- Files forbidden to touch:
  - canonical plan content
  - any runtime code or test code
  - any user verdict file
- Required reads first:
  - audited Phase 3 plan package
  - governor verification record when it exists
  - validation protocol
- Step-by-step work method:
  1. read the audited Phase 3 plan package
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
- Explicit proof that no approval is implied: validation asks for review; it does not mark the phase earned

### `P3-TC-REL-01`

- Role owner: `Release & Evidence Lead`
- Model tier: `gpt-5.4 mini`
- Objective: define the later user-facing Phase 3 demo and evidence bundle
- Exact files allowed to touch:
  - `00_admin/codex_threads/tasks/phase_03/P3-TC-REL-01_PHASE_3_DEMO_AND_EVIDENCE_PLAN.md`
- Files forbidden to touch:
  - all `04_execution/*`
  - all public release artifacts
  - all Phase 4+ artifacts
- Required reads first:
  - `01_plan/DEMO_PROTOCOL.md`
  - `01_plan/VALIDATION_PROTOCOL.md`
  - the Phase 3 plan draft
  - `TRL` outputs when available
- Step-by-step work method:
  1. define the demo bundle shape for tissue orchestration, split and merge, and bundle validation
  2. define which evidence is machine-readable and which is human-facing
  3. define the later review packet order
- Required cross-checks:
  - no release or publication drift
  - no missing demo surface
  - no evidence summary without real underlying files
- Exit criteria:
  - later user review packet is exact and inspectable
- Handoff target: `Program Governor` then `Validation Agent`
- Anti-drift rule: do not expand into later release work
- Explicit proof that no approval is implied: demo-package planning is not demo acceptance

## 11. Closure-gate mapping

| Phase 3 closure requirement | Artifact(s) that must satisfy it later | Responsible role | How it will be checked | What failure looks like |
| --- | --- | --- | --- | --- |
| cell contracts exist | `cell_contracts.py`, `schemas/phase_03_cell_contract.schema.json`, `verify_phase_03_cell_contracts.py` | `Kernel Pod Lead` | contract fields, identity linkage, allowed tissues, split/merge policy refs, and policy envelope are explicit and test-backed | ad hoc cell metadata or no schema-backed contract surface |
| tissue manifests exist | `tissue_manifests.py`, `schemas/phase_03_tissue_manifest.schema.json`, `verify_phase_03_tissue_orchestration.py` | `Kernel Pod Lead` | membership rules, routing boundaries, and tissue manifest exports exist and are inspectable | tissues exist only in prose or cannot be validated |
| activation policies exist | `activation_policies.py`, `verify_phase_03_activation_and_trust.py` | `Kernel Pod Lead` | activation triggers, approvals, and entry guards align to Phase 2 lifecycle and scheduler constraints | activation is vague or bypasses the kernel substrate |
| trust bands exist | `trust_bands.py`, `verify_phase_03_activation_and_trust.py` | `Kernel Pod Lead` | trust bands affect activation, split/merge, quarantine, or bundle admission behavior in an inspectable way | trust bands are labels only with no enforcement meaning |
| split and merge rules exist | `split_merge_rules.py`, `verify_phase_03_split_merge.py` | `Kernel Pod Lead` | proposals, approvals, lineage preservation, and conflict-aware consolidation are explicit and replayable | split or merge behavior is incomplete, unsafe, or untestable |
| active and dormant control exists | `active_dormant_control.py`, `verify_phase_03_activation_and_trust.py`, `verify_phase_03_profile_budgets.py` | `Kernel Pod Lead` | active vs dormant constraints bind to lifecycle and profile budgets | dormant and active behavior is detached from real budget rules |
| profile budget rules exist | `profile_budget_rules.py`, `verify_phase_03_profile_budgets.py` | `Test & Replay Lead` | laptop, mobile, and builder structural limits are explicit and validated | profiles are named but have no enforced structural meaning |
| bundle schema validation exists | `bundle_manifest.py`, `bundle_schema_validation.py`, `schemas/phase_03_bundle_manifest.schema.json`, `verify_phase_03_bundle_validation.py` | `Test & Replay Lead` | invalid manifests and missing required fields fail closed before load | bundle schema checking is descriptive only |
| bundle integrity checks exist | `bundle_integrity_checks.py`, `verify_phase_03_bundle_integrity.py` | `Test & Replay Lead` | missing files, hash mismatches, or invalid inventories fail closed with inspectable evidence | integrity is reduced to file presence or logging only |
| demo path exists | `06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/` | `Release & Evidence Lead` | all three required demos exist and point to real evidence | missing or narrative-only demo surfaces |
| tests and evidence path exists | `05_testing/phase_03_cells_tissues_structure_and_bundles/` and `06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/` | `Test & Replay Lead` | verifier family runs and outputs are machine-readable | no verifier family, no evidence manifest, or no inspectable reports |

## 12. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| tissue orchestration demo | valid cell contracts, at least one valid tissue manifest, orchestration verifier output, and structural evidence manifest | `Release & Evidence Lead` with `Test & Replay Lead` support | `Anti-Shortcut Auditor` | which cells belong to which tissue, why they are allowed there, and how orchestration respects Phase 2 kernel constraints |
| split and merge demo | split proposal, merge proposal, lineage-preservation evidence, conflict-aware consolidation evidence, and `verify_phase_03_split_merge.py` output | `Test & Replay Lead` with `Architecture & Contract Lead` support | `Anti-Shortcut Auditor` | approvals, lineage continuity, trust-band effect, rollback references, and the final structural outcome |
| bundle validation demo | bundle manifest schema, invalid-bundle negative cases, integrity-check evidence, and both bundle verifiers | `Test & Replay Lead` with `Release & Evidence Lead` support | `Anti-Shortcut Auditor` | fail-closed refusal for invalid schema or invalid integrity and a valid path for a correct bundle |

Validation package rules:

- later validation must point the user to the three demos above plus the audited evidence bundle
- later review must include audit, governor verification, demo bundle, validation request, and user verdict path
- demos do not imply approval; only explicit user `approved` earns the phase

## 13. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable substrate | compare subsystem plan against `COMPONENT_CATALOG.md`, `SOURCE_INHERITANCE_MATRIX.md`, and `RUNTIME_REBUILD_MAP.md` | `Source Cartographer` | a core subsystem is planned greenfield without provenance justification | reopen provenance mapping and block execution start |
| cell contracts drift away from Phase 2 kernel assumptions | compare planned contract fields and lifecycle hooks against approved Phase 2 `cell_registry.py`, `lifecycle_engine.py`, and `event_types.py` | `Architecture & Contract Lead` | a contract field conflicts with the approved kernel substrate | reopen boundary framing before execution |
| tissue manifests absorb Phase 4 or 5 logic | compare tissue-manifest responsibilities against `MEMORY_MODEL.md`, `GRAPH_STACK_MODEL.md`, and `CELL_FAMILIES.md` | `Constitution Keeper` | manifests begin carrying memory-plane or graph-policy logic | reject the drift and keep the plan structural only |
| split and merge rules become underspecified | compare planned rules against v1 lineage and lifecycle rules plus approved Phase 2 lifecycle surfaces | `Architecture & Contract Lead` | approvals, lineage, or conflict-aware consolidation are left implicit | reopen structural-governance planning |
| trust bands become labels with no enforcement meaning | inspect whether trust bands affect activation, split/merge, quarantine, or bundle admission paths | `Constitution Keeper` | trust bands appear only in naming or documentation | block execution start until enforcement points are explicit |
| active and dormant control ignores laptop, mobile, or builder profiles | compare planned controls against `DEPLOYMENT_PROFILES.md`, `CELL_FAMILIES.md`, and the approved Phase 2 scheduler budget envelope | `Program Governor` | profile names exist without structural budget consequences | reopen profile-budget planning |
| bundle validation is described but not testable | check whether schema-invalid, manifest-invalid, and integrity-invalid negative cases exist in the verifier plan | `Test & Replay Lead` | validation exists only as prose or happy-path checks | block validation readiness and reopen verification planning |
| Phase 3 accidentally absorbs memory or graph implementation | compare planned outputs against the Phase 4 and Phase 5 titles and scopes | `Program Governor` | memory tiers, graph persistence, or graph policy surfaces appear in Phase 3 deliverables | reject the drift and keep Phase 4 and 5 untouched |
| v2 tissue vocabulary is treated as default runtime truth | compare any v2 carry claim against Phase 1 provenance dispositions | `Anti-Shortcut Auditor` | `SRC-003` or `SRC-004` tissue/runtime content is treated as direct AGIFCore carry | freeze the plan for rework and escalate to `Program Governor` |
| bundle integrity is conflated with sandbox | compare the bundle plan against `BUNDLE_INTEGRITY_MODEL.md` and `SANDBOX_MODEL.md` | `Architecture & Contract Lead` | sandbox is used as a substitute for integrity checks | reopen bundle-boundary planning |

## 14. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says `approved` in a later separate run may the Phase 3 plan artifacts be committed and frozen
- Phase 3 remains `open` until later execution, verifiers, demos, audit, governor verification, validation request, and explicit user approval all exist
- after user approval, any future change to the Phase 3 plan requires explicit reopen instruction and a supersession note naming the replaced artifact

## 15. Final readiness judgment

`ready_for_user_review`

Phase 2 approval is explicit in the live phase-truth files, the Phase 1 provenance and design package are present, the approved Phase 2 kernel and workspace baseline is available on disk, the port-versus-rebuild defaults for all required Phase 3 subsystems are explicit, and the remaining gaps are expected Phase 3 outputs rather than prerequisite blockers. The only noteworthy dependency gap is that trust bands do not have a direct frozen inherited module, which is already handled in this plan as a controlled `rebuild_clean` decision rather than a blocker.
