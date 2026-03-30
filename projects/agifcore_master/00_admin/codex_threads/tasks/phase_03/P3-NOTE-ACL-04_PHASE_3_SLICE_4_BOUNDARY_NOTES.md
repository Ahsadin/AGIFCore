# Slice 4 Boundary Notes

## Scope

- Task card: `P3-TC-ACL-04`
- Role: `Architecture & Contract Lead`
- Branch: `codex/tc-p3-tc-acl-04-phase-3-slice-4-boundary-check`
- Worktree: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-ACL-04`
- Verdict: `boundary_safe_with_cross_lane_integration_gap`

## Goal

- confirm that Slice 4 keeps `bundle_integrity_checks` separate from `bundle_schema_validation`
- confirm that integrity is not delegated to sandbox execution
- confirm that tissue orchestration verification stays structural and Phase-3-only
- confirm there is no Phase 4 leakage

## Inspection Basis

- planning and design references:
  - `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
  - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
  - `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
  - `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- direct runtime inspection from KPL lane commit `5055a96722e0c8ad0026aa071c971659e87201e1`:
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-KPL-04/projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_integrity_checks.py`
- direct verifier and evidence inspection from TRL lane commit `c5cfbe0aff9027bacc045f207c1327e48c5890bd`:
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_tissue_orchestration.py`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_integrity.py`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_tissue_orchestration_report.json`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_integrity_report.json`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`

## Findings

### 1. Bundle integrity is separate from bundle schema validation at the code boundary

- `bundle_integrity_checks.py` is a distinct runtime module, not folded into `bundle_schema_validation.py`.
- The integrity runtime imports `validate_bundle_manifest_payload` from `bundle_manifest.py`, but it does not collapse integrity into schema loading.
- The integrity runtime performs integrity-specific work:
  - canonical payload byte generation
  - SHA-256 digest computation
  - digest-format validation
  - manifest-to-inventory entry matching
  - payload equality checks between manifest inventory and integrity inventory
  - digest mismatch failure
- `bundle_schema_validation.py` remains focused on:
  - schema reference resolution
  - schema JSON loading
  - bundle manifest shape validation
  - nested cell and tissue payload shape validation
- The TRL bundle-integrity verifier also preserves that split in its planned checks:
  - schema-ref and nested payload failures route through `validate_bundle_schema_foundation`
  - integrity-specific cases route through `bundle_integrity_checks`

### 2. Sandbox execution is not used as a substitute for integrity

- In the inspected Slice 4 runtime and verifier code, there is no sandbox import, no sandbox entrypoint, and no execution-isolation handoff.
- The integrity runtime is a structural pre-execution checker over manifest and inventory payloads.
- That matches the design rule in `BUNDLE_INTEGRITY_MODEL.md`: sandboxing may isolate execution later, but it does not replace integrity checks.
- I found no code path that delegates integrity truth to sandbox execution.

### 3. Tissue orchestration verification stays structural and Phase-3-only

- `verify_phase_03_tissue_orchestration.py` imports only `cell_contracts` and `tissue_manifests` from the Phase 3 structural runtime.
- Its runtime file list is limited to:
  - `cell_contracts.py`
  - `tissue_manifests.py`
  - Phase 3 structural schemas
- Its exercised checks stay structural:
  - valid cell contract
  - valid tissue manifest
  - split-review threshold exposure
  - missing contract field failure
  - duplicate member failure
  - role-family mismatch failure
  - tissue fanout breach failure
- The generated tissue orchestration report is a real executed report with status `pass`.
- Nothing in this verifier reaches into memory planes, graph persistence, sandbox execution, or product-runtime behavior.

### 4. No Phase 4 leakage is visible in the inspected Slice 4 package

- I did not find references to Phase 4 memory surfaces, graph surfaces, builder privilege, cloud correctness, or sandbox substitution in:
  - `bundle_integrity_checks.py`
  - `verify_phase_03_tissue_orchestration.py`
  - `verify_phase_03_bundle_integrity.py`
- The Slice 4 runtime and verifier surfaces stay inside Phase 3 structural concerns:
  - bundle manifest and payload inventory integrity
  - cell and tissue structure validation
  - orchestration fanout and membership constraints
- This is boundary-safe for the requested Phase 3 scope.

### 5. Cross-lane execution is still honestly blocked, but not for a boundary reason

- The TRL lane’s `phase_03_bundle_integrity_report.json` is honestly `blocked`.
- That report says the runtime file was missing in the TRL lane at the time it ran, and the evidence manifest stays blocked for the same reason.
- Direct code inspection also shows a cross-lane hookup gap:
  - KPL runtime exports `validate_bundle_integrity(bundle_manifest_payload, integrity_inventory)`
  - the TRL verifier’s generic single-payload entrypoint caller invokes the selected runtime entrypoint with one payload object
- That means the current runtime/verifier pair is not yet directly executable together without a follow-up integration fix.
- This is a real integration seam issue, but it is not a sandbox substitution issue, not a schema/integrity collapse issue, and not Phase 4 leakage.

## Assessment

- `bundle_integrity_checks` stays separate from `bundle_schema_validation`: `yes`
- integrity is separate from sandbox execution: `yes`
- tissue orchestration verification stays structural and Phase-3-only: `yes`
- no Phase 4 leakage found in inspected Slice 4 code: `yes`
- TRL bundle-integrity evidence remains blocked: `yes`, but the blocker is a lane/integration condition, not a boundary violation

## Final Verdict

- `boundary-safe at the code level`
- clarification:
  - Slice 4 is boundary-safe for the requested Architecture & Contract review.
  - The TRL bundle-integrity report remains honestly blocked because the runtime file was not present in that lane when the verifier ran, and the current runtime/verifier seam also needs a narrow integration fix before cross-lane execution can pass.
  - That integration gap does not change the boundary conclusion: no schema/integrity collapse, no sandbox substitution, and no Phase 4 leakage were found in the inspected Slice 4 code.
