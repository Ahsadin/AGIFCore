# Falsification Thresholds

## Failure Means Failure

If any of the following are true, the related claim is falsified:

- a required file is missing
- a required file is still placeholder-only
- a source pool is missing from the inheritance or freeze inventory
- a phase gate claims approval before the user verdict exists
- a review request points to an artifact that does not exist
- an artifact claims completeness without direct evidence
- a requirement or design file contradicts the frozen master plan

## Phase 1 Thresholds

- One missing required artifact is enough to fail the related closure claim.
- One silent omission is enough to fail the related coverage claim.
- One unsupported approval claim is enough to fail the related gate claim.
- One contradiction with the frozen baseline is enough to reopen the work.

## Operational Rule

When a threshold is crossed, the correct response is to stop, document the mismatch, and escalate to Program Governor.

## Cross-References

- `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_01/P1-TC-ASA-01_PHASE_1_ARTIFACT_AUDIT.md`
