# P4-NOTE-ACL-03 Phase 4 Slice-2 Boundary Notes

This note records the requested slice-2 boundary check for `P4-TC-ACL-03`.

## Scope and inspection basis

- Task card:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-ACL-03_PHASE_4_SLICE_2_LONG_TERM_BOUNDARY_CHECK.md`
- Phase 4 plan:
  - `projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`
- Design controls:
  - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
- Slice-1 merge baseline inspected on this branch:
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/__init__.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/working_memory.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/episodic_memory.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/continuity_memory.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/memory_review.py`
  - `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/rollback_safe_updates.py`
- Slice-1 evidence package present on this branch:
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_working_memory_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_episodic_memory_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_continuity_memory_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_memory_review_report.json`
  - `projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_rollback_safe_updates_report.json`
- Slice-2 runtime expectation checked against:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-MGPL-04_PHASE_4_SLICE_2_LONG_TERM_PLANES_AND_CORRECTION.md`

## Current branch truth

Current status is `slice_1_baseline_present_slice_2_runtime_not_present`.

The slice-1 merge baseline exists on this branch and exports only:

- working memory
- episodic memory
- continuity memory
- memory review
- rollback-safe updates

The expected slice-2 runtime files do not exist on this branch at inspection time:

- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/semantic_memory.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/procedural_memory.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/promotion_pipeline.py`
- `projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/correction_handling.py`

That means this note can truthfully confirm the slice-1 boundary baseline and the absence of slice-2 drift, but it cannot claim that slice-2 runtime behavior is already implemented or approved.

## Boundary findings

### 1. Semantic memory remains abstraction-only by current branch truth, because no semantic runtime surface exists yet

The Phase 4 plan says semantic memory must contain reviewed abstractions only and must not hold raw turn transcript, scratchpad state, or executable procedures.

On this branch:

- `working_memory.py` keeps scratchpad state and promotable candidates in the current-turn surface
- `episodic_memory.py` keeps replayable event history and correction markers
- `continuity_memory.py` keeps continuity anchors
- `__init__.py` does not export any semantic-memory surface
- no `semantic_memory.py` file exists

Boundary conclusion:

- no observed runtime surface currently collapses scratchpad or episodic history into semantic memory
- this is a boundary pass by absence, not a validated semantic implementation
- later audit must still inspect whether the eventual `semantic_memory.py` stores only reviewed abstractions

### 2. Procedural memory remains procedure-only by current branch truth, because no procedural runtime surface exists yet

The Phase 4 plan says procedural memory must hold reviewed reusable procedures with constraints and provenance, not generic facts or episodic timeline records.

On this branch:

- no `procedural_memory.py` file exists
- `working_memory.py` allows candidates to target `procedural`, but only as pending working-memory candidates
- `memory_review.py` can review a candidate for a target plane, but it does not itself implement a procedural store
- `__init__.py` exports no procedural-memory surface

Boundary conclusion:

- no observed runtime surface currently stores semantic facts and procedures in one long-term plane
- the baseline preserves the distinction by not implementing the procedural plane yet
- later audit must still confirm that the eventual procedural surface stores reusable procedures only

### 3. Promotion remains review-gated in the current baseline

This is the strongest positive boundary result from the existing code.

Supporting observations:

- `working_memory.py` creates promotable candidates with `status="pending_review"` by default
- `working_memory.py` records `review_ref` and requires explicit status change through `mark_candidate_reviewed(...)`
- `memory_review.py` creates explicit `ReviewCandidate` records, review decisions, assigned tiers, reviewer identity, and decision refs
- `memory_review.py` exposes `approved_candidates(...)` instead of silently promoting everything
- no `promotion_pipeline.py` file exists yet, so there is no separate slice-2 code path that bypasses review

Boundary conclusion:

- current branch behavior keeps promotion gated by explicit review records
- no observed slice-2 runtime exists that could bypass that gate today
- the future promotion pipeline is a seam risk because it will be the first place where approved candidates are turned into long-term plane writes

### 4. Correction remains rollback-safe and continuity-aware in the current baseline

This is also supported by existing code, but only at the slice-1 substrate level.

Supporting observations:

- `rollback_safe_updates.py` routes batch updates through Phase 2 `RollbackController` snapshots and `ReplayLedger` records
- `rollback_safe_updates.py` returns explicit `applied`, `rejected`, or `restored` results rather than mutating state without recovery
- `episodic_memory.py` preserves correction markers and replacement-event references on event history
- `continuity_memory.py` preserves `superseded_by` and `correction_refs` on continuity anchors
- no `correction_handling.py` file exists yet, so no slice-2 layer currently overrides or replaces the rollback-safe substrate

Boundary conclusion:

- the current baseline preserves the required rollback-safe and continuity-aware substrate
- this is not yet a full slice-2 correction-flow pass, because the dedicated correction layer is still absent
- later audit must verify that `correction_handling.py` uses these slice-1 seams instead of inventing a second undo or correction truth path

### 5. No graph implementation is present in the inspected slice-1 plus slice-2 branch state

`GRAPH_STACK_MODEL.md` keeps graph schemas, persistence, traversal, ranking, and conflict rules for Phase 5.

On this branch:

- no graph module appears in the Phase 4 runtime package
- `working_memory.py` uses plain `target_plane` labels and provenance refs, not graph nodes or edges
- `memory_review.py` uses review refs and plane names, not graph schemas
- the missing slice-2 long-term files mean there is still no graph-facing implementation to inspect

Boundary conclusion:

- no graph implementation is present in the current baseline
- later slice-2 work must keep any graph alignment as plain references only

### 6. No conversation behavior is present in the inspected slice-1 plus slice-2 branch state

`CONVERSATION_MODEL.md` keeps turn interpretation, discourse selection, answer planning, and language realization above memory.

On this branch:

- the Phase 4 runtime package contains memory stores, review state, and rollback-safe update helpers only
- no user-turn interpretation logic appears in the inspected files
- no discourse-mode or answer-composition behavior appears
- the missing slice-2 files mean there is still no new memory-driven conversation behavior to inspect

Boundary conclusion:

- no conversation behavior is present in the current Phase 4 branch state
- later slice-2 work must not let promotion or correction code become a hidden answer-planning or self-knowledge surface

## Concrete seam risks for later audit

1. Candidate-payload leak risk:
   `working_memory.py` allows arbitrary mapping payloads for promotable candidates. Later slice-2 code could move raw scratchpad-like payloads into semantic or procedural memory unless it validates abstraction-only versus procedure-only shape.

2. Review-to-write gap risk:
   `memory_review.py` can approve candidates, but the missing `promotion_pipeline.py` is where review-gated policy could be preserved or broken. Audit must check that only approved candidates with provenance are promotable.

3. Plane-collapse risk:
   because slice-2 stores do not exist yet, later code may be tempted to use one generic long-term record structure for both semantic and procedural memory. Audit must reject that collapse.

4. Rollback-shadow risk:
   `rollback_safe_updates.py` already provides the mutation substrate. Audit must reject any `correction_handling.py` logic that creates a separate rollback, replay, or restore path.

5. Continuity-overwrite risk:
   `continuity_memory.py` already tracks supersession and correction refs. Audit must check that correction code updates continuity through explicit supersession-aware records rather than in-place silent overwrite.

6. Graph-creep risk:
   later slice-2 work may introduce graph-like node ids, edges, traversal helpers, or persistence tables under the label of "graph-ready references." Audit must reject that drift before Phase 5.

7. Conversation-creep risk:
   later correction or promotion code may start classifying user intent, selecting discourse behavior, or composing self-explanations. Audit must reject that drift before Phase 7.

8. Approval-language risk:
   because the slice-1 baseline is present and slice-2 task cards now exist, later summaries may overstate readiness. Audit must keep "runtime files absent" and "not approved" language explicit until the four slice-2 files, tests, and evidence actually exist.

## Final statement

This branch currently preserves the requested slice-2 boundaries in the only truthful way available today:

- semantic memory is still abstraction-only by contract and by current runtime absence
- procedural memory is still procedure-only by contract and by current runtime absence
- promotion is still review-gated in the existing slice-1 baseline
- correction is still rollback-safe and continuity-aware in the existing slice-1 baseline
- no graph implementation is present
- no conversation behavior is present

The main remaining risks are at the exact seams where slice-2 runtime has not been landed yet: semantic storage shape, procedural storage shape, promotion execution, and correction orchestration.

No approval is implied by this note. It does not approve slice 2, Phase 4, or any later phase. Phase 4 remains `open`.
