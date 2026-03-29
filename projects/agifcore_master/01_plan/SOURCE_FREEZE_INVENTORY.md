# Source Freeze Inventory

## Purpose

This is the canonical Phase 0 source-freeze inventory for AGIFCore.

## Canonical status

- This file is the closure-target source-freeze inventory for Phase 0.
- The older draft input `projects/agifcore_master/01_plan/PHASE_00_SOURCE_FREEZE_INVENTORY.md` remains a noncanonical draft input only.
- Closure and later review must use this canonical artifact name.

## Frozen source pools

| Source Pool ID | Source Pool | Historical status | Allowed AGIFCore use | Blocked shortcut |
| --- | --- | --- | --- | --- |
| `SRC-001` | `agif_fabric_v1` | historical source | mine for fabric, shared workspace, memory, routing, authority, rollback, quarantine, tissue, benchmark, and release lineage | no direct `already done` claim |
| `SRC-002` | `agif-tasklet-cell` | historical source | mine for offline product, runner/gateway/UI split, schema contracts, bundle integrity, fail-closed UX, evidence packaging, installer, and sandbox lineage | no direct `already done` claim |
| `SRC-003` | `root v2 lineage` | archived historical source | mine only under the AGIF v2 archival rule | no direct trust, carryover, or closure claim |
| `SRC-004` | `agif_v2_master` | archived historical source | mine only under the AGIF v2 archival rule | no direct trust, carryover, or closure claim |

## Inventory rules

- No additional source pool may be treated as in-scope unless this inventory is explicitly reopened under Governor control.
- No source pool listed here may be silently omitted from Phase 1 provenance work.
- This inventory freezes source-pool scope only. It does not grant trust to inherited code, inherited proof, or inherited demos.

## Downstream dependency

- `projects/agifcore_master/01_plan/SOURCE_INHERITANCE_MATRIX.md` must later cover every source pool listed here.
- `projects/agifcore_master/01_plan/COMPONENT_CATALOG.md` and `projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md` must later align to the same source-pool scope.

## Phase boundary

This artifact freezes source-pool scope only.
It does not perform the Phase 1 row-by-row inheritance mapping.
