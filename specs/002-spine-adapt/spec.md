# Spec 002 — Spine adapt

**Status**: SHADOW specified + `adapt.py`
**Module**: `src/yggdrasil/adapt.py`

Maps copied spine records onto route atoms. No Abraxas import. No file scrape of the v2.0 tree.

Known name → lane:
- universal_ingest, familiar_ingestion, research_intake, oracle_signal → ingest
- aal_viz_projection → viz
- operator_review_queue, drift_scan, v2_hygiene, canon_sync → runtime_gate
- alembic_spine → codegen

Refuse: pse_forecast, memetic_futurecast, forecast payloads.
Unknown names become `yggdrasil.<name>` so T0 hits UNKNOWN_NODE_GATE.
