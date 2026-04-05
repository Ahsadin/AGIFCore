from __future__ import annotations

from typing import Any, Mapping

from .contracts import CLOSURE_AUDIT_SCHEMA, MAX_CLOSURE_AUDIT_FINDINGS, stable_hash_payload


def build_closure_audit(
    *,
    phase13_manifest: Mapping[str, Any],
    phase14_manifest: Mapping[str, Any],
    phase15_manifest: Mapping[str, Any],
    phase_index_text: str,
    phase_gate_text: str,
    review_surface_paths: list[str],
) -> dict[str, object]:
    findings: list[dict[str, Any]] = []
    if str(phase13_manifest.get("status")) != "phase_13_verifier_family_pass":
        findings.append({"finding_id": "phase13_evidence_incomplete", "severity": "blocker"})
    if str(phase14_manifest.get("status")) != "phase_14_verifier_family_pass":
        findings.append({"finding_id": "phase14_evidence_incomplete", "severity": "blocker"})
    phase15_status = str(phase15_manifest.get("status"))
    phase15_missing_reports = list(phase15_manifest.get("missing_reports", []))
    phase15_invalid_reports = list(phase15_manifest.get("invalid_reports", []))
    phase15_non_pass_reports = sorted(
        [
            str(report.get("report_id", ""))
            for report in phase15_manifest.get("reports", [])
            if str(report.get("status")) != "pass"
        ]
    )
    phase15_review_ready = phase15_status == "phase_15_verifier_family_pass" or (
        phase15_status == "phase_15_verifier_family_incomplete"
        and sorted(phase15_missing_reports)
        in (
            [],
            ["phase_15_reproducibility_report.json"],
            ["phase_15_closure_audit_report.json"],
            [
                "phase_15_closure_audit_report.json",
                "phase_15_reproducibility_report.json",
            ],
        )
        and phase15_non_pass_reports in (
            [],
            ["closure_audit_report"],
            ["closure_audit_report", "reproducibility_report"],
            ["reproducibility_report"],
        )
        and not phase15_invalid_reports
    )
    if not phase15_review_ready:
        findings.append({"finding_id": "phase15_evidence_incomplete", "severity": "blocker"})
    phase_index_line = next(
        (line.strip() for line in phase_index_text.splitlines() if line.strip().startswith("| 15 |")),
        "",
    )
    if (
        "final intelligence proof and closure audit" not in phase_index_line
        or "`open`" not in phase_index_line
    ):
        findings.append({"finding_id": "phase_index_truth_mismatch", "severity": "blocker"})
    phase_gate_line = next(
        (line.strip() for line in phase_gate_text.splitlines() if line.strip().startswith("| 15 |")),
        "",
    )
    if "final intelligence proof and closure audit" not in phase_gate_line or "| open |" not in phase_gate_line:
        findings.append({"finding_id": "phase_gate_truth_mismatch", "severity": "blocker"})
    if len(review_surface_paths) < 5:
        findings.append({"finding_id": "review_surface_incomplete", "severity": "blocker"})
    if len(findings) > MAX_CLOSURE_AUDIT_FINDINGS:
        raise ValueError("closure-audit findings exceed escalation ceiling")
    payload = {
        "schema": CLOSURE_AUDIT_SCHEMA,
        "gate_status": "review_ready" if not findings else "blocked",
        "phase15_status": "open",
        "phase16_status": "open",
        "phase15_manifest_status_before_closure_report": phase15_status,
        "phase15_missing_reports_before_closure_report": phase15_missing_reports,
        "phase15_non_pass_reports_before_closure_report": phase15_non_pass_reports,
        "finding_count": len(findings),
        "findings": findings,
        "review_surface_paths": list(review_surface_paths),
        "verification_commands": [
            "python3 -m compileall projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof",
            "python3 -m compileall projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit",
            "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_closure_audit.py",
        ],
        "non_claims": [
            "does not approve Phase 15",
            "does not start Phase 16",
            "does not claim release or publication completion",
        ],
        "phase16_blocked": True,
    }
    return {**payload, "audit_hash": stable_hash_payload(payload)}
