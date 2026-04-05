# Task Card

## Header

- Task Card ID: `P16-TC-PG-02`
- Phase: `16`
- Title: `Final Public Baseline Cleanup`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-04-05`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Program Governor`, `Source Cartographer`, `Architecture & Contract Lead`, `Test & Replay Lead`, `Anti-Shortcut Auditor`, `Validation Agent`
- Allowed Models: `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5.3-codex`
- Build Pod Agent Session ID: `role-separated-subagents-required`
- Merge Arbiter Session ID: `not_required_for_packaging_branch`
- Validation Agent Session ID: `role-separated-subagent-required`
- Required Reads:
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
  - `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
  - `projects/agifcore_master/02_requirements/FOLDER_OWNERSHIP_POLICY.md`
  - `projects/agifcore_master/02_requirements/MODEL_TIER_POLICY.md`
  - `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
  - `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
  - `projects/agifcore_master/00_admin/TOOL_PERMISSION_MATRIX.md`
  - `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
  - `projects/agifcore_master/00_admin/ESCALATION_AND_FREEZE_RULES.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`

## Scope Control

- Owned Files:
  - `README.md`
  - `CLAIM_BOUNDARY.md`
  - `ARCHITECTURE.md`
  - `RESULTS.md`
  - `REPRODUCIBILITY.md`
  - `NEXT_STEPS.md`
  - `paper/`
  - `archive/`
  - `projects/agifcore_master/05_testing/final_publication/`
  - `projects/agifcore_master/06_outputs/final_publication/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_16/P16-TC-PG-02_FINAL_PUBLIC_BASELINE_CLEANUP.md`
  - sanitized public-facing publication copies under `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - benchmark definitions
  - threshold definitions
  - runtime behavior files under `projects/agifcore_master/04_execution/`
- Allowed Folders:
  - repo root public docs
  - `archive/`
  - `paper/`
  - `projects/agifcore_master/05_testing/final_publication/`
  - `projects/agifcore_master/06_outputs/final_publication/`
  - `projects/agifcore_master/06_outputs/phase_16_bounded_release_and_publication/`
  - truth files only if wording/path cleanup is required and does not change claim semantics
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - unrelated earlier phase runtime directories

## Branch And Worktree

- Branch Name: `codex/final-public-baseline-cleanup`
- Worktree Path: `not_required`
- Rollback Tag Name: `rollback/P16-TC-PG-02/20260405-0000`

## Objective

- Goal:
  - Prepare AGIFCore for truthful public publication as a bounded intelligence baseline without reopening runtime engineering.
- Expected Outputs:
  - clean root documentation set
  - canonical public-safe evidence set
  - public-safety scan and redaction manifest
  - branch inventory and merge map
  - final paper draft
  - next-project handoff wording aligned to `AGIF + neural hybrid`
  - explicit GitHub-readiness result
- Non-Goals:
  - no new runtime capability work
  - no broad chat claim
  - no AGI claim
  - no benchmark or threshold changes
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `yes`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - `python3 projects/agifcore_master/05_testing/final_publication/verify_publication_safety.py`
- Required Build Commands:
  - `python3 -m py_compile projects/agifcore_master/05_testing/final_publication/verify_publication_safety.py`
- Required Verifier Paths:
  - `projects/agifcore_master/06_outputs/final_publication/publication_safety_report.json`
  - `projects/agifcore_master/06_outputs/final_publication/public_path_redaction_manifest.json`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/final_publication/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/final_publication/final_public_review_bundle/REVIEW_FIRST.md`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/06_outputs/final_publication/PUBLICATION_AUDIT_REPORT.md`
- Extra Audit Report Path: `not_required`
- Governor Verification Record Path: `projects/agifcore_master/06_outputs/final_publication/PUBLICATION_GOVERNOR_VERIFICATION.md`
- Validation Request Path: `projects/agifcore_master/06_outputs/final_publication/PUBLICATION_VALIDATION_REPORT.md`
- User Verdict Path: `not_required_for_cleanup_run`
- Additional Human Demo Checkpoint Path: `not_required`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `not_required_for_packaging_branch`
- Program Governor: `required`
- User: `not required unless push/force-push decision is blocked`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined
