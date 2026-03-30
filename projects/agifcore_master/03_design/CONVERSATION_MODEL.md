# Conversation Model

## Purpose

This file defines the first-pass conversation surface for AGIFCore.

The conversation layer is the language and interaction surface above the cognition core and below the user-facing product shell.

## Core conversation rules

- Conversation must honor the trace contract on every governed turn.
- Language quality does not count as proof of support by itself.
- The system must remain honest when support is weak by using governed outcomes rather than fluent bluffing.
- Conversation must preserve inspectable links to planning, simulation, critique, governance, and memory review where applicable.

## Surface responsibilities

- accept user turns and governed internal turns through the runtime contract
- select an allowed `discourse_mode`
- expose support-state honesty
- return either an answer, an abstention, or a governed next action
- preserve replayable references to the underlying trace surfaces

## Boundary to product runtime

- The UI presents the conversation.
- The gateway transports and validates the turn.
- The runner produces the governed trace surfaces.
- The conversation model must not collapse those boundaries into one opaque layer.

## Dependency notes

- Exact language behavior remains constrained by `CONVERSATION_SCOPE.md` and `NORTH_STAR_LANGUAGE_TARGET.md`.
- Later reasoning, simulator, and memory layers will refine what support the conversation surface can expose.
- This first-pass model freezes the surface contract and honesty rules before later runtime work.

## Cross-References

- `projects/agifcore_master/01_plan/TRACE_CONTRACT.md`
- `projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md`
- `projects/agifcore_master/03_design/GOVERNANCE_MODEL.md`
