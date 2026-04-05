from __future__ import annotations

from pathlib import Path
from typing import Mapping

from .contracts import (
    MAX_REPRODUCIBILITY_ARTIFACT_COUNT,
    REPRODUCIBILITY_PACKAGE_SCHEMA,
    file_sha256,
    stable_hash_payload,
)


def build_reproducibility_package(
    *,
    repo_root: Path,
    report_paths: Mapping[str, Path],
    demo_paths: Mapping[str, Path],
    evidence_manifest_path: Path,
) -> dict[str, object]:
    tracked = []
    for artifact_id, path in [*report_paths.items(), *demo_paths.items()]:
        tracked.append(
            {
                "artifact_id": artifact_id,
                "path": str(path.relative_to(repo_root)),
                "sha256": file_sha256(path),
                "size_bytes": path.stat().st_size,
            }
        )
    if len(tracked) > MAX_REPRODUCIBILITY_ARTIFACT_COUNT:
        raise ValueError("reproducibility artifact count exceeds planning ceiling")
    commands = [
        "python3 -m compileall projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime",
        "python3 -m compileall projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof",
        "python3 -m compileall projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_blind_packs.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_hidden_packs.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_live_demo_pack.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_real_desktop_chat_demo.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_soak_harness.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_hardening_package.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_interactive_chat.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_reproducibility.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/verify_phase_15_closure_audit.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/run_phase_15_real_desktop_chat_demo.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/run_phase_15_final_demo.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/run_phase_15_soak_summary_demo.py",
        "python3 projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/run_phase_15_closure_audit_summary_demo.py",
    ]
    payload = {
        "schema": REPRODUCIBILITY_PACKAGE_SCHEMA,
        "artifact_count": len(tracked),
        "tracked_artifacts": tracked,
        "verification_commands": commands,
        "evidence_manifest": str(evidence_manifest_path.relative_to(repo_root)),
        "evidence_manifest_tracked_by_path_only": True,
        "phase16_blocked": True,
        "notes": [
            "this package is local rerun guidance only",
            "the evidence manifest is tracked by path instead of hash because the manifest is refreshed after the final verifier writes",
            "it does not imply approval or publication",
        ],
    }
    return {**payload, "package_hash": stable_hash_payload(payload)}
