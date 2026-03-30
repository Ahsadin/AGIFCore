# Task Card

## Header

- Task Card ID: `P2-TC-ASA-01`
- Phase: `2`
- Title: `Phase 2 Execution Audit`
- Status: `completed`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Anti-Shortcut Auditor`
- Supporting Roles: `none`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `019d3bfe-64b7-7412-ad8e-23859c19aa93`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
  - all Phase 2 runtime files
  - all Phase 2 verifier files
  - all Phase 2 evidence files
  - all Phase 2 demo files
  - `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-AUDIT-01_PHASE_2_SLICE_1_AUDIT_REPORT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-AUDIT-02_PHASE_2_EXECUTION_AUDIT_REPORT.md`
- Forbidden Files:
  - all runtime files
  - all testing files
  - all demo files
  - all validation and user-verdict artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p2-tc-pg-01-phase-2-governor-control`
- Worktree Path: `thread-only audit lane`
- Rollback Tag Name: `n/a`

## Objective

- Goal:
  - audit the full Phase 2 execution package for drift, unsupported claims, and missing proof
- Expected Outputs:
  - one slice-1 audit close note
  - one full Phase 2 execution audit report
- Non-Goals:
  - rewriting code
  - approving Phase 2
  - starting Phase 3
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - read-only review of all passed verifier outputs
- Required Build Commands:
  - none
- Required Verifier Paths:
  - all `verify_phase_02_*` files
- Required Evidence Output Paths:
  - all `phase_02_*_report.json` files and `phase_02_evidence_manifest.json`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_demo_index.md`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-AUDIT-02_PHASE_2_EXECUTION_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_02/P2-AUDIT-01_PHASE_2_SLICE_1_AUDIT_REPORT.md`
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
- Merge Arbiter: `inactive`
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

1. check the full package against the frozen Phase 2 plan
2. check that no hidden greenfield rewrite displaced approved reuse
3. check that replay, rollback, quarantine, and fail-closed have real proof paths
4. check that Phase 2 remains open and no approval language leaked in
5. write explicit pass or blocker reports

## Cross-Checks

- no role self-validated its own artifact
- no missing required runtime or verifier file
- no Phase 3 drift

## Exit Criteria

- both audit reports exist and are truthful

## Handoff Target

`Program Governor`

## No Approval Implied

An audit pass is not phase approval.
