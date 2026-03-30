# P4-NOTE-ACL-02 Phase 4 Boundary Notes

This note records the requested Phase 4 boundary check for `P4-TC-ACL-02`.

## Scope and inspection basis

- Task card: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-ACL-02_PHASE_4_BOUNDARY_CHECK.md`
- Phase 4 plan: `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- Design controls:
  - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
- Approved Phase 2 kernel surfaces inspected:
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/workspace_state.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/rollback_controller.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/replay_ledger.py`
  - `projects/agifcore_master/04_execution/phase_02_fabric_kernel_and_workspace/agifcore_phase2_kernel/quarantine_controller.py`
- Approved Phase 3 structure surfaces inspected:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/cell_contracts.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/tissue_manifests.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_manifest.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/split_merge_rules.py`

## Current status

Current status is `boundary_guard_defined_with_no_phase_4_runtime_surfaces_present`.

No `projects/agifcore_master/04_execution/phase_04_memory_planes/`, `projects/agifcore_master/05_testing/phase_04_memory_planes/`, or `projects/agifcore_master/06_outputs/phase_04_memory_planes/` package exists in this worktree at the time of inspection.

That means this note is a truthful boundary-control note against:

- the approved Phase 2 kernel seams
- the approved Phase 3 structure seams
- the locked Phase 4 plan and design rules
- the present absence of Phase 4 runtime code

It is not a claim that a Phase 4 runtime package has already passed code review.

## Main boundary findings

### 1. Memory-plane separation remains a locked requirement, not an already-built runtime fact

The Phase 4 plan and memory model clearly keep these planes separate:

- working memory
- episodic memory
- semantic memory
- procedural memory
- continuity memory

The inspected Phase 2 and Phase 3 files do not collapse those planes into one shared runtime store today.

Supporting evidence:

- `workspace_state.py` exposes a bounded shared workspace state and a `memory_review_export()` surface that is references-only and explicitly says:
  - no semantic memory
  - no procedural memory
  - no graph persistence
- `cell_contracts.py`, `tissue_manifests.py`, and `bundle_manifest.py` stay structural and schema-oriented rather than acting as hidden long-term memory stores.

Boundary conclusion:

- no current inspected file contradicts the required working/episodic/semantic/procedural/continuity separation
- the separation is still mostly a governed contract to be preserved during later Phase 4 implementation

### 2. Correction, review, and lifecycle boundaries are anchored below Phase 4 and must stay layered

The required correction and lifecycle path is consistent with the approved lower layers:

- review cannot be skipped because the memory model makes review mandatory
- rollback-safe updates must stay anchored to Phase 2 rollback and replay seams
- quarantine remains a separate control path and cannot be replaced by ad hoc memory mutation

Supporting evidence:

- `rollback_controller.py` provides explicit bounded rollback snapshots and restore points
- `replay_ledger.py` provides deterministic replay anchors tied to trace and state hashes
- `quarantine_controller.py` keeps explicit quarantine records with release flow
- `workspace_state.py` keeps memory review as references attached to workspace state, not as silent long-term memory writes

Boundary conclusion:

- correction handling, promotion, compression, forgetting, retirement, and review must be built above these controls
- they must not replace or duplicate rollback, replay, or quarantine behavior that already belongs to Phase 2

### 3. No Phase 2 kernel reimplementation is present in the inspected scope

The approved kernel already owns:

- shared workspace state
- rollback snapshots
- replay ledger behavior
- quarantine records

The inspected scope shows no Phase 4 artifact attempting to re-author those behaviors, because no Phase 4 runtime package exists yet.

Boundary conclusion:

- there is currently no observed Phase 2 kernel reimplementation in the owned Phase 4 note scope
- later auditors should reject any Phase 4 code that introduces a second rollback engine, replay ledger, quarantine subsystem, or separate memory-control substrate

### 4. No Phase 3 structure drift is present in the inspected scope

The approved Phase 3 files keep structure concerns separate:

- `cell_contracts.py` validates role, tissue, trust, and policy envelope boundaries
- `tissue_manifests.py` explicitly says no memory or graph logic is allowed there
- `bundle_manifest.py` stays focused on bundle metadata, schema linkage, and provenance fields
- `split_merge_rules.py` governs structural split and merge decisions, not memory lifecycle decisions

Boundary conclusion:

- there is no observed Phase 4 change drifting Phase 3 structure files, because those files were only inspected, not modified
- later Phase 4 work must not hide memory planes inside manifests, bundle payload inventory, or split/merge policy envelopes

### 5. No Phase 5 graph logic is present in the inspected scope

The graph stack model keeps descriptor, skill, concept, and transfer graphs for later Phase 5 implementation.

The inspected lower-layer runtime files do not define:

- graph schemas
- graph persistence
- graph traversal
- graph conflict rules
- graph ranking logic

`workspace_state.py` also explicitly says there is no graph persistence in its memory hook surface.

Boundary conclusion:

- no current inspected file leaks Phase 5 graph implementation into the present Phase 4 note scope
- later Phase 4 work may emit graph-ready references only, not graph behavior

### 6. No Phase 7 conversation behavior is present in the inspected scope

The conversation model keeps interpretation, discourse selection, answer planning, and language realization above memory.

The inspected Phase 2 and Phase 3 files do not implement:

- user-turn interpretation
- discourse-mode policy logic for conversation behavior
- answer planning
- language generation behavior
- self-knowledge dialogue behavior

Boundary conclusion:

- no current inspected file leaks Phase 7 conversation behavior into the present Phase 4 note scope
- later Phase 4 work must expose only memory retrieval and review hooks, not conversation behavior

## Explicit seam risks for later audit

These are the most likely places for later Phase 4 drift. They should be checked directly when runtime code appears.

1. Workspace-overload risk:
   `workspace_state.py` already carries turn records, refs, and memory review refs. Phase 4 must not turn workspace state into a giant mixed memory store.

2. Review-bypass risk:
   the memory model requires review, but later implementation may try to write directly from working or episodic state into semantic, procedural, or continuity planes without an explicit review record.

3. Rollback-shadow risk:
   later memory correction code may try to create its own undo path instead of using Phase 2 rollback, replay, and quarantine anchors.

4. Structure-smuggling risk:
   Phase 4 code may try to place memory payloads into `policy_envelope`, bundle payload inventory, or split/merge records because those fields are flexible containers.

5. Graph-creep risk:
   "graph-ready reference" work may quietly become graph schema or edge logic ahead of Phase 5.

6. Conversation-creep risk:
   retrieval helpers may quietly become answer-composition or discourse-selection logic ahead of Phase 7.

7. Continuity-overreach risk:
   continuity memory may be used as a catch-all profile store instead of a narrow self-history and correction-aware continuity surface.

8. Lifecycle-overlap risk:
   promotion, compression, forgetting, and retirement may be mixed into structural split/merge decisions even though those are different control domains.

## Auditor watch checklist

- confirm each long-lived record is plane-specific rather than a generic blob
- confirm promotion from working or episodic state always leaves provenance and review evidence
- confirm correction flow uses rollback, replay, and quarantine anchors instead of replacing them
- confirm no memory payload is hidden in Phase 3 manifests or policy envelopes
- confirm no graph schema or traversal logic appears in Phase 4 files
- confirm no answer-planning or language behavior appears in Phase 4 files
- confirm continuity memory stays narrow and correction-aware

## Final statement

Based on the inspected Phase 2 kernel files, inspected Phase 3 structure files, locked Phase 4 plan, and the current absence of Phase 4 runtime/test/output packages, the boundary guard is clear:

- Phase 4 memory planes must stay separate
- correction, review, and lifecycle behavior must layer on top of Phase 2 controls
- Phase 4 must not reimplement the Phase 2 kernel
- Phase 4 must not drift the Phase 3 structure layer
- Phase 4 must not implement Phase 5 graph logic
- Phase 4 must not implement Phase 7 conversation behavior

No approval is implied by this note. This note does not approve Phase 4, any future Phase 4 runtime package, or any later phase.
