# P9-TC-REL-02 Phase 9 Demo Bundle

## Header

- Task Card ID: `P9-TC-REL-02`
- Phase: `9`
- Title: `Phase 9 Demo Bundle`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Test & Replay Lead`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `019d44be-a10e-7c82-abe4-601cd23246ae`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_09_RICH_EXPRESSION_AND_COMPOSITION.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/`

## Scope Control

- Owned Files:
  - all files under `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/`
- Forbidden Files:
  - any Phase 10 and later artifact
  - any runtime file
  - any verifier file
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`

## Branch And Worktree

- Branch Name: `codex/tc-p9-tc-pg-02-phase-9-execution-control`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore`
- Rollback Tag Name: `rollback/P9-TC-REL-02/20260331-0000`

## Objective

- Goal: package the Phase 9 rich-expression and non-generic chat-quality demos in a directly reviewable form.
- Expected Outputs:
  - runnable demo JSON files
  - matching markdown review surfaces
  - demo index
- Non-Goals:
  - phase approval
  - runtime behavior changes

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/run_phase_09_rich_expression_demo.py`
  - `python3 projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/run_phase_09_non_generic_chat_quality_demo.py`
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_09_rich_expression_and_composition/`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_09_rich_expression_and_composition/phase_09_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_09/P9-AUDIT-01_PHASE_9_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_09_USER_VERDICT.md`
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

## Work Method

1. Package the rich-expression demo from real runtime and verifier outputs.
2. Package the non-generic chat-quality demo from real runtime and verifier outputs.
3. Build matching markdown and JSON review surfaces.
4. Keep every demo claim linked to evidence files.

## Cross-Checks

- No demo may imply phase completion.
- No demo may hide uncertainty or support-state limits behind polished wording.
- No unsupported analogy or composition claim may appear in the packaged demos.
- No public-release packaging creep.

## Exit Criteria

- Demo bundle is directly reviewable and evidence-linked.
- Handoff target is ready for audit and governor verification.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Demo packaging is not phase approval and does not change Phase 9 from `open`.
