# Task Card

## Header

- Task Card ID: `P2-TC-KPL-01`
- Phase: `2`
- Title: `Slice 1 Typed Event Fabric And Event Bus`
- Status: `completed`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Kernel Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`, `Test & Replay Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `governor-controlled startup run; no separate KPL session recorded`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
  - `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
  - `projects/agifcore_master/03_design/ARCHITECTURE_OVERVIEW.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_types.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_bus.py`
- Forbidden Files:
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/workspace_state.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/cell_registry.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/lifecycle_engine.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/scheduler.py`
  - all Phase 3+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/`
- Forbidden Folders:
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p2-tc-pg-01-phase-2-governor-control`
- Worktree Path: `governor-controlled same-run startup`
- Rollback Tag Name: `rollback/P2-TC-KPL-01/20260330-0000`

## Objective

- Goal:
  - implement only the typed event fabric and governed event bus needed for slice 1
- Expected Outputs:
  - typed event structures aligned to trace-contract vocabulary
  - synchronous governed event dispatch with trace-export-ready recording
  - bounded queue and payload enforcement aligned to planning ceilings
- Non-Goals:
  - workspace implementation
  - registry implementation
  - lifecycle, scheduler, replay, rollback, quarantine, or fail-closed implementation beyond minimal slice-1 checks
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_kernel_trace.py`
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_kernel_trace.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_kernel_trace_report.json`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_kernel_trace_demo.md`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-AUDIT-01_PHASE_2_SLICE_1_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `n/a`
- Governor Verification Record Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_02_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_02_VALIDATION_REQUEST.md`
- User Verdict Path:
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_02_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path:
  - `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive for slice-1 startup`
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

1. port the strongest typed-event and contract-safe substrate from the approved provenance basis without copying blindly
2. align enumerated event vocabulary to the Phase 1 trace contract
3. implement only the event admission and event dispatch needed for slice 1
4. enforce bounded event size and bounded queue depth
5. leave later subsystems unimplemented

## Cross-Checks

- no new provenance category
- no workspace or registry logic beyond minimal trace-safe placeholders if strictly required
- no phase-close or approval language in code comments or docs

## Exit Criteria

- both runtime files exist
- verifier passes
- evidence and demo starter files are produced by the verifier

## Handoff Target

`Test & Replay Lead` then `Program Governor`

## No Approval Implied

Completing slice-1 runtime code does not approve Phase 2, does not close slice 1 on its own, and does not authorize slice 2.
