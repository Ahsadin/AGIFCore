from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .blind_packs import build_blind_pack_catalog
from .closure_audit import build_closure_audit
from .contracts import FINAL_PROOF_RUNTIME_SCHEMA, deep_copy_jsonable, stable_hash_payload
from .hardening_package import run_hardening_package
from .hidden_packs import build_hidden_pack_catalog
from .live_demo_pack import build_live_demo_pack
from .reproducibility_package import build_reproducibility_package
from .soak_harness import build_soak_harness_contract, run_soak_harness


class Phase15ProofRuntimeShell:
    def __init__(self, *, phase13_shell: Any, phase14_shell: Any) -> None:
        self.phase13_shell = phase13_shell
        self.phase14_shell = phase14_shell

    def runtime_snapshot(self) -> dict[str, object]:
        blind = self.blind_packs()
        hidden = self.hidden_packs()
        live_demo = self.live_demo_pack()
        soak = self.soak_contract()
        payload = {
            "schema": FINAL_PROOF_RUNTIME_SCHEMA,
            "phase13_shell_hash": self.phase13_shell.shell_snapshot()["snapshot_hash"],
            "phase14_shell_hash": self.phase14_shell.shell_snapshot()["snapshot_hash"],
            "blind_pack_count": blind["blind_pack_count"],
            "hidden_pack_count": hidden["hidden_pack_count"],
            "live_demo_pack_count": live_demo["live_demo_pack_count"],
            "soak_duration_class_count": soak["duration_class_count"],
            "phase16_blocked": True,
        }
        return {**payload, "snapshot_hash": stable_hash_payload(payload)}

    def blind_packs(self) -> dict[str, object]:
        return build_blind_pack_catalog(
            phase13_shell_snapshot=self.phase13_shell.shell_snapshot(),
            phase14_shell_snapshot=self.phase14_shell.shell_snapshot(),
        )

    def hidden_packs(self) -> dict[str, object]:
        return build_hidden_pack_catalog(
            phase13_shell_snapshot=self.phase13_shell.shell_snapshot(),
            phase14_shell_snapshot=self.phase14_shell.shell_snapshot(),
        )

    def live_demo_pack(self) -> dict[str, object]:
        return build_live_demo_pack(
            phase13_shell_snapshot=self.phase13_shell.shell_snapshot(),
            phase14_shell_snapshot=self.phase14_shell.shell_snapshot(),
        )

    def soak_contract(self) -> dict[str, object]:
        return build_soak_harness_contract(
            phase13_shell_snapshot=self.phase13_shell.shell_snapshot(),
            phase14_shell_snapshot=self.phase14_shell.shell_snapshot(),
        )

    def run_soak(self) -> dict[str, object]:
        return run_soak_harness(proof_shells={"weak": self, "contradiction": self})

    def run_hardening(self, *, repo_root: Path, phase15_output_root: Path) -> dict[str, object]:
        return run_hardening_package(
            proof_shells={"weak": self, "contradiction": self},
            repo_root=repo_root,
            phase15_output_root=phase15_output_root,
        )

    def reproducibility_package(
        self,
        *,
        repo_root: Path,
        report_paths: Mapping[str, Path],
        demo_paths: Mapping[str, Path],
        evidence_manifest_path: Path,
    ) -> dict[str, object]:
        return build_reproducibility_package(
            repo_root=repo_root,
            report_paths=report_paths,
            demo_paths=demo_paths,
            evidence_manifest_path=evidence_manifest_path,
        )

    def closure_audit(
        self,
        *,
        phase13_manifest: Mapping[str, Any],
        phase14_manifest: Mapping[str, Any],
        phase15_manifest: Mapping[str, Any],
        phase_index_text: str,
        phase_gate_text: str,
        review_surface_paths: list[str],
    ) -> dict[str, object]:
        return build_closure_audit(
            phase13_manifest=phase13_manifest,
            phase14_manifest=phase14_manifest,
            phase15_manifest=phase15_manifest,
            phase_index_text=phase_index_text,
            phase_gate_text=phase_gate_text,
            review_surface_paths=review_surface_paths,
        )

    def clone_snapshot(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        return deep_copy_jsonable(payload)


Phase15ProofShell = Phase15ProofRuntimeShell

