# P8-TC-WCPL-10 Phase 8 Slice 02D Science Reflection

## Header

- Task Card ID: `P8-TC-WCPL-10`
- Phase: `8`
- Title: `Phase 8 Slice 02D Science Reflection`
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
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/causal_chain_reasoning.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/bounded_current_world_reasoning.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/science_reflection.py`
- Forbidden Files:
  - every other Phase 8 runtime file
  - all test, output, handoff, and truth files
  - any Phase 9 and later artifact

## Objective

- Goal: implement bounded post-run science reflection below meta-cognition.
- Expected Outputs:
  - importable `science_reflection.py`
  - typed `ScienceReflectionSnapshot`
  - bounded falsifier, missing-variable, and next-verification notes
- Non-Goals:
  - self-modeling
  - strategy journal
  - thinker tissue
  - theory fragments

## Cross-Checks

- No more than `6` reflection records.
- No Phase 10 record types or control loops.
- No final answer text.
- Reflection must have effect-bound notes, not empty labels.

## Exit Criteria

- file imports cleanly
- output uses `ScienceReflectionRecord` and `ScienceReflectionSnapshot`
- reflection stays below Phase 10 and tied to one reasoning run

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- This micro-slice is only a build step. Phase 8 remains `open`.
