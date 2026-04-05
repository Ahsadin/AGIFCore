# Phase 15: Final Intelligence Proof and Closure Audit

Brief summary:

Phase 15 is the governed proof, repair-readiness, durability, reproducibility, and closure layer above approved Phase 13 product-runtime truth and approved Phase 14 sandbox/profile truth, and below Phase 16 release/publication work. It must later prove the already-built AGIFCore system honestly. If that proof is blocked because the approved live turn path is too weak, Phase 15 may repair that path only through the approved Phase 13 host seam and must then prove the repaired path through blind, hidden, live-demo, soak, hardening, reproducibility, and closure-audit lanes. The final user-facing demo for Phase 15 must be a real desktop UI chat demo on the approved Phase 13 host path, not a terminal-only shell.

Planned interface additions for later execution:

- proof runtime family under `projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/`
- thin proof contracts:
  - `agifcore.phase_15.blind_pack.v1`
  - `agifcore.phase_15.hidden_pack.v1`
  - `agifcore.phase_15.live_demo_pack.v1`
- thin durability and closure contracts:
  - `agifcore.phase_15.soak_harness.v1`
  - `agifcore.phase_15.hardening_package.v1`
  - `agifcore.phase_15.reproducibility_package.v1`
  - `agifcore.phase_15.closure_audit.v1`
- thin live-turn proof contracts over the approved Phase 13 host seam:
  - `agifcore.phase_15.live_turn_proof.v1`
  - `agifcore.phase_15.follow_up_continuity.v1`
  - `agifcore.phase_15.real_desktop_chat_demo.v1`

Planning defaults chosen:

- later execution keeps one active build pod by default: `Test & Replay Lead`
- later execution must prove the already-approved system through existing Phase 13 and Phase 14 interfaces instead of rebuilding them from zero
- later execution must treat the current weak live-turn/chat path as a Phase 15 proof-readiness gap, not as a Phase 14 prerequisite blocker
- the primary final demo host is the approved Phase 13 local desktop UI
- terminal chat remains a secondary debug/proof surface only and may not be the primary user-review host
- the desktop UI must never own correctness; the runtime remains the only correctness path
- release notes, public evidence indexes, tags, publication packages, and public reproducibility work stay out of Phase 15
- the existing project-scoped `.codex` setup is reusable as-is; no maintenance change is required before Phase 15 planning or later execution start

## 1. Phase identity

- phase number: `15`
- canonical phase name: `Final Intelligence Proof and Closure Audit`
- status: `planning_draft`
- source-of-truth references reviewed:
  - repo policy stack: `AGENTS.md`, `projects/agifcore_master/AGENTS.override.md`, `PROJECT_README.md`, `DECISIONS.md`, `CHANGELOG.md`
  - master truth and gates: `MASTER_PLAN.md`, `PHASE_INDEX.md`, `PHASE_GATE_CHECKLIST.md`
  - approved phase plans: `PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md` through `PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - Phase 1 provenance and closure stack: `SYSTEM_CONSTITUTION.md`, `HUMAN_THINKING_TARGET.md`, `COMPONENT_CATALOG.md`, `SOURCE_INHERITANCE_MATRIX.md`, `RUNTIME_REBUILD_MAP.md`, `TRACE_CONTRACT.md`, `VALIDATION_PROTOCOL.md`, `DEMO_PROTOCOL.md`
  - all files under `projects/agifcore_master/02_requirements/`
  - all files under `projects/agifcore_master/03_design/`
  - approved Phase 2 through Phase 14 execution, testing, and output surfaces under `04_execution/`, `05_testing/`, and `06_outputs/`
  - admin controls under `projects/agifcore_master/00_admin/`
  - `.codex/config.toml` and `.codex/agents/*.toml`
  - directly inspected donor proof and closure lineage from `agif_fabric_v1` and `agif_fabric_v2/projects/agif_v2_master`
  - directly inspected Phase 13 host/runtime surfaces and outputs under `phase_13_product_runtime_and_ux/`

## 2. Phase mission

- Phase 15 exists to define and later build the explicit proof, live-turn proof-readiness repair, durability, reproducibility, and closure-audit layer that proves the full approved AGIFCore system against the locked proof domains and closure rules before any release/publication work.
- Phase 15 must later build:
  - blind packs
  - hidden packs
  - live-demo pack
  - soak harness
  - hardening package
  - reproducibility package
  - closure audit
  - live-turn integration repair only where proof is blocked by the weak current Phase 13 chat path
  - a real desktop UI chat demo on the approved Phase 13 host path
- Phase 15 must later support user validation through:
  - final AGIFCore demo
  - soak summary
  - closure audit summary
- Phase 15 must not:
  - redesign or replace approved Phase 13 product-runtime behavior as a whole
  - redesign or replace approved Phase 14 sandbox/profile/scale behavior
  - start any Phase 16 release, publication, tag, or public-evidence work
  - create a second fake chat system beside AGIFCore
  - solve the chat problem with exact prompt-answer tables, regex-only routing, or a terminal-only stitched demo
  - treat notes, rubrics, or summaries as proof
  - imply commit, freeze, approval, or completion

## 3. Scope and non-goals

- in-scope artifacts:
  - canonical Phase 15 plan
  - Phase 15 planning task cards
  - proof/closure boundary rules
  - reuse and provenance decisions
  - live-turn proof-readiness repair planning over approved Phase 13 host seams
  - typed retrieval, follow-up continuity, current-world estimate, and question-class proof planning
  - real desktop UI chat demo planning
  - future execution, testing, outputs, and handoff targets
  - later demo, validation, and closure mapping
- out-of-scope work:
  - any Phase 15 runtime code
  - any Phase 15 verifier code
  - any Phase 15 evidence generation
  - any Phase 16 planning or execution
  - any team redesign
  - any commit, merge, tag, freeze, or approval action
  - any new cloud, web, or hidden external-intelligence path
  - any second correctness path outside the approved runtime
- explicit untouched-later-phase statement:
  - Phase 16 and all later phases remain untouched by this plan

## 4. Phase 14 prerequisite check

| Check | Verdict | Evidence | Impact |
| --- | --- | --- | --- |
| Phase 14 explicitly approved in current phase-truth files | `pass` | `PHASE_INDEX.md` shows Phase 14 `approved` and Phase 15 `open`; `PHASE_GATE_CHECKLIST.md` shows the same | Phase 15 planning may proceed |
| Explicit Phase 14 approval truth exists outside the gate tables | `pass` | `DECISIONS.md` entry `D-039` states that Phase 14 is approved and Phase 15 had not started when the approval was recorded | no silent approval assumption |
| Required Phase 1 provenance artifacts relied on exist | `pass` | constitution, provenance, validation, and demo files are present | provenance and closure framing exist |
| Required Phase 2 through 14 artifacts relied on exist | `pass` | approved plans and execution/testing/output families exist | downstream proof seams are inspectable |
| Approved Phase 13 host surfaces exist | `pass` | approved runtime tree includes `embeddable_runtime_api.py`, `local_runner.py`, `local_gateway.py`, `desktop_ui.py`, `product_runtime_shell.py`, and export surfaces | later live-turn proof and desktop demo may anchor to real approved hosts |
| Project-scoped custom-agent setup is reusable | `pass` | `.codex/config.toml` and all required `.codex/agents/*.toml` files exist and match the AGIFCore role rules | no setup blocker |
| Weak current chat path exists in the approved runtime | `non-blocker` | current live turn behavior is a proof-readiness gap on the approved Phase 13 host path, not a Phase 14 prerequisite failure | Phase 15 must explicitly plan repair-and-prove behavior through allowed interfaces |
| Canonical Phase 15 plan file exists | `pass` | this file exists and is the planning target | planning artifact exists |
| Phase 15 planning task surface exists | `pass` | task-card set exists under `00_admin/codex_threads/tasks/phase_15/` | planning-support surface exists |
| Blockers vs non-blockers | `planning not blocked` | prerequisites are satisfied; current chat weakness is a Phase 15 proof-readiness gap rather than a prerequisite mismatch | readiness may be `ready_for_user_review` once this replacement plan is complete |

Required Phase 1 through 14 artifacts relied on:

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
- approved Phase 13 product-runtime baseline and host surfaces
- approved Phase 14 sandbox/profile/scale baseline
- existing project-scoped `.codex` agent package

Dependency gaps:

- no prerequisite blocker exists
- the weak live turn path, terminal-heavy current demo path, and under-specified broad-chat proof shape are in-scope Phase 15 planning gaps that must be explicitly owned here

## 5. Active team map for Phase 15

Later execution default build pod: `Test & Replay Lead`

| Role | Model tier | Status | Why | Exact responsibility this phase | What it must never do this phase |
| --- | --- | --- | --- | --- | --- |
| `Program Governor` | `gpt-5.4` | active | prerequisite truth, setup verification, plan integration, live-turn proof-gap ownership, and final readiness judgment are required | own prerequisite truth, `.codex` verification, role activation, plan integration, artifact matrix, closure map, live-turn proof-gap ownership, and final readiness judgment | implement proof/runtime code, validate its own authored artifacts, or broaden into Phase 16 |
| `Constitution Keeper` | `gpt-5.4-mini` | active | final-proof work and live-turn repair work can quietly turn rhetoric into proof or leak Phase 16 publication semantics | guard no hidden-model drift, no proof laundering, no sidecar responder, no prompt-table patching passed off as intelligence, and no phase-boundary drift | author runtime design alone, approve the phase, or allow release/publication leakage |
| `Source Cartographer` | `gpt-5.4-mini` | active | donor proof/closure substrate and donor open-question/live-demo runtime lineage are real and should not be recreated blindly | map each Phase 15 subsystem, including live-turn repair and real desktop chat demo lineage, to donor basis, disposition, reuse limits, and unresolved seams | invent a fifth disposition, treat donor proof bundles as earned AGIFCore proof, or approve the phase |
| `Architecture & Contract Lead` | `gpt-5.4` | active | Phase 15 needs strict boundaries between proof packs, live-turn repair, real desktop demo, soak, hardening, reproducibility, and closure audit | own subsystem boundaries, allowed Phase 13 and 14 interfaces, forbidden Phase 16 leaks, live-turn repair boundaries, and real-demo contract strategy | redesign earlier phases, collapse all proof work into one opaque harness, create a second runtime, or approve the phase |
| `Kernel Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if a Phase 2 runner/harness seam becomes ambiguous | consult on runner, harness lifecycle, reset, rollback, and replay seams only if ambiguity appears | author the plan, implement code, or broaden Phase 2 |
| `Memory & Graph Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if Phase 4 or 5 retrieval, persistence, graph, or manifest seams become ambiguous in live-turn repair or proof packs | consult on memory continuity, graph anchors, provenance support, and manifest continuity only if ambiguity appears | author the plan, implement code, or reopen memory/graph scope |
| `World & Conversation Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if Phase 7/8/9 conversational/science/expression seams become ambiguous inside broad chat proof | consult on question interpretation, current-world estimate boundaries, planning/comparison/explanation coverage, and broad chat proof boundaries only if ambiguity appears | author the plan, implement code, or absorb Phase 15 into earlier runtime work |
| `Meta & Growth Pod Lead` | `gpt-5.3-codex` | consult-only | only needed if Phase 10/11/12 critique or danger-zone seams become ambiguous in the live-turn proof path | consult on contradiction, weak-answer diagnosis, read-only self-improvement context, and structural-history context only if ambiguity appears | author the plan, implement code, or widen scope into growth redesign |
| `Product & Sandbox Pod Lead` | `gpt-5.3-codex` | consult-only | the revised plan requires an explicit consult on the Phase 13 desktop host seam and Phase 14 budget/sandbox seam | consult on approved Phase 13 host surfaces, desktop UI presentation limits, gateway mediation, and sandbox/profile proof interfaces | author the plan, implement code, reopen Phase 13 or 14 truth, or own correctness in the demo host |
| `Test & Replay Lead` | `gpt-5.4-mini` | active | Phase 15 later executes as the default build pod and now needs explicit live-turn, follow-up, question-class, and desktop-demo proof planning | define the later proof-pack, live-turn, follow-up, current-world, soak, hardening, reproducibility, closure-audit, evidence, and verifier families | author runtime logic in this run, fabricate reports, or approve the phase |
| `Anti-Shortcut Auditor` | `gpt-5.4-mini` | active | proof work and chat-repair work are vulnerable to fake completeness and stitched demo behavior | audit for fake packs, fake chat fixes, prompt-table patches, terminal-only demos passed off as real chat, fake soak, fake hardening, fake reproducibility, fake closure audit, and Phase 16 leakage | rewrite the plan instead of auditing it, downgrade blockers casually, or approve the phase |
| `Merge Arbiter` | `gpt-5.3-codex` | inactive | planning-only run | none | imply closure or perform merge work |
| `Validation Agent` | `gpt-5.4` | active | machine-side review of the planning package is required before user review | validate the planning package after audit and Governor verification exist, with explicit checks for the live-turn repair gap and real desktop chat demo path | author the plan, implement runtime, or approve the phase |
| `Release & Evidence Lead` | `gpt-5.4-mini` | active | later demos and review packets must be inspectable, bounded, and non-terminal for primary user review | define the later final real desktop chat demo, soak-summary, closure-summary, and review-packet structure | implement runtime behavior, publish release material, let terminal debug surfaces stand in for the real demo, or imply acceptance |

## 6. Reuse and provenance strategy

Only the frozen four dispositions are allowed:

- `port_with_provenance`
- `rebuild_clean`
- `adapt_for_research_only`
- `reject`

| Subsystem | Likely inherited source basis | Default disposition | Rationale | Which Phase 1 provenance artifact justifies that decision |
| --- | --- | --- | --- | --- |
| blind packs | `agif_fabric_v2/projects/agif_v2_master/01_plan/PHASE_8C_E4_BLIND_INTELLIGENCE_VERIFICATION_PACK.md`, `FINAL_INTELLIGENCE_REVIEW_RUBRIC.md`, plus AGIFCore `TRACE_CONTRACT.md` and `VALIDATION_PROTOCOL.md` | `port_with_provenance` | the donor lineage already contains real blind-pack discipline, coverage rules, and verifier/evidence expectations; AGIFCore should port that proof structure while binding it to approved Phase 2 through 14 truth | `COMPONENT_CATALOG.md` `CC-056`; `TRACE_CONTRACT.md`; `VALIDATION_PROTOCOL.md` |
| hidden packs | v2 final-intelligence plan/rubric lineage and historical bounded hidden-proof packaging, but without one clean donor package frozen for AGIFCore | `adapt_for_research_only` | hidden-pack lineage exists, but it is not as cleanly frozen as blind-pack lineage; AGIFCore should adapt the idea carefully and rebuild the final hidden-pack design against its own locked proof domains instead of blindly porting historical bundles | `SOURCE_INHERITANCE_MATRIX.md` `SIM-063`; `HUMAN_THINKING_TARGET.md` |
| live-demo pack | `agif_fabric_v2/projects/agif_v2_master/01_plan/PHASE_9_E9_USER_LIVE_DEMO_GATE.md` and the associated v2 live-demo gate lineage | `port_with_provenance` | the donor lineage already defines a governed live-demo inventory, coverage rules, and non-claim boundaries; AGIFCore should port that discipline while binding it to approved Phase 13 runtime and Phase 14 profile truth | `DEMO_PROTOCOL.md`; `TRACE_CONTRACT.md`; `COMPONENT_CATALOG.md` `CC-058` |
| soak harness | `agif_fabric_v1/scripts/check_phase8_soak.py`, `agif_fabric_v1/PROJECT_README.md`, and v2 soak separation in `PHASE_10_MSI_SOAK_RELEASE_HARDENING_AND_PUBLICATION_PLAN.md` | `port_with_provenance` | the donor lineage already contains real soak execution and explicit separation between soak and release/publication work | `COMPONENT_CATALOG.md` `CC-052`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-016` |
| hardening package | v1 hardening passes plus the hardening lane inside v2 Phase 10 release/publication planning | `rebuild_clean` | hardening lineage is real, but the donor package is too entangled with historical publication/release flow; AGIFCore should rebuild a clean internal hardening package tied only to approved Phase 2 through 14 truth | `RUNTIME_REBUILD_MAP.md`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-063` |
| reproducibility package | `agif_fabric_v1/06_outputs/evidence_bundle_manifests/phase9_reproducibility_package.md`, `agif_fabric_v2/projects/agif_v2_master/01_plan/PHASE_8A_REPRODUCIBILITY_PACKAGE.md` | `port_with_provenance` | the donor lineage already defines rerun instructions, expected outputs, and evidence comparison discipline; AGIFCore should port that structure rather than recreate it from zero | `COMPONENT_CATALOG.md` `CC-057`; `SOURCE_INHERITANCE_MATRIX.md` `SIM-021` |
| closure audit | `agif_fabric_v2/projects/agif_v2_master/01_plan/PHASE_8C_E5_FINAL_CLOSURE_AUDIT.md`, `V2_CLOSEOUT_SCOREBOARD.md`, plus AGIFCore `VALIDATION_PROTOCOL.md` | `port_with_provenance` | the donor lineage already contains a real closure-audit pattern and non-claim discipline; AGIFCore should port the audit structure while auditing only AGIFCore-approved artifacts | `VALIDATION_PROTOCOL.md`; `COMPONENT_CATALOG.md` `CC-056`; `COMPONENT_CATALOG.md` `CC-058` |
| live-turn integration repair | approved AGIFCore Phase 13 host/runtime seams plus v2 open-question runtime lineage from `PHASE_9_REAL_RUNTIME_AND_OPEN_QUESTION_INTELLIGENCE_PLAN.md` and `PHASE_9_E8_BLIND_OPEN_QUESTION_VALIDATION.md` | `rebuild_clean` | the current AGIFCore host path already exists, but the weak chat problem cannot be solved by direct donor port or a sidecar responder; AGIFCore should rebuild the live-turn integration layer cleanly on the approved runtime seams while borrowing only reusable proof ideas and no benchmark-coupled behavior | `RUNTIME_REBUILD_MAP.md`; `TRACE_CONTRACT.md`; `COMPONENT_CATALOG.md` rows referenced by the Phase 13 host plan |
| real desktop chat demo host | approved Phase 13 desktop UI adaptation decision in `PHASE_13_PRODUCT_RUNTIME_AND_UX.md` plus donor live-demo/UI pattern lineage recorded there | `adapt_for_research_only` | the desktop host already belongs to Phase 13 and donor UI patterns are useful, but the actual final demo must be rebuilt around approved AGIFCore runtime truth so the UI presents rather than owns correctness | `RUNTIME_REBUILD_MAP.md`; `COMPONENT_CATALOG.md` `CC-060`; Phase 13 reuse decision record |
| gateway/browser support for chat demo | approved Phase 13 local gateway and host-contract lineage recorded in `PHASE_13_PRODUCT_RUNTIME_AND_UX.md` | `adapt_for_research_only` | gateway/browser support may remain useful as a secondary inspection surface, but it must not become a hidden second runtime or replace the canonical desktop UI review host | `COMPONENT_CATALOG.md` rows referenced by the Phase 13 gateway plan; `TRACE_CONTRACT.md` |

## 7. Final-proof and closure-audit boundary rules

### what belongs in live-turn integration repair only

- request-driven intake, interpretation, routing, support-state choice, and answerability behavior on the approved Phase 13 host seam
- typed local retrieval over approved AGIFCore truth buckets
- prior-turn continuity and follow-up binding rules
- broad question-class coverage rules for supported local questions
- current-world grounded-fact and bounded-estimate rules
- per-turn machine-readable phase-usage evidence
- no second runtime tree
- no exact prompt-answer maps
- no regex-only intent patching passed off as intelligence

### what belongs in real desktop chat demo only

- the primary user-review chat host on the approved Phase 13 desktop UI
- a real multi-turn conversation surface
- visible fail-closed states
- visible trace/evidence access paths
- visible proof that the UI is presenting runtime truth rather than inventing its own
- no terminal-only dependence for the primary user review path
- no correctness logic living in the UI

### what stays terminal-only as a secondary debug/proof surface

- secondary shell replay/debug launcher use
- proof/debug inspection commands
- raw JSON inspection helpers
- no requirement that the user use the terminal to perform the primary final demo

### what belongs in blind packs only

- frozen unseen proof cases
- blind-pack inventory and coverage map
- blinded answer capture and scoring surfaces
- blind-pack verifier and machine-readable blind-pack evidence
- no live-demo operator flow
- no release/publication packaging
- no prompt-specific patching after pack freeze

### what belongs in hidden packs only

- reserved proof cases withheld from authoring lanes and live-demo inventory
- hidden-pack exposure-control manifest
- anti-contamination rules
- hidden-pack verifier and machine-readable hidden-pack evidence
- no user-facing demo script
- no public-evidence packaging
- no hidden-pack contents used as patching targets during the same gate

### what belongs in live-demo pack only

- final human-inspectable demo inventory
- operator/demo script
- expected desktop host path plus any secondary inspection path list
- bounded transcript capture
- live-demo verifier and demo evidence
- no blind-pack contents
- no hidden-pack contents
- no soak-only durability data

### what belongs in soak harness only

- duration-class soak runs
- stability, restart, timeout, and fail-closed checks over approved runtime
- soak receipts and soak summaries
- no blind-pack scoring
- no hidden-pack exposure
- no release/publication materials

### what belongs in hardening package only

- issue-family ledger
- fail-closed edge-case checks
- environment and dependency stress checks
- unresolved-finding and waiver ledger
- no public release notes
- no public support claims
- no publication package content

### what belongs in reproducibility package only

- exact rerun commands
- pinned inputs and environment assumptions
- expected artifact list
- hashes and comparison rules
- reproducibility verifier and machine-readable report
- no new proof claims beyond rerunnability

### what belongs in closure audit only

- claim-to-evidence closure matrix
- unresolved blocker list
- closure-audit verifier and machine-readable report
- exact review surface list for the Governor and Validation Agent
- a ready/not-ready package verdict for review preparation only
- no user approval
- no release/publication output

### what is explicitly forbidden to leak in from Phase 16 release/publication behavior

- release notes
- public evidence index
- GitHub/public release asset flow
- tag/release flow
- paper/publication package
- public reproducibility package
- support/handoff publication materials
- browser-hosted/public chat packaging

### how Phase 15 stays separate from Phase 13 product-runtime behavior except through allowed interfaces

Allowed Phase 13 inputs:

- approved runner, gateway, API, desktop UI, shell, and export surfaces
- approved product-runtime demos and receipts
- approved runtime trace/export lanes defined earlier
- approved fail-closed UX and installer/distribution truth

Allowed Phase 13 repair seams later, only if explicitly assigned by Phase 15 task cards:

- `agifcore_phase13_product_runtime/interactive_turn.py`
- `agifcore_phase13_product_runtime/product_runtime_shell.py`
- `agifcore_phase13_product_runtime/embeddable_runtime_api.py`
- `agifcore_phase13_product_runtime/local_gateway.py`
- `agifcore_phase13_product_runtime/desktop_ui.py`

Rules for those inputs:

- Phase 15 may prove the approved Phase 13 runtime through blind, hidden, live-demo, soak, hardening, reproducibility, and closure-audit lanes
- Phase 15 may repair the live-turn path only inside the approved Phase 13 host seam when proof is blocked by shallow fallback behavior
- Phase 15 may not redesign the Phase 13 public runtime contract, host split, UI ownership, or gateway ownership
- Phase 15 may not create a second correctness path outside the approved runtime
- Phase 15 may not let the desktop UI or gateway own correctness, routing truth, or hidden cognition outside approved runtime contracts
- terminal shell may remain a secondary inspection/debug surface only and may not become the primary final demo host

### how Phase 15 stays separate from Phase 14 sandbox/profile/scale behavior except through allowed interfaces

Allowed Phase 14 inputs:

- approved sandbox receipts
- approved Wasmtime limit reports
- approved cell/tissue/profile manifests
- approved active-cell budget reports
- approved dormant-survival reports
- approved Phase 14 demo and review-bundle surfaces

Rules for those inputs:

- Phase 15 may consume Phase 14 artifacts as proof inputs
- Phase 15 may define later proof checks that verify the live-turn path still respects Phase 14 budgets and constraints
- Phase 15 may not modify sandbox policy, profile truth, active-budget rules, or manifest truth
- Phase 15 may not move Phase 14 proof surfaces into release/publication behavior

## 8. Phase 15 budget envelope

Planning ceilings only. These are not achieved measurements.

| Budget item | Planning ceiling | Stop or escalation trigger |
| --- | --- | --- |
| max blind pack count | `<= 6` packs | stop and reopen proof-pack planning if more than `6` blind packs are proposed |
| max hidden pack count | `<= 3` packs | stop if more than `3` hidden packs are proposed in Phase 15 |
| max live-demo pack count | `<= 1` pack | stop if multiple live-demo packs appear; Phase 15 owns one canonical live-demo pack |
| max soak duration classes | `<= 3` classes | stop and simplify if more than `3` soak duration classes are proposed |
| max hardening issue family count | `<= 12` families | stop and consolidate if more than `12` issue families are needed |
| max reproducibility artifact count | `<= 20` artifacts | stop and trim if the reproducibility package needs more than `20` tracked artifacts after adding chat-proof evidence |
| max closure-audit finding count before escalation | `<= 8` open findings | escalate immediately if the closure audit would carry more than `8` unresolved findings |
| max Phase 15 evidence/demo bundle size | `<= 768 MiB` | stop and reorganize outputs if the Phase 15 evidence/demo bundle exceeds `768 MiB` |
| max primary user-facing chat demo hosts | `= 1` primary host | stop if more than one host is treated as the primary user-review chat surface; desktop UI must remain canonical |
| max mandatory terminal-only steps in the primary final demo | `= 0` | stop if the user must use the terminal to complete the primary final demo |

Budget rules:

- these are planning ceilings only
- they are not achieved runtime measurements
- later execution must measure against them directly
- any ceiling breach must stop and escalate instead of widening silently
- any later higher ceiling requires reopened planning first

## 9. Artifact ownership matrix

| Artifact path | Primary author role | Reviewer role | Auditor role | Validator role | Required source inputs | Downstream dependency | Closure evidence expected |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md` | `Program Governor` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 1 provenance package, approved Phase 2 through 14 baselines, Phase 13 host truth, admin controls, donor inspection | all later Phase 15 work | section-complete Phase 15 plan |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | task-card template, model manifest, tool matrix, plan | all later valid Phase 15 work | one planning task card per active role plus the live-turn supplemental notes |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-ACL-02_PHASE_15_LIVE_TURN_AND_CHAT_BOUNDARIES.md` | `Architecture & Contract Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 13 plan/model, Phase 15 plan, donor open-question/live-demo lineage | later live-turn repair workstream | allowed host seams and forbidden chat shortcuts are explicit |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-TRL-04_PHASE_15_LIVE_TURN_ENGINE_AND_CHAT_VERIFICATION_PLAN.md` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 13 host truth, validation protocol, demo protocol, Phase 15 plan, donor open-question runtime proof | later verifier/evidence family | prompt matrix, continuity proof, phase-usage proof, and desktop-demo proof are explicit |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-REL-02_PHASE_15_REAL_DESKTOP_CHAT_DEMO_PLAN.md` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 13 desktop host truth, demo protocol, Phase 15 plan, verification-plan output | later demo bundle and user review path | real desktop chat demo host and review flow are explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_PLAN_FREEZE_HANDOFF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 15 plan and admin controls | later execution start | frozen scope and no-approval status explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_EXECUTION_START_BRIEF.md` | `Program Governor` | `Constitution Keeper` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 15 plan and admin controls | later execution start | execution scope, live-turn repair boundaries, and demo-host rules explicit |
| `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/` | `Test & Replay Lead` | `Product & Sandbox Pod Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 13 baseline, Phase 15 plan, trace contract, product-runtime model | later live-turn repair and real desktop demo | repair remains inside approved host seams and does not create a second runtime |
| `projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/` | `Test & Replay Lead` | `Architecture & Contract Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | approved Phase 13 runtime, approved Phase 14 outputs, Phase 15 plan, provenance package | later proof runtime delivery | blind/hidden/live-demo/soak/hardening/repro/closure modules exist and match the plan |
| `projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/` | `Test & Replay Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | Phase 15 plan, Phase 13 host truth, execution family, validation protocol, demo protocol | later verification and closeout | verifier family exists and covers proof packages plus live-turn proof |
| `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_evidence/` | `Test & Replay Lead` | `Release & Evidence Lead` | `Anti-Shortcut Auditor` | `Validation Agent` | verifier outputs, pack manifests, chat-proof reports, soak receipts, hardening/repro/closure reports | audit and Governor verification | machine-readable evidence bundle is inspectable and includes live-turn proof |
| `projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_demo_bundle/` | `Release & Evidence Lead` | `Program Governor` | `Anti-Shortcut Auditor` | `Validation Agent` | evidence package, demo protocol, validation protocol, approved Phase 13 desktop host, demo scripts | user review | final AGIFCore real desktop chat demo, soak summary, and closure-audit summary exist |
| `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-AUDIT-01_PHASE_15_FINAL_PACKAGE_AUDIT_REPORT.md` | `Anti-Shortcut Auditor` | `Program Governor` | `n/a` | `Validation Agent` | runtime, tests, evidence, demos, planning truth | Governor verification | standard final audit exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_GOVERNOR_VERIFICATION_RECORD.md` | `Program Governor` | `n/a` | `Anti-Shortcut Auditor` | `Validation Agent` | audited files, rerun verifiers, desktop demo bundle, evidence bundle | validation request | direct verification record exists |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_VALIDATION_REQUEST.md` | `Validation Agent` | `Program Governor` | `Anti-Shortcut Auditor` | `n/a` | audited planning or later audited execution package | user review | exact review surfaces and verdict request explicit |
| `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_USER_VERDICT.md` | `User` | `n/a` | `n/a` | `n/a` | validation request and reviewed artifacts | phase gate closeout | explicit user verdict exists |

## 10. Workstream breakdown

| Workstream | Objective | Owner | Supporting roles | Planned outputs | Entry conditions | Exit criteria |
| --- | --- | --- | --- | --- | --- | --- |
| live-turn integration repair planning | define the explicit repair lane for the weak current live-turn path through approved Phase 13 seams only | `Architecture & Contract Lead` | `Program Governor`, `Source Cartographer`, `Product & Sandbox Pod Lead` consult-only | live-turn boundary rules, allowed seam list, anti-sidecar rules | prerequisite truth and reuse map exist | repair scope is explicit without redesigning Phase 13 |
| typed retrieval and follow-up continuity planning | define typed local truth buckets, prior-turn binding rules, and support-diagnostics behavior | `Test & Replay Lead` | `Architecture & Contract Lead`, `Memory & Graph Pod Lead` consult-only, `World & Conversation Pod Lead` consult-only | live-turn verification notes, continuity proof plan, evidence fields | live-turn boundary rules are stable | follow-up continuity and source-selection proof are explicit |
| current-world and bounded-estimate planning | define grounded-fact, bounded-estimate, clarify, and abstain behavior with real target grounding | `Architecture & Contract Lead` | `World & Conversation Pod Lead` consult-only, `Constitution Keeper` | current-world boundary rules, target-grounding rules, estimate honesty rules | live-turn repair lane is defined | current-world proof expectations are explicit and non-fake |
| real desktop chat demo planning | define the canonical real desktop UI chat demo, with the terminal shell demoted to secondary debug/proof use | `Release & Evidence Lead` | `Program Governor`, `Test & Replay Lead`, `Product & Sandbox Pod Lead` consult-only | real desktop chat demo plan, demo bundle shape, review packet order | live-turn verification plan is stable | primary user demo is explicitly non-terminal and inspectable |
| blind/hidden pack planning | define blinded and hidden proof-pack families, coverage rules, contamination controls, and evidence lanes | `Test & Replay Lead` | `Source Cartographer`, `Architecture & Contract Lead`, `Constitution Keeper`, `World & Conversation Pod Lead` consult-only | future blind-pack and hidden-pack execution, verifier, and evidence family | prerequisite truth and reuse map exist | blind/hidden pack boundaries and later verifier surfaces are explicit |
| live-demo and soak planning | define the canonical live-demo inventory and the soak harness duration classes and receipts | `Test & Replay Lead` | `Release & Evidence Lead`, `Kernel Pod Lead` consult-only, `Product & Sandbox Pod Lead` consult-only | future live-demo pack, soak harness, soak summaries, and demo outputs | Phase 13 and Phase 14 interfaces are stable | live-demo, real desktop demo, and soak remain explicit, separate, and inspectable |
| hardening and reproducibility planning | define the internal hardening package and the reproducibility package without Phase 16 leakage | `Architecture & Contract Lead` | `Test & Replay Lead`, `Source Cartographer`, `Constitution Keeper` | future hardening package and reproducibility package families | reuse map and proof-pack boundaries are stable | hardening and reproducibility are explicit, bounded, and non-public |
| closure-audit and review-surface planning | define the closure matrix, claim-to-evidence contract, review-surface rules, and the final review packet | `Program Governor` | `Architecture & Contract Lead`, `Validation Agent`, `Anti-Shortcut Auditor`, `Release & Evidence Lead` | future closure-audit family, validation surfaces, and review handoffs | proof, chat, soak, hardening, and reproducibility boundaries are stable | closure audit is explicit enough to verify later |

## 11. Ordered execution sequence

1. `Program Governor` verifies Phase 14 approval truth and confirms Phase 15 remains `open`.
2. `Program Governor` verifies the reusable `.codex` package and records that no maintenance change is required.
3. `Program Governor` locks active, consult-only, and inactive roles for Phase 15 planning.
4. `Source Cartographer` maps all Phase 15 subsystems, including live-turn repair and real desktop demo host lineage, to donor basis and one allowed disposition.
5. `Architecture & Contract Lead` drafts proof-pack, live-turn repair, desktop host, soak, hardening, reproducibility, and closure-audit boundaries plus allowed Phase 13 and 14 interfaces.
6. `Product & Sandbox Pod Lead` is consulted on the approved Phase 13 host seam and Phase 14 budget/sandbox seam once the first boundary draft exists.
7. `Constitution Keeper` reviews the first-pass Phase 15 draft for hidden-model drift, proof laundering, prompt-table patching risk, terminal-only demo drift, and Phase 16 leakage.
8. `Test & Replay Lead` drafts the future proof/soak/live-turn/evidence family after first-pass reuse and boundary outputs exist.
9. `Release & Evidence Lead` drafts the later real desktop chat demo, soak-summary, closure-summary, and review-packet package after the verification targets stabilize.
10. Other consult-only pod leads are used only if a specific earlier-phase seam becomes ambiguous.
11. `Program Governor` consolidates the plan, task-card set, artifact matrix, budget envelope, closure map, and risk register.
12. `Anti-Shortcut Auditor` audits the full planning package.
13. `Program Governor` independently re-reads the cited files directly and verifies the package.
14. `Validation Agent` prepares the later review request only after audit and Governor verification exist.
15. User review happens only after the validated planning package exists.

Safe parallelism:

- `Source Cartographer` and `Architecture & Contract Lead` may work in parallel on disjoint planning outputs.
- `Constitution Keeper` can review the first-pass draft after boundary outputs exist.
- `Test & Replay Lead` waits for stable reuse, live-turn, and boundary outputs before locking the proof-family decomposition.
- `Release & Evidence Lead` waits for stable verifier and demo-host targets.
- `Merge Arbiter` remains inactive in planning-only work.

## 12. Detailed task cards

### `P15-TC-PG-01`

- role owner: `Program Governor`
- model tier: `gpt-5.4`
- objective: own prerequisite truth, `.codex` verification, canonical Phase 15 plan, role activation, artifact matrix, live-turn proof-gap ownership, budget envelope, closure map, and readiness judgment
- exact files allowed to touch:
  - `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-PG-01_PHASE_15_GOVERNOR_CONTROL.md`
- files forbidden to touch:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 16 and later artifacts
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - `.codex/agents/*`
- required reads first:
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - live phase-truth files
  - Phase 1 provenance package
  - approved Phase 2 through 14 plans and execution surfaces
  - requirements and design files relevant to proof, live-turn repair, desktop demo, soak, hardening, reproducibility, and release boundaries
  - `.codex` setup files
- step-by-step work method:
  1. verify prerequisite truth
  2. verify `.codex` setup contents
  3. lock role activation
  4. explicitly record the weak live-turn path as a Phase 15 proof-readiness gap, not a prerequisite blocker
  5. consolidate reuse, boundary, verifier, demo, and closure outputs
  6. lock artifact families and closure mapping
  7. prepare the package for audit
- required cross-checks:
  - no Phase 16 planning
  - no runtime implementation
  - no approval language
  - no silent mutation of earlier phase truth
  - no fake “chat solved by planning rhetoric” language
- exit criteria:
  - the Phase 15 planning package is section-complete and decision-complete
- handoff target: `Anti-Shortcut Auditor`
- anti-drift rule: do not let planning language imply implementation or approval
- explicit proof that no approval is implied: Phase 15 remains `open`

### `P15-TC-CK-01`

- role owner: `Constitution Keeper`
- model tier: `gpt-5.4-mini`
- objective: guard proof honesty, no hidden-model drift, no Phase 16 leakage, and no fake chat fix disguised as intelligence
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-CK-01_PHASE_15_CONSTITUTION_GUARD.md`
- files forbidden to touch:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md`
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 16 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/SYSTEM_CONSTITUTION.md`
  - `projects/agifcore_master/02_requirements/NON_NEGOTIABLES.md`
  - `projects/agifcore_master/02_requirements/FALSIFICATION_THRESHOLDS.md`
  - `projects/agifcore_master/02_requirements/SCIENTIFIC_METHOD.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - the Phase 15 draft
- step-by-step work method:
  1. check that proof packs are evidence-bound, not prose-bound
  2. check that live-turn repair stays honest and fail-closed instead of becoming a stitched responder
  3. check that the desktop demo is not just a prettier wrapper around weak unsupported behavior
  4. check that no Phase 16 publication behavior leaks in
  5. report any constitutional drift to `Program Governor`
- required cross-checks:
  - no hidden-model loophole
  - no support laundering
  - no silent degrade path
  - no prompt-table patching
  - no terminal-only demo passed off as the primary final demo
  - no Phase 16 behavior
  - no approval language
- exit criteria:
  - constitutional objections are resolved or raised explicitly
- handoff target: `Program Governor`
- anti-drift rule: do not author runtime design or implementation
- explicit proof that no approval is implied: constitutional review is a guardrail, not phase approval

### `P15-TC-SC-01`

- role owner: `Source Cartographer`
- model tier: `gpt-5.4-mini`
- objective: map each Phase 15 subsystem, including live-turn repair and real desktop chat demo lineage, to source basis, disposition, and reuse limits
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-SC-01_PHASE_15_PROVENANCE_AND_REUSE.md`
- files forbidden to touch:
  - `.codex/`
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 16 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
  - approved Phase 2 through 14 plans and execution surfaces
  - donor blind/live-demo/soak/repro/closure files
  - donor open-question runtime and live-demo lineage
- step-by-step work method:
  1. map blind packs, hidden packs, live-demo pack, soak harness, hardening package, reproducibility package, closure audit, live-turn repair, and real desktop chat demo host
  2. assign one allowed disposition to each
  3. flag where inherited contract is stronger than whole-module portability
  4. pass unresolved seams to `Architecture & Contract Lead` and `Program Governor`
- required cross-checks:
  - no fifth disposition
  - no silent omission
  - no donor proof treated as earned AGIFCore proof
  - no donor open-question runtime treated as direct drop-in replacement
- exit criteria:
  - each subsystem has source basis, disposition, and rationale
- handoff target: `Architecture & Contract Lead` then `Program Governor`
- anti-drift rule: do not claim donor code is already valid AGIFCore completion
- explicit proof that no approval is implied: provenance mapping does not earn the phase

### `P15-TC-ACL-01`

- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: own Phase 15 boundaries, allowed Phase 13 and 14 interfaces, live-turn repair rules, forbidden leaks, and the Phase 15 contract strategy
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-ACL-01_PHASE_15_BOUNDARIES_AND_CONTRACTS.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 16 and later artifacts
- required reads first:
  - `projects/agifcore_master/03_design/PUBLIC_RELEASE_MODEL.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
  - `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - approved Phase 13 and Phase 14 plans and outputs
  - `Source Cartographer` output
- step-by-step work method:
  1. define what belongs in each Phase 15 subsystem only
  2. define the live-turn repair lane separately from the proof-pack lanes
  3. define allowed Phase 13 host seams and desktop host rules
  4. define allowed Phase 14 interfaces
  5. define forbidden Phase 16 leaks
  6. pass proof-family implications to `Program Governor` and `Test & Replay Lead`
- required cross-checks:
  - no giant mixed proof harness
  - no release/publication leakage
  - no runtime redesign
  - no second runtime
  - no UI-owned correctness
  - no Phase 16 semantics
- exit criteria:
  - boundary rules are explicit enough to verify later
- handoff target: `Program Governor` then `Test & Replay Lead`
- anti-drift rule: do not redesign earlier phases or the team
- explicit proof that no approval is implied: boundary framing is planning truth only

### `P15-TC-ACL-02`

- role owner: `Architecture & Contract Lead`
- model tier: `gpt-5.4`
- objective: define the exact live-turn repair, host-seam, and real desktop chat demo boundaries for Phase 15
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-ACL-02_PHASE_15_LIVE_TURN_AND_CHAT_BOUNDARIES.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 16 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - donor Phase 9 open-question runtime and live-demo lineage
  - the Phase 15 draft
- step-by-step work method:
  1. define the live-turn repair lane separate from proof-pack execution
  2. define allowed Phase 13 host files and disallowed second-runtime shapes
  3. define desktop UI primary-host rules and terminal secondary-host rules
  4. define what proof artifacts must exist to claim the desktop chat demo is real
- required cross-checks:
  - no sidecar responder
  - no prompt-table fix strategy
  - no terminal-only primary demo
  - no gateway/browser host treated as canonical primary host
- exit criteria:
  - the host seam and demo boundary are decision-complete
- handoff target: `Program Governor` and `Release & Evidence Lead`
- anti-drift rule: do not quietly turn a planning note into runtime design authority outside the approved host seam
- explicit proof that no approval is implied: this note scopes later work only

### `P15-TC-TRL-01`

- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4-mini`
- objective: define the Phase 15 proof, live-turn, soak, hardening, reproducibility, closure-audit, verifier, and evidence family
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-TRL-01_PHASE_15_PROOF_AND_EVIDENCE_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 16 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 14 verifier and evidence families
  - the Phase 15 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` output
- step-by-step work method:
  1. define one verifier family per major Phase 15 subsystem
  2. define the live-turn proof verifier family separately from blind/hidden/demo/soak
  3. define cross-cutting evidence manifests and claim-to-evidence links
  4. define later proof-pack, live-turn, soak, hardening, reproducibility, and closure-audit outputs
  5. define demo hooks for the real desktop demo, soak summary, and closure-audit summary
- required cross-checks:
  - all proof claims must map to machine-readable evidence
  - blind, hidden, live-demo, live-turn repair, soak, hardening, reproducibility, and closure audit must stay separate
  - no soak-only notes passed off as proof
  - no terminal-only demo passed off as the final demo
  - no Phase 16/public release creep
- exit criteria:
  - later testing and evidence path is decision-complete
- handoff target: `Release & Evidence Lead` then `Program Governor`
- anti-drift rule: do not implement runtime behavior through verifier planning
- explicit proof that no approval is implied: verification planning does not earn the phase

### `P15-TC-TRL-04`

- role owner: `Test & Replay Lead`
- model tier: `gpt-5.4-mini`
- objective: define the live-turn engine, broad question-class proof, follow-up continuity proof, selective phase-usage proof, and real desktop chat demo verification plan
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-TRL-04_PHASE_15_LIVE_TURN_ENGINE_AND_CHAT_VERIFICATION_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 16 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - donor Phase 9 open-question runtime proof files
  - the Phase 15 draft
- step-by-step work method:
  1. define the broad prompt matrix across all required question classes
  2. define per-turn evidence fields, including target grounding and actual phases exercised
  3. define follow-up continuity proof requirements
  4. define current-world target-grounding and bounded-estimate proof requirements
  5. define the real desktop chat demo verifier and failure signatures
- required cross-checks:
  - no generic fallback dominating the prompt matrix
  - no over-reported phase usage
  - no exact-prompt-only success criteria
  - no terminal-only demo acceptance path
- exit criteria:
  - live-turn and chat verification plan is decision-complete
- handoff target: `Release & Evidence Lead` and `Program Governor`
- anti-drift rule: do not hide runtime design decisions inside a test plan
- explicit proof that no approval is implied: this is proof planning only

### `P15-TC-ASA-01`

- role owner: `Anti-Shortcut Auditor`
- model tier: `gpt-5.4-mini`
- objective: audit the Phase 15 planning package for fake packs, fake chat fixes, fake soak, fake hardening, fake reproducibility, fake closure audit, and Phase 16 leakage
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-ASA-01_PHASE_15_PLAN_AUDIT.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 16 and later artifacts
- required reads first:
  - full Phase 15 draft
  - `Source Cartographer` output
  - `Architecture & Contract Lead` output
  - `Test & Replay Lead` output
  - relevant approved Phase 13 and Phase 14 truth
- step-by-step work method:
  1. check that all required sections exist
  2. check that each subsystem has source basis and disposition
  3. check that no giant proof harness is being passed off as design
  4. check that no fake chat fix, prompt-table patch, regex-only route list, or terminal-only demo is being passed off as real intelligence proof
  5. check that no approval or completion claim is implied
- required cross-checks:
  - no blind greenfield recreation where donor substrate exists
  - no silent omission of required subsystems
  - no Phase 16 behavior smuggled in
  - no empty pack, chat, soak, hardening, reproducibility, or closure path
- exit criteria:
  - all blockers are cleared or raised explicitly
- handoff target: `Program Governor`
- anti-drift rule: do not rewrite the plan instead of auditing it
- explicit proof that no approval is implied: audit pass is not phase approval

### `P15-TC-VA-01`

- role owner: `Validation Agent`
- model tier: `gpt-5.4`
- objective: validate the final Phase 15 planning package before user review, including the live-turn repair gap and the real desktop demo path
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-VA-01_PHASE_15_VALIDATION_PLAN.md`
  - later `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_15_VALIDATION_REQUEST.md`
- files forbidden to touch:
  - `.codex/`
  - the canonical plan file
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 16 and later artifacts
- required reads first:
  - full Phase 15 draft
  - audit output
  - Governor verification output
  - validation protocol
- step-by-step work method:
  1. confirm the plan is decision-complete
  2. confirm every closure requirement has a later artifact path
  3. confirm later demos are inspectable and truthful
  4. confirm the live-turn repair gap is explicitly owned rather than hand-waved
  5. confirm the primary final demo path is a real desktop UI chat host rather than a terminal-only shell
  6. confirm role separation and review-surface completeness
- required cross-checks:
  - no author/validator collision
  - no missing review surface
  - no implied approval
  - no fake “real chat” claim without a non-terminal host path
- exit criteria:
  - review request scope is exact and inspectable
- handoff target: `Program Governor`
- anti-drift rule: do not author plan content or runtime behavior
- explicit proof that no approval is implied: validation asks for review and does not mark the phase earned

### `P15-TC-REL-01`

- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4-mini`
- objective: define the later Phase 15 demo-bundle shape and review-packet order without leaking Phase 16 behavior
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-REL-01_PHASE_15_DEMO_AND_REVIEW_PACKET_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `04_execution/*`, `05_testing/*`, `06_outputs/*`
  - all Phase 16 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - approved Phase 14 review-bundle structure
  - `Test & Replay Lead` verifier and evidence plan
  - the Phase 15 draft
- step-by-step work method:
  1. define the demo bundle layout
  2. define the real desktop chat final-demo surface
  3. define the soak-summary review surface
  4. define the closure-audit-summary review surface
  5. define the user-review packet order
- required cross-checks:
  - demos must stay inspectable from files alone
  - no demo may imply approval or public release
  - no terminal-only primary demo
  - no Phase 16 packaging creep
- exit criteria:
  - later review packet is exact, ordered, and bounded
- handoff target: `Program Governor` then `Validation Agent`
- anti-drift rule: do not expand into release execution or public claims
- explicit proof that no approval is implied: demo-package planning is not acceptance

### `P15-TC-REL-02`

- role owner: `Release & Evidence Lead`
- model tier: `gpt-5.4-mini`
- objective: define the real desktop chat demo plan as the canonical primary final demo host for Phase 15 user review
- exact files allowed to touch:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-REL-02_PHASE_15_REAL_DESKTOP_CHAT_DEMO_PLAN.md`
- files forbidden to touch:
  - `.codex/`
  - all `04_execution/*`
  - all `05_testing/*`
  - all `06_outputs/*`
  - all Phase 16 and later artifacts
- required reads first:
  - `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `P15-TC-ACL-02_PHASE_15_LIVE_TURN_AND_CHAT_BOUNDARIES.md`
  - `P15-TC-TRL-04_PHASE_15_LIVE_TURN_ENGINE_AND_CHAT_VERIFICATION_PLAN.md`
- step-by-step work method:
  1. define the desktop UI as the canonical primary chat host
  2. define the minimum conversation, trace, evidence, and fail-closed views the user must inspect
  3. define the terminal shell as secondary debug/proof only
  4. define the later script, bundle, and review-order shape for the real desktop chat demo
- required cross-checks:
  - desktop UI stays presentation-only
  - runtime remains the only correctness path
  - no browser-first or terminal-first substitution for the primary final demo
  - no Phase 16/public packaging drift
- exit criteria:
  - the real desktop chat demo plan is decision-complete
- handoff target: `Program Governor` and `Validation Agent`
- anti-drift rule: do not quietly turn the demo plan into host-runtime redesign
- explicit proof that no approval is implied: this is a planning artifact only

## 13. Closure-gate mapping

| Closure requirement | Artifact(s) that will satisfy it later | Role responsible | How it will be checked | What failure would look like |
| --- | --- | --- | --- | --- |
| blind packs exist | `blind_packs/`, `verify_phase_15_blind_packs.py`, `phase_15_blind_pack_report.json` | `Test & Replay Lead` | verifier confirms frozen unseen cases, coverage map, blinded scoring, and evidence receipts | blind packs exist only as labels or cases are exposed to the authoring lane |
| hidden packs exist | `hidden_packs/`, `verify_phase_15_hidden_packs.py`, `phase_15_hidden_pack_report.json` | `Test & Replay Lead` | verifier confirms reserved hidden inventory, exposure controls, and hidden-pack evidence | hidden packs are prose only or duplicate blind/live cases without real secrecy controls |
| live-turn engine exists | `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/interactive_turn.py`, `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/product_runtime_shell.py`, `verify_phase_15_live_turn_engine.py`, `phase_15_live_turn_engine_report.json` | `Test & Replay Lead` | verifier confirms broad question-driven routing, typed retrieval, support-state choice, selective phase usage, and no second runtime | prompts still collapse into one generic fallback or the runtime bypasses approved host seams |
| follow-up continuity exists | `verify_phase_15_follow_up_continuity.py`, `phase_15_follow_up_continuity_report.json` | `Test & Replay Lead` | verifier confirms prior-turn state binding for follow-up prompts like `why`, `what do you mean`, `are you sure`, and `what support is missing` | follow-ups work only for canned phrases or lose prior-turn state entirely |
| current-world target grounding exists | `verify_phase_15_current_world_grounding.py`, `phase_15_current_world_grounding_report.json` | `Test & Replay Lead` | verifier confirms grounded-fact, bounded-estimate, clarify, and abstain behavior varies honestly by target and support | Berlin-style priors are silently reused for unrelated targets or current-world questions always collapse into one answer mode |
| live-demo pack exists | `live_demo_pack/`, `verify_phase_15_live_demo_pack.py`, `phase_15_live_demo_pack_report.json` | `Test & Replay Lead` | verifier confirms one governed final-demo inventory with inspectable demo coverage | live-demo pack is just a note or leaks blind/hidden material |
| real desktop chat demo exists | `run_phase_15_real_desktop_chat_demo.py`, `phase_15_real_desktop_chat_demo.md`, `phase_15_real_desktop_chat_demo.json`, `verify_phase_15_real_desktop_chat_demo.py`, `phase_15_real_desktop_chat_demo_report.json` | `Release & Evidence Lead` with proof inputs from `Test & Replay Lead` | verifier confirms the primary final demo is a real desktop UI host over the approved runtime with visible evidence/trace access | the user must use the terminal to complete the primary final demo or the UI is a fake wrapper over a second responder |
| soak harness exists | `soak_harness/`, `verify_phase_15_soak_harness.py`, `phase_15_soak_summary.json` | `Test & Replay Lead` | verifier confirms real duration-class runs, failure receipts, and soak summaries | soak harness exists only as notes or cannot produce rerunnable summaries |
| hardening package exists | `hardening_package/`, `verify_phase_15_hardening_package.py`, `phase_15_hardening_report.json` | `Test & Replay Lead` | verifier confirms issue-family ledger, fail-closed checks, and unresolved-finding accounting | hardening package exists only as claims or summary prose |
| reproducibility package exists | `reproducibility_package/`, `verify_phase_15_reproducibility.py`, `phase_15_reproducibility_report.json` | `Test & Replay Lead` | verifier confirms exact rerun commands, expected artifacts, hashes, and comparisons | reproducibility exists only as prose with no rerun contract |
| closure audit exists | `closure_audit/`, `verify_phase_15_closure_audit.py`, `phase_15_closure_audit_report.json` | `Test & Replay Lead` | verifier confirms claim-to-evidence closure matrix and unresolved blocker accounting | closure audit exists only as summary text with no matrix or finding ledger |
| demo path exists | full demo family under `06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_demo_bundle/` | `Release & Evidence Lead` | direct demo-bundle inspection and rerunnable demo scripts | no inspectable demo path or unsupported demo claims |
| tests/evidence path exists | full verifier family under `05_testing/phase_15_final_intelligence_proof_and_closure_audit/` and `phase_15_evidence_manifest.json` | `Test & Replay Lead` | Governor rerun plus validation request | missing verifier coverage, missing manifest, or non-machine-readable evidence |

## 14. Demo and validation plan

| Demo | What must exist | Who prepares it | Who audits it | What the user must be able to inspect |
| --- | --- | --- | --- | --- |
| final AGIFCore demo | real desktop UI chat host on the approved Phase 13 runtime, multi-turn conversation, visible fail-closed states, visible trace/evidence access, demo script, and machine-readable desktop-chat demo summary | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and allowed Phase 13 host-seam work | `Anti-Shortcut Auditor` | a real desktop chat conversation, visible evidence/trace path, proof that the desktop host is presenting runtime truth, and proof that the terminal shell is not required for the primary review path |
| soak summary | soak harness, duration-class runs, soak receipts, summary script, and machine-readable soak summary | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` | `Anti-Shortcut Auditor` | soak duration class, failure receipts, restart behavior, and summary evidence |
| closure audit summary | closure-audit matrix, closure-audit report, summary script, and review packet | `Release & Evidence Lead` from outputs produced by `Test & Replay Lead` and `Program Governor` | `Anti-Shortcut Auditor` | claim-to-evidence matrix, unresolved findings, ready/not-ready status, and exact reviewed files |

Validation rules:

- `Validation Agent` prepares the review request only after standard audit and Governor verification exist.
- `Program Governor` is the only role that may ask the user for review.
- Demo surfaces must point to real evidence files and may not ask for approval by summary text alone.
- The primary final demo must be the desktop UI host; terminal shell may only appear as a secondary debug/proof surface.
- If Phase 16 behavior appears during later Phase 15 execution, the correct action is to stop and escalate boundary drift.

## 15. Risk register

| Risk | Detection method | Owner | Escalation trigger | Containment action |
| --- | --- | --- | --- | --- |
| greenfield recreation of reusable proof/closure substrate | compare planned/runtime artifacts against mapped donor files and inherited contracts | `Source Cartographer` | a subsystem is rebuilt from zero despite clear donor basis | stop and reopen reuse mapping before execution |
| one giant proof harness pretending to do blind packs, hidden packs, live-turn repair, soak, hardening, reproducibility, and closure audit | boundary audit and verifier-plan audit | `Architecture & Contract Lead` | one opaque harness is asked to own most Phase 15 behavior | reject the design and split the lanes before continuing |
| prompt-table or regex-only patching passed off as chat intelligence | audit of live-turn plan, later code review, and question-matrix verifier | `Anti-Shortcut Auditor` | broad question behavior depends on exact prompt strings rather than typed interpretation and support | stop and require real request-driven routing |
| blind packs existing only as labels | blind-pack verifier and audit | `Constitution Keeper` | blind-pack names appear without frozen cases, coverage, and scoring receipts | stop and require real blind-pack behavior |
| live-turn repair existing only as a planning label | live-turn verifier and Governor rerun | `Program Governor` | the runtime still collapses broad prompts into generic fallback behavior | stop and require real live-turn evidence before any proof claim |
| follow-up continuity existing only for canned prompts | follow-up continuity verifier | `Test & Replay Lead` | only a few hard-coded follow-ups work while general prior-turn binding fails | stop and require real stateful follow-up behavior |
| source selection collapsing to the same small file set for unrelated questions | source-diversity checks in the live-turn verifier | `Test & Replay Lead` | unrelated question classes keep consulting the same tiny fixed source set | stop and require typed retrieval repair |
| desktop UI owning correctness instead of presenting runtime truth | desktop demo verifier and boundary audit | `Product & Sandbox Pod Lead` consult to `Architecture & Contract Lead` | UI text diverges from runtime trace truth or bypasses approved host contracts | stop and re-separate presentation from correctness |
| terminal shell passed off as the real chat demo | demo audit and review-bundle inspection | `Release & Evidence Lead` | the user must use terminal flow to complete the primary final demo | stop and re-center the desktop host as canonical |
| soak harness existing only as notes | soak verifier and soak-summary audit | `Test & Replay Lead` | soak is described without real duration runs and receipts | stop and require real soak execution |
| hardening package existing only as claims | hardening verifier and audit | `Anti-Shortcut Auditor` | hardening is asserted without issue-family accounting and fail-closed checks | stop and require real hardening evidence |
| reproducibility package existing only as prose | reproducibility verifier and rerun audit | `Test & Replay Lead` | reproducibility exists without exact rerun commands, hashes, and comparisons | stop and require real reproducibility artifacts |
| closure audit existing only as summary text | closure-audit verifier and audit | `Program Governor` | closure audit exists without a claim-to-evidence matrix and unresolved-finding ledger | stop and require a real closure-audit package |
| Phase 15 accidentally absorbing Phase 16 release/publication behavior | boundary audit against the forbidden Phase 16 list | `Release & Evidence Lead` | release notes, public evidence index, public asset flow, tags, browser/public release flows, or publication package content appear in Phase 15 | stop and remove release/publication dependency |

## 16. Approval, commit, and freeze protocol

- this run is planning-only
- no commit now
- no freeze now
- no tag now
- no approval now
- only after the user explicitly says approved may a later separate run commit and freeze the Phase 15 plan artifacts
- after user approval, any future change to the Phase 15 plan requires explicit reopen instruction and a supersession note

## 17. Final readiness judgment

- `ready_for_user_review`

Why:

- Phase 14 is explicitly `approved` in live phase-truth files and corroborated by `DECISIONS.md`.
- Phase 15 remains `open`.
- The required provenance stack, approved Phase 2 through 14 baselines, requirements pack, design pack, admin controls, existing `.codex` setup, approved Phase 13 host surfaces, and donor proof/runtime substrate were reviewed directly.
- No prerequisite blocker was found.
- The weak current live-turn/chat behavior is now explicitly owned as a Phase 15 proof-readiness gap instead of being left implicit.
- The primary final demo host is now explicitly the approved Phase 13 desktop UI, with terminal shell demoted to secondary debug/proof status.
- Hidden-pack lineage remains weaker than blind/live-demo/soak/repro/closure lineage, so the default later execution disposition stays `adapt_for_research_only`.
- Hardening lineage remains too entangled with donor release/publication behavior, so AGIFCore should rebuild that package cleanly.
- This revised package is decision-complete enough for user review without claiming any Phase 15 implementation already exists.
