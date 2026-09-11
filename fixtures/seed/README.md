# Seed fixtures

Eval only. Not training weights.

Gold rows come from `build_eval_mapping_v2.py`. Run that (or pytest) to emit `eval_mapping_v2.jsonl`.

```bash
PYTHONPATH=src python fixtures/seed/build_eval_mapping_v2.py
```

Rules:

- Gold `route_class` is Spec 012 only. v2.0 `node.lane` is never a class.
- Node atoms inherit the parent pipeline's Spec 012 lane. Prefixes `scoring.*`, `forecast.*`, `projection.*` are not classes.
- `NAME_TO_LANE` is imported from `yggdrasil.adapt`. Do not copy it here.
- `pse_forecast` and `memetic_futurecast` are R004.
- `familiar_ingestion` has no route file and is name-mapped to ingest. Gold is R009. Tag `route_file_observed=false`.
- `neon_genie_ideation` has a route file and is not in `NAME_TO_LANE`. Gold is R010. Tag `route_file_observed=true`. Add a name row to change that.
- Bare `RUNE.YGGDRASIL.*` maps to `runtime_gate`. When a pipeline already has a lane, YGGDRASIL tokens set scan only.
- Other no-route pipelines with no name row are R010.
