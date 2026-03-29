# Execution Chain Of Command

## Purpose

Freeze the AGIFCore operating model so every agent knows who decides what, who reports to whom, and how phase closure works.

## Fixed Structure

AGIFCore uses this fixed structure:

- one `Governor`
- one `Manager`
- `2-5+` `Workers` under the manager as needed by task size

The number of workers may change. The authority chain may not.

## Authority Order

Authority order is:

1. `User`
2. `Governor`
3. `Manager`
4. `Workers`

The user is the final human authority.
The governor is the highest project authority below the user.

## Reporting Order

Reporting order is:

1. `Workers -> Manager`
2. `Manager -> Governor`
3. `Governor -> User`

Workers do not report final phase truth directly to the user.
Managers do not declare final phase truth directly to the user.
Governor is the only role that may carry manager output forward as official project truth below the user.

## Worker Rules

Workers:

- receive bounded tasks from the manager
- may work in parallel when scopes are disjoint
- must report results, evidence, and blockers to the manager
- may not claim a phase earned
- may not decide the next official prompt
- may not skip the manager and report final truth directly to the governor or user unless explicitly redirected

## Manager Rules

Manager:

- assigns worker scopes
- chooses whether to use `2`, `3`, `5`, or more workers
- consolidates worker output into one manager report
- prepares demos and evidence for governor review
- may not declare phase closure
- may not ask the user for final phase approval on their own

## Governor Rules

Governor:

- reviews the manager report
- reads the actual code and relevant files directly
- reruns the required checks and verifiers directly
- verifies the demo path directly
- decides whether evidence is strong enough or more work is required
- decides the next official prompt
- decides whether the phase is ready for user review
- asks the user to review the end-of-phase demo
- may not mark the phase earned without user approval

Governor must never treat report text alone as sufficient proof.

## End-Of-Phase Closure Flow

The required closure flow is:

1. workers finish bounded work
2. manager produces one consolidated report
3. governor independently reads the relevant code
4. governor independently reruns the required checks and direct sanity paths
5. governor independently verifies the demo path
6. governor requests user review with a demo
7. user checks the demo and gives a verdict
8. phase is earned only if the user approves it
9. only then may the next phase begin

## Freeze Rule

This operating model is frozen.

No one may change:

- the chain of authority
- the chain of reporting
- the governor-controlled user review rule
- the user approval requirement for phase closure

unless the user explicitly approves a revision.
