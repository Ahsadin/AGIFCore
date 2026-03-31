# P8-TC-WCPL-07 Phase 8 Slice 02A Causal Chain Reasoning

## Header

- Task Card ID: `P8-TC-WCPL-07`
- Phase: `8`
- Title: `Phase 8 Slice 02A Causal Chain Reasoning`
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
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/contracts.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/scientific_priors.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/entity_request_inference.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/world_region_selection.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/what_if_simulation.py`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/usefulness_scoring.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/causal_chain_reasoning.py`
- Forbidden Files:
  - every other Phase 8 runtime file
  - all test, output, handoff, and truth files
  - any Phase 9 and later artifact

## Objective

- Goal: implement typed, bounded causal-chain construction above priors and region selection and below current-world reasoning.
- Expected Outputs:
  - importable `causal_chain_reasoning.py`
  - typed `CausalChainSnapshot`
  - explicit missing-variable and weak-link visibility
- Non-Goals:
  - current-world reasoning
  - visible reasoning summaries
  - reflection
  - final answer text

## Work Method

1. Consume Phase 8 inference, selected priors, and region selection as read-only inputs.
2. Use Phase 6 world-model, what-if simulation, and usefulness exports as read-only evidence only.
3. Emit typed causal steps with explicit step kinds and evidence refs.
4. Preserve fail-closed and missing-variable behavior instead of prose-only certainty.

## Cross-Checks

- No more than `10` causal steps.
- No prose-only chain.
- No instrumentation or usefulness shortcut standing in for causal steps.
- No final answer text.
- No Phase 9 or Phase 10 behavior.

## Exit Criteria

- file imports cleanly
- output uses `CausalChainStep` and `CausalChainSnapshot`
- weak links and missing variables remain visible

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- This micro-slice is only a build step. Phase 8 remains `open`.
