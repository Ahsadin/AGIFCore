from __future__ import annotations

import json
import stat
from pathlib import Path
from typing import Any, Mapping

from .contracts import (
    INSTALLER_DISTRIBUTION_SCHEMA,
    MAX_INSTALLER_ARTIFACTS,
    stable_hash_payload,
)


def _write_text(path: Path, text: str, *, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if executable:
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _build_launcher_script(*, payload_expression: str) -> str:
    return "\n".join(
        [
            "#!/usr/bin/env sh",
            "set -eu",
            'SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)',
            'REPO_ROOT=$(cd "$SCRIPT_DIR/../../../../../.." && pwd)',
            'cd "$REPO_ROOT"',
            "python3 - <<'PY'",
            "from pathlib import Path",
            "import json",
            "import sys",
            "root = Path.cwd()",
            'sys.path.insert(0, str(root / "projects/agifcore_master/05_testing/phase_12_structural_growth"))',
            'sys.path.insert(0, str(root / "projects/agifcore_master/04_execution/phase_13_product_runtime_and_ux"))',
            "import _phase_12_verifier_common as p12c",
            "from agifcore_phase13_product_runtime import ProductRuntimeShell",
            'result = p12c.run_phase12_cycle(scenario="weak")',
            "shell = ProductRuntimeShell(",
            '    fixture=result["fixture"],',
            '    phase10_turn_state=result["phase10_turn"],',
            '    phase11_cycle_state=result["phase11_cycle"],',
            '    phase12_cycle_state=result["cycle"].to_dict(),',
            ")",
            f"payload = {payload_expression}",
            "print(json.dumps(payload, indent=2, sort_keys=True))",
            "PY",
            "",
        ]
    )


def build_installer_distribution_snapshot(
    *,
    session_open: Mapping[str, Any],
    policy_hash: str,
    shell_snapshot_hash: str,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    bundle_dir = output_dir / "local_distribution_bundle" if output_dir else None
    runner_script = _build_launcher_script(
        payload_expression='{"launcher": "local_runner", "session_id": shell.session_open()["session_id"], "support_state": shell.shell_snapshot()["support_state"]}'
    )
    gateway_script = _build_launcher_script(
        payload_expression='shell.api.conversation_turn(user_text="installer gateway smoke test")'
    )
    ui_script = _build_launcher_script(
        payload_expression='{"launcher": "desktop_ui", "view_count": shell.ui_snapshot()["view_count"], "selected_view": shell.ui_snapshot()["selected_view"]}'
    )
    install_local = "\n".join(
        [
            "# Phase 13 Local Distribution",
            "",
            "This bundle is local-review material only.",
            "",
            "## Included launchers",
            "",
            "- `launch_phase_13_local_runner.sh`",
            "- `launch_phase_13_local_gateway.sh`",
            "- `launch_phase_13_desktop_ui.sh`",
            "",
            "## Local install steps",
            "",
            "1. Keep the extracted review bundle folder intact so the relative launcher paths remain valid.",
            "2. Inspect `phase_13_integrity_manifest.json` before running any launcher.",
            "3. Run one launcher with `sh` locally and compare the printed identifiers to the manifest.",
            "",
            "## Scope stop",
            "",
            "- no public release behavior is included",
            "- no Phase 14 sandbox/profile/scale behavior is included",
        ]
    ) + "\n"
    integrity_payload = {
        "policy_hash": policy_hash,
        "session_id": session_open["session_id"],
        "shell_snapshot_hash": shell_snapshot_hash,
        "public_release_blocked": True,
        "artifact_hashes": {
            "launch_phase_13_local_runner.sh": stable_hash_payload(runner_script),
            "launch_phase_13_local_gateway.sh": stable_hash_payload(gateway_script),
            "launch_phase_13_local_desktop_ui.sh": stable_hash_payload(ui_script),
            "INSTALL_LOCAL.md": stable_hash_payload(install_local),
        },
    }
    integrity_payload["integrity_hash"] = stable_hash_payload(integrity_payload)
    bundle_manifest = {
        "bundle_name": f"agifcore_phase13_local_bundle_{session_open['session_id']}",
        "session_id": session_open["session_id"],
        "scope": "local_distribution_only",
        "runtime_entrypoint": "agifcore_phase13_product_runtime.product_runtime_shell.ProductRuntimeShell",
        "public_release_blocked": True,
        "artifacts": [
            "phase_13_bundle_manifest.json",
            "phase_13_integrity_manifest.json",
            "INSTALL_LOCAL.md",
            "launch_phase_13_local_runner.sh",
            "launch_phase_13_local_gateway.sh",
            "launch_phase_13_local_desktop_ui.sh",
        ],
    }
    artifacts = [
        {
            "artifact_id": "bundle_manifest",
            "filename": "phase_13_bundle_manifest.json",
            "purpose": "local distribution inventory",
            "executable": False,
        },
        {
            "artifact_id": "integrity_manifest",
            "filename": "phase_13_integrity_manifest.json",
            "purpose": "local integrity proof",
            "executable": False,
        },
        {
            "artifact_id": "install_local",
            "filename": "INSTALL_LOCAL.md",
            "purpose": "local install instructions",
            "executable": False,
        },
        {
            "artifact_id": "launcher_runner",
            "filename": "launch_phase_13_local_runner.sh",
            "purpose": "local runner launcher",
            "executable": True,
        },
        {
            "artifact_id": "launcher_gateway",
            "filename": "launch_phase_13_local_gateway.sh",
            "purpose": "local gateway launcher",
            "executable": True,
        },
        {
            "artifact_id": "launcher_desktop_ui",
            "filename": "launch_phase_13_local_desktop_ui.sh",
            "purpose": "local desktop UI launcher",
            "executable": True,
        },
    ]
    if len(artifacts) > MAX_INSTALLER_ARTIFACTS:
        raise ValueError("installer artifact count exceeds planning ceiling")
    if bundle_dir is not None:
        _write_text(bundle_dir / "phase_13_bundle_manifest.json", json.dumps(bundle_manifest, indent=2, sort_keys=True) + "\n")
        _write_text(bundle_dir / "phase_13_integrity_manifest.json", json.dumps(integrity_payload, indent=2, sort_keys=True) + "\n")
        _write_text(bundle_dir / "INSTALL_LOCAL.md", install_local)
        _write_text(bundle_dir / "launch_phase_13_local_runner.sh", runner_script, executable=True)
        _write_text(bundle_dir / "launch_phase_13_local_gateway.sh", gateway_script, executable=True)
        _write_text(bundle_dir / "launch_phase_13_local_desktop_ui.sh", ui_script, executable=True)
    payload = {
        "schema": INSTALLER_DISTRIBUTION_SCHEMA,
        "session_id": session_open["session_id"],
        "shell_snapshot_hash": shell_snapshot_hash,
        "artifact_count": len(artifacts),
        "artifacts": [
            {
                **item,
                "path": str(bundle_dir / item["filename"]) if bundle_dir is not None else item["filename"],
            }
            for item in artifacts
        ],
        "integrity_manifest": integrity_payload,
        "bundle_manifest": bundle_manifest,
        "local_install_steps": [
            "inspect the integrity manifest",
            "run one local launcher",
            "compare the printed ids to the bundle manifest",
        ],
        "public_release_blocked": True,
    }
    return {
        **payload,
        "snapshot_hash": stable_hash_payload(payload),
    }
