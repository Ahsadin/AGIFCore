# Validation Protocol

Every phase must end with:

1. automated verification
2. a user-facing demo
3. a validation-agent review package prepared for governor review
4. a governor-issued user review request
5. explicit user verdict

Allowed user verdicts:

- `approved`
- `rejected`
- `approved_with_blockers`

Only `approved` earns the phase.

Report text alone is never enough for phase truth.

Required closure chain:

1. workers complete scoped work
2. manager consolidates evidence
3. governor independently reads the relevant code
4. governor independently reruns the required checks and direct sanity paths
5. governor verifies the demo path
6. governor requests user review with the demo package
7. user gives verdict
8. only then may the phase be marked earned
