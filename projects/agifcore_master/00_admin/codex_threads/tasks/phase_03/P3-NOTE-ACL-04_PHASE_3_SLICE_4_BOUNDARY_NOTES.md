# Slice 4 Boundary Notes

## Scope

- Task card: `P3-TC-ACL-04`
- Role: `Architecture & Contract Lead`
- Branch: `codex/tc-p3-tc-acl-04-phase-3-slice-4-boundary-check`
- Worktree: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-ACL-04`
- Verdict: `blocking`

## Goal

- confirm that Slice 4 keeps `bundle_integrity_checks` separate from `bundle_schema_validation`
- confirm that integrity is not delegated to sandbox execution
- confirm that tissue orchestration verification stays structural and Phase-3-only
- confirm there is no Phase 4 leakage

## What Was Read

- `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`
- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- `projects/agifcore_master/03_design/BUNDLE_INTEGRITY_MODEL.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- current Phase 3 structural runtime already present in this worktree:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_manifest.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_schema_validation.py`
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/tissue_manifests.py`
- current Phase 3 verifiers already present in this worktree:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_validation.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_cell_contracts.py`

## Findings

### 1. `bundle_integrity_checks` separation cannot be cleared because the runtime file is missing

- The task card requires `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_integrity_checks.py`.
- That file is not present in this worktree.
- `bundle_schema_validation.py` exists and currently validates schema references, schema JSON loading, bundle manifest shape, and linked cell/tissue payload shape.
- Because the dedicated integrity module is missing, this lane cannot prove that integrity logic is separate from schema validation instead of being omitted or collapsed into another module.

### 2. No sandbox substitution can be cleared only provisionally

- `BUNDLE_INTEGRITY_MODEL.md` is explicit: sandboxing may isolate execution, but sandboxing does not replace integrity checks.
- `PRODUCT_RUNTIME_MODEL.md` keeps correctness separate from later runtime packaging concerns.
- In the current Phase 3 structural runtime files that were reviewed, there is no visible sandbox import or execution handoff.
- That is not enough to clear the boundary.
- The dedicated integrity runtime is missing, so this lane cannot verify the required fail-closed ordering of:
  - integrity check before execution
  - integrity check outside sandbox substitution
  - integrity check as its own structural concern

### 3. Tissue orchestration verification cannot be cleared because the verifier file is missing

- The task card requires `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_tissue_orchestration.py`.
- That file is not present in this worktree.
- `tissue_manifests.py` does stay structural on its face:
  - membership fanout is bounded
  - routing targets are bounded
  - role-family membership is checked against cell contracts
  - the module docstring explicitly says no memory or graph logic is allowed there
- Even with those good signs, the boundary check is still blocked because the required verifier that would prove orchestration stays structural and Phase-3-only does not exist in this lane.

### 4. No Phase 4 leakage is only partially inspectable from the currently present files

- The reviewed structural runtime files do not show direct memory-plane or graph-persistence wiring.
- `tissue_manifests.py` explicitly states that memory and graph logic are not allowed there.
- That is helpful but incomplete.
- Without the missing Slice 4 runtime and verifier files, this lane cannot verify whether later orchestration checks or integrity logic smuggle in:
  - Phase 4 memory-plane assumptions
  - sandbox execution privileges standing in for integrity truth
  - hidden builder-only correctness behavior

## Exact Missing Checks That Block Clearance

- Missing runtime file:
  - `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_integrity_checks.py`
- Missing verifier files:
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_tissue_orchestration.py`
  - `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_integrity.py`
- Missing evidence outputs named by the task card:
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_tissue_orchestration_report.json`
  - `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_integrity_report.json`

## Minimum Checks Required Before This Boundary Can Be Cleared

- `bundle_integrity_checks.py` must exist as a separate module from `bundle_schema_validation.py`.
- The integrity module must fail closed on integrity-specific conditions and must not depend on sandbox execution as a substitute for integrity truth.
- `verify_phase_03_bundle_integrity.py` must exist and prove that integrity checks stay separate from schema validation and separate from sandbox execution.
- `verify_phase_03_tissue_orchestration.py` must exist and prove that orchestration checks stay structural, Phase-3-only, and free of Phase 4 logic.
- The two required evidence reports must exist and reflect those checks directly.

## Final Verdict

- `blocked`
- Reason:
  - Slice 4 cannot be truthfully cleared in this lane because the named Slice 4 runtime, verifier, and evidence surfaces are not present.
  - Current files provide only partial structural signals, not the exact checks needed to clear the boundary.
