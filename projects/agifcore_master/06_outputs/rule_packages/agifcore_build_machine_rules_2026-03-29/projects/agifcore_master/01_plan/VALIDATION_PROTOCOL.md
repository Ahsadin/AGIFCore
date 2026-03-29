# Validation Protocol

Every phase must end with:

1. automated verification
2. a user-facing demo
3. machine-readable evidence
4. an anti-shortcut audit pass
5. a governor verification pass
6. a validation-agent review package
7. a governor-issued user review request
8. explicit user verdict

Allowed user verdicts:

- `approved`
- `rejected`
- `approved_with_blockers`

Only `approved` earns the phase.

Report text alone is never enough for phase truth.
No agent may approve its own work.

Required closure chain:

1. Program Governor opens the phase task card
2. the active build pod implements scoped work only
3. Test & Replay Lead produces tests, verifier output, and evidence
4. Anti-Shortcut Auditor checks claims against files, tests, and evidence
5. Merge Arbiter integrates only cleared patches
6. Program Governor independently reads the relevant code
7. Program Governor independently reruns the required checks and direct sanity paths
8. Program Governor independently verifies the demo path
9. Validation Agent writes the review request from code, tests, demo, and evidence
10. Program Governor asks the user to review the demo
11. the user gives a verdict
12. only then may the phase be marked earned
