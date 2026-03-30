# Phase 4 Slice 3 Compression Forgetting And Retirement

- Task card ID: `P4-TC-MGPL-06`
- Role owner: `Memory & Graph Pod Lead`
- Model tier: `gpt-5.3-codex`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Implement the final missing Phase 4 runtime lifecycle surfaces:

- `compression_pipeline.py`
- `forgetting_retirement.py`

This slice must build on the cleared slice-2 merge lane and must stay inside Phase 4 memory-lifecycle scope only.

## Exact Files Allowed To Touch

- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/compression_pipeline.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/forgetting_retirement.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/__init__.py`

## Forbidden Files

- existing slice-1 and slice-2 runtime files except `__init__.py` if export wiring is required
- verifier files
- evidence files
- demo files
- Phase 5+ files

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- `projects/agifcore_master/03_design/MEMORY_MODEL.md`
- `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md`
- `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md`
- cleared slice-2 merge runtime
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/memory_review.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/rollback_safe_updates.py`

## Step-By-Step Method

1. Implement explicit compression as a real state transition, not as a label.
2. Implement explicit forgetting with preserved retained anchors and rollback-safe behavior where state is removed.
3. Implement explicit retirement for reusable memory entries that must leave the active set.
4. Keep all lifecycle transitions review-gated and auditable.
5. Keep graph references as plain references only. No graph persistence or traversal logic.

## Required Cross-Checks

- compression has verifier-visible before or after effects
- forgetting preserves a retained anchor or summary trail
- retirement changes active state explicitly
- no one-store shortcut appears
- no Phase 5 or conversation drift appears

## Exit Criteria

- both slice-3 runtime files exist
- they import cleanly on top of the slice-2 merge baseline
- lifecycle actions are explicit and bounded

## Handoff Target

`Test & Replay Lead`

## Anti-Drift Rule

Do not rebuild memory review, correction, or graph behavior inside this slice.

## Proof That No Approval Is Implied

Slice-3 runtime work is internal execution only. Phase 4 remains `open`.
