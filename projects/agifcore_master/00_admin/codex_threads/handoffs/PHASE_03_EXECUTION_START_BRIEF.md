# Phase 3 Execution Start Brief

Use this brief to continue the approved Phase 3 execution-start baseline.

## Phase status

- active phase: `3`
- phase title: `cells, tissues, structure, and bundles`
- phase gate state: `open`
- plan baseline status: frozen for execution start

## Frozen plan path

- `projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`

## Execution slice scope

Build only slice 1:

- cell contracts
- tissue manifests
- bundle manifest surface
- bundle schema validation foundation

## Active roles

- `Program Governor`
- `Kernel Pod Lead`
- `Architecture & Contract Lead`
- `Test & Replay Lead`

## Inactive roles

- `Memory & Graph Pod Lead`
- `World & Conversation Pod Lead`
- `Meta & Growth Pod Lead`
- `Merge Arbiter`
- `Validation Agent`
- `Release & Evidence Lead`
- `Anti-Shortcut Auditor`

## Exact allowed files

- `projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/`
- `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/cell_contracts.py`
- `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/tissue_manifests.py`
- `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_manifest.py`
- `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/bundle_schema_validation.py`
- `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/schemas/phase_03_cell_contract.schema.json`
- `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/schemas/phase_03_tissue_manifest.schema.json`
- `projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/schemas/phase_03_bundle_manifest.schema.json`
- `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_cell_contracts.py`
- `projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/verify_phase_03_bundle_validation.py`
- `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`
- `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_cell_contracts_report.json`
- `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_validation_report.json`
- `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_demo_index.md`
- `projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_bundle_validation_demo.md`

## Exact forbidden files

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- all Phase 4+ artifacts
- any Phase 3 closeout verdict file
- any Phase 3 closeout validation-request file
- any slice-2 file

## Stop rule after slice 1

- stop implementation after the two verifiers pass and the slice-1 evidence package exists
- prepare the package for the next audit step
- do not start slice 2 automatically
- do not mark Phase 3 approved

## Approval note

- no approval is implied by slice-1 completion
- only a later explicit user verdict `approved` can earn Phase 3
