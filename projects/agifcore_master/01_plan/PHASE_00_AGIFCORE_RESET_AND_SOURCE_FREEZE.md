# Phase 0: AGIFCore Reset and Source Freeze

## 1. Phase identity

- Phase number: `0`
- Canonical phase name: `AGIFCore Reset and Source Freeze`
- Status: `planning_draft`
- Canonical artifact path: `projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
- Source-of-truth references reviewed:
  - `AGENTS.md`
  - `projects/agifcore_master/AGENTS.override.md`
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_01_PLAN_FREEZE_HANDOFF.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/GOVERNOR_NEXT_THREAD_BRIEF.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
  - `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`
  - current live state in `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - current noncanonical draft inputs:
    - `projects/agifcore_master/01_plan/PHASE_00_AGIF_V2_ARCHIVAL_NOTE.md`
    - `projects/agifcore_master/01_plan/PHASE_00_SOURCE_FREEZE_INVENTORY.md`
    - `projects/agifcore_master/01_plan/PHASE_00_SOURCE_FREEZE_METHOD.md`

## 2. Phase mission

- Phase 0 exists to verify the AGIFCore scaffold, freeze AGIF v2 as historical source input only, freeze the source-pool list and source-freeze method, verify planning skeleton presence, and establish truthful closure controls before clean Phase 1 progression.
- Phase 0 must establish:
  - a canonical Phase 0 plan artifact
  - one canonical AGIF v2 archival note
  - one canonical source-freeze inventory
  - one canonical source-freeze method
  - one project-structure audit
  - one truthful Phase 0 gate path that stays open until audit, validation, and user approval are complete
- Phase 0 must not:
  - draft Phase 1 requirement-pack or design-pack content
  - execute runtime work
  - perform Phase 2 planning
  - redesign the team
  - imply approval, closure, or freeze

## 3. Scope and non-goals

### In scope

- `projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
- `projects/agifcore_master/01_plan/AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md`
- `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
- `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
- `projects/agifcore_master/01_plan/PROJECT_STRUCTURE_AUDIT.md`
- `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- Phase 0 task cards under `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/`
- Phase 0 handoff-path planning under `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- deliberate reconciliation of older `PHASE_00_*` draft inputs so they do not count as closure evidence

### Out of scope

- any edits to `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- any edits to `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
- Phase 1 execution
- Phase 2 planning
- runtime code
- requirement-pack drafting under `02_requirements/`
- design-pack drafting under `03_design/`
- merge, freeze, tag, or approval actions

### Untouched boundaries

- Frozen Phase 1 execution remains untouched.
- All Phase 2 work remains untouched.
- No Phase 0 artifact may be used to claim Phase 1 completion.

## 4. Relationship to the frozen Phase 1 baseline

- Phase 1 planning is already frozen in `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`.
- That frozen baseline explicitly called out three Phase 0 blocker areas:
  - missing distinct archival note
  - missing distinct source-freeze inventory and method artifacts
  - open Phase 0 status in `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- Phase 0 must be planned and executed now because clean Phase 1 progression depends on truthful resolution of those blocker areas without mutating the frozen Phase 1 scope.
- Later Phase 0 execution may update only:
  - Phase 0 canonical artifacts
  - Phase 0 task cards and handoff records
  - the truthful Phase 0 row in `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- Phase 0 must not mutate:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - any Phase 1, Phase 2, or runtime implementation artifact
- Older `PHASE_00_*` files are treated as noncanonical draft inputs only. They are not closure evidence by requested name or approval status.

## 5. Active team map for Phase 0

| Role | Model tier | Status | Why | Exact responsibility this phase | Must never do this phase |
| --- | --- | --- | --- | --- | --- |
| User | none | active | final human approver | review Phase 0 surfaces later and approve or reject | delegate final approval |
| Program Governor | `gpt-5.4` | active | top planning and truth-control authority | own Phase 0 plan, task-card map, gate reconciliation, blocker truth, and cross-artifact alignment | rewrite frozen Phase 1, do Phase 2 planning, self-approve |
| Constitution Keeper | `gpt-5.4-mini` | active | archival wording and anti-drift discipline are needed | own the AGIF v2 archival-note artifact, review Phase 0 gate wording, guard non-negotiables and anti-drift boundaries | soften archival language, rewrite architecture, approve the phase |
| Source Cartographer | `gpt-5.4-mini` with `gpt-5.4-nano` helpers for extraction only | active | source-freeze scope must be explicit before Phase 1 provenance work | own source-freeze inventory and source-freeze method artifacts | begin Phase 1 row-by-row inheritance mapping, port code, approve the phase |
| Architecture & Contract Lead | `gpt-5.4` | inactive | Phase 0 does not need architecture drafting by default | remain available only for narrow consultation if Phase 0 wording collides with frozen contract boundaries | author design-pack work or reopen architecture scope casually |
| Kernel Pod Lead | `gpt-5.3-codex` | inactive | no runtime execution belongs in Phase 0 | none | implement Phase 2 work |
| Memory & Graph Pod Lead | `gpt-5.3-codex` | inactive | no runtime execution belongs in Phase 0 | none | implement Phase 4-5 work |
| World & Conversation Pod Lead | `gpt-5.3-codex` | inactive | no runtime execution belongs in Phase 0 | none | implement Phase 6-9 work |
| Meta & Growth Pod Lead | `gpt-5.3-codex` | inactive | danger zone not needed in Phase 0 | none | activate casually or author Phase 10-12 work |
| Product & Sandbox Pod Lead | `gpt-5.3-codex` | inactive | Phase 0 is governance/documentation only | none | become a dumping lane for late-phase product work |
| Test & Replay Lead | `gpt-5.4-mini` | active | project-structure verification and closure-check planning are required | own project-structure audit and Phase 0 verification expectations | author archival or source policy, approve the phase |
| Anti-Shortcut Auditor | `gpt-5.4-mini` with `gpt-5.4-nano` helpers for utility checking only | active | Phase 0 is vulnerable to fake blocker closure and naming drift | audit Phase 0 artifact truth, detect omissions, detect unsupported claims, detect gate misuse | implement canonical content, downgrade blockers to cosmetic issues, approve the phase |
| Merge Arbiter | `gpt-5.3-codex` | inactive by default | planning-only work does not need integration by default | remain unavailable unless later execution splits authoring into multiple governed branches | author canonical content or approve integration |
| Validation Agent | `gpt-5.4` | active | Phase 0 requires a later machine-side completeness review before user review | own the later validation request path for Phase 0 | author canonical Phase 0 content, write the user verdict |
| Release & Evidence Lead | `gpt-5.4-mini` | active, narrow scope only | later user review surface must be inspectable | define the review packet surface for project structure, archival statement, and source-freeze method | drift into Phase 16 release execution or soften claims |

## 6. Artifact ownership matrix

| Artifact path | Primary author | Reviewer | Auditor | Validator | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md` | Program Governor | Constitution Keeper | Anti-Shortcut Auditor | Validation Agent | master plan, frozen Phase 1 baseline, admin controls, current gate state, current draft-input state | all later Phase 0 execution | section-complete Phase 0 plan with explicit ownership, order, and gate mapping |
| `projects/agifcore_master/01_plan/AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md` | Constitution Keeper | Program Governor | Anti-Shortcut Auditor | Validation Agent | master plan, project truth files, frozen Phase 1 blocker language, current archival wording | clean Phase 1 prerequisite truth | explicit archival statement, allowed use, blocked shortcuts, no ambiguity |
| `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md` | Source Cartographer | Program Governor | Anti-Shortcut Auditor | Validation Agent | master plan source list, current repo state, current draft inputs | Phase 1 provenance mapping | exact four source pools listed with clear status and boundary |
| `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md` | Source Cartographer | Constitution Keeper | Anti-Shortcut Auditor | Validation Agent | source-freeze inventory, master plan, Phase 1 provenance rule set | later provenance mapping and Phase 1 closure truth | concrete method, disposition rule, reopen rule, no implied inherited trust |
| `projects/agifcore_master/01_plan/PROJECT_STRUCTURE_AUDIT.md` | Test & Replay Lead | Program Governor | Anti-Shortcut Auditor | Validation Agent | master plan, current repo tree, root/project truth files, required folders, planning skeletons | later user review of structure | honest inventory of what exists, what is placeholder-only, what is deferred |
| `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` | Program Governor | Constitution Keeper | Anti-Shortcut Auditor | Validation Agent | master plan, Phase 0 plan, actual closure records | truthful phase status | Phase 0 row stays `open` until audit, governor verification, validation request, and user approval exist |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/` | Program Governor | Constitution Keeper | Anti-Shortcut Auditor | Validation Agent | task-card template, model manifest, tool matrix, branch/worktree policy, ownership map | all later valid Phase 0 work | one task card per active non-user role with disjoint scope |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/` | Validation Agent for validation request, Program Governor for governor brief, User for verdict | Program Governor except user verdict | Anti-Shortcut Auditor | n/a | validation protocol, review-surface plan, real Phase 0 artifacts | final Phase 0 review path | real later handoff paths that point to inspectable artifacts and demo surfaces |

## 7. Workstream breakdown

### WS0 Governor planning baseline

- Objective: define the canonical Phase 0 plan and the initial Phase 0 task-card map.
- Owner: `Program Governor`
- Supporting roles: `Constitution Keeper`
- Planned outputs:
  - `projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
  - initial Phase 0 task-card set under `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/`
- Entry conditions:
  - frozen-source review complete
  - current blocker state verified from live files
- Exit criteria:
  - decision-complete plan exists
  - disjoint artifact ownership is explicit
  - no Phase 1 or Phase 2 scope leakage exists

### WS1 Repo scaffold and planning-skeleton verification

- Objective: verify the current scaffold and planning skeletons honestly.
- Owner: `Test & Replay Lead`
- Supporting roles: `Program Governor`
- Planned outputs:
  - `projects/agifcore_master/01_plan/PROJECT_STRUCTURE_AUDIT.md`
- Entry conditions:
  - current repo tree and master-plan structure list available
- Exit criteria:
  - explicit file/folder inventory exists
  - required root/project truth files are checked
  - required directories are checked
  - planning skeleton state is checked
  - placeholder state is called out honestly

### WS2 AGIF v2 archival-note planning

- Objective: freeze the historical status of AGIF v2 without loopholes.
- Owner: `Constitution Keeper`
- Supporting roles: `Program Governor`
- Planned outputs:
  - `projects/agifcore_master/01_plan/AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md`
- Entry conditions:
  - master-plan archival rule reviewed
  - current repo wording reviewed
- Exit criteria:
  - archival statement is explicit and non-reversible
  - permitted source use is explicit
  - blocked shortcuts are explicit
  - no Phase 1 or Phase 2 drift exists

### WS3 Source-freeze inventory planning

- Objective: freeze the exact source-pool scope that Phase 1 must later map.
- Owner: `Source Cartographer`
- Supporting roles: `Program Governor`
- Planned outputs:
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
- Entry conditions:
  - master-plan source-pool list reviewed
- Exit criteria:
  - exact four source pools are present
  - no silent omission exists
  - no implied trust or closure claim exists

### WS4 Source-freeze method planning

- Objective: define how frozen source material may be used without counting as AGIFCore completion.
- Owner: `Source Cartographer`
- Supporting roles: `Constitution Keeper`
- Planned outputs:
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
- Entry conditions:
  - `SOURCE_FREEZE_INVENTORY.md` first pass exists
- Exit criteria:
  - explicit use method exists
  - disposition rule exists
  - reopen rule for new source pools exists
  - Phase 1 provenance boundary is explicit

### WS5 Phase-gate reconciliation planning

- Objective: reconcile the open Phase 0 gate truthfully with the new canonical artifact set.
- Owner: `Program Governor`
- Supporting roles: `Constitution Keeper`
- Planned outputs:
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md` update plan
  - task/handoff path plan inside the main Phase 0 artifact and task cards
- Entry conditions:
  - WS1-WS4 first-pass outputs exist
- Exit criteria:
  - gate semantics are truthful
  - Phase 0 remains explicitly open until user approval
  - no false blocker-closure text exists

### WS6 Validation and review-surface planning

- Objective: define the later audit, verification, validation, and user-review surfaces for Phase 0.
- Owner: `Test & Replay Lead`
- Supporting roles: `Release & Evidence Lead`, `Validation Agent`, `Anti-Shortcut Auditor`
- Planned outputs:
  - planned audit report path
  - planned governor verification path
  - planned validation request path
  - later user-review surface definition
- Entry conditions:
  - WS0-WS5 first-pass outputs exist
- Exit criteria:
  - later review surfaces are inspectable
  - no self-approval path exists
  - evidence and user-review expectations are explicit

## 8. Ordered execution sequence

1. `Program Governor` authors the canonical Phase 0 planning artifact and opens the Phase 0 task-card set.
2. `Constitution Keeper` drafts the archival-note artifact.
3. `Source Cartographer` drafts the source-freeze inventory and source-freeze method artifacts.
4. `Test & Replay Lead` drafts the project-structure audit in parallel with steps 2 and 3.
5. `Program Governor` reconciles the Phase 0 gate language only after first-pass outputs from steps 2-4 exist.
6. `Release & Evidence Lead` defines the later review packet surface only after the structure, archival, and source-freeze outputs are first-pass complete.
7. `Anti-Shortcut Auditor` audits the Phase 0 artifact set after steps 1-6 complete.
8. `Program Governor` reviews the audited Phase 0 set and prepares the later verification path.
9. `Validation Agent` validates Phase 0 completeness for later user review.
10. User review happens later in a separate pass; no approval is implied in this execution run.

### Safe parallelism

- Safe in parallel:
  - `Constitution Keeper` archival-note lane
  - `Source Cartographer` source-freeze lane
  - `Test & Replay Lead` structure-audit lane
- Must wait:
  - gate reconciliation waits for first-pass outputs from the three drafting lanes above
  - audit waits for all authoring to finish
  - validation waits for audit and governor verification
- Handoffs:
  - `CK` -> `PG`, `ASA`
  - `SC` -> `PG`, `ASA`
  - `TRL` -> `PG`, `REL`, `ASA`
  - `REL` -> `PG`, `ASA`, `VA`
  - `ASA` -> `PG`
  - `PG` -> `VA` -> User

## 9. Detailed task cards

User is active approval-only and does not receive a task card.

### P0-TC-PG-01

- Role owner: `Program Governor`
- Model tier: `gpt-5.4`
- Objective: own the Phase 0 plan, task-card map, and gate reconciliation.
- Exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/*`
- Files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - all `projects/agifcore_master/02_requirements/*`
  - all `projects/agifcore_master/03_design/*`
  - all `projects/agifcore_master/04_execution/*`
- Required reads first:
  - all source-of-truth files listed in Section 1
- Step-by-step work method:
  1. verify live blocker state against files
  2. define active and inactive Phase 0 roles
  3. author the canonical Phase 0 plan
  4. author the Phase 0 task-card set
  5. reconcile truthful gate language
  6. hand off to `ASA`
- Required cross-checks:
  - no Phase 1 mutation
  - no Phase 2 scope
  - no false closure language
- Exit criteria:
  - section-complete Phase 0 plan exists
  - task-card set is ready
- Handoff target: `ASA`
- Anti-drift rule:
  - do not author requirement-pack, design-pack, or runtime content
- Proof that no approval is implied:
  - completion means only `ready_for_audit`

### P0-TC-CK-01

- Role owner: `Constitution Keeper`
- Model tier: `gpt-5.4-mini`
- Objective: own the archival-note artifact and archival wording discipline.
- Exact files allowed to touch:
  - `projects/agifcore_master/01_plan/AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md`
- Files forbidden to touch:
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
  - all `projects/agifcore_master/03_design/*`
  - all `projects/agifcore_master/04_execution/*`
- Required reads first:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
  - project truth files
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- Step-by-step work method:
  1. map archival language to the master-plan archival rule
  2. draft the explicit archival statement
  3. define allowed use and blocked shortcuts
  4. hand off to `PG` then `ASA`
- Required cross-checks:
  - no soft wording
  - no loophole that treats v2 as done
  - no Phase 1 or Phase 2 drift
- Exit criteria:
  - explicit archival-note draft exists
- Handoff target: `PG`, then `ASA`
- Anti-drift rule:
  - do not author source-freeze or gate content
- Proof that no approval is implied:
  - completion means only `ready_for_audit`

### P0-TC-SC-01

- Role owner: `Source Cartographer`
- Model tier: `gpt-5.4-mini` with `gpt-5.4-nano` helpers only for extraction
- Objective: own the source-freeze inventory and source-freeze method artifacts.
- Exact files allowed to touch:
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_INVENTORY.md`
  - `projects/agifcore_master/01_plan/SOURCE_FREEZE_METHOD.md`
- Files forbidden to touch:
  - all `projects/agifcore_master/02_requirements/*`
  - all `projects/agifcore_master/03_design/*`
  - all `projects/agifcore_master/04_execution/*`
  - Phase 1 provenance artifacts
- Required reads first:
  - master-plan source list
  - role rules
  - current draft source-freeze inputs if present
  - Phase 1 blocker wording
- Step-by-step work method:
  1. enumerate the exact source pools
  2. define the inventory table
  3. define the method and reopen rules
  4. hand off to `PG` then `ASA`
- Required cross-checks:
  - exact four source pools present
  - disposition rule present
  - no inherited trust claims
  - explicit Phase 1 boundary present
- Exit criteria:
  - both source-freeze artifacts are decision-complete
- Handoff target: `PG`, then `ASA`
- Anti-drift rule:
  - do not start row-by-row Phase 1 inheritance mapping
- Proof that no approval is implied:
  - completion means only `ready_for_audit`

### P0-TC-TRL-01

- Role owner: `Test & Replay Lead`
- Model tier: `gpt-5.4-mini`
- Objective: own `PROJECT_STRUCTURE_AUDIT.md` and the Phase 0 verification chain planning.
- Exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PROJECT_STRUCTURE_AUDIT.md`
  - optional Phase 0 verification-support drafts under `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/`
- Files forbidden to touch:
  - canonical archival/source-freeze content files
  - all `projects/agifcore_master/03_design/*`
  - all `projects/agifcore_master/04_execution/*`
- Required reads first:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - task-card template
  - current repo tree
- Step-by-step work method:
  1. inventory required root files, project truth files, required directories, and planning skeletons
  2. note placeholder state and deferred work honestly
  3. define exact checks and later verification expectations
  4. hand off to `PG`, `REL`, and `ASA`
- Required cross-checks:
  - no file-count theater
  - placeholder state explicitly called out
  - no later-phase completion implied
- Exit criteria:
  - structure-audit artifact exists
- Handoff target: `PG`, `REL`, `ASA`
- Anti-drift rule:
  - do not author archival policy or source-pool policy
- Proof that no approval is implied:
  - completion means only `ready_for_audit`

### P0-TC-REL-01

- Role owner: `Release & Evidence Lead`
- Model tier: `gpt-5.4-mini`
- Objective: define the later review packet surface for Phase 0.
- Exact files allowed to touch:
  - optional review-surface planning drafts under `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/`
  - references inside `projects/agifcore_master/01_plan/PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md`
- Files forbidden to touch:
  - canonical archival/source-freeze content outside narrow review-surface references
  - release execution artifacts
  - all `projects/agifcore_master/04_execution/*`
- Required reads first:
  - the Phase 0 plan
  - `PROJECT_STRUCTURE_AUDIT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- Step-by-step work method:
  1. define what the user must inspect
  2. define what good looks like for each review surface
  3. define how evidence should be grouped later
  4. hand off to `PG`, `ASA`, `VA`
- Required cross-checks:
  - no release/publication drift
  - no overclaim
- Exit criteria:
  - later review-surface plan is decision-complete
- Handoff target: `PG`, `ASA`, `VA`
- Anti-drift rule:
  - do not expand into Phase 16 release work
- Proof that no approval is implied:
  - completion means only `ready_for_audit`

### P0-TC-ASA-01

- Role owner: `Anti-Shortcut Auditor`
- Model tier: `gpt-5.4-mini` with `gpt-5.4-nano` helpers only for utility checking
- Objective: audit the full Phase 0 plan artifact set.
- Exact files allowed to touch:
  - audit records under `projects/agifcore_master/00_admin/codex_threads/tasks/phase_00/`
- Files forbidden to touch:
  - canonical `projects/agifcore_master/01_plan/*` content
  - all `projects/agifcore_master/02_requirements/*`
  - all `projects/agifcore_master/03_design/*`
  - all `projects/agifcore_master/04_execution/*`
- Required reads first:
  - all authored Phase 0 artifacts
  - task cards
  - templates
  - gate rules
- Step-by-step work method:
  1. compare claims against files
  2. compare Phase 0 requirements to actual planned outputs
  3. compare canonical naming to current worktree drift
  4. write audit findings
  5. hand off to `PG`
- Required cross-checks:
  - no fake completeness
  - no missing source pool
  - no vague archival note
  - no hidden Phase 1 mutation
- Exit criteria:
  - explicit audit result exists
- Handoff target: `PG`
- Anti-drift rule:
  - do not fix canonical content
- Proof that no approval is implied:
  - audit is not approval

### P0-TC-VA-01

- Role owner: `Validation Agent`
- Model tier: `gpt-5.4`
- Objective: perform the later machine-side completeness review of the Phase 0 package before user review.
- Exact files allowed to touch:
  - validation request drafts under `projects/agifcore_master/00_admin/codex_threads/handoffs/`
- Files forbidden to touch:
  - canonical Phase 0 content files
  - user verdict
- Required reads first:
  - audited Phase 0 artifact set
  - governor verification record
  - later review packet surface plan
- Step-by-step work method:
  1. read the finalized Phase 0 package only
  2. point the user to the exact review surfaces
  3. define what to confirm and what failure looks like
  4. hand off to `PG`
- Required cross-checks:
  - no self-approval path
  - no missing review artifact
  - every requested check points to a real file
- Exit criteria:
  - validation request is specific and evidence-backed
- Handoff target: `PG`
- Anti-drift rule:
  - do not author canonical content
- Proof that no approval is implied:
  - validation request is not approval

## 10. Closure-gate mapping

| Closure requirement | Satisfying artifact(s) | Responsible role | How checked | Failure looks like | How `PHASE_GATE_CHECKLIST.md` eventually moves |
| --- | --- | --- | --- | --- | --- |
| repo scaffold exists and planning skeletons are verified | `PROJECT_STRUCTURE_AUDIT.md` | `TRL` | file-and-folder inventory against `MASTER_PLAN.md` | missing required truth file, missing required directory, or silent omission of placeholder state | does not move until audit confirms the audit artifact is truthful |
| AGIF v2 is explicitly archived as historical source only | `AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md` | `CK` | compare wording to `MASTER_PLAN.md` and the frozen Phase 1 blocker language | vague language, reversibility, or loophole that lets v2 count as done | does not move until audit confirms the archival wording is explicit |
| source pools are explicitly frozen | `SOURCE_FREEZE_INVENTORY.md` | `SC` | compare against the four master-plan source pools | missing source pool, renamed pool, or prose-only mention with no explicit row | does not move until audit confirms all four pools are present |
| source-freeze method is explicit | `SOURCE_FREEZE_METHOD.md` | `SC` | check for required dispositions, reopen rule, and Phase 1 boundary | underspecified use rules or no reopen rule | does not move until audit confirms the method is explicit |
| Phase 0 blocker linkage to frozen Phase 1 is explicit | `PHASE_00_AGIFCORE_RESET_AND_SOURCE_FREEZE.md` | `PG` | compare to the Phase 1 prerequisite section directly | plan text ignores or rewrites the frozen blocker linkage | does not move until audit confirms the linkage is preserved |
| Phase 0 gate truth is explicit | `PHASE_GATE_CHECKLIST.md`, audit report, governor verification record, validation request, user verdict | `PG` | follow the closure chain in `VALIDATION_PROTOCOL.md` | any attempt to move the row by summary text or artifact existence alone | row stays `open` during authoring, audit, governor verification, validation request, and user review |

Phase 0 may move from `open` to `approved` only after:
1. canonical Phase 0 artifacts exist
2. an audit report exists
3. a governor verification record exists
4. a validation request exists
5. the user verdict is `approved`

There is no separate `closed` status in the current checklist scheme.

## 11. Demo and validation plan

| Review surface | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| project structure | `PROJECT_STRUCTURE_AUDIT.md`, root/project truth file list, required folder list, planning skeleton verification summary | `TRL` with `PG` support | `ASA` | what exists, what is placeholder-only, what is intentionally deferred |
| archival statement | `AGIF_V2_HISTORICAL_ARCHIVAL_NOTE.md` plus direct linkage to the master-plan archival rule | `CK` | `ASA` | exact archival wording, allowed-use boundary, blocked shortcuts |
| source-freeze method | `SOURCE_FREEZE_INVENTORY.md`, `SOURCE_FREEZE_METHOD.md`, and the four source pools from `MASTER_PLAN.md` | `SC` | `ASA` | source list, use method, reopen rule, and the rule that old artifacts do not count as AGIFCore completion |

## 12. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| archival note is vague and non-final | wording review against master plan and frozen blocker language | `CK` | any text allows AGIF v2 to count as partially done | reopen archival-note work and block gate movement |
| source-freeze inventory silently omits source pools | exact comparison to the four master-plan source pools | `SC` | any required source pool missing | reopen inventory work and reject downstream provenance planning |
| source-freeze method is underspecified | check for missing disposition rule, missing reopen rule, or missing Phase 1 boundary | `SC` | any ambiguity would force later improvisation | reopen method work before audit can pass |
| project-structure audit is superficial | compare the audit artifact to required root files, project truth files, required folders, and planning skeletons | `TRL` | audit text says only that scaffold exists without enumeration | reopen structure-audit work |
| fake blocker closure | compare `PHASE_GATE_CHECKLIST.md` language to actual audit/validation/user-review records | `ASA` | checklist implies earned status before user approval | freeze closure and reopen gate reconciliation |
| Phase 0 accidentally mutates frozen Phase 1 | direct diff review of `MASTER_PLAN.md` and `PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md` | `PG` | any edit or rewrite attempt appears | quarantine the change and escalate if needed |
| current noncanonical draft files create naming drift | check for coexistence of requested canonical names and older `PHASE_00_*` draft inputs without explicit supersession language | `PG` | later execution would leave two competing artifact families | require canonical requested names exactly and record the older files as noncanonical inputs only |

## 13. Approval, commit, and freeze protocol

- The earlier Phase 0 planning run was planning-only.
- This execution run creates the canonical Phase 0 artifact set and task-card map only.
- No commit now.
- No freeze now.
- No tag now.
- No approval now.
- Phase 0 is not complete in this run.
- Only after a later audit pass, governor verification pass, validation request, and explicit user approval may Phase 0 be considered approved.
- Any later change to the canonical Phase 0 artifacts must require:
  - explicit reopen instruction
  - a supersession note naming the replaced artifact
  - a new audit and validation pass before approval

## 14. Final readiness judgment

`ready_for_user_review`

Why:
- the canonical Phase 0 plan and closure-target artifacts now exist under the requested names,
- the older `PHASE_00_*` draft files are treated as noncanonical inputs only,
- the gate remains explicitly open,
- and the next required steps are audit, governor verification, validation request, and later user review rather than more scope expansion.
