# P8-TC-WCPL-05 Phase 8 Slice 01B Entity Request Inference

## Header

- Task Card ID: `P8-TC-WCPL-05`
- Phase: `8`
- Title: `Phase 8 Slice 01B Entity Request Inference`
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
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/question_interpretation.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/entity_request_inference.py`
- Forbidden Files:
  - every other Phase 8 runtime file
  - all test, output, handoff, and truth files
  - any Phase 9 and later artifact

## Objective

- Goal: implement the bounded entity/request inference engine above Phase 7 interpretation and below region selection.
- Expected Outputs:
  - importable `entity_request_inference.py`
  - typed `EntityRequestInferenceSnapshot`
  - bounded candidate generation up to the Phase 8 ceiling of `16`
- Non-Goals:
  - region selection
  - causal chains
  - current-world reasoning
  - visible reasoning
  - reflection
  - final answer text

## Work Method

1. Consume Phase 7 intake and interpretation as read-only inputs.
2. Detect likely entity label, entity class, request type, live-current cues, science topic cues, hidden-variable cues, and ambiguity markers.
3. Emit typed candidates and one bounded selected candidate when justified.
4. Preserve honesty when support-state hints already show weak or fresh-information-needed support.

## Cross-Checks

- No more than `16` candidates.
- No `response_text`.
- No `discourse_mode`.
- No Phase 9 runtime import.
- No direct mutation of any Phase 7 state.

## Exit Criteria

- file imports cleanly
- output uses `EntityRequestCandidate` and `EntityRequestInferenceSnapshot`
- live-current cues, self-knowledge cues, and ambiguity markers remain visible

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- This micro-slice is only a build step. Phase 8 remains `open`.
