# Branch Cleanup Report

Date: `2026-04-05`
Status: `completed`

## Final Branch State

- kept: `main`
- retained temporarily: none
- deleted safely in this pass: `36` historical `codex/*` branches

## Recoverability Basis

Branch deletion happened only after all of these were true:

- `main` already pointed at the public-baseline cleanup state
- preservation tags existed:
  - `pre-public-cleanup-main-20260405`
  - `bounded-closeout-baseline-20260405`
- a full local git bundle backup had already been created before destructive cleanup

## Deleted Branches

- `codex/tc-p3-tc-acl-02-phase-3-slice-2-boundary-check`
- `codex/tc-p3-tc-acl-03-phase-3-slice-3-boundary-check`
- `codex/tc-p3-tc-acl-04-phase-3-slice-4-boundary-check`
- `codex/tc-p3-tc-asa-02-phase-3-slice-2-audit`
- `codex/tc-p3-tc-asa-03-phase-3-slice-3-audit`
- `codex/tc-p3-tc-asa-04-phase-3-slice-4-audit`
- `codex/tc-p3-tc-asa-05-phase-3-final-audit`
- `codex/tc-p3-tc-kpl-02-phase-3-slice-2-activation-trust-and-dormant-control`
- `codex/tc-p3-tc-kpl-03-phase-3-slice-3-split-merge-and-profile-budgets`
- `codex/tc-p3-tc-kpl-04-phase-3-slice-4-bundle-integrity-runtime`
- `codex/tc-p3-tc-pg-01-phase-3-governor-control`
- `codex/tc-p3-tc-pg-02-phase-3-slice-2-governor-control`
- `codex/tc-p3-tc-rel-04-phase-3-demo-bundle`
- `codex/tc-p3-tc-trl-01-phase-3-slice-1-contract-and-bundle-verifiers`
- `codex/tc-p3-tc-trl-02-phase-3-slice-2-activation-trust-verifier`
- `codex/tc-p3-tc-trl-03-phase-3-slice-3-split-merge-and-profile-verifiers`
- `codex/tc-p3-tc-trl-04-phase-3-slice-4-integrity-and-orchestration-verifiers`
- `codex/tc-p3-tc-va-04-phase-3-validation-request`
- `codex/tc-p4-tc-acl-02-phase-4-boundary-check`
- `codex/tc-p4-tc-acl-03-phase-4-slice-2-boundary-check`
- `codex/tc-p4-tc-acl-04-phase-4-slice-3-boundary-check`
- `codex/tc-p4-tc-asa-02-phase-4-slice-1-audit`
- `codex/tc-p4-tc-asa-03-phase-4-slice-2-audit`
- `codex/tc-p4-tc-asa-04-phase-4-slice-3-audit`
- `codex/tc-p4-tc-asa-05-phase-4-final-package-audit`
- `codex/tc-p4-tc-ma-02-phase-4-slice-1-merge`
- `codex/tc-p4-tc-ma-03-phase-4-slice-2-merge`
- `codex/tc-p4-tc-ma-04-phase-4-slice-3-merge`
- `codex/tc-p4-tc-mgpl-02-phase-4-memory-plane-implementation`
- `codex/tc-p4-tc-mgpl-04-phase-4-slice-2-long-term-memory`
- `codex/tc-p4-tc-mgpl-06-phase-4-slice-3-compression-forgetting-and-retirement`
- `codex/tc-p4-tc-rel-02-phase-4-final-demo-bundle`
- `codex/tc-p4-tc-trl-02-phase-4-memory-verifiers`
- `codex/tc-p4-tc-trl-04-phase-4-slice-2-long-term-verifiers`
- `codex/tc-p4-tc-trl-05-phase-4-slice-3-lifecycle-verifiers`
- `codex/tc-p4-tc-va-02-phase-4-final-validation-request`

## Dirty File Resolution

The previously dirty Phase 13 demo artifact was restored to its committed state:

- `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_demo_bundle/phase_13_end_to_end_product_demo.json`

Reason:

- it was unrelated to the public-baseline cleanup pass
- its local changes were hash and timestamp updates to a historical demo artifact
- committing that change would have altered earlier demo evidence without a matching verification pass

## Final Rule

The repo now has one canonical local branch:

- `main`
