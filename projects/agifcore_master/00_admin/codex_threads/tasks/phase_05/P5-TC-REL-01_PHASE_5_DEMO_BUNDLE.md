# P5-TC-REL-01 Phase 5 Demo Bundle

## Header

- Task Card ID: `P5-TC-REL-01`
- Phase: `5`
- Title: `Phase 5 Demo Bundle`
- Status: `open`
- Issued By: `Program Governor`
- Issued On: `2026-03-30`

## Role Assignment

- Active Build Role: `Release & Evidence Lead`
- Supporting Roles: `Program Governor`
- Allowed Models: `gpt-5.4 mini`
- Build Pod Agent Session ID: `separate_role_lane_required`
- Merge Arbiter Session ID: `not_assigned`
- Validation Agent Session ID: `not_assigned`
- Required Reads:
  - `projects/agifcore_master/01_plan/PHASE_05_GRAPH_AND_KNOWLEDGE_STRUCTURES.md`
  - `projects/agifcore_master/01_plan/DEMO_PROTOCOL.md`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_evidence_manifest.json`
  - all Phase 5 evidence reports

## Scope Control

- Owned Files:
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/P5-TC-REL-01_PHASE_5_DEMO_BUNDLE.md`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/phase_05_demo_index.md`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/phase_05_graph_reuse_demo.md`
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/phase_05_transfer_demo.md`
- Forbidden Files:
  - any `projects/agifcore_master/04_execution/*`
  - any `projects/agifcore_master/05_testing/*`
  - any audit or validation handoff
  - all Phase 6+ artifacts
- Allowed Folders:
  - `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_demo_bundle/`
  - `projects/agifcore_master/00_admin/codex_threads/tasks/phase_05/`
- Forbidden Folders:
  - `projects/agifcore_master/04_execution/`
  - `projects/agifcore_master/05_testing/`

## Branch And Worktree

- Branch Name: `codex/tc-p5-tc-rel-01-phase-5-demo-bundle`
- Worktree Path: `.worktrees/P5-TC-REL-01`
- Rollback Tag Name: `rollback/P5-TC-REL-01/<yyyymmdd-hhmm>`

## Objective

- Goal: package the graph reuse demo and transfer demo from real Phase 5 evidence only.
- Expected Outputs:
  - this task card
  - the complete Phase 5 demo bundle
- Non-Goals:
  - runtime changes
  - verifier changes
  - phase approval

## Work Method

1. Read the evidence manifest and all seven machine-readable reports.
2. Write a demo index that points to the exact evidence artifacts.
3. Write one graph reuse demo and one transfer demo using only evidence-backed claims.
4. Keep the demo inspectable and phase-local.

## Cross-Checks

- No unsupported summary text.
- No approval language.
- No Phase 6 claims.

## Exit Criteria

- All three required demo files exist.
- Each demo points to exact evidence paths.
- The demo bundle is ready for audit.

## Handoff Target

- `Program Governor`

## Explicit Proof No Approval Is Implied

- Demo assembly is packaging only and does not approve or complete Phase 5.
