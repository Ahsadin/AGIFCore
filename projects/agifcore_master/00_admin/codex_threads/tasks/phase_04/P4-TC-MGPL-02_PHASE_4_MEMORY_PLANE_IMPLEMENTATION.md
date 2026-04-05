# P4-TC-MGPL-02 Phase 4 Memory Plane Implementation

## Header

- Task Card ID: `P4-TC-MGPL-02`
- Phase: `4`
- Title: `Phase 4 Memory Plane Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Memory & Graph Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`
- Allowed Models: `gpt-5.3-codex`
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
  - approved Phase 2 and Phase 3 runtime surfaces

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/working_memory.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/episodic_memory.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/semantic_memory.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/procedural_memory.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/continuity_memory.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/correction_handling.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/promotion_pipeline.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/compression_pipeline.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/forgetting_retirement.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/memory_review.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/rollback_safe_updates.py`
- Forbidden Files:
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - all Phase 5+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/`
- Forbidden Folders:
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`
  - any Phase 5+ execution family

## Branch And Worktree

- Branch Name: `codex/tc-p4-tc-mgpl-02-phase-4-memory-plane-implementation`
- Worktree Path: `.worktrees/P4-TC-MGPL-02`
- Rollback Tag Name: `rollback/P4-TC-MGPL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the full Phase 4 runtime package with real distinct plane behavior and real memory lifecycle behavior.
- Expected Outputs:
  - all required Phase 4 runtime files
- Non-Goals:
  - verifier implementation
  - evidence generation
  - graph implementation
  - conversation implementation
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - the full Phase 4 verifier family after TRL lands
- Required Build Commands:
  - scoped Python import sanity only if needed
- Required Verifier Paths:
  - full `verify_phase_04_*` family
- Required Evidence Output Paths:
  - full `phase_04_evidence/` family
- Required Demo Path:
  - full `phase_04_demo_bundle/`

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

1. Build five distinct memory-plane modules with real differing behavior.
2. Build explicit correction, promotion, compression, forgetting, retirement, review, and rollback-safe update behavior.
3. Keep graph references compatible but do not implement graph logic.
4. Keep conversation behavior out of the runtime.

## Cross-Checks

- No one giant untyped store.
- No fake correction path.
- No fake lifecycle labels without state transitions.
- No Phase 5 work.
- No approval implied.
