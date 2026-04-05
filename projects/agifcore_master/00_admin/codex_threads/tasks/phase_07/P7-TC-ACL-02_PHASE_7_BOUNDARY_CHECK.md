# P7-TC-ACL-02 Phase 7 Boundary Check

## Header

- Task Card ID: `P7-TC-ACL-02`
- Phase: `7`
- Title: `Phase 7 Boundary Check`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles: `Constitution Keeper`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `this_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-ACL-02_PHASE_7_BOUNDARY_CHECK.md`
- Forbidden Files:
  - any runtime, testing, or output file
  - any Phase 8 and later artifact
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p7-tc-wcpl-02-phase-7-conversation-core-implementation`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P7-TC-ACL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: verify that the implemented Phase 7 package stays inside the approved boundaries.
- Expected Outputs:
  - this boundary check record
- Non-Goals:
  - runtime implementation
  - verifier implementation
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `only if donor ambiguity appears`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 7 verifier family after implementation lands
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_07_conversation_core/phase_07_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-AUDIT-01_PHASE_7_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_07_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `Merge Arbiter`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined
