# Task Card

## Header

- Task Card ID: `P2-TC-REL-01`
- Phase: `2`
- Title: `Phase 2 Demo Bundle`
- Status: `completed`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Test & Replay Lead`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `019d3bfc-fb28-7a52-8103-6ca56b416646`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_evidence/phase_02_evidence_manifest.json`
  - all Phase 2 machine-readable evidence reports

## Scope Control

- Owned Files:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_kernel_trace_demo.md`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_shared_workspace_demo.md`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_replay_demo.md`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_rollback_quarantine_demo.md`
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_demo_index.md`
- Forbidden Files:
  - all runtime files
  - all test scripts
  - all Phase 2 closeout artifacts
  - all Phase 3+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`

## Branch And Worktree

- Branch Name: `codex/tc-p2-tc-pg-01-phase-2-governor-control`
- Worktree Path: `governor-controlled same-run phase-2 execution`
- Rollback Tag Name: `rollback/P2-TC-REL-01/20260330-0000`

## Objective

- Goal:
  - convert the machine-readable Phase 2 evidence into the human demo bundle required for review
- Expected Outputs:
  - human-inspectable demo surfaces for kernel trace, shared workspace, replay, and rollback with quarantine
  - one demo index for review order
- Non-Goals:
  - changing runtime behavior
  - changing test logic
  - public release work
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none
- Required Build Commands:
  - none
- Required Verifier Paths:
  - read-only use of all Phase 2 verifier outputs
- Required Evidence Output Paths:
  - read-only use of all Phase 2 evidence JSON files
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_demo_index.md`

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
  - `projects/agifcore_master/06_outputs/phase_02_fabric_kernel_and_workspace/phase_02_demo_bundle/phase_02_demo_index.md`

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

1. read real evidence files only
2. build one markdown demo surface per required user demo
3. build one demo index for review order
4. keep demo text truthful and evidence-backed

## Cross-Checks

- no demo claim without a real evidence file
- no approval language
- no public-release framing

## Exit Criteria

- all demo markdown files exist
- every demo points to a real evidence file
- demo index exists

## Handoff Target

`Program Governor` then `Validation Agent`

## No Approval Implied

Preparing the demo bundle does not approve Phase 2.
