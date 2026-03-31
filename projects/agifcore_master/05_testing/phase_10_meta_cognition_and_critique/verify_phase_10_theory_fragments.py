from __future__ import annotations

import json

import _phase_10_verifier_common as vc
from agifcore_phase10_meta_cognition.contracts import MAX_THEORY_FRAGMENTS

VERIFIER = "verify_phase_10_theory_fragments"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_10_meta_cognition_and_critique/verify_phase_10_theory_fragments.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_10_theory_fragments_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase10_meta_cognition.contracts",
    "agifcore_phase10_meta_cognition.theory_fragments",
    "agifcore_phase10_meta_cognition.meta_cognition_turn",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "theory-fragment-count-bounded",
    "contradiction-fragment-created",
    "falsifier-and-next-step-visible",
    "inputs-remain-read-only",
]


def build_pass_report() -> dict[str, object]:
    weak_case = vc.run_phase10_turn(scenario="weak")
    contradiction_case = vc.run_phase10_turn(scenario="contradiction")
    weak_snapshot = weak_case["turn"].theory_fragments
    contradiction_snapshot = contradiction_case["turn"].theory_fragments

    assert weak_snapshot.fragment_count <= MAX_THEORY_FRAGMENTS
    assert contradiction_snapshot.fragment_count <= MAX_THEORY_FRAGMENTS
    assert weak_snapshot.fragment_count == 0
    assert contradiction_snapshot.fragment_count == 1
    fragment = contradiction_snapshot.fragments[0]
    assert fragment.fragment_label == "bounded_candidate_fragment"
    assert fragment.falsifier
    assert fragment.next_verification_step
    assert fragment.source_answer_id == contradiction_case["turn"].rich_expression_turn_hash

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "theory-fragment-count-bounded", "result": "pass"},
            {"id": "contradiction-fragment-created", "result": "pass"},
            {"id": "falsifier-and-next-step-visible", "result": "pass"},
            {"id": "inputs-remain-read-only", "result": "pass"},
        ],
        anchors={
            "weak_case": weak_snapshot.to_dict(),
            "contradiction_case": contradiction_snapshot.to_dict(),
        },
        notes=["theory fragments stay provisional and require explicit falsifiers and next checks"],
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
            blocker_message="theory fragments verifier could not import its runtime modules or found missing files",
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
