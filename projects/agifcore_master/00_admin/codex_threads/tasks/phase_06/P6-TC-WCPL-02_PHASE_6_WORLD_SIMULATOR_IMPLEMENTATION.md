# P6-TC-WCPL-02 Phase 6 World Simulator Implementation

## Header

- Task Card ID: `P6-TC-WCPL-02`
- Phase: `6`
- Title: `Phase 6 World Simulator Implementation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `World & Conversation Pod Lead`
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
  - `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
  - approved Phase 4 and Phase 5 runtime surfaces

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/__init__.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/entity_classes.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/target_domains.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/world_model.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/candidate_futures.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/what_if_simulation.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/fault_lanes.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/pressure_lanes.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/overload_lanes.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/conflict_lanes.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/instrumentation.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/usefulness_scoring.py`
- Forbidden Files:
  - any `projects/agifcore_master/05_testing/*`
  - any `projects/agifcore_master/06_outputs/*`
  - all Phase 7+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/`
- Forbidden Folders:
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`
  - any Phase 7+ execution family

## Branch And Worktree

- Branch Name: `codex/tc-p6-tc-wcpl-02-phase-6-world-simulator-implementation`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P6-TC-WCPL-02`
- Rollback Tag Name: `rollback/P6-TC-WCPL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement the full Phase 6 runtime package with real separated world-model, future, simulation, lane, instrumentation, and usefulness behavior.
- Expected Outputs:
  - all required Phase 6 runtime files
- Non-Goals:
  - verifier implementation
  - evidence generation
  - demo markdown authoring
  - Phase 7 or Phase 8 behavior
  - live transfer execution
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `no` unless provenance ambiguity appears
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - the full Phase 6 verifier family after TRL lands
- Required Build Commands:
  - scoped Python import sanity only if needed
- Required Verifier Paths:
  - full `verify_phase_06_*` family under `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/`
- Required Evidence Output Paths:
  - full `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/` family
- Required Demo Path:
  - full `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_06/P6-AUDIT-01_PHASE_6_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_06_USER_VERDICT.md`
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

1. Build a world model from approved Phase 4 and Phase 5 export state only.
2. Keep entity classes, target-domain structures, candidate futures, simulation, and lane logic as separate verifiable modules.
3. Make every lane read-only, fail-closed, and provenance-linked.
4. Keep instrumentation and usefulness scoring evidence-bound and machine-checkable.
5. Keep Phase 7 and Phase 8 behavior out of the package.

## Cross-Checks

- No one giant undifferentiated state object.
- No candidate-future labels without branching behavior.
- No prose-only fault, pressure, overload, or conflict lanes.
- No usefulness scoring bypass around evidence and instrumentation.
- No Phase 7 or Phase 8 drift.
- No approval implied.
