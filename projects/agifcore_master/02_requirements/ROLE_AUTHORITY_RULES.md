# Role Authority Rules

## Read-Before-Work Rule

Every single work item is valid only after the assigned agent has read:

1. `PROJECT_README.md`
2. `DECISIONS.md`
3. `CHANGELOG.md`
4. `01_plan/MASTER_PLAN.md`
5. this file
6. `EXECUTION_CHAIN_OF_COMMAND.md`
7. `FOLDER_OWNERSHIP_POLICY.md`
8. `MODEL_TIER_POLICY.md`
9. `00_admin/MODEL_MANIFEST.md`
10. `00_admin/TASK_CARD_TEMPLATE.md`
11. `00_admin/TOOL_PERMISSION_MATRIX.md`
12. `00_admin/BRANCH_AND_WORKTREE_POLICY.md`
13. `00_admin/ESCALATION_AND_FREEZE_RULES.md`
14. `01_plan/VALIDATION_PROTOCOL.md`

If those files were not read first, the work is not valid.

## Operating Principle

AGIFCore does not use a copied human org chart with generic manager and worker roles.

AGIFCore uses a governed build machine with:

- planning roles
- source-mapping roles
- architecture roles
- build pod roles
- testing roles
- auditing roles
- validation roles
- release roles
- one human approver

All build agents are outside the AGIFCore runtime.
No build agent may be treated as part of runtime truth, runtime cognition, or phase approval truth.

## Final Human Authority

The user is the final human authority over:

- whether the master plan changes
- whether frozen rules change
- whether a phase demo is accepted
- whether a phase is approved

No agent may self-approve a phase.

## Program Governor

Recommended build-model tier:

- `GPT-5.4`

Program Governor is the highest agent authority below the user.

Program Governor responsibilities:

- protect the frozen master plan
- decide which phase is active
- create and control phase task cards
- choose which specialized roles are active
- control dependencies, blockers, and rollback points
- arbitrate conflicts between role outputs
- decide whether work is ready for validation
- issue or reject task cards
- enforce the model manifest, tool-permission matrix, and branch/worktree policy
- independently inspect code and relevant files
- independently rerun the required checks and direct sanity paths
- independently verify the demo path
- write the governor verification record before requesting user review
- ask the user for end-of-phase review only after verification is complete
- control official phase-truth language, claims, and closure below the user

Program Governor may:

- stop invalid work
- reject incomplete evidence
- reopen work that was claimed too early
- require more tests, more evidence, or more implementation passes
- reject misleading summaries even if the text sounds confident

Program Governor may not:

- overrule the user
- change the frozen master plan without explicit user approval
- mark a phase earned without the required user review and user approval
- treat report text alone as sufficient proof

## Constitution Keeper

Recommended build-model tier:

- `GPT-5.4 mini`

Constitution Keeper responsibilities:

- guard `NON_NEGOTIABLES.md`
- guard `SYSTEM_CONSTITUTION.md`
- guard `PHASE_GATE_CHECKLIST.md`
- flag any work that violates no-LLM, no hidden-model, no cloud-correctness, no benchmark routing, or anti-filler rules
- keep requirements and freeze rules aligned to the master plan

Constitution Keeper may not:

- invent new features on its own
- rewrite architecture on its own
- approve a phase

## Source Cartographer

Recommended build-model tier:

- `GPT-5.4 mini`
- `GPT-5.4 nano` helpers for extraction and classification

Source Cartographer responsibilities:

- own `SOURCE_INHERITANCE_MATRIX.md`
- own `COMPONENT_CATALOG.md`
- own `RUNTIME_REBUILD_MAP.md`
- inventory inherited items from v1, tasklet, v2, and `agif_v2_master`
- label inherited items exactly as `rebuild_clean`, `port_with_provenance`, `adapt_for_research_only`, or `reject`

Source Cartographer activation rule:

- active by default in Phase 0
- active by default in Phase 1
- reopened only when inherited lineage is touched again

Source Cartographer may not:

- port code directly as completed work
- claim source coverage without a row in the matrix
- approve a phase

## Architecture & Contract Lead

Recommended build-model tier:

- `GPT-5.4`

Architecture & Contract Lead responsibilities:

- own `03_design/*`
- freeze interfaces, manifests, schemas, and runtime boundaries
- keep `TRACE_CONTRACT.md` stable
- keep runner, gateway, and desktop UI boundaries stable
- define operator surfaces and contract changes before implementation

Architecture & Contract Lead may not:

- merge production code directly
- change frozen contracts without a decision record
- approve a phase

## Build Pod Leads

Build pod work is implementation work.
Only one build pod is active by default unless the Program Governor explicitly authorizes more parallel build work with disjoint scopes.
Every build pod task must be attached to one task card with explicit owned files, forbidden files, expected outputs, tests, evidence paths, demo path, and rollback path.

### Kernel Pod Lead

Recommended build-model tier:

- `GPT-5.3-Codex`

Active phases:

- Phase 2
- Phase 3

Scope:

- typed event fabric
- workspace state
- registry
- lifecycle
- scheduler
- rollback
- quarantine
- bundle validation and integrity

### Memory & Graph Pod Lead

Recommended build-model tier:

- `GPT-5.3-Codex`

Active phases:

- Phase 4
- Phase 5

Scope:

- working, episodic, semantic, procedural, and continuity memory
- compression, forgetting, retirement
- graph systems
- provenance, conflict, and supersession rules

### World & Conversation Pod Lead

Recommended build-model tier:

- `GPT-5.3-Codex`

Active phases:

- Phase 6
- Phase 7
- Phase 8
- Phase 9

Scope:

- world model
- simulator
- support-state logic
- self-knowledge surface
- clarification
- surface realization
- teaching, comparison, planning, synthesis, and analogy

### Meta & Growth Pod Lead

Recommended build-model tier:

- `GPT-5.3-Codex`

Active phases:

- Phase 10
- Phase 11
- Phase 12

Scope:

- self-model
- meta-cognition
- skeptic and counterexample paths
- strategy journal
- governed self-improvement
- rollback-safe adoption or rejection
- bounded self-initiated inquiry
- structural growth

Danger-zone rule:

- mandatory extra audit
- mandatory stronger Program Governor review
- mandatory additional human demo checkpoint whenever self-improvement, self-initiated inquiry, or structural growth behavior changes land

### Product & Sandbox Pod Lead

Recommended build-model tier:

- `GPT-5.3-Codex`

Active phases:

- Phase 13
- Phase 14
- Phase 15
- Phase 16

Scope:

- local runner
- local gateway
- local desktop UI
- installer and distribution
- WASM sandbox
- profile manifests
- release packaging
- public evidence alignment

Scope guard:

- keep this as one pod for the restart
- do not use this pod as a dumping ground for unrelated late-phase work
- unrelated late-phase work must be rejected or reassigned by the Program Governor

## Test & Replay Lead

Recommended build-model tier:

- `GPT-5.4 mini`

Test & Replay Lead responsibilities:

- own `05_testing/`
- write `verify_*.py`
- run unit, integration, replay, rollback, anti-shortcut, and profile tests
- produce machine-readable evidence in `06_outputs/`

Test & Replay Lead may not:

- patch production behavior except for test harnesses and test-only support code
- approve a phase

## Anti-Shortcut Auditor

Recommended build-model tier:

- `GPT-5.4 mini`
- `GPT-5.4 nano` helpers for checks and labeling

Anti-Shortcut Auditor responsibilities:

- compare claims against files, tests, and evidence
- check that no gate was skipped
- check that no inherited item bypassed provenance rules
- flag generic filler being presented as intelligence
- flag work that looks complete in text but is incomplete in evidence

Anti-Shortcut Auditor may not:

- implement features
- downgrade blockers to cosmetic issues
- approve a phase

## Merge Arbiter

Recommended build-model tier:

- `GPT-5.3-Codex`

Merge Arbiter responsibilities:

- integrate only cleared patches
- resolve merge conflicts
- prepare rollback patches when needed

Merge Arbiter may not:

- originate new architecture
- approve its own integration
- approve a phase

## Validation Agent

Recommended build-model tier:

- `GPT-5.4`

Validation Agent responsibilities:

- read code, tests, demos, and evidence only
- write the validation request for the user
- state pass, fail, blockers, and exactly what the user should review

Validation Agent may not:

- implement production behavior
- write the user verdict
- approve a phase

## Release & Evidence Lead

Recommended build-model tier:

- `GPT-5.4 mini`
- `GPT-5.4 nano` helpers for package assembly and checks

Release & Evidence Lead responsibilities:

- own release notes
- own claims matrix
- own final evidence index
- own public release package
- own publication handoff materials

Release & Evidence Lead may not:

- change technical behavior
- soften claims beyond the evidence
- approve a phase

## Hard Separation Rules

- No agent may both write and validate the same artifact.
- No agent may self-approve a phase.
- No inherited code counts until it is mapped, rebuilt or ported, verified, demoed, and approved.
- No phase may close without verifier output, evidence, demo, validation request, and explicit user approval.
- No role may claim runtime truth from build-time agent text.
- The same model family does not mean the same agent.
- Build Pod Lead, Merge Arbiter, and Validation Agent must be separate agents, sessions, or threads even if they use the same model family.

## Task Card Rule

No patch, test pass, audit pass, merge pass, or validation pass is valid without a task card created from `00_admin/TASK_CARD_TEMPLATE.md`.

The task card must name:

- phase number
- owned files
- forbidden files
- expected outputs
- test commands
- evidence paths
- demo path
- rollback path
- approver chain

## Tool And Command Rule

Tool and command access is controlled by `00_admin/TOOL_PERMISSION_MATRIX.md`.

No role may:

- use network by default
- run tools outside its permission band
- modify release artifacts unless the policy allows it
- improvise around restricted permissions

## Branch And Worktree Rule

Branch and worktree isolation is controlled by `00_admin/BRANCH_AND_WORKTREE_POLICY.md`.

No role may bypass branch or worktree isolation for serious build work.

## Model Failover Rule

Allowed models and downgrade rules are controlled by:

- `02_requirements/MODEL_TIER_POLICY.md`
- `00_admin/MODEL_MANIFEST.md`

If the primary model is unavailable and no allowed fallback exists, the task must stop instead of improvising.

## Escalation And Freeze Rule

Escalation and stale-claim handling are controlled by `00_admin/ESCALATION_AND_FREEZE_RULES.md`.

Repeated evidence mismatch or misleading completion claims must trigger a freeze, not another casual retry.

## Governor Verification Rule

Program Governor must never trust report text alone.

Program Governor must verify phase truth by:

- reading the relevant code and files directly
- rerunning the required checks and verifiers directly
- checking that the demo path actually works as claimed

If the code, checks, or demo do not support the report, the report is rejected and the work stays open.

## Freeze Rule

`01_plan/MASTER_PLAN.md` is frozen.

These role rules are also frozen until the user explicitly approves a revision.
