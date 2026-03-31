# P8-TC-WCPL-06 Phase 8 Slice 01C World Region Selection

## Header

- Task Card ID: `P8-TC-WCPL-06`
- Phase: `8`
- Title: `Phase 8 Slice 01C World Region Selection`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `World & Conversation Pod Lead`
- Supporting Roles: `Architecture & Contract Lead`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-WCPL-03_PHASE_8_SLICE_01_RUNTIME_FOUNDATION.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/entity_request_inference.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/world_model.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/target_domains.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/world_region_selection.py`
- Forbidden Files:
  - every other Phase 8 runtime file
  - all test, output, handoff, and truth files
  - any Phase 9 and later artifact

## Objective

- Goal: implement the bounded world-region selector above entity/request inference and below causal reasoning.
- Expected Outputs:
  - importable `world_region_selection.py`
  - typed `WorldRegionSelectionSnapshot`
  - bounded candidate generation up to the Phase 8 ceiling of `8`
- Non-Goals:
  - causal chains
  - current-world reasoning
  - visible reasoning
  - reflection
  - final answer text

## Work Method

1. Consume Phase 8 entity/request inference as read-only input.
2. Use Phase 6 target-domain and world-model exports as read-only evidence inputs.
3. Emit bounded region candidates with explicit reason codes and supporting refs.
4. Preserve unresolved output when no safe region can be selected.

## Cross-Checks

- No more than `8` region candidates.
- No ad hoc default region bluff.
- No mutation of Phase 6 state.
- No final answer text.
- No Phase 9 or Phase 10 behavior.

## Exit Criteria

- file imports cleanly
- output uses `WorldRegionCandidate` and `WorldRegionSelectionSnapshot`
- unresolved cases remain unresolved instead of being forced into false precision

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- This micro-slice is only a build step. Phase 8 remains `open`.
