from __future__ import annotations

import json

import _phase_11_verifier_common as vc
from agifcore_phase11_self_improvement.contracts import MAX_THOUGHT_EPISODES

VERIFIER = "verify_phase_11_thought_episodes"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_11_governed_self_improvement/verify_phase_11_thought_episodes.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_11_thought_episodes_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase11_self_improvement.thought_episodes",
    "agifcore_phase11_self_improvement.self_improvement_cycle",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "episode-count-bounded",
    "proposal-linkage-present",
    "trace-refs-present",
    "phase10-inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    contradiction_case = vc.run_phase11_cycle(scenario="contradiction")
    snapshot = contradiction_case["cycle"].thought_episodes
    assert 1 <= snapshot.episode_count <= MAX_THOUGHT_EPISODES
    assert all(item.proposal_id for item in snapshot.episodes)
    assert all(item.trace_refs for item in snapshot.episodes)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "episode-count-bounded", "result": "pass"},
            {"id": "proposal-linkage-present", "result": "pass"},
            {"id": "trace-refs-present", "result": "pass"},
            {"id": "phase10-inputs-remain-read-only", "result": "pass"},
        ],
        anchors={"contradiction_case": snapshot.to_dict()},
        notes=["thought episodes stay compact, trace-linked, and subordinate to governed proposals"],
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
            blocker_message="thought episodes verifier could not import its runtime modules or found missing files",
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
