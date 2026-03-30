# Phase 5 Review Bundle

This bundle preserves repo-root-relative paths under:

- `projects/agifcore_master/...`

Phase 5 is ready for review, but it is still `open`.
Nothing in this bundle means Phase 5 is approved.

## Review Order

1. Read the plan and protocol files:
   - `projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md`
   - `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
   - `projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md`
   - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
2. Read the governance checks:
   - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-AUDIT-01_PHASE_5_FINAL_PACKAGE_AUDIT_REPORT.md`
   - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-NOTE-ACL-01_PHASE_5_BOUNDARY_NOTES.md`
   - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_GOVERNOR_VERIFICATION_RECORD.md`
   - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_MERGE_HANDOFF.md`
   - `projects/agifcore_master/00_admin/codex_threads/handoffs/PHASE_05_VALIDATION_REQUEST.md`
3. Read the design files:
   - `projects/agifcore_master/03_design/GRAPH_STACK_MODEL.md`
   - `projects/agifcore_master/03_design/SKILL_GRAPH_MODEL.md`
   - `projects/agifcore_master/03_design/MEMORY_MODEL.md`
   - `projects/agifcore_master/03_design/WORKSPACE_MODEL.md`
4. Read the demo bundle:
   - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/phase_05_demo_index.md`
   - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/phase_05_graph_reuse_demo.md`
   - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/phase_05_transfer_demo.md`
5. Check the evidence:
   - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_evidence_manifest.json`
   - all seven `phase_05_*_report.json` files in the same folder
6. If you want deeper inspection:
   - runtime: `projects/agifcore_master/04_execution/phase_05_graph_and_knowledge_structures/agifcore_phase5_graph/`
   - tests: `projects/agifcore_master/05_testing/phase_05_graph_and_knowledge_structures/`

## What Good Looks Like

- The evidence manifest shows all seven required reports and `status: phase_5_verifier_family_pass`.
- The demo bundle matches the evidence reports.
- The graph layers are separate: descriptor, skill, concept, and transfer.
- Provenance, conflict, supersession, and support selection are real runtime behavior.
- Cross-domain transfer requires explicit approval and an authority review reference.
- No file claims Phase 5 is approved or closed.
- No file starts Phase 6.

## What Failure Looks Like

- A listed file is missing.
- The demo claims do not match the evidence JSON.
- A graph layer is missing or collapsed into one mixed structure.
- Provenance or transfer governance is only described in prose and not reflected in runtime behavior.
- Any file says Phase 5 is approved, complete, or closed.

## Reply Format

Please reply with exactly one of:

- `approved`
- `approved_with_blockers`
- `rejected`

If you choose `approved_with_blockers` or `rejected`, include the blockers you want fixed.
