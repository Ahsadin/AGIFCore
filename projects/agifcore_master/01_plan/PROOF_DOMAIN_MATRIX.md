# Proof Domain Matrix

## Purpose

This file freezes the eight proof domains named by the master plan and the minimum proof path each domain must later support.

This file is a Phase 1 planning and closure artifact. It does not claim that any proof domain is already implemented or demonstrated.

## Locked proof-domain rules

- The proof-domain list may not be renamed, merged, or reduced without explicit master-plan revision.
- Every domain must later support:
  - local baseline
  - fabric run without transfer
  - fabric run with transfer
  - governed conversation layer
  - replayable traces
  - laptop and mobile profile checks
- If a domain is not represented here, it does not count as part of AGIFCore proof.

## Locked proof-domain matrix

| Domain | Canonical scope | Why it is locked in Phase 1 | Minimum later proof path |
| --- | --- | --- | --- |
| `finance_document_workflows` | document-heavy finance operations under governed handling | proves structured reasoning, traceability, and evidence-heavy workflow support | local baseline, fabric without transfer, fabric with transfer, governed conversation, replayable traces, laptop/mobile checks |
| `pos_store_operations` | point-of-sale and store-floor operational support | proves real-time operational coordination under constrained environments | local baseline, fabric without transfer, fabric with transfer, governed conversation, replayable traces, laptop/mobile checks |
| `procurement_work_order_processing` | procurement, work-order, and fulfillment handling | proves multi-step planning and controlled execution across operational queues | local baseline, fabric without transfer, fabric with transfer, governed conversation, replayable traces, laptop/mobile checks |
| `claims_case_handling` | claims and case-style workflow support | proves governed evidence handling, escalation, and case continuity | local baseline, fabric without transfer, fabric with transfer, governed conversation, replayable traces, laptop/mobile checks |
| `maintenance_diagnostics` | maintenance triage and diagnostic reasoning | proves fault isolation, explanation quality, and procedural follow-through | local baseline, fabric without transfer, fabric with transfer, governed conversation, replayable traces, laptop/mobile checks |
| `building_home_infrastructure_events` | home, building, and infrastructure event support | proves event interpretation, multi-system coordination, and safe boundary handling | local baseline, fabric without transfer, fabric with transfer, governed conversation, replayable traces, laptop/mobile checks |
| `planning_coordination_workflows` | planning, coordination, and governance-heavy workflow support | proves high-order planning, sequencing, and artifact control under governance | local baseline, fabric without transfer, fabric with transfer, governed conversation, replayable traces, laptop/mobile checks |
| `compliance_support_triage` | compliance-oriented intake, triage, and evidence review | proves fail-closed handling, boundary discipline, and auditability | local baseline, fabric without transfer, fabric with transfer, governed conversation, replayable traces, laptop/mobile checks |

## Phase 1 use

- `DOMAIN_MATRIX.md` in `02_requirements/` must stay aligned with the domain names frozen here.
- Later demo and validation work must point to these exact eight domains.
- Any later phase artifact that uses a different domain name should be treated as drift until reconciled.

## Cross-References

- `projects/agifcore_master/01_plan/MASTER_PLAN.md`
- `projects/agifcore_master/02_requirements/DOMAIN_MATRIX.md`
- `projects/agifcore_master/01_plan/PHASE_01_CONSTITUTION_AND_FULL_SYSTEM_BLUEPRINT.md`
