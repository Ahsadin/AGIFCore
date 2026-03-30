# Phase 3 Bundle Validation Demo

Phase 3 remains open. This is slice 1 only.

Governor can rerun the same verifier later without external `PYTHONPATH` wiring.

## Review

- `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-01/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_validation_report.json`
- `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-TRL-01/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`

## Good Looks Like

- the bundle report shows a valid pass case
- the bundle report shows fail-closed cases for missing fields, bad shape, missing schema refs, and invalid nested payloads
- the evidence manifest references the actual report files on disk
- the verifier resolves the runtime directory from the repo layout directly
- nothing claims Phase 3 is closed

## Failure Looks Like

- the report is missing
- the report is narrative only
- the demo path points to files that do not exist
- the demo text claims Phase 3 is approved or closed
