# Execution Chain Of Command

## Purpose

Freeze the AGIFCore build-machine workflow so every agent knows:

- who owns which kind of work
- how work moves from plan to code to validation
- how phase closure actually happens

## Fixed Authority Order

Authority order is:

1. `User`
2. `Program Governor`
3. specialized frozen roles

Specialized frozen roles include:

- Constitution Keeper
- Source Cartographer
- Architecture & Contract Lead
- the one active Build Pod Lead
- Test & Replay Lead
- Anti-Shortcut Auditor
- Merge Arbiter
- Validation Agent
- Release & Evidence Lead

There is no generic manager/worker approval chain anymore.

The same model family does not mean the same agent.
Build Pod Lead, Merge Arbiter, and Validation Agent must be separate agents, sessions, or threads.

## Fixed Reporting Rule

- specialized roles report findings through the frozen task-card and evidence flow
- Program Governor is the only agent role that turns role output into official project truth below the user
- Program Governor is the only role that may ask the user for final phase review
- every serious pass must reference the active task card id

## Folder Ownership Rule

Folder ownership is frozen in `FOLDER_OWNERSHIP_POLICY.md`.

No role may write outside its owned area unless the Program Governor issues an explicit task card.

## One Active Build Pod Rule

Only one build pod is active by default.

More parallel build pods require:

- explicit Program Governor approval
- disjoint write scopes
- evaluation evidence that the extra coordination cost is justified

Source Cartographer is not a forever-active role.
It is active by default in Phase 0 and Phase 1, and reopens only when inherited lineage is touched again.

## Phase Work Pipeline

Every phase follows this pipeline:

1. Program Governor creates the phase task card and governed branch or worktree
2. Constitution Keeper and Source Cartographer confirm the work is allowed and mapped
3. Architecture & Contract Lead confirms the required contracts and boundaries
4. the active Build Pod Lead implements only the scoped work
5. Test & Replay Lead writes and runs tests, verifiers, and evidence capture
6. Anti-Shortcut Auditor checks claims against files, tests, and evidence
7. Anti-Shortcut Auditor writes the audit report
8. Merge Arbiter integrates only cleared patches
9. Program Governor independently reads the relevant code
10. Program Governor independently reruns the required checks and direct sanity paths
11. Program Governor independently verifies the demo path
12. Program Governor writes the governor verification record
13. Validation Agent writes the user review request from code, tests, demo, and evidence
14. Program Governor asks the user to review the phase demo
15. the user approves or rejects
16. only then may the phase be marked earned and the next phase begin

If the active pod is Meta & Growth Pod Lead, add these mandatory controls:

- one extra audit pass
- stronger Program Governor review
- one additional human demo checkpoint before phase close whenever self-improvement, self-initiated inquiry, or structural growth behavior changes land

## Hard Work Rules

- No patch without a task card naming the exact files and expected outputs.
- No role may claim “done” without tests or evidence when tests or evidence are required.
- No role may bypass provenance, gates, or demos.
- No role may invent public claims beyond the evidence bundle.
- No role may close a phase by summary text alone.
- No role may bypass the tool-permission matrix, branch/worktree policy, or escalation rules.
- Product & Sandbox Pod may not become a dumping ground for unrelated late-phase work.

## Runtime Separation Rule

All of these roles are part of the AGIFCore build machine.

They are not part of the shipped AGIFCore runtime.

This means:

- they may help build AGIFCore
- they may not count as AGIFCore cognition
- they may not count as AGIFCore runtime truth
- they may not be used to fake runtime capability

## Model Escalation Rule

Use the frozen model-tier policy:

- `GPT-5.4 nano` for classify, extract, rank, route, and log triage work
- `GPT-5.4 mini` for well-scoped low-ambiguity tasks
- `GPT-5.3-Codex` for hard implementation, integration, and merge work
- `GPT-5.4` for global judgment, architecture, arbitration, and final validation reading

Exact allowed role-to-model mappings and failover rules are frozen in `00_admin/MODEL_MANIFEST.md`.

## Freeze Rule

No one may change:

- the authority order
- the phase work pipeline
- the user approval requirement
- the runtime separation rule
- the one-active-build-pod default

unless the user explicitly approves a revision.
