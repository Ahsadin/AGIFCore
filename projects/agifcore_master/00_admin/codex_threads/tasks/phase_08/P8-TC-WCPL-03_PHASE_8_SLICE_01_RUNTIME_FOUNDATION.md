# P8-TC-WCPL-03 Phase 8 Slice 01 Runtime Foundation

## Header

- Task Card ID: `P8-TC-WCPL-03`
- Phase: `8`
- Title: `Phase 8 Slice 01 Runtime Foundation`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `World & Conversation Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-WCPL-02_PHASE_8_SCIENCE_WORLD_AWARENESS_IMPLEMENTATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/question_interpretation.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/contracts.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/world_model.py`
  - donor files cited in the Phase 8 plan for scientific priors and public reasoning lineage

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/__init__.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/scientific_priors.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/entity_request_inference.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/world_region_selection.py`
- Forbidden Files:
  - any test, output, handoff, or truth file
  - `science_world_turn.py`
  - `causal_chain_reasoning.py`
  - `bounded_current_world_reasoning.py`
  - `visible_reasoning_summaries.py`
  - `science_reflection.py`
  - any Phase 9 and later artifact

## Objective

- Goal: land the first bounded runtime slice for Phase 8: prior selection, entity/request inference, and world-region selection.
- Expected Outputs:
  - importable runtime foundation files for slice 1
  - no final answer generation
  - no current-world exact fact output
- Non-Goals:
  - causal-chain construction
  - current-world reasoning
  - visible reasoning summaries
  - reflection
  - phase approval

## Work Method

1. Keep `contracts.py` as the typed base and adjust it only if the slice cannot work otherwise.
2. Implement `scientific_priors.py` first.
3. Implement `entity_request_inference.py` second.
4. Implement `world_region_selection.py` third.
5. Export the slice in `__init__.py`.

## Cross-Checks

- No donor runtime imports from Phase 8C or Phase 9.
- No final `response_text`.
- No `discourse_mode`.
- No single giant function covering all slice behaviors.
- Prior selection must stay within the ceiling of `12`.
- Entity/request inference candidates must stay within the ceiling of `16`.
- Region candidates must stay within the ceiling of `8`.

## Exit Criteria

- all owned files import cleanly
- slice 1 stays inside the boundary record
- later causal-chain and current-world files are still untouched

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- Slice completion is only an internal execution milestone. Phase 8 remains `open`.
