# Phase 3 Slice 3 Boundary Notes

## Scope of this note

This note covers the requested Phase 3 Slice 3 boundary check for:

- `split_merge_rules.py`
- `profile_budget_rules.py`

Reference surfaces reviewed before writing this note:

- `P3-TC-ACL-03_PHASE_3_BOUNDARY_CHECK.md`
- `PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md`
- `PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
- approved Phase 2 `cell_registry.py`
- approved Phase 2 `lifecycle_engine.py`
- approved Phase 2 `scheduler.py`
- approved Phase 2 `workspace_state.py`
- `P3-NOTE-ACL-01_PHASE_3_SLICE_1_BOUNDARY_NOTES.md`
- `P3-NOTE-ACL-02_PHASE_3_SLICE_2_BOUNDARY_NOTES.md`
- current Phase 3 Slice 1 and Slice 2 runtime files present in this worktree

## Inspection result

Current status is `provisional and blocking for runtime verdict`.

This worktree contains the integrated Slice 1 and Slice 2 runtime surfaces, but it does not contain `split_merge_rules.py` or `profile_budget_rules.py`. Because the target Slice 3 runtime files are not present here yet, a real post-build runtime boundary pass is blocked. What can be recorded now is the binding boundary those files must satisfy when they arrive.

## Boundary verdict

Verdict: `provisional/blocking`

Reason:

- the required Slice 3 runtime surfaces are not on disk in this lane
- no Slice 3 verifier surface is present in this lane for these modules
- a runtime-safe verdict would be false confidence without direct file inspection

## Checks completed now

1. Phase 2 lifecycle ownership remains below Slice 3
   - `pass`
   - The approved Phase 2 lifecycle owner is still `LifecycleEngine`.
   - Phase 2 already owns the explicit lifecycle verbs `activate`, `hibernate`, `reactivate`, `quarantine`, `clear_quarantine`, `retire`, `split`, and `merge`.
   - The approved registry state family is already frozen in `cell_registry.py`:
     - `seed`
     - `dormant`
     - `active`
     - `split_pending`
     - `consolidating`
     - `quarantined`
     - `retired`
   - Slice 3 may shape rules, proposals, and validation around those states and verbs, but it may not create a second state machine or directly replace Phase 2 lifecycle ownership.

2. Phase 2 scheduler ownership remains below Slice 3
   - `pass`
   - The approved Phase 2 scheduler still owns queue depth, task ordering, enqueue and dispatch, payload-size checks, and latency metrics.
   - `profile_budget_rules.py`, when integrated, may constrain scheduler inputs or profile ceilings, but it may not recreate queue logic, dispatch logic, heap ordering, or scheduler metrics.

3. No hidden Slice 3 runtime logic was found in the integrated Slice 1 and Slice 2 files present here
   - `pass`
   - Slice 1 stays structural only.
   - Slice 2 already states that it does not import `profile_budget_rules`.
   - Slice 2 uses visible ceiling constants only:
     - mobile active cells `8`
     - laptop active cells `32`
     - tissues `12`
     - dormant blueprints `128`
   - That means the missing Slice 3 modules are not already silently embedded in the currently integrated Slice 1 and Slice 2 runtime surfaces.

4. Phase 4 exclusion is still explicit
   - `pass`
   - Phase 4 in `PHASE_INDEX.md` remains the separate `memory planes` phase.
   - `PHASE_02_FABRIC_KERNEL_AND_WORKSPACE.md` allows only bounded memory-hook references and explicitly forbids semantic memory, procedural memory, reviewed long-term memory, promotion, compression, forgetting, retirement logic for memory, graph persistence, and memory-plane-specific algorithms.
   - `split_merge_rules.py` and `profile_budget_rules.py` therefore must not contain:
     - memory-plane storage policy
     - reviewed-memory promotion or retention logic
     - deduplication, supersession, compression, forgetting, or memory GC
     - graph persistence or conversation behavior

## Binding boundary rules for Slice 3 runtime when integrated

1. `split_merge_rules.py` must stay policy-bound to Phase 2 lifecycle.
   - It may validate whether a requested split or merge is structurally allowed.
   - It may shape a proposal or request payload for Phase 2 execution.
   - It may read current lifecycle state names that already exist in Phase 2.
   - It may not mutate registry state directly.
   - It may not maintain a second lifecycle history.
   - It may not add new lifecycle states beyond the approved Phase 2 state family.
   - It may not reimplement `LifecycleEngine.split()` or `LifecycleEngine.merge()`.

2. `profile_budget_rules.py` must stay policy-bound to Phase 2 scheduler and Phase 3 ceilings.
   - It may define profile ceilings and structural guardrails for mobile, laptop, and later builder use.
   - It may validate active-cell counts, tissue counts, tissue fanout, or split-pressure thresholds against the approved Phase 3 envelope.
   - It may cap scheduler inputs such as allowed priority or estimated cost envelopes.
   - It may not enqueue tasks.
   - It may not dispatch tasks.
   - It may not implement heap ordering, queue storage, or latency measurement.
   - It may not widen Phase 3 ceilings silently.

3. Slice 3 must remain above Phase 2 and below Phase 4.
   - allowed: structural policy, rule validation, proposal shaping, and profile-bound structural checks
   - forbidden: memory review policy, long-term retention, graph mutation, simulator logic, conversation behavior, or product-runtime logic

4. Cell retirement wording must stay precise.
   - Cell lifecycle retirement already exists in Phase 2 and can be referenced as a lifecycle outcome.
   - Memory retirement remains Phase 4 scope and must not be smuggled into Slice 3 under split/merge or profile-budget wording.

## Required post-integration checks

When `split_merge_rules.py` and `profile_budget_rules.py` are integrated into this lane, rerun this boundary pass and confirm all of the following directly from code:

1. imports and call sites
   - confirm whether the modules import `LifecycleEngine`, `CellRegistry`, or `Scheduler`
   - if they do, confirm usage is read-only, validation-only, or request-shaping only
   - block if they mutate registry state, own transition history, or dispatch scheduler work directly

2. lifecycle-state handling
   - confirm the modules use only approved Phase 2 lifecycle state names
   - block if new structural-only states are invented

3. split/merge implementation boundary
   - confirm `split_merge_rules.py` does not recreate child registration, survivor retirement, or lineage mutation already owned by Phase 2 lifecycle execution

4. budget boundary
   - confirm `profile_budget_rules.py` uses the approved Phase 3 ceilings and does not silently widen them
   - confirm any builder-profile handling is explicit, bounded, and still inside master-plan ceilings

5. Phase 4 exclusion
   - confirm neither module imports memory-plane code or introduces memory lifecycle algorithms under structural names

## Conclusion

Slice 3 cannot receive a runtime `pass` yet in this lane because the target runtime files are absent.

The current note is still useful because it records a concrete blocking condition and the exact contract that `split_merge_rules.py` and `profile_budget_rules.py` must satisfy after integration.

## No approval implied

This note does not approve Slice 3, Phase 3, or any later phase. It records a provisional and blocking boundary result until the actual Slice 3 runtime surfaces are present for direct inspection.
