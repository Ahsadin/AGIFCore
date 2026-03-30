# Task Card

## Header

- Task Card ID: `P2-TC-TRL-02`
- Phase: `2`
- Title: `Slice 2 Workspace And Registry Verifier`
- Status: `completed`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Kernel Pod Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `019d3bf8-8b40-7912-9225-24d2c7b5d6f6`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/workspace_state.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/cell_registry.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_workspace_state.py`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_workspace_state_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
- Forbidden Files:
  - all runtime files outside read-only inspection
  - all demo bundle markdown files
  - all Phase 2 closeout artifacts
  - all Phase 3+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/`

## Branch And Worktree

- Branch Name: `codex/tc-p2-tc-pg-01-phase-2-governor-control`
- Worktree Path: `governor-controlled same-run phase-2 execution`
- Rollback Tag Name: `rollback/P2-TC-TRL-02/20260330-0000`

## Objective

- Goal:
  - verify shared workspace state, registry anchors, and the bounded memory-hook surface
- Expected Outputs:
  - passing workspace verifier
  - machine-readable workspace evidence report
  - updated aggregate evidence manifest
- Non-Goals:
  - lifecycle verification
  - scheduler verification
  - replay, rollback, quarantine, or fail-closed verification
  - writing demo markdown
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
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

1. import the slice-2 runtime modules directly from the execution folder
2. assert shared workspace exports, registry anchors, and bounded memory hooks
3. fail loudly if any forbidden memory behavior appears
4. update machine-readable evidence only
5. stop at slice 2 only

## Cross-Checks

- workspace exports must preserve conversation and turn anchors
- memory hook surface must be reference-only
- verifier must not write or reshape runtime code

## Exit Criteria

- verifier exits `0`
- workspace evidence report exists
- evidence manifest includes workspace checks

## Handoff Target

`Release & Evidence Lead` then `Program Governor`

## No Approval Implied

Passing this verifier does not approve Phase 2 and does not authorize later slices automatically.
