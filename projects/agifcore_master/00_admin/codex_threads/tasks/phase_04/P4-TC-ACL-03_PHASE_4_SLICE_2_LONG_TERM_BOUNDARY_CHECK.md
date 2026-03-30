# Phase 4 Slice 2 Long-Term Boundary Check

- Task card ID: `P4-TC-ACL-03`
- Role owner: `Architecture & Contract Lead`
- Model tier: `gpt-5.4`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Check the Phase 4 slice-2 boundary discipline around semantic memory, procedural memory, promotion, and correction.

## Exact Files Allowed To Touch

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-NOTE-ACL-03_PHASE_4_SLICE_2_BOUNDARY_NOTES.md`

## Forbidden Files

- runtime files
- verifier files
- evidence files
- plan files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- slice-1 merge lane runtime and evidence
- slice-2 runtime files
- `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
- `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`

## Step-By-Step Method

1. Confirm semantic memory remains abstraction-only.
2. Confirm procedural memory remains procedure-only.
3. Confirm promotion stays review-gated.
4. Confirm correction stays rollback-safe and continuity-aware.
5. Confirm no graph implementation or conversation behavior appears.

## Required Cross-Checks

- no semantic/procedural collapse
- no graph schema, persistence, or traversal
- no Phase 2 rollback replacement
- no Phase 7 behavior

## Exit Criteria

- one substantive slice-2 boundary note exists
- it records pass or concrete seam risks

## Handoff Target

`Program Governor`

## Anti-Drift Rule

Do not rewrite slice-2 runtime while checking it.

## Proof That No Approval Is Implied

Boundary review does not approve slice 2 or Phase 4. Phase 4 remains `open`.
