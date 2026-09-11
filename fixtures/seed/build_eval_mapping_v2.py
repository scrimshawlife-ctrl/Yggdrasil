#!/usr/bin/env python3
"""Build fixtures/seed/eval_mapping_v2.jsonl from compact tables.

v2.0 node.lane is never gold route_class.
"""
from __future__ import annotations

import json
from pathlib import Path

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
FORECAST = {"pse_forecast", "memetic_futurecast"}
PARTIAL = [
    "beatoven_psyfi_integration",
    "familiar_ingestion",
    "hollersports_ticket",
    "level99_content",
    "memetic_futurecast",
    "noctis_dream",
    "phonomicon_artifact",
]
NODES = {
    "universal_ingest": ["ingest.trigger", "ingest.parser|RUNE.PIPELINE.PARSE", "ingest.ir_builder|RUNE.PIPELINE.IR_BUILD", "ingest.conflict_scanner|RUNE.PIPELINE.CONFLICT_SCAN", "ingest.dependency_scan|RUNE.YGGDRASIL.DEPENDENCY_SCAN", "ingest.lane_boundary_scan|RUNE.YGGDRASIL.LANE_BOUNDARY_SCAN", "ingest.edge_validation|RUNE.YGGDRASIL.EDGE_VALIDATION", "ingest.unknown_node_gate|RUNE.YGGDRASIL.UNKNOWN_NODE_GATE", "ingest.validator|RUNE.PIPELINE.VALIDATE", "ingest.receipt"],
    "aal_viz_projection": ["projection.trigger", "projection.parser|RUNE.PIPELINE.PARSE", "projection.ir_builder|RUNE.PIPELINE.IR_BUILD", "projection.aal_viz_projector|RUNE.PIPELINE.AAL_VIZ_PROJECT", "projection.validator|RUNE.PIPELINE.VALIDATE", "projection.receipt"],
    "alembic_spine": ["alembic.trigger", "alembic.route|RUNE.PIPELINE.ROUTE", "alembic.validate|RUNE.PIPELINE.VALIDATE", "alembic.conflict_scan|RUNE.PIPELINE.CONFLICT_SCAN", "alembic.operator_review|RUNE.PIPELINE.OPERATOR_REVIEW", "alembic.not_computable_gate|RUNE.GOVERNANCE.NOT_COMPUTABLE_GATE", "alembic.route_receipt|RUNE.YGGDRASIL.ROUTE_RECEIPT", "alembic.receipt|RUNE.PIPELINE.RECEIPT"],
    "canon_sync": ["canon.trigger", "canon.parser|RUNE.PIPELINE.PARSE", "canon.ir_builder|RUNE.PIPELINE.IR_BUILD", "canon.promotion_lock|RUNE.GOVERNANCE.PROMOTION_LOCK", "canon.mutation_lock|RUNE.GOVERNANCE.RUNTIME_MUTATION_LOCK", "canon.validator|RUNE.PIPELINE.VALIDATE", "canon.canon_sync|RUNE.PIPELINE.CANON_SYNC", "canon.receipt"],
    "drift_scan": ["drift.trigger", "drift.proposal", "drift.overlay", "drift.replay", "drift.validator|RUNE.PIPELINE.VALIDATE", "drift.review|RUNE.PIPELINE.OPERATOR_REVIEW", "drift.receipt"],
    "neon_genie_ideation": ["neon_genie.trigger", "neon_genie.route|RUNE.PIPELINE.ROUTE", "neon_genie.novelty_validate|RUNE.PIPELINE.VALIDATE", "neon_genie.overlap_scan|RUNE.PIPELINE.CONFLICT_SCAN", "neon_genie.operator_packet", "neon_genie.operator_review|RUNE.PIPELINE.OPERATOR_REVIEW", "neon_genie.receipt|RUNE.YGGDRASIL.ROUTE_RECEIPT"],
    "operator_review_queue": ["operator_review.trigger", "operator_review.parser|RUNE.PIPELINE.PARSE", "operator_review.ir_builder|RUNE.PIPELINE.IR_BUILD", "operator_review.validator|RUNE.PIPELINE.VALIDATE", "operator_review.queue_review|RUNE.PIPELINE.OPERATOR_REVIEW", "operator_review.canon_sync|RUNE.PIPELINE.CANON_SYNC", "operator_review.receipt"],
    "oracle_signal": ["oracle_signal.trigger", "oracle_signal.intake", "oracle_signal.processing", "oracle_signal.receipt"],
    "outcome_brier": ["scoring.trigger", "scoring.parser|RUNE.PIPELINE.PARSE", "scoring.ir_builder|RUNE.PIPELINE.IR_BUILD", "scoring.invariance_gate|RUNE.GOVERNANCE.INVARIANCE_GATE", "scoring.validator|RUNE.PIPELINE.VALIDATE", "scoring.receipt"],
    "pse_forecast": ["forecast.trigger", "forecast.parser|RUNE.PIPELINE.PARSE", "forecast.ir_builder|RUNE.PIPELINE.IR_BUILD", "forecast.forecast_gate|RUNE.GOVERNANCE.FORECAST_GATE", "forecast.validator|RUNE.PIPELINE.VALIDATE", "forecast.receipt"],
    "research_drop_validation": ["research_drop.trigger", "research_drop.parser|RUNE.PIPELINE.PARSE", "research_drop.ir_builder|RUNE.PIPELINE.IR_BUILD", "research_drop.invariance_gate|RUNE.GOVERNANCE.INVARIANCE_GATE", "research_drop.validator|RUNE.PIPELINE.VALIDATE", "research_drop.receipt"],
    "research_intake": ["research.intake.trigger", "research.intake.parser|RUNE.PIPELINE.PARSE", "research.intake.ir_builder|RUNE.PIPELINE.IR_BUILD", "research.intake.validator|RUNE.PIPELINE.VALIDATE", "research.intake.receipt"],
    "v2_hygiene": ["v2_hygiene.trigger", "v2_hygiene.loop_awareness", "v2_hygiene.provenance", "v2_hygiene.adversarial", "v2_hygiene.output_register", "v2_hygiene.receipt"],
}
SCAN = {"DEPENDENCY_SCAN": "dependency", "LANE_BOUNDARY_SCAN": "lane_boundary", "EDGE_VALIDATION": "edge_validation", "UNKNOWN_NODE_GATE": "unknown_node"}


def gold(name: str, rune_id: str | None) -> dict:
    if name in FORECAST:
        return {"gold_route_class": "unknown", "gold_scan_class": "none", "gold_integrity": "NOT_COMPUTABLE", "gold_failure": "SPECIALIST_LANE_VIOLATION", "gold_rule": "R004"}
    scan = None
    if rune_id:
        for tok, sc in SCAN.items():
            if tok in rune_id:
                scan = sc
                break
    lane = NAME_TO_LANE.get(name)
    if lane:
        return {"gold_route_class": lane, "gold_scan_class": scan or "none", "gold_integrity": "ALIGNED", "gold_failure": None, "gold_rule": "R009"}
    return {"gold_route_class": "unknown", "gold_scan_class": scan or "unknown_node", "gold_integrity": "NOT_COMPUTABLE", "gold_failure": "UNKNOWN_NODE_GATE", "gold_rule": "R010"}


def rows() -> list[dict]:
    out: list[dict] = []
    for pid in list(NODES) + PARTIAL:
        g = gold(pid, None)
        out.append({"source": "YGGDRASIL_ROUTE_NAMESPACE_MAPPING_001", "grain": "pipeline", "payload_class": "forecast_request" if pid in FORECAST else "route_atom", "name": pid, "namespace": None, "rune_id": None, "claimed_lane": NAME_TO_LANE.get(pid), "node_id": None, "v2_node_lane_is_not_route_class": True, **g})
    for pid, nodes in NODES.items():
        for spec in nodes:
            node_id, _, rune = spec.partition("|")
            rune_id = rune or None
            g = gold(pid, rune_id)
            out.append({"source": f"contracts/yggdrasil/routes/{pid}.route.v1.json", "grain": "node", "payload_class": "forecast_request" if pid in FORECAST else "route_atom", "name": pid, "namespace": None, "rune_id": rune_id, "claimed_lane": NAME_TO_LANE.get(pid), "node_id": node_id, "v2_node_lane_is_not_route_class": True, **g})
    return out


def write(path: Path | None = None) -> Path:
    target = path or Path(__file__).with_name("eval_mapping_v2.jsonl")
    target.write_text("\n".join(json.dumps(r, separators=(",", ":")) for r in rows()) + "\n")
    return target


if __name__ == "__main__":
    print(write())
