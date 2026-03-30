# Validation Protocol

## Purpose

This file defines the AGIFCore phase validation and closure protocol.

No phase may be treated as earned unless the full closure chain below exists and the user has explicitly approved the phase review package.

## Phase closure requirements

Every phase closeout must include all of the following:

1. automated verification
2. a user-facing demo
3. machine-readable evidence
4. an anti-shortcut audit pass
5. a governor verification pass
6. a validation-agent review package
7. a governor-issued user review request
8. an explicit user verdict

Only `approved` earns the phase.

Allowed user verdicts:

- `approved`
- `rejected`
- `approved_with_blockers`

## Closure records

Phase closure must be backed by these records, with no substitution by summary text:

- task card from `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
- audit report from `projects/agifcore_master/00_admin/AUDIT_REPORT_TEMPLATE.md`
- governor verification record from `projects/agifcore_master/00_admin/GOVERNOR_VERIFICATION_RECORD_TEMPLATE.md`
- validation request from `projects/agifcore_master/00_admin/VALIDATION_REQUEST_TEMPLATE.md`
- user verdict from `projects/agifcore_master/00_admin/USER_VERDICT_TEMPLATE.md`

If any required record is missing, the phase stays open.

## Required closure chain

The closure order is fixed:

1. Program Governor opens the phase task card.
2. the active build role implements scoped work only.
3. Test & Replay Lead produces tests, verifier output, and evidence.
4. Anti-Shortcut Auditor checks claims against files, tests, and evidence.
5. Anti-Shortcut Auditor writes the audit report.
6. Merge Arbiter integrates only cleared patches under the branch/worktree policy.
7. Program Governor independently reads the relevant files.
8. Program Governor independently reruns the required checks and direct sanity paths.
9. Program Governor independently verifies the demo path.
10. Program Governor writes the governor verification record.
11. Validation Agent writes the review request from the audited files, demo path, and evidence.
12. Program Governor asks the user to review the demo.
13. the user gives a verdict.
14. only then may the phase be marked earned.

## Validation package shape

The validation package must be inspectable by a human and must separate the following surfaces:

- the authored phase artifacts
- the audit report
- the Governor verification record
- the demo path
- the validation request
- the user verdict request

The validation request must point to real files and concrete review questions. It may not ask the user to approve a phase without showing the artifacts to inspect.

## Required checks

The Governor verification pass must independently confirm all of the following:

- the files exist on disk
- the checks were rerun directly
- the demo path is inspectable
- the phase gate language is truthful
- the approved phase baseline was not mutated outside the permitted scope

The Anti-Shortcut Auditor must independently confirm all of the following:

- no placeholder file is mislabeled as complete
- no required artifact is silently missing
- no closure claim rests on report text alone
- no role validates its own work

## Special rules

- Build Pod Lead, Merge Arbiter, and Validation Agent must be separate agents, sessions, or threads even if they use the same model family.
- If Meta & Growth Pod Lead is active, one extra audit pass and one additional human demo checkpoint are mandatory when self-improvement, self-initiated inquiry, or structural growth behavior changes land.
- Report text alone is never enough for phase truth.
- No agent may approve its own work.
- A later user verdict may be `approved_with_blockers`, but only `approved` earns the phase.

## Phase demo and review handoff

The final user review request must be issued only after:

- the audit report exists
- the Governor verification record exists
- the Validation Agent has prepared the review request
- the demo path is ready for inspection

The user review request must clearly state:

- what to inspect
- what good looks like
- what failure looks like
- which verdicts are allowed

## Cross-References

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- `projects/agifcore_master/01_plan/PHASE_INDEX.md`
- `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- `projects/agifcore_master/00_admin/TASK_CARD_TEMPLATE.md`
- `projects/agifcore_master/00_admin/AUDIT_REPORT_TEMPLATE.md`
- `projects/agifcore_master/00_admin/GOVERNOR_VERIFICATION_RECORD_TEMPLATE.md`
- `projects/agifcore_master/00_admin/VALIDATION_REQUEST_TEMPLATE.md`
- `projects/agifcore_master/00_admin/USER_VERDICT_TEMPLATE.md`
