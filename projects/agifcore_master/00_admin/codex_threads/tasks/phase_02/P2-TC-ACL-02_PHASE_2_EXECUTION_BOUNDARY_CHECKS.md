# Task Card

## Header

- Task Card ID: `P2-TC-ACL-02`
- Phase: `2`
- Title: `Phase 2 Execution Boundary Checks`
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
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/FORMAL_MODELS.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
  - all Phase 2 runtime and verifier files after each slice lands

## Scope Control

- Owned Files:
  - `none; read-only consultation only`
- Forbidden Files:
  - all runtime files
  - all testing files
  - all evidence and demo files
  - all closeout artifacts
- Allowed Folders:
  - `read-only review across projects/agifcore_master/`
- Forbidden Folders:
  - `write access is forbidden in this card`

## Branch And Worktree

- Branch Name: `codex/tc-p2-tc-pg-01-phase-2-governor-control`
- Worktree Path: `thread-only read path`
- Rollback Tag Name: `n/a`

## Objective

- Goal:
  - review slices 2 through 4 for boundary drift before audit
- Expected Outputs:
  - clear boundary findings returned to Program Governor
  - confirmation or rejection of memory-hook, replay, rollback, quarantine, and fail-closed boundaries
- Non-Goals:
  - writing code
  - writing audit or validation artifacts
  - approving Phase 2
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none
- Required Build Commands:
  - none
- Required Verifier Paths:
  - read-only review of all `verify_phase_02_*` files
- Required Evidence Output Paths:
  - read-only review of all `phase_02_*_report.json` files
- Required Demo Path:
  - read-only review of all `phase_02_*_demo.md` files

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

1. inspect each slice after code and verifier outputs exist
2. check memory-hook boundaries remain bounded
3. check replay, rollback, quarantine, and fail-closed surfaces stay inside Phase 2
4. report exact drift findings to Program Governor before audit

## Cross-Checks

- no Phase 3 cell or tissue behavior
- no Phase 4 memory behavior beyond bounded anchors
- runner, gateway, and UI split remains intact

## Exit Criteria

- Program Governor receives clear boundary findings or a clean pass note

## Handoff Target

`Program Governor`

## No Approval Implied

Boundary review is advisory and does not approve Phase 2.
