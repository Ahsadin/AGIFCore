# Task Card

## Header

- Task Card ID: `P2-TC-KPL-02`
- Phase: `2`
- Title: `Slice 2 Shared Workspace And Registry`
- Status: `completed`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Kernel Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`, `Test & Replay Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `019d3bea-0c4c-75b3-ab4c-ea6b8258df80`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_types.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_bus.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/workspace_state.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/cell_registry.py`
- Forbidden Files:
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/lifecycle_engine.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/scheduler.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/replay_ledger.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/rollback_controller.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/quarantine_controller.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/kernel_fail_closed.py`
  - all test, output, and Phase 3+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/`
- Forbidden Folders:
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p2-tc-pg-01-phase-2-governor-control`
- Worktree Path: `governor-controlled same-run phase-2 execution`
- Rollback Tag Name: `rollback/P2-TC-KPL-02/20260330-0000`

## Objective

- Goal:
  - implement the bounded shared workspace state and governed cell registry for Phase 2
- Expected Outputs:
  - shared workspace export with replay, rollback, quarantine, evidence, and memory-review anchors
  - cell registry with explicit lifecycle and workspace references
  - no semantic or long-term memory behavior
- Non-Goals:
  - lifecycle engine logic
  - scheduler logic
  - replay, rollback, quarantine, or fail-closed control logic
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_workspace_state.py`
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_workspace_state.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_workspace_state_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_shared_workspace_demo.md`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-AUDIT-02_PHASE_2_EXECUTION_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `n/a`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_02_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_02_VALIDATION_REQUEST.md`
- User Verdict Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_02_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_shared_workspace_demo.md`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive unless Governor reopens integration`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined

## Work Method

1. port the strongest shared-workspace and registry substrate from the approved provenance basis without copying blindly
2. keep workspace state bounded and export-safe
3. expose only the allowed memory-hook surface
4. preserve replay, rollback, quarantine, and evidence references as anchors, not full implementations
5. leave lifecycle, scheduler, replay, rollback, quarantine, and fail-closed logic to later slices

## Cross-Checks

- no semantic memory
- no procedural memory
- no reviewed long-term memory
- no graph persistence
- no hidden autonomy channel

## Exit Criteria

- both runtime files exist
- verifier passes
- workspace evidence report exists

## Handoff Target

`Test & Replay Lead` then `Program Governor`

## No Approval Implied

Completing slice 2 runtime code does not approve Phase 2, does not close the phase, and does not authorize Phase 3.
