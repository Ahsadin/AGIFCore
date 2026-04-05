from __future__ import annotations

import argparse
import json
import re
import subprocess
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_DIR = REPO_ROOT / "projects/agifcore_master/06_outputs/final_publication"
REPORT_PATH = OUTPUT_DIR / "publication_safety_report.json"
SUMMARY_PATH = OUTPUT_DIR / "publication_safety_summary.md"
REDACTION_MANIFEST_PATH = OUTPUT_DIR / "public_path_redaction_manifest.json"

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".py",
    ".sh",
    ".csv",
    ".tsv",
    ".log",
}
ZIP_SUFFIXES = {".zip"}

FINDINGS = {
    "absolute_local_path": re.compile(r"/Users/[A-Za-z0-9._-]+/[^\s`\"']+"),
    "local_install_path": re.compile(r"(?:~/(?:\.wasmtime|\.codex|\.cargo)[^\s`\"']*|/(?:opt/homebrew|usr/local|private/var|var/run/com\.apple)[^\s`\"']*)"),
    "local_email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "private_hostname": re.compile(r"\b(?:[A-Za-z0-9-]+\.)+(?:local|lan|home|internal)\b"),
    "phone_number": re.compile(
        r"(?:\+\d[\d .()-]{7,}\d|\(\d{3}\)\s*\d{3}[-.\s]?\d{4}\b|\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b)"
    ),
    "token_like": re.compile(
        r"(ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|"
        r"(?:(?:api[_-]?key|token|password|secret)\s*[:=]\s*[\"']?[A-Za-z0-9._/-]{8,}))",
        re.IGNORECASE,
    ),
}

SAFE_PRIVATE_HOSTNAMES = {
    "region.provenance.local",
    "region.local",
    "phase8.local",
}

NON_PUBLIC_PREFIXES = (
    ".codex/",
    "projects/agifcore_master/00_admin/codex_threads/",
    "projects/agifcore_master/08_logs/",
)
PUBLIC_SAFE_PREFIXES = (
    "README.md",
    "CLAIM_BOUNDARY.md",
    "ARCHITECTURE.md",
    "RESULTS.md",
    "REPRODUCIBILITY.md",
    "NEXT_STEPS.md",
    "paper/",
    "archive/",
    "projects/agifcore_master/06_outputs/final_publication/",
)


@dataclass
class Finding:
    path: str
    line_number: int | None
    kind: str
    match: str
    treatment: str
    reason: str
    source: str


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def visible_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [REPO_ROOT / line for line in result.stdout.splitlines() if line.strip()]


def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def is_zip_candidate(path: Path) -> bool:
    return path.suffix.lower() in ZIP_SUFFIXES


def classify_treatment(rel_path: str, kind: str) -> tuple[str, str]:
    if rel_path.startswith(NON_PUBLIC_PREFIXES):
        return (
            "move_to_local_nonpublic_archive",
            "Raw internal or machine-specific material is safer outside the public branch.",
        )
    if rel_path.startswith(PUBLIC_SAFE_PREFIXES):
        return (
            "redact_for_public_branch",
            "Public-facing material should keep the same meaning but remove local details.",
        )
    if kind == "token_like":
        return (
            "move_to_local_nonpublic_archive",
            "Credential-like strings should not stay on the public branch.",
        )
    return (
        "redact_for_public_branch",
        "The file can stay public after local or personal traces are removed.",
    )


def decode_text(payload: bytes) -> str | None:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None


def scan_text(rel_path: str, text: str, source: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for kind, pattern in FINDINGS.items():
            for match in pattern.finditer(line):
                if kind == "private_hostname" and match.group(0) in SAFE_PRIVATE_HOSTNAMES:
                    continue
                treatment, reason = classify_treatment(rel_path, kind)
                findings.append(
                    Finding(
                        path=rel_path,
                        line_number=line_number,
                        kind=kind,
                        match=match.group(0),
                        treatment=treatment,
                        reason=reason,
                        source=source,
                    )
                )
    return findings


def scan_zip(path: Path) -> list[Finding]:
    rel_path = repo_relative(path)
    findings: list[Finding] = []
    try:
        with zipfile.ZipFile(path) as bundle:
            for name in bundle.namelist():
                suffix = Path(name).suffix.lower()
                if suffix not in TEXT_SUFFIXES:
                    continue
                payload = decode_text(bundle.read(name))
                if payload is None:
                    continue
                findings.extend(scan_text(rel_path, payload, f"zip:{name}"))
    except zipfile.BadZipFile:
        treatment, reason = classify_treatment(rel_path, "token_like")
        findings.append(
            Finding(
                path=rel_path,
                line_number=None,
                kind="zip_read_error",
                match="zip file could not be inspected",
                treatment=treatment,
                reason=f"{reason} Zip file inspection failed.",
                source="zip",
            )
        )
    return findings


def scan_paths(paths: Iterable[Path]) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    scanned: list[str] = []
    for path in paths:
        if not path.exists() or path.is_symlink():
            continue
        rel_path = repo_relative(path)
        if is_text_candidate(path):
            scanned.append(rel_path)
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                text = path.read_text(encoding="latin-1")
            findings.extend(scan_text(rel_path, text, "file"))
            continue
        if is_zip_candidate(path):
            scanned.append(rel_path)
            findings.extend(scan_zip(path))
    return findings, scanned


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def write_summary(report: dict[str, object]) -> None:
    lines = [
        "# Publication Safety Summary",
        "",
        f"- scanned files: `{report['scanned_file_count']}`",
        f"- flagged files: `{report['flagged_file_count']}`",
        f"- total findings: `{report['finding_count']}`",
        "",
        "## Findings By Kind",
        "",
    ]
    by_kind = report["counts_by_kind"]
    if by_kind:
        for kind, count in by_kind.items():
            lines.append(f"- `{kind}`: `{count}`")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Findings By Treatment",
            "",
        ]
    )
    by_treatment = report["counts_by_treatment"]
    if by_treatment:
        for treatment, count in by_treatment.items():
            lines.append(f"- `{treatment}`: `{count}`")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Highest-Risk Files",
            "",
        ]
    )
    highest_risk = report["highest_risk_files"]
    if highest_risk:
        for item in highest_risk:
            lines.append(
                f"- `{item['path']}`: `{item['finding_count']}` findings, "
                f"primary treatment `{item['primary_treatment']}`"
            )
    else:
        lines.append("- none")
    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_redaction_manifest(findings: list[Finding]) -> dict[str, object]:
    file_map: dict[str, dict[str, object]] = {}
    for finding in findings:
        entry = file_map.setdefault(
            finding.path,
            {
                "path": finding.path,
                "treatments": [],
                "kinds": [],
                "sources": [],
                "recommended_public_action": finding.treatment,
            },
        )
        if finding.treatment not in entry["treatments"]:
            entry["treatments"].append(finding.treatment)
        if finding.kind not in entry["kinds"]:
            entry["kinds"].append(finding.kind)
        if finding.source not in entry["sources"]:
            entry["sources"].append(finding.source)
        if finding.treatment == "move_to_local_nonpublic_archive":
            entry["recommended_public_action"] = "move_to_local_nonpublic_archive"
    return {
        "generated_on": "2026-04-05",
        "repo_root": ".",
        "files": sorted(file_map.values(), key=lambda item: item["path"]),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan tracked and publication-candidate files for public publication risks."
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Limit the scan to one or more repo-relative paths.",
    )
    return parser.parse_args()


def resolve_scan_roots(args: argparse.Namespace) -> list[Path]:
    if not args.path:
        return visible_files()
    explicit: list[Path] = []
    for raw in args.path:
        target = REPO_ROOT / raw
        if target.is_dir():
            explicit.extend(sorted(p for p in target.rglob("*") if p.is_file()))
        elif target.is_file():
            explicit.append(target)
    return explicit


def main() -> int:
    args = parse_args()
    scan_targets = resolve_scan_roots(args)
    findings, scanned = scan_paths(scan_targets)
    counts_by_kind = Counter(item.kind for item in findings)
    counts_by_treatment = Counter(item.treatment for item in findings)
    findings_by_file = Counter(item.path for item in findings)
    highest_risk_files = []
    for path, count in findings_by_file.most_common(25):
        file_findings = [item for item in findings if item.path == path]
        treatment_counts = Counter(item.treatment for item in file_findings)
        highest_risk_files.append(
            {
                "path": path,
                "finding_count": count,
                "primary_treatment": treatment_counts.most_common(1)[0][0],
                "kinds": sorted({item.kind for item in file_findings}),
            }
        )
    report = {
        "schema": "agifcore.final_publication.publication_safety_report.v1",
        "generated_on": "2026-04-05",
        "scan_root": ".",
        "scanned_file_count": len(scanned),
        "flagged_file_count": len(findings_by_file),
        "finding_count": len(findings),
        "counts_by_kind": dict(sorted(counts_by_kind.items())),
        "counts_by_treatment": dict(sorted(counts_by_treatment.items())),
        "highest_risk_files": highest_risk_files,
        "findings": [
            {
                "path": item.path,
                "line_number": item.line_number,
                "kind": item.kind,
                "match": item.match,
                "treatment": item.treatment,
                "reason": item.reason,
                "source": item.source,
            }
            for item in findings
        ],
    }
    write_json(REPORT_PATH, report)
    write_summary(report)
    write_json(REDACTION_MANIFEST_PATH, build_redaction_manifest(findings))
    print(f"Scanned {len(scanned)} files; found {len(findings)} findings across {len(findings_by_file)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
