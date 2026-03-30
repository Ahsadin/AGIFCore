# Phase 4 Validation Request

Phase 4 is ready for user review, but it remains open. No approval is implied by this request.

Please inspect these files in this order:

1. Review context and rules
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-VA-02/projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-TC-VA-02_PHASE_4_FINAL_VALIDATION_REQUEST.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-VA-02/projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-VA-02/projects/agifcore_master/01_plan/PHASE_04_MEMORY_PLANES.md`

2. Independent checks already completed
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-ASA-05/projects/agifcore_master/00_admin/codex_threads/tasks/phase_04/P4-AUDIT-06_PHASE_4_FINAL_PACKAGE_REAUDIT_REPORT.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-VA-02/projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_04_GOVERNOR_VERIFICATION_RECORD.md`

3. User-facing demo bundle
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-REL-02/projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_demo_bundle/phase_04_demo_index.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-REL-02/projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_demo_bundle/phase_04_memory_carry_forward_demo.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-REL-02/projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_demo_bundle/phase_04_correction_demo.md`
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-REL-02/projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_demo_bundle/phase_04_forgetting_compression_demo.md`

4. Evidence package behind the demos
   - `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-MA-04/projects/agifcore_master/06_outputs/phase_04_memory_planes/phase_04_evidence/phase_04_evidence_manifest.json`

5. Optional deep inspection surfaces
   - runtime: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-MA-04/projects/agifcore_master/04_execution/phase_04_memory_planes/agifcore_phase4_memory/`
   - testing: `/Users/ahsadin/Documents/AGIFCore/.worktrees/P4-TC-MA-04/projects/agifcore_master/05_testing/phase_04_memory_planes/`

What good looks like:

- the re-audit report says the final package passed audit while keeping Phase 4 open
- the Governor verification record says the full verifier family was rerun and the demo bundle was directly checked
- the demo pages open cleanly and stay review-only
- the evidence manifest and linked reports match the demo claims
- no file claims Phase 4 is approved, complete, or closed
- no file starts Phase 5

What failure looks like:

- a listed file is missing or points to the wrong surface
- the demo bundle and evidence package do not agree
- any file implies approval, closure, or Phase 5 start
- you find a blocker that makes the Phase 4 package unfit for review approval

Please reply with exactly one of these verdicts:

- `approved`
- `rejected`
- `approved_with_blockers`

If you choose `approved_with_blockers` or `rejected`, include the blockers you want corrected. Until an explicit user verdict exists, Phase 4 remains open.
