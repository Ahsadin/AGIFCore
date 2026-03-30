# Phase Approval Rules

## Approval Standard

AGIFCore phases are approved only by the user after the full closure chain has completed.

## Required Closure Chain

1. scoped work is implemented
2. tests and verifiers pass
3. a user-facing demo exists
4. the Anti-Shortcut Auditor passes the artifact set
5. the Program Governor verifies the files and demo directly
6. the Validation Agent issues the user review request
7. the user gives an explicit verdict

## Verdict Rule

- `approved` earns the phase
- `rejected` does not earn the phase
- `approved_with_blockers` does not earn the phase

## Phase 1 Rule

Phase 1 planning may prepare the closure chain, but it may not claim approval, closure, or freeze before the user verdict exists.

## Cross-References

- `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- `projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md`
