# Phase 8 Science Explanation Demo

Purpose:
- show a bounded science explanation path using the Phase 8 reasoning surfaces in this bundle
- show that the explanation stays grounded in scientific priors, typed inference, a bounded region choice, a typed causal chain, a public reasoning summary, and a short science reflection

Scenario:
- prompt family: a weather-and-climate explanation request with local scientific cues
- supported path: scientific priors -> entity/request inference -> world-region selection -> causal-chain reasoning -> visible reasoning summaries -> science reflection

Inspect:
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_demo_bundle/phase_08_science_explanation_demo.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_evidence_manifest.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_scientific_priors_report.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_entity_request_inference_report.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_world_region_selection_report.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_causal_chain_reasoning_report.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_visible_reasoning_summaries_report.json`
- `projects/agifcore_master/06_outputs/phase_08_science_and_world_awareness/phase_08_evidence/phase_08_science_reflection_report.json`

Evidence-backed facts shown by this demo:
- the scientific-priors path has a bounded request with `available_prior_count: 3` and selected cells that include `coastal_weather_baseline` and `measurement_uncertainty`
- entity/request inference produces a live-current-aware weather request with `support_state_hint: search_needed` or a grounded explanation path depending on the turn
- world-region selection keeps the candidate set bounded and produces a selected region for the weather-climate domain
- causal-chain reasoning produces a typed chain with `weakest_link_reason: none_detected` for the strong path
- visible reasoning summaries exist as public-only reasoning outputs
- science reflection exists as a bounded review layer and does not expand into later meta-cognition

Truth note:
- this demo is inspectable only from local files
- Phase 8 remains `open`
