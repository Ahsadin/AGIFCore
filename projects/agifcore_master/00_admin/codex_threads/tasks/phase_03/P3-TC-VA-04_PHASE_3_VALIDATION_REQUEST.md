# Task Card

## Header

- Task Card ID: `P3-TC-VA-04`
- Phase: `3`
- Title: `Phase 3 Validation Request`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Validation Agent`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `pending_spawn`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `pending_spawn`
- Required Reads:
  - final audited Phase 3 package
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_GOVERNOR_VERIFICATION_RECORD.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-VA-04_PHASE_3_VALIDATION_REQUEST.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_VALIDATION_REQUEST.md`
- Forbidden Files:
  - all runtime files
  - all verifier files
  - all phase-truth files
  - all user verdict files
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-va-04-phase-3-validation-request`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-VA-04`
- Rollback Tag Name: `rollback/P3-TC-VA-04/20260330-0000`

## Objective

- Goal:
  - prepare the final Phase 3 user review request from the audited package
- Expected Outputs:
  - a clear review checklist
  - exact files for the user to inspect
  - exact allowed verdict words
- Non-Goals:
  - approval
  - repairs
  - phase-truth edits

## Completion Checklist

- the request points only to real files
- the request does not claim approval
- the request stops at user review

## No Approval Implied

The validation request asks for review only. It does not approve or close Phase 3.
