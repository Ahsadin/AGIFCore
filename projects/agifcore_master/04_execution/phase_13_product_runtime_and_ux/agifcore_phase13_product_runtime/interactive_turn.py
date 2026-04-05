from __future__ import annotations

import ast
import json
import operator
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping
from zoneinfo import ZoneInfo

from .contracts import INTERACTIVE_TURN_SCHEMA, bounded_unique, stable_hash_payload


def _find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / "projects" / "agifcore_master" / "PROJECT_README.md").exists():
            return candidate
    raise RuntimeError("unable to locate repo root for interactive turn engine")


REPO_ROOT = _find_repo_root()
PROJECT_ROOT = REPO_ROOT / "projects" / "agifcore_master"
PHASE15_TURN_EVIDENCE_SCHEMA = "agifcore.phase_15.interactive_turn_evidence.v1"
PHASE15_TURN_EVIDENCE_DIR = (
    PROJECT_ROOT
    / "06_outputs"
    / "phase_15_final_intelligence_proof_and_closure_audit"
    / "phase_15_evidence"
    / "interactive_turn_records"
)


def _ensure_phase_import_paths() -> None:
    runtime_paths = (
        PROJECT_ROOT / "04_execution" / "phase_02_fabric_kernel_and_workspace" / "agifcore_phase2_kernel",
        PROJECT_ROOT / "04_execution" / "phase_04_memory_planes",
        PROJECT_ROOT / "04_execution" / "phase_05_graph_and_knowledge_structures",
        PROJECT_ROOT / "04_execution" / "phase_06_world_model_and_simulator",
        PROJECT_ROOT / "04_execution" / "phase_07_conversation_core",
        PROJECT_ROOT / "04_execution" / "phase_08_science_and_world_awareness",
        PROJECT_ROOT / "04_execution" / "phase_09_rich_expression_and_composition",
        PROJECT_ROOT / "04_execution" / "phase_10_meta_cognition_and_critique",
        PROJECT_ROOT / "04_execution" / "phase_14_sandbox_profiles_and_scale_realization",
    )
    for runtime_path in runtime_paths:
        runtime_str = str(runtime_path)
        if runtime_str not in sys.path:
            sys.path.insert(0, runtime_str)


_ensure_phase_import_paths()

from event_bus import EventBus
from event_types import (  # type: ignore[import-not-found]
    AbstainOrAnswer as P2AbstainOrAnswer,
    DiscourseMode as P2DiscourseMode,
    FinalAnswerMode as P2FinalAnswerMode,
    KernelEventType,
    KernelResponseSurface,
    KernelTraceRefs,
    KernelTurnContext,
    KnowledgeGapReason as P2KnowledgeGapReason,
    NextAction as P2NextAction,
    SupportState as P2SupportState,
    new_kernel_event,
)
from replay_ledger import ReplayLedger  # type: ignore[import-not-found]
from workspace_state import SharedWorkspaceState  # type: ignore[import-not-found]

from agifcore_phase4_memory.continuity_memory import ContinuityMemoryStore
from agifcore_phase4_memory.memory_review import MemoryReviewQueue
from agifcore_phase4_memory.procedural_memory import ProceduralMemoryStore
from agifcore_phase4_memory.semantic_memory import SemanticMemoryStore
from agifcore_phase4_memory.working_memory import WorkingMemoryStore
from agifcore_phase5_graph.concept_graph import ConceptGraphStore
from agifcore_phase5_graph.descriptor_graph import DescriptorGraphStore
from agifcore_phase5_graph.skill_graph import SkillGraphStore
from agifcore_phase5_graph.support_selection import SupportSelectionEngine
from agifcore_phase5_graph.transfer_graph import TransferGraphStore
from agifcore_phase6_world_simulator.candidate_futures import CandidateFuturePlanner
from agifcore_phase6_world_simulator.conflict_lanes import ConflictLaneEngine
from agifcore_phase6_world_simulator.fault_lanes import FaultLaneEngine
from agifcore_phase6_world_simulator.instrumentation import InstrumentationEngine
from agifcore_phase6_world_simulator.overload_lanes import OverloadLaneEngine
from agifcore_phase6_world_simulator.pressure_lanes import PressureLaneEngine
from agifcore_phase6_world_simulator.target_domains import build_default_registry
from agifcore_phase6_world_simulator.usefulness_scoring import UsefulnessScoringEngine
from agifcore_phase6_world_simulator.what_if_simulation import WhatIfSimulationEngine
from agifcore_phase6_world_simulator.world_model import WorldModelBuilder
from agifcore_phase7_conversation.anti_generic_filler import AntiGenericFillerError
from agifcore_phase7_conversation.contracts import (
    FinalAnswerMode as P7FinalAnswerMode,
    ResponseSurface as P7ResponseSurface,
)
from agifcore_phase7_conversation.conversation_turn import ConversationTurnEngine
from agifcore_phase8_science_world_awareness.science_world_turn import ScienceWorldTurnEngine
from agifcore_phase9_rich_expression.rich_expression_turn import RichExpressionTurnEngine
from agifcore_phase10_meta_cognition.meta_cognition_turn import MetaCognitionTurnEngine
from agifcore_phase14_sandbox.sandbox_profile_shell import SandboxProfileRuntimeShell

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "be",
    "can",
    "do",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "the",
    "this",
    "to",
    "what",
    "who",
    "why",
    "you",
    "your",
}

TOKEN_ALIASES = {
    "u": "you",
    "ur": "your",
    "yu": "you",
    "ya": "you",
}

PROJECT_TOKENS = {
    "agif",
    "agifcore",
    "project",
    "phase",
    "plan",
    "runtime",
    "shell",
    "capability",
    "capabilities",
    "system",
    "status",
    "manifest",
    "evidence",
    "report",
    "decision",
    "changelog",
    "review",
    "bundle",
    "trace",
    "memory",
    "closure",
    "audit",
    "reproducibility",
    "blind",
    "hidden",
    "soak",
    "hardening",
}

SELF_TOKENS = {
    "you",
    "your",
    "runtime",
    "shell",
    "session",
    "system",
    "surface",
    "surfaces",
    "route",
    "routes",
    "view",
    "views",
    "status",
    "available",
}

PHASE_TOKENS = {
    "phase",
    "approved",
    "open",
    "complete",
    "completed",
    "status",
    "statuses",
    "gate",
    "index",
}

EVIDENCE_TOKENS = {
    "manifest",
    "evidence",
    "report",
    "reports",
    "audit",
    "closure",
    "reproducibility",
    "bundle",
    "review",
    "decision",
    "decisions",
    "changelog",
    "latest",
    "recent",
    "cell",
    "tissue",
    "profile",
}

CONTRADICTION_TOKENS = {
    "contradiction",
    "contradict",
    "conflict",
    "conflicting",
    "inconsistent",
    "inconsistency",
    "mismatch",
    "both",
    "versus",
    "against",
    "compare",
}

LIVE_CURRENT_TOKENS = {
    "weather",
    "temperature",
    "time",
    "date",
    "day",
    "night",
    "morning",
    "afternoon",
    "evening",
    "today",
    "tonight",
    "now",
    "current",
    "latest",
}

CURRENT_WORLD_TIME_TOKENS = {
    "time",
    "date",
    "day",
    "night",
    "morning",
    "afternoon",
    "evening",
    "today",
    "tonight",
    "now",
}

CURRENT_WORLD_WEATHER_TOKENS = {
    "weather",
    "temperature",
    "cold",
    "cool",
    "warm",
    "hot",
    "outside",
    "rain",
    "rainy",
    "cloud",
    "cloudy",
    "wind",
    "windy",
    "sunny",
    "storm",
    "stormy",
    "snow",
    "snowy",
}

CURRENT_WORLD_PRECISE_TOKENS = {
    "exact",
    "degree",
    "degrees",
    "celsius",
    "fahrenheit",
    "humidity",
    "humid",
    "windspeed",
    "pressure",
}

CURRENT_WORLD_CONCEPTUAL_TOKENS = {
    "black",
    "dark",
    "color",
    "colour",
    "meaning",
    "mean",
}

WORLD_KNOWLEDGE_TOKENS = {
    "capital",
    "country",
    "population",
    "currency",
    "president",
    "prime",
    "minister",
    "leader",
    "government",
    "nation",
    "state",
    "city",
    "match",
    "score",
    "won",
    "yesterday",
    "football",
    "soccer",
}

FINANCE_TOKENS = {
    "stock",
    "stocks",
    "buy",
    "sell",
    "purchase",
    "invest",
    "investment",
    "investing",
    "market",
    "portfolio",
    "equity",
    "equities",
    "shares",
    "ticker",
    "trading",
    "trade",
}

LIMITATION_TOKENS = {
    "mistake",
    "mistakes",
    "wrong",
    "error",
    "errors",
    "fail",
    "fails",
    "failed",
    "failing",
    "stupid",
    "dumb",
    "bad",
    "broken",
}

LOCAL_ARTIFACT_TOKENS = {
    "artifact",
    "artifacts",
    "bundle",
    "directory",
    "file",
    "files",
    "folder",
    "manifest",
    "output",
    "outputs",
    "path",
    "paths",
    "packet",
    "report",
    "reports",
    "review",
}

STATUS_TRUTH_TOKENS = {
    "approved",
    "closed",
    "complete",
    "completed",
    "open",
}

ORDERING_MATH_TOKENS = {
    "bigger",
    "greater",
    "higher",
    "larger",
    "less",
    "lower",
    "smaller",
}

ORIGIN_TOKENS = {
    "invent",
    "invented",
    "made",
    "make",
    "created",
    "creator",
    "built",
    "author",
    "origin",
}

FOLLOWUP_TOKENS = {
    "why",
    "how",
    "mean",
    "sure",
    "that",
    "this",
    "it",
    "explain",
    "clarify",
}

MATH_TOKENS = {
    "math",
    "calculate",
    "calculation",
    "compute",
    "count",
    "sum",
    "plus",
    "minus",
    "times",
    "multiply",
    "multiplied",
    "product",
    "divide",
    "divided",
    "quotient",
    "mod",
    "modulo",
}

PLANNING_TOKENS = {
    "confirm",
    "plan",
    "steps",
    "step",
    "outline",
    "verify",
    "verification",
    "check",
    "checklist",
    "review",
    "prove",
}

COMPARISON_TOKENS = {
    "compare",
    "comparison",
    "difference",
    "differ",
    "differs",
    "different",
    "versus",
    "vs",
    "contrast",
}

SESSION_HISTORY_TOKENS = {
    "ask",
    "asked",
    "say",
    "said",
    "previous",
    "prior",
    "last",
    "earlier",
    "before",
    "remember",
    "recall",
}

SUPPORT_DIAGNOSTIC_TOKENS = {
    "support",
    "missing",
    "evidence",
    "proof",
    "refs",
    "reference",
    "references",
    "uncertain",
    "uncertainty",
    "confidence",
    "confident",
    "sure",
}

ANSWER_MODE_TOKENS = {
    "grounded_fact",
    "bounded_estimate",
    "derived_explanation",
    "derived_estimate",
    "clarify",
    "abstain",
    "search_needed",
}

PROOF_RELEASE_TOKENS = {
    "proof",
    "release",
    "publish",
    "publication",
    "package",
    "packaging",
    "review",
    "validation",
}

ARTIFACT_LOCATION_TOKENS = {
    "archive",
    "bundle",
    "directory",
    "exists",
    "file",
    "files",
    "folder",
    "located",
    "location",
    "path",
    "paths",
    "where",
}

GOVERNANCE_HISTORY_TOKENS = {
    "change",
    "changes",
    "changelog",
    "decision",
    "decisions",
    "history",
    "latest",
    "recent",
}

PHASE_TRUTH_VERIFICATION_TOKENS = {
    "check",
    "checklist",
    "phase",
    "status",
    "truth",
    "verify",
    "verification",
}

FAIL_CLOSED_POLICY_TOKENS = {
    "fail",
    "failed",
    "closed",
    "support",
    "missing",
    "weak",
    "honest",
    "guess",
    "guessing",
    "bluff",
    "certainty",
    "confident",
}

SOURCE_BUCKET_BY_ID = {
    "project_readme": "project_identity",
    "master_plan": "project_identity",
    "human_target": "project_identity",
    "phase_truth": "phase_truth",
    "decisions": "phase_truth",
    "changelog": "phase_truth",
    "runtime_shell_snapshot": "runtime_identity",
    "runtime_session_open": "runtime_identity",
    "state_export": "runtime_state",
    "memory_review_export": "runtime_state",
    "safe_shutdown": "runtime_state",
    "phase10_overlay": "phase_context",
    "phase11_overlay": "phase_context",
    "phase12_overlay": "phase_context",
    "phase13_manifest": "evidence",
    "phase14_manifest": "evidence",
    "phase15_manifest": "evidence",
    "phase14_audit": "manifest_budget",
    "phase14_profiles": "manifest_budget",
    "phase15_artifact_inventory": "evidence",
    "claim_boundary": "verification_policy",
    "phase16_bounded_plan": "verification_policy",
    "role_authority_rules": "verification_policy",
    "validation_protocol": "verification_policy",
    "runtime_rebuild_map": "project_history",
    "runtime_limits": "runtime_limits",
    "local_clock_context": "current_world",
    "local_world_prior": "current_world",
    "prior_turn": "turn_history",
    "interactive_history": "turn_history",
}

CLASS_BUCKET_PRIORITY: dict[str, tuple[str, ...]] = {
    "self_system_status": ("runtime_identity", "runtime_limits", "runtime_state", "project_identity"),
    "project_phase_capability": ("project_identity", "phase_truth", "runtime_limits", "runtime_identity"),
    "local_truth_evidence": ("phase_truth", "evidence", "manifest_budget", "runtime_state"),
    "reasoning_math": ("runtime_limits", "turn_history", "project_identity"),
    "comparison_planning": ("verification_policy", "project_identity", "phase_truth", "project_history", "evidence"),
    "session_history": ("turn_history", "runtime_state", "runtime_identity"),
    "support_diagnostics": ("turn_history", "phase_truth", "evidence", "verification_policy", "runtime_limits"),
    "contradiction": ("phase_truth", "evidence", "phase_context"),
    "current_world": ("current_world", "runtime_identity", "runtime_limits"),
    "underspecified": ("turn_history", "runtime_identity", "phase_truth"),
    "unsupported": ("runtime_limits", "project_identity"),
}

BOUNDARY_TOKENS = {
    "bound",
    "bounded",
    "limit",
    "limits",
    "limitation",
    "limitations",
    "scope",
    "support",
}

FOLLOW_UP_REASON_TOKENS = {
    "why",
    "because",
    "mistake",
    "mistakes",
    "wrong",
    "error",
    "errors",
    "reason",
}

FOLLOW_UP_EXPLANATION_TOKENS = {
    "mean",
    "means",
    "explain",
    "explains",
    "explained",
    "clarify",
    "clarification",
}

FOLLOW_UP_METHOD_TOKENS = {"how"}

FOLLOW_UP_CONFIDENCE_TOKENS = {
    "sure",
    "certain",
    "confident",
    "confidence",
    "right",
    "verify",
    "verified",
}

UNDERSPECIFIED_REFERENCE_TOKENS = {"it", "that", "this", "there", "here"}
USER_IDENTITY_TOKENS = {"i", "me", "my", "mine"}
PROFILE_NAME = "laptop"
DEFAULT_TARGET_DOMAIN = "planning_coordination_workflows"
LOCAL_CURRENT_WORLD_TIMEZONE = ZoneInfo("Europe/Berlin")
LOCAL_CURRENT_WORLD_LOCATION = "berlin"
CURRENT_WORLD_TARGET_PREPOSITIONS = {"in", "on", "at", "for", "near", "around", "over"}
CURRENT_WORLD_PRIOR_REGISTRY = (
    {
        "location_key": "berlin",
        "label": "Berlin",
        "timezone": "Europe/Berlin",
        "climate_profile": "temperate_central_europe",
        "prior_ref": "dynamic::local_world_prior:2",
        "estimate_allowed": True,
        "target_kind": "local_city",
        "aliases": ("berlin", "berlin germany", "local city"),
    },
    {
        "location_key": "polar_region",
        "label": "a polar region",
        "timezone": "UTC",
        "climate_profile": "polar_continent",
        "prior_ref": "dynamic::global_world_prior:1",
        "estimate_allowed": True,
        "target_kind": "polar_region",
        "aliases": (
            "antarctica",
            "antarctic",
            "arctic",
            "north pole",
            "south pole",
            "polar region",
            "polar continent",
        ),
    },
)
CURRENT_WORLD_PRIORS = {
    str(item["location_key"]): dict(item)
    for item in CURRENT_WORLD_PRIOR_REGISTRY
}
CURRENT_WORLD_PRIOR_ALIAS_MAP = {
    alias: dict(item)
    for item in CURRENT_WORLD_PRIOR_REGISTRY
    for alias in item["aliases"]
}
EXTRATERRESTRIAL_TARGET_TOKENS = {
    "asteroid",
    "asteroids",
    "comet",
    "comets",
    "galaxy",
    "jupiter",
    "lunar",
    "mars",
    "mercury",
    "moon",
    "neptune",
    "orbit",
    "orbital",
    "planet",
    "planets",
    "pluto",
    "saturn",
    "space",
    "star",
    "stars",
    "sun",
    "uranus",
    "venus",
}
CLIMATE_PRIOR_PROFILES = {
    "temperate_central_europe": {
        "winter": {
            "general": "cold overall",
            "day": "cold to cool",
            "night": "cold",
            "outdoor": "more likely cold than mild",
            "sky": "cloud, wind, or light precipitation remain plausible",
        },
        "spring": {
            "general": "cool to mild overall",
            "day": "cool to mild",
            "night": "cool",
            "outdoor": "more likely cool than warm",
            "sky": "clouds or light rain remain plausible",
        },
        "summer": {
            "general": "mild to warm overall",
            "day": "warm to hot",
            "night": "mild",
            "outdoor": "more likely mild or warm than cold",
            "sky": "sun or broken cloud are plausible, with storms still possible",
        },
        "autumn": {
            "general": "cool overall",
            "day": "cool to mild",
            "night": "cool to cold",
            "outdoor": "more likely cool than warm",
            "sky": "cloud, wind, or rain remain plausible",
        },
    },
    "polar_continent": {
        "winter": {
            "general": "extremely cold overall",
            "day": "extremely cold",
            "night": "extremely cold",
            "outdoor": "extremely cold and potentially windy",
            "sky": "snow, wind, and whiteout conditions remain plausible",
        },
        "spring": {
            "general": "extremely cold overall",
            "day": "extremely cold",
            "night": "extremely cold",
            "outdoor": "extremely cold and likely harsh",
            "sky": "snow and wind remain plausible",
        },
        "summer": {
            "general": "still very cold overall",
            "day": "very cold",
            "night": "very cold",
            "outdoor": "very cold with wind still plausible",
            "sky": "snow, wind, and cloud remain plausible",
        },
        "autumn": {
            "general": "extremely cold overall",
            "day": "extremely cold",
            "night": "extremely cold",
            "outdoor": "extremely cold and likely harsh",
            "sky": "snow and wind remain plausible",
        },
    }
}
QUESTION_CLASS_ORDER = (
    "self_system_status",
    "project_phase_capability",
    "local_truth_evidence",
    "reasoning_math",
    "comparison_planning",
    "session_history",
    "support_diagnostics",
    "contradiction",
    "current_world",
    "follow_up_context",
    "underspecified",
    "unsupported",
)

ROUTE_FAMILIES: dict[str, tuple[str, ...]] = {
    "self_system_status": (
        "continuity_self_history",
        "governance_authority",
        "language_realizer",
    ),
    "project_phase_capability": (
        "planner",
        "language_realizer",
        "governance_authority",
    ),
    "local_truth_evidence": (
        "audit_replay",
        "continuity_self_history",
        "working_memory",
    ),
    "reasoning_math": (
        "planner",
        "critic_error_monitor",
        "working_memory",
    ),
    "comparison_planning": (
        "planner",
        "audit_replay",
        "language_realizer",
    ),
    "session_history": (
        "continuity_self_history",
        "working_memory",
        "language_realizer",
    ),
    "support_diagnostics": (
        "critic_error_monitor",
        "audit_replay",
        "continuity_self_history",
    ),
    "contradiction": (
        "critic_error_monitor",
        "audit_replay",
        "planner",
    ),
    "current_world": (
        "planner",
        "critic_error_monitor",
        "language_realizer",
    ),
    "underspecified": (
        "intake_router",
        "attention",
        "planner",
    ),
    "unsupported": (
        "attention",
        "governance_authority",
        "language_realizer",
    ),
}


@dataclass(slots=True)
class SourceLine:
    source_id: str
    path: str
    line_number: int
    text: str
    tags: tuple[str, ...]
    bucket: str
    tokens: set[str]
    target_domain: str
    trust_band: str

    @property
    def ref(self) -> str:
        return f"{self.path}:{self.line_number}"


@dataclass(slots=True)
class FollowUpBindingDecision:
    detected: bool
    intent: str | None
    anchor_turn: Mapping[str, Any] | None
    anchor_turn_id: str | None
    confidence: float
    reason: str
    success: bool


@dataclass(slots=True)
class ProcedureSpec:
    procedure_id: str
    procedure_name: str
    objective: str
    steps: list[str]
    preconditions: list[str]
    postconditions: list[str]
    constraints: list[str]
    graph_refs: list[str]
    provenance_refs: list[str]


def _bucket_for_source(source_id: str) -> str:
    bucket_map = {
        "project_readme": "project_identity",
        "master_plan": "project_identity",
        "human_target": "project_identity",
        "phase_truth": "phase_truth",
        "decisions": "governance_history",
        "changelog": "governance_history",
        "runtime_shell_snapshot": "runtime_identity",
        "runtime_session_open": "runtime_identity",
        "state_export": "runtime_state",
        "memory_review_export": "runtime_state",
        "safe_shutdown": "runtime_state",
        "phase10_overlay": "critique_state",
        "phase11_overlay": "historical_context",
        "phase12_overlay": "historical_context",
        "phase13_manifest": "evidence_manifest",
        "phase14_manifest": "evidence_manifest",
        "phase15_manifest": "evidence_manifest",
        "phase14_audit": "manifest_profile",
        "phase14_profiles": "manifest_profile",
        "phase15_artifact_inventory": "evidence_manifest",
        "claim_boundary": "verification_policy",
        "phase16_bounded_plan": "verification_policy",
        "role_authority_rules": "verification_policy",
        "validation_protocol": "verification_policy",
        "runtime_rebuild_map": "project_history",
        "local_clock_context": "current_world",
        "local_world_prior": "current_world",
        "prior_turn_context": "prior_turn_context",
        "prior_turn_support": "prior_turn_context",
    }
    return bucket_map.get(source_id, "local_truth")


def _parse_ref(ref: str) -> tuple[str, int]:
    path, sep, maybe_line = ref.rpartition(":")
    if sep and maybe_line.isdigit():
        return path, int(maybe_line)
    return ref, 1


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_token(token: str) -> str:
    clean = token.strip().lower()
    if clean.endswith("'s"):
        clean = clean[:-2]
    clean = TOKEN_ALIASES.get(clean, clean)
    if clean.endswith("ies") and len(clean) > 4:
        clean = clean[:-3] + "y"
    elif clean.endswith("s") and len(clean) > 4:
        clean = clean[:-1]
    return clean


def _tokenize(text: str) -> tuple[str, ...]:
    tokens: list[str] = []
    for raw in re.findall(r"[a-zA-Z0-9']+", text.lower()):
        clean = _normalize_token(raw)
        if clean:
            tokens.append(clean)
    return tuple(tokens)


def _season_name(month: int) -> str:
    if month in {12, 1, 2}:
        return "winter"
    if month in {3, 4, 5}:
        return "spring"
    if month in {6, 7, 8}:
        return "summer"
    return "autumn"


def _time_band(hour: int) -> str:
    if 0 <= hour < 5:
        return "late_night"
    if 5 <= hour < 8:
        return "early_morning"
    if 8 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    if 17 <= hour < 21:
        return "evening"
    return "night"


def _local_current_world_context() -> dict[str, Any]:
    now = datetime.now(LOCAL_CURRENT_WORLD_TIMEZONE).replace(second=0, microsecond=0)
    hour = now.hour
    month = now.month
    season = _season_name(month)
    band = _time_band(hour)
    return {
        "iso_timestamp": now.isoformat(),
        "date": now.date().isoformat(),
        "time": now.strftime("%H:%M"),
        "timezone": "Europe/Berlin",
        "month_number": month,
        "month_name": now.strftime("%B"),
        "season": season,
        "hour": hour,
        "time_band": band,
        "is_night": band in {"late_night", "night"},
    }


def _current_world_prior_for_target(target_text: str) -> dict[str, Any] | None:
    normalized_target = re.sub(r"\s+", " ", target_text.strip().lower()).strip()
    if not normalized_target:
        return None
    compact_target = normalized_target.replace(" ", "_")
    if compact_target in CURRENT_WORLD_PRIORS:
        return dict(CURRENT_WORLD_PRIORS[compact_target])
    return dict(CURRENT_WORLD_PRIOR_ALIAS_MAP.get(normalized_target, {})) or None


def _current_world_request_kind(question_text: str) -> str | None:
    tokens = _content_tokens(question_text)
    raw_tokens = set(_tokenize(question_text))
    runtime_context = PROJECT_TOKENS | SELF_TOKENS | PHASE_TOKENS | EVIDENCE_TOKENS | {"runtime", "session"}
    excluded_tokens = FINANCE_TOKENS | WORLD_KNOWLEDGE_TOKENS
    if raw_tokens.intersection(CURRENT_WORLD_CONCEPTUAL_TOKENS):
        return None
    if raw_tokens.intersection(CURRENT_WORLD_WEATHER_TOKENS):
        if not tokens.intersection(runtime_context):
            return "weather"
    time_signal = raw_tokens.intersection(CURRENT_WORLD_TIME_TOKENS - {"current", "latest", "today", "tonight"})
    if time_signal:
        if not tokens.intersection(runtime_context) and not raw_tokens.intersection(excluded_tokens):
            return "time"
    return None


def _display_target_label(target_text: str) -> str:
    normalized = re.sub(r"\s+", " ", target_text.strip()).strip()
    if not normalized:
        return "unknown location"
    lowered = normalized.lower()
    if lowered.startswith("the "):
        return "the " + " ".join(part.capitalize() for part in normalized.split()[1:])
    return " ".join(part.capitalize() for part in normalized.split())


def _current_world_target_kind(target_text: str) -> str:
    normalized_target = re.sub(r"\s+", " ", target_text.strip().lower()).strip()
    if not normalized_target:
        return "unknown_target"
    prior = _current_world_prior_for_target(target_text)
    if prior:
        return str(prior.get("target_kind", "supported_local_prior"))
    target_tokens = set(_tokenize(normalized_target))
    if target_tokens.intersection(EXTRATERRESTRIAL_TARGET_TOKENS):
        return "extraterrestrial_body"
    return "named_earth_location"


def _current_world_location(question_text: str) -> dict[str, Any]:
    raw_tokens = tuple(_tokenize(question_text))
    explicit_tokens: list[str] = []
    stop_tokens = STOPWORDS | CURRENT_WORLD_TIME_TOKENS | CURRENT_WORLD_WEATHER_TOKENS | CURRENT_WORLD_PRECISE_TOKENS
    for index, token in enumerate(raw_tokens):
        if token not in CURRENT_WORLD_TARGET_PREPOSITIONS:
            continue
        collected: list[str] = []
        for candidate in raw_tokens[index + 1 :]:
            if candidate in stop_tokens:
                if collected:
                    break
                continue
            collected.append(candidate)
            if len(collected) >= 3:
                break
        if collected:
            explicit_tokens = collected
            break
    explicit_target = " ".join(explicit_tokens).strip()
    if explicit_target:
        target_kind = _current_world_target_kind(explicit_target)
        prior = _current_world_prior_for_target(explicit_target)
        if prior:
            return {
                "location_key": str(prior["location_key"]),
                "label": _display_target_label(explicit_target),
                "explicit": True,
                "grounded": True,
                "supported": bool(prior.get("climate_profile")),
                "estimate_allowed": bool(prior.get("estimate_allowed")),
                "target_kind": target_kind,
                "prior": prior,
            }
        return {
            "location_key": explicit_target.replace(" ", "_"),
            "label": _display_target_label(explicit_target),
            "explicit": True,
            "grounded": True,
            "supported": False,
            "estimate_allowed": False,
            "target_kind": target_kind,
            "prior": None,
        }
    if set(raw_tokens).intersection(CURRENT_WORLD_WEATHER_TOKENS | CURRENT_WORLD_TIME_TOKENS):
        prior = CURRENT_WORLD_PRIORS[LOCAL_CURRENT_WORLD_LOCATION]
        return {
            "location_key": LOCAL_CURRENT_WORLD_LOCATION,
            "label": prior["label"],
            "explicit": False,
            "grounded": True,
            "supported": True,
            "estimate_allowed": True,
            "target_kind": str(prior.get("target_kind", "local_city")),
            "prior": prior,
        }
    return {
        "location_key": "unknown",
        "label": "unknown location",
        "explicit": False,
        "grounded": False,
        "supported": False,
        "estimate_allowed": False,
        "target_kind": "unknown_target",
        "prior": None,
    }


def _has_local_runtime_anchor(question_text: str) -> bool:
    raw_tokens = set(_tokenize(question_text))
    tokens = _content_tokens(question_text)
    local_anchor_tokens = (
        PROJECT_TOKENS
        | PHASE_TOKENS
        | EVIDENCE_TOKENS
        | {"runtime", "session", "shell", "repo", "repository", "file", "files", "path", "paths"}
    )
    return bool(tokens.intersection(local_anchor_tokens) or raw_tokens.intersection({"agif", "agifcore"}))


def _unsupported_request_domain(question_text: str) -> str | None:
    raw_tokens = set(_tokenize(question_text))
    tokens = _content_tokens(question_text)
    if "who" in raw_tokens and tokens.intersection(USER_IDENTITY_TOKENS):
        return "personal_identity"
    if _has_local_runtime_anchor(question_text):
        return None
    if raw_tokens.intersection(FINANCE_TOKENS):
        return "finance"
    if _current_world_request_kind(question_text) is None and raw_tokens.intersection(WORLD_KNOWLEDGE_TOKENS):
        return "external_fact"
    if "who" in raw_tokens and not ({"you", "yourself", "system", "runtime", "agifcore"} & raw_tokens):
        return "external_fact"
    return None


def _extract_math_expression(question_text: str) -> str | None:
    candidate = question_text.lower().strip()
    candidate = candidate.replace("what's", "what is")
    for source, target in (
        ("multiplied by", "*"),
        ("times", "*"),
        ("x", "*"),
        ("plus", "+"),
        ("minus", "-"),
        ("divided by", "/"),
        ("over", "/"),
        ("modulo", "%"),
        ("mod", "%"),
    ):
        candidate = re.sub(rf"\b{re.escape(source)}\b", f" {target} ", candidate)
    candidate = re.sub(r"\b(what is|calculate|compute|solve|evaluate)\b", " ", candidate)
    candidate = candidate.replace("?", " ").replace("=", " ")
    candidate = " ".join(candidate.split())
    if not re.search(r"\d", candidate):
        return None
    if not re.search(r"[+\-*/%()]", candidate):
        return None
    if not re.fullmatch(r"[0-9\.\s+\-*/%()]+", candidate):
        return None
    return candidate


def _safe_eval_math_expression(expression: str) -> int | float | None:
    binary_ops: dict[type[Any], Any] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
    }
    unary_ops: dict[type[Any], Any] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def _eval(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_ops:
            return unary_ops[type(node.op)](_eval(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in binary_ops:
            return binary_ops[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("unsupported math node")

    try:
        parsed = ast.parse(expression, mode="eval")
        result = _eval(parsed)
    except Exception:
        return None
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result


def _extract_compare_entities(question_text: str) -> tuple[str, str] | None:
    normalized = re.sub(r"\s+", " ", question_text.lower()).strip(" ?.!")
    patterns = (
        r"\bcompare\s+(.+?)\s+(?:and|vs|versus|with)\s+(.+)$",
        r"\bdifference\s+between\s+(.+?)\s+and\s+(.+)$",
    )
    for pattern in patterns:
        match = re.search(pattern, normalized)
        if not match:
            continue
        left = _clean_text(match.group(1))
        right = _clean_text(match.group(2))
        if left and right:
            return left, right
    return None


def _content_tokens(text: str) -> set[str]:
    return {token for token in _tokenize(text) if token not in STOPWORDS}


def _extract_phase_numbers(text: str) -> tuple[int, ...]:
    matches: list[int] = []
    for match in re.finditer(r"\bphase\s*(\d{1,2})\b", text.lower()):
        matches.append(int(match.group(1)))
    return tuple(dict.fromkeys(matches))


def _numeric_literals(text: str) -> tuple[float, ...]:
    values: list[float] = []
    for match in re.finditer(r"(?<!\w)-?\d+(?:\.\d+)?(?!\w)", text):
        values.append(float(match.group(0)))
    return tuple(values)


def _is_ordering_math_request(question_text: str) -> bool:
    raw_tokens = set(_tokenize(question_text))
    return len(_numeric_literals(question_text)) >= 2 and bool(raw_tokens.intersection(ORDERING_MATH_TOKENS))


def _looks_like_self_system_request(question_text: str) -> bool:
    raw_tokens = set(_tokenize(question_text))
    if raw_tokens.intersection({"bundle", "manifest", "output", "phase", "profile", "report"}):
        return False
    if raw_tokens.intersection({"capability", "capabilities"}) or {"can", "do"} <= raw_tokens:
        return False
    if raw_tokens.intersection({"you", "your", "yourself"}) and raw_tokens.intersection(
        ORIGIN_TOKENS | {"builder", "runtime", "shell", "surface", "surfaces", "system"}
    ):
        return True
    if raw_tokens.intersection({"builder", "runtime", "shell", "system"}) and raw_tokens.intersection({"are", "is", "what", "which"}):
        return True
    if raw_tokens.intersection(ORIGIN_TOKENS) and raw_tokens.intersection({"repo", "repository", "runtime", "system", "you", "your"}):
        return True
    return False


def _looks_like_contradiction_request(
    question_text: str,
    *,
    phase7_interpretation_state: Mapping[str, Any] | None = None,
) -> bool:
    raw_tokens = set(_tokenize(question_text))
    tokens = _content_tokens(question_text)
    phase_numbers = _extract_phase_numbers(question_text)
    status_tokens = raw_tokens.intersection(STATUS_TRUTH_TOKENS)
    support_absence = bool(raw_tokens.intersection({"without", "missing", "absent"})) and bool(
        raw_tokens.intersection({"support", "evidence", "proof", "local"})
    )
    support_resolution = bool(
        raw_tokens.intersection({"answer", "answered", "claim", "claimed", "confidence", "confident", "confidently", "guess", "guessing", "valid"})
    )
    if raw_tokens.intersection({"conflict", "conflicting", "contradict", "contradiction", "disagree", "inconsistent", "mismatch"}):
        return True
    if len(phase_numbers) == 1 and len(status_tokens) >= 2:
        return True
    if phase_numbers and len(status_tokens) >= 2 and raw_tokens.intersection({"also", "both", "true"}):
        return True
    if support_absence and support_resolution:
        return True
    if raw_tokens.intersection({"guess", "gues"}) and raw_tokens.intersection({"support", "evidence", "proof", "local", "absent", "missing"}):
        return True
    if raw_tokens.intersection({"manifest", "manifests"}) and raw_tokens.intersection({"disagree", "mismatch", "conflict"}):
        return True
    if phase7_interpretation_state and bool(phase7_interpretation_state.get("comparison_requested")) and (
        phase_numbers or tokens.intersection(PHASE_TOKENS | STATUS_TRUTH_TOKENS)
    ):
        return True
    return False


def _looks_like_local_artifact_request(question_text: str) -> bool:
    raw_tokens = set(_tokenize(question_text))
    tokens = _content_tokens(question_text)
    if _extract_compare_entities(question_text) is not None:
        return False
    if _looks_like_contradiction_request(question_text):
        return False
    if raw_tokens.intersection(LOCAL_ARTIFACT_TOKENS) and tokens.intersection(EVIDENCE_TOKENS | {"local", "proof", "runtime"}):
        return True
    if raw_tokens.intersection({"exist", "exists", "available"} | ARTIFACT_LOCATION_TOKENS) and tokens.intersection(EVIDENCE_TOKENS | LOCAL_ARTIFACT_TOKENS):
        return True
    return False


def _looks_like_support_diagnostic_request(question_text: str) -> bool:
    raw_tokens = set(_tokenize(question_text))
    tokens = _content_tokens(question_text)
    referential_tokens = {"answer", "earlier", "it", "previous", "prior", "response", "that", "this"}
    if _extract_compare_entities(question_text) is not None:
        return False
    if _looks_like_contradiction_request(question_text):
        return False
    if raw_tokens.intersection(COMPARISON_TOKENS | {"compare", "difference", "explain", "valid", "guess", "should", "happen"}):
        return False
    if not raw_tokens.intersection(SUPPORT_DIAGNOSTIC_TOKENS):
        return False
    if raw_tokens.intersection({"if"}) and not raw_tokens.intersection(referential_tokens):
        return False
    if tokens.intersection(LOCAL_ARTIFACT_TOKENS) and not raw_tokens.intersection(referential_tokens):
        return False
    if raw_tokens.intersection({"what", "which"}) and raw_tokens.intersection({"support", "evidence", "missing"}):
        return True
    if raw_tokens.intersection(referential_tokens) and raw_tokens.intersection(SUPPORT_DIAGNOSTIC_TOKENS):
        return True
    return False


def _looks_like_underspecified_request(question_text: str) -> bool:
    raw_tokens = set(_tokenize(question_text))
    tokens = _content_tokens(question_text)
    domain_anchor_tokens = (
        PROJECT_TOKENS
        | EVIDENCE_TOKENS
        | PHASE_TOKENS
        | SUPPORT_DIAGNOSTIC_TOKENS
        | CURRENT_WORLD_WEATHER_TOKENS
        | CURRENT_WORLD_TIME_TOKENS
        | FINANCE_TOKENS
    )
    if (
        raw_tokens.intersection({"mean", "sure", "asked", "ask", "response", "answer"})
        or (raw_tokens.intersection({"why"}) and raw_tokens.intersection({"that", "this", "it"}))
    ) and not tokens.intersection(domain_anchor_tokens):
        return False
    if raw_tokens == {"why"}:
        return False
    if raw_tokens.intersection({"why"}) and raw_tokens.intersection({"that", "this", "it"}) and not raw_tokens.intersection({"fail", "failed"}):
        return False
    if len(tokens) <= 1 and raw_tokens.intersection({"what", "why", "tell", "explain"}) and not tokens.intersection(domain_anchor_tokens) and not ({"can", "do"} <= raw_tokens):
        return True
    if raw_tokens.intersection({"what", "why", "tell", "explain", "show"}) and raw_tokens.intersection(
        {"about", "break", "broke", "broken", "change", "changed", "detail", "details", "event", "events", "fail", "failed", "failing", "happen", "happened", "it", "more", "that", "this"}
    ) and not tokens.intersection(domain_anchor_tokens):
        return True
    if len(tokens) <= 3 and raw_tokens.intersection({"it", "that", "this"}) and not tokens.intersection(domain_anchor_tokens):
        return True
    return False


def _anchor_turn(
    *,
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]] | None = None,
) -> Mapping[str, Any] | None:
    if prior_turn:
        return prior_turn
    if recent_turns:
        for turn in reversed(recent_turns):
            if str(turn.get("question_text", "")).strip():
                return turn
    return None


def _clean_text(value: str) -> str:
    return " ".join(str(value).split()).strip()


def _truncate_text(value: str, *, limit: int = 180) -> str:
    text = _clean_text(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _turn_local_refs(turn_state: Mapping[str, Any] | None) -> tuple[str, ...]:
    if not turn_state:
        return ()
    refs = turn_state.get("local_truth_refs", [])
    return tuple(str(ref) for ref in refs if str(ref).strip())


def _turn_source_ids(turn_state: Mapping[str, Any] | None) -> tuple[str, ...]:
    if not turn_state:
        return ()
    source_ids = turn_state.get("source_set_used", [])
    return tuple(str(source_id) for source_id in source_ids if str(source_id).strip())


def _turn_request_text(turn_state: Mapping[str, Any] | None) -> str:
    if not turn_state:
        return ""
    request_text = str(turn_state.get("request_text") or turn_state.get("question_text") or "").strip()
    return _clean_text(request_text)


def _turn_lookup(
    *,
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]] | None = None,
) -> dict[str, Mapping[str, Any]]:
    ordered: list[Mapping[str, Any]] = []
    for turn in list(recent_turns or []):
        if _turn_request_text(turn):
            ordered.append(turn)
    if prior_turn and _turn_request_text(prior_turn):
        prior_id = str(prior_turn.get("turn_id", "")).strip()
        if not prior_id or all(str(item.get("turn_id", "")).strip() != prior_id for item in ordered):
            ordered.append(prior_turn)
    lookup: dict[str, Mapping[str, Any]] = {}
    for turn in ordered:
        turn_id = str(turn.get("turn_id", "")).strip()
        if turn_id:
            lookup[turn_id] = turn
    return lookup


def _resolve_follow_up_subject_turn(
    *,
    turn_state: Mapping[str, Any] | None,
    turn_lookup: Mapping[str, Mapping[str, Any]],
) -> Mapping[str, Any] | None:
    current = turn_state
    visited: set[str] = set()
    while current:
        anchor_id = str(current.get("followup_anchor_turn_id", "")).strip()
        if not anchor_id or anchor_id in visited:
            break
        if not bool(current.get("followup_detected")) or not bool(current.get("followup_binding_success")):
            break
        if anchor_id not in turn_lookup:
            break
        visited.add(anchor_id)
        next_turn = turn_lookup[anchor_id]
        if next_turn is current:
            break
        current = next_turn
    return current


def _build_follow_up_binding(
    *,
    question_text: str,
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]] | None = None,
) -> FollowUpBindingDecision:
    anchor_source_turn = _anchor_turn(prior_turn=prior_turn, recent_turns=recent_turns)
    detected_intent = _follow_up_intent(question_text=question_text, prior_turn=anchor_source_turn)
    if detected_intent is None:
        return FollowUpBindingDecision(
            detected=False,
            intent=None,
            anchor_turn=None,
            anchor_turn_id=None,
            confidence=0.0,
            reason="prompt does not require prior-turn binding",
            success=False,
        )
    if not anchor_source_turn:
        return FollowUpBindingDecision(
            detected=True,
            intent=detected_intent,
            anchor_turn=None,
            anchor_turn_id=None,
            confidence=0.0,
            reason="no stored prior turn exists yet",
            success=False,
        )
    turn_lookup = _turn_lookup(prior_turn=prior_turn, recent_turns=recent_turns)
    if detected_intent == "history":
        anchor_turn = anchor_source_turn
        confidence = 0.99
        reason = "history follow-up binds to the immediately previous stored turn"
    else:
        anchor_turn = _resolve_follow_up_subject_turn(turn_state=anchor_source_turn, turn_lookup=turn_lookup)
        if anchor_turn is anchor_source_turn:
            confidence = 0.92
            reason = "binding uses the most recent stored turn state"
        elif anchor_turn is not None:
            confidence = 0.95
            reason = "previous turn was itself a follow-up, so binding reuses its stored anchor state"
        else:
            confidence = 0.0
            reason = "no stable follow-up anchor could be resolved from stored turn state"
    anchor_turn_id = str(anchor_turn.get("turn_id", "")).strip() if anchor_turn else None
    return FollowUpBindingDecision(
        detected=True,
        intent=detected_intent,
        anchor_turn=anchor_turn,
        anchor_turn_id=anchor_turn_id or None,
        confidence=confidence if anchor_turn_id else 0.0,
        reason=reason,
        success=bool(anchor_turn_id),
    )


def _format_local_refs_text(turn_state: Mapping[str, Any] | None, *, ceiling: int = 3) -> str:
    refs = list(_turn_local_refs(turn_state))[:ceiling]
    if not refs:
        return ""
    return f" Local refs: {', '.join(refs)}."


def _turn_topic_label(turn_state: Mapping[str, Any] | None) -> str:
    request_text = _turn_request_text(turn_state)
    if not request_text:
        return "the previous turn"
    return f"`{request_text}`"


def _turn_policy_summary(turn_state: Mapping[str, Any] | None) -> str:
    if not turn_state:
        return "the earlier turn had no stored state"
    question_class = str(turn_state.get("question_class", "unsupported"))
    support_state = str(turn_state.get("support_state", "unknown"))
    next_action = str(turn_state.get("next_action", "abstain"))
    answer_mode = str(turn_state.get("answer_mode", "abstain"))
    return (
        f"it was classified as {question_class}, support state was {support_state}, "
        f"next action was {next_action}, and answer mode was {answer_mode}"
    )


def _follow_up_intent(
    *,
    question_text: str,
    prior_turn: Mapping[str, Any] | None,
) -> str | None:
    if not prior_turn:
        return None
    raw_tokens = set(_tokenize(question_text))
    tokens = _content_tokens(question_text)
    standalone_domain_tokens = {
        "runtime",
        "shell",
        "local",
        "agif",
        "agifcore",
        "project",
        "phase",
        "policy",
        "evidence",
        "manifest",
        "report",
        "surface",
        "surfaces",
        "status",
        "capability",
        "capabilities",
        "limit",
        "limits",
        "task",
        "tasks",
        "repo",
        "repository",
        "file",
        "files",
        "path",
        "paths",
        "builder",
        "proof",
        "release",
    }
    if not raw_tokens or _current_world_request_kind(question_text) is not None:
        return None
    if _looks_like_contradiction_request(question_text) or _extract_compare_entities(question_text) is not None:
        return None
    if _looks_like_underspecified_request(question_text):
        return None
    referential = bool(raw_tokens.intersection({"that", "this", "it", "previous", "prior", "before", "earlier", "answer", "response"}))
    if referential and (tokens | raw_tokens).intersection(standalone_domain_tokens):
        referential = False
    meta_tokens = (
        FOLLOW_UP_REASON_TOKENS
        | FOLLOW_UP_METHOD_TOKENS
        | FOLLOW_UP_EXPLANATION_TOKENS
        | FOLLOW_UP_CONFIDENCE_TOKENS
        | {"why"}
    )
    if raw_tokens.intersection(SESSION_HISTORY_TOKENS) and raw_tokens.intersection({"ask", "asked", "say", "said"}):
        return "history"
    if _looks_like_support_diagnostic_request(question_text):
        return "support"
    non_meta_tokens = {token for token in tokens if token not in meta_tokens}
    compact_meta_request = bool(raw_tokens.intersection(meta_tokens)) and not non_meta_tokens
    if not (referential or compact_meta_request):
        return None
    if raw_tokens.intersection(FOLLOW_UP_REASON_TOKENS):
        return "reason"
    if raw_tokens.intersection(FOLLOW_UP_METHOD_TOKENS):
        return "method"
    if raw_tokens.intersection(FOLLOW_UP_EXPLANATION_TOKENS) or ("what" in raw_tokens and "mean" in raw_tokens):
        return "explanation"
    if raw_tokens.intersection(FOLLOW_UP_CONFIDENCE_TOKENS):
        return "confidence"
    if referential:
        return "explanation"
    return None


@lru_cache(maxsize=1)
def _project_goal() -> str:
    return "Build AGIFCore as the new canonical AGIF system from scratch, using earlier AGIF repos as source material only."


@lru_cache(maxsize=1)
def _master_plan_goal_lines() -> tuple[str, ...]:
    return (
        "AGIFCore's end goal is human-like functional thinking under AGIF rules.",
        "The target includes understanding messy language, reasoning through support and planning, remembering, correcting itself, and staying honest when support is weak.",
        "The system must remain local-first, auditable, governed, fail-closed, and free of hidden external models.",
    )


@lru_cache(maxsize=1)
def _human_target_lines() -> tuple[str, ...]:
    return tuple(
        line.strip("- ").strip()
        for line in _read_text(PROJECT_ROOT / "01_plan" / "HUMAN_THINKING_TARGET.md").splitlines()
        if line.startswith("- ")
    )


@lru_cache(maxsize=1)
def _phase_index_rows() -> dict[int, dict[str, str]]:
    rows: dict[int, dict[str, str]] = {}
    pattern = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|$")
    for line in _read_text(PROJECT_ROOT / "01_plan" / "PHASE_INDEX.md").splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        rows[int(match.group(1))] = {
            "title": match.group(2).strip(),
            "purpose": match.group(3).strip(),
            "status": match.group(4).strip(),
        }
    return rows


@lru_cache(maxsize=1)
def _phase_gate_rows() -> dict[int, dict[str, str]]:
    rows: dict[int, dict[str, str]] = {}
    pattern = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|$")
    for line in _read_text(PROJECT_ROOT / "01_plan" / "PHASE_GATE_CHECKLIST.md").splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        rows[int(match.group(1))] = {
            "title": match.group(2).strip(),
            "status": match.group(3).strip(),
            "notes": match.group(4).strip(),
        }
    return rows


@lru_cache(maxsize=1)
def _latest_decision_line() -> str:
    lines = [line for line in _read_text(PROJECT_ROOT / "DECISIONS.md").splitlines() if line.startswith("| D-")]
    return lines[-1] if lines else "No decisions recorded."


@lru_cache(maxsize=1)
def _latest_change_lines() -> tuple[str, ...]:
    section_lines: list[str] = []
    in_latest = False
    for line in _read_text(PROJECT_ROOT / "CHANGELOG.md").splitlines():
        if line.startswith("## 2026-04-01"):
            in_latest = True
            continue
        if in_latest and line.startswith("## "):
            break
        if in_latest and line.startswith("- "):
            section_lines.append(line.strip("- ").strip())
    return tuple(section_lines[:8])


@lru_cache(maxsize=3)
def _evidence_manifest_summary(phase: int) -> dict[str, Any]:
    if phase == 13:
        path = PROJECT_ROOT / "06_outputs" / "phase_13_product_runtime_and_ux" / "phase_13_evidence" / "phase_13_evidence_manifest.json"
    elif phase == 14:
        path = PROJECT_ROOT / "06_outputs" / "phase_14_sandbox_profiles_and_scale_realization" / "phase_14_evidence" / "phase_14_evidence_manifest.json"
    elif phase == 15:
        path = PROJECT_ROOT / "06_outputs" / "phase_15_final_intelligence_proof_and_closure_audit" / "phase_15_evidence" / "phase_15_evidence_manifest.json"
    else:
        raise ValueError(f"unsupported phase manifest: {phase}")
    payload = _load_json(path)
    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "status": str(payload.get("status", "unknown")),
        "required_report_count": int(payload.get("required_report_count", 0)),
        "available_report_count": int(payload.get("available_report_count", 0)),
        "missing_reports": list(payload.get("missing_reports", [])),
        "invalid_reports": list(payload.get("invalid_reports", [])),
        "phase_remains_open": bool(payload.get("phase_remains_open", False)),
    }


def _trust_band_for_source(source_id: str) -> str:
    if source_id in {
        "project_readme",
        "master_plan",
        "human_target",
        "phase_truth",
        "phase14_audit",
        "phase15_manifest",
        "phase14_manifest",
        "phase13_manifest",
    }:
        return "reviewed"
    return "bounded_local"


def _document_lines(
    *,
    source_id: str,
    path: str,
    tags: Iterable[str],
    lines: Iterable[str],
    bucket: str | None = None,
    target_domain: str = DEFAULT_TARGET_DOMAIN,
) -> list[SourceLine]:
    result: list[SourceLine] = []
    tag_tuple = tuple(tags)
    trust_band = _trust_band_for_source(source_id)
    source_bucket = bucket or _bucket_for_source(source_id)
    for index, raw in enumerate(lines, start=1):
        text = _clean_text(str(raw))
        if not text or set(text) == {"|", "-", " "}:
            continue
        result.append(
            SourceLine(
                source_id=source_id,
                path=path,
                line_number=index,
                text=text,
                tags=tag_tuple,
                bucket=source_bucket,
                tokens=_content_tokens(text),
                target_domain=target_domain,
                trust_band=trust_band,
            )
        )
    return result


def _source_line_from_ref(
    *,
    source_id: str,
    ref: str,
    text: str,
    tags: Iterable[str],
    bucket: str | None = None,
    target_domain: str = DEFAULT_TARGET_DOMAIN,
) -> SourceLine:
    path, line_number = _parse_ref(ref)
    return SourceLine(
        source_id=source_id,
        path=path,
        line_number=line_number,
        text=_clean_text(text),
        tags=tuple(tags),
        bucket=bucket or _bucket_for_source(source_id),
        tokens=_content_tokens(text),
        target_domain=target_domain,
        trust_band=_trust_band_for_source(source_id),
    )

def _phase_truth_summary(phase: int) -> str | None:
    index_row = _phase_index_rows().get(phase)
    gate_row = _phase_gate_rows().get(phase)
    if not index_row or not gate_row:
        return None
    return f"Phase {phase} is `{gate_row['status']}` in the live gate files, with title `{index_row['title']}`."


def _latest_phase_lines() -> list[str]:
    lines: list[str] = []
    for phase in sorted(_phase_index_rows()):
        summary = _phase_truth_summary(phase)
        if summary:
            lines.append(summary)
    return lines


def _phase11_lines(phase11_cycle_state: Mapping[str, Any]) -> list[str]:
    overlay = dict(phase11_cycle_state.get("overlay_contract", {}))
    return [
        f"Phase 11 support state is {overlay.get('support_state', 'unknown')}.",
        f"Phase 11 monitoring ref count is {len(overlay.get('monitoring_refs', []))}.",
        f"Phase 11 rollback ref count is {len(overlay.get('rollback_refs', []))}.",
        f"Phase 11 adopted proposal count is {len(overlay.get('adopted_proposal_ids', []))}.",
    ]


def _phase12_lines(phase12_cycle_state: Mapping[str, Any]) -> list[str]:
    overlay = dict(phase12_cycle_state.get("overlay_contract", {}))
    return [
        f"Phase 12 support state is {overlay.get('support_state', 'unknown')}.",
        f"Phase 12 selected gap count is {len(overlay.get('selected_gap_ids', []))}.",
        f"Phase 12 candidate theory count is {len(overlay.get('candidate_theory_ids', []))}.",
        f"Phase 12 candidate domain count is {len(overlay.get('candidate_domain_ids', []))}.",
        f"Phase 12 candidate procedure count is {len(overlay.get('candidate_procedure_ids', []))}.",
    ]


def _build_source_corpus(
    *,
    session_open: Mapping[str, Any],
    shell_snapshot: Mapping[str, Any],
    state_export: Mapping[str, Any],
    memory_review_export: Mapping[str, Any],
    safe_shutdown: Mapping[str, Any],
    phase10_turn_state: Mapping[str, Any],
    phase11_cycle_state: Mapping[str, Any],
    phase12_cycle_state: Mapping[str, Any],
    phase14_shell: SandboxProfileRuntimeShell,
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]],
) -> list[SourceLine]:
    current_world = _local_current_world_context()
    phase13_manifest = _evidence_manifest_summary(13)
    phase14_manifest = _evidence_manifest_summary(14)
    phase15_manifest = _evidence_manifest_summary(15)
    claim_boundary_path = PROJECT_ROOT / "01_plan" / "AGIFCORE_BOUNDED_INTELLIGENCE_CLAIM_BOUNDARY.md"
    phase16_bounded_plan_path = PROJECT_ROOT / "01_plan" / "PHASE_16_BOUNDED_RELEASE_AND_PUBLICATION.md"
    phase15_outputs_root = PROJECT_ROOT / "06_outputs" / "phase_15_final_intelligence_proof_and_closure_audit"
    phase15_evidence_dir = phase15_outputs_root / "phase_15_evidence"
    phase15_review_bundle_dir = phase15_outputs_root / "phase_15_review_bundle"
    artifact_inventory_paths = [
        phase15_review_bundle_dir / "REVIEW_FIRST.md",
        phase15_outputs_root / "phase_15_review_bundle.zip",
        *sorted(phase15_evidence_dir.glob("*.json")),
    ]
    phase14_audit = phase14_shell.manifest_audit()
    phase14_profiles = phase14_shell.profile_manifests()
    world_prior_lines = [
        "bounded current-world estimation uses registered local priors when available and abstains when no supported prior or live measurement exists."
    ]
    for prior in CURRENT_WORLD_PRIOR_REGISTRY:
        climate_profile = CLIMATE_PRIOR_PROFILES[str(prior["climate_profile"])][current_world["season"]]
        world_prior_lines.extend(
            [
                (
                    "supported_current_world_prior "
                    f"location_key={prior['location_key']} "
                    f"label={prior['label']} "
                    f"target_kind={prior['target_kind']} "
                    f"timezone={prior['timezone']} "
                    f"estimate_allowed={prior['estimate_allowed']}"
                ),
                (
                    "seasonal_current_world_prior "
                    f"location_key={prior['location_key']} "
                    f"season={current_world['season']} "
                    f"general={climate_profile['general']} "
                    f"outdoor={climate_profile['outdoor']} "
                    f"sky={climate_profile['sky']}"
                ),
            ]
        )
    world_prior_lines.extend(
        [
            "named Earth targets without a registered prior stay abstain unless a live measurement exists.",
            "extraterrestrial targets stay abstain because this shell has no extraterrestrial measurement path.",
        ]
    )
    artifact_inventory_lines = [
        f"artifact_path={path.relative_to(REPO_ROOT)} file_name={path.name}"
        for path in artifact_inventory_paths
        if path.exists()
    ]
    artifact_inventory_lines.append(f"runtime_profile={PROFILE_NAME}")
    lines: list[SourceLine] = []
    lines.extend(
        _document_lines(
            source_id="project_readme",
            path="projects/agifcore_master/PROJECT_README.md",
            tags=("project", "identity", "capability"),
            lines=(
                "AGIFCore is the canonical local AGIF system in this repo.",
                _project_goal(),
                "AGIFCore uses a governed build machine and the user is the final approver.",
                "No phase is earned until implementation, verifiers, demos, audit, validation, and explicit user approval are complete.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="master_plan",
            path="projects/agifcore_master/01_plan/MASTER_PLAN.md",
            tags=("project", "mission", "capability", "phase"),
            lines=(
                *_master_plan_goal_lines(),
                "Phase 15 builds blind packs, hidden packs, live-demo pack, soak harness, hardening package, reproducibility package, and closure audit.",
                "Phase 16 builds release notes, claims matrix, public release package, and public reproducibility package.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="human_target",
            path="projects/agifcore_master/01_plan/HUMAN_THINKING_TARGET.md",
            tags=("project", "capability"),
            lines=_human_target_lines(),
        )
    )
    lines.extend(
        _document_lines(
            source_id="phase_truth",
            path="projects/agifcore_master/01_plan/PHASE_INDEX.md",
            tags=("phase", "status", "truth"),
            lines=_latest_phase_lines(),
        )
    )
    lines.extend(
        _document_lines(
            source_id="decisions",
            path="projects/agifcore_master/DECISIONS.md",
            tags=("decision", "status", "history"),
            lines=(_latest_decision_line(),),
        )
    )
    lines.extend(
        _document_lines(
            source_id="changelog",
            path="projects/agifcore_master/CHANGELOG.md",
            tags=("changelog", "history", "status"),
            lines=_latest_change_lines(),
        )
    )
    lines.extend(
        _document_lines(
            source_id="runtime_shell_snapshot",
            path="dynamic::runtime_shell_snapshot",
            tags=("self", "system", "status", "capability"),
            lines=(
                f"Local AGIFCore runtime shell session {shell_snapshot['session_id']} is active for conversation {shell_snapshot['conversation_id']}.",
                f"Available surfaces are {', '.join(shell_snapshot['available_surfaces'])}.",
                f"Blocked surfaces are {', '.join(shell_snapshot['blocked_surface_names'])}.",
                f"Current runtime support state is {shell_snapshot['support_state']}.",
                f"UI exposes {shell_snapshot['ui_view_count']} views named {', '.join(shell_snapshot['ui_view_ids'])}.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="runtime_session_open",
            path="dynamic::session_open",
            tags=("self", "system", "status"),
            lines=(
                f"Session open exposes {', '.join(session_open['available_surfaces'])}.",
                f"Session open currently reports support state {session_open['support_state']}.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="runtime_limits",
            path="dynamic::runtime_limits",
            tags=("self", "capability", "limits", "status"),
            lines=(
                "This local shell answers only from approved AGIFCore local truth and runtime state.",
                "Unsupported or missing-local-support questions must fail closed with clarify, abstain, or search_needed.",
                "The interactive path is bounded and does not use hidden external services.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="local_clock_context",
            path="dynamic::local_clock_context",
            tags=("current", "clock", "time", "world", "estimate"),
            lines=(
                f"Local shell clock timezone is {current_world['timezone']}.",
                f"Local shell clock now is {current_world['iso_timestamp']}.",
                f"Local shell month is {current_world['month_name']} and local season is {current_world['season']}.",
                f"Local shell time band is {current_world['time_band']} and local night status is {current_world['is_night']}.",
            ),
            bucket="current_world",
            target_domain="situated_current_world_reasoning",
        )
    )
    lines.extend(
        _document_lines(
            source_id="local_world_prior",
            path="dynamic::local_world_prior",
            tags=("current", "world", "estimate", "weather", "outside"),
            lines=tuple(world_prior_lines),
            bucket="current_world",
            target_domain="situated_current_world_reasoning",
        )
    )
    lines.extend(
        _document_lines(
            source_id="phase15_artifact_inventory",
            path="dynamic::phase15_artifact_inventory",
            tags=("artifact", "bundle", "evidence", "manifest", "path", "profile", "report", "review", "runtime", "status"),
            lines=tuple(artifact_inventory_lines),
        )
    )
    if claim_boundary_path.exists():
        lines.extend(
            _document_lines(
                source_id="claim_boundary",
                path=str(claim_boundary_path.relative_to(REPO_ROOT)),
                tags=("comparison", "contradiction", "policy", "proof", "release", "support", "verification"),
                lines=_read_text(claim_boundary_path).splitlines(),
                bucket="verification_policy",
            )
        )
    if phase16_bounded_plan_path.exists():
        lines.extend(
            _document_lines(
                source_id="phase16_bounded_plan",
                path=str(phase16_bounded_plan_path.relative_to(REPO_ROOT)),
                tags=("comparison", "plan", "policy", "proof", "release", "verification"),
                lines=_read_text(phase16_bounded_plan_path).splitlines(),
                bucket="verification_policy",
            )
        )
    lines.extend(
        _document_lines(
            source_id="role_authority_rules",
            path="projects/agifcore_master/02_requirements/ROLE_AUTHORITY_RULES.md",
            tags=("verification", "plan", "phase", "truth", "review"),
            lines=_read_text(PROJECT_ROOT / "02_requirements" / "ROLE_AUTHORITY_RULES.md").splitlines(),
            bucket="verification_policy",
        )
    )
    lines.extend(
        _document_lines(
            source_id="validation_protocol",
            path="projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md",
            tags=("verification", "plan", "review", "phase", "truth"),
            lines=_read_text(PROJECT_ROOT / "01_plan" / "VALIDATION_PROTOCOL.md").splitlines(),
            bucket="verification_policy",
        )
    )
    lines.extend(
        _document_lines(
            source_id="runtime_rebuild_map",
            path="projects/agifcore_master/01_plan/RUNTIME_REBUILD_MAP.md",
            tags=("history", "comparison", "project", "lineage", "source"),
            lines=_read_text(PROJECT_ROOT / "01_plan" / "RUNTIME_REBUILD_MAP.md").splitlines(),
            bucket="project_history",
        )
    )
    if prior_turn:
        prior_refs = list(prior_turn.get("local_truth_refs", []))
        lines.extend(
            _document_lines(
                source_id="prior_turn",
                path="dynamic::prior_turn_context",
                tags=("history", "follow_up", "status"),
                lines=(
                    f"Previous turn class was {prior_turn.get('question_class', 'unknown')} with support state {prior_turn.get('support_state', 'unknown')}.",
                    f"Previous next action was {prior_turn.get('next_action', 'unknown')} and final answer mode was {prior_turn.get('final_answer_mode', 'unknown')}.",
                    f"Previous response summary: {_clean_text(str(prior_turn.get('response_text', '')))}",
                    *[f"Previous local truth ref {ref}." for ref in prior_refs[:4]],
                ),
            )
        )
    if recent_turns:
        history_lines: list[str] = []
        for offset, turn in enumerate(reversed(recent_turns[-4:]), start=1):
            history_lines.append(
                (
                    f"Recent interactive turn {offset} used question class {turn.get('question_class', 'unknown')} "
                    f"with support state {turn.get('support_state', 'unknown')} and next action {turn.get('next_action', 'unknown')}."
                )
            )
            history_lines.append(
                f"Recent interactive turn {offset} response summary: {_truncate_text(str(turn.get('response_text', '')))}"
            )
        lines.extend(
            _document_lines(
                source_id="interactive_history",
                path="dynamic::interactive_history",
                tags=("history", "follow_up", "status"),
                lines=history_lines,
            )
        )
    lines.extend(
        _document_lines(
            source_id="state_export",
            path="dynamic::state_export",
            tags=("runtime", "state", "evidence"),
            lines=(
                f"State export hash is {state_export.get('snapshot_hash', 'missing')}.",
                f"State export preserves session {state_export.get('session_id', 'missing')}.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="memory_review_export",
            path="dynamic::memory_review_export",
            tags=("runtime", "memory", "evidence"),
            lines=(
                f"Memory review export hash is {memory_review_export.get('snapshot_hash', 'missing')}.",
                f"Memory review export supports session {memory_review_export.get('session_id', 'missing')}.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="safe_shutdown",
            path="dynamic::safe_shutdown",
            tags=("runtime", "safe_shutdown", "evidence"),
            lines=(
                f"Safe shutdown receipt hash is {safe_shutdown.get('receipt_hash', 'missing')}.",
                f"Safe shutdown preserves replay readiness as {safe_shutdown.get('replay_ready', 'unknown')}.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="phase10_overlay",
            path="dynamic::phase10_overlay",
            tags=("phase10", "critique", "status"),
            lines=(
                f"Phase 10 selected outcome is {phase10_turn_state.get('overlay_contract', {}).get('selected_outcome', 'unknown')}.",
                f"Phase 10 support state is {phase10_turn_state.get('overlay_contract', {}).get('support_state', 'unknown')}.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="phase11_overlay",
            path="dynamic::phase11_overlay",
            tags=("phase11", "history", "status"),
            lines=_phase11_lines(phase11_cycle_state),
        )
    )
    lines.extend(
        _document_lines(
            source_id="phase12_overlay",
            path="dynamic::phase12_overlay",
            tags=("phase12", "history", "status"),
            lines=_phase12_lines(phase12_cycle_state),
        )
    )
    lines.extend(
        _document_lines(
            source_id="phase13_manifest",
            path=phase13_manifest["path"],
            tags=("manifest", "evidence", "phase", "status"),
            lines=(
                f"Phase 13 evidence manifest status {phase13_manifest['status']}.",
                f"Phase 13 required report count {phase13_manifest['required_report_count']} and available report count {phase13_manifest['available_report_count']}.",
                f"Phase 13 remains open is {phase13_manifest['phase_remains_open']}.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="phase14_manifest",
            path=phase14_manifest["path"],
            tags=("manifest", "evidence", "phase", "status"),
            lines=(
                f"Phase 14 evidence manifest status {phase14_manifest['status']}.",
                f"Phase 14 required report count {phase14_manifest['required_report_count']} and available report count {phase14_manifest['available_report_count']}.",
                f"Phase 14 remains open is {phase14_manifest['phase_remains_open']}.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="phase15_manifest",
            path=phase15_manifest["path"],
            tags=("manifest", "evidence", "phase", "status", "proof"),
            lines=(
                f"Phase 15 evidence manifest status {phase15_manifest['status']}.",
                f"Phase 15 required report count {phase15_manifest['required_report_count']} and available report count {phase15_manifest['available_report_count']}.",
                f"Phase 15 missing report count {len(phase15_manifest['missing_reports'])} and invalid report count {len(phase15_manifest['invalid_reports'])}.",
                f"Phase 15 remains open is {phase15_manifest['phase_remains_open']}.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="phase14_audit",
            path="dynamic::phase14_manifest_audit",
            tags=("phase14", "routing", "budget", "manifest"),
            lines=(
                f"Phase 14 cell count is {phase14_audit.get('logical_cell_count', 0)} and tissue count is {phase14_audit.get('tissue_count', 0)}.",
                f"Phase 14 manifest audit status is {phase14_audit.get('audit_status', 'unknown')}.",
                f"Phase 14 per-profile total active caps are {phase14_audit.get('per_profile_total_active_cap', {})}.",
                f"Phase 14 sandbox policy count is {phase14_shell.shell_snapshot().get('sandbox_policy_count', 0)}.",
            ),
        )
    )
    lines.extend(
        _document_lines(
            source_id="phase14_profiles",
            path="dynamic::phase14_profile_manifests",
            tags=("phase14", "profile", "budget"),
            lines=(
                f"Phase 14 profile count is {phase14_profiles.get('manifest_count', 0)}.",
                *[
                    (
                        f"Profile {profile['profile']} targets {profile['target_active_cells']} active cells "
                        f"with active cell band {profile['active_cell_band']}."
                    )
                    for profile in phase14_profiles.get("profiles", [])
                ],
            ),
        )
    )
    return lines


def _score_line(
    *,
    question_tokens: set[str],
    provisional_class: str,
    phase_numbers: tuple[int, ...],
    line: SourceLine,
) -> int:
    overlap = len(question_tokens.intersection(line.tokens))
    if overlap == 0:
        return 0
    score = overlap * 3
    if provisional_class in line.tags:
        score += 4
    if "phase" in line.tags and phase_numbers:
        lowered = line.text.lower()
        for phase in phase_numbers:
            if f"phase {phase}" in lowered:
                score += 6
    if provisional_class == "self_system_status" and "self" in line.tags:
        score += 3
    if provisional_class == "project_phase_capability" and "capability" in line.tags:
        score += 2
    if provisional_class == "local_truth_evidence" and ("manifest" in line.tags or "truth" in line.tags):
        score += 2
    if provisional_class == "local_truth_evidence" and (
        {"artifact", "bundle", "path", "profile", "report", "review"} & set(line.tags)
    ):
        score += 3
    if provisional_class == "contradiction" and "truth" in line.tags:
        score += 2
    if provisional_class in {"comparison_planning", "contradiction"} and (
        {"policy", "verification", "support"} & set(line.tags)
    ):
        score += 3
    if provisional_class == "current_world" and (
        {"current", "clock", "weather", "estimate", "outside"} & set(line.tags)
    ):
        score += 4
    return score


def _source_bucket(line: SourceLine) -> str:
    bucket = SOURCE_BUCKET_BY_ID.get(line.source_id)
    if bucket:
        return bucket
    if "truth" in line.tags or "phase" in line.tags:
        return "phase_truth"
    if "manifest" in line.tags or "evidence" in line.tags:
        return "evidence"
    if "self" in line.tags or "system" in line.tags:
        return "runtime_identity"
    if "runtime" in line.tags:
        return "runtime_state"
    if "history" in line.tags:
        return "turn_history"
    if "current" in line.tags or "weather" in line.tags:
        return "current_world"
    return "project_identity"


def _select_candidate_lines(
    *,
    question_text: str,
    provisional_class: str,
    lines: list[SourceLine],
    prior_turn: Mapping[str, Any] | None = None,
    limit: int = 16,
) -> list[tuple[int, SourceLine]]:
    tokens = _content_tokens(question_text)
    phase_numbers = _extract_phase_numbers(question_text)
    preferred_buckets = CLASS_BUCKET_PRIORITY.get(provisional_class, ("project_identity",))
    follow_up_requested = _follow_up_intent(question_text=question_text, prior_turn=prior_turn) is not None
    prior_refs = set(prior_turn.get("local_truth_refs", [])) if prior_turn else set()
    prior_sources = set(prior_turn.get("source_set_used", [])) if prior_turn else set()
    scored: list[tuple[int, SourceLine]] = []
    for line in lines:
        score = _score_line(
            question_tokens=tokens,
            provisional_class=provisional_class,
            phase_numbers=phase_numbers,
            line=line,
        )
        bucket = _source_bucket(line)
        if bucket in preferred_buckets:
            score += max(1, len(preferred_buckets) - preferred_buckets.index(bucket))
        if bucket == "turn_history" and not follow_up_requested:
            score -= 4
        if bucket == "turn_history" and follow_up_requested:
            score += 5
        if line.ref in prior_refs:
            score += 5
        if line.source_id in prior_sources:
            score += 2
        if not tokens and bucket == "turn_history":
            score += 2
        if score > 0:
            scored.append((score, line))
    scored.sort(key=lambda item: (-item[0], item[1].path, item[1].line_number))
    selected: list[tuple[int, SourceLine]] = []
    seen_refs: set[str] = set()
    source_counts: dict[str, int] = {}
    bucket_counts: dict[str, int] = {}
    for score, line in scored:
        if len(selected) >= limit:
            break
        if line.ref in seen_refs:
            continue
        bucket = _source_bucket(line)
        if source_counts.get(line.source_id, 0) >= 3:
            continue
        if len(selected) < 8 and bucket_counts.get(bucket, 0) >= 2:
            continue
        selected.append((score, line))
        seen_refs.add(line.ref)
        source_counts[line.source_id] = source_counts.get(line.source_id, 0) + 1
        bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1
    if len(selected) < min(limit, len(scored)):
        for score, line in scored:
            if len(selected) >= limit:
                break
            if line.ref in seen_refs:
                continue
            selected.append((score, line))
            seen_refs.add(line.ref)
    return selected


def _fallback_candidate_lines(
    *,
    question_class: str,
    lines: list[SourceLine],
    limit: int = 8,
) -> list[tuple[int, SourceLine]]:
    tag_priority: dict[str, tuple[str, ...]] = {
        "self_system_status": ("self", "system", "status", "identity", "capability"),
        "project_phase_capability": ("project", "mission", "capability", "phase", "status"),
        "local_truth_evidence": ("truth", "manifest", "evidence", "phase", "status"),
        "reasoning_math": ("capability", "project", "self"),
        "comparison_planning": ("verification", "plan", "comparison", "history", "phase"),
        "session_history": ("history", "status", "self"),
        "support_diagnostics": ("history", "evidence", "verification", "phase", "status"),
        "contradiction": ("truth", "phase", "status"),
        "current_world": ("current", "clock", "weather", "estimate", "outside"),
        "underspecified": ("capability", "project", "self"),
        "unsupported": ("capability", "project", "self", "status"),
    }
    preferred_tags = tag_priority.get(question_class, ("project", "capability"))
    selected: list[tuple[int, SourceLine]] = []
    seen_refs: set[str] = set()
    selected_sources: set[str] = set()
    for priority, tag in enumerate(preferred_tags, start=1):
        for line in lines:
            if line.ref in seen_refs or tag not in line.tags:
                continue
            if line.source_id in selected_sources and len(selected) < 6:
                continue
            seen_refs.add(line.ref)
            selected_sources.add(line.source_id)
            selected.append((max(1, len(preferred_tags) - priority + 1), line))
            if len(selected) >= limit:
                return selected
    for line in lines:
        if line.ref in seen_refs:
            continue
        seen_refs.add(line.ref)
        selected.append((1, line))
        if len(selected) >= limit:
            break
    return selected


def _provisional_question_class(question_text: str) -> str:
    tokens = _content_tokens(question_text)
    raw_tokens = set(_tokenize(question_text))
    phase_numbers = _extract_phase_numbers(question_text)
    current_world_kind = _current_world_request_kind(question_text)
    if not tokens:
        return "underspecified"
    if current_world_kind is not None:
        return "current_world"
    if _extract_math_expression(question_text) is not None or _is_ordering_math_request(question_text) or tokens.intersection(MATH_TOKENS):
        return "reasoning_math"
    if _looks_like_contradiction_request(question_text):
        return "contradiction"
    if _looks_like_self_system_request(question_text):
        return "self_system_status"
    if raw_tokens.intersection({"agif", "agifcore"}) and raw_tokens.intersection({"define", "describe", "explain", "what"}) and not raw_tokens.intersection(
        LOCAL_ARTIFACT_TOKENS | SUPPORT_DIAGNOSTIC_TOKENS | PHASE_TOKENS
    ):
        return "project_phase_capability"
    if "phase" in raw_tokens and raw_tokens.intersection({"what", "which", "current", "currently", "on"}) and raw_tokens.intersection(
        {"agif", "agifcore", "project", "runtime", "shell", "system", "you"}
    ):
        return "project_phase_capability"
    if raw_tokens.intersection(SESSION_HISTORY_TOKENS) and raw_tokens.intersection({"ask", "asked", "say", "said"}):
        return "session_history"
    if _looks_like_support_diagnostic_request(question_text):
        return "support_diagnostics"
    if _unsupported_request_domain(question_text) is not None:
        return "unsupported"
    if _looks_like_local_artifact_request(question_text):
        return "local_truth_evidence"
    if _extract_compare_entities(question_text) or raw_tokens.intersection(PLANNING_TOKENS | COMPARISON_TOKENS):
        return "comparison_planning"
    if raw_tokens.intersection({"why", "explain", "difference", "compare", "contrast"}) and raw_tokens.intersection(
        PROOF_RELEASE_TOKENS | PHASE_TRUTH_VERIFICATION_TOKENS | {"claim", "claims", "closed", "guess", "guessing", "policy", "proof", "release", "support"}
    ):
        return "comparison_planning"
    if _looks_like_underspecified_request(question_text):
        return "underspecified"
    if {"can", "do"} <= raw_tokens and ({"you", "runtime", "system", "agifcore", "project"} & raw_tokens):
        return "project_phase_capability"
    if phase_numbers or tokens.intersection(PHASE_TOKENS) or tokens.intersection(EVIDENCE_TOKENS):
        return "local_truth_evidence"
    if tokens.intersection(SELF_TOKENS) and ("you" in tokens or "runtime" in tokens or "session" in tokens):
        return "self_system_status"
    if tokens.intersection(PROJECT_TOKENS):
        return "project_phase_capability"
    if len(tokens) <= 2 or tokens.intersection(UNDERSPECIFIED_REFERENCE_TOKENS):
        return "underspecified"
    return "unsupported"


def _is_follow_up_request(question_text: str) -> bool:
    return _follow_up_intent(question_text=question_text, prior_turn={"turn_id": "present"}) is not None


def _bind_follow_up_class(
    *,
    question_text: str,
    derived_class: str,
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]] | None = None,
) -> tuple[str, bool, FollowUpBindingDecision]:
    binding = _build_follow_up_binding(
        question_text=question_text,
        prior_turn=prior_turn,
        recent_turns=recent_turns,
    )
    anchor_turn = binding.anchor_turn
    follow_up_intent = binding.intent
    if not binding.success or not anchor_turn or follow_up_intent is None:
        return derived_class, False, binding
    prior_support = str(anchor_turn.get("support_state", "unknown"))
    prior_next_action = str(anchor_turn.get("next_action", "abstain"))
    if follow_up_intent == "history":
        return "session_history", True, binding
    if follow_up_intent == "support":
        return "support_diagnostics", True, binding
    if follow_up_intent == "confidence":
        return "support_diagnostics", True, binding
    if follow_up_intent in {"reason", "method", "explanation"}:
        return "session_history", True, binding
    if prior_next_action in {"search_needed", "search_local"}:
        return "local_truth_evidence", True, binding
    if prior_next_action == "abstain" and prior_support == "unknown":
        return "unsupported", True, binding
    return derived_class, False, binding


def _derive_question_class(
    *,
    question_text: str,
    phase7_interpretation_state: Mapping[str, Any],
    candidate_lines: list[tuple[int, SourceLine]],
) -> str:
    tokens = _content_tokens(question_text)
    raw_tokens = set(_tokenize(question_text))
    current_world_kind = _current_world_request_kind(question_text)
    if current_world_kind is not None:
        return "current_world"
    if _extract_math_expression(question_text) is not None or _is_ordering_math_request(question_text) or raw_tokens.intersection(MATH_TOKENS):
        return "reasoning_math"
    if _looks_like_contradiction_request(question_text, phase7_interpretation_state=phase7_interpretation_state):
        return "contradiction"
    if _looks_like_self_system_request(question_text):
        return "self_system_status"
    if raw_tokens.intersection({"agif", "agifcore"}) and raw_tokens.intersection({"define", "describe", "explain", "what"}) and not raw_tokens.intersection(
        LOCAL_ARTIFACT_TOKENS | SUPPORT_DIAGNOSTIC_TOKENS | PHASE_TOKENS
    ):
        return "project_phase_capability"
    if "phase" in raw_tokens and raw_tokens.intersection({"what", "which", "current", "currently", "on"}) and raw_tokens.intersection(
        {"agif", "agifcore", "project", "runtime", "shell", "system", "you"}
    ):
        return "project_phase_capability"
    if raw_tokens.intersection(SESSION_HISTORY_TOKENS) and raw_tokens.intersection({"ask", "asked", "say", "said"}):
        return "session_history"
    if _looks_like_support_diagnostic_request(question_text) and (
        raw_tokens.intersection({"that", "this", "it", "missing", "support", "evidence"})
        or any("history" in line.tags or "evidence" in line.tags for _, line in candidate_lines[:4])
    ):
        return "support_diagnostics"
    if _unsupported_request_domain(question_text) is not None:
        return "unsupported"
    if "who" in raw_tokens and ({"you", "yourself", "system", "agifcore", "runtime"} & raw_tokens):
        return "self_system_status"
    if _looks_like_local_artifact_request(question_text):
        return "local_truth_evidence"
    if _extract_compare_entities(question_text) or (
        raw_tokens.intersection(PLANNING_TOKENS | COMPARISON_TOKENS)
        and not raw_tokens.intersection(CONTRADICTION_TOKENS - COMPARISON_TOKENS)
    ):
        return "comparison_planning"
    if raw_tokens.intersection({"why", "explain", "difference", "compare", "contrast"}) and raw_tokens.intersection(
        PROOF_RELEASE_TOKENS | PHASE_TRUTH_VERIFICATION_TOKENS | {"claim", "claims", "closed", "guess", "guessing", "policy", "proof", "release", "support"}
    ):
        return "comparison_planning"
    if _looks_like_underspecified_request(question_text):
        return "underspecified"
    if raw_tokens.intersection(LIMITATION_TOKENS):
        if raw_tokens.intersection({"runtime", "system", "agifcore", "project"}) or raw_tokens.intersection(BOUNDARY_TOKENS):
            return "project_phase_capability"
        return "unsupported"
    if {"can", "do"} <= raw_tokens and ({"you", "runtime", "system", "agifcore", "project"} & raw_tokens):
        return "project_phase_capability"
    if len(tokens) <= 2 and not (
        raw_tokens.intersection({"who", "what", "why", "how"})
        or tokens.intersection(
            PROJECT_TOKENS
            | SELF_TOKENS
            | PHASE_TOKENS
            | EVIDENCE_TOKENS
            | MATH_TOKENS
            | CURRENT_WORLD_WEATHER_TOKENS
            | CURRENT_WORLD_TIME_TOKENS
        )
    ):
        return "unsupported"
    if len(tokens) <= 1 and not (
        tokens.intersection(PROJECT_TOKENS | SELF_TOKENS | PHASE_TOKENS | EVIDENCE_TOKENS)
        or raw_tokens.intersection({"you", "yourself", "system", "runtime", "agifcore"})
    ):
        return "underspecified"
    if _extract_phase_numbers(question_text) or tokens.intersection(PHASE_TOKENS) or tokens.intersection(EVIDENCE_TOKENS):
        return "local_truth_evidence"
    if tokens.intersection(SELF_TOKENS) and (
        {"session", "surface", "surfaces", "status"} & tokens
    ):
        return "self_system_status"
    if "can" in raw_tokens and "do" in raw_tokens and (
        {"runtime", "agifcore", "project"} & raw_tokens
    ):
        return "project_phase_capability"
    if raw_tokens.intersection(BOUNDARY_TOKENS) and (
        {"you", "runtime", "system", "agifcore", "project"} & raw_tokens
        or tokens.intersection(PROJECT_TOKENS)
    ):
        return "project_phase_capability"
    if bool(phase7_interpretation_state.get("ambiguous_request")) or (
        len(tokens) <= 2 and tokens.intersection(UNDERSPECIFIED_REFERENCE_TOKENS)
    ):
        return "underspecified"
    if {"repo", "repository", "file", "path", "diff", "line", "commit", "change"} & (
        tokens | raw_tokens
    ):
        return "local_truth_evidence"
    if bool(phase7_interpretation_state.get("local_artifact_requested")):
        return "local_truth_evidence"
    if tokens.intersection(EVIDENCE_TOKENS):
        return "local_truth_evidence"
    if tokens.intersection(PROJECT_TOKENS) or any("project" in line.tags or "capability" in line.tags for _, line in candidate_lines[:4]):
        return "project_phase_capability"
    if bool(phase7_interpretation_state.get("live_current_requested")) and current_world_kind is None:
        return "unsupported"
    if not candidate_lines or max((score for score, _ in candidate_lines), default=0) < 5:
        return "unsupported"
    return "project_phase_capability"


def _profile_allows_tissue(profile: str, tissue: Mapping[str, Any]) -> bool:
    caps = dict(tissue.get("active_cell_cap_by_profile", {}))
    return int(caps.get(profile, 0)) > 0


def _build_phase3_route(
    *,
    question_class: str,
    phase14_shell: SandboxProfileRuntimeShell,
    profile: str,
) -> dict[str, Any]:
    cell_manifest = phase14_shell.cell_manifest()
    tissue_manifest = phase14_shell.tissue_manifest()
    cells_by_id = {cell["cell_id"]: cell for cell in cell_manifest["cells"]}
    family_order = ROUTE_FAMILIES.get(question_class, ROUTE_FAMILIES["unsupported"])
    ordered_tissues = sorted(
        [
            tissue
            for tissue in tissue_manifest["tissues"]
            if _profile_allows_tissue(profile, tissue) and tissue.get("focus_family") in family_order
        ],
        key=lambda tissue: (
            family_order.index(str(tissue.get("focus_family"))),
            -int(tissue.get("active_cell_cap_by_profile", {}).get(profile, 0)),
            str(tissue.get("tissue_id")),
        ),
    )
    if not ordered_tissues:
        ordered_tissues = sorted(
            [tissue for tissue in tissue_manifest["tissues"] if _profile_allows_tissue(profile, tissue)],
            key=lambda tissue: (-int(tissue.get("active_cell_cap_by_profile", {}).get(profile, 0)), str(tissue.get("tissue_id"))),
        )
    selected_tissues = ordered_tissues[:2]
    requested_cell_ids: list[str] = []
    for tissue in selected_tissues:
        candidate_ids = [
            cell_id
            for cell_id in tissue.get("cell_ids", [])
            if cell_id in cells_by_id and str(cells_by_id[cell_id].get("role_family")) in family_order
        ]
        requested_cell_ids.extend(candidate_ids[:5])
    if not requested_cell_ids and selected_tissues:
        requested_cell_ids.extend(selected_tissues[0].get("cell_ids", [])[:4])
    requested_cell_ids = list(dict.fromkeys(requested_cell_ids))[:8]
    requested_tissues = max(1, len({cells_by_id[cell_id]["primary_tissue_id"] for cell_id in requested_cell_ids if cell_id in cells_by_id}))
    budget = phase14_shell.active_cell_budget(
        profile=profile,
        requested_active_cells=max(1, len(requested_cell_ids)),
        requested_active_tissues=requested_tissues,
        requested_cell_ids=requested_cell_ids,
    )
    selected_cell_ids = list(budget.get("selected_active_cell_ids", []))
    selected_cells = [cells_by_id[cell_id] for cell_id in selected_cell_ids if cell_id in cells_by_id]
    selected_tissue_ids = list(budget.get("selected_active_tissue_ids", []))
    route_refs = [
        *[f"phase14::cell::{cell_id}" for cell_id in selected_cell_ids],
        *[f"phase14::tissue::{tissue_id}" for tissue_id in selected_tissue_ids],
        f"phase14::budget::{budget['receipt_hash']}",
    ]
    return {
        "profile": profile,
        "family_order": family_order,
        "selected_cell_ids": selected_cell_ids,
        "selected_cells": selected_cells,
        "selected_tissue_ids": selected_tissue_ids,
        "budget": budget,
        "route_refs": route_refs,
        "selected_family_counts": dict(budget.get("selected_family_counts", {})),
    }


def _continuity_specs(
    *,
    shell_snapshot: Mapping[str, Any],
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]],
) -> list[tuple[str, str, str, str, list[str], dict[str, Any]]]:
    phase14 = _phase_truth_summary(14) or "Phase 14 truth is unavailable."
    phase15 = _phase_truth_summary(15) or "Phase 15 truth is unavailable."
    specs = [
        (
            "continuity-self-runtime",
            "agifcore_runtime",
            "self_identity",
            f"I am the local AGIFCore product-runtime shell for session {shell_snapshot['session_id']}.",
            ["projects/agifcore_master/PROJECT_README.md:1", "dynamic::runtime_shell_snapshot:1"],
            {"kind": "self"},
        ),
        (
            "continuity-self-boundary",
            "agifcore_runtime",
            "self_capability",
            "I answer from approved local AGIFCore files and runtime state only, with no hidden cloud or web path.",
            ["projects/agifcore_master/01_plan/MASTER_PLAN.md:1", "projects/agifcore_master/PROJECT_README.md:1"],
            {"kind": "boundary"},
        ),
        (
            "continuity-phase-14",
            "agifcore_runtime",
            "phase_status",
            phase14,
            ["projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md:1", "projects/agifcore_master/01_plan/PHASE_INDEX.md:1"],
            {"kind": "phase_truth"},
        ),
        (
            "continuity-phase-15",
            "agifcore_runtime",
            "phase_status",
            phase15 + " Phase 16 has not started.",
            ["projects/agifcore_master/01_plan/PHASE_GATE_CHECKLIST.md:1", "projects/agifcore_master/01_plan/PHASE_INDEX.md:1"],
            {"kind": "phase_truth"},
        ),
    ]
    if prior_turn:
        prior_refs = list(_turn_local_refs(prior_turn)[:4]) or ["dynamic::prior_turn_context:1"]
        specs.extend(
            [
                (
                    "continuity-prior-turn-decision",
                    "agifcore_runtime",
                    "turn_history",
                    (
                        f"Previous interactive turn used question class {prior_turn.get('question_class', 'unknown')} "
                        f"with support state {prior_turn.get('support_state', 'unknown')} and next action {prior_turn.get('next_action', 'unknown')}."
                    ),
                    prior_refs,
                    {"kind": "follow_up"},
                ),
                (
                    "continuity-prior-turn-response",
                    "agifcore_runtime",
                    "turn_history",
                    f"Previous interactive response was: {_truncate_text(str(prior_turn.get('response_text', '')))}",
                    prior_refs,
                    {"kind": "follow_up"},
                ),
            ]
        )
    if recent_turns:
        specs.append(
            (
                "continuity-recent-turn-count",
                "agifcore_runtime",
                "turn_history",
                f"Recent interactive turn count in session memory is {len(recent_turns)}.",
                ["dynamic::interactive_history:1"],
                {"kind": "follow_up"},
            )
        )
    return specs


def _build_phase4_state(
    *,
    question_text: str,
    conversation_id: str,
    turn_id: str,
    question_class: str,
    candidate_lines: list[tuple[int, SourceLine]],
    route: Mapping[str, Any],
    shell_snapshot: Mapping[str, Any],
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]],
) -> dict[str, Any]:
    continuity = ContinuityMemoryStore()
    for anchor_id, subject, continuity_kind, statement, refs, metadata in _continuity_specs(
        shell_snapshot=shell_snapshot,
        prior_turn=prior_turn,
        recent_turns=recent_turns,
    ):
        continuity.record_anchor(
            anchor_id=anchor_id,
            subject=subject,
            continuity_kind=continuity_kind,
            statement=statement,
            provenance_refs=refs,
            metadata=metadata,
        )

    working = WorkingMemoryStore()
    working.bind_turn(
        conversation_id=conversation_id,
        turn_id=turn_id,
        task_id=f"interactive::{question_class}",
        support_refs=list(route["route_refs"]),
        scratchpad={
            "question_text": question_text,
            "question_class": question_class,
            "phase14_profile": route["profile"],
            "phase3_selected_cell_count": len(route["selected_cell_ids"]),
        },
    )

    review = MemoryReviewQueue()
    semantic = SemanticMemoryStore()
    procedural = ProceduralMemoryStore()

    semantic_candidates: list[dict[str, Any]] = []
    selected_lines = [line for _, line in candidate_lines[:8]]
    for index, line in enumerate(selected_lines, start=1):
        candidate_id = f"semantic-candidate-{index:02d}"
        working.add_support_ref(line.ref)
        working.add_candidate(
            candidate_id=candidate_id,
            candidate_kind="local_truth_line",
            target_plane="semantic",
            payload={
                "abstraction": line.text,
                "source_id": line.source_id,
                "path": line.path,
                "line_number": line.line_number,
                "target_domain": line.target_domain,
            },
            provenance_refs=[line.ref],
        )
        semantic_candidates.append(
            {
                "candidate_id": candidate_id,
                "line": line,
                "descriptor_id": f"desc-{index:02d}",
                "concept_id": f"concept-{index:02d}",
            }
        )

    procedure_specs: list[ProcedureSpec] = [
        ProcedureSpec(
            procedure_id="proc-local-truth-answer",
            procedure_name="local truth answer",
            objective="Answer from approved local AGIFCore truth when grounded support exists.",
            steps=[
                "retrieve the best local truth refs for the request",
                "keep the answer bounded to those refs",
                "state limits when support is partial",
            ],
            preconditions=["approved local support exists"],
            postconditions=["bounded local answer emitted"],
            constraints=["no web access", "no hidden model path"],
            graph_refs=["skill-local-truth-answer"],
            provenance_refs=["projects/agifcore_master/PROJECT_README.md:1"],
        ),
        ProcedureSpec(
            procedure_id="proc-local-clarify",
            procedure_name="bounded clarification",
            objective="Ask for the missing variable when the question is underspecified.",
            steps=[
                "detect the missing subject or target",
                "ask one bounded clarifying question",
                "do not invent the missing context",
            ],
            preconditions=["request is ambiguous or underspecified"],
            postconditions=["clarification request emitted"],
            constraints=["no fake answer", "one clarification question"],
            graph_refs=["skill-bounded-clarify"],
            provenance_refs=["projects/agifcore_master/01_plan/VALIDATION_PROTOCOL.md:1"],
        ),
        ProcedureSpec(
            procedure_id="proc-local-abstain",
            procedure_name="bounded abstain",
            objective="Abstain honestly when the request is unsupported by local AGIFCore truth.",
            steps=[
                "check local support",
                "do not upgrade missing support into an answer",
                "return abstain or search_needed honestly",
            ],
            preconditions=["local support is missing or external freshness is required"],
            postconditions=["bounded abstain emitted"],
            constraints=["no bluff", "no external lookup in the live turn"],
            graph_refs=["skill-bounded-abstain"],
            provenance_refs=["projects/agifcore_master/01_plan/MASTER_PLAN.md:1"],
        ),
    ]

    approved_review_refs: dict[str, str] = {}
    for index, candidate in enumerate(semantic_candidates, start=1):
        review_ref = review.submit_candidate(
            candidate_id=candidate["candidate_id"],
            source_plane="working",
            target_plane="semantic",
            candidate_kind="local_truth_line",
            proposed_tier="hot" if index <= 3 else "warm",
            payload={
                "text": candidate["line"].text,
                "source_ref": candidate["line"].ref,
            },
            provenance_refs=[candidate["line"].ref],
        )
        review.decide(
            review_ref=review_ref,
            decision="approve",
            assigned_tier="hot" if index <= 3 else "warm",
            rationale="interactive local truth candidate approved for bounded turn use",
            reviewer="phase13-live-turn",
        )
        semantic.add_entry(
            entry_id=f"semantic-entry-{index:02d}",
            concept_type="local_truth",
            abstraction=candidate["line"].text,
            provenance_refs=[candidate["line"].ref],
            review_ref=review_ref,
            source_candidate_id=candidate["candidate_id"],
            supporting_refs=[candidate["line"].ref],
            graph_refs=[candidate["descriptor_id"], candidate["concept_id"]],
            metadata={"question_class": question_class, "source_id": candidate["line"].source_id},
        )
        approved_review_refs[candidate["candidate_id"]] = review_ref

    for index, procedure in enumerate(procedure_specs, start=1):
        candidate_id = f"procedure-candidate-{index:02d}"
        working.add_candidate(
            candidate_id=candidate_id,
            candidate_kind="bounded_procedure",
            target_plane="procedural",
            payload={
                "procedure_name": procedure.procedure_name,
                "objective": procedure.objective,
                "steps": procedure.steps,
            },
            provenance_refs=procedure.provenance_refs,
        )
        review_ref = review.submit_candidate(
            candidate_id=candidate_id,
            source_plane="working",
            target_plane="procedural",
            candidate_kind="bounded_procedure",
            proposed_tier="warm",
            payload={
                "procedure_name": procedure.procedure_name,
                "objective": procedure.objective,
            },
            provenance_refs=procedure.provenance_refs,
        )
        review.decide(
            review_ref=review_ref,
            decision="approve",
            assigned_tier="warm",
            rationale="interactive bounded procedure approved for read-only turn guidance",
            reviewer="phase13-live-turn",
        )
        procedural.add_procedure(
            procedure_id=procedure.procedure_id,
            procedure_name=procedure.procedure_name,
            objective=procedure.objective,
            steps=procedure.steps,
            preconditions=procedure.preconditions,
            postconditions=procedure.postconditions,
            constraints=procedure.constraints,
            provenance_refs=procedure.provenance_refs,
            review_ref=review_ref,
            source_candidate_id=candidate_id,
            graph_refs=procedure.graph_refs,
        )

    return {
        "continuity_memory_state": continuity.export_state(),
        "working_memory_state": working.export_state(),
        "memory_review_state": review.export_state(),
        "semantic_memory_state": semantic.export_state(),
        "procedural_memory_state": procedural.export_state(),
        "semantic_candidates": semantic_candidates,
        "procedure_specs": procedure_specs,
    }


def _build_phase5_state(
    *,
    question_text: str,
    question_class: str,
    target_domain: str,
    phase4_state: Mapping[str, Any],
) -> dict[str, Any]:
    descriptor_graph = DescriptorGraphStore()
    skill_graph = SkillGraphStore()
    concept_graph = ConceptGraphStore()
    transfer_graph = TransferGraphStore()

    semantic_entries = {
        entry["entry_id"]: entry
        for entry in phase4_state["semantic_memory_state"]["entries"]
    }

    for candidate in phase4_state["semantic_candidates"]:
        line = candidate["line"]
        entry = semantic_entries[f"semantic-entry-{candidate['descriptor_id'].split('-')[-1]}"]
        review_ref = entry["review_ref"]
        descriptor_graph.add_node(
            descriptor_id=candidate["descriptor_id"],
            descriptor_type="local_truth_descriptor",
            label=line.text,
            alias_tags=list(sorted(line.tokens))[:8],
            domain_tags=[line.target_domain],
            concept_tags=list(line.tags)[:8],
            support_refs=[line.ref],
            trust_band=line.trust_band,
            policy_requirements=["route"],
            provenance_links=[
                {
                    "role": "source_memory",
                    "ref_id": entry["entry_id"],
                    "ref_kind": "semantic_entry",
                    "source_path": "phase4/semantic_memory",
                },
                {
                    "role": "review",
                    "ref_id": review_ref,
                    "ref_kind": "memory_review",
                    "source_path": "phase4/memory_review",
                },
            ],
        )
        concept_graph.add_concept(
            concept_id=candidate["concept_id"],
            concept_type="local_truth_concept",
            statement=line.text,
            theory_fragments=[line.text],
            descriptor_refs=[candidate["descriptor_id"]],
            tags=list(dict.fromkeys([*line.tags, question_class]))[:8],
            trust_band=line.trust_band,
            policy_requirements=["route"],
            provenance_links=[
                {
                    "role": "source_memory",
                    "ref_id": entry["entry_id"],
                    "ref_kind": "semantic_entry",
                    "source_path": "phase4/semantic_memory",
                },
                {
                    "role": "review",
                    "ref_id": review_ref,
                    "ref_kind": "memory_review",
                    "source_path": "phase4/memory_review",
                },
            ],
        )
        transfer_graph.record_transfer(
            transfer_id=f"transfer-{candidate['descriptor_id']}",
            source_graph="descriptor",
            source_id=candidate["descriptor_id"],
            source_domain=line.target_domain,
            target_graph="target_domain",
            target_id=line.target_domain,
            target_domain=line.target_domain,
            source_status="active",
            trust_band=line.trust_band,
            source_policy_requirements=["route"],
            requested_policy_requirements=["route"],
            allowed_target_domains=[line.target_domain],
            explicit_transfer_approval=True,
            provenance_links=[
                {
                    "role": "source_memory",
                    "ref_id": entry["entry_id"],
                    "ref_kind": "semantic_entry",
                    "source_path": "phase4/semantic_memory",
                },
                {
                    "role": "review",
                    "ref_id": review_ref,
                    "ref_kind": "memory_review",
                    "source_path": "phase4/memory_review",
                },
            ],
            baseline_support_score=min(1.0, 0.55 + (len(line.tokens) / 20.0)),
            target_support_score=0.78 if line.target_domain == DEFAULT_TARGET_DOMAIN else 0.68,
            authority_review_ref=review_ref,
        )

    skill_specs = (
        {
            "skill_id": "skill-local-truth-answer",
            "skill_name": "local truth answer",
            "objective": "answer from approved local AGIFCore truth and manifests",
            "descriptor_refs": [item["descriptor_id"] for item in phase4_state["semantic_candidates"][:4]],
            "preconditions": ["approved local support exists"],
            "postconditions": ["bounded answer emitted"],
            "constraints": ["read only", "no web"],
        },
        {
            "skill_id": "skill-bounded-clarify",
            "skill_name": "bounded clarification",
            "objective": "clarify an underspecified local request",
            "descriptor_refs": [item["descriptor_id"] for item in phase4_state["semantic_candidates"][4:6]] or [phase4_state["semantic_candidates"][0]["descriptor_id"]],
            "preconditions": ["request is ambiguous"],
            "postconditions": ["single clarification emitted"],
            "constraints": ["no fake context"],
        },
        {
            "skill_id": "skill-bounded-abstain",
            "skill_name": "bounded abstain",
            "objective": "abstain or return search_needed when local support is missing",
            "descriptor_refs": [item["descriptor_id"] for item in phase4_state["semantic_candidates"][6:8]] or [phase4_state["semantic_candidates"][0]["descriptor_id"]],
            "preconditions": ["support remains missing or external freshness is required"],
            "postconditions": ["honest fail-closed result emitted"],
            "constraints": ["no bluff", "no hidden model"],
        },
    )
    for skill_spec in skill_specs:
        skill_graph.add_skill(
            skill_id=skill_spec["skill_id"],
            skill_name=skill_spec["skill_name"],
            objective=skill_spec["objective"],
            descriptor_refs=skill_spec["descriptor_refs"],
            preconditions=skill_spec["preconditions"],
            postconditions=skill_spec["postconditions"],
            constraints=skill_spec["constraints"],
            allowed_target_domains=[target_domain],
            trust_band="reviewed",
            policy_requirements=["route"],
            provenance_links=[
                {
                    "role": "source_memory",
                    "ref_id": phase4_state["procedure_specs"][0].procedure_id,
                    "ref_kind": "procedure_entry",
                    "source_path": "phase4/procedural_memory",
                },
                {
                    "role": "review",
                    "ref_id": f"skill-review::{skill_spec['skill_id']}",
                    "ref_kind": "review",
                    "source_path": "phase5/skill_graph",
                },
            ],
        )
        for index, descriptor_ref in enumerate(skill_spec["descriptor_refs"], start=1):
            skill_graph.add_grounding(
                edge_id=f"{skill_spec['skill_id']}::grounding::{index}",
                skill_id=skill_spec["skill_id"],
                descriptor_id=descriptor_ref,
                provenance_links=[
                    {
                        "role": "review",
                        "ref_id": f"grounding-review::{skill_spec['skill_id']}::{index}",
                        "ref_kind": "review",
                        "source_path": "phase5/skill_graph",
                    }
                ],
            )

    support_selection = SupportSelectionEngine().select_from_graphs(
        query_id=f"interactive-query::{stable_hash_payload({'text': question_text, 'class': question_class})[:12]}",
        query_text=question_text,
        target_domain=target_domain,
        required_policy_requirements=["route"],
        descriptor_graph=descriptor_graph,
        skill_graph=skill_graph,
        concept_graph=concept_graph,
    )
    return {
        "descriptor_graph_state": descriptor_graph.export_state(),
        "skill_graph_state": skill_graph.export_state(),
        "concept_graph_state": concept_graph.export_state(),
        "transfer_graph_state": transfer_graph.export_state(),
        "support_selection_result": support_selection.to_dict(),
    }


def _build_phase6_state(
    *,
    phase4_state: Mapping[str, Any],
    phase5_state: Mapping[str, Any],
) -> dict[str, Any]:
    target_domain_registry = build_default_registry()
    world_model = WorldModelBuilder().build_snapshot(
        semantic_memory_state=phase4_state["semantic_memory_state"],
        procedural_memory_state=phase4_state["procedural_memory_state"],
        continuity_memory_state=phase4_state["continuity_memory_state"],
        working_memory_state=phase4_state["working_memory_state"],
        descriptor_graph_state=phase5_state["descriptor_graph_state"],
        skill_graph_state=phase5_state["skill_graph_state"],
        concept_graph_state=phase5_state["concept_graph_state"],
        transfer_graph_state=phase5_state["transfer_graph_state"],
        support_selection_result=phase5_state["support_selection_result"],
        target_domain_registry_state=target_domain_registry.export_state(),
    )
    candidate_futures = CandidateFuturePlanner().build_snapshot(world_model_state=world_model.to_dict())
    what_if_simulation = WhatIfSimulationEngine().build_snapshot(
        world_model_state=world_model.to_dict(),
        candidate_future_state=candidate_futures.to_dict(),
    )
    fault_lanes = FaultLaneEngine().build_snapshot(
        world_model_state=world_model.to_dict(),
        what_if_simulation_state=what_if_simulation.to_dict(),
    )
    pressure_lanes = PressureLaneEngine().build_snapshot(
        what_if_simulation_state=what_if_simulation.to_dict(),
        fault_lane_state=fault_lanes.to_dict(),
        working_memory_state=phase4_state["working_memory_state"],
    )
    conflict_lanes = ConflictLaneEngine().build_snapshot(
        what_if_simulation_state=what_if_simulation.to_dict(),
        pressure_lane_state=pressure_lanes.to_dict(),
        transfer_graph_state=phase5_state["transfer_graph_state"],
    )
    overload_lanes = OverloadLaneEngine().build_snapshot(
        pressure_lane_state=pressure_lanes.to_dict(),
        conflict_lane_state=conflict_lanes.to_dict(),
    )
    instrumentation = InstrumentationEngine().build_snapshot(
        world_model_state=world_model.to_dict(),
        candidate_future_state=candidate_futures.to_dict(),
        what_if_simulation_state=what_if_simulation.to_dict(),
        fault_lane_state=fault_lanes.to_dict(),
        pressure_lane_state=pressure_lanes.to_dict(),
        conflict_lane_state=conflict_lanes.to_dict(),
        overload_lane_state=overload_lanes.to_dict(),
    )
    usefulness = UsefulnessScoringEngine().build_snapshot(
        target_domain_registry_state=target_domain_registry.export_state(),
        world_model_state=world_model.to_dict(),
        candidate_future_state=candidate_futures.to_dict(),
        what_if_simulation_state=what_if_simulation.to_dict(),
        fault_lane_state=fault_lanes.to_dict(),
        pressure_lane_state=pressure_lanes.to_dict(),
        conflict_lane_state=conflict_lanes.to_dict(),
        overload_lane_state=overload_lanes.to_dict(),
        instrumentation_state=instrumentation.to_dict(),
    )
    return {
        "target_domain_registry_state": target_domain_registry.export_state(),
        "world_model_state": world_model.to_dict(),
        "candidate_future_state": candidate_futures.to_dict(),
        "what_if_simulation_state": what_if_simulation.to_dict(),
        "fault_lane_state": fault_lanes.to_dict(),
        "pressure_lane_state": pressure_lanes.to_dict(),
        "conflict_lane_state": conflict_lanes.to_dict(),
        "overload_lane_state": overload_lanes.to_dict(),
        "instrumentation_state": instrumentation.to_dict(),
        "usefulness_state": usefulness.to_dict(),
    }


def _phase7_fallback_mode(
    *,
    support_resolution_state: Mapping[str, Any],
    self_knowledge_state: Mapping[str, Any],
    clarification_state: Mapping[str, Any],
) -> P7FinalAnswerMode:
    next_action = str(support_resolution_state.get("next_action", "abstain"))
    support_state = str(support_resolution_state.get("support_state", "unknown"))
    if int(clarification_state.get("question_count", 0)) > 0:
        return P7FinalAnswerMode.CLARIFY
    if next_action in {"search_external", "search_local"}:
        return P7FinalAnswerMode.SEARCH_NEEDED
    if next_action == "abstain":
        return P7FinalAnswerMode.ABSTAIN
    if int(self_knowledge_state.get("statement_count", 0)) > 0 or support_state == "grounded":
        return P7FinalAnswerMode.GROUNDED_FACT
    return P7FinalAnswerMode.DERIVED_EXPLANATION


def _phase7_guardrail_recovery_text(
    *,
    question_class: str,
    interpretation_state: Mapping[str, Any],
    support_resolution_state: Mapping[str, Any],
    self_knowledge_state: Mapping[str, Any],
    clarification_state: Mapping[str, Any],
) -> str:
    if int(clarification_state.get("question_count", 0)) > 0:
        questions = list(clarification_state.get("questions", []))
        if questions:
            return str(questions[0].get("question_text", "I need a narrower question.")).strip()
    if int(self_knowledge_state.get("statement_count", 0)) > 0:
        statements = [
            str(item.get("statement", "")).strip()
            for item in list(self_knowledge_state.get("statements", []))
            if str(item.get("statement", "")).strip()
        ]
        if statements:
            return "From this local AGIFCore state: " + " ".join(statements[:2])

    next_action = str(support_resolution_state.get("next_action", "abstain"))
    if next_action == "search_external":
        return (
            "I can't answer that honestly from local AGIFCore state because it needs fresh external information. "
            "The correct next step is search_external."
        )
    if next_action == "search_local":
        return (
            "I don't have enough grounded local evidence in the current turn to answer directly. "
            "The correct next step is search_local."
        )
    if next_action == "abstain":
        return (
            "I don't have enough grounded local evidence to answer that honestly. "
            "The correct result is to abstain."
        )

    extracted_terms = [
        str(item).strip()
        for item in list(interpretation_state.get("extracted_terms", []))
        if str(item).strip()
    ]
    subject = " ".join(extracted_terms[:4]).strip()
    if not subject:
        subject = str(
            next(iter(support_resolution_state.get("selected_domain_ids", [])), "local runtime state")
        )
    if question_class == "self_system_status":
        return (
            f"From this local AGIFCore state, {subject} stays bounded to approved local runtime surfaces "
            "and governed routing."
        )
    return (
        f"From the local AGIFCore evidence about {subject}, support stays bounded, local-only, and honest about limits."
    )


def _build_phase7_state(
    *,
    question_text: str,
    question_class: str,
    conversation_id: str,
    turn_id: str,
    active_context_refs: list[str],
    phase4_state: Mapping[str, Any],
    phase5_state: Mapping[str, Any],
    phase6_state: Mapping[str, Any],
) -> dict[str, Any]:
    phase7_engine = ConversationTurnEngine()
    intake = phase7_engine.intake.build_record(
        conversation_id=conversation_id,
        turn_id=turn_id,
        raw_text=question_text,
        active_context_refs=active_context_refs,
    )
    interpretation = phase7_engine.interpretation.build_snapshot(intake_record=intake)
    support_resolution = phase7_engine.support_state.build_resolution(
        question_interpretation_state=interpretation.to_dict(),
        continuity_memory_state=phase4_state["continuity_memory_state"],
        memory_review_state=phase4_state["memory_review_state"],
        support_selection_result=phase5_state["support_selection_result"],
        world_model_state=phase6_state["world_model_state"],
        what_if_simulation_state=phase6_state["what_if_simulation_state"],
        conflict_lane_state=phase6_state["conflict_lane_state"],
        usefulness_state=phase6_state["usefulness_state"],
    )
    self_knowledge = phase7_engine.self_knowledge.build_snapshot(
        question_interpretation_state=interpretation.to_dict(),
        support_state_resolution_state=support_resolution.to_dict(),
        continuity_memory_state=phase4_state["continuity_memory_state"],
    )
    clarification = phase7_engine.clarification.build_request(
        question_interpretation_state=interpretation.to_dict(),
        support_state_resolution_state=support_resolution.to_dict(),
    )
    utterance_plan = phase7_engine.planner.build_plan(
        question_interpretation_state=interpretation.to_dict(),
        support_state_resolution_state=support_resolution.to_dict(),
        self_knowledge_state=self_knowledge.to_dict(),
        clarification_state=clarification.to_dict(),
    )
    draft = phase7_engine.realizer.build_draft(
        question_interpretation_state=interpretation.to_dict(),
        support_state_resolution_state=support_resolution.to_dict(),
        self_knowledge_state=self_knowledge.to_dict(),
        clarification_state=clarification.to_dict(),
        utterance_plan_state=utterance_plan.to_dict(),
    )
    cited_refs = tuple(str(item) for item in draft.cited_evidence_refs)
    try:
        guardrail_result = phase7_engine.guardrails.enforce(
            question_interpretation_state=interpretation.to_dict(),
            support_state_resolution_state=support_resolution.to_dict(),
            self_knowledge_state=self_knowledge.to_dict(),
            clarification_state=clarification.to_dict(),
            realization_draft=draft,
        ).to_dict()
        response_text = str(guardrail_result["output_text"])
        final_answer_mode = draft.final_answer_mode
    except AntiGenericFillerError:
        response_text = _phase7_guardrail_recovery_text(
            question_class=question_class,
            interpretation_state=interpretation.to_dict(),
            support_resolution_state=support_resolution.to_dict(),
            self_knowledge_state=self_knowledge.to_dict(),
            clarification_state=clarification.to_dict(),
        )
        final_answer_mode = _phase7_fallback_mode(
            support_resolution_state=support_resolution.to_dict(),
            self_knowledge_state=self_knowledge.to_dict(),
            clarification_state=clarification.to_dict(),
        )
        guardrail_payload = {
            "schema": "agifcore.phase_07.anti_generic_filler.v1",
            "status": "fallback_applied",
            "fallback_action": str(support_resolution.next_action.value),
            "output_text": response_text,
            "violations": [
                {
                    "violation_id": f"violation::{stable_hash_payload({'turn_id': turn_id, 'reason': 'interactive_guardrail_recovery'})[:12]}",
                    "reason_code": "interactive_guardrail_recovery",
                    "detail": "interactive live turn recovered from a generic Phase 7 draft without bypassing Phase 7 routing",
                    "violation_hash": stable_hash_payload(
                        {"turn_id": turn_id, "reason_code": "interactive_guardrail_recovery"}
                    ),
                }
            ],
        }
        guardrail_result = {
            **guardrail_payload,
            "guardrail_hash": stable_hash_payload(guardrail_payload),
        }
    response_surface = P7ResponseSurface(
        response_id=f"response::{stable_hash_payload({'turn_id': turn_id, 'response_text': response_text})[:12]}",
        response_text=response_text,
        final_answer_mode=final_answer_mode,
        cited_evidence_refs=cited_refs,
        response_hash=stable_hash_payload(
            {
                "response_text": response_text,
                "final_answer_mode": final_answer_mode.value,
                "cited_evidence_refs": list(cited_refs),
            }
        ),
    )
    answer_contract = phase7_engine.answer_contract.build(
        intake_state=intake.to_dict(),
        question_interpretation_state=interpretation.to_dict(),
        support_state_resolution_state=support_resolution.to_dict(),
        utterance_plan_state=utterance_plan.to_dict(),
        response_surface=response_surface,
    )
    return {
        "intake": intake.to_dict(),
        "interpretation": interpretation.to_dict(),
        "support_resolution": support_resolution.to_dict(),
        "self_knowledge": self_knowledge.to_dict(),
        "clarification": clarification.to_dict(),
        "utterance_plan": utterance_plan.to_dict(),
        "response_surface": response_surface.to_dict(),
        "guardrail_result": guardrail_result,
        "answer_contract": answer_contract.to_dict(),
    }


def _selected_support_lines(
    *,
    candidate_lines: list[tuple[int, SourceLine]],
    phase5_state: Mapping[str, Any],
    phase4_state: Mapping[str, Any],
) -> list[tuple[int, SourceLine]]:
    line_by_descriptor = {
        candidate["descriptor_id"]: candidate["line"]
        for candidate in phase4_state["semantic_candidates"]
    }
    selected: list[tuple[int, SourceLine]] = []
    seen_refs: set[str] = set()
    ranked_candidates = phase5_state["support_selection_result"].get("ranked_candidates", [])
    for candidate in ranked_candidates:
        candidate_id = str(candidate.get("candidate_id", ""))
        layer, _, entity_id = candidate_id.partition("::")
        line = None
        if layer == "descriptor":
            line = line_by_descriptor.get(entity_id)
        elif layer == "concept":
            for semantic_candidate in phase4_state["semantic_candidates"]:
                if semantic_candidate["concept_id"] == entity_id:
                    line = semantic_candidate["line"]
                    break
        if line is None or line.ref in seen_refs:
            continue
        seen_refs.add(line.ref)
        selected.append((int(round(float(candidate.get("selection_score", 0.0)) * 10)), line))
    for score, line in candidate_lines:
        if line.ref in seen_refs:
            continue
        seen_refs.add(line.ref)
        selected.append((score, line))
        if len(selected) >= 8:
            break
    return selected[:8]


def _p2_discourse_mode(value: str) -> P2DiscourseMode:
    try:
        return P2DiscourseMode(value)
    except Exception:
        return P2DiscourseMode.EXPLAIN


def _p2_support_state(value: str) -> P2SupportState:
    try:
        return P2SupportState(value)
    except Exception:
        return P2SupportState.UNKNOWN


def _p2_gap_reason(value: str) -> P2KnowledgeGapReason:
    try:
        return P2KnowledgeGapReason(value)
    except Exception:
        return P2KnowledgeGapReason.MISSING_LOCAL_EVIDENCE


def _p2_next_action(value: str) -> P2NextAction:
    normalized = value.replace("search_needed", "search_external")
    if normalized == "search_local":
        return P2NextAction.SEARCH_LOCAL
    if normalized == "search_external":
        return P2NextAction.SEARCH_EXTERNAL
    if normalized == "clarify":
        return P2NextAction.CLARIFY
    if normalized == "answer":
        return P2NextAction.ANSWER
    return P2NextAction.ABSTAIN


def _p2_final_answer_mode(value: str) -> P2FinalAnswerMode:
    try:
        return P2FinalAnswerMode(value)
    except Exception:
        return P2FinalAnswerMode.UNKNOWN


def _direct_phase_truth_answer(question_text: str) -> dict[str, str] | None:
    tokens = _content_tokens(question_text)
    phase_numbers = _extract_phase_numbers(question_text)
    if not phase_numbers:
        return None
    parts: list[str] = []
    for phase in phase_numbers:
        summary = _phase_truth_summary(phase)
        if summary:
            parts.append(summary)
    if not parts:
        return None
    text = " ".join(parts)
    if "complete" in tokens or "completed" in tokens:
        text += " In AGIFCore, an open phase is not complete."
    return {
        "response_text": text,
        "support_state": "grounded",
        "knowledge_gap_reason": "none",
        "next_action": "answer",
        "final_answer_mode": "grounded_fact",
        "response_kind": "bounded_answer",
    }


def _support_excerpt(
    support_lines: list[tuple[int, SourceLine]],
    *,
    limit: int = 2,
) -> str | None:
    excerpt = " ".join(line.text for _, line in support_lines[:limit]).strip()
    return excerpt or None


def _support_source_ids(
    support_lines: list[tuple[int, SourceLine]],
) -> tuple[str, ...]:
    source_ids: list[str] = []
    seen: set[str] = set()
    for _, line in support_lines:
        if line.source_id in seen:
            continue
        seen.add(line.source_id)
        source_ids.append(line.source_id)
    return tuple(source_ids)


def _short_plan_from_support(
    support_lines: list[tuple[int, SourceLine]],
    *,
    limit: int = 3,
) -> str | None:
    steps: list[str] = []
    seen: set[str] = set()
    for _, line in support_lines:
        text = _clean_text(line.text).rstrip(".")
        if not text or text in seen:
            continue
        seen.add(text)
        steps.append(f"{len(steps) + 1}. {text}.")
        if len(steps) >= limit:
            break
    return " ".join(steps) if steps else None


def _external_request_scope(question_text: str) -> str | None:
    raw_tokens = set(_tokenize(question_text))
    tokens = _content_tokens(question_text)
    local_scope_tokens = PROJECT_TOKENS | PHASE_TOKENS | EVIDENCE_TOKENS | SELF_TOKENS | {"runtime", "session"}
    if tokens.intersection(local_scope_tokens):
        return None
    if raw_tokens.intersection(FINANCE_TOKENS):
        return "finance"
    if _current_world_request_kind(question_text) is not None:
        return "current_world"
    if "who" in raw_tokens and raw_tokens.intersection(USER_IDENTITY_TOKENS):
        return "personal_identity"
    if raw_tokens.intersection(WORLD_KNOWLEDGE_TOKENS):
        return "world_fact"
    return None


def _answer_self_system(
    *,
    question_text: str,
    shell_snapshot: Mapping[str, Any],
    route: Mapping[str, Any],
    self_knowledge_state: Mapping[str, Any],
    support_lines: list[tuple[int, SourceLine]],
) -> dict[str, str]:
    tokens = _content_tokens(question_text)
    raw_tokens = set(_tokenize(question_text))
    if "who" in tokens and tokens.intersection(USER_IDENTITY_TOKENS):
        return {
            "response_text": "I do not have local proof of your personal identity. I only know there is a user operating this local AGIFCore session.",
            "support_state": "unknown",
            "knowledge_gap_reason": "missing_local_evidence",
            "next_action": "abstain",
            "final_answer_mode": "unknown",
            "response_kind": "fail_closed_unknown",
        }
    statements = [item["statement"] for item in self_knowledge_state.get("statements", [])]
    if "surface" in tokens or "surfaces" in tokens or "available" in tokens:
        response_text = (
            f"The local runtime currently exposes {', '.join(shell_snapshot['available_surfaces'])}. "
            f"The live path is routed through {len(route['selected_cell_ids'])} active Phase 14-governed cells under the `{route['profile']}` profile."
        )
    elif raw_tokens.intersection(ORIGIN_TOKENS):
        support_excerpt = _support_excerpt(support_lines, limit=2)
        response_text = (
            f"{support_excerpt} I do not see an approved local record naming a personal inventor for this runtime shell."
            if support_excerpt
            else "The approved local truth identifies this as the AGIFCore runtime shell inside the AGIFCore repo. I do not see an approved local record naming a personal inventor for it."
        )
    elif raw_tokens.intersection(LIMITATION_TOKENS):
        response_text = (
            _support_excerpt(support_lines, limit=2)
            or "This local shell is bounded by approved AGIFCore local truth. When support is weak, it should clarify, abstain, or search_needed instead of bluffing."
        )
    elif support_lines:
        response_text = _support_excerpt(support_lines, limit=2) or (
            statements[0] if statements else f"I am the local AGIFCore runtime shell for session {shell_snapshot['session_id']}."
        )
    else:
        core = statements[0] if statements else f"I am the local AGIFCore runtime shell for session {shell_snapshot['session_id']}."
        response_text = core + " I answer from approved local AGIFCore files and runtime state only."
    return {
        "response_text": response_text,
        "support_state": "grounded",
        "knowledge_gap_reason": "none",
        "next_action": "answer",
        "final_answer_mode": "grounded_fact",
        "response_kind": "bounded_answer",
    }


def _answer_project_capability(
    *,
    question_text: str,
    shell_snapshot: Mapping[str, Any],
    support_lines: list[tuple[int, SourceLine]],
) -> dict[str, str]:
    tokens = _content_tokens(question_text)
    raw_tokens = set(_tokenize(question_text))
    approved = [str(phase) for phase, row in _phase_gate_rows().items() if row["status"] == "approved"]
    open_phases = [str(phase) for phase, row in _phase_gate_rows().items() if row["status"] == "open"]
    if {"agif", "agifcore"} & (tokens | raw_tokens) and not (
        {"phase", "approved", "open", "complete", "completed"} & tokens
    ):
        response_text = (
            "AGIFCore is the canonical local AGIF system in this repo. "
            f"{_project_goal()} {_master_plan_goal_lines()[0]}"
        )
        final_mode = "derived_explanation"
        support_state = "grounded"
    elif {"can", "do"} <= raw_tokens and ("not" in raw_tokens or raw_tokens.intersection(LIMITATION_TOKENS | BOUNDARY_TOKENS)):
        response_text = (
            "This local shell cannot use hidden cloud or web knowledge, cannot approve its own phase, and cannot bluff when support is weak. "
            "It stays bounded to approved local AGIFCore truth, manifests, evidence, and runtime state."
        )
        final_mode = "grounded_fact"
        support_state = "grounded"
    elif "capability" in tokens or ("can" in raw_tokens and "do" in raw_tokens):
        support_excerpt = _support_excerpt(support_lines, limit=1)
        if support_excerpt and "hash" in support_excerpt.lower():
            support_excerpt = None
        response_text = (
            f"{support_excerpt} Available runtime surfaces: {', '.join(shell_snapshot['available_surfaces'])}."
            if support_excerpt
            else f"Available runtime surfaces: {', '.join(shell_snapshot['available_surfaces'])}."
        )
        final_mode = "grounded_fact"
        support_state = "grounded"
    elif "phase" in tokens or "approved" in tokens or "open" in tokens:
        response_text = (
            f"Approved phases are {', '.join(approved)}. Open phases are {', '.join(open_phases)}. "
            "Phase 15 remains open and Phase 16 has not started."
        )
        final_mode = "grounded_fact"
        support_state = "grounded"
    elif support_lines:
        response_text = _support_excerpt(support_lines, limit=2) or _project_goal()
        final_mode = "derived_explanation"
        support_state = "inferred"
    else:
        response_text = (
            f"AGIFCore is the canonical local AGIF system in this repo. {_project_goal()} "
            f"{_master_plan_goal_lines()[0]} "
            "The current live shell is bounded, local, auditable, and honest about support limits."
        )
        final_mode = "derived_explanation"
        support_state = "inferred"
    return {
        "response_text": response_text,
        "support_state": support_state,
        "knowledge_gap_reason": "none" if support_state != "unknown" else "missing_local_evidence",
        "next_action": "answer",
        "final_answer_mode": final_mode,
        "response_kind": "bounded_answer",
    }


def _answer_local_truth(
    *,
    question_text: str,
    support_lines: list[tuple[int, SourceLine]],
) -> dict[str, str]:
    raw_tokens = set(_tokenize(question_text))
    phase_numbers = _extract_phase_numbers(question_text)
    support_excerpt = _support_excerpt(support_lines, limit=2)
    source_ids = set(_support_source_ids(support_lines))
    if raw_tokens.intersection({"claim", "claimed", "closed"}) and phase_numbers:
        parts: list[str] = []
        for phase in phase_numbers:
            summary = _phase_truth_summary(phase)
            if summary:
                parts.append(summary)
        response_text = " ".join(parts)
        if 16 in phase_numbers:
            response_text += " Phase 16 is not closed, so claiming it closed would be false."
        return {
            "response_text": response_text,
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "grounded_fact",
            "response_kind": "bounded_answer",
        }
    direct_truth = _direct_phase_truth_answer(question_text)
    if direct_truth is not None:
        return direct_truth
    if raw_tokens.intersection(GOVERNANCE_HISTORY_TOKENS):
        if support_excerpt:
            return {
                "response_text": support_excerpt,
                "support_state": "grounded",
                "knowledge_gap_reason": "none",
                "next_action": "answer",
                "final_answer_mode": "derived_explanation",
                "response_kind": "bounded_answer",
            }
        response_text = (
            f"Latest decision entry: {_latest_decision_line()} "
            f"Latest change notes include: {'; '.join(_latest_change_lines()[:3])}."
        )
        return {
            "response_text": response_text,
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "grounded_fact",
            "response_kind": "bounded_answer",
        }
    if raw_tokens.intersection({"diff", "line", "commit", "git"}):
        return {
            "response_text": "I do not have local git history wired into the bounded live turn path. The honest result is search_needed on local repo state.",
            "support_state": "search_needed",
            "knowledge_gap_reason": "missing_local_evidence",
            "next_action": "search_needed",
            "final_answer_mode": "search_needed",
            "response_kind": "guided_search",
        }
    if support_lines:
        final_mode = "derived_explanation"
        if source_ids.intersection({"phase13_manifest", "phase14_manifest", "phase15_manifest", "phase15_artifact_inventory"}):
            final_mode = "grounded_fact"
        return {
            "response_text": support_excerpt or "I need a narrower local artifact target.",
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": final_mode,
            "response_kind": "bounded_answer",
        }
    if phase_numbers:
        target_phase = phase_numbers[0]
        try:
            manifest = _evidence_manifest_summary(target_phase)
        except ValueError:
            manifest = None
        if manifest is not None:
            return {
                "response_text": (
                    f"Phase {target_phase} evidence manifest status is `{manifest['status']}`. "
                    f"It requires {manifest['required_report_count']} reports and currently has {manifest['available_report_count']}. "
                    f"Missing reports: {len(manifest['missing_reports'])}. Invalid reports: {len(manifest['invalid_reports'])}."
                ),
                "support_state": "grounded",
                "knowledge_gap_reason": "none",
                "next_action": "answer",
                "final_answer_mode": "grounded_fact",
                "response_kind": "bounded_answer",
            }
    return {
        "response_text": "This looks AGIFCore-related, but I do not have enough direct local support in the current bounded live turn. Narrow the phase, report, or artifact.",
        "support_state": "search_needed",
        "knowledge_gap_reason": "missing_local_evidence",
        "next_action": "search_needed",
        "final_answer_mode": "search_needed",
        "response_kind": "guided_search",
    }


def _answer_reasoning_math(question_text: str) -> dict[str, str]:
    expression = _extract_math_expression(question_text)
    raw_tokens = set(_tokenize(question_text))
    numbers = _numeric_literals(question_text)
    if expression is None and len(numbers) >= 2 and raw_tokens.intersection(ORDERING_MATH_TOKENS):
        left, right = numbers[0], numbers[1]
        if left == right:
            response_text = f"Bounded local comparison: {int(left) if left.is_integer() else left} and {int(right) if right.is_integer() else right} are equal."
        else:
            larger = left if left > right else right
            smaller = right if left > right else left
            response_text = (
                f"Bounded local comparison: {int(larger) if float(larger).is_integer() else larger} is larger than "
                f"{int(smaller) if float(smaller).is_integer() else smaller}."
            )
        return {
            "response_text": response_text,
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "grounded_fact",
            "response_kind": "bounded_answer",
        }
    if expression is None:
        return {
            "response_text": "I can help with bounded local arithmetic if you give me the expression or math problem to solve.",
            "support_state": "unknown",
            "knowledge_gap_reason": "ambiguous_request",
            "next_action": "clarify",
            "final_answer_mode": "clarify",
            "response_kind": "guided_clarification",
        }
    result = _safe_eval_math_expression(expression)
    if result is None:
        return {
            "response_text": "I could not safely parse that arithmetic request in the current bounded math path.",
            "support_state": "unknown",
            "knowledge_gap_reason": "missing_local_evidence",
            "next_action": "abstain",
            "final_answer_mode": "unknown",
            "response_kind": "fail_closed_unknown",
        }
    return {
        "response_text": f"Bounded local computation: {expression} = {result}.",
        "support_state": "grounded",
        "knowledge_gap_reason": "none",
        "next_action": "answer",
        "final_answer_mode": "grounded_fact",
        "response_kind": "bounded_answer",
    }


def _comparison_topic(
    *,
    question_text: str,
    comparison: tuple[str, str] | None,
) -> str | None:
    raw_tokens = set(_tokenize(question_text))
    if raw_tokens.intersection(PLANNING_TOKENS) and raw_tokens.intersection(PHASE_TRUTH_VERIFICATION_TOKENS):
        return "planning"
    if comparison is not None:
        return "entity_comparison"
    if raw_tokens.intersection(COMPARISON_TOKENS | {"explain", "why"}):
        return "policy_explanation"
    return None


def _entity_support_lines(
    *,
    entity: str,
    support_lines: list[tuple[int, SourceLine]],
) -> list[SourceLine]:
    entity_tokens = _content_tokens(entity)
    if not entity_tokens:
        return []
    return [line for _, line in support_lines if entity_tokens.intersection(line.tokens)]


def _answer_comparison_planning(
    *,
    question_text: str,
    support_lines: list[tuple[int, SourceLine]],
) -> dict[str, str]:
    comparison = _extract_compare_entities(question_text)
    topic = _comparison_topic(question_text=question_text, comparison=comparison)
    if comparison is not None:
        left, right = comparison
        left_lines = _entity_support_lines(entity=left, support_lines=support_lines)
        right_lines = _entity_support_lines(entity=right, support_lines=support_lines)
        comparison_lines = [*left_lines[:2], *[line for line in right_lines if line not in left_lines][:2]]
        if comparison_lines:
            left_summary = left_lines[0].text if left_lines else None
            right_summary = right_lines[0].text if right_lines else None
            if left_summary and right_summary:
                summary = f"{left}: {left_summary} {right}: {right_summary}"
            else:
                summary = " ".join(line.text for line in comparison_lines[:3])
            response_text = (
                f"Bounded local comparison for {left} and {right}: "
                f"{summary}"
            )
            return {
                "response_text": response_text,
                "support_state": "inferred",
                "knowledge_gap_reason": "none",
                "next_action": "answer",
                "final_answer_mode": "derived_explanation",
                "response_kind": "bounded_answer",
            }
        return {
            "response_text": f"I need stronger approved local support to compare {left} and {right} honestly in this shell.",
            "support_state": "search_needed",
            "knowledge_gap_reason": "missing_local_evidence",
            "next_action": "search_needed",
            "final_answer_mode": "search_needed",
            "response_kind": "guided_search",
        }
    if topic == "planning" and support_lines:
        plan_text = _short_plan_from_support(support_lines, limit=3)
        if plan_text:
            return {
                "response_text": f"Bounded local plan: {plan_text}",
                "support_state": "grounded",
                "knowledge_gap_reason": "none",
                "next_action": "answer",
                "final_answer_mode": "derived_explanation",
                "response_kind": "bounded_answer",
            }
    if support_lines:
        return {
            "response_text": _support_excerpt(support_lines, limit=2) or "I need a narrower comparison or planning target.",
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "derived_explanation",
            "response_kind": "bounded_answer",
        }
    return {
        "response_text": "I need a narrower comparison or planning target to answer that honestly.",
        "support_state": "unknown",
        "knowledge_gap_reason": "ambiguous_request",
        "next_action": "clarify",
        "final_answer_mode": "clarify",
        "response_kind": "guided_clarification",
    }


def _answer_session_history(
    *,
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]],
) -> dict[str, str]:
    if prior_turn and str(prior_turn.get("question_text", "")).strip():
        return {
            "response_text": f"Your previous question was: {str(prior_turn['question_text']).strip()}",
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "grounded_fact",
            "response_kind": "bounded_answer",
        }
    if recent_turns:
        last_turn = recent_turns[-1]
        question_text = str(last_turn.get("question_text", "")).strip()
        if question_text:
            return {
                "response_text": f"The most recent stored question in this session was: {question_text}",
                "support_state": "grounded",
                "knowledge_gap_reason": "none",
                "next_action": "answer",
                "final_answer_mode": "grounded_fact",
                "response_kind": "bounded_answer",
            }
    return {
        "response_text": "I do not have a prior user question stored yet in this interactive session.",
        "support_state": "unknown",
        "knowledge_gap_reason": "missing_local_evidence",
        "next_action": "abstain",
        "final_answer_mode": "unknown",
        "response_kind": "fail_closed_unknown",
    }


def _answer_support_diagnostics(
    *,
    question_text: str,
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]] | None = None,
) -> dict[str, str]:
    anchor_turn = _anchor_turn(prior_turn=prior_turn, recent_turns=recent_turns)
    raw_tokens = set(_tokenize(question_text))
    if not anchor_turn:
        if raw_tokens.intersection({"evidence", "support", "proof"}):
            return {
                "response_text": "There is no prior claim stored yet for this session, so I cannot point back to one answer. In this shell, bounded support comes from local manifests, evidence reports, validation surfaces, and runtime state.",
                "support_state": "grounded",
                "knowledge_gap_reason": "none",
                "next_action": "answer",
                "final_answer_mode": "grounded_fact",
                "response_kind": "bounded_answer",
            }
        return {
            "response_text": "I need a prior turn to explain what support was used or what support was missing.",
            "support_state": "unknown",
            "knowledge_gap_reason": "ambiguous_request",
            "next_action": "clarify",
            "final_answer_mode": "clarify",
            "response_kind": "guided_clarification",
        }
    prior_support = str(anchor_turn.get("support_state", "unknown"))
    prior_next = str(anchor_turn.get("next_action", "abstain"))
    prior_refs = [str(ref) for ref in anchor_turn.get("local_truth_refs", [])]
    refs_text = ", ".join(prior_refs[:4]) if prior_refs else "no local refs recorded"
    if "missing" in raw_tokens:
        if prior_next == "answer" and prior_support in {"grounded", "inferred"}:
            return {
                "response_text": "No critical support was missing for the previous bounded answer. The remaining uncertainty was already reflected in its support state and answer mode.",
                "support_state": "grounded",
                "knowledge_gap_reason": "none",
                "next_action": "answer",
                "final_answer_mode": "grounded_fact",
                "response_kind": "bounded_answer",
            }
        if prior_next == "search_needed":
            return {
                "response_text": "The missing support was fresh or unavailable local evidence. The previous turn needed a deeper local search or fresher information than this shell had loaded.",
                "support_state": "grounded",
                "knowledge_gap_reason": "none",
                "next_action": "answer",
                "final_answer_mode": "grounded_fact",
                "response_kind": "bounded_answer",
            }
        return {
            "response_text": f"The previous turn was missing enough approved local support to avoid bluffing. It stayed fail-closed with support state {prior_support} and next action {prior_next}.",
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "grounded_fact",
            "response_kind": "bounded_answer",
        }
    if raw_tokens.intersection({"evidence", "support", "proof"}) and prior_refs:
        return {
            "response_text": f"The previous answer was supported by these local refs: {refs_text}.",
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "grounded_fact",
            "response_kind": "bounded_answer",
        }
    return {
        "response_text": f"Prior-turn support state was {prior_support}, next action was {prior_next}, and cited refs were {refs_text}.",
        "support_state": "grounded",
        "knowledge_gap_reason": "none",
        "next_action": "answer",
        "final_answer_mode": "grounded_fact",
        "response_kind": "bounded_answer",
    }


def _answer_contradiction(
    *,
    question_text: str,
    support_lines: list[tuple[int, SourceLine]],
) -> dict[str, str]:
    phase_numbers = _extract_phase_numbers(question_text)
    raw_tokens = set(_tokenize(question_text))
    support_excerpt = _support_excerpt(support_lines, limit=2)
    if phase_numbers and len(raw_tokens.intersection(STATUS_TRUTH_TOKENS)) >= 2:
        findings: list[str] = []
        mismatches: list[str] = []
        for phase in phase_numbers:
            index_row = _phase_index_rows().get(phase)
            gate_row = _phase_gate_rows().get(phase)
            if not index_row or not gate_row:
                findings.append(f"Phase {phase} is missing from one of the live truth files.")
                continue
            if index_row["status"] != gate_row["status"]:
                mismatches.append(
                    f"Phase {phase} mismatches: phase index says `{index_row['status']}` but gate checklist says `{gate_row['status']}`."
                )
            else:
                findings.append(
                    f"Phase {phase} is `{gate_row['status']}` in both the phase index and the gate checklist, so the contradictory premise is false."
                )
        response_text = " ".join(mismatches or findings)
        return {
            "response_text": response_text,
            "support_state": "grounded" if response_text else "unknown",
            "knowledge_gap_reason": "none" if response_text else "missing_local_evidence",
            "next_action": "answer" if response_text else "abstain",
            "final_answer_mode": "grounded_fact" if response_text else "unknown",
            "response_kind": "bounded_answer" if response_text else "fail_closed_unknown",
        }
    if support_lines:
        return {
            "response_text": support_excerpt or "Local bounded policy requires contradiction checks to stay support-driven and honest about mismatch risk.",
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "derived_explanation",
            "response_kind": "bounded_answer",
        }
    return {
        "response_text": "I can see a contradiction-style request, but I need the exact phase, file, or claim you want compared so I can resolve it from local truth instead of guessing.",
        "support_state": "unknown",
        "knowledge_gap_reason": "ambiguous_request",
        "next_action": "clarify",
        "final_answer_mode": "clarify",
        "response_kind": "guided_clarification",
    }


def _answer_current_world(question_text: str) -> dict[str, Any]:
    raw_tokens = set(_tokenize(question_text))
    context = _local_current_world_context()
    location = _current_world_location(question_text)
    time_request = bool(raw_tokens.intersection(CURRENT_WORLD_TIME_TOKENS))
    weather_request = bool(raw_tokens.intersection(CURRENT_WORLD_WEATHER_TOKENS))
    target_meta = {
        "extracted_target": location["label"],
        "target_grounded": bool(location["grounded"]),
    }
    if weather_request and location["supported"] and location["estimate_allowed"]:
        prior = location["prior"]
        climate = CLIMATE_PRIOR_PROFILES[str(prior["climate_profile"])][str(context["season"])]
        exact_measurement_requested = bool(raw_tokens.intersection(CURRENT_WORLD_PRECISE_TOKENS))
        if exact_measurement_requested:
            return {
                "response_text": (
                    f"I do not have a live measurement for {location['label']}, so an exact current weather reading "
                    "would be misleading. I can only offer a bounded estimate, and here the request is too precise."
                ),
                "support_state": "unknown",
                "knowledge_gap_reason": "needs_fresh_information",
                "next_action": "abstain",
                "final_answer_mode": "unknown",
                "response_kind": "fail_closed_unknown",
                "answer_mode": "abstain",
                "uncertainty_band": "high",
                "live_measurement_required": True,
                **target_meta,
            }
        if {"cold", "cool", "hot", "warm", "outside"} & raw_tokens:
            response_text = (
                f"Bounded estimate only: in {location['label']} during {context['month_name']} "
                f"{context['time_band'].replace('_', ' ')}, outside conditions are {climate['outdoor']}. "
                "Treat that as an estimate with medium uncertainty, not a fact."
            )
        else:
            response_text = (
                f"Bounded estimate only: in {location['label']} during {context['month_name']} the weather is usually "
                f"{climate['general']}, and at {context['time_band'].replace('_', ' ')} it is often {climate['outdoor']}. "
                f"{climate['sky'].capitalize()}. Exact current conditions still require live measurement."
            )
        return {
            "response_text": response_text,
            "support_state": "inferred",
            "knowledge_gap_reason": "needs_fresh_information",
            "next_action": "answer",
            "final_answer_mode": "derived_estimate",
            "response_kind": "bounded_estimate",
            "answer_mode": "bounded_estimate",
            "uncertainty_band": "medium",
            "live_measurement_required": True,
            **target_meta,
        }
    if time_request and "night" in raw_tokens:
        return {
            "response_text": (
                f"{'Yes' if context['is_night'] else 'No'}. In the local shell timezone "
                f"{context['timezone']}, it is currently {context['time']} and the time band is "
                f"{context['time_band'].replace('_', ' ')}."
            ),
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "grounded_fact",
            "response_kind": "bounded_answer",
            "answer_mode": "grounded_fact",
            "uncertainty_band": "low",
            "live_measurement_required": False,
            **target_meta,
        }
    if time_request and raw_tokens.intersection({"time", "date", "today", "now"}):
        return {
            "response_text": (
                f"In the local shell timezone {context['timezone']}, it is {context['time']} on "
                f"{context['date']}. That is a grounded local clock fact, not a weather measurement."
            ),
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "grounded_fact",
            "response_kind": "bounded_answer",
            "answer_mode": "grounded_fact",
            "uncertainty_band": "low",
            "live_measurement_required": False,
            **target_meta,
        }
    if weather_request and location["explicit"] and location["grounded"] and not location["estimate_allowed"]:
        target_kind = str(location.get("target_kind", "unknown_target"))
        if target_kind == "extraterrestrial_body":
            response_text = (
                f"I can ground the target as {location['label']}, but this shell has no extraterrestrial weather prior or live measurement path for that kind of target. "
                "Treating it like an Earth weather report would be misleading, so I abstain."
            )
        else:
            response_text = (
                f"I can ground the target as {location['label']}, but I do not have a supported local climate prior or live measurement for that Earth location in this shell. "
                "Treating it like a supported weather report would be misleading, so I abstain."
            )
        return {
            "response_text": response_text,
            "support_state": "unknown",
            "knowledge_gap_reason": "missing_local_evidence",
            "next_action": "abstain",
            "final_answer_mode": "unknown",
            "response_kind": "fail_closed_unknown",
            "answer_mode": "abstain",
            "uncertainty_band": "high",
            "live_measurement_required": False,
            **target_meta,
        }
    return {
        "response_text": (
            "I do not have enough approved local context for an honest current-world estimate here. "
            "Without live measurement or a supported local prior, the safe result is abstain."
        ),
        "support_state": "unknown",
        "knowledge_gap_reason": "needs_fresh_information",
        "next_action": "abstain",
        "final_answer_mode": "unknown",
        "response_kind": "fail_closed_unknown",
        "answer_mode": "abstain",
        "uncertainty_band": "high",
        "live_measurement_required": True,
        **target_meta,
    }


def _answer_underspecified(
    question_text: str,
    phase7_turn_state: Mapping[str, Any],
    prior_turn: Mapping[str, Any] | None,
) -> dict[str, str]:
    clarification = dict(phase7_turn_state.get("clarification", {}))
    questions = clarification.get("questions", [])
    raw_tokens = set(_tokenize(question_text))
    anchor_turn = _anchor_turn(prior_turn=prior_turn)
    referential_request = bool(raw_tokens.intersection(UNDERSPECIFIED_REFERENCE_TOKENS))
    if raw_tokens.intersection({"change", "changed", "event", "events", "happen", "happened"}):
        response_text = "I need the event or artifact you want checked. You can point me to a phase status, verifier, evidence report, runtime turn, or review bundle."
    elif raw_tokens.intersection({"break", "broke", "broken", "fail", "failed", "failing"}) and raw_tokens.intersection({"what", "why"}):
        response_text = "Name the failing phase, verifier, artifact, or prior answer you want explained. Without that target, the safe move is clarification."
    elif anchor_turn and referential_request and raw_tokens.intersection({"detail", "details", "expand", "explain", "mean", "more"}):
        response_text = "Point me to the part you want expanded from the anchor turn: its claim, evidence, support state, answer mode, or missing support."
    elif anchor_turn and referential_request:
        response_text = "I need the specific referent for `that`. Point to the prior claim, phase, evidence file, or runtime behavior you want continued."
    elif raw_tokens.intersection({"detail", "details", "expand", "explain", "further", "more"}):
        response_text = "Tell me which part you want expanded: the claim, evidence, support state, answer mode, or missing support."
    elif questions:
        response_text = str(questions[0].get("question_text", "I need a narrower question.")).strip()
    else:
        response_text = "I need a narrower question. I can answer about AGIFCore identity, runtime status, phase truth, manifests, evidence, and review state from local files."
    return {
        "response_text": response_text,
        "support_state": "unknown",
        "knowledge_gap_reason": "ambiguous_request",
        "next_action": "clarify",
        "final_answer_mode": "clarify",
        "response_kind": "guided_clarification",
    }


def _answer_follow_up(
    *,
    question_text: str,
    follow_up_binding: FollowUpBindingDecision,
) -> dict[str, str] | None:
    anchor_turn = follow_up_binding.anchor_turn
    follow_up_intent = follow_up_binding.intent
    if not follow_up_binding.success or not anchor_turn or follow_up_intent is None:
        return None
    if follow_up_intent in {"history", "support"}:
        return None
    prior_request = _turn_topic_label(anchor_turn)
    prior_support = str(anchor_turn.get("support_state", "unknown"))
    prior_mode = str(anchor_turn.get("final_answer_mode", "unknown"))
    prior_next = str(anchor_turn.get("next_action", "abstain"))
    prior_class = str(anchor_turn.get("question_class", "unsupported"))
    binding_text = (
        f"Binding confidence was {follow_up_binding.confidence:.2f} because {follow_up_binding.reason}."
        if follow_up_binding.confidence > 0
        else follow_up_binding.reason
    )
    ref_text = _format_local_refs_text(anchor_turn)
    if follow_up_intent == "reason":
        if prior_next == "clarify":
            return {
                "response_text": (
                    f"Because the anchor turn on {prior_request} still had an unresolved referent or missing variable. "
                    f"It stayed fail-closed in clarify mode instead of inventing context. {binding_text}{ref_text}"
                ),
                "support_state": "grounded",
                "knowledge_gap_reason": "none",
                "next_action": "answer",
                "final_answer_mode": "derived_explanation",
                "response_kind": "bounded_answer",
            }
        if prior_next in {"abstain", "search_needed", "search_local"}:
            return {
                "response_text": (
                    f"Because the anchor turn on {prior_request} did not have enough approved local support for a safe answer. "
                    f"{_turn_policy_summary(anchor_turn)}. {binding_text}{ref_text}"
                ),
                "support_state": "grounded",
                "knowledge_gap_reason": "none",
                "next_action": "answer",
                "final_answer_mode": "derived_explanation",
                "response_kind": "bounded_answer",
            }
        return {
            "response_text": (
                f"Because the anchor turn on {prior_request} had enough approved local support to answer. "
                f"{_turn_policy_summary(anchor_turn)}. {binding_text}{ref_text}"
            ),
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "derived_explanation",
            "response_kind": "bounded_answer",
        }
    if follow_up_intent == "method":
        return {
            "response_text": (
                f"The anchor turn on {prior_request} was processed through the live AGIFCore path. "
                f"{_turn_policy_summary(anchor_turn)}. {binding_text}{ref_text}"
            ),
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "derived_explanation",
            "response_kind": "bounded_answer",
        }
    if follow_up_intent == "confidence":
        if prior_support == "grounded":
            response_text = (
                f"Boundedly yes. The anchor turn on {prior_request} stayed grounded in approved local support. {binding_text}{ref_text}"
            )
        elif prior_support == "inferred":
            response_text = (
                f"Only partially. The anchor turn on {prior_request} was inferred rather than fully grounded, so it should be treated as bounded and revisitable. {binding_text}{ref_text}"
            )
        else:
            response_text = (
                f"No. The anchor turn on {prior_request} did not have strong enough local support and stayed fail-closed with next action {prior_next}. {binding_text}{ref_text}"
            )
        return {
            "response_text": response_text,
            "support_state": "grounded",
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "grounded_fact",
            "response_kind": "bounded_answer",
        }
    if follow_up_intent == "explanation":
        if prior_next == "clarify":
            response_text = (
                f"I mean the anchor turn on {prior_request} was still missing a concrete referent or variable, so it stayed in clarify mode. "
                f"{binding_text}{ref_text}"
            )
        else:
            response_text = (
                f"I mean the anchor turn on {prior_request} was handled as a bounded {prior_class} answer. "
                f"{_turn_policy_summary(anchor_turn)}. {binding_text}{ref_text}"
            )
        return {
            "response_text": response_text,
            "support_state": "grounded" if prior_support in {"grounded", "inferred"} else "unknown",
            "knowledge_gap_reason": "none" if prior_support in {"grounded", "inferred"} else "missing_local_evidence",
            "next_action": "answer" if prior_support in {"grounded", "inferred"} or prior_next == "clarify" else "abstain",
            "final_answer_mode": "derived_explanation" if prior_support in {"grounded", "inferred"} or prior_next == "clarify" else "unknown",
            "response_kind": "bounded_answer" if prior_support in {"grounded", "inferred"} or prior_next == "clarify" else "fail_closed_unknown",
        }
    if prior_next == "clarify":
        return {
            "response_text": (
                f"The anchor turn on {prior_request} was ambiguous. Clarify the missing variable so I can bind the follow-up to a concrete local claim. "
                f"{binding_text}"
            ),
            "support_state": "unknown",
            "knowledge_gap_reason": "ambiguous_request",
            "next_action": "clarify",
            "final_answer_mode": "clarify",
            "response_kind": "guided_clarification",
        }
    if prior_support in {"grounded", "inferred"}:
        return {
            "response_text": (
                f"The follow-up binds to the anchor turn on {prior_request}. "
                f"{_turn_policy_summary(anchor_turn)}. {binding_text}{ref_text}"
            ),
            "support_state": prior_support,
            "knowledge_gap_reason": "none",
            "next_action": "answer",
            "final_answer_mode": "grounded_fact" if prior_mode == "grounded_fact" else "derived_explanation",
            "response_kind": "bounded_answer",
        }
    if prior_next in {"search_needed", "search_local"}:
        return {
            "response_text": "The previous turn already needed missing local support. I still need additional local evidence to answer this follow-up safely.",
            "support_state": "search_needed",
            "knowledge_gap_reason": "missing_local_evidence",
            "next_action": "search_needed",
            "final_answer_mode": "search_needed",
            "response_kind": "guided_search",
        }
    return {
        "response_text": "The previous turn did not have enough local support for a safe answer, so this follow-up also remains unsupported.",
        "support_state": "unknown",
        "knowledge_gap_reason": "missing_local_evidence",
        "next_action": "abstain",
        "final_answer_mode": "unknown",
        "response_kind": "fail_closed_unknown",
    }


def _answer_unsupported(*, question_text: str, phase7_turn_state: Mapping[str, Any]) -> dict[str, str]:
    unsupported_domain = _unsupported_request_domain(question_text) or _external_request_scope(question_text)
    support_state = str(phase7_turn_state.get("support_resolution", {}).get("support_state", "unknown"))
    next_action = str(phase7_turn_state.get("support_resolution", {}).get("next_action", "abstain"))
    if unsupported_domain == "finance":
        return {
            "response_text": "I do not have local support or current financial data for that. In this AGIFCore shell, investment questions stay fail-closed and need current external information.",
            "support_state": "search_needed",
            "knowledge_gap_reason": "needs_fresh_information",
            "next_action": "search_needed",
            "final_answer_mode": "search_needed",
            "response_kind": "guided_search",
        }
    if unsupported_domain in {"external_fact", "world_fact"}:
        return {
            "response_text": "I do not have local support for that question in the current AGIFCore shell. It needs current information outside the approved local project truth surface.",
            "support_state": "unknown",
            "knowledge_gap_reason": "missing_local_evidence",
            "next_action": "abstain",
            "final_answer_mode": "unknown",
            "response_kind": "fail_closed_unknown",
        }
    if next_action == "search_external":
        return {
            "response_text": "I cannot answer that honestly from local AGIFCore state because it needs fresh external information. The bounded result is search_needed.",
            "support_state": "search_needed",
            "knowledge_gap_reason": "needs_fresh_information",
            "next_action": "search_needed",
            "final_answer_mode": "search_needed",
            "response_kind": "guided_search",
        }
    if unsupported_domain == "personal_identity":
        return {
            "response_text": "I do not have local proof of your personal identity. I only know there is a user operating this local AGIFCore session.",
            "support_state": "unknown",
            "knowledge_gap_reason": "missing_local_evidence",
            "next_action": "abstain",
            "final_answer_mode": "unknown",
            "response_kind": "fail_closed_unknown",
        }
    return {
        "response_text": "I do not have local support for that question in the current AGIFCore shell. I can answer only from local AGIFCore truth, manifests, evidence, and runtime state.",
        "support_state": "unknown" if support_state != "search_needed" else "search_needed",
        "knowledge_gap_reason": "missing_local_evidence" if support_state != "search_needed" else "needs_fresh_information",
        "next_action": "abstain" if support_state != "search_needed" else "search_needed",
        "final_answer_mode": "unknown" if support_state != "search_needed" else "search_needed",
        "response_kind": "fail_closed_unknown" if support_state != "search_needed" else "guided_search",
    }


def _compose_response(
    *,
    question_class: str,
    question_text: str,
    shell_snapshot: Mapping[str, Any],
    route: Mapping[str, Any],
    support_lines: list[tuple[int, SourceLine]],
    phase7_turn_state: Mapping[str, Any],
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]],
    follow_up_binding: FollowUpBindingDecision,
) -> dict[str, str]:
    follow_up_answer = _answer_follow_up(
        question_text=question_text,
        follow_up_binding=follow_up_binding,
    )
    if follow_up_answer is not None:
        return follow_up_answer
    if question_class == "session_history":
        anchor_turn = follow_up_binding.anchor_turn if follow_up_binding.success else prior_turn
        return _answer_session_history(prior_turn=anchor_turn, recent_turns=recent_turns)
    if question_class == "support_diagnostics":
        anchor_turn = follow_up_binding.anchor_turn if follow_up_binding.success else prior_turn
        return _answer_support_diagnostics(question_text=question_text, prior_turn=anchor_turn, recent_turns=recent_turns)
    if question_class == "self_system_status":
        return _answer_self_system(
            question_text=question_text,
            shell_snapshot=shell_snapshot,
            route=route,
            self_knowledge_state=phase7_turn_state.get("self_knowledge", {}),
            support_lines=support_lines,
        )
    if question_class == "project_phase_capability":
        return _answer_project_capability(
            question_text=question_text,
            shell_snapshot=shell_snapshot,
            support_lines=support_lines,
        )
    if question_class == "local_truth_evidence":
        return _answer_local_truth(question_text=question_text, support_lines=support_lines)
    if question_class == "reasoning_math":
        return _answer_reasoning_math(question_text)
    if question_class == "comparison_planning":
        return _answer_comparison_planning(question_text=question_text, support_lines=support_lines)
    if question_class == "contradiction":
        return _answer_contradiction(question_text=question_text, support_lines=support_lines)
    if question_class == "current_world":
        return _answer_current_world(question_text)
    if question_class == "underspecified":
        anchor_turn = follow_up_binding.anchor_turn if follow_up_binding.success else prior_turn
        return _answer_underspecified(question_text, phase7_turn_state, anchor_turn)
    return _answer_unsupported(question_text=question_text, phase7_turn_state=phase7_turn_state)


def _attach_answer_metadata(
    *,
    question_class: str,
    response: Mapping[str, Any],
) -> dict[str, Any]:
    final_answer_mode = str(response.get("final_answer_mode", "unknown"))
    support_state = str(response.get("support_state", "unknown"))
    next_action = str(response.get("next_action", "abstain"))
    if "answer_mode" in response:
        answer_mode = str(response["answer_mode"])
    elif final_answer_mode == "derived_estimate" and next_action == "answer":
        answer_mode = "bounded_estimate"
    elif next_action == "answer":
        answer_mode = "grounded_fact"
    else:
        answer_mode = "abstain"
    uncertainty_band = str(
        response.get(
            "uncertainty_band",
            "low"
            if answer_mode == "grounded_fact" and support_state == "grounded"
            else "medium"
            if answer_mode == "grounded_fact"
            else "medium"
            if answer_mode == "bounded_estimate"
            else "high",
        )
    )
    live_measurement_required = bool(
        response.get(
            "live_measurement_required",
            question_class == "current_world" and answer_mode != "grounded_fact",
        )
    )
    return {
        **response,
        "answer_mode": answer_mode,
        "uncertainty_band": uncertainty_band,
        "live_measurement_required": live_measurement_required,
    }


def _apply_phase10_guardrails(
    *,
    question_class: str,
    response: dict[str, str],
    phase10_turn_state: Mapping[str, Any],
) -> dict[str, str]:
    selected_outcome = str(phase10_turn_state.get("overlay_contract", {}).get("selected_outcome", "recheck_support"))
    if question_class == "current_world" and response.get("final_answer_mode") == "derived_estimate":
        return response
    if response.get("next_action") == "clarify" and question_class not in {"underspecified", "contradiction"}:
        return response
    if selected_outcome == "abstain" and response["support_state"] != "grounded":
        return {
            "response_text": str(phase10_turn_state.get("overlay_contract", {}).get("public_explanation", response["response_text"])),
            "support_state": "unknown",
            "knowledge_gap_reason": "conflicting_state",
            "next_action": "abstain",
            "final_answer_mode": "unknown",
            "response_kind": "fail_closed_unknown",
        }
    if (
        selected_outcome == "clarify"
        and response["support_state"] in {"unknown", "search_needed"}
        and (
            response["next_action"] == "clarify"
            or question_class in {"underspecified", "contradiction"}
        )
    ):
        return {
            "response_text": str(phase10_turn_state.get("overlay_contract", {}).get("public_explanation", response["response_text"])),
            "support_state": "unknown",
            "knowledge_gap_reason": "ambiguous_request",
            "next_action": "clarify",
            "final_answer_mode": "clarify",
            "response_kind": "guided_clarification",
        }
    return response


def _build_phase2_evidence(
    *,
    conversation_id: str,
    turn_id: str,
    phase7_turn_state: Mapping[str, Any],
    final_response: Mapping[str, str],
    local_truth_refs: tuple[str, ...],
) -> dict[str, Any]:
    answer_contract = dict(phase7_turn_state.get("answer_contract", {}))
    utterance_plan = dict(phase7_turn_state.get("utterance_plan", {}))
    event_bus = EventBus()
    workspace = SharedWorkspaceState(workspace_id="phase-13-live-interactive-workspace")
    replay_ledger = ReplayLedger()
    event_bus.subscribe(KernelEventType.RESPONSE_READY, workspace.bind_event)

    turn_context = KernelTurnContext(
        conversation_id=conversation_id,
        turn_id=turn_id,
        user_intent=str(answer_contract.get("user_intent", "interactive_turn")),
        discourse_mode=_p2_discourse_mode(str(answer_contract.get("discourse_mode", utterance_plan.get("discourse_mode", "explain")))),
        support_state=_p2_support_state(str(final_response["support_state"])),
        knowledge_gap_reason=_p2_gap_reason(str(final_response["knowledge_gap_reason"])),
        next_action=_p2_next_action(str(final_response["next_action"])),
        active_context_refs=tuple(local_truth_refs[:8]),
    )
    trace_refs = KernelTraceRefs(
        planner_trace_ref=str(answer_contract.get("planner_trace_ref", "planner::missing")),
        simulation_trace_ref=str(answer_contract.get("simulation_trace_ref", "simulation::missing")),
        critic_trace_ref=str(answer_contract.get("critic_trace_ref", "critic::missing")),
        governance_trace_ref=str(answer_contract.get("governance_trace_ref", "governance::missing")),
    )
    response_surface = KernelResponseSurface(
        response_text=str(final_response["response_text"]),
        abstain_or_answer=(
            P2AbstainOrAnswer.ANSWER
            if str(final_response["final_answer_mode"]) in {"grounded_fact", "derived_explanation", "derived_estimate", "hypothesis"}
            else P2AbstainOrAnswer.ABSTAIN
        ),
        final_answer_mode=_p2_final_answer_mode(str(final_response["final_answer_mode"])),
        memory_review_ref=str(answer_contract.get("memory_review_ref", "")) or None,
    )
    events = (
        new_kernel_event(
            event_type=KernelEventType.TURN_ADMITTED,
            turn=turn_context,
            trace_refs=trace_refs,
            producer="phase13-live-turn",
            payload={"stage": "turn_admitted"},
        ),
        new_kernel_event(
            event_type=KernelEventType.TRACE_ANNOTATED,
            turn=turn_context,
            trace_refs=trace_refs,
            producer="phase13-live-turn",
            payload={"stage": "trace_annotated"},
        ),
        new_kernel_event(
            event_type=KernelEventType.GOVERNANCE_DECIDED,
            turn=turn_context,
            trace_refs=trace_refs,
            producer="phase13-live-turn",
            payload={"stage": "governance_decided"},
        ),
        new_kernel_event(
            event_type=KernelEventType.RESPONSE_READY,
            turn=turn_context,
            trace_refs=trace_refs,
            producer="phase13-live-turn",
            payload={"stage": "response_ready"},
            response=response_surface,
        ),
    )
    event_ids: list[str] = []
    for event in events:
        event_bus.publish(event)
        event_ids.append(event.event_id)
    for ref in local_truth_refs[:12]:
        workspace.attach_evidence_ref(ref)
    if response_surface.memory_review_ref:
        workspace.attach_memory_review_ref(
            response_surface.memory_review_ref,
            conversation_id=conversation_id,
            turn_id=turn_id,
        )
    replay_record = replay_ledger.record_replay(
        replay_id=f"replay::{stable_hash_payload({'conversation_id': conversation_id, 'turn_id': turn_id})[:12]}",
        conversation_id=conversation_id,
        turn_id=turn_id,
        trace_export=event_bus.trace_export(),
        state_export=workspace.state_export(),
        event_ids=event_ids,
    )
    workspace.attach_replay_ref(replay_record.replay_id)
    replay_verification = replay_ledger.verify_replay(
        replay_id=replay_record.replay_id,
        trace_export=event_bus.trace_export(),
        state_export=workspace.state_export(),
    )
    return {
        "event_export": event_bus.event_export(),
        "trace_export": event_bus.trace_export(),
        "workspace_state_export": workspace.state_export(),
        "workspace_memory_review_export": workspace.memory_review_export(),
        "replay_export": replay_ledger.replay_export(),
        "replay_verification": replay_verification,
        "event_count": len(event_ids),
        "replay_id": replay_record.replay_id,
    }


def _phase_support_delta(
    *,
    before: str | None = None,
    after: str | None = None,
    note: str | None = None,
    **extra: Any,
) -> dict[str, Any] | None:
    delta: dict[str, Any] = {}
    if before is not None:
        delta["before"] = str(before)
    if after is not None:
        delta["after"] = str(after)
    if note:
        delta["note"] = str(note)
    for key, value in extra.items():
        if value is None:
            continue
        delta[key] = value
    if not delta:
        return None
    if delta.get("before") == delta.get("after") and set(delta) <= {"before", "after"}:
        return None
    return delta


def _phase_result(
    *,
    phase_id: int,
    status: str,
    reason: str,
    inputs_used: Iterable[str],
    outputs_added: Iterable[str],
    refs_used: Iterable[str],
    support_delta: Mapping[str, Any] | None,
    state_changed: bool,
) -> dict[str, Any]:
    clean_status = str(status).strip().lower()
    if clean_status not in {"used", "no_op", "blocked", "insufficient_input"}:
        raise RuntimeError(f"unsupported interactive phase status: {clean_status}")
    clean_reason = " ".join(str(reason).split()).strip()
    return {
        "phase_id": phase_id,
        "status": clean_status,
        "reason": clean_reason,
        "inputs_used": list(
            bounded_unique(
                list(inputs_used),
                ceiling=24,
                field_name=f"interactive_phase_{phase_id}_inputs_used",
                allow_empty=True,
            )
        ),
        "outputs_added": list(
            bounded_unique(
                list(outputs_added),
                ceiling=24,
                field_name=f"interactive_phase_{phase_id}_outputs_added",
                allow_empty=True,
            )
        ),
        "support_delta": dict(support_delta) if support_delta else None,
        "refs_used": list(
            bounded_unique(
                list(refs_used),
                ceiling=24,
                field_name=f"interactive_phase_{phase_id}_refs_used",
                allow_empty=True,
            )
        ),
        "state_changed": bool(state_changed),
    }


def _phase15_turn_evidence_relpath(*, session_id: str, turn_id: str) -> str:
    safe_session = re.sub(r"[^a-zA-Z0-9._-]+", "_", session_id).strip("_") or "unknown_session"
    safe_turn = re.sub(r"[^a-zA-Z0-9._-]+", "_", turn_id).strip("_") or "unknown_turn"
    evidence_path = PHASE15_TURN_EVIDENCE_DIR / safe_session / f"{safe_turn}.json"
    return str(evidence_path.relative_to(REPO_ROOT))


def _write_phase15_turn_evidence(
    *,
    rel_path: str,
    payload: Mapping[str, Any],
) -> tuple[bool, str, str | None]:
    evidence_path = REPO_ROOT / rel_path
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    written_at = datetime.now().replace(microsecond=0).isoformat()
    evidence_payload = {
        "schema": PHASE15_TURN_EVIDENCE_SCHEMA,
        **dict(payload),
        "written_at": written_at,
    }
    evidence_payload["evidence_hash"] = stable_hash_payload(evidence_payload)
    evidence_path.write_text(json.dumps(evidence_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return True, written_at, evidence_payload["evidence_hash"]


def _build_phase_results(
    *,
    question_class: str,
    follow_up_bound: bool,
    candidate_lines: list[tuple[float, LocalTruthLine]],
    local_truth_refs: tuple[str, ...],
    route: Mapping[str, Any],
    phase2_evidence: Mapping[str, Any],
    phase4_state: Mapping[str, Any],
    phase5_state: Mapping[str, Any],
    phase6_state: Mapping[str, Any],
    phase7_turn: Mapping[str, Any],
    phase8_turn: Any,
    phase9_turn: Any,
    phase10_turn: Any,
    phase11_cycle_state: Mapping[str, Any],
    phase12_cycle_state: Mapping[str, Any],
    shell_snapshot: Mapping[str, Any],
    response: Mapping[str, Any],
    phase_usage_raw: Mapping[str, Mapping[str, Any]],
    phase15_turn_evidence_ref: str | None,
    proof_record_written: bool,
) -> list[dict[str, Any]]:
    candidate_refs = bounded_unique(
        [line.ref for _, line in candidate_lines],
        ceiling=12,
        field_name="interactive_candidate_refs",
        allow_empty=True,
    )
    route_refs = bounded_unique(
        list(route["route_refs"]),
        ceiling=12,
        field_name="interactive_route_refs",
        allow_empty=True,
    )
    phase11_refs = bounded_unique(
        list(phase11_cycle_state.get("overlay_contract", {}).get("monitoring_refs", [])),
        ceiling=12,
        field_name="interactive_phase11_refs",
        allow_empty=True,
    )
    phase12_refs = bounded_unique(
        list(phase12_cycle_state.get("overlay_contract", {}).get("selected_gap_ids", [])),
        ceiling=12,
        field_name="interactive_phase12_refs",
        allow_empty=True,
    )
    phase7_support_state = str(phase7_turn["support_resolution"]["support_state"])
    final_support_state = str(response["support_state"])
    final_next_action = str(response["next_action"])
    phase10_diagnosis_ref = phase10_turn.overlay_contract.diagnosis_ref

    phase2_status = "used" if int(phase2_evidence["event_count"]) > 0 else "blocked"
    phase4_status = (
        "used"
        if phase4_state["semantic_candidates"] or phase4_state["procedure_specs"]
        else "insufficient_input"
    )
    phase5_status = (
        "used"
        if phase5_state["descriptor_graph_state"]["nodes"] or phase5_state["skill_graph_state"]["nodes"]
        else "insufficient_input"
    )
    phase6_status = (
        "used"
        if phase_usage_raw["phase_6"]["used"]
        else ("insufficient_input" if question_class == "reasoning_math" else "no_op")
    )
    if question_class == "current_world" and not phase_usage_raw["phase_8"]["used"]:
        phase8_status = "insufficient_input"
    elif question_class == "comparison_planning" and final_next_action != "answer":
        phase8_status = "insufficient_input"
    else:
        phase8_status = "used" if phase_usage_raw["phase_8"]["used"] else "no_op"
    phase9_status = "used" if phase_usage_raw["phase_9"]["used"] else "no_op"
    phase10_status = "used" if phase_usage_raw["phase_10"]["used"] else "no_op"
    phase11_status = "used" if phase_usage_raw["phase_11"]["used"] else "no_op"
    phase12_status = "used" if phase_usage_raw["phase_12"]["used"] else "no_op"
    phase14_status = "used"
    phase15_status = "used" if proof_record_written and phase15_turn_evidence_ref else "blocked"

    return [
        _phase_result(
            phase_id=2,
            status=phase2_status,
            reason=(
                "phase 2 recorded trace, replay, workspace, and fail-closed evidence for the live turn"
                if phase2_status == "used"
                else "phase 2 could not record its replay and evidence baseline for this turn"
            ),
            inputs_used=[
                "conversation_id",
                "turn_id",
                "phase7.answer_contract",
                "final_response",
                "local_truth_refs",
            ],
            outputs_added=[
                "event_export",
                "trace_export",
                "workspace_state_export",
                "workspace_memory_review_export",
                "replay_export",
                "replay_verification",
            ],
            refs_used=local_truth_refs,
            support_delta=None,
            state_changed=phase2_status == "used",
        ),
        _phase_result(
            phase_id=3,
            status="used",
            reason="phase 3 routed the turn through governed families, cells, and tissues",
            inputs_used=["question_class", "profile", "target_domain_hint"],
            outputs_added=[
                "route.family_order",
                "route.selected_cell_ids",
                "route.selected_tissue_ids",
                "route.route_refs",
                "route.budget",
            ],
            refs_used=route_refs,
            support_delta=None,
            state_changed=True,
        ),
        _phase_result(
            phase_id=4,
            status=phase4_status,
            reason=(
                "phase 4 built continuity, working, semantic, procedural, and review memory for this turn"
                if phase4_status == "used"
                else "phase 4 ran, but there was not enough candidate support to populate memory planes"
            ),
            inputs_used=[
                "question_text",
                "candidate_lines",
                "prior_turn",
                "recent_turns",
                "route",
                "shell_snapshot",
            ],
            outputs_added=[
                "continuity_memory_state",
                "working_memory_state",
                "memory_review_state",
                "semantic_memory_state",
                "procedural_memory_state",
            ],
            refs_used=candidate_refs,
            support_delta=_phase_support_delta(
                note="memory_context_prepared",
                semantic_candidate_count=len(phase4_state["semantic_candidates"]),
                procedural_candidate_count=len(phase4_state["procedure_specs"]),
            ),
            state_changed=phase4_status == "used",
        ),
        _phase_result(
            phase_id=5,
            status=phase5_status,
            reason=(
                "phase 5 selected graph-backed support from descriptor, concept, skill, and transfer structures"
                if phase5_status == "used"
                else "phase 5 ran, but graph selection could not add useful support candidates"
            ),
            inputs_used=[
                "question_text",
                "question_class",
                "target_domain",
                "phase4.semantic_memory_state",
                "phase4.procedural_memory_state",
            ],
            outputs_added=[
                "descriptor_graph_state",
                "skill_graph_state",
                "concept_graph_state",
                "transfer_graph_state",
                "support_selection_result",
            ],
            refs_used=local_truth_refs,
            support_delta=_phase_support_delta(
                note="graph_support_selected",
                selected_candidate_count=len(
                    phase5_state["support_selection_result"].get("selected_candidate_ids", [])
                ),
            ),
            state_changed=phase5_status == "used",
        ),
        _phase_result(
            phase_id=6,
            status=phase6_status,
            reason=(
                "phase 6 built world-model, candidate-future, simulation, and usefulness context"
                if phase6_status == "used"
                else (
                    "phase 6 was visited, but the prompt lacked enough concrete mathematical state to run a useful simulation"
                    if phase6_status == "insufficient_input"
                    else "phase 6 was visited, but world-model simulation was not needed for this turn"
                )
            ),
            inputs_used=[
                "phase4.semantic_memory_state",
                "phase4.procedural_memory_state",
                "phase4.continuity_memory_state",
                "phase5.support_selection_result",
            ],
            outputs_added=[
                "target_domain_registry_state",
                "world_model_state",
                "candidate_future_state",
                "what_if_simulation_state",
                "usefulness_state",
            ],
            refs_used=local_truth_refs,
            support_delta=None,
            state_changed=phase6_status == "used",
        ),
        _phase_result(
            phase_id=7,
            status="used",
            reason="phase 7 performed intake, interpretation, support-state routing, and answer-contract selection",
            inputs_used=[
                "question_text",
                "question_class",
                "active_context_refs",
                "phase4_state",
                "phase5_state",
                "phase6_state",
            ],
            outputs_added=[
                "intake",
                "interpretation",
                "support_resolution",
                "answer_contract",
                "utterance_plan",
                "guardrail_result",
            ],
            refs_used=tuple(phase7_turn["intake"]["active_context_refs"]),
            support_delta=_phase_support_delta(
                after=phase7_support_state,
                note="support_state_resolved",
                next_action=phase7_turn["support_resolution"]["next_action"],
            ),
            state_changed=True,
        ),
        _phase_result(
            phase_id=8,
            status=phase8_status,
            reason=(
                "phase 8 performed bounded science or world-awareness reasoning for the turn"
                if phase8_status == "used"
                else (
                    "phase 8 was visited, but the grounded target or current-world support was too weak for a safe science/world-aware answer"
                    if phase8_status == "insufficient_input"
                    else "phase 8 was visited, but science/world-awareness reasoning was not needed for this turn"
                )
            ),
            inputs_used=[
                "phase7.intake",
                "phase7.interpretation",
                "phase7.support_resolution",
                "phase6.world_model_state",
                "phase6.what_if_simulation_state",
                "phase5.support_selection_result",
            ],
            outputs_added=[
                "entity_request_inference",
                "visible_reasoning_summary",
                "overlay_contract",
            ],
            refs_used=local_truth_refs,
            support_delta=None,
            state_changed=phase8_status == "used",
        ),
        _phase_result(
            phase_id=9,
            status=phase9_status,
            reason=(
                "phase 9 composed the bounded response lane, synthesis, and public expression contract"
                if phase9_status == "used"
                else "phase 9 was visited, but no richer public expression layer was allowed beyond the fail-closed outcome"
            ),
            inputs_used=[
                "phase7.intake",
                "phase7.interpretation",
                "phase7.support_resolution",
                "phase7.utterance_plan",
                "phase7.answer_contract",
                "phase8_turn",
            ],
            outputs_added=["selected_lane", "overlay_contract"],
            refs_used=local_truth_refs,
            support_delta=None,
            state_changed=phase9_status == "used",
        ),
        _phase_result(
            phase_id=10,
            status=phase10_status,
            reason=(
                "phase 10 ran critique, contradiction, or weak-answer diagnosis before the final answer"
                if phase10_status == "used"
                else "phase 10 was visited, but no extra critique overlay was needed for this turn"
            ),
            inputs_used=[
                "phase7.support_resolution",
                "phase7.answer_contract",
                "phase7.self_knowledge",
                "phase8_turn",
                "phase9_turn",
                "phase4.continuity_memory_state",
            ],
            outputs_added=["overlay_contract", "selected_outcome", "public_explanation"],
            refs_used=[*local_truth_refs, *( [phase10_diagnosis_ref] if phase10_diagnosis_ref else [] )],
            support_delta=_phase_support_delta(
                before=phase7_support_state,
                after=final_support_state,
                note="critique_pass_complete",
                selected_outcome=phase10_turn.overlay_contract.selected_outcome.value,
                diagnosis_ref=phase10_diagnosis_ref,
            ),
            state_changed=phase10_status == "used",
        ),
        _phase_result(
            phase_id=11,
            status=phase11_status,
            reason=(
                "phase 11 supplied read-only monitoring and self-improvement history context"
                if phase11_status == "used"
                else "phase 11 was visited, but no read-only self-improvement overlay was relevant to this turn"
            ),
            inputs_used=["phase11_cycle_state.overlay_contract", "phase11_cycle_state.monitoring_refs"],
            outputs_added=["read_only_monitoring_context"],
            refs_used=phase11_refs,
            support_delta=None,
            state_changed=False,
        ),
        _phase_result(
            phase_id=12,
            status=phase12_status,
            reason=(
                "phase 12 supplied read-only structural growth context"
                if phase12_status == "used"
                else "phase 12 was visited, but no read-only structural overlay was relevant to this turn"
            ),
            inputs_used=["phase12_cycle_state.overlay_contract", "phase12_cycle_state.selected_gap_ids"],
            outputs_added=["read_only_structural_context"],
            refs_used=phase12_refs,
            support_delta=None,
            state_changed=False,
        ),
        _phase_result(
            phase_id=13,
            status="used",
            reason="phase 13 hosted the live turn inside the real product runtime shell",
            inputs_used=["session_open", "shell_snapshot", "state_export", "memory_review_export", "safe_shutdown"],
            outputs_added=["interactive_turn_payload", "session_history_update_ready"],
            refs_used=[],
            support_delta=None,
            state_changed=False,
        ),
        _phase_result(
            phase_id=14,
            status=phase14_status,
            reason=(
                "phase 14 enforced sandbox profile, routing budget, and active-cell selection"
                if bool(route["budget"]["allowed"])
                else "phase 14 enforced the sandbox profile and budget gate, but the budget outcome constrained the turn"
            ),
            inputs_used=["profile", "route", "budget", "selected_active_cells", "selected_active_tissues"],
            outputs_added=["budget_receipt", "budget_state", "selected_active_cell_count", "selected_active_tissue_count"],
            refs_used=route_refs,
            support_delta=_phase_support_delta(
                note="budget_enforced",
                budget_state=route["budget"]["budget_state"],
                allowed=bool(route["budget"]["allowed"]),
            ),
            state_changed=True,
        ),
        _phase_result(
            phase_id=15,
            status=phase15_status,
            reason=(
                "phase 15 wrote per-turn proof, review, and machine-readable evidence fields"
                if phase15_status == "used"
                else "phase 15 could not write the per-turn proof and evidence record"
            ),
            inputs_used=[
                "final_response",
                "phase_usage_raw",
                "local_truth_refs",
                "phase2_evidence",
                "question_class",
                "follow_up_bound",
            ],
            outputs_added=[
                "phase_results",
                "phase_usage",
                "phases_exercised",
                "phase_chain_completed",
                "phase_status_counts",
            ],
            refs_used=[phase15_turn_evidence_ref] if phase15_turn_evidence_ref else [],
            support_delta=_phase_support_delta(
                after=final_support_state,
                note="proof_record_written",
                final_answer_mode=response["final_answer_mode"],
            ),
            state_changed=phase15_status == "used",
        ),
    ]


def build_interactive_turn(
    *,
    user_text: str,
    session_open: Mapping[str, Any],
    shell_snapshot: Mapping[str, Any],
    state_export: Mapping[str, Any],
    memory_review_export: Mapping[str, Any],
    safe_shutdown: Mapping[str, Any],
    phase10_turn_state: Mapping[str, Any],
    phase11_cycle_state: Mapping[str, Any],
    phase12_cycle_state: Mapping[str, Any],
    turn_sequence: int,
    prior_turn: Mapping[str, Any] | None,
    recent_turns: list[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    question_text = _clean_text(str(user_text))
    if not question_text:
        question_text = "empty interactive request"
    conversation_id = str(shell_snapshot["conversation_id"])
    turn_id = f"interactive::{stable_hash_payload({'session_id': shell_snapshot['session_id'], 'turn_sequence': turn_sequence, 'question_text': question_text})[:12]}"

    phase14_shell = SandboxProfileRuntimeShell(
        phase13_session_open=session_open,
        phase13_shell_snapshot=shell_snapshot,
        phase13_state_export=state_export,
        phase13_memory_review_export=memory_review_export,
        phase13_safe_shutdown=safe_shutdown,
    )
    source_corpus = _build_source_corpus(
        session_open=session_open,
        shell_snapshot=shell_snapshot,
        state_export=state_export,
        memory_review_export=memory_review_export,
        safe_shutdown=safe_shutdown,
        phase10_turn_state=phase10_turn_state,
        phase11_cycle_state=phase11_cycle_state,
        phase12_cycle_state=phase12_cycle_state,
        phase14_shell=phase14_shell,
        prior_turn=prior_turn,
        recent_turns=list(recent_turns or []),
    )

    phase7_engine = ConversationTurnEngine()
    provisional_intake = phase7_engine.intake.build_record(
        conversation_id=conversation_id,
        turn_id=turn_id,
        raw_text=question_text,
        active_context_refs=[],
    )
    provisional_interpretation = phase7_engine.interpretation.build_snapshot(intake_record=provisional_intake)
    provisional_class = _provisional_question_class(question_text)
    candidate_lines = _select_candidate_lines(
        question_text=question_text,
        provisional_class=provisional_class,
        lines=source_corpus,
        prior_turn=prior_turn,
    )
    derived_question_class = _derive_question_class(
        question_text=question_text,
        phase7_interpretation_state=provisional_interpretation.to_dict(),
        candidate_lines=candidate_lines,
    )
    question_class, follow_up_bound, follow_up_binding = _bind_follow_up_class(
        question_text=question_text,
        derived_class=derived_question_class,
        prior_turn=prior_turn,
        recent_turns=list(recent_turns or []),
    )
    candidate_lines = _select_candidate_lines(
        question_text=question_text,
        provisional_class=question_class,
        lines=source_corpus,
        prior_turn=prior_turn,
    )
    if not candidate_lines:
        candidate_lines = _fallback_candidate_lines(
            question_class=question_class,
            lines=source_corpus,
        )
    target_domain = str(provisional_interpretation.target_domain_hint or DEFAULT_TARGET_DOMAIN)
    route = _build_phase3_route(
        question_class=question_class,
        phase14_shell=phase14_shell,
        profile=PROFILE_NAME,
    )
    phase4_state = _build_phase4_state(
        question_text=question_text,
        conversation_id=conversation_id,
        turn_id=turn_id,
        question_class=question_class,
        candidate_lines=candidate_lines,
        route=route,
        shell_snapshot=shell_snapshot,
        prior_turn=prior_turn,
        recent_turns=list(recent_turns or []),
    )
    phase5_state = _build_phase5_state(
        question_text=question_text,
        question_class=question_class,
        target_domain=target_domain,
        phase4_state=phase4_state,
    )
    phase6_state = _build_phase6_state(
        phase4_state=phase4_state,
        phase5_state=phase5_state,
    )

    active_context_refs = [
        *route["route_refs"],
        *[line.ref for _, line in candidate_lines[:4]],
    ]
    phase7_turn = _build_phase7_state(
        question_text=question_text,
        question_class=question_class,
        conversation_id=conversation_id,
        turn_id=turn_id,
        active_context_refs=active_context_refs,
        phase4_state=phase4_state,
        phase5_state=phase5_state,
        phase6_state=phase6_state,
    )
    phase8_turn = ScienceWorldTurnEngine().run_turn(
        intake_state=phase7_turn["intake"],
        question_interpretation_state=phase7_turn["interpretation"],
        support_state_resolution_state=phase7_turn["support_resolution"],
        target_domain_registry_state=phase6_state["target_domain_registry_state"],
        world_model_state=phase6_state["world_model_state"],
        what_if_simulation_state=phase6_state["what_if_simulation_state"],
        usefulness_scoring_state=phase6_state["usefulness_state"],
        continuity_memory_state=phase4_state["continuity_memory_state"],
        working_memory_state=phase4_state["working_memory_state"],
        memory_review_state=phase4_state["memory_review_state"],
        support_selection_result=phase5_state["support_selection_result"],
        answer_contract_state=phase7_turn["answer_contract"],
    )
    phase9_turn = RichExpressionTurnEngine().run_turn(
        intake_state=phase7_turn["intake"],
        question_interpretation_state=phase7_turn["interpretation"],
        support_state_resolution_state=phase7_turn["support_resolution"],
        utterance_plan_state=phase7_turn["utterance_plan"],
        answer_contract_state=phase7_turn["answer_contract"],
        science_world_turn_state=phase8_turn.to_dict(),
        anti_generic_filler_state=phase7_turn["guardrail_result"],
    )
    phase10_turn = MetaCognitionTurnEngine().run_turn(
        support_state_resolution_state=phase7_turn["support_resolution"],
        answer_contract_state=phase7_turn["answer_contract"],
        self_knowledge_surface_state=phase7_turn["self_knowledge"],
        science_world_turn_state=phase8_turn.to_dict(),
        rich_expression_turn_state=phase9_turn.to_dict(),
        continuity_memory_state=phase4_state["continuity_memory_state"],
    )

    selected_support_lines = _selected_support_lines(
        candidate_lines=candidate_lines,
        phase5_state=phase5_state,
        phase4_state=phase4_state,
    )
    response = _compose_response(
        question_class=question_class,
        question_text=question_text,
        shell_snapshot=shell_snapshot,
        route=route,
        support_lines=selected_support_lines,
        phase7_turn_state=phase7_turn,
        prior_turn=prior_turn,
        recent_turns=list(recent_turns or []),
        follow_up_binding=follow_up_binding,
    )
    response = _apply_phase10_guardrails(
        question_class=question_class,
        response=response,
        phase10_turn_state=phase10_turn.to_dict(),
    )
    response = _attach_answer_metadata(
        question_class=question_class,
        response=response,
    )

    local_truth_refs = bounded_unique(
        [line.ref for _, line in selected_support_lines],
        ceiling=12,
        field_name="interactive_local_truth_refs",
        allow_empty=True,
    )
    source_set_used = bounded_unique(
        [line.source_id for _, line in selected_support_lines],
        ceiling=8,
        field_name="interactive_source_set_used",
        allow_empty=True,
    )
    phase2_evidence = _build_phase2_evidence(
        conversation_id=conversation_id,
        turn_id=turn_id,
        phase7_turn_state=phase7_turn,
        final_response=response,
        local_truth_refs=local_truth_refs,
    )

    used_source_ids = {line.source_id for _, line in selected_support_lines}
    phase6_used = question_class in {"contradiction", "current_world", "comparison_planning"} or (
        question_class == "reasoning_math" and response["next_action"] == "answer"
    )
    phase8_used = question_class in {"current_world", "comparison_planning"} and response["next_action"] in {"answer", "clarify"}
    phase9_used = response["final_answer_mode"] in {"grounded_fact", "derived_explanation", "derived_estimate", "clarify"} and question_class not in {"unsupported"}
    phase10_used = question_class in {"contradiction", "current_world", "support_diagnostics", "reasoning_math"} or follow_up_bound or response["next_action"] != "answer"
    phase11_used = "phase11_overlay" in used_source_ids
    phase12_used = "phase12_overlay" in used_source_ids
    memory_consulted = bool(selected_support_lines)
    graph_support_consulted = bool(phase5_state["support_selection_result"].get("selected_candidate_ids", []))
    simulation_world_model_consulted = phase6_used and question_class in {"current_world", "comparison_planning", "contradiction"}
    critique_diagnosis_fired = phase10_used and bool(phase10_turn.overlay_contract.diagnosis_ref)
    phase15_turn_evidence_ref = _phase15_turn_evidence_relpath(
        session_id=str(shell_snapshot["session_id"]),
        turn_id=turn_id,
    )
    phase_usage_raw = {
        "phase_2": {
            "used": True,
            "event_count": phase2_evidence["event_count"],
            "replay_id": phase2_evidence["replay_id"],
            "trace_record_count": len(phase2_evidence["trace_export"]),
        },
        "phase_3": {
            "used": True,
            "route_families": list(route["family_order"]),
            "selected_cell_ids": list(route["selected_cell_ids"]),
            "selected_tissue_ids": list(route["selected_tissue_ids"]),
        },
        "phase_4": {
            "used": True,
            "continuity_anchor_count": len(phase4_state["continuity_memory_state"]["anchors"]),
            "semantic_entry_count": len(phase4_state["semantic_memory_state"]["entries"]),
            "procedural_entry_count": len(phase4_state["procedural_memory_state"]["entries"]),
        },
        "phase_5": {
            "used": True,
            "selected_candidate_ids": list(phase5_state["support_selection_result"].get("selected_candidate_ids", [])),
            "descriptor_node_count": len(phase5_state["descriptor_graph_state"]["nodes"]),
            "concept_node_count": len(phase5_state["concept_graph_state"]["nodes"]),
            "skill_node_count": len(phase5_state["skill_graph_state"]["nodes"]),
        },
        "phase_6": {
            "used": phase6_used,
            "world_model_hash": phase6_state["world_model_state"]["snapshot_hash"],
            "candidate_future_hash": phase6_state["candidate_future_state"]["snapshot_hash"],
            "simulation_hash": phase6_state["what_if_simulation_state"]["snapshot_hash"],
            "usefulness_hash": phase6_state["usefulness_state"]["snapshot_hash"],
        },
        "phase_7": {
            "used": True,
            "question_category": phase7_turn["interpretation"]["question_category"],
            "support_state": phase7_turn["support_resolution"]["support_state"],
            "next_action": phase7_turn["support_resolution"]["next_action"],
            "answer_contract_hash": phase7_turn["answer_contract"]["contract_hash"],
        },
        "phase_8": {
            "used": phase8_used,
            "entity_request_hash": phase8_turn.entity_request_inference.inference_hash,
            "reasoning_summary_hash": phase8_turn.visible_reasoning_summary.summary_hash,
        },
        "phase_9": {
            "used": phase9_used,
            "selected_lane": phase9_turn.selected_lane.value,
            "overlay_hash": phase9_turn.overlay_contract.contract_hash,
        },
        "phase_10": {
            "used": phase10_used,
            "selected_outcome": phase10_turn.overlay_contract.selected_outcome.value,
            "diagnosis_ref": phase10_turn.overlay_contract.diagnosis_ref,
        },
        "phase_11": {
            "used": phase11_used,
            "read_only_context": True,
            "monitoring_ref_count": len(phase11_cycle_state.get("overlay_contract", {}).get("monitoring_refs", [])),
        },
        "phase_12": {
            "used": phase12_used,
            "read_only_context": True,
            "selected_gap_count": len(phase12_cycle_state.get("overlay_contract", {}).get("selected_gap_ids", [])),
        },
        "phase_13": {
            "used": True,
            "session_id": shell_snapshot["session_id"],
            "shell_snapshot_hash": shell_snapshot["snapshot_hash"],
        },
        "phase_14": {
            "used": True,
            "profile": route["profile"],
            "budget_receipt_hash": route["budget"]["receipt_hash"],
            "budget_state": route["budget"]["budget_state"],
            "selected_active_cell_count": route["budget"]["selected_active_cell_count"],
        },
        "phase_15": {
            "used": True,
            "turn_evidence_ref": phase15_turn_evidence_ref,
            "review_ready_fields_present": True,
        },
    }
    proof_record_written = True
    phase15_turn_evidence_written_at: str | None = None
    phase15_turn_evidence_hash: str | None = None
    phase_results = _build_phase_results(
        question_class=question_class,
        follow_up_bound=follow_up_bound,
        candidate_lines=candidate_lines,
        local_truth_refs=local_truth_refs,
        route=route,
        phase2_evidence=phase2_evidence,
        phase4_state=phase4_state,
        phase5_state=phase5_state,
        phase6_state=phase6_state,
        phase7_turn=phase7_turn,
        phase8_turn=phase8_turn,
        phase9_turn=phase9_turn,
        phase10_turn=phase10_turn,
        phase11_cycle_state=phase11_cycle_state,
        phase12_cycle_state=phase12_cycle_state,
        shell_snapshot=shell_snapshot,
        response=response,
        phase_usage_raw=phase_usage_raw,
        phase15_turn_evidence_ref=phase15_turn_evidence_ref,
        proof_record_written=proof_record_written,
    )
    follow_up_detected = follow_up_binding.detected
    follow_up_binding_success = follow_up_binding.success
    follow_up_anchor_turn_id = follow_up_binding.anchor_turn_id
    follow_up_binding_confidence = round(follow_up_binding.confidence, 2)
    follow_up_binding_reason = follow_up_binding.reason
    phase_usage = {}
    for phase_result in phase_results:
        phase_key = f"phase_{phase_result['phase_id']}"
        legacy_summary = dict(phase_usage_raw[phase_key])
        phase_usage[phase_key] = {
            **legacy_summary,
            "used": phase_result["status"] == "used",
            "status": phase_result["status"],
            "reason": phase_result["reason"],
            "inputs_used": phase_result["inputs_used"],
            "outputs_added": phase_result["outputs_added"],
            "support_delta": phase_result["support_delta"],
            "refs_used": phase_result["refs_used"],
            "state_changed": phase_result["state_changed"],
        }
    phases_exercised = [result["phase_id"] for result in phase_results if result["status"] == "used"]
    phase_chain_phase_ids = [result["phase_id"] for result in phase_results]
    phase_chain_completed = phase_chain_phase_ids == list(range(2, 16))
    phases_used_count = sum(1 for result in phase_results if result["status"] == "used")
    phases_no_op_count = sum(1 for result in phase_results if result["status"] == "no_op")
    phases_blocked_count = sum(1 for result in phase_results if result["status"] == "blocked")
    phases_insufficient_input_count = sum(
        1 for result in phase_results if result["status"] == "insufficient_input"
    )

    payload = {
        "schema": INTERACTIVE_TURN_SCHEMA,
        "session_id": shell_snapshot["session_id"],
        "conversation_id": conversation_id,
        "turn_id": turn_id,
        "question_text": question_text,
        "request_text": question_text,
        "question_class": question_class,
        "extracted_target": response.get("extracted_target"),
        "target_grounded": response.get("target_grounded"),
        "followup_detected": follow_up_detected,
        "followup_intent": follow_up_binding.intent,
        "followup_anchor_turn_id": follow_up_anchor_turn_id,
        "followup_binding_confidence": follow_up_binding_confidence,
        "followup_binding_reason": follow_up_binding_reason,
        "followup_binding_success": follow_up_binding_success,
        "phase7_question_category": phase7_turn["interpretation"]["question_category"],
        "follow_up_bound": follow_up_bound,
        "derived_question_class": derived_question_class,
        "support_state": response["support_state"],
        "final_support_state": response["support_state"],
        "knowledge_gap_reason": response["knowledge_gap_reason"],
        "next_action": response["next_action"],
        "answer_mode": response["answer_mode"],
        "uncertainty_band": response["uncertainty_band"],
        "live_measurement_required": response["live_measurement_required"],
        "final_answer_mode": response["final_answer_mode"],
        "response_kind": response["response_kind"],
        "abstain_or_answer": (
            "answer"
            if response["final_answer_mode"] in {"grounded_fact", "derived_explanation", "derived_estimate", "hypothesis"}
            else "abstain"
        ),
        "response_text": response["response_text"],
        "final_response": response["response_text"],
        "local_truth_refs": list(local_truth_refs),
        "source_set_used": list(source_set_used),
        "support_snippets": [
            {
                "ref": line.ref,
                "text": line.text,
                "score": score,
            }
            for score, line in selected_support_lines
        ],
        "selected_candidate_ids": list(phase5_state["support_selection_result"].get("selected_candidate_ids", [])),
        "phase_results": phase_results,
        "phase_chain_phase_ids": phase_chain_phase_ids,
        "phase_chain_completed": phase_chain_completed,
        "phases_exercised": phases_exercised,
        "phases_used_count": phases_used_count,
        "phases_no_op_count": phases_no_op_count,
        "phases_blocked_count": phases_blocked_count,
        "phases_insufficient_input_count": phases_insufficient_input_count,
        "phase_usage": phase_usage,
        "memory_consulted": memory_consulted,
        "graph_support_consulted": graph_support_consulted,
        "simulation_world_model_consulted": simulation_world_model_consulted,
        "critique_diagnosis_fired": critique_diagnosis_fired,
        "final_critique_complete": True,
        "phase15_turn_evidence_ref": phase15_turn_evidence_ref,
        "phase15_turn_evidence_hash": phase15_turn_evidence_hash,
        "phase15_turn_evidence_written_at": phase15_turn_evidence_written_at,
        "proof_record_written": proof_record_written,
        "final_answer_released_after_full_chain": phase_chain_completed,
        "phase2_trace_record_count": len(phase2_evidence["trace_export"]),
        "phase2_replay_match": bool(phase2_evidence["replay_verification"]["replay_match"]),
        "phase14_profile": route["profile"],
        "phase14_budget_state": route["budget"]["budget_state"],
        "phase14_budget_allowed": bool(route["budget"]["allowed"]),
        "phase14_selected_cell_count": route["budget"]["selected_active_cell_count"],
        "phase14_selected_tissue_count": route["budget"]["selected_active_tissue_count"],
        "phase10_selected_outcome": phase10_turn.overlay_contract.selected_outcome.value,
        "phase10_public_explanation": phase10_turn.overlay_contract.public_explanation,
        "phase11_read_only_refs": list(phase11_cycle_state.get("overlay_contract", {}).get("monitoring_refs", [])),
        "phase12_read_only_refs": list(phase12_cycle_state.get("overlay_contract", {}).get("selected_gap_ids", [])),
        "local_sources_consulted": [
            {
                "source_id": line.source_id,
                "path": line.path,
                "line_number": line.line_number,
                "ref": line.ref,
            }
            for _, line in selected_support_lines
        ],
        "phase2_evidence": {
            "trace_export": phase2_evidence["trace_export"],
            "replay_verification": phase2_evidence["replay_verification"],
            "workspace_state_export": phase2_evidence["workspace_state_export"],
            "workspace_memory_review_export": phase2_evidence["workspace_memory_review_export"],
        },
    }
    evidence_payload = {
        "turn_id": turn_id,
        "session_id": payload["session_id"],
        "conversation_id": payload["conversation_id"],
        "request_text": payload["request_text"],
        "question_class": payload["question_class"],
        "derived_question_class": payload["derived_question_class"],
        "followup_detected": payload["followup_detected"],
        "followup_intent": payload["followup_intent"],
        "followup_anchor_turn_id": payload["followup_anchor_turn_id"],
        "followup_binding_confidence": payload["followup_binding_confidence"],
        "followup_binding_reason": payload["followup_binding_reason"],
        "followup_binding_success": payload["followup_binding_success"],
        "follow_up_bound": payload["follow_up_bound"],
        "support_state": payload["support_state"],
        "next_action": payload["next_action"],
        "answer_mode": payload["answer_mode"],
        "final_answer_mode": payload["final_answer_mode"],
        "uncertainty_band": payload["uncertainty_band"],
        "local_truth_refs": payload["local_truth_refs"],
        "source_set_used": payload["source_set_used"],
        "local_sources_consulted": payload["local_sources_consulted"],
        "support_snippets": payload["support_snippets"],
        "phases_exercised": payload["phases_exercised"],
        "phase_results": payload["phase_results"],
        "phase_usage": payload["phase_usage"],
        "memory_consulted": payload["memory_consulted"],
        "graph_support_consulted": payload["graph_support_consulted"],
        "simulation_world_model_consulted": payload["simulation_world_model_consulted"],
        "critique_diagnosis_fired": payload["critique_diagnosis_fired"],
        "final_response": payload["final_response"],
    }
    try:
        proof_record_written, phase15_turn_evidence_written_at, phase15_turn_evidence_hash = _write_phase15_turn_evidence(
            rel_path=phase15_turn_evidence_ref,
            payload=evidence_payload,
        )
    except OSError as exc:
        proof_record_written = False
        phase15_turn_evidence_written_at = None
        phase15_turn_evidence_hash = stable_hash_payload({"error": str(exc), "turn_id": turn_id})
    phase_usage_raw["phase_15"]["used"] = proof_record_written
    phase_usage_raw["phase_15"]["review_ready_fields_present"] = proof_record_written
    phase_usage_raw["phase_15"]["turn_evidence_hash"] = phase15_turn_evidence_hash
    phase_usage_raw["phase_15"]["turn_evidence_written_at"] = phase15_turn_evidence_written_at
    phase_results = _build_phase_results(
        question_class=question_class,
        follow_up_bound=follow_up_bound,
        candidate_lines=candidate_lines,
        local_truth_refs=local_truth_refs,
        route=route,
        phase2_evidence=phase2_evidence,
        phase4_state=phase4_state,
        phase5_state=phase5_state,
        phase6_state=phase6_state,
        phase7_turn=phase7_turn,
        phase8_turn=phase8_turn,
        phase9_turn=phase9_turn,
        phase10_turn=phase10_turn,
        phase11_cycle_state=phase11_cycle_state,
        phase12_cycle_state=phase12_cycle_state,
        shell_snapshot=shell_snapshot,
        response=response,
        phase_usage_raw=phase_usage_raw,
        phase15_turn_evidence_ref=phase15_turn_evidence_ref,
        proof_record_written=proof_record_written,
    )
    phase_usage = {}
    for phase_result in phase_results:
        phase_key = f"phase_{phase_result['phase_id']}"
        legacy_summary = dict(phase_usage_raw[phase_key])
        phase_usage[phase_key] = {
            **legacy_summary,
            "used": phase_result["status"] == "used",
            "status": phase_result["status"],
            "reason": phase_result["reason"],
            "inputs_used": phase_result["inputs_used"],
            "outputs_added": phase_result["outputs_added"],
            "support_delta": phase_result["support_delta"],
            "refs_used": phase_result["refs_used"],
            "state_changed": phase_result["state_changed"],
        }
    phases_exercised = [result["phase_id"] for result in phase_results if result["status"] == "used"]
    phase_chain_phase_ids = [result["phase_id"] for result in phase_results]
    phase_chain_completed = phase_chain_phase_ids == list(range(2, 16))
    phases_used_count = sum(1 for result in phase_results if result["status"] == "used")
    phases_no_op_count = sum(1 for result in phase_results if result["status"] == "no_op")
    phases_blocked_count = sum(1 for result in phase_results if result["status"] == "blocked")
    phases_insufficient_input_count = sum(
        1 for result in phase_results if result["status"] == "insufficient_input"
    )
    payload["phase_results"] = phase_results
    payload["phase_chain_phase_ids"] = phase_chain_phase_ids
    payload["phase_chain_completed"] = phase_chain_completed
    payload["phases_exercised"] = phases_exercised
    payload["phases_used_count"] = phases_used_count
    payload["phases_no_op_count"] = phases_no_op_count
    payload["phases_blocked_count"] = phases_blocked_count
    payload["phases_insufficient_input_count"] = phases_insufficient_input_count
    payload["phase_usage"] = phase_usage
    payload["phase15_turn_evidence_hash"] = phase15_turn_evidence_hash
    payload["phase15_turn_evidence_written_at"] = phase15_turn_evidence_written_at
    payload["proof_record_written"] = proof_record_written
    payload["final_answer_released_after_full_chain"] = phase_chain_completed and proof_record_written
    return {
        **payload,
        "turn_hash": stable_hash_payload(payload),
    }
