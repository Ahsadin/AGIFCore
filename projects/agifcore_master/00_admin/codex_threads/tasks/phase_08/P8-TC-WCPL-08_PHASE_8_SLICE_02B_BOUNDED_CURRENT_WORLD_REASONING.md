# P8-TC-WCPL-08 Phase 8 Slice 02B Bounded Current World Reasoning

## Header

- Task Card ID: `P8-TC-WCPL-08`
- Phase: `8`
- Title: `Phase 8 Slice 02B Bounded Current World Reasoning`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `World & Conversation Pod Lead`
- Supporting Roles: `Constitution Keeper`
- Allowed Models: `gpt-5.3-codex`
- Build Pod Agent Session ID: `pending_subagent_assignment`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/entity_request_inference.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/causal_chain_reasoning.py`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/support_state_logic.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/bounded_current_world_reasoning.py`
- Forbidden Files:
  - every other Phase 8 runtime file
  - all test, output, handoff, and truth files
  - any Phase 9 and later artifact

## Objective

- Goal: implement the fail-closed freshness and bounded-local-evidence layer for current-world questions.
- Expected Outputs:
  - importable `bounded_current_world_reasoning.py`
  - typed `BoundedCurrentWorldSnapshot`
  - explicit `needs_fresh_information` and `live_measurement_required` handling
- Non-Goals:
  - visible reasoning summaries
  - reflection
  - final answer text
  - external search execution

## Work Method

1. Consume Phase 8 inference and causal-chain state as read-only inputs.
2. Preserve Phase 7 honesty semantics for `search_needed`, `unknown`, and fresh-information gaps.
3. Emit bounded-local-support refs only when the local evidence is strong enough.
4. Fail closed on exact current fact claims when freshness is missing.

## Cross-Checks

- No external search execution.
- No unsupported exact current-fact allowance.
- No laundering of weak support into stronger support.
- No final answer text.
- No Phase 9 or Phase 10 behavior.

## Exit Criteria

- file imports cleanly
- output uses `BoundedCurrentWorldSnapshot`
- live-current requests fail closed when freshness is missing

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- This micro-slice is only a build step. Phase 8 remains `open`.
