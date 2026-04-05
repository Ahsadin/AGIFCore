# P8-TC-ASA-02 Phase 8 Final Audit

## Header

- Task Card ID: `P8-TC-ASA-02`
- Phase: `8`
- Title: `Phase 8 Final Audit`
- Status: `open`
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-PG-02_PHASE_8_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-WCPL-02_PHASE_8_SCIENCE_WORLD_AWARENESS_IMPLEMENTATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-TRL-02_PHASE_8_VERIFIERS_AND_EVIDENCE.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-REL-02_PHASE_8_DEMO_BUNDLE.md`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/`
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ASA-02_PHASE_8_FINAL_AUDIT.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-AUDIT-01_PHASE_8_FINAL_PACKAGE_AUDIT_REPORT.md`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - any handoff file other than the audit report
  - all Phase 9 and later artifacts
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-wcpl-02-phase-8-science-world-awareness-implementation`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P8-TC-ASA-02/20260331-0000`

## Objective

- Goal: audit the full built Phase 8 package for fake completeness, unsupported exact current-fact claims, prose-only causal chains, fake visible reasoning, empty evidence, and Phase 9 or Phase 10 leakage.
- Expected Outputs:
  - this task card
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-AUDIT-01_PHASE_8_FINAL_PACKAGE_AUDIT_REPORT.md`
- Non-Goals:
  - fixing runtime
  - fixing verifiers
  - demo authoring
  - phase approval

## Work Method

1. Read the Phase 8 plan, boundary record, runtime package, verifier family, evidence manifest, and demo bundle.
2. Check that all required Phase 8 surfaces exist and are populated by real outputs.
3. Check for prohibited shortcuts, empty reports, unsupported current-world claims, prose-only causal chains, fake visible reasoning, and Phase 9 or Phase 10 leakage.
4. Write concrete findings and an explicit pass or blocked judgment for audit only.

## Cross-Checks

- No authoring-role overlap.
- No one giant mixed reasoning shortcut.
- No unsupported exact current-world answer.
- No prose-only causal-chain claim.
- No visible reasoning summary acting as hidden-thought disclosure.
- No report text accepted without corresponding files.
- No approval implied.

## Exit Criteria

- Audit report is written with concrete file-backed findings.
- Any blocking issue is explicit.
- Handoff target is ready for `Program Governor`.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Audit completion is not phase approval and does not change Phase 8 from `open`.
