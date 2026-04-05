# P15-TC-TRL-01 Phase 15 Proof And Evidence Plan

- Task Card ID: `P15-TC-TRL-01`
- Phase: `15`
- Title: `Phase 15 proof, verifier, and evidence family planning`
- Status: `open`
- Issued By: `Program Governor`

## Role Assignment

- Active Build Role: `Test & Replay Lead`
- Supporting Roles:
  - `Program Governor`
  - `Architecture & Contract Lead`
  - `Release & Evidence Lead`
- Allowed Models: `gpt-5.4-mini`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_15/P15-TC-TRL-01_PHASE_15_PROOF_AND_EVIDENCE_PLAN.md`
- Forbidden Files:
  - `.codex/`
  - all `projects/agifcore_master/04_execution/*`
  - all `projects/agifcore_master/05_testing/*`
  - all `projects/agifcore_master/06_outputs/*`
  - all Phase 16 and later artifacts

## Objective

- Goal: define the later Phase 15 proof, live-turn, soak, hardening, reproducibility, closure-audit, verifier, and evidence family
- Expected Outputs:
  - verifier-family decomposition
  - evidence-manifest strategy
  - later output family list
- Non-Goals:
  - runtime logic
  - fabricated reports
  - approval

## Required Reads First

- `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
- approved Phase 14 verifier and evidence families
- `projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md`
- `Source Cartographer` output
- `Architecture & Contract Lead` output

## Step-by-Step Work Method

1. Define one verifier family per major Phase 15 subsystem.
2. Define the live-turn proof verifier family separately from blind, hidden, live-demo, and soak.
3. Define cross-cutting evidence manifests and claim-to-evidence links.
4. Define later proof-pack, live-turn, soak, hardening, reproducibility, and closure-audit outputs.
5. Define demo hooks for the real desktop demo, soak summary, and closure-audit summary.

## Required Cross-Checks

- all proof claims must map to machine-readable evidence
- blind, hidden, live-demo, live-turn repair, soak, hardening, reproducibility, and closure audit must stay separate
- no soak-only notes passed off as proof
- no terminal-only demo passed off as the final demo
- no Phase 16/public release creep

## Exit Criteria

- later testing and evidence path is decision-complete

## Handoff Target

- `Release & Evidence Lead`
- `Program Governor`

## Anti-Drift Rule

- Do not implement runtime behavior through verifier planning.

## Explicit Proof That No Approval Is Implied

- Verification planning does not earn Phase 15.
