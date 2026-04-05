# P15-TC-ASA-01 Phase 15 Plan Audit

- Task Card ID: `P15-TC-ASA-01`
- Phase: `15`
- Title: `Phase 15 planning-package audit`
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-ASA-01_PHASE_15_PLAN_AUDIT.md`
- Forbidden Files:
  - `.codex/`
  - `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 16 and later artifacts

## Objective

- Goal: audit the Phase 15 planning package for fake packs, fake chat fixes, fake soak, fake hardening, fake reproducibility, fake closure audit, and Phase 16 leakage
- Expected Outputs:
  - explicit findings or no-finding audit result
  - residual risk note if needed
- Non-Goals:
  - code fixes
  - plan rewriting
  - approval

## Required Reads First

- full Phase 15 draft
- `Source Cartographer` output
- `Architecture & Contract Lead` output
- `Test & Replay Lead` output
- relevant approved Phase 13 and Phase 14 truth

## Step-by-Step Work Method

1. Check that all required sections exist.
2. Check that each subsystem has source basis and disposition.
3. Check that no giant proof harness is being passed off as design.
4. Check that no fake chat fix, prompt-table patch, regex-only route list, or terminal-only demo is being passed off as real intelligence proof.
5. Check that no approval or completion claim is implied.

## Required Cross-Checks

- no blind greenfield recreation where donor substrate exists
- no silent omission of required subsystems
- no Phase 16 behavior smuggled in
- no empty pack, chat, soak, hardening, reproducibility, or closure path

## Exit Criteria

- all blockers are cleared or raised explicitly

## Handoff Target

- `Program Governor`

## Anti-Drift Rule

- Do not rewrite the plan instead of auditing it.

## Explicit Proof That No Approval Is Implied

- Audit pass is not phase approval.
