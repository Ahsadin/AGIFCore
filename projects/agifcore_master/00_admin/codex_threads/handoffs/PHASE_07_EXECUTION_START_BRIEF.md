# Phase 7 Execution Start Brief

Use this brief to continue the approved Phase 7 execution-start baseline.

## Phase status

- active phase: `7`
- phase title: `conversation core`
- phase gate state: `open`
- plan baseline status: user-provided execution baseline

## Plan path

- `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md`

## Full phase scope

Build the full approved Phase 7 scope:

- raw text intake
- question interpretation
- support-state logic
- self-knowledge surface
- clarification
- utterance planner
- surface realizer
- answer contract
- anti-generic filler guardrails

## Active roles

- `Program Governor`
- `World & Conversation Pod Lead`
- `Architecture & Contract Lead`
- `Test & Replay Lead`
- `Release & Evidence Lead`

## Consult-only roles

- `Constitution Keeper`
- `Source Cartographer`
- `Kernel Pod Lead`
- `Memory & Graph Pod Lead`
- `Product & Sandbox Pod Lead`

## Inactive roles

- `Meta & Growth Pod Lead`
- `Merge Arbiter`
- `Anti-Shortcut Auditor`
- `Validation Agent`

## Exact allowed files

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/`
- `projects/agifcore_master/04_execution/phase_07_conversation_core/`
- `projects/agifcore_master/05_testing/phase_07_conversation_core/`
- `projects/agifcore_master/06_outputs/phase_07_conversation_core/`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_*`
- `projects/agifcore_master/DECISIONS.md`
- `projects/agifcore_master/CHANGELOG.md`
- `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md` only for tiny consistency fixes if strictly required

## Exact forbidden files

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- all Phase 8 and later plan artifacts
- all Phase 8 and later implementation targets
- any Phase 7 user-verdict artifact that marks the phase approved before the user actually approves

## Stop rule

- continue internal build, verify, audit, repair, and review loops until the whole Phase 7 package is ready for final user review
- stop only when runtime, verifiers, evidence, demos, and governor verification are ready
- do not start Phase 8
- do not mark Phase 7 approved

## Approval note

- no approval is implied by internal completion
- only a later explicit user verdict `approved` can earn Phase 7
