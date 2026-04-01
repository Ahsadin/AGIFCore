# Phase 14 Demo: Mobile Constrained Profile

Phase 14 remains `open`. This demo is inspectable review material only.

## Mobile Profile Manifest

- same contract hash: `a4b5ddf226b315733337354ea7731744c45d57a5ea440bee9824dbc33b06a0be`
- laptop contract hash: `a4b5ddf226b315733337354ea7731744c45d57a5ea440bee9824dbc33b06a0be`
- active cell band: `{'min': 8, 'max': 24}`
- diagnostics scope: `bounded local diagnostics only`

## Budget Outcomes

- within-budget state: `within_budget`
- blocked state: `ceiling_blocked`
- blocked reason: `ACTIVE_CELL_BUDGET_EXCEEDED`

## Constrained Fail-Closed Path

- mobile fuel receipt: `FUEL_LIMIT_EXCEEDED`

## Evidence Links

- `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_profile_manifest_report.json`
- `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_active_cell_budget_report.json`
- `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_wasmtime_fuel_report.json`
- `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_evidence_manifest.json`

## Truth Note

- mobile stays on the same public runtime contract while using tighter bounded resources
- no approval or phase completion is implied
