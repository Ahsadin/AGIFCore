# Phase 13 Execution Start Brief

Use this brief to continue the user-directed Phase 13 execution baseline.

## Phase status

- active phase: `13`
- phase title: `product runtime and ux`
- phase gate state: `open`
- execution baseline status: user-directed build and verification run

## Plan path

- `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md`

## Full phase scope

Build the full approved Phase 13 scope:

- embeddable runtime API
- local runner
- local gateway
- local desktop UI
- state export
- trace export
- memory review export
- safe shutdown
- fail-closed UX
- installer/distribution flow

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

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_13/`
- `projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/`
- `projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/`
- `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_13_*`
- `projects/agifcore_master/DECISIONS.md`
- `projects/agifcore_master/CHANGELOG.md`
- `projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md` only for tiny consistency fixes if strictly required

## Exact forbidden files

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- all Phase 14 and later plan artifacts
- all Phase 14 and later implementation targets
- any Phase 13 user-verdict artifact that marks the phase approved before the user actually approves

## Stop rule

- continue internal build, verify, and demo loops until the whole Phase 13 implementation package is ready for separate audit and validation lanes
- stop only when runtime, verifiers, evidence, demos, and local distribution bundle surfaces are ready
- do not start Phase 14
- do not mark Phase 13 approved

## Approval note

- no approval is implied by internal completion
- only a later explicit user verdict `approved` can earn Phase 13
