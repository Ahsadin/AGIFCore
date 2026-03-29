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

Required closure records:

- task card from `00_admin/TASK_CARD_TEMPLATE.md`
- audit report from `00_admin/AUDIT_REPORT_TEMPLATE.md`
- governor verification record from `00_admin/GOVERNOR_VERIFICATION_RECORD_TEMPLATE.md`
- validation request from `00_admin/VALIDATION_REQUEST_TEMPLATE.md`
- user verdict from `00_admin/USER_VERDICT_TEMPLATE.md`

Required closure chain:

1. Program Governor opens the phase task card
2. the active build pod implements scoped work only
3. Test & Replay Lead produces tests, verifier output, and evidence
4. Anti-Shortcut Auditor checks claims against files, tests, and evidence
5. Anti-Shortcut Auditor writes the audit report
6. Merge Arbiter integrates only cleared patches under the branch/worktree policy
7. Program Governor independently reads the relevant code
8. Program Governor independently reruns the required checks and direct sanity paths
9. Program Governor independently verifies the demo path
10. Program Governor writes the governor verification record
11. Validation Agent writes the review request from code, tests, demo, and evidence
12. Program Governor asks the user to review the demo
13. the user gives a verdict
14. only then may the phase be marked earned

If any required record is missing, the phase stays open.

Special rules:

- Build Pod Lead, Merge Arbiter, and Validation Agent must be separate agents, sessions, or threads even if they use the same model family.
- If Meta & Growth Pod Lead is active, one extra audit pass and one additional human demo checkpoint are mandatory when self-improvement, self-initiated inquiry, or structural growth behavior changes land.
