from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .provenance_links import require_mapping, require_non_empty_str, utc_timestamp

MAX_SUPERSESSION_CHAIN = 4


class SupersessionRulesError(ValueError):
    """Raised when supersession chains become cyclic or exceed bounded length."""


@dataclass(slots=True)
class SupersessionRecord:
    entity_kind: str
    predecessor_id: str
    successor_id: str
    review_ref: str
    reason: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_kind": self.entity_kind,
            "predecessor_id": self.predecessor_id,
            "successor_id": self.successor_id,
            "review_ref": self.review_ref,
            "reason": self.reason,
            "created_at": self.created_at,
        }


class SupersessionLedger:
    """Bounded supersession ledger with replayable predecessor visibility."""

    def __init__(self, *, max_chain_length: int = MAX_SUPERSESSION_CHAIN) -> None:
        self.max_chain_length = max_chain_length
        self._records: list[SupersessionRecord] = []
        self._successor_by_predecessor: dict[str, str] = {}
        self._record_by_predecessor: dict[str, SupersessionRecord] = {}

    def register(
        self,
        *,
        entity_kind: str,
        predecessor_id: str,
        successor_id: str,
        review_ref: str,
        reason: str = "superseded",
    ) -> SupersessionRecord:
        normalized_predecessor = require_non_empty_str(predecessor_id, "predecessor_id")
        normalized_successor = require_non_empty_str(successor_id, "successor_id")
        if normalized_predecessor == normalized_successor:
            raise SupersessionRulesError("predecessor_id and successor_id must differ")
        if normalized_predecessor in self._successor_by_predecessor:
            raise SupersessionRulesError("predecessor already has a recorded successor")
        if self.active_id(normalized_successor) == normalized_predecessor:
            raise SupersessionRulesError("supersession cycle detected")

        record = SupersessionRecord(
            entity_kind=require_non_empty_str(entity_kind, "entity_kind"),
            predecessor_id=normalized_predecessor,
            successor_id=normalized_successor,
            review_ref=require_non_empty_str(review_ref, "review_ref"),
            reason=require_non_empty_str(reason, "reason"),
            created_at=utc_timestamp(),
        )
        self._records.append(record)
        self._successor_by_predecessor[record.predecessor_id] = record.successor_id
        self._record_by_predecessor[record.predecessor_id] = record
        if self._max_chain_hops() > self.max_chain_length:
            self._records.pop()
            self._successor_by_predecessor.pop(record.predecessor_id, None)
            self._record_by_predecessor.pop(record.predecessor_id, None)
            raise SupersessionRulesError("supersession chain exceeds Phase 5 bounded depth")
        return record

    def is_superseded(self, entity_id: str) -> bool:
        return require_non_empty_str(entity_id, "entity_id") in self._successor_by_predecessor

    def successor_of(self, entity_id: str) -> str | None:
        return self._successor_by_predecessor.get(require_non_empty_str(entity_id, "entity_id"))

    def active_id(self, entity_id: str) -> str:
        current = require_non_empty_str(entity_id, "entity_id")
        seen: set[str] = set()
        while current in self._successor_by_predecessor:
            if current in seen:
                raise SupersessionRulesError("supersession cycle detected during resolution")
            seen.add(current)
            current = self._successor_by_predecessor[current]
        return current

    def predecessor_chain(self, entity_id: str) -> list[str]:
        current = require_non_empty_str(entity_id, "entity_id")
        chain = [current]
        while current in self._successor_by_predecessor:
            current = self._successor_by_predecessor[current]
            chain.append(current)
            if len(chain) - 1 > self.max_chain_length:
                break
        return chain

    def _chain_hops(self, entity_id: str) -> int:
        return len(self.predecessor_chain(entity_id)) - 1

    def _max_chain_hops(self) -> int:
        if not self._successor_by_predecessor:
            return 0
        return max(self._chain_hops(entity_id) for entity_id in self._successor_by_predecessor)

    def export_state(self) -> dict[str, Any]:
        return {
            "schema": "agifcore.phase_05.supersession_rules.v1",
            "max_chain_length": self.max_chain_length,
            "records": [record.to_dict() for record in self._records],
        }

    def load_state(self, payload: Mapping[str, Any]) -> None:
        payload_map = require_mapping(payload, "supersession_state")
        if payload_map.get("schema") != "agifcore.phase_05.supersession_rules.v1":
            raise SupersessionRulesError("supersession rules schema mismatch")
        max_chain_length = payload_map.get("max_chain_length", self.max_chain_length)
        if not isinstance(max_chain_length, int) or max_chain_length <= 0:
            raise SupersessionRulesError("max_chain_length must be a positive integer")
        self.max_chain_length = max_chain_length
        self._records = []
        self._successor_by_predecessor = {}
        self._record_by_predecessor = {}
        records = payload_map.get("records", [])
        if not isinstance(records, list):
            raise SupersessionRulesError("records must be a list")
        for record_payload in records:
            record_map = require_mapping(record_payload, "record")
            record = self.register(
                entity_kind=record_map.get("entity_kind"),
                predecessor_id=record_map.get("predecessor_id"),
                successor_id=record_map.get("successor_id"),
                review_ref=record_map.get("review_ref"),
                reason=record_map.get("reason", "superseded"),
            )
            record.created_at = require_non_empty_str(record_map.get("created_at"), "created_at")
