# Phase 3 Slice 3 Boundary Notes

## Scope of this note

This note covers the requested Phase 3 Slice 3 boundary check for:

- `split_merge_rules.py`
- `profile_budget_rules.py`
- `verify_phase_03_split_merge.py`
- `verify_phase_03_profile_budgets.py`

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
- KPL Slice 3 runtime:
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-KPL-03/projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/split_merge_rules.py`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-KPL-03/projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/profile_budget_rules.py`
- TRL Slice 3 verifiers:
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-03/projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_split_merge.py`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-03/projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_profile_budgets.py`

## Inspection result

Current status is `runtime pass with verifier blocker`.

The actual Slice 3 runtime code now exists in the KPL lane and was inspected directly. It stays inside the approved Phase 3 structural boundary and remains subordinate to the approved Phase 2 lifecycle and scheduler substrate.

The blocker is now verifier alignment, not runtime boundary drift. The TRL verifier files are still written as blocked-state placeholders and do not yet reflect the real Slice 3 runtime now on disk in the KPL lane.

## Boundary verdict

Verdict: `blocking`

Reason:

- the Slice 3 runtime itself is boundary-safe for the requested checks
- the Slice 3 verifier surfaces are not aligned to the runtime intent and still hard-code blocked behavior
- because verifier alignment was part of the requested check, Slice 3 cannot receive an unqualified pass from this boundary note

## Requested checks and findings

1. No second lifecycle state machine
   - `pass`
   - `split_merge_rules.py` does not import `LifecycleEngine`, `CellRegistry`, or `workspace_state`.
   - It uses only structural state validation helpers:
     - split parent must be `active`
     - merge participants must be `active` or `dormant`
   - It does not introduce any new lifecycle states.
   - It does not keep transition history, mutate records, or recreate Phase 2 verbs such as bootstrap, quarantine, clear_quarantine, retire, split, or merge.

2. `split_merge_rules` shapes requests and does not mutate registry or lifecycle directly
   - `pass`
   - The module builds `SplitProposal` and `MergeProposal` objects from payloads.
   - The exported decision from `evaluate_split_proposal()` and `evaluate_merge_proposal()` is a policy result with:
     - `allowed`
     - `reason`
     - `lifecycle_input`
     - `lineage_ledger_entry`
   - For split, `lifecycle_input` contains only:
     - `parent_cell_id`
     - child `cell_id` and `role_family`
     - `reason`
     - `actor`
   - For merge, `lifecycle_input` contains only:
     - `survivor_cell_id`
     - `merged_cell_id`
     - `reason`
     - `actor`
   - No call to `register_cell`, `update_cell`, `split`, `merge`, `retire`, or any registry/lifecycle mutation surface appears in the module.

3. `profile_budget_rules` stays structural and is not a scheduler implementation
   - `pass`
   - `profile_budget_rules.py` does not import `Scheduler`.
   - It defines bounded profile-budget payload validation, default payload construction, context validation, and `ProfileBudgetRule.evaluate()`.
   - It evaluates counts and byte ceilings only:
     - `active_cell_count`
     - `tissue_count`
     - `largest_tissue_member_count`
     - `dormant_blueprint_count`
     - `manifest_size_bytes`
     - `bundle_payload_size_bytes`
   - It does not enqueue tasks, dispatch tasks, order queues, measure latency, or implement heap logic.

4. No Phase 4 logic
   - `pass`
   - Neither runtime module imports memory-plane code, graph code, simulator code, or conversation code.
   - No semantic memory, procedural memory, reviewed-memory policy, retention policy, deduplication, supersession, compression, forgetting, memory GC, or graph persistence logic appears in these files.
   - The only use of the word `retired` in Slice 3 context is the merge lineage output field `retired_cell_id`, which is still referring to the already approved Phase 2 cell lifecycle outcome, not Phase 4 memory retirement.

5. Builder profile handling is explicit and bounded
   - `pass`
   - `profile_budget_rules.py` defines:
     - `PROFILE_NAMES = ("mobile", "laptop", "builder")`
     - `BUILDER_ACTIVE_CELL_CEILING = 64`
   - Builder is explicit rather than hidden.
   - `64` stays within the master-plan hard ceiling for laptop-builder scale and does not exceed the frozen `1024` logical-cell program ceiling.
   - The module keeps builder under the same Phase 3 structural ceilings for:
     - tissues
     - dormant blueprints
     - manifest size
     - bundle payload size
   - This is bounded structural handling, not an open-ended scale escape hatch.

6. Verifier surfaces are aligned to runtime intent
   - `block`
   - `verify_phase_03_split_merge.py` is still a blocked-state verifier.
   - Even when the runtime file exists, its `main()` path still writes `build_blocked_report(...)`, prints `BLOCKED`, and returns exit code `1`.
   - It does not execute the planned split/merge cases against the real runtime.
   - `verify_phase_03_profile_budgets.py` is also still blocked-state oriented.
   - It can exercise some Slice 2 supporting runtime behavior, but it still reports `status: "blocked"`, forces `runtime_modules_available` to `False`, and keeps builder-specific checks in `blocked_checks`.
   - Its notes still say builder remains blocked until `profile_budget_rules` exists, but the runtime file now does exist in the KPL lane.
   - This means the verifier layer is behind the runtime and does not yet prove the actual Slice 3 behavior it is supposed to validate.

## Supporting observations

- `split_merge_rules.py` correctly keeps trust-band enforcement at the policy layer through `allow_split_merge` and `require_manual_review`.
- Split pressure stays bounded by `SPLIT_PRESSURE_MEMBER_COUNT`, and oversized split pressure returns manual-review blocking instead of silent expansion.
- `profile_budget_rules.py` reuses the existing Phase 3 ceilings from Slice 2 constants for mobile, laptop, tissue, and dormant-blueprint bounds, then adds explicit builder handling rather than hiding it elsewhere.
- The runtime modules are proposal and ceiling surfaces, not execution engines.

## Concrete blocker

The blocker is not runtime boundary drift. The blocker is verifier mismatch.

Exact verifier problems found:

1. `verify_phase_03_split_merge.py`
   - still assumes the slice is blocked
   - contains planned checks only, not executed runtime cases
   - returns `1` in both the missing-runtime and runtime-present paths
   - keeps notes that say the runtime file is absent even though it now exists in the KPL lane

2. `verify_phase_03_profile_budgets.py`
   - still emits `status: "blocked"` even in the runtime-present path
   - still forces `runtime_modules_available` to `False`
   - still treats builder profile checks as unavailable because the runtime file is supposedly absent
   - therefore does not align with the real runtime intent now implemented in `profile_budget_rules.py`

## Conclusion

Slice 3 runtime now passes the requested boundary checks.

Slice 3 as a whole remains blocked from a clean boundary close because the verifier surfaces are not aligned to the runtime they are supposed to validate. The next repair should be on the TRL verifier side, not in the KPL runtime.

## No approval implied

This note does not approve Slice 3, Phase 3, or any later phase. It records a code-backed runtime pass with a concrete verifier blocker that must be repaired before Slice 3 can claim a clean boundary close.
