# Bottleneck Escalation Rules

## Escalation Triggers

Escalate to Program Governor when any of the following appears:

- a required artifact is missing
- a task-card scope is unclear
- two roles would write the same file
- a file drifts outside frozen Phase 1 scope
- a reviewer or auditor finds unsupported completeness
- a user-approval path is implied without a verdict
- source lineage is ambiguous or incomplete

## Escalation Shape

Every escalation must include:

- the exact file path
- the exact mismatch
- the role that detected it
- the immediate containment action

## Containment Rule

Do not patch around a bottleneck by expanding scope. Do not treat a bottleneck as a reason to skip audit, verification, or user review.

## Cross-References

- `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
- `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
