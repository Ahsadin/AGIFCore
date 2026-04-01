# P14-TC-ASA-01 Phase 14 Plan Audit

- Task Card ID: `P14-TC-ASA-01`
- Phase: `14`
- Title: `Phase 14 planning-package audit`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Anti-Shortcut Auditor`
- Supporting Roles:
  - `Program Governor`
  - `Validation Agent`
- Allowed Models: `gpt-5.4-mini`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_14/P14-TC-ASA-01_PHASE_14_PLAN_AUDIT.md`
- Forbidden Files:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 15 and later artifacts

## Objective

- Goal: audit the Phase 14 planning package for fake completeness, fake sandboxing, fake manifests, fake budgets, fake dormant proofs, and phase-leak drift
- Expected Outputs:
  - audit findings or pass record
  - explicit blocker list when needed
- Non-Goals:
  - rewriting authored artifacts
  - implementation
  - approval

## Required Reads First

- full Phase 14 draft
- `P14-TC-SC-01` output
- `P14-TC-ACL-01` output
- `P14-TC-TRL-01` output
- relevant approved Phase 3 and Phase 13 truth

## Step-by-Step Work Method

1. Check that all required plan sections exist.
2. Check that each subsystem has source basis and disposition.
3. Check that no giant deployment shell is being passed off as design.
4. Check that no approval or completion claim is implied.

## Required Cross-Checks

- no blind rewrite where plausible substrate exists
- no silent omission of required subsystems
- no Phase 15 or 16 behavior smuggled in
- no empty manifest, budget, or proof path

## Exit Criteria

- all blockers are either cleared or raised explicitly

## Handoff Target

- `Program Governor`

## Anti-Drift Rule

- Do not rewrite the plan instead of auditing it.

## Explicit Proof That No Approval Is Implied

- Audit is not approval and does not earn Phase 14.
