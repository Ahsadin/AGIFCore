# P4-TC-PG-02 Phase 4 Execution Control

## Header

- Task Card ID: `P4-TC-PG-02`
- Phase: `4`
- Title: `Phase 4 Execution Control`
- Status: `in_progress`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles: `Memory & Graph Pod Lead`, `Architecture & Contract Lead`, `Test & Replay Lead`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `not_yet_assigned`
- Validation Agent Session ID: `not_yet_assigned`
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

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-PG-02_PHASE_4_EXECUTION_CONTROL.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
  - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_*`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 5+ artifacts
  - any file outside explicitly governed Phase 4 scope
- Allowed Folders:
  - `projects/agifcore_master/00_admin/`
  - `projects/agifcore_master/01_plan/`
- Forbidden Folders:
  - `projects/agifcore_master/07_assets/`
  - any Phase 5+ execution family

## Branch And Worktree

- Branch Name: `codex/tc-p4-tc-pg-01-phase-4-governor-control`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P4-TC-PG-02/<yyyymmdd-hhmm>`

## Objective

- Goal: govern the full Phase 4 execution from freeze through final review readiness without starting Phase 5 or asking for user approval in the middle.
- Expected Outputs:
  - execution task-card set
  - end-of-phase audit path
  - governor verification record
  - validation request draft
  - final user review request
- Non-Goals:
  - direct runtime implementation
  - self-approval
  - Phase 5 planning or execution
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 4 verifier family after integration
- Required Build Commands:
  - scoped Python verifier runs only
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_working_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_episodic_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_semantic_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_procedural_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_continuity_memory.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_corrections_and_promotion.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_forgetting_and_compression.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_rollback_safe_updates.py`
  - `projects/agifcore_master/05_testing/phase_04_memory_planes/verify_phase_04_memory_review.py`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_demo_bundle/`

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

1. Keep Phase 4 `open` while executing the full approved scope.
2. Open and manage separate role lanes for implementation, verification, audit, merge, validation, and release.
3. Stop build work if audit or verifier evidence breaks.
4. Stop only when the full runtime, verifier, evidence, demo, audit, governor verification, and validation package is ready for user review.

## Cross-Checks

- No Phase 5 work.
- No mid-phase user approval request.
- No role validates its own authored artifact.
- No approval implied.
