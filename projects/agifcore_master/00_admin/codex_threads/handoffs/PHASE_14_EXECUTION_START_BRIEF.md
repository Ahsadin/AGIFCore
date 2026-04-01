# Phase 14 Execution Start Brief

Use this brief to continue the user-directed Phase 14 execution baseline.

## Phase status

- active phase: `14`
- phase title: `sandbox, profiles, and scale realization`
- phase gate state: `open`
- execution baseline status: user-directed build and verification run

## Plan path

- `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`

## Full phase scope

Build the full approved Phase 14 scope:

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

## Active roles

- `Program Governor`
- `Product & Sandbox Pod Lead`
- `Architecture & Contract Lead`
- `Test & Replay Lead`
- `Release & Evidence Lead`

## Consult-only roles

- `Constitution Keeper`
- `Source Cartographer`
- `Kernel Pod Lead`
- `Memory & Graph Pod Lead`
- `World & Conversation Pod Lead`
- `Meta & Growth Pod Lead`

## Inactive roles

- `Merge Arbiter`
- `Anti-Shortcut Auditor` until the review packet is assembled
- `Validation Agent` until Governor verification is complete

## Exact allowed files

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/`
- `projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/`
- `projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/`
- `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_14_*`
- `projects/agifcore_master/DECISIONS.md`
- `projects/agifcore_master/CHANGELOG.md`
- `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md` only for tiny consistency fixes if strictly required

## Exact forbidden files

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- all Phase 15 and later plan artifacts
- all Phase 15 and later implementation targets
- any Phase 14 user-verdict artifact that marks the phase approved before the user actually approves

## Stop rule

- continue internal build, verify, and demo loops until the whole Phase 14 implementation package is ready for separate audit and validation lanes
- stop only when runtime, verifiers, evidence, and demos are ready
- do not start Phase 15
- do not mark Phase 14 approved

## Approval note

- no approval is implied by internal completion
- only a later explicit user verdict `approved` can earn Phase 14
