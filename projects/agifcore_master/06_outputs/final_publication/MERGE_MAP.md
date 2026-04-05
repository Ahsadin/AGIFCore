# Merge Map

This map describes how local branches should flow to the final public `main` branch.

## Direct Public Target

- `main`

## Merge Or Cherry-Pick Candidates

These are the only branches worth carrying into `main` if a publication file is still missing there:

- `codex/tc-p15-pg-04-final-bounded-closeout`
- `codex/final-public-baseline-cleanup`

Guidance:

- start from current `main`
- fast-forward or merge in the bounded closeout branch first because `main` is an ancestor of `codex/tc-p15-pg-04-final-bounded-closeout`
- merge or cherry-pick the cleanup branch after the bounded closeout branch content is present
- use the smallest possible merge or cherry-pick set
- do not re-merge historical phase branches into `main`
- if the target files already exist on `main`, archive the branch instead of reapplying it

## Archive Only

These branches should not be promoted into final public `main`:

- `codex/phase-14-manifest-strengthening-closeout`
- `codex/tc-p0-tc-pg-01-phase-0-reset-source-freeze`
- `codex/tc-p1-tc-pg-01-phase-1-governor-control`
- `codex/tc-p1-tc-pg-02-phase-0-blocker-remediation`
- `codex/tc-p10-tc-pg-02-phase-10-execution-control`
- `codex/tc-p12-tc-pg-02-phase-12-execution-control`
- `codex/tc-p13-tc-pg-03-phase-13-closeout`
- `codex/tc-p2-tc-pg-01-phase-2-governor-control`
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
- `codex/tc-p3-tc-ma-05-phase-3-closeout-integration`
- `codex/tc-p3-tc-pg-01-phase-3-governor-control`
- `codex/tc-p3-tc-pg-02-phase-3-slice-2-governor-control`
- `codex/tc-p3-tc-pg-03-phase-3-slice-3-governor-control`
- `codex/tc-p3-tc-pg-04-phase-3-slice-4-governor-control`
- `codex/tc-p3-tc-pg-05-phase-3-review-package`
- `codex/tc-p3-tc-pg-06-phase-3-closeout`
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
- `codex/tc-p6-tc-pg-02-phase-6-execution-control`
- `codex/tc-p6-tc-pg-03-phase-6-closeout`
- `codex/tc-p7-tc-pg-03-phase-7-closeout`
- `codex/tc-p7-tc-wcpl-02-phase-7-conversation-core-implementation`
- `codex/tc-p8-tc-pg-01-phase-8-plan`
- `codex/tc-p8-tc-wcpl-02-phase-8-science-world-awareness-implementation`
- `codex/tc-p9-tc-pg-02-phase-9-execution-control`

## Final Rule

Nothing here should be cherry-picked into `main` just because it exists.
If a file is already present in the canonical closeout surfaces, archive the branch instead.
