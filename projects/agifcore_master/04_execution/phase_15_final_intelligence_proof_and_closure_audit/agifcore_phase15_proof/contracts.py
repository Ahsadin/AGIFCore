from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping


class Phase15ProofError(ValueError):
    """Raised when the Phase 15 proof and closure contract is violated."""


FINAL_PROOF_RUNTIME_SCHEMA = "agifcore.phase_15.final_proof_runtime.v1"
BLIND_PACK_SCHEMA = "agifcore.phase_15.blind_pack.v1"
HIDDEN_PACK_SCHEMA = "agifcore.phase_15.hidden_pack.v1"
LIVE_DEMO_PACK_SCHEMA = "agifcore.phase_15.live_demo_pack.v1"
REAL_DESKTOP_CHAT_DEMO_SCHEMA = "agifcore.phase_15.real_desktop_chat_demo.v1"
SOAK_HARNESS_SCHEMA = "agifcore.phase_15.soak_harness.v1"
HARDENING_PACKAGE_SCHEMA = "agifcore.phase_15.hardening_package.v1"
REPRODUCIBILITY_PACKAGE_SCHEMA = "agifcore.phase_15.reproducibility_package.v1"
CLOSURE_AUDIT_SCHEMA = "agifcore.phase_15.closure_audit.v1"

MAX_BLIND_PACK_COUNT = 6
MAX_HIDDEN_PACK_COUNT = 3
MAX_LIVE_DEMO_PACK_COUNT = 1
MAX_SOAK_DURATION_CLASSES = 3
MAX_HARDENING_ISSUE_FAMILY_COUNT = 12
MAX_REPRODUCIBILITY_ARTIFACT_COUNT = 16
MAX_CLOSURE_AUDIT_FINDINGS = 8
MAX_PHASE15_BUNDLE_BYTES = 512 * 1024 * 1024

FORBIDDEN_PHASE16_KEYWORDS = (
    "release note",
    "public evidence index",
    "github release",
    "public release",
    "tag/release",
    "paper",
    "publication",
    "public reproducibility",
)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_hash_payload(payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return sha256(encoded).hexdigest()


def canonical_size_bytes(payload: Mapping[str, Any] | list[Any] | tuple[Any, ...] | str) -> int:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, default=str).encode("utf-8")
    return len(encoded)


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require_non_empty_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Phase15ProofError(f"{field_name} must be a non-empty string")
    return value.strip()


def require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise Phase15ProofError(f"{field_name} must be a mapping")
    return dict(value)


def bounded_unique(
    values: list[str] | tuple[str, ...],
    *,
    ceiling: int,
    field_name: str,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    result: list[str] = []
    seen: set[str] = set()
    for raw in values:
        cleaned = " ".join(str(raw).split()).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
        if len(result) >= ceiling:
            break
    if not result and not allow_empty:
        raise Phase15ProofError(f"{field_name} must include at least one value")
    return tuple(result)


def deep_copy_jsonable(value: Any) -> Any:
    return deepcopy(value)
