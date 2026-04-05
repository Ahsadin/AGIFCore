# Branch Inventory

This inventory records the current local branch state after the final public-baseline cleanup.

## Buckets

- `contributes_to_final_main`: branch content is needed in the final public `main`
- `retain_temporarily`: keep until tags, git bundle, and final verification are complete
- `delete_after_verification`: safe candidate for deletion only after archival and final verification
- `manual_review_required`: do not delete until a human or Governor explicitly clears it

## Branch Summary

- `contributes_to_final_main`
  - `main`
- `retain_temporarily`
  - none currently
- `delete_after_verification`
  - none currently
- `manual_review_required`
  - none currently

## Current Meaning

The branch cleanup is complete at the local-branch level.
The working repository now has one canonical branch:

- `main`

Historical `codex/*` branches were deleted only after:

- updating `main` to the public-baseline cleanup state
- creating local preservation tags
- creating a full local git bundle backup

See `BRANCH_CLEANUP_REPORT.md` for the deleted branch list and recoverability record.
