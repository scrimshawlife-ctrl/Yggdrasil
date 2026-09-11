"""T0 rule classifier. Route atoms to yggdrasil.route.v0."""

from __future__ import annotations

from typing import Any

SCHEMA = "yggdrasil.route.v0"

LANES = (
    "ingest",
    "belief",
    "replay",
    "phase",
    "viz",
    "situation",
    "codegen",
    "runtime_gate",
)

SCANS = {
    "DEPENDENCY_SCAN": "dependency",
    "LANE_BOUNDARY_SCAN": "lane_boundary",
    "EDGE_VALIDATION": "edge_validation",
    "UNKNOWN_NODE_GATE": "unknown_node",
}

FAMILY_TO_LANE = {
    "INGEST": "ingest",
    "BELIEF": "belief",
    "REPLAY": "replay",
    "PHASE": "phase",
    "VIZ": "viz",
    "SITUATION": "situation",
    "CODEGEN": "codegen",
    "RUNTIME_GATE": "runtime_gate",
}

_SCAN_CLASSES = frozenset(
    {"dependency", "lane_boundary", "edge_validation", "unknown_node", "none"}
)

FORECAST_PAYLOADS = {"forecast_request", "settled_forecast"}
PROMOTE_PAYLOADS = {"promotion_request", "canon_promote"}


def _lane_from_namespace(namespace: Any) -> str | None:
    if not isinstance(namespace, str):
        return None
    ns = namespace.strip().lower()
    if ns.startswith("yggdrasil."):
        tail = ns.split(".", 1)[1]
        if tail in LANES:
            return tail
        return None
    if ns in LANES:
        return ns
    return None


def _lane_from_rune(rune_id: Any) -> tuple[str | None, str | None]:
    if not isinstance(rune_id, str):
        return None, None
    rid = rune_id.strip().upper().replace("-", "_")
    scan = None
    for token, name in SCANS.items():
        if token in rid:
            scan = name
            break
    lane = None
    if rid.startswith("RUNE."):
        parts = rid.split(".")
        if len(parts) >= 2 and parts[1] in FAMILY_TO_LANE:
            lane = FAMILY_TO_LANE[parts[1]]
    return lane, scan


def _scan_class(candidate: object) -> str:
    if isinstance(candidate, str) and candidate in _SCAN_CLASSES:
        return candidate
    return "none"


def _is_bare_yggdrasil(atom: dict[str, Any]) -> bool:
    """True when a YGGDRASIL rune has no pipeline namespace or claimed lane."""
    rune_id = atom.get("rune_id")
    return (
        isinstance(rune_id, str)
        and "YGGDRASIL" in rune_id.upper()
        and not atom.get("namespace")
        and not atom.get("claimed_lane")
    )


def _refuse(atom: dict[str, Any], failure: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "route_class": "unknown",
        "scan_class": "none",
        "integrity": "NOT_COMPUTABLE",
        "forecast_eligible": False,
        "can_promote": False,
        "phenomenal": False,
        "brier": None,
        "epistemic": "NOT_COMPUTABLE",
        "failure": failure,
        "corpus_ref": atom.get("corpus_ref"),
    }


def classify(atom: dict[str, Any]) -> dict[str, Any]:
    payload = atom.get("payload_class")
    if payload in FORECAST_PAYLOADS or atom.get("forecast_eligible") is True:
        frame = _refuse(atom, "SPECIALIST_LANE_VIOLATION")
        frame["scan_class"] = "none"
        return frame
    if payload in PROMOTE_PAYLOADS or atom.get("can_promote") is True:
        frame = _refuse(atom, "REJECT_OR_SHADOW")
        return frame

    ns_lane = _lane_from_namespace(atom.get("namespace"))
    rune_lane, rune_scan = _lane_from_rune(atom.get("rune_id"))
    claimed = atom.get("claimed_lane")
    if isinstance(claimed, str):
        claimed = claimed.strip().lower()
        if claimed not in LANES:
            claimed = None
    else:
        claimed = None

    lanes = [x for x in (ns_lane, rune_lane, claimed) if x]
    if not lanes and not atom.get("namespace") and not atom.get("rune_id") and not atom.get("claimed_lane"):
        return _refuse(atom, "NOT_COMPUTABLE")

    unique = set(lanes)
    if len(unique) > 1:
        route_class = ns_lane or rune_lane or claimed or "unknown"
        scan_class = "lane_boundary"
        integrity = "SHIFTING"
        epistemic = "INFERRED"
        failure = "LANE_MISMATCH"
    elif len(unique) == 1:
        route_class = unique.pop()
        scan_class = _scan_class(rune_scan or atom.get("scan_hint") or "none")
        integrity = "ALIGNED"
        epistemic = "OBSERVED" if atom.get("corpus_ref") or atom.get("namespace") else "INFERRED"
        failure = None
    elif _is_bare_yggdrasil(atom):
        route_class = "runtime_gate"
        scan_class = _scan_class(rune_scan or atom.get("scan_hint") or "none")
        integrity = "ALIGNED"
        epistemic = "OBSERVED" if atom.get("corpus_ref") else "INFERRED"
        failure = None
    else:
        route_class = "unknown"
        scan_class = "unknown_node"
        integrity = "NOT_COMPUTABLE"
        epistemic = "NOT_COMPUTABLE"
        failure = "UNKNOWN_NODE_GATE"

    hint = atom.get("scan_hint")
    if hint in {"dependency", "lane_boundary", "edge_validation", "unknown_node"} and scan_class == "none":
        scan_class = hint

    if route_class == "unknown" and failure is None:
        scan_class = "unknown_node"
        integrity = "NOT_COMPUTABLE"
        epistemic = "NOT_COMPUTABLE"
        failure = "UNKNOWN_NODE_GATE"

    return {
        "schema": SCHEMA,
        "route_class": route_class,
        "scan_class": scan_class,
        "integrity": integrity,
        "forecast_eligible": False,
        "can_promote": False,
        "phenomenal": False,
        "brier": None,
        "epistemic": epistemic,
        "failure": failure,
        "corpus_ref": atom.get("corpus_ref"),
    }
