# Phase 2 Plan Freeze Handoff

## Freeze status

- Freeze date: `2026-03-30`
- Approved planning baseline for execution start: `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
- Phase gate truth: Phase 2 remains `open`
- Phase 3 status: not started

## Frozen source-of-truth files

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- `projects/agifcore_master/01_plan/PHASE_INDEX.md`
- `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
- `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
- `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md`
- `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
- all files in `projects/agifcore_master/02_requirements/`
- all files in `projects/agifcore_master/03_design/`

## Execution-start role state

### Active now

- `Program Governor`
- `Kernel Pod Lead`
- `Architecture & Contract Lead`
- `Test & Replay Lead`

### Consult only if blocked

- `Constitution Keeper`
- `Source Cartographer`

### Inactive now

- `Memory & Graph Pod Lead`
- `World & Conversation Pod Lead`
- `Meta & Growth Pod Lead`
- `Product & Sandbox Pod Lead`
- `Merge Arbiter`
- `Validation Agent`
- `Release & Evidence Lead`
- `Anti-Shortcut Auditor`

## One-build-pod default

- One active build pod is the default at execution start.
- The only active build pod for slice 1 is `Kernel Pod Lead`.
- No second build pod may start without explicit Program Governor approval.

## First execution slice

Slice 1 scope only:

- typed event fabric
- event bus
- kernel trace verification substrate

Target files:

- `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_types.py`
- `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_bus.py`
- `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_kernel_trace.py`
- starter evidence and demo surfaces under:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/`

## Blocked actions

- do not mark Phase 2 approved
- do not mark Phase 2 complete
- do not start Phase 3
- do not begin slice 2 automatically
- do not implement workspace state, registry, lifecycle, scheduler, replay, rollback, quarantine, or kernel fail-closed beyond minimal slice-1 support interfaces if strictly required
- do not activate a second build pod
- do not open final validation or user closeout artifacts for Phase 2

## Exact success meaning for slice 1

Slice 1 counts as successful only if all of the following are true:

1. `event_types.py` defines typed governed event structures aligned to the Phase 1 trace contract.
2. `event_bus.py` provides governed event admission, handler dispatch, and trace-export-ready event recording.
3. `verify_phase_02_kernel_trace.py` passes directly and verifies the slice-1 event flow.
4. machine-readable evidence is written under `phase_02_evidence/`.
5. a human-inspectable kernel-trace demo surface is written under `phase_02_demo_bundle/`.
6. no Phase 3 behavior is implemented.
7. Phase 2 still remains `open`.

## Next handoff after slice 1

- Program Governor verifies slice-1 files and checks directly.
- Implementation stops at slice 1 packaging.
- The next step is audit preparation, not automatic continuation into slice 2.
