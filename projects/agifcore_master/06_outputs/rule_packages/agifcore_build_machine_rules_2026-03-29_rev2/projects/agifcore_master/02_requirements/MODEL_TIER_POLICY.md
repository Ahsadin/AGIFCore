# Model Tier Policy

## Purpose

Freeze which model tier is used for which kind of build-machine work.

These model roles apply to the build process only.
They are not part of the shipped AGIFCore runtime.

## Tier 1: Global Judgment

Recommended model:

- `GPT-5.4`

Use for:

- architecture judgment
- contract freezes
- phase arbitration
- final validation reading
- high-ambiguity decisions

## Tier 2: Hardest Coding Work

Recommended model:

- `GPT-5.3-Codex`

Use for:

- long-horizon implementation
- cross-file refactors
- integration work
- deep debugging
- merge conflict repair

## Tier 3: Default Scoped Worker Work

Recommended model:

- `GPT-5.4 mini`

Use for:

- well-scoped subagent tasks
- source mapping
- interface checks
- test writing
- doc sync
- schema work
- narrow coding tasks

## Tier 4: Cheap High-Volume Utility Work

Recommended model:

- `GPT-5.4 nano`

Use for:

- classification
- extraction
- ranking
- diff labeling
- log triage
- checklist checks
- routing

## Escalation Rule

- use `GPT-5.4 nano` first for classify, extract, rank, and route work
- use `GPT-5.4 mini` first for well-defined low-ambiguity tasks
- use `GPT-5.3-Codex` when behavior changes across files, modules, or long-running code paths
- use `GPT-5.4` when whole-system judgment or final evaluation is required

## Snapshot Rule

When dated snapshots are available, prefer them for critical roles so behavior stays stable across long AGIFCore phases.

## Freeze Rule

This model-tier policy is frozen until the user explicitly approves a revision.
