# Task Card

## Header

- Task Card ID: `P2-TC-ACL-01`
- Phase: `2`
- Title: `Slice 1 Boundary Check`
- Status: `completed`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `019d3bea-0f80-7180-976b-5cb737ce98a0`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/03_design/ARCHITECTURE_OVERVIEW.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_types.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_bus.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-TC-ACL-01_PHASE_2_SLICE_1_BOUNDARY_CHECK.md`
- Forbidden Files:
  - all `04_execution/*`
  - all `05_testing/*`
  - all `06_outputs/*`
  - all Phase 3+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p2-tc-pg-01-phase-2-governor-control`
- Worktree Path: `governor-controlled same-run startup`
- Rollback Tag Name: `rollback/P2-TC-ACL-01/20260330-0000`

## Objective

- Goal:
  - confirm that slice-1 event types and event bus stay inside the approved Phase 2 boundary
- Expected Outputs:
  - boundary notes are reflected in the slice-1 implementation choices
  - no workspace, registry, or memory-plane drift appears
- Non-Goals:
  - architecture redesign
  - new design documents
  - approval or validation
- Inherited Lineage Touched: `no`
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
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/`

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

1. check the runtime file pair against the trace contract and Phase 2 slice-1 boundary
2. confirm no memory-hook overreach
3. confirm no workspace, registry, lifecycle, or scheduler drift
4. report any boundary violation back to the Program Governor immediately

## Cross-Checks

- runner, gateway, and UI split remains untouched
- no hidden Phase 3 scope
- no contract values are silently renamed

## Exit Criteria

- slice-1 runtime files are boundary-safe or explicitly blocked

## Handoff Target

`Program Governor`

## No Approval Implied

This boundary check is a control pass only. It does not approve the phase or the slice.
