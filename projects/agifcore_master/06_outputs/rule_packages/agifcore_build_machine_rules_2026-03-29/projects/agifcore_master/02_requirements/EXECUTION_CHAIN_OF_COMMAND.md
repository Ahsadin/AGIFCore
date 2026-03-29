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

## Fixed Reporting Rule

- specialized roles report findings through the frozen task-card and evidence flow
- Program Governor is the only agent role that turns role output into official project truth below the user
- Program Governor is the only role that may ask the user for final phase review

## Folder Ownership Rule

Folder ownership is frozen in `FOLDER_OWNERSHIP_POLICY.md`.

No role may write outside its owned area unless the Program Governor issues an explicit task card.

## One Active Build Pod Rule

Only one build pod is active by default.

More parallel build pods require:

- explicit Program Governor approval
- disjoint write scopes
- evaluation evidence that the extra coordination cost is justified

## Phase Work Pipeline

Every phase follows this pipeline:

1. Program Governor creates the phase task card
2. Constitution Keeper and Source Cartographer confirm the work is allowed and mapped
3. Architecture & Contract Lead confirms the required contracts and boundaries
4. the active Build Pod Lead implements only the scoped work
5. Test & Replay Lead writes and runs tests, verifiers, and evidence capture
6. Anti-Shortcut Auditor checks claims against files, tests, and evidence
7. Merge Arbiter integrates only cleared patches
8. Program Governor independently reads the relevant code
9. Program Governor independently reruns the required checks and direct sanity paths
10. Program Governor independently verifies the demo path
11. Validation Agent writes the user review request from code, tests, demo, and evidence
12. Program Governor asks the user to review the phase demo
13. the user approves or rejects
14. only then may the phase be marked earned and the next phase begin

## Hard Work Rules

- No patch without a task card naming the exact files and expected outputs.
- No role may claim “done” without tests or evidence when tests or evidence are required.
- No role may bypass provenance, gates, or demos.
- No role may invent public claims beyond the evidence bundle.
- No role may close a phase by summary text alone.

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

## Freeze Rule

No one may change:

- the authority order
- the phase work pipeline
- the user approval requirement
- the runtime separation rule
- the one-active-build-pod default

unless the user explicitly approves a revision.
