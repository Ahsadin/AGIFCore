# P8-TC-WCPL-09 Phase 8 Slice 02C Visible Reasoning Summaries

## Header

- Task Card ID: `P8-TC-WCPL-09`
- Phase: `8`
- Title: `Phase 8 Slice 02C Visible Reasoning Summaries`
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
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/causal_chain_reasoning.py`
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/bounded_current_world_reasoning.py`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/04_execution/phase_08_science_and_world_awareness/agifcore_phase8_science_world_awareness/visible_reasoning_summaries.py`
- Forbidden Files:
  - every other Phase 8 runtime file
  - all test, output, handoff, and truth files
  - any Phase 9 and later artifact

## Objective

- Goal: implement the bounded public reasoning summary surface for Phase 8.
- Expected Outputs:
  - importable `visible_reasoning_summaries.py`
  - typed `VisibleReasoningSummary`
  - only the four approved public summary fields plus allowed public metadata
- Non-Goals:
  - final answer text
  - hidden chain-of-thought
  - rhetorical polish

## Cross-Checks

- Summary stays within `1200` characters.
- Only `what_is_known`, `what_is_inferred`, `uncertainty`, and `what_would_verify` as the summary fields.
- No freeform monologue.
- No Phase 9 or Phase 10 behavior.

## Exit Criteria

- file imports cleanly
- output uses `VisibleReasoningSummary`
- summary remains public-summary-only and evidence-linked

## Handoff Target

- `Program Governor`

## Explicit Proof That No Approval Is Implied

- This micro-slice is only a build step. Phase 8 remains `open`.
