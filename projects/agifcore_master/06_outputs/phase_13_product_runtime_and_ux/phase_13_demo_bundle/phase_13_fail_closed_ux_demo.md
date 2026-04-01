# Phase 13 Demo: Fail-Closed UX

Phase 13 remains `open`. This demo is inspectable review material only.

## Explicit Blocked States

- task_submit reason: `reserved_surface_fail_closed`
- policy_update reason: `reserved_surface_fail_closed`
- unknown route reason: `unknown_route`

## Why The UX Is Fail-Closed

- task_submit guidance: `Task submission stays blocked in the first Phase 13 slice. Use conversation_turn instead.`
- policy_update guidance: `Policy updates stay blocked in Phase 13 so the product shell cannot self-widen runtime policy.`
- unknown route guidance: `The requested local route is not allowlisted for this product shell.`

## Evidence Links

- `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/phase_13_local_gateway_report.json`
- `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/phase_13_fail_closed_ux_report.json`
- `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/phase_13_desktop_ui_report.json`
- `projects/agifcore_master/06_outputs/phase_13_product_runtime_and_ux/phase_13_evidence/phase_13_evidence_manifest.json`

## Truth Note

- blocked paths stay visible instead of being dressed up as success
- no approval or phase completion is implied
