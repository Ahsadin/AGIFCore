# P8-TC-WCPL-11 Phase 8 Slice 03 Coordinator And Exports

## Header

- Task Card ID: `P8-TC-WCPL-11`
- Phase: `8`
- Title: `Phase 8 Slice 03 Coordinator And Exports`
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
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
  - all completed Phase 8 runtime modules

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/__init__.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/science_world_turn.py`
- Forbidden Files:
  - all test, output, handoff, and truth files
  - any Phase 9 and later artifact

## Objective

- Goal: wire the completed Phase 8 modules together without collapsing them into one opaque function.
- Expected Outputs:
  - thin `science_world_turn.py`
  - package exports in `__init__.py`
- Non-Goals:
  - hidden rewrite engine
  - final answer text
  - replacing Phase 7 conversation execution

## Cross-Checks

- `science_world_turn.py` stays thin and sequencing-only.
- No final `response_text`.
- No `discourse_mode`.
- No Phase 9 or Phase 10 behavior.

## Exit Criteria

- coordinator imports cleanly
- package exports are explicit
- the thin-coordinator rule remains true

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- This micro-slice is only a build step. Phase 8 remains `open`.
