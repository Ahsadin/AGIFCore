# Slice 4 Boundary Notes

## Scope

- Task card: `P3-TC-ACL-04`
- Role: `Architecture & Contract Lead`
- Branch: `codex/tc-p3-tc-acl-04-phase-3-slice-4-boundary-check`
- Worktree: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-ACL-04`
- Verdict: `boundary_safe_with_file_backed_evidence_blocker`

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
- direct verifier and evidence inspection from TRL lane commits:
  - `c5cfbe0aff9027bacc045f207c1327e48c5890bd`
  - `44a4aff`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_tissue_orchestration.py`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_integrity.py`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_tissue_orchestration_report.json`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_integrity_report.json`
  - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`

## Findings

### 1. Bundle integrity remains separate from bundle schema validation

- `bundle_integrity_checks.py` is a dedicated runtime module.
- Its runtime concerns are integrity-specific:
  - canonical payload encoding
  - SHA-256 digest generation
  - digest-format validation
  - manifest-to-inventory entry matching
  - payload equality checks
  - hash mismatch failure
- `bundle_schema_validation.py` remains a separate structural validator for:
  - schema references
  - schema JSON loading
  - bundle manifest shape
  - nested cell and tissue payload shape
- The repaired TRL verifier preserves that split:
  - schema and nested payload failures route through `validate_bundle_schema_foundation`
  - integrity-specific failures route through `bundle_integrity_checks`

### 2. Sandbox execution is not used as an integrity substitute

- In the inspected Slice 4 runtime and verifier code, I found no sandbox import, no sandbox entrypoint, and no handoff that treats sandbox isolation as integrity truth.
- The integrity runtime operates as a structural pre-execution check over manifest and inventory data.
- That matches the frozen design rule that sandboxing may isolate later execution but does not replace integrity checks.

### 3. Tissue orchestration verification stays structural and Phase-3-only

- `verify_phase_03_tissue_orchestration.py` imports only `cell_contracts` and `tissue_manifests`.
- Its runtime file list stays inside the Phase 3 structural layer and its schemas.
- The exercised cases are structural:
  - valid cell contract
  - valid tissue manifest
  - split-review threshold exposure
  - missing contract field failure
  - duplicate member failure
  - role-family mismatch failure
  - tissue fanout breach failure
- `phase_03_tissue_orchestration_report.json` is a real executed report with status `pass`.

### 4. No Phase 4 leakage was found in the inspected Slice 4 code

- I found no references to Phase 4 memory surfaces, graph surfaces, hidden builder privilege, cloud correctness, or sandbox substitution in:
  - `bundle_integrity_checks.py`
  - `verify_phase_03_tissue_orchestration.py`
  - `verify_phase_03_bundle_integrity.py`
- The inspected Slice 4 package stays inside Phase 3 structural concerns.

### 5. The prior verifier-shape gap is repaired in code, but the TRL evidence files still show a concrete blocker

- TRL commit `44a4aff` updates the bundle-integrity verifier so it now calls the runtime entrypoint with:
  - `bundle_manifest_payload`
  - `integrity_inventory`
- That removes the earlier code-level argument-shape mismatch.
- However, the inspected file [phase_03_bundle_integrity_report.json](/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_integrity_report.json) still records:
  - status `blocked`
  - blocker kind `missing_runtime_dependencies`
  - missing file `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_integrity_checks.py`
- The inspected file [phase_03_evidence_manifest.json](/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json) also still reports Slice 4 as blocked for the same file-backed reason.
- So the remaining blocker is concrete and file-backed:
  - the code boundary is clean
  - the TRL evidence has not yet been regenerated in a lane where the KPL runtime file is actually present on disk

## Assessment

- `bundle_integrity_checks` stays separate from `bundle_schema_validation`: `yes`
- integrity is separate from sandbox execution: `yes`
- tissue orchestration verification stays structural and Phase-3-only: `yes`
- no Phase 4 leakage found in inspected Slice 4 code: `yes`
- remaining blocker: `yes`, but it is evidence-state only and is explicitly recorded in the current TRL report files

## Final Verdict

- `boundary-safe at the code level`
- concrete remaining blocker:
  - [phase_03_bundle_integrity_report.json](/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_integrity_report.json) is still `blocked` because the runtime file `bundle_integrity_checks.py` was not on disk in the TRL lane when that evidence was produced.
  - [phase_03_evidence_manifest.json](/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json) still reflects that blocked state.
- boundary conclusion:
  - Slice 4 is boundary-safe in the inspected code.
  - The only remaining issue is a concrete, file-backed evidence rerun gap, not a boundary violation.
