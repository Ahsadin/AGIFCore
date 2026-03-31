# P7-TC-ASA-01 Phase 7 Final Audit

## Header

- Task Card ID: `P7-TC-ASA-01`
- Phase: `7`
- Title: `Phase 7 Final Audit`
- Status: `complete`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Anti-Shortcut Auditor`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-PG-02_PHASE_7_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/01_plan/PHASE_07_CONVERSATION_CORE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-WCPL-02_PHASE_7_CONVERSATION_CORE_IMPLEMENTATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-TRL-02_PHASE_7_CONVERSATION_VERIFIERS_AND_EVIDENCE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-ACL-02_PHASE_7_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-REL-02_PHASE_7_DEMO_BUNDLE.md`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/`
  - `projects/agifcore_master/05_testing/phase_07_conversation_core/`
  - `projects/agifcore_master/06_outputs/phase_07_conversation_core/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-TC-ASA-01_PHASE_7_FINAL_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-AUDIT-01_PHASE_7_FINAL_PACKAGE_AUDIT_REPORT.md`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - any handoff file other than the audit report
  - all Phase 8+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p7-tc-pg-03-phase-7-closeout`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P7-TC-ASA-01/20260331-0000`

## Objective

- Goal: audit the full built Phase 7 package for fake completeness, unsupported self-knowledge, one-big-function shortcuts, unverifiable answer-contract claims, anti-filler drift, and later-phase leakage.
- Expected Outputs:
  - this task card
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_07/P7-AUDIT-01_PHASE_7_FINAL_PACKAGE_AUDIT_REPORT.md`
- Non-Goals:
  - fixing runtime
  - fixing verifiers
  - demo authoring
  - phase approval

## Work Method

1. Read the plan, task cards, runtime package, verifier family, evidence manifest, and demo bundle.
2. Check that all required Phase 7 surfaces exist and are populated by real outputs.
3. Check for prohibited shortcuts, empty reports, unsupported self-knowledge, prose-only answer contracts, anti-filler drift, and Phase 8 or Phase 9 leakage.
4. Write concrete findings and an explicit pass or blocked judgment for audit only.

## Cross-Checks

- No authoring-role overlap.
- No one giant mixed conversation shortcut.
- No unsupported self-assertion.
- No prose-only answer-contract claims.
- No report text accepted without corresponding files.
- No approval implied.

## Exit Criteria

- Audit report is written with concrete file-backed findings.
- Any blocking issue is explicit.
- Handoff target is ready for `Program Governor`.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Audit completion is not phase approval and does not change Phase 7 from `open`.
