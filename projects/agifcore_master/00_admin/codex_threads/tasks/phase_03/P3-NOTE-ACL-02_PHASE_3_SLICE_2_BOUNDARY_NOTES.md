# Phase 3 Slice 2 Boundary Notes

## Scope of this note

This note covers the requested Phase 3 Slice 2 boundary check for the current runtime and verifier surfaces:

- `activation_policies.py`
- `trust_bands.py`
- `active_dormant_control.py`
- `verify_phase_03_activation_and_trust.py`

Reference surfaces reviewed before writing this note:

- `P3-TC-ACL-02_PHASE_3_SLICE_2_BOUNDARY_CHECK.md`
- `PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
- approved Phase 2 `lifecycle_engine.py`
- approved Phase 2 `scheduler.py`
- current Slice 2 runtime files in `P3-TC-KPL-02`
- current Slice 2 verifier file in `P3-TC-TRL-02`

## Inspection result

Current status is `pass with residual verifier-integration risk`.

The real Slice 2 runtime files now exist and were inspected directly in the KPL lane. The three runtime modules stay inside the approved Phase 3 structural layer and remain bounded to the approved Phase 2 lifecycle and scheduler seams.

## Boundary verdict

Verdict: `pass`

The Slice 2 runtime is boundary-safe for the requested checks.

## Requested checks and findings

1. No Phase 4 leakage
   - `pass`
   - The inspected runtime files contain activation-policy, trust-band, and active-dormant-control logic only.
   - No memory-plane, graph, semantic, episodic, procedural, simulator, or conversation logic appears in these modules.
   - `active_dormant_control.py` is limited to lifecycle-state validation, readiness decisions, dormant-pressure checks, and transition-request shaping.

2. No second lifecycle state machine
   - `pass`
   - `active_dormant_control.py` explicitly constrains itself to the approved Phase 2 lifecycle state names:
     - `dormant`
     - `active`
     - `quarantined`
     - `retired`
     - `split_pending`
     - `consolidating`
   - It returns `ActiveDormantDecision` recommendations and transition-request dictionaries only.
   - It does not mutate registry state, does not implement transition history, and does not recreate Phase 2 lifecycle methods such as bootstrap, quarantine, clear_quarantine, retire, split, or merge.
   - `build_lifecycle_transition_request()` allows only `dormant -> active` and `active -> dormant`, which keeps Slice 2 policy-bound rather than turning it into a second lifecycle engine.

3. Trust bands have enforcement meaning, including explicit activation blocking
   - `pass`
   - `trust_bands.py` is not label-only. It defines concrete enforcement fields and methods:
     - `allow_activation`
     - `max_scheduler_priority`
     - `enforce_activation()`
     - `enforce_scheduler_priority()`
     - `enforce_minimum_band()`
   - The `blocked` default policy sets `allow_activation=False`, `allow_split_merge=False`, `require_manual_review=True`, and `max_scheduler_priority=0`.
   - `ActivationPolicy.evaluate_activation()` uses that enforcement meaning directly:
     - if the provided `TrustBand` has `allow_activation=False`, it returns `allow=False` with reason `trust band blocks activation`
   - Manual runtime probe against the current KPL code confirmed that a `blocked` trust band produces an explicit activation denial both in `ActivationPolicy.evaluate_activation()` and in `evaluate_activation_readiness()`.

4. No hidden `profile_budget_rules` module logic
   - `pass`
   - The inspected Slice 2 runtime files do not import `profile_budget_rules`.
   - The only profile-budget behavior present here is explicit and local:
     - `PHASE3_PROFILE_ACTIVE_CELL_CEILINGS = {"mobile": 8, "laptop": 32}`
     - `PHASE3_TISSUE_CEILING = 12`
     - `PHASE3_DORMANT_BLUEPRINT_CEILING = 128`
   - Those constants align with the Phase 3 plan ceilings and are visible in `activation_policies.py` and `active_dormant_control.py`.
   - No hidden helper module or silent budget subsystem appears in the inspected runtime surfaces.

5. No direct scheduler reimplementation
   - `pass`
   - None of the Slice 2 runtime modules imports the Phase 2 scheduler or reimplements its queue, heap ordering, dispatch loop, payload validation, or latency metrics.
   - The scheduler seam here is policy-only:
     - `ActivationPolicy` gates activation by `maximum_estimated_cost`
     - `TrustBand` caps `max_scheduler_priority`
   - That is boundary-safe because it constrains scheduler inputs without recreating scheduler behavior.

## Supporting observations

- `activation_policies.py` stays at the structural-policy layer. It does not schedule tasks, mutate lifecycle state, or add new state families.
- `trust_bands.py` adds explicit fail-closed trust controls and band ordering without drifting into memory, graph, or conversation scope.
- `active_dormant_control.py` is careful to build requests rather than execute them.
- Split and merge behavior is not implemented here. The only split/merge mention is a trust-band flag and recognition of Phase 2 lifecycle states that already exist.

## Residual risk

Residual risk is in verifier alignment, not in the runtime boundary itself.

- The current verifier file in `P3-TC-TRL-02` still assumes an older payload shape such as trust band name `trusted` and activation-policy fields like `policy_name`, `allowed_trust_bands`, and `max_scheduler_cost`.
- The current Slice 2 runtime instead requires explicit fields like:
  - trust band: `band_name`, `allow_activation`, `max_scheduler_priority`
  - activation policy: `policy_id`, `cell_id`, `tissue_id`, `profile`, `minimum_need_score`, `maximum_estimated_cost`, `minimum_trust_band`, `policy_envelope`
- Running the verifier in its own TRL worktree currently blocks because it expects the runtime files under its own repo root and does not see the KPL-lane modules there yet.

This is a real follow-up item for TRL or later integration, but it is not a runtime boundary failure in the Slice 2 KPL code that was inspected here.

## Conclusion

Slice 2 now passes the requested boundary check.

## No approval implied

This note does not approve Slice 2, Phase 3, or any later phase. It records that the current Slice 2 runtime is boundary-safe for the requested checks, with residual verifier-integration risk still remaining outside this runtime boundary verdict.
