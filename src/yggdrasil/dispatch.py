"""SHADOW Spec 009 rules dispatcher. No weights. No Hub."""

from __future__ import annotations

from typing import Any

from yggdrasil.adapt import adapt
from yggdrasil.classify import classify

FOREIGN = {
    "slang_atom": ("R001", ["hyperlex.hyperlexical"]),
    "tradition_atom": ("R002", ["athanor.structure"]),
    "sign_atom": ("R006", ["semion.triad"]),
    "corpus_atom": ("R006B", ["semion.triad"]),
    "settled_forecast": ("R004B", ["abx.brier"]),
}

# Spec 013 / 013A. Classify only. Geometry stays in Sigil-Forge.
CONSTRUCT = {
    "construct_atom": ("R011", ["sigil.forge.construct"], "FOREIGN_SPECIALIST"),
    "intent_glyph": ("R011", ["sigil.forge.construct"], "FOREIGN_SPECIALIST"),
    "sigil_request": ("R011", ["sigil.forge.construct"], "FOREIGN_SPECIALIST"),
    "mixed_tradition_construct": (
        "R011B",
        ["athanor.structure", "sigil.forge.construct"],
        "CHAIN",
    ),
    "mixed_sign_construct": (
        "R011C",
        ["semion.triad", "sigil.forge.construct"],
        "CHAIN",
    ),
    "noctis_sig": (
        "R011D",
        ["noctis.interpret", "sigil.forge.construct"],
        "CHAIN",
    ),
}


def _packet_class(req: dict[str, Any]) -> str:
    explicit = req.get("packet") or req.get("payload_class")
    if explicit:
        return str(explicit)
    if req.get("forecast_eligible") is True:
        return "forecast_request"
    raw = str(req.get("namespace") or req.get("name") or "")
    tail = raw.split(".")[-1].lower().replace("-", "_") if raw else ""
    if tail in {"pse_forecast", "memetic_futurecast", "forecast_request", "settled_forecast"}:
        return "forecast_request" if tail != "settled_forecast" else "settled_forecast"
    if raw.endswith(".forecast") or tail == "forecast":
        return "unknown_namespace"
    if req.get("namespace") or req.get("rune_id") or req.get("claimed_lane") or req.get("name"):
        return "route_atom"
    return "other"


def dispatch(req: dict[str, Any]) -> dict[str, Any]:
    packet = _packet_class(req)

    if packet in {"forecast_request"}:
        return {
            "rule": "R004",
            "packet": packet,
            "specialists": [],
            "result": "NOT_COMPUTABLE",
            "failure": "SPECIALIST_LANE_VIOLATION",
            "forecast_eligible": False,
            "frame": None,
        }

    if packet in CONSTRUCT:
        rule, specs, result = CONSTRUCT[packet]
        return {
            "rule": rule,
            "packet": packet,
            "specialists": specs,
            "result": result,
            "failure": None,
            "forecast_eligible": False,
            "home": "yggdrasil.viz",
            "frame": None,
        }

    if packet in FOREIGN:
        rule, specs = FOREIGN[packet]
        return {
            "rule": rule,
            "packet": packet,
            "specialists": specs,
            "result": "FOREIGN_SPECIALIST",
            "failure": None,
            "forecast_eligible": False,
            "frame": None,
        }

    if packet == "unknown_namespace" or packet == "unknown specialist id":
        atom = adapt(req) if packet == "unknown_namespace" else None
        frame = classify(atom or req)
        return {
            "rule": "R010" if packet == "unknown_namespace" else "R005",
            "packet": packet,
            "specialists": ["yggdrasil.topology"] if packet == "unknown_namespace" else [],
            "result": "NOT_COMPUTABLE",
            "failure": frame.get("failure") or "UNKNOWN_NODE_GATE",
            "forecast_eligible": False,
            "frame": frame,
        }

    if packet == "route_atom":
        atom = adapt(req)
        frame = classify(atom)
        if frame.get("failure") == "SPECIALIST_LANE_VIOLATION":
            return {
                "rule": "R004",
                "packet": "forecast_request",
                "specialists": [],
                "result": "NOT_COMPUTABLE",
                "failure": "SPECIALIST_LANE_VIOLATION",
                "forecast_eligible": False,
                "frame": frame,
            }
        if frame.get("failure") == "UNKNOWN_NODE_GATE":
            return {
                "rule": "R010",
                "packet": "unknown_namespace",
                "specialists": ["yggdrasil.topology"],
                "result": "NOT_COMPUTABLE",
                "failure": "UNKNOWN_NODE_GATE",
                "forecast_eligible": False,
                "frame": frame,
            }
        return {
            "rule": "R009",
            "packet": "route_atom",
            "specialists": ["yggdrasil.topology"],
            "result": frame.get("integrity"),
            "failure": frame.get("failure"),
            "forecast_eligible": False,
            "frame": frame,
        }

    return {
        "rule": "R999",
        "packet": packet,
        "specialists": [],
        "result": "LAYER_ENGINE_ONLY",
        "failure": None,
        "forecast_eligible": False,
        "frame": None,
    }
