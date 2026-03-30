# Task Card

## Header

- Task Card ID: `P3-TC-ASA-03`
- Phase: `3`
- Title: `Slice 3 Audit`
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-KPL-03_PHASE_3_SLICE_3_SPLIT_MERGE_AND_PROFILE_BUDGETS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-TRL-03_PHASE_3_SLICE_3_SPLIT_MERGE_AND_PROFILE_VERIFIERS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ACL-03_PHASE_3_BOUNDARY_CHECK.md`
  - Slice 3 runtime, verifier, evidence, and boundary-note files when ready

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-ASA-03_PHASE_3_SLICE_3_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-04_PHASE_3_SLICE_3_AUDIT_REPORT.md`
- Forbidden Files:
  - all runtime files
  - all verifier files
  - all output evidence files
  - all Phase 4+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p3-tc-asa-03-phase-3-slice-3-audit`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-ASA-03`
- Rollback Tag Name: `rollback/P3-TC-ASA-03/20260330-0000`

## Objective

- Goal:
  - audit the completed Slice 3 package for scope discipline, task-card alignment, structural correctness, evidence honesty, and boundary accuracy
- Expected Outputs:
  - one explicit pass or blocker report for Slice 3
- Non-Goals:
  - runtime repair
  - verifier repair
  - merge or approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - none authored by audit; rely on Governor rerun evidence
- Required Build Commands:
  - none
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_split_merge.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_profile_budgets.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_split_merge_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_profile_budget_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`
- Required Demo Path:
  - `n/a for Slice 3`

## Handoff Records

- Audit Report Path:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-04_PHASE_3_SLICE_3_AUDIT_REPORT.md`
- Extra Audit Report Path:
  - `n/a`
- Governor Verification Record Path:
  - `deferred until later integration checkpoint`
- Validation Request Path:
  - `deferred until later phase closeout`
- User Verdict Path:
  - `deferred until later phase closeout`
- Additional Human Demo Checkpoint Path:
  - `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `inactive in this run`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- audit result is explicit
- rollback path is defined

## Work Method

1. check Slice 3 scope discipline
2. check task-card alignment and role separation
3. check split/merge and profile-budget structural correctness
4. check evidence honesty and report coherence
5. check boundary-note relevance against the actual Slice 3 runtime
6. write explicit pass or blocker result

## Cross-Checks

- no Slice 4 work
- no Phase 4 drift
- no fake passing evidence
- no second lifecycle state machine
- no profile-budget behavior outside the frozen profile names

## Exit Criteria

- the audit report explicitly states `pass` or `blocked_for_repair` with file-backed reasons

## Handoff Target

`Program Governor`

## No Approval Implied

An audit pass does not approve Phase 3 and does not authorize final closeout.
