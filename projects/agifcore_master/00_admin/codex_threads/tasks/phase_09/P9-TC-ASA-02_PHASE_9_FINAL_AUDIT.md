# P9-TC-ASA-02 Phase 9 Final Audit

## Header

- Task Card ID: `P9-TC-ASA-02`
- Phase: `9`
- Title: `Phase 9 Final Audit`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Anti-Shortcut Auditor`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `019d44c0-532f-7953-9b92-43ce5fd3c485`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-PG-02_PHASE_9_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-WCPL-02_PHASE_9_RICH_EXPRESSION_IMPLEMENTATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-TRL-02_PHASE_9_VERIFIERS_AND_EVIDENCE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-ACL-02_PHASE_9_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-REL-02_PHASE_9_DEMO_BUNDLE.md`
  - `projects/agifcore_master/04_execution/phase_09_rich_expression_and_composition/`
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/`
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-TC-ASA-02_PHASE_9_FINAL_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-AUDIT-01_PHASE_9_FINAL_PACKAGE_AUDIT_REPORT.md`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - any handoff file other than the audit report
  - all Phase 10 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p9-tc-pg-02-phase-9-execution-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P9-TC-ASA-02/20260331-0000`

## Objective

- Goal: audit the full built Phase 9 package for fake completeness, giant style-engine collapse, unsupported analogy or composition claims, support laundering, persuasion drift, empty evidence, and Phase 10 or Phase 11 leakage.
- Expected Outputs:
  - this task card
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-AUDIT-01_PHASE_9_FINAL_PACKAGE_AUDIT_REPORT.md`
- Non-Goals:
  - fixing runtime
  - fixing verifiers
  - demo authoring
  - phase approval

## Work Method

1. Read the Phase 9 plan, boundary record, runtime package, verifier family, evidence manifest, and demo bundle.
2. Check that all required Phase 9 surfaces exist and are populated by real outputs.
3. Check for prohibited shortcuts, lane collapse, unsupported analogy or composition claims, support-state upgrades by wording, persuasion drift, empty evidence, and Phase 10 or Phase 11 leakage.
4. Write concrete findings and an explicit pass or blocked judgment for audit only.

## Cross-Checks

- No authoring-role overlap.
- No one giant mixed rich-expression shortcut.
- No unsupported analogy or composition trace claim.
- No support-state upgrade by wording alone.
- No audience-quality lane acting as persuasion.
- No report text accepted without corresponding files.
- No approval implied.

## Exit Criteria

- Audit report is written with concrete file-backed findings.
- Any blocking issue is explicit.
- Handoff target is ready for `Program Governor`.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Audit completion is not phase approval and does not change Phase 9 from `open`.
