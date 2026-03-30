from __future__ import annotations

import importlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

PHASE_NAME = "phase_03_cells_tissues_structure_and_bundles"
PHASE_LABEL = "Phase 3"
SLICE_ID = "slice_3"
VERIFICATION_NAME = "split_merge"
TEST_ROOT_NAME = "05_testing"
OUTPUT_ROOT_NAME = "06_outputs"
EXECUTION_ROOT_NAME = "04_execution"

RUNTIME_IMPORTS = ("split_merge_rules",)
RUNTIME_FILES = ("split_merge_rules.py",)
SUPPORTING_IMPORTS = (
    "cell_contracts",
    "tissue_manifests",
    "trust_bands",
    "active_dormant_control",
)

PLAN_REFS = (
    "projects/agifcore_master/01_plan/PHASE_03_CELLS_TISSUES_STRUCTURE_AND_BUNDLES.md",
    "projects/agifcore_master/01_plan/TRACE_CONTRACT.md",
    "projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
    "projects/agifcore_master/02_requirements/DEPLOYMENT_PROFILES.md",
)

SUPPORTING_EVIDENCE_REFS = (
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_cell_contracts_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_activation_and_trust_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_bundle_validation_report.json",
    "projects/agifcore_master/06_outputs/phase_03_cells_tissues_structure_and_bundles/phase_03_evidence/phase_03_evidence_manifest.json",
)


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    target: str
    expected_pass: bool
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "target": self.target,
            "expected_pass": self.expected_pass,
            "passed": self.passed,
            "message": self.message,
        }


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root from verifier path")


REPO_ROOT = find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
TESTING_DIR = PROJECT_ROOT / TEST_ROOT_NAME / PHASE_NAME
OUTPUT_DIR = PROJECT_ROOT / OUTPUT_ROOT_NAME / PHASE_NAME
EVIDENCE_DIR = OUTPUT_DIR / "phase_03_evidence"
RUNTIME_DIR = PROJECT_ROOT / EXECUTION_ROOT_NAME / PHASE_NAME / "agifcore_phase3_structure"
REPORT_PATH = EVIDENCE_DIR / "phase_03_split_merge_report.json"
MANIFEST_PATH = EVIDENCE_DIR / "phase_03_evidence_manifest.json"


class ContractViolation(ValueError):
    pass


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_import_path() -> None:
    runtime_path = str(RUNTIME_DIR)
    if runtime_path not in sys.path:
        sys.path.insert(0, runtime_path)


ensure_runtime_import_path()


def dump_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def missing_files(paths: list[Path]) -> list[str]:
    return [rel(path) for path in paths if not path.exists()]


def import_runtime_module(module_name: str) -> Any | None:
    try:
        return importlib.import_module(module_name)
    except Exception:  # noqa: BLE001 - surfaced in the report.
        return None


def runtime_modules_available() -> bool:
    return all(import_runtime_module(module_name) is not None for module_name in RUNTIME_IMPORTS)


def supporting_modules_available() -> bool:
    return all(import_runtime_module(module_name) is not None for module_name in SUPPORTING_IMPORTS)


def refresh_evidence_manifest() -> dict[str, Any]:
    reports: list[dict[str, Any]] = []
    for report_path in sorted(EVIDENCE_DIR.glob("*_report.json")):
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        overall_pass = payload.get("overall_pass")
        if overall_pass is None:
            summary = payload.get("summary")
            if isinstance(summary, Mapping):
                overall_pass = summary.get("overall_pass")
        if overall_pass is None and isinstance(payload.get("status"), str):
            overall_pass = payload["status"] == "pass"
        reports.append(
            {
                "report_id": report_path.stem.removeprefix("phase_03_").removesuffix("_report"),
                "path": str(report_path),
                "overall_pass": bool(overall_pass),
            }
        )

    manifest = {
        "phase": PHASE_LABEL,
        "phase_remains_open": True,
        "reports": reports,
        "runtime_modules_available": runtime_modules_available(),
        "slice": SLICE_ID,
        "status": "slice_3_blocked" if not runtime_modules_available() else "slice_3_ready",
        "notes": [
            "evidence manifest is rebuilt from actual report files on disk",
            "slice 1 evidence remains present and real",
            "slice 2 evidence remains present and real",
            "slice 3 split/merge runtime is absent in this lane, so the slice remains blocked rather than faked",
        ],
    }
    dump_json(MANIFEST_PATH, manifest)
    return manifest


def build_blocked_report(missing: list[str]) -> dict[str, Any]:
    return {
        "phase": PHASE_LABEL,
        "slice": SLICE_ID,
        "verification": VERIFICATION_NAME,
        "status": "blocked",
        "runtime_modules_available": False,
        "supporting_modules_available": supporting_modules_available(),
        "runtime_imports": list(RUNTIME_IMPORTS),
        "supporting_imports": list(SUPPORTING_IMPORTS),
        "checked_files": [
            *PLAN_REFS,
            *SUPPORTING_EVIDENCE_REFS,
            *[rel(RUNTIME_DIR / filename) for filename in RUNTIME_FILES],
        ],
        "blocker": {
            "kind": "missing_runtime_dependencies",
            "message": "Phase 3 slice 3 split/merge runtime module is not on disk yet.",
            "missing_files": missing,
        },
        "planned_checks": [
            {
                "case_id": "split-happy-path-preserves-lineage",
                "target": "split_merge_rules",
                "expected_pass": True,
            },
            {
                "case_id": "split-missing-lineage-parent-fails",
                "target": "split_merge_rules",
                "expected_pass": False,
            },
            {
                "case_id": "split-role-family-tissue-mismatch-fails",
                "target": "split_merge_rules",
                "expected_pass": False,
            },
            {
                "case_id": "merge-happy-path-preserves-survivor-lineage",
                "target": "split_merge_rules",
                "expected_pass": True,
            },
            {
                "case_id": "merge-lineage-conflict-fails",
                "target": "split_merge_rules",
                "expected_pass": False,
            },
            {
                "case_id": "policy-bounds-breach-fails-closed",
                "target": "split_merge_rules",
                "expected_pass": False,
            },
            {
                "case_id": "conflict-aware-consolidation-remains-fail-closed",
                "target": "split_merge_rules",
                "expected_pass": False,
            },
        ],
        "summary": {
            "overall_pass": False,
            "planned_checks": 7,
            "blocked_checks": 7,
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "manifest": rel(MANIFEST_PATH),
        },
        "notes": [
            "no integrated split/merge success is claimed because the runtime file is absent",
            "the verifier stays repo-relative and does not rely on external PYTHONPATH wiring",
            "existing slice 1 and slice 2 evidence remains intact",
        ],
    }


def main() -> int:
    runtime_missing = missing_files([RUNTIME_DIR / filename for filename in RUNTIME_FILES])
    if runtime_missing:
        report = build_blocked_report(runtime_missing)
        dump_json(REPORT_PATH, report)
        refresh_evidence_manifest()
        print("phase_3 slice_3 split/merge verifier: BLOCKED")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1

    report = build_blocked_report(runtime_missing)
    dump_json(REPORT_PATH, report)
    refresh_evidence_manifest()
    print("phase_3 slice_3 split/merge verifier: BLOCKED")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
