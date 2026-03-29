# Changelog

## 2026-03-29

- Created the canonical AGIFCore project scaffold.
- Added the frozen master plan placeholder files and role-authority rules.
- Added the initial planning, requirement, design, execution, testing, outputs, assets, and logs directories.
- Replaced the older simple governor/manager/worker rule set with a governed build-machine model.
- Froze specialized roles for planning, source mapping, architecture, implementation, testing, auditing, merge, validation, and release.
- Froze the rule that build agents stay outside the AGIFCore runtime truth path.
- Froze the rule that no agent may both write and validate the same artifact.
- Kept the rule that Program Governor must independently inspect code, rerun checks, and verify demos before any user review request.
- Added the missing enforcement layer:
  - task card template
  - audit report template
  - governor verification checklist and record template
  - validation request template
  - user verdict template
  - model manifest
  - tool permission matrix
  - branch and worktree policy
  - escalation and freeze rules
- Expanded the external rule package so it includes the full Phase 1 plan files, the requirements pack, the design pack, and the admin enforcement files.
- Tightened role-level enforcement:
  - same model family does not mean same agent
  - Build Pod Lead, Merge Arbiter, and Validation Agent must be separate sessions or threads
  - Meta & Growth Pod is now marked as a danger zone with extra audit and stronger governor review
  - Source Cartographer is default-active only in Phase 0 and Phase 1 unless lineage is touched again
  - Product & Sandbox Pod stays one pod for restart but cannot become a late-phase dumping ground
