# Phase 2 Rollback And Quarantine Demo

## Scope

- Covers `rollback_controller.py`, `quarantine_controller.py`, `kernel_fail_closed.py`, `verify_phase_02_rollback_quarantine.py`, and `verify_phase_02_fail_closed.py`.

## What Exists

- `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/rollback_controller.py`
- `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/quarantine_controller.py`
- `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/kernel_fail_closed.py`
- `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_rollback_quarantine.py`
- `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_fail_closed.py`

## What Was Checked

- Rollback creates a bounded snapshot.
- Quarantine contains the unsafe state.
- Restoration returns to a known-good state.
- Fail-closed blocks unsafe continuation and exposes explicit reason codes.

## Evidence

- Evidence manifest: `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
- Replay report: `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_replay_report.json`
- Rollback and quarantine report: `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_rollback_quarantine_report.json`
- Fail-closed report: `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_fail_closed_report.json`

## Result

- Rollback, quarantine, and fail-closed verification passed.

## Boundary Note

- The recovery surface is bounded and explicit.
- It does not expand into Phase 3 cell behavior or Phase 4 memory behavior.

## Gate Note

- Phase 2 remains `open`.
- No phase approval is implied.
