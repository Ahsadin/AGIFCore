# Tool Permission Matrix

## Purpose

Freeze who may read, write, test, build, install, use network, or modify release artifacts.

Network is off by default for all roles unless the task card explicitly allows it and the user has approved that class of work.

## Matrix

| Role | Read | Write | Run Tests | Run Build/Install | Network | Modify Release Artifacts |
| --- | --- | --- | --- | --- | --- | --- |
| Program Governor | all project files | `00_admin/`, `01_plan/`, project truth files | yes | yes | no by default | no |
| Constitution Keeper | all project files | `02_requirements/` | text checks only | no | no | no |
| Source Cartographer | all source repos and project files | `01_plan/` mapping files | inventory scripts only | no | no | no |
| Architecture & Contract Lead | all project files | `03_design/` | contract checks only | no | no | no |
| Active Build Pod Lead | task-card scope | task-card owned files only | scoped tests | scoped builds | no | no |
| Test & Replay Lead | all project files | `05_testing/`, `06_outputs/` | yes | yes | no | no |
| Anti-Shortcut Auditor | all project files | audit records only | yes | yes if needed for proof | no | no |
| Merge Arbiter | all project files | integrated cleared patches in allowed scope | yes | yes | no | no |
| Validation Agent | all project files | validation request only | yes | demo verification only | no | no |
| Release & Evidence Lead | all project files | `06_outputs/`, release package files | package checks | packaging only | no by default | yes |

## Hard Rules

- A role may only write where both the matrix and the active task card allow it.
- Tool permission does not override folder ownership.
- Network use without explicit approval is a policy violation.
- Build or install commands outside the role's band are invalid work.
