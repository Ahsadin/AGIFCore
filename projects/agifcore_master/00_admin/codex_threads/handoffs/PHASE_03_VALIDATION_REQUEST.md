# Phase 3 Validation Request

Phase 3 is ready for user review, but it remains open. No approval is implied by this request.

Please inspect these files in this order:

1. Review context and rules
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-PG-05/projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-TC-VA-04_PHASE_3_VALIDATION_REQUEST.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-PG-05/projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-PG-05/projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md`

2. Independent checks already completed
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-ASA-05/projects/agifcore_master/00_admin/codex_threads/tasks/phase_03/P3-AUDIT-07_PHASE_3_FINAL_PACKAGE_AUDIT_REPORT.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-PG-05/projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_03_GOVERNOR_VERIFICATION_RECORD.md`

3. User-facing demo bundle
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-REL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_demo_index.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-REL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_tissue_orchestration_demo.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-REL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_split_merge_demo.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-REL-04/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_demo_bundle/phase_03_bundle_validation_demo.md`

4. Evidence package behind the demos
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-PG-05/projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json`

5. Optional deep inspection surfaces
   - runtime: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-PG-05/projects/agifcore_master/04_execution/phase_03_cells_tissues_structure_and_bundles/agifcore_phase3_structure/`
   - testing: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P3-TC-PG-05/projects/agifcore_master/05_testing/phase_03_cells_tissues_structure_and_bundles/`

What good looks like:

- the audit report says the final package passed audit while keeping Phase 3 open
- the governor verification record says the verifiers were rerun and the demo bundle was directly checked
- the demo pages open cleanly and stay review-only
- the evidence manifest and linked reports match the demo claims
- no file claims Phase 3 is approved, complete, or closed

What failure looks like:

- a listed file is missing or points to the wrong surface
- the demo bundle and evidence package do not agree
- any file implies approval, closure, or Phase 4 start
- you find a blocker that makes the Phase 3 package unfit for review approval

Please reply with exactly one of these verdicts:

- `approved`
- `rejected`
- `approved_with_blockers`

If you choose `approved_with_blockers` or `rejected`, include the blockers you want corrected. Until an explicit user verdict exists, Phase 3 remains open.
