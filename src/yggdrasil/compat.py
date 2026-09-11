"""Export helper. No Abraxas import."""

from __future__ import annotations

from typing import Any


def frame_to_route_packet(frame: dict[str, Any]) -> dict[str, Any]:
    packet = {
        "packet": "yggdrasil.route.v0",
        "specialist": "yggdrasil.topology",
        "route_class": frame.get("route_class"),
        "scan_class": frame.get("scan_class"),
        "integrity": frame.get("integrity"),
        "forecast_eligible": False,
        "can_promote": False,
        "phenomenal": False,
        "brier": None,
        "epistemic": frame.get("epistemic"),
        "failure": frame.get("failure"),
        "corpus_ref": frame.get("corpus_ref"),
    }
    if frame.get("forecast_eligible") is True:
        packet["failure"] = "SPECIALIST_LANE_VIOLATION"
        packet["integrity"] = "NOT_COMPUTABLE"
    return packet
