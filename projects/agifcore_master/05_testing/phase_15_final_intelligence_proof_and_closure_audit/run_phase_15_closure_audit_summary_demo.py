from __future__ import annotations

import json

import _phase_15_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    closure_audit_path = vc.EVIDENCE_DIR / "phase_15_closure_audit_report.json"
    if not closure_audit_path.exists():
        raise RuntimeError("closure audit report is required before building the closure-audit summary demo")
    closure_audit = vc.load_json(closure_audit_path)
    return {
        "phase": "15",
        "demo_id": "closure_audit_summary",
        "status": "open",
        "closure_audit": closure_audit,
        "review_surface_paths": closure_audit["anchors"]["closure_audit"]["review_surface_paths"],
        "evidence_reports": [
            vc.rel(closure_audit_path),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only closure-audit summary demo",
            "Phase 15 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    audit = payload["closure_audit"]["anchors"]["closure_audit"]
    return [
        "# Phase 15 Demo: Closure Audit Summary",
        "",
        "Phase 15 remains `open`. This demo is inspectable review material only.",
        "",
        "## Closure Audit Summary",
        "",
        f"- gate status: `{audit['gate_status']}`",
        f"- finding count: `{audit['finding_count']}`",
        f"- review surface count: `{len(audit['review_surface_paths'])}`",
        f"- phase15 truth: `{audit['phase15_status']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- closure audit readiness is separate from user approval",
        "- no approval or phase completion is implied",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_15_closure_audit_summary_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_15_closure_audit_summary_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
