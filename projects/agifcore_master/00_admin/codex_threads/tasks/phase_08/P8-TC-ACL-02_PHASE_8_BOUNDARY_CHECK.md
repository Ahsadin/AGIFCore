# P8-TC-ACL-02 Phase 8 Boundary Check

## Header

- Task Card ID: `P8-TC-ACL-02`
- Phase: `8`
- Title: `Phase 8 Boundary Check`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-31`

## Role Assignment

- Active Build Role: `Architecture & Contract Lead`
- Supporting Roles: `Constitution Keeper`
- Allowed Models: `gpt-5.4`
- Build Pod Agent Session ID: `this_thread`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
  - `projects/agifcore_master/04_execution/phase_07_conversation_core/agifcore_phase7_conversation/`
  - `projects/agifcore_master/04_execution/phase_06_world_model_and_simulator/agifcore_phase6_world_simulator/`
  - direct donor files named in `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-TC-ACL-02_PHASE_8_BOUNDARY_CHECK.md`
- Forbidden Files:
  - any runtime, testing, or output file
  - any Phase 9 and later artifact
- Allowed Folders:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`
  - `projects/agifcore_master/06_outputs/`

## Branch And Worktree

- Branch Name: `codex/tc-p8-tc-wcpl-02-phase-8-science-world-awareness-implementation`
- Worktree Path: `<repo_root>`
- Rollback Tag Name: `rollback/P8-TC-ACL-02/<yyyymmdd-hhmm>`

## Objective

- Goal: convert this task file into the concrete execution-time boundary record for Phase 8 so later implementation, audit, and governor replay use the same hard seams.
- Expected Outputs:
  - this boundary check record with exact allowed seams, forbidden leaks, contract expectations, and anti-cheat checks
- Non-Goals:
  - runtime implementation
  - verifier implementation
  - phase approval
- Inherited Lineage Touched: `yes`
- Source Cartographer Required: `only if donor ambiguity appears`
- Meta & Growth Danger-Zone Controls Required: `no`

## Verification

- Required Test Commands:
  - full Phase 8 verifier family after implementation lands
- Required Build Commands:
  - `n/a`
- Required Verifier Paths:
  - `projects/agifcore_master/05_testing/phase_08_science_and_world_awareness/`
- Required Evidence Output Paths:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/`
- Required Demo Path:
  - `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/`

## Handoff Records

- Audit Report Path: `projects/agifcore_master/00_admin/codex_threads/tasks/phase_08/P8-AUDIT-01_PHASE_8_FINAL_PACKAGE_AUDIT_REPORT.md`
- Extra Audit Report Path: `n/a`
- Governor Verification Record Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_GOVERNOR_VERIFICATION_RECORD.md`
- Validation Request Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_VALIDATION_REQUEST.md`
- User Verdict Path: `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_08_USER_VERDICT.md`
- Additional Human Demo Checkpoint Path: `n/a`

## Approval Chain

- Auditor: `Anti-Shortcut Auditor`
- Merge Arbiter: `Merge Arbiter`
- Program Governor: `Program Governor`
- User: `User`

## Completion Checklist

- scope stayed inside owned files
- forbidden files were not touched
- required tests ran
- required evidence was produced
- demo path is ready
- rollback path is defined

## Record Status

- Record type: `execution_time_boundary_record`
- Planning authority basis: approved Phase 8 plan plus inspected Phase 6 and Phase 7 runtime surfaces
- Runtime judgment status: `boundary_locked_for_later_execution`
- Approval claim: `none`
- Closure claim: `none`

## Inspected Basis

- Frozen plan basis:
  - `projects/agifcore_master/01_plan/PHASE_08_SCIENCE_AND_WORLD_AWARENESS.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
- Design basis:
  - `projects/agifcore_master/03_design/CONVERSATION_MODEL.md`
  - `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
  - `projects/agifcore_master/03_design/SIMULATOR_MODEL.md`
  - `projects/agifcore_master/03_design/COGNITIVE_PRIORS.md`
- Inspected AGIFCore runtime seams:
  - Phase 7: `raw_text_intake.py`, `question_interpretation.py`, `support_state_logic.py`, `answer_contract.py`, `utterance_planner.py`, `surface_realizer.py`, `conversation_turn.py`, `anti_generic_filler.py`, `clarification.py`
  - Phase 6: `target_domains.py`, `world_model.py`, `candidate_futures.py`, `what_if_simulation.py`, `fault_lanes.py`, `pressure_lanes.py`, `conflict_lanes.py`, `overload_lanes.py`, `instrumentation.py`, `usefulness_scoring.py`
- Inspected donor basis named by the plan:
  - Phase 8B donor answer-contract and public-summary contracts
  - Phase 8B donor grounded-fact and derived-science fail-closed lanes
  - Phase 8C donor `ScientificPriorCell` and meta-growth records
  - Phase 9 donor messy-question signal vocabulary in `UnifiedQuestionAnalysis`

## Allowed Phase 8 Module Boundary

- The later Phase 8 runtime must stay split into these modules only:
  - `contracts.py`
  - `scientific_priors.py`
  - `entity_request_inference.py`
  - `world_region_selection.py`
  - `causal_chain_reasoning.py`
  - `bounded_current_world_reasoning.py`
  - `visible_reasoning_summaries.py`
  - `science_reflection.py`
  - `science_world_turn.py`
- `science_world_turn.py` must remain a thin coordinator. It may sequence the bounded modules, but it must not absorb prior selection, messy-question inference, region selection, causal-chain construction, current-world honesty, visible-summary rendering, and reflection into one opaque reasoning function.

## Exact Allowed Phase 7 Interface Seams

These are the only approved Phase 7 runtime seams for Phase 8 consumption. All are read-only.

| Allowed seam | Inspected source | Exact allowed Phase 8 use | Hard stop |
| --- | --- | --- | --- |
| `RawTextIntakeRecord` | `raw_text_intake.py` | preserve raw user wording for messy-question interpretation, entity extraction, and audit replay | no mutation, no new intake normalization rules stored back into Phase 7 |
| `agifcore.phase_07.question_interpretation.v1` | `question_interpretation.py` | consume interpreted question shape, ambiguity markers, live-current cues, and request framing as input to Phase 8 entity/request inference | no direct replacement of Phase 7 question interpretation and no hidden Phase 9 analyzer import |
| `agifcore.phase_07.support_state_logic.v1` | `support_state_logic.py` | preserve honesty state, especially `grounded`, `inferred`, `search_needed`, `unknown`, `knowledge_gap_reason`, and `next_action` constraints | no silent upgrade of weak support and no downgrade of `needs_fresh_information` into a stronger answer |
| `agifcore.phase_07.answer_contract.v1` | `answer_contract.py` | validation and demo linkage only so Phase 8 evidence later lines up with the existing turn contract | not a science-truth source and not permission for Phase 8 to author final response text |

### Phase 7 surfaces that Phase 8 must not steal or replace

- `conversation_turn.py` may not become a Phase 8 dependency or be reimplemented inside Phase 8.
- `utterance_planner.py` remains the owner of discourse planning. Phase 8 may not choose `discourse_mode`.
- `surface_realizer.py` remains the owner of final `response_text`.
- `anti_generic_filler.py` remains a Phase 7 guardrail, not a Phase 8 correctness path.
- `clarification.py` remains Phase 7 behavior. Phase 8 may surface ambiguity evidence but may not replace the clarify path itself.
- `self_knowledge_surface.py` is not an approved Phase 8 seam.

## Exact Allowed Phase 6 Interface Seams

These are the only approved Phase 6 runtime seams for Phase 8 consumption. All are read-only evidence inputs.

| Allowed seam | Inspected source | Exact allowed Phase 8 use | Hard stop |
| --- | --- | --- | --- |
| `agifcore.phase_06.target_domains.v1` | `target_domains.py` | bound domain and region context candidates | no ad hoc region truth outside approved domain exports |
| `agifcore.phase_06.world_model.v1` | `world_model.py` | ground entities, relationships, and local support references for region selection and causal chains | no reinterpretation as raw memory or graph ownership |
| `agifcore.phase_06.candidate_futures.v1` | `candidate_futures.py` | bounded scenario context when useful for scientific explanations | no speculative answer inflation |
| `agifcore.phase_06.what_if_simulation.v1` | `what_if_simulation.py` | trace-linked support for typed causal-chain steps | no rerun inside Phase 8 and no hidden simulator execution during summary generation |
| `agifcore.phase_06.fault_lanes.v1` | `fault_lanes.py` | expose failure pressure or fail-closed conditions | no conversion into final prose without typed chain support |
| `agifcore.phase_06.pressure_lanes.v1` | `pressure_lanes.py` | bounded context about system stressors | no unsupported causal shortcut |
| `agifcore.phase_06.conflict_lanes.v1` | `conflict_lanes.py` | preserve contradictions and conflict markers | no silent conflict laundering |
| `agifcore.phase_06.overload_lanes.v1` | `overload_lanes.py` | surface overload or boundedness warnings | no ignored overload state when building a confident answer |
| `agifcore.phase_06.instrumentation.v1` | `instrumentation.py` | traceability and evidence linkage only | not a substitute for causal reasoning |
| `agifcore.phase_06.usefulness_scoring.v1` | `usefulness_scoring.py` | usefulness hints may rank support relevance | may not replace explicit causal-chain steps |

### Additional approved read-only dependencies

- Phase 8 may also read approved Phase 4 reviewed-memory and continuity exports.
- Phase 8 may also read approved Phase 5 support-selection, concept, provenance, and trust exports.
- Phase 8 may not mutate any Phase 4 or Phase 5 store or package.

## Exact Forbidden Leaks From Phase 9

The plan allows Phase 8 to reuse some donor vocabulary from Phase 9 question analysis, but not Phase 9 runtime behavior.

- Do not import or rebuild Phase 9 `ActivationPlan`, `SupportGraph`, `SupportCapabilityHook`, `ReasoningAttempt`, or Phase 9 memory-operation surfaces as part of Phase 8.
- Do not add open-support-graph orchestration, composer logic, or multi-attempt revision loops.
- Do not add teaching-quality rewrite engines, comparison engines, synthesis engines, analogy engines, or audience-aware explanation optimization as a correctness path.
- Do not add multi-draft composition, persuasive polish, or "natural answer plus visible logic" loops from the Phase 8C donor runtime.
- The only Phase 9 donor reuse allowed by the approved Phase 8 plan is signal vocabulary for messy-question inference. That reuse must be rebuilt clean against approved Phase 7 seams.

## Exact Forbidden Leaks From Phase 10

These records and behaviors were inspected in the donor Phase 8C contracts/runtime and are explicitly out of scope for AGIFCore Phase 8.

- `SelfModelRecord`
- `MetaCognitionObserverRecord`
- `StrategyJournalEntry`
- `SkepticCounterexampleRecord`
- `SurpriseEngineRecord`
- `ThinkerTissueRecord`
- `TheoryFragmentRecord`
- `AdoptionRecord`
- any self-model feedback loop
- any reflection control loop
- any proposal-generation or proposal-adoption runtime
- any weak-answer diagnosis loop that belongs to later critique and meta-cognition phases

If any of those records, fields, or control loops appear in later Phase 8 runtime code, that is boundary failure, not "early helpful reuse."

## Runtime Contract Expectations

### Conversation and honesty contract expectations

- Phase 8 must preserve the existing Phase 7 honesty surface rather than replace it.
- If Phase 7 or Phase 8 evidence indicates weak or stale support, downstream turn output must remain compatible with:
  - `support_state`: `search_needed` or `unknown`
  - `knowledge_gap_reason`: including `needs_fresh_information` when current-world support is stale or missing
  - `next_action`: `search_local`, `search_external`, `clarify`, or `abstain` when appropriate
  - `final_answer_mode`: never stronger than the evidence allows
- Phase 8 may constrain honesty outcomes with better bounded evidence, but it may not launder `search_needed`, `unknown`, or `abstain` into a stronger-looking answer without new bounded support.

### Trace and governance expectations

- Phase 8 outputs must stay trace-linked to existing turn surfaces and later remain compatible with:
  - `planner_trace_ref`
  - `simulation_trace_ref`
  - `critic_trace_ref`
  - `governance_trace_ref`
- `response_text` remains a user-facing Phase 7 surface, not a Phase 8 proof artifact.
- Governance must still be able to block or downgrade the turn before language reaches the user.

### Phase 8 bounded output expectations

- `scientific_priors.py` must emit typed prior selections with provenance, scope limits, failure cases, and hidden-variable hints.
- `entity_request_inference.py` must emit typed messy-question interpretation results only. It must not emit final text.
- `world_region_selection.py` must emit bounded region or context candidates with reason codes and no default single-region bluff.
- `causal_chain_reasoning.py` must emit typed causal steps with evidence refs, missing-variable markers, and weak-link visibility.
- `bounded_current_world_reasoning.py` must emit freshness and honesty outputs such as `live_measurement_required`, bounded-local support refs, and fail-closed reason codes. It must not execute search.
- `visible_reasoning_summaries.py` must emit public summary fields only:
  - `what_is_known`
  - `what_is_inferred`
  - `uncertainty`
  - `what_would_verify`
- The visible summary surface may also emit public metadata such as `principle_refs`, `causal_chain_ref`, `uncertainty_band`, and `live_measurement_required`.
- `science_reflection.py` must emit only bounded post-run verification notes like weak prior choice, missing variable, falsifier, next verification step, and uncertainty increase signal.

## Budget And Boundedness Gates

The later implementation must remain inside the frozen Phase 8 budget envelope.

| Boundary item | Maximum |
| --- | --- |
| selected prior cells per run | `<= 12` |
| entity/request inference candidates | `<= 16` |
| world-region candidates | `<= 8` |
| causal-chain steps | `<= 10` |
| current-world evidence inputs | `<= 24` |
| visible reasoning summary size | `<= 1200` characters total |
| science-reflection records | `<= 6` |
| combined evidence and demo bundle | `<= 96 MiB` |

Crossing any ceiling without an explicit re-plan is a boundary violation, not a harmless implementation detail.

## Anti-Cheat Checks For Auditor And Governor

### Structural anti-cheat checks

- Reject any implementation where one file or function performs prior selection, request inference, region selection, causal chains, freshness honesty, visible summary generation, and final answer generation together.
- Reject any implementation where `science_world_turn.py` becomes the real reasoning engine instead of a thin coordinator.
- Reject any implementation that imports later-phase donor runtime modules directly instead of rebuilding or porting the narrow approved seam.

### Phase 7 boundary anti-cheat checks

- Fail the package if Phase 8 generates final `response_text`.
- Fail the package if Phase 8 chooses `discourse_mode` or replaces the utterance planner.
- Fail the package if Phase 8 mutates any Phase 7 snapshot or reruns the Phase 7 conversation-turn engine internally.
- Fail the package if a later demo shows a stronger answer mode than the incoming honesty state allows and no new bounded evidence exists.

### Phase 6 boundary anti-cheat checks

- Fail the package if Phase 8 reruns a simulator path during visible reasoning generation.
- Fail the package if reasoning-summary text is written back into Phase 6 packages.
- Fail the package if instrumentation or usefulness scores are presented as causal proof without explicit causal-chain records.
- Fail the package if Phase 6 conflict or overload markers are present but disappear from the resulting reasoning state.

### Live-fact honesty anti-cheat checks

- Fail the package if a live-current question gets an exact current answer without `live_measurement_required` or equivalent fail-closed output.
- Fail the package if any hidden external search execution occurs inside Phase 8.
- Fail the package if currentness is implied by wording alone while the actual support is frozen local evidence.
- Fail the package if timestamps or freshness language are silently laundered into certainty.

### Visible-summary anti-cheat checks

- Fail the package if the visible reasoning summary is an unstructured monologue instead of the four bounded public fields.
- Fail the package if the summary leaks hidden-thought text, scratchpad content, or rhetorical filler not linked to evidence.
- Fail the package if `what_is_known` or `what_is_inferred` contains claims that cannot be traced to priors, region candidates, world-model evidence, or causal-chain steps.

### Meta-leak anti-cheat checks

- Fail the package if any Phase 10 self-model or reflection-loop records appear in Phase 8 runtime outputs.
- Fail the package if Phase 8 contains strategy journal, skeptic loop, thinker tissue, theory fragment, or surprise engine behavior.
- Fail the package if proposal-governance or structural-growth adoption logic appears anywhere in the Phase 8 execution family.

## Concrete Failure Signatures To Watch

- One giant "science reasoning" function returns a polished answer and a summary, but there are no separate prior, inference, region, causal-chain, and reflection records.
- A live question such as current weather, latest measurement, or "right now" gets an exact answer from local support without `search_needed`, `unknown`, `abstain`, or `live_measurement_required`.
- Phase 8 imports Phase 9 question-analysis or Phase 8C meta-growth runtime files directly and calls that reuse "implementation speed."
- The visible reasoning summary reads like hidden chain-of-thought or teaching prose and has no bounded evidence refs.
- Usefulness scores, instrumentation, or a world-model presence flag are treated as proof of causality.
- Phase 8 emits or stores `response_text`, `discourse_mode`, self-model records, strategy journals, or theory fragments.
- A demo shows Phase 8 overriding an incoming `search_needed` or `unknown` state without new bounded evidence.

## Current Boundary Judgment

- Phase 8 is correctly defined as a read-only science/world-awareness layer above approved Phase 6 and Phase 7 exports.
- The safe seam set is narrow:
  - Phase 7 intake, interpretation, support-state, and answer-contract linkage only
  - Phase 6 target-domain, world-model, simulator, lane, instrumentation, and usefulness exports only
  - approved Phase 4 and Phase 5 read-only exports only
- The highest implementation risk is scope collapse:
  - turning Phase 8 into a hidden conversation engine
  - turning it into a hidden simulator rerun path
  - turning visible reasoning into chain-of-thought theater
  - turning bounded science reflection into early meta-cognition
- This record does not approve Phase 8 runtime work. It freezes the boundary that later implementation, audit, governor verification, and validation must check against.
