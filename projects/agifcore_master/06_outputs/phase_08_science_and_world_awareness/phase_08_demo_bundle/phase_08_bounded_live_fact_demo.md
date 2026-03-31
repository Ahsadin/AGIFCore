# Phase 8 Bounded Live-Fact Demo

Purpose:
- show that Phase 8 handles a current-world request honestly
- show that the system does not emit an unsupported exact current answer when the evidence is fresh-only or bounded-only

Scenario:
- prompt family: a live-current weather request
- supported path: entity/request inference -> world-region selection -> causal-chain reasoning -> bounded current-world reasoning -> visible reasoning summaries

Inspect:
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_bounded_live_fact_demo.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_evidence_manifest.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_entity_request_inference_report.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_world_region_selection_report.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_causal_chain_reasoning_report.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_bounded_current_world_reasoning_report.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_visible_reasoning_summaries_report.json`

Evidence-backed facts shown by this demo:
- the inference layer marks the request as live-current aware and records `support_state_hint: search_needed` for the current-fact path
- the bounded current-world report includes a `decision` of `live_measurement_required` for the fresh-measurement path
- the chain records `weakest_link_reason: needs_fresh_information` for the unresolved current-world branch
- the visible reasoning summary path stays public and bounded
- no unsupported exact current answer is emitted from the evidence-backed local path

Truth note:
- this demo is inspectable only from local files
- Phase 8 remains `open`
