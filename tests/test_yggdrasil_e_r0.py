from yggdrasil.classify import classify
from yggdrasil.compat import frame_to_route_packet


def test_ingest_ok():
    frame = classify(
        {
            "namespace": "yggdrasil.ingest",
            "rune_id": "RUNE.INGEST.HANDOFF_BUILD",
            "claimed_lane": "ingest",
            "corpus_ref": "E-R0-ingest",
        }
    )
    assert frame["schema"] == "yggdrasil.route.v0"
    assert frame["route_class"] == "ingest"
    assert frame["integrity"] == "ALIGNED"
    assert frame["forecast_eligible"] is False
    assert frame["can_promote"] is False
    assert frame["brier"] is None
    assert frame["failure"] is None


def test_forecast_refuse():
    frame = classify({"payload_class": "forecast_request", "namespace": "yggdrasil.belief"})
    assert frame["integrity"] == "NOT_COMPUTABLE"
    assert frame["failure"] == "SPECIALIST_LANE_VIOLATION"
    assert frame["forecast_eligible"] is False


def test_promotion_refuse():
    frame = classify({"can_promote": True, "namespace": "yggdrasil.replay"})
    assert frame["failure"] == "REJECT_OR_SHADOW"
    assert frame["can_promote"] is False


def test_unknown_node():
    frame = classify({"namespace": "yggdrasil.forecast"})
    assert frame["route_class"] == "unknown"
    assert frame["scan_class"] == "unknown_node"
    assert frame["failure"] == "UNKNOWN_NODE_GATE"


def test_lane_mismatch():
    frame = classify({"namespace": "yggdrasil.ingest", "claimed_lane": "belief"})
    assert frame["scan_class"] == "lane_boundary"
    assert frame["integrity"] == "SHIFTING"
    assert frame["failure"] == "LANE_MISMATCH"


def test_scan_rune():
    frame = classify({"rune_id": "RUNE.YGGDRASIL.DEPENDENCY_SCAN"})
    assert frame["route_class"] == "runtime_gate"
    assert frame["scan_class"] == "dependency"
    assert frame["forecast_eligible"] is False


def test_empty_not_computable():
    frame = classify({})
    assert frame["failure"] == "NOT_COMPUTABLE"


def test_export_cannot_set_forecast():
    packet = frame_to_route_packet(
        {"route_class": "ingest", "forecast_eligible": True, "integrity": "ALIGNED"}
    )
    assert packet["forecast_eligible"] is False
    assert packet["failure"] == "SPECIALIST_LANE_VIOLATION"
    assert packet["specialist"] == "yggdrasil.topology"
