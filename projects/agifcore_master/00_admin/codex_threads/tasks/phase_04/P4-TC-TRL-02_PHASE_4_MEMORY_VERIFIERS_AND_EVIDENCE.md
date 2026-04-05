# P4-TC-TRL-02 Phase 4 Memory Verifiers And Evidence

## Header

- Task Card ID: `P4-TC-TRL-02`
- Phase: `4`
- Title: `Phase 4 Memory Verifiers And Evidence`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
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
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
  - approved Phase 2 and Phase 3 verifier families

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_working_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_episodic_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_semantic_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_procedural_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_continuity_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_corrections_and_promotion.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_forgetting_and_compression.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_rollback_safe_updates.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_memory_review.py`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_evidence_manifest.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_working_memory_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_episodic_memory_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_semantic_memory_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_procedural_memory_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_continuity_memory_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_corrections_and_promotion_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_forgetting_and_compression_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_rollback_safe_updates_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_memory_review_report.json`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - demo bundle markdown files until Release & Evidence Lead is activated
  - all Phase 5+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/07_assets/`

## Branch And Worktree

- Branch Name: `codex/tc-p4-tc-trl-02-phase-4-memory-verifiers`
- Worktree Path: `.worktrees/P4-TC-TRL-02`
- Rollback Tag Name: `rollback/P4-TC-TRL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement and run the full Phase 4 verifier family and produce honest machine-readable evidence.
- Expected Outputs:
  - full Phase 4 verifier family
  - full Phase 4 evidence family
- Non-Goals:
  - runtime implementation
  - final demo markdown bundle
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - every `verify_phase_04_*` file under `projects/agifcore_master/05_testing/phase_04_memory_planes/`
- Required Build Commands:
  - `python3` verifier runs only
- Required Verifier Paths:
  - full `verify_phase_04_*` family
- Required Evidence Output Paths:
  - full `phase_04_evidence/` family
- Required Demo Path:
  - handoff to Release & Evidence Lead at end of phase

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-02_PHASE_4_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_USER_VERDICT.md`
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

1. Build one verifier per required Phase 4 surface.
2. Run real checks against the runtime package.
3. Generate machine-readable evidence only from actual verifier results.
4. Keep evidence honest and phase-local.

## Cross-Checks

- No empty reports.
- No report text alone as proof.
- No runtime implementation in this lane.
- No approval implied.
