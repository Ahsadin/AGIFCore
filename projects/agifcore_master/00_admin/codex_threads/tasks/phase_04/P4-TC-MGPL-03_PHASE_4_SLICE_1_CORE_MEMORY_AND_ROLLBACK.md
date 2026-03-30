# Phase 4 Slice 1 Core Memory And Rollback

- Task card ID: `P4-TC-MGPL-03`
- Role owner: `Memory & Graph Pod Lead`
- Model tier: `gpt-5.3-codex`
- Phase: `Phase 4`
- Status: `execution_ready`

## Objective

Implement the bounded Phase 4 slice-1 runtime core:

- working memory
- episodic memory
- continuity memory
- memory review
- rollback-safe updates

This slice establishes the bounded current-state, replayable event-history, continuity-anchor, review, and rollback substrate needed before semantic, procedural, correction, promotion, compression, forgetting, or retirement logic can be completed.

## Exact Files Allowed To Touch

- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/__init__.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/working_memory.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/episodic_memory.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/continuity_memory.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/memory_review.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/rollback_safe_updates.py`

## Forbidden Files

- all Phase 4 verifier files
- all Phase 4 evidence files
- all Phase 4 demo files
- all plan files
- all Phase 5+ files
- semantic, procedural, correction, promotion, compression, forgetting, and retirement runtime files beyond what is strictly required for import-safe package structure

## Required Reads First

- `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- `projects/agifcore_master/03_design/MEMORY_MODEL.md`
- `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
- `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
- `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/workspace_state.py`
- `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/rollback_controller.py`
- `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/replay_ledger.py`

## Step-By-Step Method

1. Create the Phase 4 runtime package root if needed.
2. Implement a bounded working-memory surface for current turn/task state and promotable candidates.
3. Implement a replayable episodic-memory surface with correction-marker support.
4. Implement a continuity-memory surface for self-history anchors and supersession markers.
5. Implement a memory-review surface with explicit candidate and decision objects.
6. Implement rollback-safe update batching that uses the approved Phase 2 rollback and replay substrate directly.
7. Keep every store exportable and reloadable.
8. Keep every class and method Phase-4-only, with no graph or conversation behavior.

## Required Cross-Checks

- working memory is not reused as long-term memory
- episodic memory remains event-style and replayable
- continuity memory remains distinct from episodic and semantic memory
- review decisions have real enforcement meaning
- rollback-safe updates support restore or reject behavior
- no graph persistence or schemas appear
- no conversation behavior appears

## Exit Criteria

- all six slice-1 runtime files exist
- each file exposes a real bounded runtime surface
- the package can be imported by later verifiers without external path tricks
- no Phase 5 or conversation drift appears

## Handoff Target

`Test & Replay Lead`

## Anti-Drift Rule

Do not pad slice 1 by silently implementing the full remaining Phase 4 lifecycle surface under generic helper names.

## Proof That No Approval Is Implied

Slice-1 runtime creation is internal execution work only. Phase 4 remains `open` and requires later verification, audit, integration, validation, and explicit user approval.
