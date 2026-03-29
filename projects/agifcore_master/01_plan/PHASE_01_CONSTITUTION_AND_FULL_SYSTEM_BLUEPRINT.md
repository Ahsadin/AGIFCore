# Phase 1: Constitution and Full-System Blueprint

## 1. Phase identity

- Phase number: `1`
- Canonical phase name: `Constitution and Full-System Blueprint`
- Status: `planning_draft`
- Intended canonical artifact path: `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
- Source-of-truth references reviewed:
  - `/Users/ahsadin/Documents/AGIFCore/AGENTS.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/AGENTS.override.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/PROJECT_README.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/DECISIONS.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/CHANGELOG.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `/Users/ahsadin/Documents/AGIFCore/projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`

## 2. Phase mission

- Phase 1 exists to turn the frozen master plan into a decision-complete governance and blueprint layer for all later phases.
- Phase 1 must freeze:
  - the AGIFCore constitution and human-thinking target
  - the full requirement pack
  - the full design pack
  - the component catalog
  - the source inheritance matrix
  - the runtime rebuild map
  - the proof-domain matrix
  - the trace contract
  - the phase index and phase gate checklist
- Phase 1 must not:
  - implement runtime code
  - draft later-phase execution code
  - claim requirement-pack or design-pack completion from placeholders
  - activate later execution pods casually
  - approve itself
  - move to Phase 2

## 3. Scope and non-goals

### In scope

- Authoring the main Phase 1 execution-plan artifact.
- Planning the controlled authoring of all required `01_plan`, `02_requirements`, and `03_design` artifacts named in the master plan.
- Defining role ownership, review flow, audit flow, validation flow, and user-approval flow for those artifacts.
- Defining the exact work order, allowed parallelism, and handoffs for later Phase 1 execution.

### Out of scope

- Any `04_execution/` runtime code.
- Any `05_testing/verify_*.py` implementation work.
- Any later-phase pod implementation.
- Any commit, freeze, merge, tag, or approval action.
- Any final publication or release execution.

### Later-phase work that must remain untouched

- Phase 2 fabric kernel execution
- Phase 3 cell/tissue execution
- Phase 4-16 runtime behavior execution
- Any Meta & Growth activation
- Any Product & Sandbox implementation work beyond Phase 1 blueprint planning

## 4. Phase 0 prerequisite check

### Prerequisites already satisfied from files

- Canonical repo and project scaffolds exist.
- Root and project truth files exist.
- Frozen master plan exists.
- Frozen build-machine rule stack exists.
- Admin enforcement templates exist.
- Placeholder targets exist for all required `01_plan`, `02_requirements`, and `03_design` Phase 1 artifacts.
- Root README and decisions already mark AGIF v2 as historical source material.

### Unresolved prerequisites

- No distinct project-level archival note file was found that explicitly closes AGIF v2 as a failed historical attempt inside the project workspace.
- No distinct source-freeze inventory or source-freeze method artifact was found inside the project workspace.
- `PHASE_GATE_CHECKLIST.md` still shows Phase 0 as `open`.

### Blockers

- Phase 1 execution should not be treated as closure-ready until the missing Phase 0 archival note and source-freeze method are explicitly resolved or explicitly waived by the user.
- Phase 0 open status is a governance blocker for later Phase 1 closure, even though it does not block planning this draft.

### Non-blockers

- Existing placeholder files in `01_plan`, `02_requirements`, and `03_design` are acceptable starting targets for later Phase 1 authoring.
- The Phase 1 plan file now exists as the canonical frozen planning baseline for the later execution run.

## 5. Active team map for Phase 1

| Role | Model tier | Status | Why | Exact responsibility this phase | Must never do this phase |
| --- | --- | --- | --- | --- | --- |
| User | none | active | final human approver | review demos later; approve or reject | delegate final approval |
| Program Governor | `gpt-5.4` | active | top planning authority | own Phase 1 plan, sequencing, blockers, phase index, proof-domain matrix, gate alignment, final cross-artifact truth check | self-approve, implement runtime code, treat placeholders as done |
| Constitution Keeper | `gpt-5.4 mini` | active | requirement-discipline owner | author constitution and requirement-pack planning lane; guard non-negotiables and anti-drift boundaries | author design-pack or inheritance-mapping artifacts, approve phase |
| Source Cartographer | `gpt-5.4 mini` | active | Phase 1 requires full lineage mapping | author component catalog, source inheritance matrix, runtime rebuild map | author requirement/design pack content, approve phase, stay active beyond mapped need |
| Architecture & Contract Lead | `gpt-5.4` | active | Phase 1 must freeze architecture framing | author trace contract and full design-pack planning lane; freeze runner/gateway/UI and operator-boundary logic | author inheritance matrix or approve phase |
| Kernel Pod Lead | `gpt-5.3-codex` | inactive | no Phase 1 runtime execution | none unless Governor explicitly reopens for narrow planning consultation | author or implement Phase 2 work |
| Memory & Graph Pod Lead | `gpt-5.3-codex` | inactive | no Phase 1 runtime execution | none unless Governor explicitly reopens for narrow planning consultation | author or implement Phase 4-5 work |
| World & Conversation Pod Lead | `gpt-5.3-codex` | inactive | architecture framing handled by ACL this phase | none unless Governor explicitly reopens for narrow planning consultation | author or implement Phase 6-9 work |
| Meta & Growth Pod Lead | `gpt-5.3-codex` | inactive | danger zone; not needed for Phase 1 planning | none | activate casually, author Phase 10-12 work |
| Product & Sandbox Pod Lead | `gpt-5.3-codex` | inactive | Phase 1 sandbox/product framing stays with ACL | none unless Governor explicitly reopens for narrow planning consultation | become a late-phase dumping lane |
| Test & Replay Lead | `gpt-5.4 mini` | active | closure rules need verification planning | author validation-protocol planning lane and verification expectations for later Phase 1 execution | author requirement/design content, approve phase |
| Anti-Shortcut Auditor | `gpt-5.4 mini` | active | Phase 1 high risk is fake completeness | audit artifact coverage, placeholder drift, unsupported claims, omitted source pools | author canonical content, downgrade blockers |
| Merge Arbiter | `gpt-5.3-codex` | active | parallel authoring lanes later need controlled integration | own merge-only integration lane for later Phase 1 execution | author content, approve its own integration |
| Validation Agent | `gpt-5.4` | active | final machine-side plan completeness review is required | validate Phase 1 artifact set for user review readiness | author canonical content, write user verdict |
| Release & Evidence Lead | `gpt-5.4 mini` | active | Phase 1 demos and evidence must be planned | author demo-protocol planning lane and Phase 1 evidence/demo packaging expectations | expand into release execution or public claims |

## 6. Artifact ownership matrix

Role legend:
- `PG` Program Governor
- `CK` Constitution Keeper
- `SC` Source Cartographer
- `ACL` Architecture & Contract Lead
- `TRL` Test & Replay Lead
- `ASA` Anti-Shortcut Auditor
- `MA` Merge Arbiter
- `VA` Validation Agent
- `REL` Release & Evidence Lead

Input legend:
- `MP` master plan
- `PT` project truth files
- `RR` frozen role/rule stack
- `ADM` admin control files
- `SRC` v1/tasklet/v2 lineage sources
- `PF` current placeholder file state
- `GATE` Phase 1 closure gates

### Planning artifacts

| Artifact | Primary | Review | Audit | Validate | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md` | PG | CK | ASA | VA | MP+PT+RR+ADM+PF | all later Phase 1 execution | section-complete draft with explicit role/task/gate mapping |
| `01_plan/PHASE_INDEX.md` | PG | CK | ASA | VA | MP+PF | all later phase plans | substantive phase ladder with dependency notes |
| `01_plan/PHASE_GATE_CHECKLIST.md` | PG | CK | ASA | VA | MP+GATE+PF | Phase 1 closure review | gate list aligned to master plan, no placeholder-only rows |
| `01_plan/COMPONENT_CATALOG.md` | SC | ACL | ASA | VA | MP+SRC+PF | all execution phases | exact-name coverage seeded, missing rows flagged |
| `01_plan/SOURCE_INHERITANCE_MATRIX.md` | SC | PG | ASA | VA | MP+SRC+PF | all inheritance/port decisions | row-by-row source pool coverage with dispositions |
| `01_plan/RUNTIME_REBUILD_MAP.md` | SC | ACL | ASA | VA | MP+SRC+PF | Phase 2-16 planning | exact runtime module mapping and destination logic |
| `01_plan/TRACE_CONTRACT.md` | ACL | PG | ASA | VA | MP+RR+PF | conversation/runtime later phases | explicit turn/trace framing, no bypass ambiguity |
| `01_plan/PROOF_DOMAIN_MATRIX.md` | PG | CK | ASA | VA | MP+GATE+PF | proof-domain demos and Phase 6+ work | all 8 proof domains explicit and frozen |
| `01_plan/VALIDATION_PROTOCOL.md` | TRL | PG | ASA | VA | MP+RR+ADM+PF | all phase closures | closure records, audit/validation flow, no self-approval |
| `01_plan/DEMO_PROTOCOL.md` | REL | PG | ASA | VA | MP+RR+ADM+PF | user demos for Phase 1 and later | demo pack rules and inspectable outputs defined |
| `01_plan/HUMAN_THINKING_TARGET.md` | CK | PG | ASA | VA | MP+PF | requirement/design pack alignment | explicit functional-thinking target, no style-only claims |
| `01_plan/SYSTEM_CONSTITUTION.md` | CK | PG | ASA | VA | MP+RR+PF | all later phase plans | constitution rules tied back to master plan |

### Requirement-pack artifacts

| Artifact | Primary | Review | Audit | Validate | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `02_requirements/NON_NEGOTIABLES.md` | CK | PG | ASA | VA | MP+RR+PF | all phases | non-placeholder rules aligned to constitution |
| `02_requirements/INNOVATION_RULES.md` | CK | PG | ASA | VA | MP+RR+PF | later redesign/self-improvement limits | explicit innovation boundaries |
| `02_requirements/SCIENTIFIC_METHOD.md` | CK | PG | ASA | VA | MP+PF | world/science later phases | real method/falsifier framing, no vagueness |
| `02_requirements/FALSIFICATION_THRESHOLDS.md` | CK | PG | ASA | VA | MP+PF | evaluation and critique later phases | explicit falsification triggers |
| `02_requirements/BOTTLENECK_ESCALATION_RULES.md` | CK | PG | ASA | VA | MP+ADM+PF | execution governance | concrete escalation rules, not slogans |
| `02_requirements/DEPLOYMENT_PROFILES.md` | CK | ACL | ASA | VA | MP+PF | deployment/design later phases | laptop/mobile/builder profiles explicit |
| `02_requirements/DOMAIN_MATRIX.md` | CK | PG | ASA | VA | MP+PF | proof-domain matrix and demos | domain scope aligned to 8 domains |
| `02_requirements/CONVERSATION_SCOPE.md` | CK | ACL | ASA | VA | MP+PF | trace contract and conversation model | answer-mode boundaries explicit |
| `02_requirements/NORTH_STAR_LANGUAGE_TARGET.md` | CK | ACL | ASA | VA | MP+PF | conversation model and demos | target language behavior explicit |
| `02_requirements/MACHINE_ROLE_POLICY.md` | CK | PG | ASA | VA | MP+ADM+PF | deployment/model/runtime boundaries | laptop/builder/soak roles explicit |
| `02_requirements/PHASE_APPROVAL_RULES.md` | CK | PG | ASA | VA | MP+RR+ADM+PF | closure protocol | explicit approval-only-by-user rule |

### Design-pack artifacts

| Artifact | Primary | Review | Audit | Validate | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `03_design/ARCHITECTURE_OVERVIEW.md` | ACL | PG | ASA | VA | MP+SRC+PF | all design/execution phases | architecture framing tied to master plan |
| `03_design/CELL_FAMILIES.md` | ACL | PG | ASA | VA | MP+SRC+PF | Phase 3 and later | frozen family definitions seeded from lineage |
| `03_design/COGNITIVE_PRIORS.md` | ACL | PG | ASA | VA | MP+SRC+PF | Phase 8 and later | non-placeholder priors framing |
| `03_design/FORMAL_MODELS.md` | ACL | PG | ASA | VA | MP+PF | simulator/governance later phases | formal framing linked to architecture |
| `03_design/MEMORY_MODEL.md` | ACL | PG | ASA | VA | MP+SRC+PF | Phase 4 execution | memory planes and lifecycle framing explicit |
| `03_design/SIMULATOR_MODEL.md` | ACL | PG | ASA | VA | MP+SRC+PF | Phase 6 execution | simulator boundaries and responsibilities explicit |
| `03_design/GOVERNANCE_MODEL.md` | ACL | PG | ASA | VA | MP+RR+PF | all phases | governance/control surfaces explicit |
| `03_design/CONVERSATION_MODEL.md` | ACL | PG | ASA | VA | MP+SRC+PF | Phase 7-9 execution | conversation path aligned to trace contract |
| `03_design/DEPLOYMENT_MODEL.md` | ACL | PG | ASA | VA | MP+PF | Phase 13-16 execution | deployment architecture explicit |
| `03_design/SKILL_GRAPH_MODEL.md` | ACL | PG | ASA | VA | MP+SRC+PF | Phase 5 execution | skill-graph framing explicit |
| `03_design/GRAPH_STACK_MODEL.md` | ACL | PG | ASA | VA | MP+SRC+PF | Phase 5 execution | descriptor/skill/concept/transfer stack explicit |
| `03_design/WORKSPACE_MODEL.md` | ACL | PG | ASA | VA | MP+RR+ADM+PF | operator and branch rules | operator/workspace boundaries explicit |
| `03_design/PRODUCT_RUNTIME_MODEL.md` | ACL | PG | ASA | VA | MP+RR+SRC+PF | Phase 13+ execution | runner/gateway/UI split explicit |
| `03_design/BUNDLE_INTEGRITY_MODEL.md` | ACL | PG | ASA | VA | MP+SRC+PF | sandbox/product later phases | bundle integrity rules explicit |
| `03_design/SANDBOX_MODEL.md` | ACL | PG | ASA | VA | MP+SRC+PF | Phase 14 execution | sandbox boundaries explicit |
| `03_design/PUBLIC_RELEASE_MODEL.md` | ACL | PG | ASA | VA | MP+SRC+PF | Phase 16 execution | release/publication lane explicit |

## 7. Workstream breakdown

### Workstream 1: Constitution and requirement discipline

- Objective: define the constitution-facing planning layer and the full requirement-pack authoring lane.
- Owner: `CK`
- Supporting roles: `PG`, `ASA`
- Planned outputs:
  - `01_plan/SYSTEM_CONSTITUTION.md`
  - `01_plan/HUMAN_THINKING_TARGET.md`
  - full `02_requirements/` pack
- Entry conditions:
  - Phase 0 prerequisite scan completed
  - master plan reviewed
  - current placeholders confirmed
- Exit criteria:
  - no requirement file remains a 4-line placeholder
  - every requirement file cites the master-plan rule it is freezing
  - Constitution Keeper confirms no drift beyond Phase 1 scope

### Workstream 2: Inheritance and provenance mapping

- Objective: freeze what AGIFCore inherits, rejects, or rebuilds from v1/tasklet/v2 lineage.
- Owner: `SC`
- Supporting roles: `PG`, `ASA`
- Planned outputs:
  - `01_plan/COMPONENT_CATALOG.md`
  - `01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `01_plan/RUNTIME_REBUILD_MAP.md`
- Entry conditions:
  - source pools confirmed
  - exact inherited component/module names pulled from master plan
- Exit criteria:
  - every source pool has seeded row coverage
  - exact inherited names and runtime modules are present
  - any unresolved lineage item is explicit, not silent

### Workstream 3: Architecture and contract freezing

- Objective: freeze the design-pack authoring lane and the key contract surfaces Phase 2+ depend on.
- Owner: `ACL`
- Supporting roles: `PG`, `CK`
- Planned outputs:
  - `01_plan/TRACE_CONTRACT.md`
  - full `03_design/` pack
- Entry conditions:
  - Workstream 1 and Workstream 2 produce first-pass boundaries
  - current design placeholders confirmed
- Exit criteria:
  - runner/gateway/UI split is explicit
  - operator command family is explicit
  - bundle integrity and sandbox rules are explicit
  - no design file remains placeholder-only

### Workstream 4: Proof-domain and closure-gate freezing

- Objective: freeze the 8 proof domains, phase order, and closure-gate mapping.
- Owner: `PG`
- Supporting roles: `CK`, `ACL`
- Planned outputs:
  - `01_plan/PHASE_INDEX.md`
  - `01_plan/PHASE_GATE_CHECKLIST.md`
  - `01_plan/PROOF_DOMAIN_MATRIX.md`
- Entry conditions:
  - master plan reviewed
  - Workstream 1 scope boundaries drafted
- Exit criteria:
  - all 8 proof domains are explicit
  - gate checklist maps directly to master-plan closure gates
  - no phase-order ambiguity remains

### Workstream 5: Verification, demo, and validation planning

- Objective: define how later Phase 1 execution will be audited, demoed, and reviewed.
- Owner: `TRL`
- Supporting roles: `REL`, `ASA`, `VA`
- Planned outputs:
  - `01_plan/VALIDATION_PROTOCOL.md`
  - `01_plan/DEMO_PROTOCOL.md`
- Entry conditions:
  - first-pass outputs from Workstreams 1-4 exist
  - admin enforcement templates are available
- Exit criteria:
  - required closure records are explicit
  - user-inspectable demos are explicit
  - extra danger-zone handling is explicit even though Meta & Growth stays inactive this phase

### Workstream 6: Final consolidation and review

- Objective: consolidate the whole Phase 1 artifact set into one reviewable package without silent omissions.
- Owner: `PG`
- Supporting roles: `ASA`, `MA`, `VA`, `REL`
- Planned outputs:
  - cross-artifact gap list
  - audit findings
  - validation-request draft
  - user review packet plan
- Entry conditions:
  - Workstreams 1-5 all at first-pass exit
- Exit criteria:
  - no required artifact is missing
  - all blockers are explicit
  - readiness state is explicit
  - no approval is implied

## 8. Ordered execution sequence

1. `PG` performs Phase 0 prerequisite scan and role activation check.
2. `PG` opens the Phase 1 task-card set and fixes active/inactive role list.
3. `CK` starts Workstream 1 and `SC` starts Workstream 2 in parallel.
4. `ACL` may start architecture framing immediately from the master plan and placeholders, but may not freeze final boundaries until Workstream 1 and Workstream 2 produce first-pass outputs.
5. `PG` runs Workstream 4 once Workstream 1 has first-pass scope boundaries.
6. `TRL` and `REL` start Workstream 5 only after first-pass outputs exist from Workstreams 1-4.
7. `ASA` audits all first-pass artifacts after Workstreams 1-5 complete.
8. `MA` performs merge-only consolidation after audit clearance and only if authoring ran in parallel lanes.
9. `PG` performs direct verification against files, blockers, and closure gates.
10. `VA` prepares the validation request for user review.
11. User review occurs later in a separate run; no approval is implied in this planning draft.

### Safe parallelism

- Safe in parallel:
  - `CK` requirement-discipline lane
  - `SC` provenance lane
  - `ACL` architecture-outline lane
- Must wait:
  - final `TRACE_CONTRACT.md` freeze waits for Workstream 1 and 2 first-pass outputs
  - `VALIDATION_PROTOCOL.md` and `DEMO_PROTOCOL.md` wait for Workstreams 1-4 first-pass outputs
  - `ASA`, `MA`, `VA` wait for first-pass drafting to finish
- Handoffs:
  - `CK` -> `PG`, `ASA`
  - `SC` -> `ACL`, `PG`, `ASA`
  - `ACL` -> `PG`, `ASA`
  - `TRL`/`REL` -> `PG`, `ASA`, `VA`
  - `ASA` -> `MA`, `PG`
  - `PG` -> `VA` -> User

## 9. Detailed task cards

User is active approval-only and does not receive a task card.

### P1-TC-PG-01

- Role owner: `Program Governor`
- Model tier: `gpt-5.4`
- Objective: author the Phase 1 plan, phase index, phase gate checklist, and proof-domain matrix; control sequencing and blocker truth.
- Exact files allowed to touch:
  - `01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - `01_plan/PHASE_INDEX.md`
  - `01_plan/PHASE_GATE_CHECKLIST.md`
  - `01_plan/PROOF_DOMAIN_MATRIX.md`
- Files forbidden to touch:
  - all `04_execution/` files
  - all `03_design/` files owned by `ACL`
  - all `02_requirements/` files owned by `CK`
  - all provenance files owned by `SC`
- Required reads first:
  - all source-of-truth files already listed in Section 1
- Step-by-step work method:
  1. scan current placeholder state and Phase 0 prerequisites
  2. define active/inactive role map
  3. author Phase 1 plan and gate/order artifacts
  4. cross-check every closure gate against named artifacts
  5. hand off to `ASA`
- Required cross-checks:
  - phase order matches master plan
  - all 8 proof domains present
  - no later-phase execution scope leaked in
- Exit criteria:
  - all four allowed files are substantive and cross-linked
- Handoff target: `ASA`
- Anti-drift rule:
  - do not author requirement-pack, design-pack, or provenance-pack content
- Proof that no approval is implied:
  - completion means only “ready for audit,” never “phase approved”

### P1-TC-CK-01

- Role owner: `Constitution Keeper`
- Model tier: `gpt-5.4 mini`
- Objective: author the constitution-facing plan artifacts and the full requirement-pack lane.
- Exact files allowed to touch:
  - `01_plan/SYSTEM_CONSTITUTION.md`
  - `01_plan/HUMAN_THINKING_TARGET.md`
  - `02_requirements/NON_NEGOTIABLES.md`
  - `02_requirements/INNOVATION_RULES.md`
  - `02_requirements/SCIENTIFIC_METHOD.md`
  - `02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `02_requirements/BOTTLENECK_ESCALATION_RULES.md`
  - `02_requirements/DEPLOYMENT_PROFILES.md`
  - `02_requirements/DOMAIN_MATRIX.md`
  - `02_requirements/CONVERSATION_SCOPE.md`
  - `02_requirements/NORTH_STAR_LANGUAGE_TARGET.md`
  - `02_requirements/MACHINE_ROLE_POLICY.md`
  - `02_requirements/PHASE_APPROVAL_RULES.md`
- Files forbidden to touch:
  - all `03_design/` files
  - all provenance files
  - all `04_execution/` files
- Required reads first:
  - master plan
  - role rules
  - validation protocol
  - current placeholder files in `02_requirements/`
- Step-by-step work method:
  1. map each requirement file to a master-plan clause
  2. replace placeholder-only text with freeze-level Phase 1 draft content
  3. cross-link requirement files to constitution and human-thinking target
  4. hand off to `PG` and `ASA`
- Required cross-checks:
  - no hidden-model/cloud loopholes
  - requirement files do not drift into later-phase execution detail
  - deployment, conversation, and machine-role requirements remain consistent with master plan
- Exit criteria:
  - no requirement file remains placeholder-only
- Handoff target: `PG`, then `ASA`
- Anti-drift rule:
  - do not author design-pack or provenance-pack artifacts
- Proof that no approval is implied:
  - completion means only “requirements lane drafted”

### P1-TC-SC-01

- Role owner: `Source Cartographer`
- Model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- Objective: author the inheritance, catalog, and runtime-rebuild mapping lane.
- Exact files allowed to touch:
  - `01_plan/COMPONENT_CATALOG.md`
  - `01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `01_plan/RUNTIME_REBUILD_MAP.md`
- Files forbidden to touch:
  - all requirement-pack files
  - all design-pack files
  - all `04_execution/` files
- Required reads first:
  - master plan inheritance sections
  - source-of-truth governance files
  - relevant v1/tasklet/v2 lineage sources
- Step-by-step work method:
  1. enumerate required source pools and exact inherited names
  2. seed row-by-row coverage in the inheritance matrix
  3. seed exact-name rows in the component catalog
  4. map exact runtime modules in runtime rebuild map
  5. flag unresolved lineage items explicitly
  6. hand off to `ACL`, `PG`, and `ASA`
- Required cross-checks:
  - every source pool represented
  - exact inherited component names present
  - exact runtime modules present
- Exit criteria:
  - omission risk reduced to explicit unresolved rows only
- Handoff target: `ACL`, `PG`, `ASA`
- Anti-drift rule:
  - do not port code and do not claim lineage completeness without rows
- Proof that no approval is implied:
  - completion means only “mapping lane drafted”

### P1-TC-ACL-01

- Role owner: `Architecture & Contract Lead`
- Model tier: `gpt-5.4`
- Objective: author `TRACE_CONTRACT.md` and the full design-pack lane.
- Exact files allowed to touch:
  - `01_plan/TRACE_CONTRACT.md`
  - all required `03_design/*.md` files
- Files forbidden to touch:
  - all provenance files
  - all requirement-pack files except by reviewer comments in later review
  - all `04_execution/` files
- Required reads first:
  - master plan architecture/contract sections
  - `SC` first-pass mapping outputs
  - `CK` first-pass constitution/requirement outputs
- Step-by-step work method:
  1. draft architecture overview and contract framing
  2. freeze runner/gateway/UI split, operator command family, bundle integrity, sandbox, deployment, workspace, and public release framing
  3. align design files to the trace contract
  4. hand off to `PG` and `ASA`
- Required cross-checks:
  - runner/gateway/UI split explicit
  - bundle integrity and sandbox explicit
  - design files do not remain placeholder-only
- Exit criteria:
  - all design files are substantive Phase 1 drafts
- Handoff target: `PG`, then `ASA`
- Anti-drift rule:
  - do not author provenance or requirement-pack artifacts
- Proof that no approval is implied:
  - completion means only “design lane drafted”

### P1-TC-TRL-01

- Role owner: `Test & Replay Lead`
- Model tier: `gpt-5.4 mini`
- Objective: author the Phase 1 validation-protocol planning lane.
- Exact files allowed to touch:
  - `01_plan/VALIDATION_PROTOCOL.md`
- Files forbidden to touch:
  - requirement-pack files
  - design-pack files
  - provenance files
  - all `04_execution/` files
- Required reads first:
  - validation protocol current state
  - admin templates
  - closure-gate section of master plan
- Step-by-step work method:
  1. map closure records to required templates
  2. map closure chain to role-separated handoffs
  3. embed special Meta & Growth rule without activating that pod
  4. hand off to `PG`, `ASA`, `VA`
- Required cross-checks:
  - no self-approval path
  - no report-text-only closure path
  - closure records match admin templates
- Exit criteria:
  - validation protocol supports all Phase 1 closure gates
- Handoff target: `PG`, `ASA`, `VA`
- Anti-drift rule:
  - do not author requirement/design content
- Proof that no approval is implied:
  - completion means only “validation lane drafted”

### P1-TC-REL-01

- Role owner: `Release & Evidence Lead`
- Model tier: `gpt-5.4 mini`
- Objective: author the Phase 1 demo-protocol planning lane and evidence expectations.
- Exact files allowed to touch:
  - `01_plan/DEMO_PROTOCOL.md`
  - optional support draft under `00_admin/codex_threads/tasks/phase_01/` only if later execution needs a written demo checklist
- Files forbidden to touch:
  - requirement-pack files
  - design-pack files
  - provenance files
  - release execution artifacts
- Required reads first:
  - master plan demo expectations
  - validation protocol
  - current placeholder demo protocol
- Step-by-step work method:
  1. define the four user-review demos required for Phase 1
  2. define what must exist before each demo is shown
  3. define how evidence and demo package organization should look
  4. hand off to `PG`, `ASA`, `VA`
- Required cross-checks:
  - demos are inspectable by a human
  - evidence expectations do not overclaim
- Exit criteria:
  - demo protocol ties directly to user review package
- Handoff target: `PG`, `ASA`, `VA`
- Anti-drift rule:
  - do not drift into Phase 16 release execution
- Proof that no approval is implied:
  - completion means only “demo lane drafted”

### P1-TC-ASA-01

- Role owner: `Anti-Shortcut Auditor`
- Model tier: `gpt-5.4 mini` with `gpt-5.4 nano` utility helpers only
- Objective: audit Phase 1 artifact coverage and detect fake completeness.
- Exact files allowed to touch:
  - optional audit support draft under `00_admin/codex_threads/tasks/phase_01/`
- Files forbidden to touch:
  - canonical content files in `01_plan`, `02_requirements`, `03_design`
  - all `04_execution/` files
- Required reads first:
  - all authored Phase 1 artifacts
  - closure-gate list
  - admin templates
- Step-by-step work method:
  1. compare artifact set to master-plan required file list
  2. compare required closure gates to actual drafted coverage
  3. compare source-pool requirements to inheritance artifacts
  4. write audit findings and blockers
  5. hand off to `MA` and `PG`
- Required cross-checks:
  - no placeholder file is mislabeled as complete
  - no required source pool omitted
  - no exact inherited name or runtime module silently missing
- Exit criteria:
  - audit findings explicit and reproducible
- Handoff target: `MA`, `PG`
- Anti-drift rule:
  - do not “help by fixing content”
- Proof that no approval is implied:
  - audit pass is not approval

### P1-TC-MA-01

- Role owner: `Merge Arbiter`
- Model tier: `gpt-5.3-codex`
- Objective: integrate cleared Phase 1 artifact changes only after audit clearance in the later execution run.
- Exact files allowed to touch:
  - merge-only integration across the planned Phase 1 artifact set after audit clearance
- Files forbidden to touch:
  - authoring fresh content
  - approval records
  - user verdict
- Required reads first:
  - branch/worktree policy
  - audit findings
  - governor instructions
- Step-by-step work method:
  1. verify disjoint authoring lanes and audit clearance
  2. integrate cleared changes only
  3. preserve rollback path
  4. hand off to `PG`
- Required cross-checks:
  - same-model different-agent rule preserved
  - no unaudited content integrated
- Exit criteria:
  - integrated draft set matches audited content
- Handoff target: `PG`
- Anti-drift rule:
  - do not author, reinterpret, or approve content
- Proof that no approval is implied:
  - merge completion is not validation or approval

### P1-TC-VA-01

- Role owner: `Validation Agent`
- Model tier: `gpt-5.4`
- Objective: prepare the machine-side review request for user review of the Phase 1 artifact set.
- Exact files allowed to touch:
  - optional validation request draft under `00_admin/codex_threads/tasks/phase_01/`
- Files forbidden to touch:
  - canonical Phase 1 content files
  - user verdict
  - approval state
- Required reads first:
  - audited Phase 1 artifact set
  - governor verification record
  - demo protocol
- Step-by-step work method:
  1. read only the drafted artifacts, audit findings, and demo plan
  2. write the review request with exact inspectable checkpoints
  3. hand off to `PG`
- Required cross-checks:
  - validation request points to real artifacts and demos
  - no self-approval or hidden claims
- Exit criteria:
  - user review request is specific and evidence-backed
- Handoff target: `PG`
- Anti-drift rule:
  - do not author canonical content or final verdict text
- Proof that no approval is implied:
  - validation request is not approval

## 10. Closure-gate mapping

| Closure gate | Satisfying artifacts | Responsible role | How checked | Failure looks like |
| --- | --- | --- | --- | --- |
| every source pool has row-by-row inheritance coverage | `SOURCE_INHERITANCE_MATRIX.md` | `SC` | `ASA` samples each required source pool and checks row presence | source pool missing or only mentioned in prose |
| all required AGIFCore project-level truth files exist | project truth files + Phase 1 plan | `PG` | existence check against master plan | missing truth file or missing review reference |
| all required requirement files exist | full `02_requirements/` pack | `CK` | existence + non-placeholder audit | any requirement file missing or still 4-line placeholder |
| all required design files exist | full `03_design/` pack | `ACL` | existence + non-placeholder audit | any design file missing or still 4-line placeholder |
| all 8 proof domains are frozen explicitly | `PROOF_DOMAIN_MATRIX.md` | `PG` | exact 8 domains checked against master plan | missing, renamed, or merged domain |
| all exact inherited component names are cataloged | `COMPONENT_CATALOG.md` | `SC` | required exact-name sample list checked | one or more required exact names absent |
| all exact runtime modules are mapped | `RUNTIME_REBUILD_MAP.md` | `SC` | exact module list checked | any required runtime module absent |
| operator command family is frozen | `WORKSPACE_MODEL.md`, `PRODUCT_RUNTIME_MODEL.md`, `ARCHITECTURE_OVERVIEW.md` | `ACL` | command family explicitly present in text | operator surfaces vague or missing |
| machine-role policy is frozen | `MACHINE_ROLE_POLICY.md`, `DEPLOYMENT_PROFILES.md` | `CK` | laptop/builder/soak rules explicit | ambiguous machine privilege or missing soak rule |
| runner/gateway/UI split is frozen | `PRODUCT_RUNTIME_MODEL.md`, `ARCHITECTURE_OVERVIEW.md` | `ACL` | split explicitly named and bounded | mixed or missing boundaries |
| bundle integrity and sandbox rules are frozen | `BUNDLE_INTEGRITY_MODEL.md`, `SANDBOX_MODEL.md` | `ACL` | explicit integrity and sandbox rule sections | placeholder-only or vague security text |
| release/publication lane is frozen explicitly | `PUBLIC_RELEASE_MODEL.md`, `DEMO_PROTOCOL.md` | `ACL` with `REL` support | explicit release/publication lane present | no explicit publication or evidence-lane logic |

## 11. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| full architecture demo | architecture overview, trace contract, full design-pack first-pass drafts, runner/gateway/UI split | `PG` with `ACL` support | `ASA` | system framing, design boundaries, no runtime implementation drift |
| inheritance matrix demo | source inheritance matrix, component catalog, runtime rebuild map, sampled lineage references | `SC` | `ASA` | row-by-row source coverage, exact-name mapping, exact runtime-module mapping |
| requirement pack demo | full requirement-pack first-pass drafts, constitution, human-thinking target, phase approval rules | `CK` | `ASA` | non-negotiables, scientific method, conversation scope, machine-role policy, no placeholder fake-completion |
| design pack demo | full design-pack first-pass drafts, proof-domain matrix, validation protocol, demo protocol | `ACL` with `REL` support | `ASA` | architecture completeness, contract framing, proof-domain freezing, later demo readiness |

## 12. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| silent omission from source inheritance matrix | row-by-row source-pool audit | `ASA` | any required source pool or lineage family missing | freeze provenance lane and reopen `SC` task |
| fake completeness in requirement pack | placeholder-length and content audit | `ASA` | any requirement file remains placeholder-only | block closure and reopen `CK` lane |
| contract drift | cross-check `TRACE_CONTRACT.md` against conversation/product/workspace design files | `PG` | contract language conflicts across files | reopen `ACL` lane before validation |
| architecture vagueness | design-pack review for missing boundaries | `PG` | runner/gateway/UI, operator family, sandbox, or release lane not explicit | hold design demo and reopen `ACL` |
| over-activation of unnecessary pods | team-map review | `PG` | inactive pod given authoring scope without narrow justification | deactivate pod and reset task cards |
| model misuse for wrong task type | compare task cards to model manifest | `PG` | top-tier model used for utility work or wrong-model role activation | reopen task cards and reassign |
| premature implementation before planning approval | branch/worktree and file-scope audit | `ASA` | any `04_execution/` or runtime code touched | freeze work and escalate to user |
| same-model separation becomes fake | session-id check in task cards and governor checklist | `PG` | Build Pod, Merge Arbiter, and Validation share agent identity | invalidate lane separation and reopen tasks |
| Source Cartographer overhead persists after Phase 1 | role-activation review | `PG` | `SC` remains active without lineage touch | deactivate `SC` and record reason |
| Product & Sandbox becomes late-phase dumping lane | task-card scope audit | `ASA` | unrelated late-phase work assigned to Product & Sandbox | reject assignment and reassign by Governor |
| placeholder planning files get mistaken as completion | line-count and substantive-content audit | `ASA` | any current placeholder file counted as closure evidence | block closure and require substantive draft |
| unresolved Phase 0 blockers ignored | prerequisite check before execution | `PG` | archival note/source-freeze method still absent at execution start | hold Phase 1 execution until resolved or explicitly waived |

## 13. Approval, commit, and freeze protocol

- This run is planning-only.
- No commit now.
- No freeze now.
- No tag now.
- No merge now.
- No approval now.
- No runtime code now.
- No later-phase work now.
- This planning draft does not authorize writing any Phase 1 artifact by itself.
- Only after the user explicitly says approved may a later separate run create or update the Phase 1 plan artifact and any optional planning-support drafts.
- Only after a later separate user approval may another later run commit and freeze the approved Phase 1 plan artifacts.
- After user approval and any later freeze, any future change must require:
  - explicit reopen instruction from the user
  - a supersession note that names the replaced Phase 1 plan artifact
  - a new validation pass before re-freeze
- Nothing in this draft implies that Phase 1 is complete.
- Nothing in this draft implies that Phase 2 may begin.

## 14. Final readiness judgment

`blocked_pending_prerequisites`

Why:
- the planning draft can be reviewed now,
- but Phase 0 still appears open from repo files,
- and the explicit Phase 0 archival note and source-freeze method artifacts required by the master plan were not found as distinct project artifacts,
- so later Phase 1 execution should be treated as blocked until those prerequisites are resolved or explicitly waived by the user.
