# Changelog

## 2026-03-29

- Created the canonical AGIFCore project scaffold.
- Added the frozen master plan placeholder files and role-authority rules.
- Added the initial planning, requirement, design, execution, testing, outputs, assets, and logs directories.
- Expanded the authority model with a frozen chain-of-command rule:
  - one governor
  - one manager
  - `2-5+` workers under the manager as needed
  - workers report to manager
  - manager reports to governor
  - governor asks the user for end-of-phase review
  - no next phase starts before user approval
- Tightened the governor rule so report text alone never counts as proof.
- Required the governor to independently inspect code, rerun checks, and verify demos before phase decisions or user review.
