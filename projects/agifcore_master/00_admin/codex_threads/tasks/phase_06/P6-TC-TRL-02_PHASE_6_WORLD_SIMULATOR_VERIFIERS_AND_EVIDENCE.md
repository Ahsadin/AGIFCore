# P6-TC-TRL-02 Phase 6 World Simulator Verifiers And Evidence

## Header

- Task Card ID: `P6-TC-TRL-02`
- Phase: `6`
- Title: `Phase 6 World Simulator Verifiers And Evidence`
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
  - `projects/agifcore_master/01_plan/PHASE_06_WORLD_MODEL_AND_SIMULATOR.md`
  - approved Phase 4 and Phase 5 verifier and evidence surfaces

## Scope Control

- Owned Files:
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/_phase_06_verifier_common.py`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/verify_phase_06_world_model_representation.py`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/verify_phase_06_entity_classes.py`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/verify_phase_06_target_domain_structures.py`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/verify_phase_06_candidate_futures.py`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/verify_phase_06_what_if_simulation.py`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/verify_phase_06_fault_pressure_overload_conflict_lanes.py`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/verify_phase_06_instrumentation.py`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/verify_phase_06_usefulness_scoring.py`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/run_phase_06_causal_simulation_demo.py`
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/run_phase_06_stress_conflict_demo.py`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_evidence_manifest.json`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_world_model_representation_report.json`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_entity_classes_report.json`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_target_domain_structures_report.json`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_candidate_futures_report.json`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_what_if_simulation_report.json`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_fault_pressure_overload_conflict_report.json`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_instrumentation_report.json`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/phase_06_usefulness_scoring_report.json`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - demo bundle markdown files until Release & Evidence Lead is activated
  - all Phase 7+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/`
  - `projects/agifcore_master/06_outputs/phase_06_world_model_and_simulator/phase_06_evidence/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/07_assets/`

## Branch And Worktree

- Branch Name: `codex/tc-p6-tc-trl-02-phase-6-world-simulator-verifiers`
- Worktree Path: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P6-TC-TRL-02`
- Rollback Tag Name: `rollback/P6-TC-TRL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: implement and run the full Phase 6 verifier family and produce honest machine-readable evidence for every required world-model and simulator surface.
- Expected Outputs:
  - full Phase 6 verifier family
  - full Phase 6 evidence family
- Non-Goals:
  - runtime implementation
  - final demo markdown bundle
  - phase approval
- Inherited Lineage Touched: `no`
- Source Cartographer Required: `no`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - every `verify_phase_06_*` file under `projects/agifcore_master/05_testing/phase_06_world_model_and_simulator/`
- Required Build Commands:
  - `python3` verifier runs only
- Required Verifier Paths:
  - full `verify_phase_06_*` family
- Required Evidence Output Paths:
  - full `phase_06_evidence/` family
- Required Demo Path:
  - handoff to Release & Evidence Lead at end of phase

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

1. Build one verifier per required Phase 6 subsystem group.
2. Run real checks against the runtime package.
3. Generate machine-readable evidence only from actual verifier results.
4. Keep evidence honest, phase-local, and inspectable.

## Cross-Checks

- No empty reports.
- No report text alone as proof.
- No runtime implementation in this lane.
- No approval implied.
