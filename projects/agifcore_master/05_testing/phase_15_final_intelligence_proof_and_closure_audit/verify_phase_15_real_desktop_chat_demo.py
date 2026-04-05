from __future__ import annotations

import json
from urllib import request

import _phase_15_verifier_common as vc

VERIFIER = "verify_phase_15_real_desktop_chat_demo"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_real_desktop_chat_demo.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_15_real_desktop_chat_demo_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase13_product_runtime.product_runtime_shell",
    "run_phase_15_real_desktop_chat_demo",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "desktop-demo-payload-builds",
    "desktop-demo-host-serves-real-ui",
    "desktop-demo-turns-use-live-path",
    "desktop-demo-follow-up-and-scenario-switch-work",
]


def _load_json(url: str) -> dict[str, object]:
    with request.urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def _post_json(url: str, payload: dict[str, object]) -> dict[str, object]:
    encoded = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def build_pass_report() -> dict[str, object]:
    import run_phase_15_real_desktop_chat_demo as desktop_demo

    payload = desktop_demo.build_demo_payload()
    assert payload["schema"] == "agifcore.phase_15.real_desktop_chat_demo.v1"
    assert payload["demo_id"] == "real_desktop_chat_demo"
    assert payload["host_kind"] == "local_desktop_ui_browser_host"
    assert payload["runtime_host"] == "approved_phase13_desktop_ui"
    assert payload["ui_schema"] == "agifcore.phase_13.local_desktop_chat_demo.v1"
    assert payload["ui_snapshot"]["selected_view"] == "chat_workspace"
    assert payload["ui_snapshot"]["view_count"] == 7
    assert payload["ui_snapshot"]["message_count"] >= 6
    assert len(payload["turn_summaries"]) == len(payload["sample_prompts"]) == 3
    assert payload["turn_summaries"][0]["phase_chain_completed"] is True
    assert len(payload["turn_summaries"][0]["phase_results"]) == 14

    server = desktop_demo.RealDesktopChatDemoServer(scenario="weak", port=0).start()
    try:
        state_payload = _load_json(server.url + "api/state")
        assert state_payload["scenario"] == "weak"
        assert state_payload["ui_snapshot"]["schema"] == "agifcore.phase_13.local_desktop_chat_demo.v1"
        assert state_payload["ui_snapshot"]["selected_view"] == "chat_workspace"

        capability_payload = _post_json(server.url + "api/turn", {"user_text": "what can you do"})
        capability_turn = capability_payload["turn"]
        assert capability_turn["question_class"] == "project_phase_capability"
        assert capability_turn["answer_mode"] in {"grounded_fact", "bounded_estimate"}
        assert capability_turn["phase_chain_completed"] is True
        assert capability_turn["phase_chain_phase_ids"] == list(range(2, 16))
        assert len(capability_turn["phase_results"]) == 14
        assert capability_payload["ui_snapshot"]["message_count"] >= 2
        assert capability_payload["ui_snapshot"]["latest_turn"]["phase_chain_completed"] is True
        assert len(capability_payload["ui_snapshot"]["latest_turn"]["phase_results"]) == 14

        follow_up_payload = _post_json(server.url + "api/turn", {"user_text": "what evidence supports that"})
        follow_up_turn = follow_up_payload["turn"]
        assert follow_up_turn["question_class"] == "support_diagnostics"
        assert follow_up_turn["follow_up_bound"] is True
        assert len(follow_up_turn["local_truth_refs"]) >= 1
        assert follow_up_payload["ui_snapshot"]["latest_turn"]["question_class"] == "support_diagnostics"
        assert len(follow_up_payload["ui_snapshot"]["latest_turn"]["phase_results"]) == 14

        scenario_payload = _post_json(server.url + "api/scenario", {"scenario": "contradiction"})
        assert scenario_payload["scenario"] == "contradiction"
        assert scenario_payload["ui_snapshot"]["message_count"] == 0

        contradiction_payload = _post_json(
            server.url + "api/turn",
            {"user_text": "is there any contradiction between the phase index and gate checklist for phase 15"},
        )
        contradiction_turn = contradiction_payload["turn"]
        assert contradiction_turn["question_class"] == "contradiction"
        assert contradiction_turn["final_answer_mode"] == "grounded_fact"
    finally:
        server.close()

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "desktop-demo-payload-builds", "result": "pass"},
            {"id": "desktop-demo-host-serves-real-ui", "result": "pass"},
            {"id": "desktop-demo-turns-use-live-path", "result": "pass"},
            {"id": "desktop-demo-follow-up-and-scenario-switch-work", "result": "pass"},
        ],
        anchors={
            "desktop_demo_payload": payload,
            "state_payload": state_payload,
            "capability_turn": capability_turn,
            "follow_up_turn": follow_up_turn,
            "contradiction_turn": contradiction_turn,
            "evidence_manifest": vc.evidence_manifest_anchor(),
        },
        notes=[
            "the primary non-terminal Phase 15 demo is a real local desktop UI host over the approved Phase 13 runtime seam",
            "the desktop UI presents runtime truth only and routes turns through the repaired interactive path",
            "scenario switching resets the local host without creating a second responder",
        ],
    )


def main() -> int:
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    missing = vc.missing_files(checked_files)
    if missing or not vc.runtime_modules_available(RUNTIME_IMPORTS):
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=checked_files,
            assertion_ids=ASSERTION_IDS,
            blocker_kind="missing_runtime_or_dependencies",
            blocker_message="real desktop chat demo verifier could not import its runtime modules or found missing files",
            missing=missing,
        )
        vc.write_report(REPORT_PATH, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    try:
        report = build_pass_report()
    except Exception as exc:
        report = vc.build_blocked_report(
            verifier=VERIFIER,
            report_path=REPORT_PATH,
            checked_files=checked_files,
            assertion_ids=ASSERTION_IDS,
            blocker_kind="verification_failed",
            blocker_message=str(exc),
        )
        vc.write_report(REPORT_PATH, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1
    vc.write_report(REPORT_PATH, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
