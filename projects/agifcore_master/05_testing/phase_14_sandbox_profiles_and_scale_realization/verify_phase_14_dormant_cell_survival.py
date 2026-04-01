from __future__ import annotations

import json

import _phase_14_verifier_common as vc

VERIFIER = "verify_phase_14_dormant_cell_survival"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/verify_phase_14_dormant_cell_survival.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_14_dormant_survival_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase14_sandbox.dormant_cell_survival",
    "agifcore_phase14_sandbox.sandbox_profile_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "proof-case-count-bounded",
    "continuity-preserved",
    "memory-anchor-preserved",
    "shutdown-and-export-anchors-present",
]


def _proof_is_stable(proof: dict[str, object]) -> bool:
    return all(
        case["preserved_identity"]
        and case["preserved_lineage"]
        and case["preserved_continuity"]
        and case["preserved_memory_anchor"]
        and case["preserved_policy_envelope"]
        for case in proof["cases"]
    )


def build_pass_report() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    shell = result["shell"]
    mobile_proof = shell.dormant_cell_survival(profile="mobile")
    laptop_proof = shell.dormant_cell_survival(profile="laptop")
    builder_proof = shell.dormant_cell_survival(profile="builder")
    for proof in (mobile_proof, laptop_proof, builder_proof):
        assert proof["case_count"] <= 12
        assert proof["shutdown_receipt_hash"]
        assert proof["state_export_hash"]
        assert proof["memory_review_export_hash"]
        assert _proof_is_stable(proof)
    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "proof-case-count-bounded", "result": "pass"},
            {"id": "continuity-preserved", "result": "pass"},
            {"id": "memory-anchor-preserved", "result": "pass"},
            {"id": "shutdown-and-export-anchors-present", "result": "pass"},
        ],
        anchors={
            "mobile_proof": mobile_proof,
            "laptop_proof": laptop_proof,
            "builder_proof": builder_proof,
        },
        notes=["dormant survival proofs stay tied to exported continuity and shutdown anchors instead of prose-only claims"],
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
            blocker_message="dormant survival verifier could not import its runtime modules or found missing files",
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
