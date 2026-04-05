# AGIFCore Architecture

## Overview

AGIFCore is a governed local intelligence baseline.

Its purpose is to answer supported questions from local truth, maintain turn continuity, and fail closed when support is missing.

The final architecture should be read as a bounded runtime core, not as a general chat stack.

## Core behavior

AGIFCore is designed to:

- identify the question type
- locate the right local support
- bind follow-up questions to prior turn state
- detect contradiction or ambiguity
- choose a safe answer mode
- emit inspectable evidence for the turn

## Main layers

### Memory and continuity

- prior-turn state is kept for follow-up binding
- runtime state tracks the previous request, answer mode, support state, and unresolved ambiguity
- follow-up handling is grounded in stored turn structure rather than generic repetition

### Local truth and retrieval

- supported answers come from local project files, manifests, evidence, and runtime-facing records
- the runtime distinguishes supported local truth from unsupported external truth
- unsupported questions fail closed instead of being converted into fake grounded answers

### Graph, world, and critique support

- graph and provenance structures support local retrieval and explanation
- bounded world reasoning supports narrow estimate-style answers when exact live truth is unavailable
- critique and diagnosis lanes help detect contradiction, ambiguity, or support gaps before response composition

### Runtime governance

- question class selection determines the allowed answer mode
- answer modes stay bounded to grounded fact, bounded estimate, clarify, abstain, or search-needed behavior
- the runtime records which phases and support surfaces were actually exercised

### Proof and audit surfaces

- machine-readable gate outputs support the bounded claim
- shadow-benchmark outputs check paraphrase generalization
- anti-shortcut review checks that the claim is not benchmark-shaped or synthetic
- publication packaging creates a cleaner public-facing evidence layer without widening the claim

## What the runtime is not

AGIFCore is not:

- a broad open-ended chat system
- a general AGI system
- a free-form world model for everything
- a hidden-cloud answer service

## High-level flow

1. A user asks a question.
2. The runtime classifies the question.
3. The runtime checks local support and prior-turn state.
4. The runtime selects a safe answer mode.
5. The runtime produces a final response only after the bounded chain completes.
6. The runtime records machine-readable evidence for review.

## Supported behavior

The verified baseline supports:

- local system and project questions
- runtime and evidence questions
- simple math and structured reasoning
- comparison and planning questions
- follow-up questions
- contradiction and ambiguity handling
- bounded current-world estimates
- honest unsupported-question fail-closed behavior

## Design principle

The system should behave like a bounded local intelligence core, not like a polished general chat product.

That distinction is part of the claim boundary.
