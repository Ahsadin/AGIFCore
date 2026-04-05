# AGIFCore Architecture

## Overview

AGIFCore is a governed local-intelligence baseline.

Its job is not to answer everything.
Its job is to answer supported questions from local truth, preserve turn continuity, choose a safe answer mode, and fail closed when support is missing.

The final architecture should be read as a bounded runtime core, not as a general chat stack.

## System Scope

AGIFCore is designed for:

- local project and runtime truth
- bounded reasoning over supported inputs
- explicit continuity between turns
- inspectable evidence and review surfaces

AGIFCore is not designed for:

- broad open-domain chat
- unrestricted external world knowledge
- hidden-cloud correctness
- free-form unbounded conversational behavior

## Runtime Flow

The live turn path follows a bounded chain:

1. classify the request into a supported question family
2. detect whether the turn is standalone, follow-up, contradictory, underspecified, or unsupported
3. gather local support from runtime state, project files, manifests, evidence, or prior-turn structure
4. decide whether the target is grounded enough to answer safely
5. choose an answer mode
6. produce the final response only after the bounded chain completes
7. write machine-readable evidence about what was used and why

## Core Subsystems

### Question interpretation

The runtime first decides what kind of question it is handling.
That classification controls what evidence is allowed and which answer modes are legal.

The bounded gate evaluated ten major class families:

- identity and system questions
- project, phase, and capability questions
- local runtime and evidence questions
- math and structured reasoning
- comparison and planning
- bounded current-world estimates
- contradiction and inconsistency handling
- follow-up questions
- underspecified questions
- unsupported questions

### Local truth and retrieval

Supported answers come from local project truth and runtime truth.
Typical sources include:

- project planning and requirement files
- runtime snapshots and exported state
- evidence manifests and review bundles
- prior-turn memory and continuity state
- graph and provenance references when explanation needs traceable support

The runtime explicitly separates:

- grounded local support
- bounded estimate support
- insufficient support
- unsupported external truth

That separation is what keeps the system fail-closed instead of hallucinating.

### Continuity and follow-up binding

AGIFCore stores structured prior-turn state rather than relying on generic conversational repetition.

Follow-up handling uses fields such as:

- prior request text
- detected question class
- support state
- next action
- answer mode
- unresolved ambiguity
- extracted target or entity

This allows prompts such as `why`, `what did I ask`, or `are you sure` to bind back to the right prior turn when confidence is high enough.

### Critique, contradiction, and ambiguity handling

Before composing a response, the runtime checks whether the turn is internally contradictory, too vague, or missing support.

This critique path can push the system toward:

- clarify
- abstain
- search needed
- bounded answer with explicit uncertainty

The goal is not conversational smoothness at any cost.
The goal is support-state honesty.

### Bounded world reasoning

AGIFCore supports narrow estimate-style current-world questions only when they fit the bounded contract.

That means:

- the target kind must be recognized
- the system must stay explicit about uncertainty
- no fake live factual grounding is allowed
- unsupported current-world questions must fail closed

This is deliberately narrower than general world knowledge.

### Answer modes

The runtime uses a small bounded set of answer modes rather than an open-ended response policy.

The important public modes are:

- `grounded_fact`
- `bounded_estimate`
- `clarify`
- `abstain`
- `search_needed`

Each mode implies different obligations for support, caution, and evidence recording.

### Proof and audit surfaces

AGIFCore does not rely on answer text alone.
It writes machine-readable records that describe what the system did on each turn.

The bounded gate spec requires fields such as:

- `request_text`
- `detected_question_class`
- `local_sources_consulted`
- `support_state`
- `next_action`
- `answer_mode`
- `phases_actually_exercised`
- `memory_used`
- `graph_or_provenance_used`
- `simulation_or_world_model_used`
- `critique_or_diagnosis_fired`
- `final_response`
- `pass_or_fail`

These records feed three proof layers:

- the frozen bounded-intelligence gate
- the paraphrased shadow benchmark
- the anti-shortcut audit

## Supported Behavior

The verified baseline supports:

- local system and project questions
- runtime and evidence questions
- simple math and structured reasoning
- comparison and planning inside local support limits
- follow-up questions grounded in prior state
- contradiction and ambiguity handling
- bounded current-world estimates
- honest unsupported-question fail-closed behavior

## Why The Architecture Is Bounded

AGIFCore is strongest when it stays tied to:

- known local support
- explicit answer modes
- inspectable evidence
- selective continuity
- fail-closed behavior

That is enough to support the bounded-intelligence claim.
It is not enough to support a broad general-chat claim, and the architecture is intentionally not presented that way.
