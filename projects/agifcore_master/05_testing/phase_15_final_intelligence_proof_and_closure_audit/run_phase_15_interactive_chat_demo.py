from __future__ import annotations

import json

import _phase_15_verifier_common as vc


HELP_TEXT = """Commands:
- type any question and press Enter
- /scenario weak
- /scenario contradiction
- /show-json
- /help
- /exit
"""


def print_intro() -> None:
    print("Phase 15 Interactive Chat Demo")
    print("Phase 15 remains open. This is local review material only.")
    print("Current scenario: weak")
    print(
        "This demo uses the real bounded AGIFCore live turn path. Your typed request drives local routing, support selection, and fail-closed response logic."
    )
    print(HELP_TEXT)


def print_turn_summary(payload: dict[str, object], *, scenario: str) -> None:
    response = payload
    print("")
    print(f"scenario: {scenario}")
    print(f"class: {response['question_class']}")
    print(f"request: {response['question_text']}")
    print(f"response: {response['response_text']}")
    print(f"answer_mode: {response['answer_mode']}")
    print(f"final_answer_mode: {response['final_answer_mode']}")
    print(f"kind: {response['response_kind']}")
    print(f"support_state: {response['support_state']}")
    print(f"uncertainty_band: {response['uncertainty_band']}")
    print(f"live_measurement_required: {response['live_measurement_required']}")
    print(f"next_action: {response['next_action']}")
    print(f"phases: {', '.join(str(item) for item in response['phases_exercised'])}")
    print(f"session_id: {payload['session_id']}")
    refs = response.get("local_truth_refs", [])
    if refs:
        print(f"local_truth_refs: {', '.join(refs[:3])}")
    print("")


def main() -> int:
    shells = vc.run_phase15_shells()["proof_shells"]
    scenario = "weak"
    show_json = False
    print_intro()
    while True:
        try:
            raw = input("agif> ").strip()
        except EOFError:
            print("")
            break
        if not raw:
            continue
        if raw in {"/exit", "/quit"}:
            break
        if raw == "/help":
            print(HELP_TEXT)
            continue
        if raw == "/show-json":
            show_json = not show_json
            print(f"raw JSON output: {'on' if show_json else 'off'}")
            continue
        if raw.startswith("/scenario "):
            selected = raw.split(" ", 1)[1].strip().lower()
            if selected not in {"weak", "contradiction"}:
                print("Allowed scenarios: weak, contradiction")
                continue
            scenario = selected
            print(f"scenario switched to: {scenario}")
            continue
        shell = shells[scenario].phase13_shell
        payload = shell.interactive_turn(user_text=raw)
        print_turn_summary(payload, scenario=scenario)
        if show_json:
            print(json.dumps(payload, indent=2, sort_keys=True))
            print("")
    print("interactive demo closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
