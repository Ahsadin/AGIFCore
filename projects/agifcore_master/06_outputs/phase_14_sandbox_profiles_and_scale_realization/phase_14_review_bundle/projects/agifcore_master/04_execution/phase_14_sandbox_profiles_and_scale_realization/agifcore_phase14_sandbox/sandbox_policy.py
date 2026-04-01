from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Mapping

from .contracts import (
    DEFAULT_POLICY_BY_PROFILE,
    MAX_SANDBOX_POLICY_COUNT,
    PACKAGE_MANIFEST_SCHEMA,
    POLICY_CLASS_IDS,
    POLICY_IDS,
    PROFILE_NAMES,
    SANDBOX_EXECUTION_RECEIPT_SCHEMA,
    SANDBOX_POLICY_SCHEMA,
    WASM_FALLBACK_CODES,
    bounded_unique,
    require_mapping,
    require_non_empty_str,
    require_profile_name,
    stable_hash_payload,
    utc_timestamp,
)
from .wasmtime_fuel_limits import select_fuel_class
from .wasmtime_memory_limits import select_memory_class
from .wasmtime_wall_time_limits import select_wall_time_class


def locate_wasmtime_cli() -> str | None:
    return shutil.which("wasmtime")


def build_sandbox_policies() -> dict[str, object]:
    policies: list[dict[str, object]] = []
    policy_descriptions = {
        "mobile_constrained_policy": "mobile fail-closed constrained package execution",
        "laptop_default_policy": "reference laptop package execution",
        "builder_diagnostic_policy": "builder diagnostics without correctness privilege",
        "strict_fail_closed_policy": "strict deny-first sandbox envelope",
    }
    allowed_profiles = {
        "mobile_constrained_policy": ("mobile",),
        "laptop_default_policy": ("laptop",),
        "builder_diagnostic_policy": ("builder",),
        "strict_fail_closed_policy": PROFILE_NAMES,
    }
    for policy_id in POLICY_IDS:
        payload = {
            "schema": SANDBOX_POLICY_SCHEMA,
            "policy_id": policy_id,
            "description": policy_descriptions[policy_id],
            "allowed_profiles": list(allowed_profiles[policy_id]),
            "fuel_class_id": POLICY_CLASS_IDS[policy_id],
            "memory_class_id": POLICY_CLASS_IDS[policy_id],
            "wall_time_class_id": POLICY_CLASS_IDS[policy_id],
            "bundle_integrity_required": True,
            "sandbox_process_model": "dedicated_wasmtime_subprocess",
            "phase15_blocked": True,
            "phase16_blocked": True,
        }
        policies.append({**payload, "policy_hash": stable_hash_payload(payload)})
    if len(policies) > MAX_SANDBOX_POLICY_COUNT:
        raise ValueError("sandbox policy count exceeds planning ceiling")
    catalog = {
        "schema": SANDBOX_POLICY_SCHEMA,
        "policy_count": len(policies),
        "reason_codes": list(WASM_FALLBACK_CODES),
        "policies": policies,
    }
    return {**catalog, "catalog_hash": stable_hash_payload(catalog)}


def select_sandbox_policy(*, policy_id: str) -> dict[str, object]:
    resolved_id = require_non_empty_str(policy_id, "policy_id")
    for policy in build_sandbox_policies()["policies"]:
        if policy["policy_id"] == resolved_id:
            return dict(policy)
    raise ValueError(f"unknown sandbox policy: {resolved_id}")


def _default_module_text() -> str:
    return "\n".join(
        [
            "(module",
            "  (memory (export \"memory\") 1)",
            "  (func (export \"add\") (param i32 i32) (result i32)",
            "    local.get 0",
            "    local.get 1",
            "    i32.add)",
            "  (func (export \"spin\")",
            "    (loop br 0))",
            "  (func (export \"grow_to_pages\") (param i32) (result i32)",
            "    local.get 0",
            "    memory.grow)",
            ")",
            "",
        ]
    )


def _module_text_for_variant(variant: str) -> str:
    clean_variant = require_non_empty_str(variant, "variant")
    if clean_variant in {"valid", "tampered"}:
        return _default_module_text()
    if clean_variant == "invalid":
        return "(module (func (export \"broken\") local.get 0)\n"
    raise ValueError(f"unsupported wasm package variant: {clean_variant}")


def build_sample_wasm_package(
    *,
    profile: str,
    output_dir: Path | None = None,
    variant: str = "valid",
    allowed_profiles: tuple[str, ...] | None = None,
) -> dict[str, object]:
    resolved_profile = require_profile_name(profile, "profile")
    resolved_variant = require_non_empty_str(variant, "variant")
    module_text = _module_text_for_variant(resolved_variant)
    package_root = output_dir or Path(tempfile.mkdtemp(prefix="agifcore_phase14_wasm_"))
    package_dir = package_root / "sandbox_packages"
    package_dir.mkdir(parents=True, exist_ok=True)
    module_path = package_dir / f"phase14_{resolved_profile}_{resolved_variant}_sample_module.wat"
    module_path.write_text(module_text, encoding="utf-8")
    actual_module_hash = stable_hash_payload(module_text)
    exported_functions = ("add", "spin", "grow_to_pages") if resolved_variant != "invalid" else ("broken",)
    package_allowed_profiles = bounded_unique(
        list(allowed_profiles or PROFILE_NAMES),
        ceiling=len(PROFILE_NAMES),
        field_name="allowed_profiles",
    )
    integrity_payload = {
        "profile_hint": resolved_profile,
        "variant": resolved_variant,
        "module_hash": actual_module_hash,
        "exported_functions": list(exported_functions),
        "allowed_profiles": list(package_allowed_profiles),
    }
    recorded_module_hash = (
        stable_hash_payload({"tampered": actual_module_hash})
        if resolved_variant == "tampered"
        else actual_module_hash
    )
    recorded_integrity_hash = (
        stable_hash_payload({"tampered": integrity_payload})
        if resolved_variant == "tampered"
        else stable_hash_payload(integrity_payload)
    )
    payload = {
        "schema": PACKAGE_MANIFEST_SCHEMA,
        "package_id": f"phase14_wasm_package::{resolved_profile}::{resolved_variant}",
        "profile_hint": resolved_profile,
        "variant": resolved_variant,
        "module_format": "wat_text",
        "module_path": str(module_path),
        "module_hash": recorded_module_hash,
        "integrity_hash": recorded_integrity_hash,
        "allowed_profiles": list(package_allowed_profiles),
        "exported_functions": list(exported_functions),
        "sandbox_backend": "wasmtime_cli",
        "phase15_blocked": True,
        "phase16_blocked": True,
    }
    return {**payload, "package_hash": stable_hash_payload(payload)}


def _classify_failure(stderr_text: str) -> str:
    lower = stderr_text.lower()
    if "all fuel consumed" in lower:
        return "FUEL_LIMIT_EXCEEDED"
    if "forcing trap when growing memory" in lower or "memory.grow" in lower:
        return "MEMORY_LIMIT_EXCEEDED"
    if "wasm trap: interrupt" in lower or "timed out" in lower:
        return "WALL_TIMEOUT_EXCEEDED"
    if "failed to parse webassembly module" in lower or "expected `" in lower or "unknown operator" in lower:
        return "INVALID_WASM_MODULE"
    return "INVALID_WASM_MODULE"


def execute_sandbox_request(
    *,
    profile: str,
    policy_id: str | None,
    package: Mapping[str, Any],
    function_name: str,
    function_args: list[Any] | tuple[Any, ...] | None = None,
) -> dict[str, object]:
    resolved_profile = require_profile_name(profile, "profile")
    chosen_policy_id = policy_id or DEFAULT_POLICY_BY_PROFILE[resolved_profile]
    policy = select_sandbox_policy(policy_id=chosen_policy_id)
    package_map = require_mapping(package, "package")
    function = require_non_empty_str(function_name, "function_name")
    args = [str(item) for item in (function_args or [])]
    wasmtime_path = locate_wasmtime_cli()
    actual_module_hash = ""
    module_path = Path(str(package_map["module_path"]))
    if module_path.exists():
        actual_module_hash = stable_hash_payload(module_path.read_text(encoding="utf-8"))
    integrity_payload = {
        "profile_hint": package_map.get("profile_hint"),
        "variant": package_map.get("variant"),
        "module_hash": actual_module_hash,
        "exported_functions": list(package_map.get("exported_functions", [])),
        "allowed_profiles": list(package_map.get("allowed_profiles", [])),
    }
    integrity_verified = (
        actual_module_hash == package_map.get("module_hash")
        and stable_hash_payload(integrity_payload) == package_map.get("integrity_hash")
    )
    profile_allowed = resolved_profile in set(package_map.get("allowed_profiles", []))
    policy_allows_profile = resolved_profile in set(policy["allowed_profiles"])
    fuel_class = select_fuel_class(policy_id=chosen_policy_id)
    memory_class = select_memory_class(policy_id=chosen_policy_id)
    wall_time_class = select_wall_time_class(policy_id=chosen_policy_id)
    base_payload = {
        "schema": SANDBOX_EXECUTION_RECEIPT_SCHEMA,
        "profile": resolved_profile,
        "policy_id": chosen_policy_id,
        "package_id": package_map.get("package_id"),
        "function_name": function,
        "function_args": args,
        "sandbox_backend": "wasmtime_cli" if wasmtime_path else "unavailable",
        "wasmtime_cli_path": wasmtime_path,
        "sandboxed_execution": True,
        "bundle_integrity_verified": integrity_verified,
        "profile_allowed": profile_allowed and policy_allows_profile,
        "fuel_limit": fuel_class["fuel_limit"],
        "memory_limit_mb": memory_class["memory_limit_mb"],
        "memory_limit_bytes": int(memory_class["memory_limit_mb"]) * 1024 * 1024,
        "wall_time_limit_ms": wall_time_class["wall_time_ms"],
        "executed_at": utc_timestamp(),
        "phase15_blocked": True,
        "phase16_blocked": True,
        "command": [],
        "stdout": "",
        "stderr": "",
        "exit_code": None,
    }
    if not wasmtime_path:
        payload = {
            **base_payload,
            "status": "blocked",
            "reason_code": "WASMTIME_UNAVAILABLE",
            "admitted": False,
        }
        return {**payload, "receipt_hash": stable_hash_payload(payload)}
    if not integrity_verified:
        payload = {
            **base_payload,
            "status": "blocked",
            "reason_code": "BUNDLE_INTEGRITY_REQUIRED",
            "admitted": False,
        }
        return {**payload, "receipt_hash": stable_hash_payload(payload)}
    if not (profile_allowed and policy_allows_profile):
        payload = {
            **base_payload,
            "status": "blocked",
            "reason_code": "PROFILE_NOT_ALLOWED",
            "admitted": False,
        }
        return {**payload, "receipt_hash": stable_hash_payload(payload)}
    if function not in set(package_map.get("exported_functions", [])):
        payload = {
            **base_payload,
            "status": "blocked",
            "reason_code": "INVALID_WASM_MODULE",
            "admitted": False,
        }
        return {**payload, "receipt_hash": stable_hash_payload(payload)}

    command = [
        wasmtime_path,
        "run",
        "-W",
        f"fuel={fuel_class['fuel_limit']}",
        "-W",
        f"max-memory-size={int(memory_class['memory_limit_mb']) * 1024 * 1024}",
        "-W",
        f"timeout={wall_time_class['wall_time_ms']}ms",
        "-W",
        "trap-on-grow-failure=y",
        "--invoke",
        function,
        str(module_path),
        *args,
    ]
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            cwd=str(module_path.parent),
            timeout=max(5.0, (wall_time_class["wall_time_ms"] / 1000.0) + 2.0),
        )
        stderr_text = completed.stderr.strip()
        stdout_text = completed.stdout.strip()
        if completed.returncode == 0:
            payload = {
                **base_payload,
                "status": "pass",
                "reason_code": "none",
                "admitted": True,
                "command": command,
                "stdout": stdout_text,
                "stderr": stderr_text,
                "exit_code": completed.returncode,
            }
        else:
            payload = {
                **base_payload,
                "status": "blocked",
                "reason_code": _classify_failure(stderr_text),
                "admitted": True,
                "command": command,
                "stdout": stdout_text,
                "stderr": stderr_text,
                "exit_code": completed.returncode,
            }
    except subprocess.TimeoutExpired as exc:
        payload = {
            **base_payload,
            "status": "blocked",
            "reason_code": "WALL_TIMEOUT_EXCEEDED",
            "admitted": True,
            "command": command,
            "stdout": (exc.stdout or "").strip(),
            "stderr": (exc.stderr or "").strip(),
            "exit_code": None,
        }
    return {**payload, "receipt_hash": stable_hash_payload(payload)}
