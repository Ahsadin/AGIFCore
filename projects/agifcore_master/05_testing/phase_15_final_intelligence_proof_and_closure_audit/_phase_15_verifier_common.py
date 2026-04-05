from __future__ import annotations

import importlib
import json
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any, Mapping

PHASE = "15"
PHASE_NAME = "phase_15_final_intelligence_proof_and_closure_audit"
OUTPUT_ROOT_NAME = "06_outputs"
RUNTIME_PACKAGE = "agifcore_phase15_proof"
PHASE_15_RUNTIME_PARENT = (
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit"
)
PHASE_14_TEST_PARENT = "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization"

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md",
    "projects/agifcore_master/01_plan/PHASE_14_SANDBOX_PROFILES_AND_SCALE_REALIZATION.md",
    "projects/agifcore_master/01_plan/PHASE_13_PRODUCT_RUNTIME_AND_UX.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/01_plan/DEMO_PROTOCOL.md",
    "projects/agifcore_master/03_design/PRODUCT_RUNTIME_MODEL.md",
    "projects/agifcore_master/03_design/SANDBOX_MODEL.md",
    "projects/agifcore_master/03_design/DEPLOYMENT_MODEL.md",
    "projects/agifcore_master/03_design/PUBLIC_RELEASE_MODEL.md",
)

CONTRACT_REFS = (
    "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux/agifcore_phase13_product_runtime/product_runtime_shell.py",
    "projects/agifcore_master/04_execution/phase_14_sandbox_profiles_and_scale_realization/agifcore_phase14_sandbox/sandbox_profile_shell.py",
    "projects/agifcore_master/05_testing/phase_13_product_runtime_and_ux/_phase_13_verifier_common.py",
    "projects/agifcore_master/05_testing/phase_14_sandbox_profiles_and_scale_realization/_phase_14_verifier_common.py",
)

RUNTIME_FILES = (
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/contracts.py",
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/proof_runtime_shell.py",
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/blind_packs.py",
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/hidden_packs.py",
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/live_demo_pack.py",
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/soak_harness.py",
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/hardening_package.py",
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/reproducibility_package.py",
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/closure_audit.py",
    "projects/agifcore_master/04_execution/phase_15_final_intelligence_proof_and_closure_audit/agifcore_phase15_proof/__init__.py",
)

COMMON_TEST_FILE = (
    "projects/agifcore_master/05_testing/phase_15_final_intelligence_proof_and_closure_audit/_phase_15_verifier_common.py"
)

REQUIRED_REPORT_FILES = (
    "phase_15_blind_pack_report.json",
    "phase_15_hidden_pack_report.json",
    "phase_15_live_demo_pack_report.json",
    "phase_15_real_desktop_chat_demo_report.json",
    "phase_15_soak_summary.json",
    "phase_15_hardening_report.json",
    "phase_15_interactive_chat_report.json",
    "phase_15_reproducibility_report.json",
    "phase_15_closure_audit_report.json",
)

EXPECTED_REPORT_VERIFIERS = {
    "phase_15_blind_pack_report.json": "verify_phase_15_blind_packs",
    "phase_15_hidden_pack_report.json": "verify_phase_15_hidden_packs",
    "phase_15_live_demo_pack_report.json": "verify_phase_15_live_demo_pack",
    "phase_15_real_desktop_chat_demo_report.json": "verify_phase_15_real_desktop_chat_demo",
    "phase_15_soak_summary.json": "verify_phase_15_soak_harness",
    "phase_15_hardening_report.json": "verify_phase_15_hardening_package",
    "phase_15_interactive_chat_report.json": "verify_phase_15_interactive_chat",
    "phase_15_reproducibility_report.json": "verify_phase_15_reproducibility",
    "phase_15_closure_audit_report.json": "verify_phase_15_closure_audit",
}


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
TEST_ROOT = PROJECT_ROOT / "05_testing" / PHASE_NAME
PHASE_OUTPUT_ROOT = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = PHASE_OUTPUT_ROOT / "phase_15_evidence"
DEMO_DIR = PHASE_OUTPUT_ROOT / "phase_15_demo_bundle"
REVIEW_BUNDLE_DIR = PHASE_OUTPUT_ROOT / "phase_15_review_bundle"
REVIEW_BUNDLE_ZIP = PHASE_OUTPUT_ROOT / "phase_15_review_bundle.zip"
MANIFEST_PATH = EVIDENCE_DIR / "phase_15_evidence_manifest.json"
PHASE13_MANIFEST_PATH = (
    PROJECT_ROOT
    / "06_outputs"
    / "phase_13_product_runtime_and_ux"
    / "phase_13_evidence"
    / "phase_13_evidence_manifest.json"
)
PHASE14_MANIFEST_PATH = (
    PROJECT_ROOT
    / "06_outputs"
    / "phase_14_sandbox_profiles_and_scale_realization"
    / "phase_14_evidence"
    / "phase_14_evidence_manifest.json"
)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_paths() -> None:
    for runtime_parent in (
        REPO_ROOT / PHASE_15_RUNTIME_PARENT,
        REPO_ROOT / "projects" / "agifcore_master" / "04_execution" / "phase_13_product_runtime_and_ux",
        REPO_ROOT / PHASE_14_TEST_PARENT,
    ):
        runtime_str = str(runtime_parent)
        if runtime_str not in sys.path:
            sys.path.insert(0, runtime_str)


ensure_runtime_import_paths()

import _phase_14_verifier_common as p14c
from agifcore_phase15_proof.contracts import (
    MAX_PHASE15_BUNDLE_BYTES,
    canonical_size_bytes,
    stable_hash_payload,
)
from agifcore_phase15_proof.proof_runtime_shell import Phase15ProofRuntimeShell


def dump_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def missing_files(paths: list[str]) -> list[str]:
    return [path for path in paths if not (REPO_ROOT / path).exists()]


def runtime_modules_available(module_names: tuple[str, ...]) -> bool:
    try:
        for module_name in module_names:
            importlib.import_module(module_name)
    except Exception:
        return False
    return True


def dedupe_paths(paths: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        result.append(path)
    return result


def checked_files_for(verifier_file: str) -> list[str]:
    return dedupe_paths([*PLAN_REFS, *CONTRACT_REFS, *RUNTIME_FILES, COMMON_TEST_FILE, verifier_file])


def build_blocked_report(
    *,
    verifier: str,
    report_path: Path,
    checked_files: list[str],
    assertion_ids: list[str],
    blocker_kind: str,
    blocker_message: str,
    missing: list[str] | None = None,
) -> dict[str, Any]:
    blocker: dict[str, Any] = {"kind": blocker_kind, "message": blocker_message}
    if missing:
        blocker["missing_files"] = missing
    return {
        "phase": PHASE,
        "verifier": verifier,
        "status": "blocked",
        "blocker": blocker,
        "checked_files": checked_files,
        "assertions": [{"id": item, "result": "blocked"} for item in assertion_ids],
        "outputs": {"report": rel(report_path), "manifest": rel(MANIFEST_PATH)},
        "notes": ["Phase 15 remains open", "no approval implied"],
    }


def build_pass_report(
    *,
    verifier: str,
    report_path: Path,
    checked_files: list[str],
    assertions: list[dict[str, Any]],
    anchors: Mapping[str, Any],
    notes: list[str],
) -> dict[str, Any]:
    return {
        "phase": PHASE,
        "verifier": verifier,
        "status": "pass",
        "checked_files": checked_files,
        "assertions": assertions,
        "outputs": {"report": rel(report_path), "manifest": rel(MANIFEST_PATH)},
        "anchors": dict(anchors),
        "notes": [*notes, "Phase 15 remains open", "no approval implied"],
    }


def refresh_evidence_manifest() -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    missing_reports: list[str] = []
    invalid_reports: list[str] = []
    for filename in REQUIRED_REPORT_FILES:
        report_path = EVIDENCE_DIR / filename
        if not report_path.exists():
            missing_reports.append(filename)
            continue
        payload = load_json(report_path)
        status = str(payload.get("status", "unknown"))
        if status not in {"pass", "blocked"}:
            invalid_reports.append(filename)
        if payload.get("phase") != PHASE:
            invalid_reports.append(filename)
        if payload.get("verifier") != EXPECTED_REPORT_VERIFIERS[filename]:
            invalid_reports.append(filename)
        reports.append(
            {
                "report_id": filename.removeprefix("phase_15_").removesuffix(".json"),
                "path": rel(report_path),
                "status": status,
            }
        )
    invalid_reports = sorted(set(invalid_reports))
    overall_pass = (
        not missing_reports
        and not invalid_reports
        and len(reports) == len(REQUIRED_REPORT_FILES)
        and all(report["status"] == "pass" for report in reports)
    )
    manifest = {
        "phase": PHASE,
        "phase_remains_open": True,
        "required_report_count": len(REQUIRED_REPORT_FILES),
        "available_report_count": len(reports),
        "missing_reports": missing_reports,
        "invalid_reports": invalid_reports,
        "reports": reports,
        "status": "phase_15_verifier_family_pass"
        if overall_pass
        else "phase_15_verifier_family_incomplete",
        "output_bundle_size_bytes": phase15_output_bundle_size_bytes(),
        "output_bundle_within_planning_ceiling": phase15_output_bundle_size_bytes()
        <= MAX_PHASE15_BUNDLE_BYTES,
        "notes": [
            "this manifest tracks machine-readable verifier outputs only",
            "Phase 15 remains open",
            "manifest is rebuilt from actual report files on disk",
            "no approval implied",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def write_report(report_path: Path, payload: Mapping[str, Any]) -> None:
    dump_json(report_path, payload)
    refresh_evidence_manifest()


def build_report_path_map() -> dict[str, Path]:
    return {
        filename.removeprefix("phase_15_").removesuffix(".json"): EVIDENCE_DIR / filename
        for filename in REQUIRED_REPORT_FILES
    }


def build_demo_path_map() -> dict[str, Path]:
    return {
        "phase_15_real_desktop_chat_demo": DEMO_DIR / "phase_15_real_desktop_chat_demo.json",
        "phase_15_final_demo": DEMO_DIR / "phase_15_final_demo.json",
        "phase_15_soak_summary_demo": DEMO_DIR / "phase_15_soak_summary_demo.json",
        "phase_15_closure_audit_summary_demo": DEMO_DIR / "phase_15_closure_audit_summary_demo.json",
    }


def build_review_surface_paths() -> list[str]:
    candidates = [
        PROJECT_ROOT / "01_plan" / "PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md",
        MANIFEST_PATH,
        EVIDENCE_DIR / "phase_15_blind_pack_report.json",
        EVIDENCE_DIR / "phase_15_hidden_pack_report.json",
        EVIDENCE_DIR / "phase_15_live_demo_pack_report.json",
        EVIDENCE_DIR / "phase_15_real_desktop_chat_demo_report.json",
        EVIDENCE_DIR / "phase_15_soak_summary.json",
        EVIDENCE_DIR / "phase_15_hardening_report.json",
        EVIDENCE_DIR / "phase_15_interactive_chat_report.json",
        EVIDENCE_DIR / "phase_15_reproducibility_report.json",
        EVIDENCE_DIR / "phase_15_closure_audit_report.json",
        DEMO_DIR / "phase_15_demo_index.md",
        DEMO_DIR / "phase_15_real_desktop_chat_demo.json",
        DEMO_DIR / "phase_15_real_desktop_chat_demo.md",
        DEMO_DIR / "phase_15_final_demo.md",
        DEMO_DIR / "phase_15_soak_summary_demo.md",
        DEMO_DIR / "phase_15_closure_audit_summary_demo.md",
        DEMO_DIR / "INTERACTIVE_CHAT.md",
        DEMO_DIR / "launch_phase_15_interactive_chat.sh",
        DEMO_DIR / "launch_phase_15_real_desktop_chat_demo.sh",
        PROJECT_ROOT / "00_admin" / "codex_threads" / "tasks" / "phase_15" / "P15-AUDIT-01_PHASE_15_FINAL_PACKAGE_AUDIT_REPORT.md",
        PROJECT_ROOT / "00_admin" / "codex_threads" / "handoffs" / "PHASE_15_GOVERNOR_VERIFICATION_RECORD.md",
        PROJECT_ROOT / "00_admin" / "codex_threads" / "handoffs" / "PHASE_15_VALIDATION_REQUEST.md",
    ]
    return [rel(path) for path in candidates if path.exists()]


def load_phase_status_texts() -> tuple[str, str]:
    phase_index_text = (
        PROJECT_ROOT / "01_plan" / "PHASE_INDEX.md"
    ).read_text(encoding="utf-8")
    phase_gate_text = (
        PROJECT_ROOT / "01_plan" / "PHASE_GATE_CHECKLIST.md"
    ).read_text(encoding="utf-8")
    return phase_index_text, phase_gate_text


def load_upstream_manifests() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return (
        load_json(PHASE13_MANIFEST_PATH),
        load_json(PHASE14_MANIFEST_PATH),
        load_json(MANIFEST_PATH) if MANIFEST_PATH.exists() else refresh_evidence_manifest(),
    )


def phase15_output_bundle_size_bytes() -> int:
    total = 0
    if not PHASE_OUTPUT_ROOT.exists():
        return total
    for path in PHASE_OUTPUT_ROOT.rglob("*"):
        if path.is_file():
            total += path.stat().st_size
    return total


def run_phase15_shells() -> dict[str, Any]:
    weak_phase14 = p14c.run_phase14_shell(scenario="weak")
    contradiction_phase14 = p14c.run_phase14_shell(scenario="contradiction")
    weak_shell = Phase15ProofRuntimeShell(
        phase13_shell=weak_phase14["phase13"]["shell"],
        phase14_shell=weak_phase14["shell"],
    )
    contradiction_shell = Phase15ProofRuntimeShell(
        phase13_shell=contradiction_phase14["phase13"]["shell"],
        phase14_shell=contradiction_phase14["shell"],
    )
    return {
        "weak": {
            "phase14": weak_phase14,
            "shell": weak_shell,
            "snapshot": weak_shell.runtime_snapshot(),
        },
        "contradiction": {
            "phase14": contradiction_phase14,
            "shell": contradiction_shell,
            "snapshot": contradiction_shell.runtime_snapshot(),
        },
        "proof_shells": {
            "weak": weak_shell,
            "contradiction": contradiction_shell,
        },
        "combined_snapshot_hash": stable_hash_payload(
            {
                "weak": weak_shell.runtime_snapshot(),
                "contradiction": contradiction_shell.runtime_snapshot(),
            }
        ),
    }


def write_demo_payload(*, filename: str, payload: Mapping[str, Any]) -> Path:
    path = DEMO_DIR / filename
    dump_json(path, payload)
    return path


def write_demo_markdown(*, filename: str, lines: list[str]) -> Path:
    path = DEMO_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def build_demo_index() -> None:
    index_json = {
        "phase": PHASE,
        "status": "open",
        "scenario_files": [
            "phase_15_real_desktop_chat_demo.json",
            "phase_15_final_demo.json",
            "phase_15_soak_summary_demo.json",
            "phase_15_closure_audit_summary_demo.json",
            "launch_phase_15_real_desktop_chat_demo.sh",
            "launch_phase_15_interactive_chat.sh",
        ],
        "supporting_evidence_manifest": "phase_15_evidence_manifest.json",
        "notes": [
            "summary only",
            "Phase 15 remains open",
            "no approval implied",
        ],
    }
    write_demo_payload(filename="phase_15_demo_index.json", payload=index_json)
    write_demo_markdown(
        filename="phase_15_demo_index.md",
        lines=[
            "# Phase 15 Demo Index",
            "",
            "Phase 15 remains `open`. This bundle is for inspection only and does not imply approval or finality.",
            "",
            "Demo scenarios:",
            "",
            "- `phase_15_real_desktop_chat_demo.md` for the primary non-terminal desktop UI chat host.",
            "- `phase_15_final_demo.md` for the governed final live-demo pack path.",
            "- `phase_15_soak_summary_demo.md` for the bounded local soak summary path.",
            "- `phase_15_closure_audit_summary_demo.md` for the closure-audit review path.",
            "- `INTERACTIVE_CHAT.md` and `launch_phase_15_interactive_chat.sh` for the secondary terminal debug path.",
            "",
            "Supporting demo payloads:",
            "",
            "- `phase_15_real_desktop_chat_demo.json`",
            "- `phase_15_final_demo.json`",
            "- `phase_15_soak_summary_demo.json`",
            "- `phase_15_closure_audit_summary_demo.json`",
            "",
            "Evidence source:",
            "",
            f"- [{MANIFEST_PATH.name}]({MANIFEST_PATH})",
            "",
            "Truth note:",
            "",
            "- the bundle is local-file inspectable only",
            "- no approval language is used",
        ],
    )


def _review_bundle_source_paths() -> list[Path]:
    candidates = [
        PROJECT_ROOT / "01_plan" / "PHASE_15_FINAL_INTELLIGENCE_PROOF_AND_CLOSURE_AUDIT.md",
        PROJECT_ROOT / "00_admin" / "codex_threads" / "tasks" / "phase_15" / "P15-AUDIT-01_PHASE_15_FINAL_PACKAGE_AUDIT_REPORT.md",
        PROJECT_ROOT / "00_admin" / "codex_threads" / "handoffs" / "PHASE_15_EXECUTION_START_BRIEF.md",
        PROJECT_ROOT / "00_admin" / "codex_threads" / "handoffs" / "PHASE_15_GOVERNOR_VERIFICATION_RECORD.md",
        PROJECT_ROOT / "00_admin" / "codex_threads" / "handoffs" / "PHASE_15_VALIDATION_REQUEST.md",
        MANIFEST_PATH,
        *build_report_path_map().values(),
        DEMO_DIR / "phase_15_demo_index.json",
        DEMO_DIR / "phase_15_demo_index.md",
        DEMO_DIR / "phase_15_real_desktop_chat_demo.json",
        DEMO_DIR / "phase_15_real_desktop_chat_demo.md",
        DEMO_DIR / "phase_15_final_demo.json",
        DEMO_DIR / "phase_15_final_demo.md",
        DEMO_DIR / "phase_15_soak_summary_demo.json",
        DEMO_DIR / "phase_15_soak_summary_demo.md",
        DEMO_DIR / "phase_15_closure_audit_summary_demo.json",
        DEMO_DIR / "phase_15_closure_audit_summary_demo.md",
        DEMO_DIR / "INTERACTIVE_CHAT.md",
        DEMO_DIR / "launch_phase_15_interactive_chat.sh",
        DEMO_DIR / "launch_phase_15_real_desktop_chat_demo.sh",
    ]
    deduped: list[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        if not path.exists() or path in seen:
            continue
        seen.add(path)
        deduped.append(path)
    return deduped


def refresh_review_bundle() -> None:
    REVIEW_BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
    for path in REVIEW_BUNDLE_DIR.iterdir():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

    for source_path in _review_bundle_source_paths():
        shutil.copy2(source_path, REVIEW_BUNDLE_DIR / source_path.name)

    review_lines = [
        "# Phase 15 Review Bundle",
        "",
        "This bundle contains the refreshed Phase 15 execution package and review chain.",
        "It includes the repaired live-turn path, the primary real desktop chat host, the secondary terminal debug surface, and the machine-readable evidence required to inspect them locally.",
        "",
        "- Phase 15 remains `open`.",
        "- Phase 16 has not started.",
        "",
        "## Review Order",
        "",
        "1. `P15-AUDIT-01_PHASE_15_FINAL_PACKAGE_AUDIT_REPORT.md`",
        "2. `PHASE_15_GOVERNOR_VERIFICATION_RECORD.md`",
        "3. `PHASE_15_VALIDATION_REQUEST.md`",
        "4. `phase_15_evidence_manifest.json`",
        "5. `phase_15_real_desktop_chat_demo_report.json`",
        "6. `phase_15_real_desktop_chat_demo.md`",
        "7. `launch_phase_15_real_desktop_chat_demo.sh`",
        "8. `phase_15_interactive_chat_report.json`",
        "9. `INTERACTIVE_CHAT.md`",
        "10. `launch_phase_15_interactive_chat.sh`",
        "11. `phase_15_closure_audit_report.json`",
        "12. `phase_15_reproducibility_report.json`",
        "13. `phase_15_demo_index.md`",
        "",
        "## What This Bundle Proves",
        "",
        f"- all `{len(REQUIRED_REPORT_FILES)}` Phase 15 verifiers passed",
        f"- all `{len(build_demo_path_map())}` scripted Phase 15 demos were generated",
        "- the primary final user demo is a real local desktop UI chat host over the approved Phase 13 runtime seam",
        "- the secondary terminal chat path remains available for debug and evidence inspection",
        "- the live-turn engine answers supported local AGIFCore questions from local truth, binds follow-ups to prior turn state, and fails closed honestly when support is weak",
        "- blind packs, hidden packs, the live-demo pack, the soak harness, the hardening package, the reproducibility package, and the closure audit are all backed by machine-readable outputs",
        "- the evidence manifest reports `phase_15_verifier_family_pass`",
        "- the phase remains `open`",
        "",
        "## Truth Note",
        "",
        "- no approval is implied",
        "- no Phase 16 work is included",
    ]
    (REVIEW_BUNDLE_DIR / "REVIEW_FIRST.md").write_text(
        "\n".join(review_lines) + "\n",
        encoding="utf-8",
    )

    with zipfile.ZipFile(REVIEW_BUNDLE_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(REVIEW_BUNDLE_DIR.iterdir()):
            archive.write(path, arcname=path.name)


def evidence_manifest_anchor() -> dict[str, Any]:
    manifest = refresh_evidence_manifest()
    return {
        "manifest_path": rel(MANIFEST_PATH),
        "manifest_status": manifest["status"],
        "required_report_count": manifest["required_report_count"],
        "available_report_count": manifest["available_report_count"],
        "bundle_size_bytes": manifest["output_bundle_size_bytes"],
        "bundle_size_within_ceiling": manifest["output_bundle_within_planning_ceiling"],
        "manifest_hash": stable_hash_payload(manifest),
        "manifest_size_bytes": canonical_size_bytes(manifest),
    }
