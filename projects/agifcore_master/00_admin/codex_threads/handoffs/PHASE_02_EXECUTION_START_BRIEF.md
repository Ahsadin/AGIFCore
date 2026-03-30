# Phase 2 Execution Start Brief

Use this brief to continue the Phase 2 execution start without reopening planning.

## Current truth

- Phase 1 is `approved`
- Phase 2 is `open`
- Phase 2 plan baseline is frozen for execution start
- Phase 3 has not started

## Canonical plan

- `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`

## Execution start roles

- active:
  - `Program Governor`
  - `Kernel Pod Lead`
  - `Architecture & Contract Lead`
  - `Test & Replay Lead`
- consult only if blocked:
  - `Constitution Keeper`
  - `Source Cartographer`
- inactive:
  - `Memory & Graph Pod Lead`
  - `World & Conversation Pod Lead`
  - `Meta & Growth Pod Lead`
  - `Product & Sandbox Pod Lead`
  - `Merge Arbiter`
  - `Validation Agent`
  - `Release & Evidence Lead`
  - `Anti-Shortcut Auditor`

## First execution slice only

Implement only:

- typed event fabric
- event bus
- kernel trace verification substrate

Do not implement:

- workspace state
- cell registry
- lifecycle
- scheduler
- replay
- rollback
- quarantine
- kernel fail-closed
- any Phase 3+ scope

## File targets

- runtime:
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_types.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_bus.py`
- testing:
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_kernel_trace.py`
- outputs:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/`

## Required startup records

Create or maintain these task cards before code changes:

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-TC-PG-01_PHASE_2_GOVERNOR_CONTROL.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-TC-KPL-01_PHASE_2_SLICE_1_TYPED_EVENT_FABRIC_AND_BUS.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-TC-TRL-01_PHASE_2_SLICE_1_KERNEL_TRACE_VERIFIER.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-TC-ACL-01_PHASE_2_SLICE_1_BOUNDARY_CHECK.md`

## Required check

Run:

```bash
python3 projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_kernel_trace.py
```

Expected result:

- exit code `0`
- machine-readable evidence written under `phase_02_evidence/`
- demo markdown written under `phase_02_demo_bundle/`

## Stop condition

After slice 1 is ready:

- stop implementation
- prepare for the next audit step
- do not self-approve
- do not begin slice 2 automatically
