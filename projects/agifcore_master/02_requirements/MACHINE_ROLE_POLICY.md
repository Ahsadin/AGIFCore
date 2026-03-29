# Machine Role Policy

## Purpose

This file defines the machine-side role boundaries that support AGIFCore without confusing build roles with runtime cognition.

## Frozen Role Classes

- `laptop` for local user-side work
- `mobile` for constrained user-side work
- `builder` for governed build-machine work
- `soak` for long-running validation work

## Hard Rules

- Build roles are not runtime roles.
- A build role may not become hidden project truth.
- Each task card must name one active role, one file scope, and one model tier.
- Build Pod Lead, Merge Arbiter, and Validation Agent must stay separate agents, sessions, or threads.
- No role may write outside its owned area unless the Program Governor explicitly authorizes it.

## Phase 1 Rule

Phase 1 uses this policy to keep the build machine governed and to keep later runtime claims from leaking into planning language.

## Cross-References

- `projects/agifcore_master/02_requirements/EXECUTION_CHAIN_OF_COMMAND.md`
- `projects/agifcore_master/00_admin/MODEL_MANIFEST.md`
