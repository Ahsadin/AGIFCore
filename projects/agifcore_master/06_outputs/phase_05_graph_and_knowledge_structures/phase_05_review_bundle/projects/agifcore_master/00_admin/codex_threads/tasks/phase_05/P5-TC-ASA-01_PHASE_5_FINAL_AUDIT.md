# P5-TC-ASA-01 Phase 5 Final Audit

## Header

- Task Card ID: `P5-TC-ASA-01`
- Phase: `5`
- Title: `Phase 5 Final Audit`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Anti-Shortcut Auditor`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-PG-02_PHASE_5_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-MGPL-01_PHASE_5_GRAPH_IMPLEMENTATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-TRL-01_PHASE_5_GRAPH_VERIFIERS_AND_EVIDENCE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-ACL-01_PHASE_5_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/`
  - `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-ASA-01_PHASE_5_FINAL_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-AUDIT-01_PHASE_5_FINAL_PACKAGE_AUDIT_REPORT.md`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - any handoff file other than the audit report
  - all Phase 6+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p5-tc-asa-01-phase-5-final-audit`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P5-TC-ASA-01`
- Rollback Tag Name: `rollback/P5-TC-ASA-01/<yyyymmdd-hhmm>`

## Objective

- Goal: audit the full built Phase 5 package for fake completeness, silent omission, unsupported claims, greenfield drift, and later-phase leakage.
- Expected Outputs:
  - this task card
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-AUDIT-01_PHASE_5_FINAL_PACKAGE_AUDIT_REPORT.md`
- Non-Goals:
  - fixing runtime
  - fixing verifiers
  - demo authoring
  - phase approval

## Work Method

1. Read the plan, task cards, runtime package, verifier family, evidence manifest, and demo bundle.
2. Check that all required Phase 5 surfaces exist and are populated by real outputs.
3. Check for prohibited shortcuts, empty reports, unverifiable claims, and Phase 6 or 7 leakage.
4. Write concrete findings and an explicit pass or blocked judgment for audit only.

## Cross-Checks

- No authoring-role overlap.
- No one giant graph shortcut.
- No prose-only provenance, conflict, or supersession claims.
- No report text accepted without corresponding files.
- No approval implied.

## Exit Criteria

- Audit report is written with concrete file-backed findings.
- Any blocking issue is explicit.
- Handoff target is ready for `Program Governor`.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Audit completion is not phase approval and does not change Phase 5 from `open`.
