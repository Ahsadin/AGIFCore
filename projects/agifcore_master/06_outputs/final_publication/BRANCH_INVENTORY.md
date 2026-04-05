# Branch Inventory

This inventory classifies every local branch into one of four buckets for final public cleanup.

## Buckets

- `contributes_to_final_main`: branch content is needed in the final public `main`
- `retain_temporarily`: keep until tags, git bundle, and final verification are complete
- `delete_after_verification`: safe candidate for deletion only after archival and final verification
- `manual_review_required`: do not delete until a human or Governor explicitly clears it

## Branch Summary

- `contributes_to_final_main`
  - `main`
  - `codex/tc-p15-pg-04-final-bounded-closeout`
  - `codex/final-public-baseline-cleanup`
- `retain_temporarily`
  - `codex/phase-14-manifest-strengthening-closeout`
- `delete_after_verification`
  - `codex/tc-p0-tc-pg-01-phase-0-reset-source-freeze`
  - `codex/tc-p1-tc-pg-01-phase-1-governor-control`
  - `codex/tc-p1-tc-pg-02-phase-0-blocker-remediation`
  - `codex/tc-p10-tc-pg-02-phase-10-execution-control`
  - `codex/tc-p12-tc-pg-02-phase-12-execution-control`
  - `codex/tc-p13-tc-pg-03-phase-13-closeout`
  - `codex/tc-p2-tc-pg-01-phase-2-governor-control`
  - `codex/tc-p3-tc-ma-05-phase-3-closeout-integration`
  - `codex/tc-p3-tc-pg-06-phase-3-closeout`
  - `codex/tc-p3-tc-acl-01-phase-3-slice-1-boundary-check`
  - `codex/tc-p3-tc-acl-02-phase-3-slice-2-boundary-check`
  - `codex/tc-p3-tc-acl-03-phase-3-slice-3-boundary-check`
  - `codex/tc-p3-tc-acl-04-phase-3-slice-4-boundary-check`
  - `codex/tc-p3-tc-asa-01-phase-3-slice-1-audit`
  - `codex/tc-p3-tc-asa-02-phase-3-slice-2-audit`
  - `codex/tc-p3-tc-asa-03-phase-3-slice-3-audit`
  - `codex/tc-p3-tc-asa-04-phase-3-slice-4-audit`
  - `codex/tc-p3-tc-asa-05-phase-3-final-audit`
  - `codex/tc-p3-tc-kpl-01-phase-3-slice-1-cell-tissues-and-bundle-schema`
  - `codex/tc-p3-tc-kpl-02-phase-3-slice-2-activation-trust-and-dormant-control`
  - `codex/tc-p3-tc-kpl-03-phase-3-slice-3-split-merge-and-profile-budgets`
  - `codex/tc-p3-tc-kpl-04-phase-3-slice-4-bundle-integrity-runtime`
  - `codex/tc-p3-tc-ma-01-phase-3-slice-1-merge`
  - `codex/tc-p3-tc-ma-02-phase-3-slice-2-merge`
  - `codex/tc-p3-tc-ma-03-phase-3-slice-3-merge`
  - `codex/tc-p3-tc-ma-04-phase-3-slice-4-merge`
  - `codex/tc-p3-tc-pg-01-phase-3-governor-control`
  - `codex/tc-p3-tc-pg-02-phase-3-slice-2-governor-control`
  - `codex/tc-p3-tc-pg-03-phase-3-slice-3-governor-control`
  - `codex/tc-p3-tc-pg-04-phase-3-slice-4-governor-control`
  - `codex/tc-p3-tc-pg-05-phase-3-review-package`
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
  - `codex/tc-p4-tc-pg-01-phase-4-governor-control`
  - `codex/tc-p4-tc-pg-05-phase-4-closeout`
  - `codex/tc-p4-tc-rel-02-phase-4-final-demo-bundle`
  - `codex/tc-p4-tc-trl-02-phase-4-memory-verifiers`
  - `codex/tc-p4-tc-trl-04-phase-4-slice-2-long-term-verifiers`
  - `codex/tc-p4-tc-trl-05-phase-4-slice-3-lifecycle-verifiers`
  - `codex/tc-p4-tc-va-02-phase-4-final-validation-request`
  - `codex/tc-p6-tc-pg-03-phase-6-closeout`
  - `codex/tc-p7-tc-pg-03-phase-7-closeout`
  - `codex/tc-p8-tc-pg-01-phase-8-plan`
  - `codex/tc-p8-tc-wcpl-02-phase-8-science-world-awareness-implementation`
  - `codex/tc-p9-tc-pg-02-phase-9-execution-control`
- `manual_review_required`
  - none currently

## Merge / Cherry-Pick Guidance To `main`

- Keep on `main`
  - `main`
- Merge or cherry-pick into `main`
  - `codex/tc-p15-pg-04-final-bounded-closeout`
  - `codex/final-public-baseline-cleanup`
- Keep temporarily until final verification and archival are complete
  - `codex/phase-14-manifest-strengthening-closeout`
- Delete only after verification, local tags, and git-bundle preservation
  - every branch listed under `delete_after_verification`

## Cleanup Note

The historical branches are useful as provenance, but they are not publication targets.
They should be archived or deleted only after the final public `main` is preserved locally and verified.
