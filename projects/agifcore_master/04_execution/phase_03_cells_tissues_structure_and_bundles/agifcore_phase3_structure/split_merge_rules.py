from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from cell_contracts import (
    Phase3StructureError,
    require_mapping,
    require_non_empty_str,
    require_unique_string_list,
)
from tissue_manifests import SPLIT_PRESSURE_MEMBER_COUNT
from trust_bands import TrustBand

MERGE_ALLOWED_STATES = frozenset({"active", "dormant"})
SPLIT_ALLOWED_PARENT_STATE = "active"
MIN_SPLIT_CHILD_COUNT = 2
MAX_SPLIT_CHILD_COUNT = SPLIT_PRESSURE_MEMBER_COUNT


def require_non_negative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int):
        raise Phase3StructureError(f"{field_name} must be an int")
    if value < 0:
        raise Phase3StructureError(f"{field_name} must be >= 0")
    return value


def normalize_child_spec(payload: Mapping[str, Any]) -> dict[str, Any]:
    child_payload = dict(payload)
    return {
        "cell_id": require_non_empty_str(child_payload.get("cell_id"), "child cell_id"),
        "role_family": require_non_empty_str(
            child_payload.get("role_family"), "child role_family"
        ),
        "policy_envelope": require_mapping(
            child_payload.get("policy_envelope", {}), "child policy_envelope"
        ),
    }


def normalize_split_child_specs(child_specs: Any) -> list[dict[str, Any]]:
    if not isinstance(child_specs, list):
        raise Phase3StructureError("child_specs must be a list")
    normalized_children = [normalize_child_spec(item) for item in child_specs]
    if len(normalized_children) < MIN_SPLIT_CHILD_COUNT:
        raise Phase3StructureError("split requires at least two child specs")
    if len(normalized_children) > MAX_SPLIT_CHILD_COUNT:
        raise Phase3StructureError("split child count exceeds phase-3 ceiling")
    child_ids = [item["cell_id"] for item in normalized_children]
    require_unique_string_list(child_ids, "child cell ids")
    return normalized_children


def normalize_merge_state(state: Any, field_name: str = "lifecycle_state") -> str:
    normalized = require_non_empty_str(state, field_name)
    if normalized not in MERGE_ALLOWED_STATES:
        raise Phase3StructureError(
            f"{field_name} must be one of {sorted(MERGE_ALLOWED_STATES)}"
        )
    return normalized


def normalize_split_state(state: Any, field_name: str = "lifecycle_state") -> str:
    normalized = require_non_empty_str(state, field_name)
    if normalized != SPLIT_ALLOWED_PARENT_STATE:
        raise Phase3StructureError("split requires parent lifecycle_state=active")
    return normalized


@dataclass(frozen=True, slots=True)
class SplitProposal:
    proposal_id: str
    parent_cell_id: str
    lineage_id: str
    child_specs: list[dict[str, Any]]
    reason: str
    actor: str
    policy_envelope: dict[str, Any]

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "SplitProposal":
        normalized = dict(payload)
        return cls(
            proposal_id=require_non_empty_str(normalized.get("proposal_id"), "proposal_id"),
            parent_cell_id=require_non_empty_str(
                normalized.get("parent_cell_id"), "parent_cell_id"
            ),
            lineage_id=require_non_empty_str(normalized.get("lineage_id"), "lineage_id"),
            child_specs=normalize_split_child_specs(normalized.get("child_specs")),
            reason=require_non_empty_str(normalized.get("reason"), "reason"),
            actor=require_non_empty_str(normalized.get("actor", "kernel"), "actor"),
            policy_envelope=require_mapping(
                normalized.get("policy_envelope", {}), "policy_envelope"
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "parent_cell_id": self.parent_cell_id,
            "lineage_id": self.lineage_id,
            "child_specs": [dict(item) for item in self.child_specs],
            "reason": self.reason,
            "actor": self.actor,
            "policy_envelope": dict(self.policy_envelope),
        }


@dataclass(frozen=True, slots=True)
class MergeProposal:
    proposal_id: str
    survivor_cell_id: str
    merged_cell_id: str
    lineage_id: str
    reason: str
    actor: str
    policy_envelope: dict[str, Any]

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MergeProposal":
        normalized = dict(payload)
        return cls(
            proposal_id=require_non_empty_str(normalized.get("proposal_id"), "proposal_id"),
            survivor_cell_id=require_non_empty_str(
                normalized.get("survivor_cell_id"), "survivor_cell_id"
            ),
            merged_cell_id=require_non_empty_str(
                normalized.get("merged_cell_id"), "merged_cell_id"
            ),
            lineage_id=require_non_empty_str(normalized.get("lineage_id"), "lineage_id"),
            reason=require_non_empty_str(normalized.get("reason"), "reason"),
            actor=require_non_empty_str(normalized.get("actor", "kernel"), "actor"),
            policy_envelope=require_mapping(
                normalized.get("policy_envelope", {}), "policy_envelope"
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "survivor_cell_id": self.survivor_cell_id,
            "merged_cell_id": self.merged_cell_id,
            "lineage_id": self.lineage_id,
            "reason": self.reason,
            "actor": self.actor,
            "policy_envelope": dict(self.policy_envelope),
        }


def _trust_band_name(trust_band: TrustBand | str | None) -> str:
    if trust_band is None:
        return "untrusted"
    if isinstance(trust_band, TrustBand):
        return trust_band.band_name
    return require_non_empty_str(trust_band, "trust_band")


def _enforce_split_merge_trust(trust_band: TrustBand | str | None) -> str | None:
    if trust_band is None:
        return "split/merge requires explicit trust band"
    if not isinstance(trust_band, TrustBand):
        return "split/merge requires a TrustBand instance"
    if not trust_band.allow_split_merge:
        return f"trust band {trust_band.band_name} blocks split/merge"
    if trust_band.require_manual_review:
        return f"trust band {trust_band.band_name} requires manual review"
    return None


def _lineage_from_record(record: Mapping[str, Any], field_name: str) -> str:
    return require_non_empty_str(record.get("lineage_id"), field_name)


def _role_family_from_record(record: Mapping[str, Any], field_name: str) -> str:
    return require_non_empty_str(record.get("role_family"), field_name)


def _decision_payload(
    *,
    allowed: bool,
    action: str,
    reason: str,
    proposal_id: str,
    lineage_id: str,
    trust_band: TrustBand | str | None,
    lifecycle_input: Mapping[str, Any] | None = None,
    lineage_ledger_entry: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "allowed": allowed,
        "action": action,
        "reason": reason,
        "proposal_id": proposal_id,
        "lineage_id": lineage_id,
        "trust_band": _trust_band_name(trust_band),
        "lifecycle_input": dict(lifecycle_input or {}),
        "lineage_ledger_entry": dict(lineage_ledger_entry or {}),
    }
    return payload


def evaluate_split_proposal(
    *,
    proposal: SplitProposal,
    parent_record: Mapping[str, Any],
    trust_band: TrustBand | str | None,
    tissue_member_count_before_split: int | None = None,
) -> dict[str, Any]:
    normalized_parent = dict(parent_record)
    if proposal.parent_cell_id != require_non_empty_str(
        normalized_parent.get("cell_id"), "parent_record.cell_id"
    ):
        return _decision_payload(
            allowed=False,
            action="split",
            reason="proposal parent_cell_id does not match parent record",
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    try:
        normalize_split_state(
            normalized_parent.get("lifecycle_state"), "parent_record.lifecycle_state"
        )
    except Phase3StructureError as exc:
        return _decision_payload(
            allowed=False,
            action="split",
            reason=str(exc),
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    if proposal.lineage_id != _lineage_from_record(
        normalized_parent, "parent_record.lineage_id"
    ):
        return _decision_payload(
            allowed=False,
            action="split",
            reason="proposal lineage_id does not match parent lineage_id",
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    trust_failure = _enforce_split_merge_trust(trust_band)
    if trust_failure is not None:
        return _decision_payload(
            allowed=False,
            action="split",
            reason=trust_failure,
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    if tissue_member_count_before_split is not None:
        member_count = require_non_negative_int(
            tissue_member_count_before_split, "tissue_member_count_before_split"
        )
        if member_count > SPLIT_PRESSURE_MEMBER_COUNT:
            return _decision_payload(
                allowed=False,
                action="split",
                reason="split pressure threshold exceeded; manual review required",
                proposal_id=proposal.proposal_id,
                lineage_id=proposal.lineage_id,
                trust_band=trust_band,
            )
    parent_role_family = _role_family_from_record(
        normalized_parent, "parent_record.role_family"
    )
    for child_spec in proposal.child_specs:
        if child_spec["role_family"] != parent_role_family:
            return _decision_payload(
                allowed=False,
                action="split",
                reason="child role_family must match parent role_family",
                proposal_id=proposal.proposal_id,
                lineage_id=proposal.lineage_id,
                trust_band=trust_band,
            )
    lifecycle_input = {
        "parent_cell_id": proposal.parent_cell_id,
        "child_specs": [
            {"cell_id": item["cell_id"], "role_family": item["role_family"]}
            for item in proposal.child_specs
        ],
        "reason": proposal.reason,
        "actor": proposal.actor,
    }
    lineage_ledger_entry = {
        "operation": "split",
        "proposal_id": proposal.proposal_id,
        "lineage_id": proposal.lineage_id,
        "parent_cell_id": proposal.parent_cell_id,
        "child_cell_ids": [item["cell_id"] for item in proposal.child_specs],
        "reason": proposal.reason,
        "actor": proposal.actor,
    }
    return _decision_payload(
        allowed=True,
        action="split",
        reason="split proposal is structurally valid and lineage-aware",
        proposal_id=proposal.proposal_id,
        lineage_id=proposal.lineage_id,
        trust_band=trust_band,
        lifecycle_input=lifecycle_input,
        lineage_ledger_entry=lineage_ledger_entry,
    )


def evaluate_merge_proposal(
    *,
    proposal: MergeProposal,
    survivor_record: Mapping[str, Any],
    merged_record: Mapping[str, Any],
    trust_band: TrustBand | str | None,
) -> dict[str, Any]:
    normalized_survivor = dict(survivor_record)
    normalized_merged = dict(merged_record)
    if proposal.survivor_cell_id != require_non_empty_str(
        normalized_survivor.get("cell_id"), "survivor_record.cell_id"
    ):
        return _decision_payload(
            allowed=False,
            action="merge",
            reason="proposal survivor_cell_id does not match survivor record",
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    if proposal.merged_cell_id != require_non_empty_str(
        normalized_merged.get("cell_id"), "merged_record.cell_id"
    ):
        return _decision_payload(
            allowed=False,
            action="merge",
            reason="proposal merged_cell_id does not match merged record",
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    if proposal.survivor_cell_id == proposal.merged_cell_id:
        return _decision_payload(
            allowed=False,
            action="merge",
            reason="survivor and merged cell ids must be different",
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    try:
        normalize_merge_state(
            normalized_survivor.get("lifecycle_state"), "survivor_record.lifecycle_state"
        )
        normalize_merge_state(
            normalized_merged.get("lifecycle_state"), "merged_record.lifecycle_state"
        )
    except Phase3StructureError as exc:
        return _decision_payload(
            allowed=False,
            action="merge",
            reason=str(exc),
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    if proposal.lineage_id != _lineage_from_record(
        normalized_survivor, "survivor_record.lineage_id"
    ) or proposal.lineage_id != _lineage_from_record(
        normalized_merged, "merged_record.lineage_id"
    ):
        return _decision_payload(
            allowed=False,
            action="merge",
            reason="proposal lineage_id must match both survivor and merged lineage_id",
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    if _role_family_from_record(
        normalized_survivor, "survivor_record.role_family"
    ) != _role_family_from_record(normalized_merged, "merged_record.role_family"):
        return _decision_payload(
            allowed=False,
            action="merge",
            reason="merge requires matching role_family",
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    trust_failure = _enforce_split_merge_trust(trust_band)
    if trust_failure is not None:
        return _decision_payload(
            allowed=False,
            action="merge",
            reason=trust_failure,
            proposal_id=proposal.proposal_id,
            lineage_id=proposal.lineage_id,
            trust_band=trust_band,
        )
    lifecycle_input = {
        "survivor_cell_id": proposal.survivor_cell_id,
        "merged_cell_id": proposal.merged_cell_id,
        "reason": proposal.reason,
        "actor": proposal.actor,
    }
    lineage_ledger_entry = {
        "operation": "merge",
        "proposal_id": proposal.proposal_id,
        "lineage_id": proposal.lineage_id,
        "survivor_cell_id": proposal.survivor_cell_id,
        "retired_cell_id": proposal.merged_cell_id,
        "reason": proposal.reason,
        "actor": proposal.actor,
    }
    return _decision_payload(
        allowed=True,
        action="merge",
        reason="merge proposal is structurally valid and lineage-aware",
        proposal_id=proposal.proposal_id,
        lineage_id=proposal.lineage_id,
        trust_band=trust_band,
        lifecycle_input=lifecycle_input,
        lineage_ledger_entry=lineage_ledger_entry,
    )

