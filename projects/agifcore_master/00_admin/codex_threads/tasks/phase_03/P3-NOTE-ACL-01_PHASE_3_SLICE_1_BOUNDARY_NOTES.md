# Phase 3 Slice 1 Boundary Notes

## Scope of this note

This is a minimal pre-implementation boundary check for Phase 3 slice 1 only.

Covered slice-1 surfaces:

- `cell_contracts.py`
- `tissue_manifests.py`
- `bundle_manifest.py`
- `bundle_schema_validation.py`
- the matching slice-1 schemas and verifiers

Not covered here:

- trust bands
- activation policies
- split or merge implementation
- active or dormant control
- profile budget rule implementation
- bundle integrity hashing or attestation
- any Phase 4 memory logic

## Required boundary rules

1. `CellContract` must reference the approved Phase 2 cell identity and lifecycle substrate instead of replacing it.
   - `cell_id` must stay compatible with Phase 2 registry records.
   - lifecycle semantics must remain owned by the Phase 2 registry and lifecycle engine.
   - slice 1 may point to split or merge policy fields, but it may not implement split or merge behavior.

2. `TissueManifest` must remain structural.
   - it may define membership, allowed role families, and routing targets.
   - it may not carry semantic memory, procedural memory, graph structure, or world-model logic.
   - it may not create a second hidden scheduler or second lifecycle state machine.

3. `BundleManifest` must remain metadata plus schema-linkage surface only.
   - required provenance and manifest fields are allowed.
   - schema references are allowed.
   - payload inventory is allowed.
   - hashing, signatures, attestation, and full integrity enforcement are not slice-1 work.

4. `bundle_schema_validation.py` must enforce structure, not full later integrity.
   - fail closed on missing required fields or missing schema refs.
   - validate embedded contract and tissue payload shape against slice-1 schema surfaces.
   - do not silently downgrade invalid inputs.
   - do not treat sandboxing as a substitute for validation.

5. Slice 1 must respect the approved Phase 3 structural ceilings now.
   - treat `<= 64 KiB` as the manifest ceiling.
   - treat `<= 8 MiB` as the bundle payload ceiling.
   - treat `<= 16` direct cell members per tissue as the hard fanout ceiling.
   - treat `<= 8` routing targets per tissue manifest as the routing ceiling.
   - treat `> 8` cells per tissue as split-pressure or review territory, not normal unconstrained growth.

6. Verifier behavior must stay honest and slice-1-only.
   - the verifiers may prove contract shape and bundle schema validation.
   - they may not imply trust-band enforcement, split or merge behavior, or bundle integrity completion.

## Current blocker status

- No planning blocker was found for the boundary itself.
- Runtime and verifier files do not exist yet in this lane, so this note is a pre-build guardrail rather than a post-build approval.

## No approval implied

This note does not approve slice 1, Phase 3, or any later phase. It only freezes the minimal structural boundary that later slice-1 implementation must preserve.
