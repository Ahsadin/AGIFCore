from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from .active_cell_budget import build_active_cell_budget
from .cell_manifest import build_cell_manifest
from .contracts import (
    MANIFEST_AUDIT_SCHEMA,
    PROFILE_NAMES,
    SANDBOX_PROFILE_RUNTIME_SCHEMA,
    deep_copy_jsonable,
    require_mapping,
    stable_hash_payload,
)
from .dormant_cell_survival import build_dormant_survival_proof
from .profile_manifests import build_all_profile_manifests
from .sandbox_policy import (
    build_sample_wasm_package,
    build_sandbox_policies,
    execute_sandbox_request,
    locate_wasmtime_cli,
)
from .tissue_manifest import build_tissue_manifest
from .wasmtime_fuel_limits import build_wasmtime_fuel_limits
from .wasmtime_memory_limits import build_wasmtime_memory_limits
from .wasmtime_wall_time_limits import build_wasmtime_wall_time_limits


class SandboxProfileRuntimeShell:
    def __init__(
        self,
        *,
        phase13_session_open: Mapping[str, Any],
        phase13_shell_snapshot: Mapping[str, Any],
        phase13_state_export: Mapping[str, Any],
        phase13_memory_review_export: Mapping[str, Any],
        phase13_safe_shutdown: Mapping[str, Any],
    ) -> None:
        self._phase13_session_open = require_mapping(phase13_session_open, "phase13_session_open")
        self._phase13_shell_snapshot = require_mapping(
            phase13_shell_snapshot, "phase13_shell_snapshot"
        )
        self._phase13_state_export = require_mapping(phase13_state_export, "phase13_state_export")
        self._phase13_memory_review_export = require_mapping(
            phase13_memory_review_export, "phase13_memory_review_export"
        )
        self._phase13_safe_shutdown = require_mapping(
            phase13_safe_shutdown, "phase13_safe_shutdown"
        )
        self._fuel_limits = build_wasmtime_fuel_limits()
        self._memory_limits = build_wasmtime_memory_limits()
        self._wall_time_limits = build_wasmtime_wall_time_limits()
        self._cell_manifest = build_cell_manifest()
        self._tissue_manifest = build_tissue_manifest(cell_manifest=self._cell_manifest)
        self._profile_manifests = build_all_profile_manifests(
            phase13_session_open=self._phase13_session_open,
            phase13_shell_snapshot=self._phase13_shell_snapshot,
        )
        self._sandbox_policies = build_sandbox_policies()
        self._wasmtime_path = locate_wasmtime_cli()

    def wasmtime_fuel_limits(self) -> dict[str, object]:
        return deep_copy_jsonable(self._fuel_limits)

    def wasmtime_memory_limits(self) -> dict[str, object]:
        return deep_copy_jsonable(self._memory_limits)

    def wasmtime_wall_time_limits(self) -> dict[str, object]:
        return deep_copy_jsonable(self._wall_time_limits)

    def cell_manifest(self) -> dict[str, object]:
        return deep_copy_jsonable(self._cell_manifest)

    def tissue_manifest(self) -> dict[str, object]:
        return deep_copy_jsonable(self._tissue_manifest)

    def profile_manifests(self) -> dict[str, object]:
        return deep_copy_jsonable(self._profile_manifests)

    def sandbox_policies(self) -> dict[str, object]:
        return deep_copy_jsonable(self._sandbox_policies)

    def sample_wasm_package(
        self,
        *,
        profile: str,
        output_dir: Path | None = None,
        variant: str = "valid",
        allowed_profiles: tuple[str, ...] | None = None,
    ) -> dict[str, object]:
        return build_sample_wasm_package(
            profile=profile,
            output_dir=output_dir,
            variant=variant,
            allowed_profiles=allowed_profiles,
        )

    def sandbox_execute(
        self,
        *,
        profile: str,
        function_name: str,
        function_args: list[Any] | tuple[Any, ...] | None = None,
        output_dir: Path | None = None,
        variant: str = "valid",
        policy_id: str | None = None,
        allowed_profiles: tuple[str, ...] | None = None,
    ) -> dict[str, object]:
        package = self.sample_wasm_package(
            profile=profile,
            output_dir=output_dir,
            variant=variant,
            allowed_profiles=allowed_profiles,
        )
        return execute_sandbox_request(
            profile=profile,
            policy_id=policy_id,
            package=package,
            function_name=function_name,
            function_args=function_args,
        )

    def _profile_manifest_by_name(self, profile: str) -> dict[str, object]:
        for manifest in self._profile_manifests["profiles"]:
            if manifest["profile"] == profile:
                return dict(manifest)
        raise ValueError(f"missing profile manifest: {profile}")

    def active_cell_budget(
        self,
        *,
        profile: str,
        requested_active_cells: int | None = None,
        requested_active_tissues: int | None = None,
        requested_cell_ids: list[str] | tuple[str, ...] | None = None,
        current_active_cells: int | None = None,
        current_active_tissues: int | None = None,
    ) -> dict[str, object]:
        return build_active_cell_budget(
            profile=profile,
            cell_manifest=self._cell_manifest,
            tissue_manifest=self._tissue_manifest,
            profile_manifest=self._profile_manifest_by_name(profile),
            requested_active_cells=requested_active_cells,
            requested_active_tissues=requested_active_tissues,
            requested_cell_ids=requested_cell_ids,
            current_active_cells=current_active_cells,
            current_active_tissues=current_active_tissues,
        )

    def dormant_cell_survival(
        self,
        *,
        profile: str,
        requested_active_cells: int | None = None,
    ) -> dict[str, object]:
        budget = self.active_cell_budget(
            profile=profile,
            requested_active_cells=requested_active_cells,
        )
        return build_dormant_survival_proof(
            profile=profile,
            cell_manifest=self._cell_manifest,
            active_budget=budget,
            phase13_state_export=self._phase13_state_export,
            phase13_memory_review_export=self._phase13_memory_review_export,
            phase13_safe_shutdown=self._phase13_safe_shutdown,
        )

    def manifest_audit(self) -> dict[str, object]:
        profile_manifests = list(self._profile_manifests["profiles"])
        contract_hashes = sorted({str(item["same_contract_hash"]) for item in profile_manifests})
        cell_manifest = dict(self._cell_manifest)
        tissue_manifest = dict(self._tissue_manifest)
        per_profile_total_active_cap = dict(
            tissue_manifest.get(
                "per_profile_total_active_cap",
                {"mobile": 0, "laptop": 0, "builder": 0},
            )
        )
        metrics = {
            "family_count": int(cell_manifest.get("family_count", 0)),
            "contract_variant_count": int(cell_manifest.get("contract_variant_count", 0)),
            "exemplar_class_count": len(cell_manifest.get("exemplar_class_ids", [])),
            "allowed_profile_pattern_count": int(cell_manifest.get("allowed_profile_pattern_count", 0)),
            "activation_budget_class_count": int(cell_manifest.get("activation_budget_class_count", 0)),
            "dormancy_behavior_class_count": int(cell_manifest.get("dormancy_behavior_class_count", 0)),
            "continuity_requirement_class_count": int(
                cell_manifest.get("continuity_requirement_class_count", 0)
            ),
            "evidence_requirement_class_count": int(
                cell_manifest.get("evidence_requirement_class_count", 0)
            ),
            "operation_set_signature_count": int(
                cell_manifest.get("operation_set_signature_count", 0)
            ),
            "tissue_variant_count": int(tissue_manifest.get("tissue_variant_count", 0)),
            "continuity_handling_class_count": len(
                tissue_manifest.get("continuity_handling_class_counts", {})
            ),
            "escalation_handling_class_count": len(
                tissue_manifest.get("escalation_handling_class_counts", {})
            ),
        }
        checks = [
            {
                "id": "same-contract-hash-single",
                "passed": len(contract_hashes) == 1,
                "expected": "exactly 1 same contract hash",
                "observed": len(contract_hashes),
            },
            {
                "id": "literal-cell-count",
                "passed": int(cell_manifest.get("cell_count", 0)) == 1024,
                "expected": 1024,
                "observed": int(cell_manifest.get("cell_count", 0)),
            },
            {
                "id": "literal-tissue-count",
                "passed": int(tissue_manifest.get("tissue_count", 0)) == 32,
                "expected": 32,
                "observed": int(tissue_manifest.get("tissue_count", 0)),
            },
            {
                "id": "family-differentiation-present",
                "passed": (
                    metrics["family_count"] == 16
                    and metrics["activation_budget_class_count"] >= 4
                    and metrics["evidence_requirement_class_count"] >= 4
                ),
                "expected": "16 families with >=4 activation classes and >=4 evidence classes",
                "observed": {
                    "family_count": metrics["family_count"],
                    "activation_budget_class_count": metrics["activation_budget_class_count"],
                    "evidence_requirement_class_count": metrics["evidence_requirement_class_count"],
                },
            },
            {
                "id": "tissue-specialization-present",
                "passed": (
                    metrics["tissue_variant_count"] >= 2
                    and metrics["continuity_handling_class_count"] >= 2
                    and metrics["escalation_handling_class_count"] >= 2
                ),
                "expected": ">=2 tissue variants with >=2 continuity and >=2 escalation handling classes",
                "observed": {
                    "tissue_variant_count": metrics["tissue_variant_count"],
                    "continuity_handling_class_count": metrics["continuity_handling_class_count"],
                    "escalation_handling_class_count": metrics["escalation_handling_class_count"],
                },
            },
            {
                "id": "constraint-diversity-present",
                "passed": (
                    metrics["allowed_profile_pattern_count"] >= 3
                    and metrics["dormancy_behavior_class_count"] >= 3
                    and metrics["continuity_requirement_class_count"] >= 3
                ),
                "expected": ">=3 profile patterns, >=3 dormancy classes, >=3 continuity classes",
                "observed": {
                    "allowed_profile_pattern_count": metrics["allowed_profile_pattern_count"],
                    "dormancy_behavior_class_count": metrics["dormancy_behavior_class_count"],
                    "continuity_requirement_class_count": metrics["continuity_requirement_class_count"],
                },
            },
            {
                "id": "exemplar-layer-present",
                "passed": (
                    metrics["exemplar_class_count"] >= 8
                    and metrics["contract_variant_count"] >= 24
                    and metrics["operation_set_signature_count"] >= 8
                ),
                "expected": ">=8 exemplar classes, >=24 contract variants, >=8 operation signatures",
                "observed": {
                    "exemplar_class_count": metrics["exemplar_class_count"],
                    "contract_variant_count": metrics["contract_variant_count"],
                    "operation_set_signature_count": metrics["operation_set_signature_count"],
                },
            },
            {
                "id": "profile-cap-ordering-valid",
                "passed": (
                    int(per_profile_total_active_cap.get("mobile", 0))
                    < int(per_profile_total_active_cap.get("laptop", 0))
                    < int(per_profile_total_active_cap.get("builder", 0))
                ),
                "expected": "mobile < laptop < builder active-cap totals",
                "observed": {
                    "mobile": int(per_profile_total_active_cap.get("mobile", 0)),
                    "laptop": int(per_profile_total_active_cap.get("laptop", 0)),
                    "builder": int(per_profile_total_active_cap.get("builder", 0)),
                },
            },
        ]
        blocked_reason_codes = [str(item["id"]) for item in checks if not bool(item["passed"])]
        audit_status = "pass" if not blocked_reason_codes else "blocked"
        payload = {
            "schema": MANIFEST_AUDIT_SCHEMA,
            "cell_manifest_hash": self._cell_manifest["manifest_hash"],
            "tissue_manifest_hash": self._tissue_manifest["manifest_hash"],
            "profile_manifest_hash": self._profile_manifests["manifest_hash"],
            "logical_cell_count": self._cell_manifest["cell_count"],
            "tissue_count": self._tissue_manifest["tissue_count"],
            "profile_count": self._profile_manifests["manifest_count"],
            "same_contract_hash_count": len(contract_hashes),
            "same_contract_hashes": contract_hashes,
            "differentiation_metrics": metrics,
            "per_profile_total_active_cap": per_profile_total_active_cap,
            "audit_checks": checks,
            "blocked_reason_codes": blocked_reason_codes,
            "audit_status": audit_status,
        }
        return {**payload, "audit_hash": stable_hash_payload(payload)}

    def shell_snapshot(self) -> dict[str, object]:
        payload = {
            "schema": SANDBOX_PROFILE_RUNTIME_SCHEMA,
            "phase13_session_id": self._phase13_session_open["session_id"],
            "phase13_shell_hash": self._phase13_shell_snapshot["snapshot_hash"],
            "phase13_state_export_hash": self._phase13_state_export["snapshot_hash"],
            "phase13_memory_review_export_hash": self._phase13_memory_review_export["snapshot_hash"],
            "phase13_safe_shutdown_hash": self._phase13_safe_shutdown["receipt_hash"],
            "public_surfaces": list(self._phase13_session_open["available_surfaces"]),
            "blocked_surface_names": [
                item["surface_name"] for item in self._phase13_session_open["blocked_surfaces"]
            ],
            "profile_manifest_count": self._profile_manifests["manifest_count"],
            "cell_count": self._cell_manifest["cell_count"],
            "tissue_count": self._tissue_manifest["tissue_count"],
            "sandbox_policy_count": self._sandbox_policies["policy_count"],
            "wasmtime_available": bool(self._wasmtime_path),
            "wasmtime_cli_path": self._wasmtime_path,
            "phase15_blocked": True,
            "phase16_blocked": True,
        }
        return {**payload, "snapshot_hash": stable_hash_payload(payload)}


SandboxProfileShell = SandboxProfileRuntimeShell
