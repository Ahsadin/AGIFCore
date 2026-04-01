# Phase 14 Demo: Sandbox Enforcement

Phase 14 remains `open`. This demo is inspectable review material only.

## Runtime Snapshot

- phase13 shell hash: `0631e6644cf655966fc8a79f1f75a5cd60b5bb14c5fdc76a7799f5b0ef63c638`
- wasmtime available: `True`
- sandbox policy count: `4`

## Enforcement Receipts

- allowed packaged execution: `pass` with stdout `3`
- tampered package: `BUNDLE_INTEGRITY_REQUIRED`
- fuel limit: `FUEL_LIMIT_EXCEEDED`
- memory limit: `MEMORY_LIMIT_EXCEEDED`
- wall timeout: `WALL_TIMEOUT_EXCEEDED`

## Evidence Links

- `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_sandbox_report.json`
- `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_wasmtime_fuel_report.json`
- `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_wasmtime_memory_report.json`
- `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_wasmtime_wall_time_report.json`
- `projects/agifcore_master/06_outputs/phase_14_sandbox_profiles_and_scale_realization/phase_14_evidence/phase_14_evidence_manifest.json`

## Truth Note

- sandbox enforcement is explicit and fail-closed
- no approval or phase completion is implied
