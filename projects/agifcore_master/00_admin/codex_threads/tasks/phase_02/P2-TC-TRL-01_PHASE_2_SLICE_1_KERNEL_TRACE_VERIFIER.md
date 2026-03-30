# Task Card

## Header

- Task Card ID: `P2-TC-TRL-01`
- Phase: `2`
- Title: `Slice 1 Kernel Trace Verifier`
- Status: `completed`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Kernel Pod Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `019d3bfd-a950-79a2-87e9-385f914dd614`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_types.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/event_bus.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/verify_phase_02_kernel_trace.py`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_kernel_trace_report.json`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_kernel_trace_demo.md`
- Forbidden Files:
  - all runtime files outside read-only inspection
  - all Phase 2 closeout artifacts
  - all Phase 3+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_02_fabric_kernel_and_workspace/`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/07_assets/`

## Branch And Worktree

- Branch Name: `codex/tc-p2-tc-pg-01-phase-2-governor-control`
- Worktree Path: `governor-controlled same-run startup`
- Rollback Tag Name: `rollback/P2-TC-TRL-01/20260330-0000`

## Objective

- Goal:
  - verify slice-1 event flow and produce starter evidence plus demo outputs
- Expected Outputs:
  - passing kernel-trace verifier
  - machine-readable evidence manifest and report
  - human-inspectable kernel-trace demo markdown
- Non-Goals:
  - replay verification
  - rollback or quarantine verification
  - fail-closed closeout verification
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
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

1. import the slice-1 runtime module directly from the execution folder
2. assert governed event admission, dispatch, and trace export behavior
3. write machine-readable evidence
4. write one human-readable demo surface
5. stop at slice 1 only

## Cross-Checks

- evidence must point to real trace data, not summary text only
- demo must stay inside slice-1 event flow
- verifier must fail loudly if trace anchors or output files are missing

## Exit Criteria

- verifier exits `0`
- evidence report and manifest exist
- demo markdown exists

## Handoff Target

`Program Governor`

## No Approval Implied

Passing this verifier does not approve Phase 2 and does not authorize slice 2.
