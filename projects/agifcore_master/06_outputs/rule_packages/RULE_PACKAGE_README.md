# AGIFCore Rule Package

## Purpose

This package is a frozen rule set for external review.

It is meant to be uploaded as supporting context so another GPT can verify:

- the AGIFCore build-machine role model
- the separation between build agents and runtime truth
- the phase-validation and user-approval rules
- the folder ownership and model-tier policies
- the task-card and handoff templates
- the tool-permission, branch/worktree, and escalation rules
- the full Phase 1 planning files required by the master plan
- the full requirements pack and design pack that the package refers to
- the rule that same model family does not mean same agent
- the danger-zone controls for Meta & Growth Pod

## Included Files

- root repo rules:
  - `AGENTS.md`
- project truth files:
  - `projects/agifcore_master/AGENTS.override.md`
  - `projects/agifcore_master/PROJECT_README.md`
  - `projects/agifcore_master/DECISIONS.md`
  - `projects/agifcore_master/CHANGELOG.md`
- full `01_plan/` file set
- full `02_requirements/` file set
- full `03_design/` file set
- admin enforcement files under `projects/agifcore_master/00_admin/`:
  - task card template
  - audit report template
  - governor verification checklist
  - governor verification record template
  - validation request template
  - user verdict template
  - model manifest
  - tool permission matrix
  - branch and worktree policy
  - escalation and freeze rules

## Freeze Rule

These files should be treated as frozen for verification unless the user explicitly approves a revision.
