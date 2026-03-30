# Task Card

## Header

- Task Card ID: `P2-TC-KPL-04`
- Phase: `2`
- Title: `Slice 4 Replay Rollback Quarantine And Fail-Closed`
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
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/workspace_state.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/cell_registry.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/lifecycle_engine.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/scheduler.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/replay_ledger.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/rollback_controller.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/quarantine_controller.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/kernel_fail_closed.py`
- Forbidden Files:
  - all test, output, and Phase 3+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/`
- Forbidden Folders:
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p2-tc-pg-01-phase-2-governor-control`
- Worktree Path: `governor-controlled same-run phase-2 execution`
- Rollback Tag Name: `rollback/P2-TC-KPL-04/20260330-0000`

## Objective

- Goal:
  - implement replay, rollback, quarantine, and fail-closed kernel control for Phase 2
- Expected Outputs:
  - replay ledger with deterministic hash checks
  - bounded rollback snapshots and restore path
  - explicit quarantine control
  - fail-closed refusal decisions with reason codes
- Non-Goals:
  - Phase 3 cell or tissue behavior
  - long-term memory behavior
  - product UI or gateway behavior
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_replay.py`
  - `python3 projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_rollback_quarantine.py`
  - `python3 projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_fail_closed.py`
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_replay.py`
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_rollback_quarantine.py`
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_fail_closed.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_replay_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_rollback_quarantine_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_fail_closed_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_replay_demo.md`

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
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_rollback_quarantine_demo.md`

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

1. port the strongest replay, rollback, and quarantine substrate from the approved provenance basis without copying blindly
2. rebuild kernel fail-closed decisions cleanly with explicit reason codes
3. keep rollback bounded to the approved snapshot ceiling
4. keep quarantine first-class and explicit
5. preserve deterministic replay anchors

## Cross-Checks

- fail-closed must stop unsafe continuation
- replay must compare deterministic anchors, not narrative text
- rollback must restore known-good state rather than partially patch it

## Exit Criteria

- all four runtime files exist
- all three verifiers pass
- replay, rollback and quarantine, and fail-closed evidence reports exist

## Handoff Target

`Test & Replay Lead` then `Program Governor`

## No Approval Implied

Completing slice 4 runtime code does not approve Phase 2 and does not authorize Phase 3.
