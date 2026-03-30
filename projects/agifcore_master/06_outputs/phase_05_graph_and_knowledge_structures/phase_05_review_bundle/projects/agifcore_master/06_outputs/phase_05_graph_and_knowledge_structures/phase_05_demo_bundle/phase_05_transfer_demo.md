# Phase 5 Transfer Demo

## Purpose

This demo shows governed transfer behavior for Phase 5. It is backed by the transfer report, conflict/supersession report, and evidence manifest only.

## What Exists

- Transfer graph runtime exists and passed verification in `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_transfer_graph_report.json`.
- Conflict and supersession behavior exists and passed verification in `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_conflict_and_supersession_report.json`.
- Provenance links exist and passed verification in `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_provenance_links_report.json`.

## Evidence-Backed Transfer Cases

- Same-domain approval is present in the transfer report.
- Cross-domain transfer without explicit transfer approval is denied.
- Cross-domain transfer with explicit transfer approval and an authority review reference is approved.
- Low-quality transfer is abstained.
- Retired-source transfer is blocked.
- Load-state round-trip verification passes.

## What The User Should Inspect

- `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_transfer_graph_report.json`
- `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_conflict_and_supersession_report.json`
- `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_provenance_links_report.json`

## What This Demo Proves

- Transfer is governed and read-only.
- Explicit transfer approval is required for cross-domain approval.
- Authority review reference is retained for approved cross-domain transfer.
- Conflict and supersession outcomes are real runtime decisions.

## What This Demo Does Not Claim

- It does not claim Phase 5 approval.
- It does not claim Phase 5 completion.
- It does not claim Phase 6 behavior.
- It does not claim Phase 7 behavior.
