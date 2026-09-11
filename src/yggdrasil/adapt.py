"""Map live spine records onto route atoms. Spec 002.

Does not scrape. Does not gold-settle. Does not import Abraxas.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

FORECAST_NAMES = frozenset(
    {
        "pse_forecast",
        "memetic_futurecast",
        "forecast",
        "forecast_request",
        "settled_forecast",
    }
)

FORECAST_PAYLOAD = frozenset({"forecast_request", "settled_forecast"})

NAME_TO_LANE = {
    "universal_ingest": "ingest",
    "familiar_ingestion": "ingest",
    "research_intake": "ingest",
    "oracle_signal": "ingest",
    "aal_viz_projection": "viz",
    "operator_review_queue": "runtime_gate",
    "drift_scan": "runtime_gate",
    "v2_hygiene": "runtime_gate",
    "canon_sync": "runtime_gate",
    "alembic_spine": "codegen",
}

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


def _norm(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text or None


def _tail(name: str) -> str:
    lowered = name.strip().lower().replace("-", "_")
    if lowered.startswith("yggdrasil."):
        return lowered.split(".", 1)[1]
    return lowered


def adapt(source: dict[str, Any]) -> dict[str, Any]:
    payload = source.get("payload_class")
    namespace = _norm(source.get("namespace") or source.get("route_id") or source.get("name"))
    rune_id = _norm(source.get("rune_id"))
    claimed = _norm(source.get("claimed_lane") or source.get("lane") or source.get("node_type"))
    tail = _tail(namespace) if namespace else None

    if payload in FORECAST_PAYLOAD or (tail in FORECAST_NAMES) or (claimed in FORECAST_NAMES):
        return {
            "payload_class": payload or "forecast_request",
            "namespace": namespace,
            "rune_id": rune_id,
            "claimed_lane": None,
            "scan_hint": None,
            "corpus_ref": source.get("corpus_ref") or source.get("mapping_id") or source.get("artifact_id"),
            "rejected": True,
            "reject_reason": "SPECIALIST_LANE_VIOLATION",
        }

    lane = None
    if claimed in LANES:
        lane = claimed
    elif tail in LANES:
        lane = tail
    elif tail in NAME_TO_LANE:
        lane = NAME_TO_LANE[tail]

    ns_out = None
    if lane:
        ns_out = f"yggdrasil.{lane}"
    elif namespace:
        ns_out = namespace if namespace.startswith("yggdrasil.") else f"yggdrasil.{tail}"

    scan_hint = source.get("scan_hint") or source.get("scan_class")
    if rune_id and "YGGDRASIL" in rune_id.upper() and not scan_hint:
        rid = rune_id.upper()
        if "DEPENDENCY_SCAN" in rid:
            scan_hint = "dependency"
        elif "LANE_BOUNDARY" in rid:
            scan_hint = "lane_boundary"
        elif "EDGE_VALIDATION" in rid:
            scan_hint = "edge_validation"
        elif "UNKNOWN_NODE" in rid:
            scan_hint = "unknown_node"

    return {
        "payload_class": payload or "route_atom",
        "namespace": ns_out,
        "rune_id": rune_id,
        "claimed_lane": lane,
        "scan_hint": scan_hint if scan_hint in {"dependency", "lane_boundary", "edge_validation", "unknown_node"} else None,
        "corpus_ref": source.get("corpus_ref")
        or source.get("mapping_id")
        or source.get("artifact_id")
        or source.get("pipeline_id")
        or source.get("node_id"),
        "rejected": False,
        "reject_reason": None,
    }


def adapt_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(adapt(json.loads(line)))
    return rows


def atoms_only(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        if row.get("rejected"):
            continue
        out.append(
            {
                "payload_class": row.get("payload_class"),
                "namespace": row.get("namespace"),
                "rune_id": row.get("rune_id"),
                "claimed_lane": row.get("claimed_lane"),
                "scan_hint": row.get("scan_hint"),
                "corpus_ref": row.get("corpus_ref"),
            }
        )
    return out
