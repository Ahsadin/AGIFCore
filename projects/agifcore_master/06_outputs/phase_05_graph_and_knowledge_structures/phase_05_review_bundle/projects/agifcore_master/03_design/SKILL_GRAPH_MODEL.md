# Skill Graph Model

## Purpose

This file defines the first-pass skill-graph framing for AGIFCore.

The skill graph is the governed structure for reusable procedural ability, not a loose list of tools.

## Skill-graph responsibilities

- represent reusable procedures and callable skills
- record preconditions, postconditions, and governance-relevant limits
- support provenance-aware reuse and transfer
- separate procedural reuse from semantic abstraction

## First-pass node expectations

- skill identity
- required context or inputs
- allowed target domains
- execution or invocation constraints
- provenance status
- trace and review references where later execution requires them

## Hard rules

- A skill edge or node may not imply unrestricted transfer.
- Skills must stay compatible with the machine-role policy, sandbox limits, and governance model.
- A skill graph is not permission to execute a skill automatically.
- Later product/runtime work may expose skills, but the graph itself remains a governed support structure.

## Dependency notes

- Exact graph schemas and runtime invocation semantics remain later Phase 5 and later runtime work.
- This first-pass model depends on the graph-stack layer split and the provenance lane staying explicit.
- Procedural memory and skill graph should remain aligned but not be collapsed into one vague concept.

## Cross-References

- `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
- `projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md`
- `projects/agifcore_master/03_design/SANDBOX_MODEL.md`
- `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
