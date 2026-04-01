# P14-TC-PG-01 Phase 14 Governor Control

- Task Card ID: `P14-TC-PG-01`
- Phase: `14`
- Title: `Phase 14 Governor control and planning integration`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Program Governor`
- Supporting Roles:
  - `Constitution Keeper`
  - `Source Cartographer`
  - `Architecture & Contract Lead`
  - `Product & Sandbox Pod Lead`
  - `Test & Replay Lead`
  - `Anti-Shortcut Auditor`
  - `Validation Agent`
  - `Release & Evidence Lead`
- Allowed Models: `gpt-5.4`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-PG-01_PHASE_14_GOVERNOR_CONTROL.md`
- Forbidden Files:
  - `projects/agifcore_master/01_plan/MASTER_PLAN.md`
  - all Phase 15 and later artifacts
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - `.codex/agents/*`

## Objective

- Goal: own prerequisite truth, role activation, plan integration, artifact ownership, budget envelope, and readiness judgment for Phase 14
- Expected Outputs:
  - canonical Phase 14 plan
  - planning task-card set
  - locked workstream and closure mapping
- Non-Goals:
  - runtime implementation
  - verifier implementation
  - evidence generation
  - approval or gate mutation

## Required Reads First

- `projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md`
- `projects/agifcore_master/01_plan/PHASE_INDEX.md`
- `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- Phase 1 provenance package
- approved Phase 2 through Phase 13 plans and execution surfaces
- relevant sandbox/deployment/lifecycle requirements and design files
- `.codex/config.toml`
- `.codex/agents/*.toml`

## Step-by-Step Work Method

1. Verify Phase 13 approval and Phase 14 open-state truth.
2. Verify the reusable `.codex` package and note any real maintenance gap.
3. Lock active, consult-only, and inactive roles for Phase 14 planning.
4. Consolidate reuse, boundaries, decomposition, verifier, and demo planning outputs.
5. Lock artifact families, budget envelope, closure map, and risk register.
6. Hand the package to audit only after the plan is decision-complete.

## Required Cross-Checks

- no Phase 15 planning
- no Phase 16 planning
- no runtime implementation
- no approval language
- no mutation of live phase truth

## Exit Criteria

- Phase 14 planning package is section-complete and decision-complete
- task-card set exists for every active role
- readiness can be stated as `ready_for_user_review` without unsupported claims

## Handoff Target

- `Anti-Shortcut Auditor`

## Anti-Drift Rule

- Do not let planning language imply implementation, closure, or approval.

## Explicit Proof That No Approval Is Implied

- This task ends at planning-package readiness only.
- Phase 14 remains `open`.
