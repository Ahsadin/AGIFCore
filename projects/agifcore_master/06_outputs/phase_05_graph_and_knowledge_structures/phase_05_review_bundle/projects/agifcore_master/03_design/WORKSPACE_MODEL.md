# Workspace Model

## Purpose

This file defines the first-pass workspace and operator boundary for AGIFCore.

The workspace is the governed shared state surface that later fabric, runtime, and evidence flows must coordinate through.

## Workspace responsibilities

- hold shared workspace state
- expose the operator command family
- preserve lineage, rollback, quarantine, and evidence references
- separate user-visible state from internal execution traces
- support replayable coordination across later cells, tissues, and runtime surfaces

## Operator command family

The operator family must remain explicit and governed. First-pass command classes are:

- inspect current state
- plan or propose a governed action
- verify or replay a prior action
- rollback or quarantine when policy requires it
- export governed evidence

These are command classes, not a final CLI or API syntax freeze.

## Hard boundaries

- The workspace is shared state, not a hidden autonomy channel.
- Operator commands must pass through governance and trace surfaces.
- Rollback and quarantine must remain first-class workspace concepts.
- Branch/worktree build rules support governance around the workspace, but build-branch state is not runtime truth by itself.
- Any state export must preserve provenance and replay anchors.

## Dependencies and open points

- The exact workspace schema still depends on the later graph, memory, and runtime phases.
- The operator family must stay aligned to the trace contract and product runtime model.
- This first-pass model intentionally freezes boundaries before later implementation chooses exact storage details.

## Cross-References

- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
- `projects/agifcore_master/00_admin/BRANCH_AND_WORKTREE_POLICY.md`
