# Phase 6 Execution Start Brief

Use this brief to continue the approved Phase 6 execution-start baseline.

## Phase status

- active phase: `6`
- phase title: `world model and simulator`
- phase gate state: `open`
- plan baseline status: user-provided execution baseline

## Plan path

- `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`

## Full phase scope

Build the full approved Phase 6 scope:

- world-model representation
- entity classes
- target-domain structures
- candidate futures
- what-if simulation
- fault lanes
- pressure lanes
- overload lanes
- conflict lanes
- instrumentation
- usefulness scoring

## Active roles

- `Program Governor`
- `World & Conversation Pod Lead`
- `Architecture & Contract Lead`
- `Test & Replay Lead`

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
- `Release & Evidence Lead`

## Exact allowed files

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/`
- `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/`
- `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/`
- `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_*`
- `projects/agifcore_master/DECISIONS.md`
- `projects/agifcore_master/CHANGELOG.md`
- `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md` only for tiny consistency fixes if strictly required

## Exact forbidden files

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- all Phase 7 and later plan artifacts
- all Phase 7 and later implementation targets
- any Phase 6 user-verdict artifact that marks the phase approved before the user actually approves

## Stop rule

- continue internal build, verify, audit, repair, and merge loops until the whole Phase 6 package is ready for final user review
- stop only when runtime, verifiers, evidence, demos, audit report, governor verification record, and validation request draft all exist
- do not start Phase 7
- do not mark Phase 6 approved

## Approval note

- no approval is implied by internal completion
- only a later explicit user verdict `approved` can earn Phase 6
