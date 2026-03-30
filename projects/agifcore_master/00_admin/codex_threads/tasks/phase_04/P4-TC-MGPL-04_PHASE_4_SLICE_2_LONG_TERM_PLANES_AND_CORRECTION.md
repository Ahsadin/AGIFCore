# Phase 4 Slice 2 Long-Term Planes And Correction

- Task card ID: `P4-TC-MGPL-04`
- Role owner: `Memory & Graph Pod Lead`
- Model tier: `gpt-5.3-codex`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Implement the Phase 4 slice-2 runtime surfaces that add the remaining long-term planes and governed correction path:

- semantic memory
- procedural memory
- promotion pipeline
- correction handling

This slice must build on the cleared slice-1 merge lane, not on the older role branches.

## Exact Files Allowed To Touch

- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/semantic_memory.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/procedural_memory.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/promotion_pipeline.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/correction_handling.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/__init__.py`

## Forbidden Files

- slice-1 runtime files except `__init__.py` if import exports must be extended
- compression and forgetting or retirement runtime files
- demo files
- plan files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- `projects/agifcore_master/03_design/MEMORY_MODEL.md`
- `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
- `projects/agifcore_master/03_design/CELL_FAMILIES.md`
- cleared slice-1 runtime on the slice-1 merge lane
- `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
- `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`

## Step-By-Step Method

1. Implement semantic memory as reviewed abstractions only.
2. Implement procedural memory as reusable procedures with explicit constraints.
3. Implement promotion from review-approved candidates into semantic, procedural, or continuity memory with provenance.
4. Implement correction handling with explicit before or after mutation flow using slice-1 rollback-safe updates.
5. Keep graph-facing references as plain references only. No Phase 5 graph logic.

## Required Cross-Checks

- semantic memory does not hold raw turn transcript or scratchpad state
- procedural memory stays distinct from semantic memory
- promotion depends on review-approved candidates
- correction uses rollback-safe updates and preserves supersession markers
- no graph persistence or traversal appears

## Exit Criteria

- all four slice-2 runtime files exist
- slice-2 runtime imports cleanly on top of the slice-1 merge baseline
- no Phase 5 or conversation drift appears

## Handoff Target

`Test & Replay Lead`

## Anti-Drift Rule

Do not sneak compression, forgetting, or retirement into this slice.

## Proof That No Approval Is Implied

Slice-2 runtime work is internal execution only. Phase 4 remains `open`.
