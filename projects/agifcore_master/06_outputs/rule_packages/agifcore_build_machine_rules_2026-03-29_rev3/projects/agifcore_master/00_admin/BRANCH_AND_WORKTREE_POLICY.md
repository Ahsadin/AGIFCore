# Branch And Worktree Policy

## Purpose

Freeze isolation rules so serious work does not happen directly on the canonical branch.

## Core Rules

- One branch per task card.
- One worktree per task card when isolation is needed.
- No mixed-task branches.
- No direct implementation edits on `main`.

## Naming

- Branch format: `codex/tc-<task_card_id>-<slug>`
- Worktree format: `.worktrees/<task_card_id>`
- Rollback tag format: `rollback/<task_card_id>/<yyyymmdd-hhmm>`

## Merge Rules

- Only Merge Arbiter may integrate cleared patches into the canonical branch.
- A rollback tag must exist before integration.
- Merge Arbiter may not integrate if audit, governor verification, or validation records are missing.

## Exceptions

Direct commits on `main` are allowed only for:

- repository bootstrap
- frozen policy updates
- explicit user-approved admin-only maintenance

Those exceptions do not apply to implementation work.

## Closeout

- After merge, the task branch may be deleted or archived.
- The worktree may be removed only after evidence and rollback references are preserved.
