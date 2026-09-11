from pathlib import Path

from yggdrasil.adapt import adapt, adapt_jsonl, atoms_only
from yggdrasil.classify import classify


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "seed" / "spine_records.jsonl"


def test_ingest_name_maps():
    atom = adapt({"name": "universal_ingest", "mapping_id": "YGGDRASIL_ROUTE_NAMESPACE_MAPPING_001"})
    assert atom["rejected"] is False
    assert atom["namespace"] == "yggdrasil.ingest"
    assert atom["claimed_lane"] == "ingest"
    frame = classify(atom)
    assert frame["route_class"] == "ingest"
    assert frame["integrity"] == "ALIGNED"


def test_forecast_name_rejected():
    atom = adapt({"name": "pse_forecast"})
    assert atom["rejected"] is True
    assert atom["reject_reason"] == "SPECIALIST_LANE_VIOLATION"
    frame = classify(atom)
    assert frame["failure"] == "SPECIALIST_LANE_VIOLATION"
    assert frame["forecast_eligible"] is False


def test_unknown_mapping_becomes_unknown_node():
    atom = adapt({"name": "hollersports_ticket"})
    assert atom["rejected"] is False
    assert atom["namespace"] == "yggdrasil.hollersports_ticket"
    frame = classify(atom)
    assert frame["scan_class"] == "unknown_node"
    assert frame["failure"] == "UNKNOWN_NODE_GATE"


def test_scan_rune_record():
    atom = adapt({"rune_id": "RUNE.YGGDRASIL.LANE_BOUNDARY_SCAN"})
    assert atom["scan_hint"] == "lane_boundary"
    frame = classify(atom)
    assert frame["scan_class"] == "lane_boundary"
    assert frame["route_class"] == "runtime_gate"


def test_fixture_jsonl():
    rows = adapt_jsonl(FIXTURE)
    kept = atoms_only(rows)
    assert any(r["rejected"] for r in rows)
    assert all(not r.get("rejected") for r in kept)
    assert any(r["claimed_lane"] == "ingest" for r in kept)
