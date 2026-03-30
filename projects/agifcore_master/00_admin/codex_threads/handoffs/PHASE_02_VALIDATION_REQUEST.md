# Phase 2 Validation Request

- Task Card ID: `P2-TC-VA-01`
- Phase: `2`
- Validation Agent: `Validation Agent`
- Date: `2026-03-30`

## What The User Should Review

- Demo Path:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_demo_index.md`
- Exact Behavior To Check:
  - typed event fabric and event bus are present and trace-aligned
  - shared workspace state and registry stay bounded and reference-only
  - lifecycle and scheduler behavior are explicit and inspectable
  - replay, rollback, quarantine, and fail-closed behavior have real proof paths
  - the demo bundle and evidence package stay truthful while Phase 2 remains `open`
- What Good Looks Like:
  - all four demo surfaces exist and point to real JSON evidence
  - the audit report is `pass`
  - the Governor verification record is `ready_for_user_review`
  - the evidence manifest and all seven verifier reports exist on disk
  - Phase 2 still shows `open` in the live gate files
- What Failure Looks Like:
  - a demo file points to missing or mismatched evidence
  - a kernel surface is claimed in demo text without a matching verifier or evidence report
  - replay, rollback, quarantine, or fail-closed proof is missing or only described in prose
  - Phase 2 is presented as approved or complete before the user verdict exists

## Supporting Evidence

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-AUDIT-02_PHASE_2_EXECUTION_AUDIT_REPORT.md`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_02_GOVERNOR_VERIFICATION_RECORD.md`
- Verifier Output Paths:
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_kernel_trace.py`
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_workspace_state.py`
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_lifecycle.py`
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_scheduler.py`
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_replay.py`
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_rollback_quarantine.py`
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_fail_closed.py`
- Evidence JSON Paths:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_kernel_trace_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_workspace_state_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_lifecycle_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_scheduler_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_replay_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_rollback_quarantine_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_fail_closed_report.json`

## Exact Review Surfaces

- `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- `projects/agifcore_master/01_plan/PHASE_INDEX.md`
- `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-AUDIT-02_PHASE_2_EXECUTION_AUDIT_REPORT.md`
- `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_02_GOVERNOR_VERIFICATION_RECORD.md`
- `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_demo_index.md`
- all demo files under `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/`
- `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
- all evidence JSON files under `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/`

## Review Questions

1. Do the four demo surfaces and their linked evidence prove the planned Phase 2 kernel surfaces without drifting into Phase 3?
2. Do the audit report and Governor verification record support the claim that the package is review-ready while Phase 2 remains `open`?
3. Is there any blocker that would prevent Phase 2 from being approved at closeout, or is the package ready for your verdict now?

## Requested User Verdict

- `approved`
- `rejected`
- `approved_with_blockers`

## Gate Note

- Phase 2 remains `open`.
- No approval is implied before the explicit user verdict.
