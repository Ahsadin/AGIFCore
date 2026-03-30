# Phase 5 Graph Reuse Demo

## Purpose

This demo shows that Phase 5 reuses governed substrate where appropriate and keeps the graph layers distinct. It is backed by the runtime reports and the evidence manifest only.

## What Exists

- Descriptor graph runtime exists and passed verification in `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_descriptor_graph_report.json`.
- Skill graph runtime exists and passed verification in `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_skill_graph_report.json`.
- Concept graph runtime exists and passed verification in `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_concept_graph_report.json`.
- Reusable support selection exists and passed verification in `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_support_selection_report.json`.
- Provenance links exist and passed verification in `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_provenance_links_report.json`.

## Evidence-Backed Reuse Signals

- The descriptor report shows a retired descriptor, a superseded descriptor, and an active replacement descriptor with separate provenance and trust states.
- The skill report shows a superseded skill and an active replacement skill with distinct preconditions, postconditions, and provenance.
- The concept report shows a superseded concept and an active replacement concept with abstraction-only content.
- The support-selection report shows graph-grounded selection across descriptor, concept, and skill layers, with candidate ceilings and policy filtering enforced.
- The provenance report shows required roles, a fanout ceiling, score computation, and tampering rejection through round-trip verification.

## What The User Should Inspect

- `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_descriptor_graph_report.json`
- `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_skill_graph_report.json`
- `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_concept_graph_report.json`
- `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_provenance_links_report.json`
- `projects/agifcore_master/06_outputs/phase_05_graph_and_knowledge_structures/phase_05_evidence/phase_05_support_selection_report.json`

## What This Demo Proves

- Descriptor, skill, and concept are separate graph layers.
- Reuse is governed by provenance and trust, not by hidden shortcuts.
- Support selection is bounded and graph-grounded.
- Provenance is enforced as structured data, not a label.

## What This Demo Does Not Claim

- It does not claim Phase 5 approval.
- It does not claim Phase 5 completion.
- It does not claim Phase 6 behavior.
- It does not claim Phase 7 behavior.
