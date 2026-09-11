# Seed fixtures

Eval only. Not training weights.

`eval_mapping_v2.jsonl` is labeled from Abraxas-v2.0 route graphs plus the 20 pipeline IDs in `YGGDRASIL_ROUTE_NAMESPACE_MAPPING_001`.

Rules:

- Gold `route_class` is Spec 012 only: ingest, belief, replay, phase, viz, situation, codegen, runtime_gate, or unknown.
- v2.0 `node.lane` values (`SHADOW`, `GOVERNANCE`, `GOVERNANCE_SHADOW`, `PROJECTION`, `FORECAST_GATED`) are not route_class.
- `pse_forecast` and `memetic_futurecast` are R004 refuse.
- Names absent from `NAME_TO_LANE` are R010 (`neon_genie_ideation`, `outcome_brier`, `research_drop_validation`, and the seven pipelines with no route file).
- `claimed_lane` is only a Spec 012 lane or null.

The mapping artifact on v2.0 still lists `neon_genie_ideation` as missing. The route file is on disk. Re-run:

`python scripts/operator/run_yggdrasil_route_namespace_mapping.py`
