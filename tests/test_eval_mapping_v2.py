from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from yggdrasil.adapt import NAME_TO_LANE, adapt
from yggdrasil.classify import classify

SEED = Path(__file__).resolve().parents[1] / "fixtures" / "seed"
BUILDER = SEED / "build_eval_mapping_v2.py"
JSONL = SEED / "eval_mapping_v2.jsonl"
FORBIDDEN = {"shadow", "governance", "governance_shadow", "projection", "forecast_gated", "forecast", "scoring"}


def _load_builder():
    spec = importlib.util.spec_from_file_location("build_eval_mapping_v2", BUILDER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _rows():
    mod = _load_builder()
    mod.write(JSONL)
    return mod.rows()


def test_builder_uses_adapt_name_map() -> None:
    mod = _load_builder()
    assert mod.NAME_TO_LANE is NAME_TO_LANE


def test_eval_has_pipeline_and_node_grains() -> None:
    rows = _rows()
    assert len(rows) == 106
    assert sum(1 for r in rows if r["grain"] == "pipeline") == 20
    assert sum(1 for r in rows if r["grain"] == "node") == 86
    written = [json.loads(line) for line in JSONL.read_text().splitlines() if line.strip()]
    assert len(written) == 106


def test_gold_never_uses_v2_node_lane() -> None:
    for row in _rows():
        assert row["v2_node_lane_is_not_route_class"] is True
        assert row["inherit_pipeline_lane"] is True
        assert row["gold_route_class"] not in FORBIDDEN
        claimed = row.get("claimed_lane")
        if claimed is not None:
            assert claimed not in FORBIDDEN


def test_forecast_rows_are_r004() -> None:
    rows = [r for r in _rows() if r["name"] in {"pse_forecast", "memetic_futurecast"}]
    assert rows
    assert all(r["gold_rule"] == "R004" for r in rows)
    assert all(r["payload_class"] == "forecast_request" for r in rows)


def test_familiar_ingestion_is_name_mapped_without_route() -> None:
    rows = [r for r in _rows() if r["name"] == "familiar_ingestion"]
    assert len(rows) == 1
    row = rows[0]
    assert row["grain"] == "pipeline"
    assert row["route_file_observed"] is False
    assert row["name_mapped"] is True
    assert row["gold_rule"] == "R009"
    assert row["gold_route_class"] == "ingest"


def test_neon_genie_has_route_file_and_stays_r010() -> None:
    rows = [r for r in _rows() if r["name"] == "neon_genie_ideation"]
    assert rows
    assert all(r["route_file_observed"] is True for r in rows)
    assert all(r["name_mapped"] is False for r in rows)
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
