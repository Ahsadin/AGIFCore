# Phase 0 Source Freeze Inventory

## Purpose

This file freezes the source pools that AGIFCore Phase 1 must map explicitly.

## Frozen source pools

| Source Pool ID | Source Pool | Historical status | Allowed AGIFCore use | Blocked shortcut |
| --- | --- | --- | --- | --- |
| `SRC-001` | `agif_fabric_v1` | historical source | mine for fabric, workspace, memory, routing, authority, rollback, quarantine, tissue, benchmark, and release lineage | no direct “already done” claim |
| `SRC-002` | `agif-tasklet-cell` | historical source | mine for offline product, runner/gateway/UI split, schema contracts, bundle integrity, fail-closed UX, evidence packaging, installer, and sandbox lineage | no direct “already done” claim |
| `SRC-003` | `root v2 lineage` | archived historical source | mine only as source material under the AGIF v2 archival rule | no direct trust, carryover, or closure claim |
| `SRC-004` | `agif_v2_master` | archived historical source | mine only as source material under the AGIF v2 archival rule | no direct trust, carryover, or closure claim |

## Freeze rules

- No additional source pool may be treated as in-scope unless this inventory is updated under Governor control and logged in `CHANGELOG.md`.
- No source pool listed here may be silently omitted from `01_plan/SOURCE_INHERITANCE_MATRIX.md`.
- This inventory freezes source-pool scope only. It does not grant trust to any inherited code or proof.

## Boundary note

This inventory resolves the missing distinct source-freeze inventory artifact.
Detailed row-by-row inheritance work still belongs to Phase 1 execution.
