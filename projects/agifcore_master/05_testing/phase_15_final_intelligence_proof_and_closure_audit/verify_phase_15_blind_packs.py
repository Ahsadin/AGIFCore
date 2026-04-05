from __future__ import annotations

import json

import _phase_15_verifier_common as vc

VERIFIER = "verify_phase_15_blind_packs"
VERIFIER_FILE = "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_blind_packs.py"
REPORT_PATH = vc.EVIDENCE_DIR / "phase_15_blind_pack_report.json"
RUNTIME_IMPORTS = (
    "agifcore_phase15_proof.blind_packs",
    "agifcore_phase15_proof.proof_runtime_shell",
)
ASSERTION_IDS = [
    "runtime-imports-available",
    "blind-pack-count-bounded",
    "blind-case-catalog-frozen",
    "blind-pack-results-pass",
    "blind-packs-remain-non-subjective",
]


def build_pass_report() -> dict[str, object]:
    from agifcore_phase15_proof.blind_packs import run_blind_pack_catalog

    shells = vc.run_phase15_shells()
    weak_shell = shells["proof_shells"]["weak"]
    catalog = weak_shell.blind_packs()
    result = run_blind_pack_catalog(
        pack_catalog=catalog,
        proof_shells=shells["proof_shells"],
        output_dir=vc.EVIDENCE_DIR,
    )

    assert catalog["blind_pack_count"] == 2
    assert result["total_case_count"] == 8
    assert result["passed_case_count"] == 8
    assert result["status"] == "pass"
    assert all(pack["subjective_override_allowed"] is False for pack in catalog["packs"])

    checked_files = vc.checked_files_for(VERIFIER_FILE)
    return vc.build_pass_report(
        verifier=VERIFIER,
        report_path=REPORT_PATH,
        checked_files=checked_files,
        assertions=[
            {"id": "runtime-imports-available", "result": "pass"},
            {"id": "blind-pack-count-bounded", "result": "pass"},
            {"id": "blind-case-catalog-frozen", "result": "pass"},
            {"id": "blind-pack-results-pass", "result": "pass"},
            {"id": "blind-packs-remain-non-subjective", "result": "pass"},
        ],
        anchors={
            "weak_shell_snapshot": shells["weak"]["snapshot"],
            "contradiction_shell_snapshot": shells["contradiction"]["snapshot"],
            "blind_pack_catalog": catalog,
            "blind_pack_result": result,
            "evidence_manifest": vc.evidence_manifest_anchor(),
        },
        notes=[
            "blind packs run against the real approved Phase 13 and Phase 14 shells",
            "blind case expectations stay frozen and machine-checkable",
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
            blocker_message="blind-pack verifier could not import its runtime modules or found missing files",
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
