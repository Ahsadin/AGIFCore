# Phase 2 Demo Index

## Review Order

1. Start with [Phase 2 Kernel Trace Demo](./phase_02_kernel_trace_demo.md)
2. Then read [Phase 2 Shared Workspace Demo](./phase_02_shared_workspace_demo.md)
3. Then read [Phase 2 Replay Demo](./phase_02_replay_demo.md)
4. Then read [Phase 2 Rollback And Quarantine Demo](./phase_02_rollback_quarantine_demo.md)

## What To Inspect

- Kernel trace demo:
  - trace-anchored event admission and response export
  - evidence paths:
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_kernel_trace_report.json`
- Shared workspace demo:
  - bounded workspace anchors and registry round-trip
  - evidence paths:
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_workspace_state_report.json`
- Replay demo:
  - deterministic replay match and mismatch proof
  - evidence paths:
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_replay_report.json`
- Rollback and quarantine demo:
  - snapshot, quarantine, restore, and fail-closed safety
  - evidence paths:
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_rollback_quarantine_report.json`
    - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_fail_closed_report.json`

## Review Boundary

- Read only the demo files and their linked evidence JSON files.
- Do not treat this bundle as phase approval.
- Phase 2 remains `open`.

## Package Summary

- The demo bundle is evidence-backed and matches the approved Phase 2 planning baseline.
- It is ready for user review, not phase closeout.
