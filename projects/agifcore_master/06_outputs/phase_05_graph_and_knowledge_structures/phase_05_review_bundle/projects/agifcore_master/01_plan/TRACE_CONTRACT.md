# Trace Contract

## Purpose

This file freezes the first-pass AGIFCore conversation and trace contract for Phase 1.

No runner, gateway, UI, or later conversation implementation may bypass this contract.

## Contract boundary

- The contract begins when a governed user or system turn is admitted into AGIFCore.
- The contract ends when the turn produces a response, abstention, clarification request, or governed stop state plus a memory-review reference when applicable.
- The contract is a runtime and evidence boundary, not an implementation claim.

## Frozen turn fields

Every governed turn must preserve these fields:

- `conversation_id`
- `turn_id`
- `user_intent`
- `active_context_refs`
- `planner_trace_ref`
- `simulation_trace_ref`
- `critic_trace_ref`
- `governance_trace_ref`
- `response_text`
- `abstain_or_answer`
- `memory_review_ref`

## Frozen richer conversation fields

These fields must remain explicit in the contract even if a later UI hides some of them:

- `discourse_mode`
- `support_state`
- `knowledge_gap_reason`
- `next_action`

## Allowed discourse modes

- `status`
- `explain`
- `compare`
- `teach`
- `analogy`
- `plan`
- `synthesize`
- `critique_rewrite`
- `clarify`
- `self_knowledge`
- `abstain`

## Allowed support states

- `grounded`
- `inferred`
- `search_needed`
- `unknown`

## Allowed knowledge-gap reasons

- `none`
- `ambiguous_request`
- `missing_local_evidence`
- `conflicting_state`
- `blocked_by_policy`
- `needs_fresh_information`
- `out_of_scope`

## Allowed next actions

- `answer`
- `clarify`
- `search_local`
- `search_external`
- `abstain`

## Allowed final answer modes

- `grounded_fact`
- `derived_estimate`
- `derived_explanation`
- `hypothesis`
- `clarify`
- `search_needed`
- `unknown`
- `abstain`

## Contract rules

- `conversation_id` and `turn_id` are the stable replay anchors.
- `response_text` is the user-facing surface, not the proof of cognition by itself.
- `abstain_or_answer` must allow honest outcomes when support is weak or blocked.
- `planner_trace_ref`, `simulation_trace_ref`, `critic_trace_ref`, and `governance_trace_ref` are trace links, not optional decoration.
- `memory_review_ref` is required whenever a turn changes what AGIFCore should retain, revise, compress, or reject.
- `support_state` and `knowledge_gap_reason` must make weak-support states visible instead of hiding them in fluent language.
- `next_action` must describe the governed next step, not a hidden background behavior.
- The allowed values above are frozen Phase 1 contract boundaries, not proof that the later runtime implementation is already complete.
- `final_answer_mode` classification must stay honest about evidence strength and may not launder `search_needed`, `unknown`, or `abstain` into a stronger-looking answer mode.

## Runtime-split alignment

- The runner owns turn execution and trace production.
- The local gateway/API owns contract transport and validation.
- The local desktop UI owns presentation only and may not alter contract truth.
- Export surfaces `state_export`, `trace_export`, and `memory_review_export` must preserve this contract.

## First-pass dependency notes

- This first-pass contract is aligned to the frozen master plan, the system constitution, and the current requirement pack.
- Final field-level schema details still need later refinement against the full conversation and product-runtime models.
- Any later change to this contract requires explicit Governor review because contract drift would affect conversation, product runtime, and evidence packaging together.

## Cross-References

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
