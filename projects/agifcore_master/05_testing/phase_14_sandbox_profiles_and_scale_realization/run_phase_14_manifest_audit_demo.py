from __future__ import annotations

import json

import _phase_14_verifier_common as vc


def build_demo_payload() -> dict[str, object]:
    result = vc.run_phase14_shell(scenario="weak")
    shell = result["shell"]
    manifest_audit = shell.manifest_audit()
    manifest_differentiation = vc.build_manifest_differentiation_summary(shell=shell, profile="laptop")
    cell_manifest = shell.cell_manifest()
    tissue_manifest = shell.tissue_manifest()
    profile_manifests = shell.profile_manifests()
    laptop_budget = shell.active_cell_budget(profile="laptop")
    mobile_proof = shell.dormant_cell_survival(profile="mobile")
    laptop_proof = shell.dormant_cell_survival(profile="laptop")
    builder_proof = shell.dormant_cell_survival(profile="builder")
    return {
        "phase": "14",
        "demo_id": "manifest_audit",
        "status": "open",
        "manifest_audit": manifest_audit,
        "manifest_differentiation": manifest_differentiation,
        "cell_manifest_hash": cell_manifest["manifest_hash"],
        "tissue_manifest_hash": tissue_manifest["manifest_hash"],
        "profile_manifest_hash": profile_manifests["manifest_hash"],
        "laptop_budget": laptop_budget,
        "mobile_proof": mobile_proof,
        "laptop_proof": laptop_proof,
        "builder_proof": builder_proof,
        "evidence_reports": [
            vc.rel(vc.EVIDENCE_DIR / "phase_14_cell_manifest_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_tissue_manifest_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_profile_manifest_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_manifest_differentiation_report.json"),
            vc.rel(vc.EVIDENCE_DIR / "phase_14_dormant_survival_report.json"),
            vc.rel(vc.MANIFEST_PATH),
        ],
        "notes": [
            "review-only manifest audit demo",
            "Phase 14 remains open",
            "no approval implied",
        ],
    }


def build_markdown(payload: dict[str, object]) -> list[str]:
    audit = payload["manifest_audit"]
    differentiation = payload["manifest_differentiation"]
    budget = payload["laptop_budget"]
    return [
        "# Phase 14 Demo: Manifest Audit",
        "",
        "Phase 14 remains `open`. This demo is inspectable review material only.",
        "",
        "## Manifest Audit Snapshot",
        "",
        f"- logical cell count: `{audit['logical_cell_count']}`",
        f"- tissue count: `{audit['tissue_count']}`",
        f"- profile count: `{audit['profile_count']}`",
        f"- audit status: `{audit['audit_status']}`",
        f"- family signatures: `{differentiation['family_signature_count']}`",
        f"- tissue signatures: `{differentiation['tissue_signature_count']}`",
        "",
        "## Manifest Hashes",
        "",
        f"- cell manifest hash: `{payload['cell_manifest_hash']}`",
        f"- tissue manifest hash: `{payload['tissue_manifest_hash']}`",
        f"- profile manifest hash: `{payload['profile_manifest_hash']}`",
        "",
        "## Constraint Diversity",
        "",
        f"- allowed profile patterns: `{differentiation['constraint_diversity']['allowed_profile_pattern_count']}`",
        f"- activation budget classes: `{differentiation['constraint_diversity']['activation_budget_class_count']}`",
        f"- export visibility classes: `{differentiation['constraint_diversity']['export_visibility_class_count']}`",
        f"- dormancy behavior classes: `{differentiation['constraint_diversity']['dormancy_behavior_class_count']}`",
        f"- continuity requirement classes: `{differentiation['constraint_diversity']['continuity_requirement_class_count']}`",
        f"- evidence requirement classes: `{differentiation['constraint_diversity']['evidence_requirement_class_count']}`",
        "",
        "## Laptop Budget Trace",
        "",
        f"- selected cells: `{budget['selected_active_cell_count']}`",
        f"- selected tissues: `{budget['selected_active_tissue_count']}`",
        f"- budget state: `{budget['budget_state']}`",
        f"- activation priority span: `{budget['selected_activation_priority_min']}` to `{budget['selected_activation_priority_max']}`",
        "",
        "## Dormant Survival Proofs",
        "",
        f"- mobile cases: `{payload['mobile_proof']['case_count']}`",
        f"- laptop cases: `{payload['laptop_proof']['case_count']}`",
        f"- builder cases: `{payload['builder_proof']['case_count']}`",
        "",
        "## Evidence Links",
        "",
        *[f"- `{path}`" for path in payload["evidence_reports"]],
        "",
        "## Truth Note",
        "",
        "- literal manifests, differentiation metrics, and dormant proofs stay evidence-linked and inspectable",
        "- no approval or phase completion is implied",
    ]


def main() -> int:
    payload = build_demo_payload()
    vc.write_demo_payload(filename="phase_14_manifest_audit_demo.json", payload=payload)
    vc.write_demo_markdown(
        filename="phase_14_manifest_audit_demo.md",
        lines=build_markdown(payload),
    )
    vc.build_demo_index()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
