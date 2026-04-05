# Task Card

## Header

- Task Card ID: `P3-TC-ASA-05`
- Phase: `3`
- Title: `Phase 3 Final Package Audit`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Anti-Shortcut Auditor`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4-mini`
- Build Pod Agent Session ID: `pending_spawn`
- Merge Arbiter Session ID: `inactive`
- Validation Agent Session ID: `inactive`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - current integrated Phase 3 runtime, testing, evidence, and demo files
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ASA-05_PHASE_3_FINAL_AUDIT.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ASA-05_PHASE_3_FINAL_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-07_PHASE_3_FINAL_PACKAGE_AUDIT_REPORT.md`
- Forbidden Files:
  - all runtime files
  - all verifier files
  - all output evidence and demo files
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-asa-05-phase-3-final-audit`
- Worktree Path: `.worktrees/P3-TC-ASA-05`
- Rollback Tag Name: `rollback/P3-TC-ASA-05/20260330-0000`

## Objective

- Goal:
  - audit the full Phase 3 package for completeness, honesty, and review readiness
- Expected Outputs:
  - one explicit pass or blockers report for the full Phase 3 package
- Non-Goals:
  - repairs
  - approval
  - phase-truth edits

## Verification

- Required Test Commands:
  - none authored by audit; rely on Governor reruns and integrated reports
- Required Verifier Paths:
  - all current `verify_phase_03_*` files on the final integrated lane
- Required Evidence Output Paths:
  - all current Phase 3 evidence reports plus `phase_03_evidence_manifest.json`
- Required Demo Path:
  - full `phase_03_demo_bundle/`

## Completion Checklist

- the audit verdict is explicit
- missing review surfaces are called out if present
- no approval language is used

## No Approval Implied

An audit pass does not approve Phase 3.
