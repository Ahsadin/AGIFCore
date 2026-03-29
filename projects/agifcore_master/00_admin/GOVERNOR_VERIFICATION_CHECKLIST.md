# Governor Verification Checklist

Program Governor must complete this checklist before asking the user for phase review.

## Inputs Present

- active task card exists
- audit report exists
- required evidence files exist
- demo path exists
- validation request draft exists
- required agent session ids are recorded

## Code Truth

- read the relevant changed code directly
- confirm changed files match the task card scope
- confirm forbidden files were not changed
- confirm contracts and gates were not bypassed

## Check Truth

- rerun the required tests directly
- rerun required verifiers directly
- confirm evidence outputs match the latest code

## Demo Truth

- run or verify the demo path directly
- confirm the demo shows the claimed behavior
- confirm fail-closed or honest-abstain behavior where relevant

## Process Truth

- confirm tool-permission rules were not violated
- confirm branch/worktree policy was followed
- confirm no unauthorized model downgrade occurred
- confirm no role both wrote and validated the same artifact
- confirm Build Pod Lead, Merge Arbiter, and Validation Agent are separate agents or sessions

## Danger-Zone Truth

If Meta & Growth Pod Lead is active:

- confirm the extra audit pass exists
- confirm stronger Program Governor review was performed
- confirm the additional human demo checkpoint was completed when required

## Decision

- `ready_for_user_review`
- `reopen_for_more_work`
- `freeze_and_escalate`
