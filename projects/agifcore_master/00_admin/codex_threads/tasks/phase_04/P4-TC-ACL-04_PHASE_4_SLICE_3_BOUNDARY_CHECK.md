# Phase 4 Slice 3 Boundary Check

- Task card ID: `P4-TC-ACL-04`
- Role owner: `Architecture & Contract Lead`
- Model tier: `gpt-5.4`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Check the final lifecycle slice for boundary discipline:

- compression
- forgetting
- retirement

The check must confirm that Phase 4 lifecycle logic stays separate from Phase 5 graph logic and Phase 7 conversation behavior.

## Exact Files Allowed To Touch

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-NOTE-ACL-04_PHASE_4_SLICE_3_BOUNDARY_NOTES.md`

## Forbidden Files

- runtime files
- verifier files
- evidence files
- plan files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- slice-3 runtime files
- `projects/agifcore_master/03_design/MEMORY_MODEL.md`
- `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
- `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`

## Step-By-Step Method

1. Confirm compression, forgetting, and retirement stay in the memory-lifecycle layer.
2. Confirm lifecycle transitions remain review-gated and auditable.
3. Confirm no graph persistence, graph schemas, traversal, or conversation behavior appears.
4. Write a short truthful boundary note.

## Required Cross-Checks

- no one-store collapse
- no hidden graph behavior
- no hidden conversation behavior

## Exit Criteria

- boundary note exists
- it states whether slice-3 boundaries stayed intact

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not redesign the phase plan or runtime from the boundary lane.

## Proof That No Approval Is Implied

Slice-3 boundary review is advisory only. Phase 4 remains `open`.
