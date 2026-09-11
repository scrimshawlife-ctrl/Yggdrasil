from __future__ import annotations

import importlib.util
from pathlib import Path

from yggdrasil.adapt import adapt
from yggdrasil.classify import classify

BUILDER = Path(__file__).resolve().parents[1] / "fixtures" / "seed" / "build_eval_mapping_v2.py"
FORBIDDEN = {"shadow", "governance", "governance_shadow", "projection", "forecast_gated", "forecast", "scoring"}


def _load_builder():
    spec = importlib.util.spec_from_file_location("build_eval_mapping_v2", BUILDER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _rows():
    return _load_builder().rows()


def test_eval_has_pipeline_and_node_grains() -> None:
    rows = _rows()
    assert len(rows) == 106
    assert sum(1 for r in rows if r["grain"] == "pipeline") == 20
    assert sum(1 for r in rows if r["grain"] == "node") == 86


def test_gold_never_uses_v2_node_lane() -> None:
    for row in _rows():
        assert row["v2_node_lane_is_not_route_class"] is True
        assert row["gold_route_class"] not in FORBIDDEN
        claimed = row.get("claimed_lane")
        if claimed is not None:
            assert claimed not in FORBIDDEN


def test_forecast_rows_are_r004() -> None:
    rows = [r for r in _rows() if r["name"] in {"pse_forecast", "memetic_futurecast"}]
    assert rows
    assert all(r["gold_rule"] == "R004" for r in rows)
    assert all(r["payload_class"] == "forecast_request" for r in rows)


def test_neon_genie_is_r010_until_name_row() -> None:
    rows = [r for r in _rows() if r["name"] == "neon_genie_ideation"]
    assert rows
    assert all(r["gold_rule"] == "R010" for r in rows)


def test_adapt_classify_matches_gold() -> None:
    for row in _rows():
        atom = adapt({"payload_class": row["payload_class"], "name": row["name"], "rune_id": row["rune_id"], "claimed_lane": row["claimed_lane"], "corpus_ref": row.get("node_id") or row["name"]})
        frame = classify({"payload_class": atom["payload_class"], "namespace": atom.get("namespace"), "rune_id": atom.get("rune_id"), "claimed_lane": atom.get("claimed_lane"), "scan_hint": atom.get("scan_hint"), "corpus_ref": atom.get("corpus_ref")})
        assert frame["route_class"] == row["gold_route_class"], row
        assert frame["scan_class"] == row["gold_scan_class"], row
        assert frame["integrity"] == row["gold_integrity"], row
        assert frame["failure"] == row["gold_failure"], row
        assert frame["forecast_eligible"] is False
        assert frame["can_promote"] is False
