# Phase 15 Interactive Chat

The primary Phase 15 chat demo is now the real desktop UI host.
This terminal path remains available as a secondary debug and evidence-inspection surface.

## Primary Demo First

```sh
cd <repo_root>
sh projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_demo_bundle/launch_phase_15_real_desktop_chat_demo.sh
```

Use the browser-hosted desktop UI if you want a real non-terminal chat experience.

## Run

```sh
cd <repo_root>
sh projects/agifcore_master/06_outputs/phase_15_final_intelligence_proof_and_closure_audit/phase_15_demo_bundle/launch_phase_15_interactive_chat.sh
```

## What You Can Do

- type your own question
- type `/scenario weak` to see the bounded weak-support path
- type `/scenario contradiction` to see the bounded clarification path
- type `/show-json` to toggle the full gateway payload
- type `/exit` to quit

## What The Live Turn Now Does

- routes your actual question through the bounded AGIFCore runtime path
- selects local truth and runtime sources based on question class
- binds follow-up prompts to prior turn state when the context is sufficient
- handles bounded arithmetic, comparison/planning, contradiction checks, and current-world target grounding without using a prompt-answer table
- records per-turn phase usage, support state, local sources, and final response mode
- answers, clarifies, abstains, or returns `search_needed` honestly from local support

## How To Review

- prefer `launch_phase_15_real_desktop_chat_demo.sh` for the main user-facing demo
- start with `launch_phase_15_interactive_chat.sh`
- ask your own question at the `agif>` prompt
- inspect `phase_15_interactive_chat_report.json` for question class, local sources, support state, next action, and phase usage
- use `/show-json` if you want the full turn payload in the terminal

## Truth Note

- the primary Phase 15 chat demo host is the real desktop UI path
- this terminal path uses the same repaired local approved product-runtime path through the Phase 15 demo shell
- it is still a bounded review demo, not a finished public chat product
- Phase 15 remains `open`
- Phase 16 has not started
