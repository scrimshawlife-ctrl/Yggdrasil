# Yggdrasil

<p align="center">
  <img src="assets/hero.png" alt="Yggdrasil hero — bronze world-tree topology graph" width="100%" />
</p>

**SHADOW topology specialist** for the Abraxas model stack. Route atoms in. `yggdrasil.route.v0` out.

Named for the world tree: namespaces, edges, and gates. This repo **classifies topology**. It does **not** replace the runtime spine in Abraxas-v2.0.

| | |
|---|---|
| **Owns** | route_class · scan_class · integrity · unknown-node gate |
| **Honesty** | `OBSERVED` / `INFERRED` / `SPECULATIVE` / `NOT_COMPUTABLE` |
| **Shape** | Spec 001–004 **T0 rules live**. Encoder `name_gate` **false**. Not a chatbot. |
| **Anti** | promotion · forecast mint · chat trunk · Hyperlex form · Athanor family · Semion triad · settled Brier |
| **Lane** | SHADOW — classify live · **no train weights at T0** · Hub closed |
| **Router** | Spec 009 R009 / R010. Forecast stays R004 `NOT_COMPUTABLE`. |
| **Version** | `0.1.0` (see [`STATUS.md`](STATUS.md)) |

## What ships / what does not

| Ships now | Does **not** ship |
|-----------|-------------------|
| T0 `classify` / `adapt` / `compat` / `dispatch` | Learned router / train weights |
| Eval mapping v2 **builder + tests** (106 rows when built) | Populated `eval_mapping_v2.jsonl` committed as gold (emit stub only) |
| Spec 009 bind flipped (R009/R010) | Replacement of Abraxas-v2.0 `core/yggdrasil/` |
| Hero + OG rasters | Auto Settings social-preview write |

**Train?** Not for the current job. Yggdrasil is a deterministic route classifier. Eval gold checks classify honesty; it is not a training corpus. A learned router would be a later product decision.

## Current state (OBSERVED 2026-09-11 PT)

| Area | State |
|------|-------|
| Spec 000–004 | Specified + code |
| Encoder | `name_gate` **false** |
| Hub | closed |
| Spec 009 router bind | flipped (R009 / R010) |
| Replaces Abraxas-v2.0 `core/yggdrasil/` | **false** |
| Eval mapping v2 | builder + tests; committed file is emit stub |
| Eval tests | **28 passed** after YGGDRASIL bare-vs-pipeline lane fix |
| When built | **106** rows (20 pipeline / 86 node) · R009/R010/R004 |

Live spine code stays in `scrimshawlife-ctrl/Abraxas-v2.0` `core/yggdrasil/`. This specialist does not hard-import that tree.
Bind record on v2.0 main: `specs/012-yggdrasil-topology/BIND.md` (PR #1139). Local receipt: [`BIND_RECEIPT.md`](BIND_RECEIPT.md).

## Social preview

Raster card: [`assets/og-social.jpg`](assets/og-social.jpg) (1280×640) · also [`assets/og-social.png`](assets/og-social.png).
Settings → Social preview is **manual** (no API/MCP).

## Pipeline

```
spine / route packet → adapt() → atom → classify() → yggdrasil.route.v0
                                              ↓
                                         dispatch()
```

Bare `RUNE.YGGDRASIL.*` (no namespace, no claimed lane) → `runtime_gate` + ALIGNED.
When a pipeline already has a Spec 012 lane, YGGDRASIL tokens set **scan only** (no fake `runtime_gate` conflict).
See [`fixtures/seed/README.md`](fixtures/seed/README.md).

## Specs

| Spec | Role | Path |
|------|------|------|
| 000 spine | Constitution | [`specs/000-yggdrasil-spine/`](specs/000-yggdrasil-spine/) |
| 001 classifier | T0 route classify | [`specs/001-route-classifier/`](specs/001-route-classifier/) |
| 002 adapt | Spine → atoms | [`specs/002-spine-adapt/`](specs/002-spine-adapt/) |
| 003 export | Compat export | [`specs/003-export/`](specs/003-export/) |
| 004 dispatch | Shadow dispatch | [`specs/004-shadow-dispatch/`](specs/004-shadow-dispatch/) |

## Quick links

| Doc | Path |
|-----|------|
| Status | [`STATUS.md`](STATUS.md) |
| Bind receipt | [`BIND_RECEIPT.md`](BIND_RECEIPT.md) |
| Constitution | [`constitution.md`](constitution.md) |
| Model card | [`MODEL_CARD.md`](MODEL_CARD.md) |
| Seed / eval | [`fixtures/seed/README.md`](fixtures/seed/README.md) |
| Contributing | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Security | [`SECURITY.md`](SECURITY.md) |

## Install and run

```bash
pip install -e ".[dev]"
python -m yggdrasil --version
python -m yggdrasil classify '{"namespace":"yggdrasil.ingest"}'
python -m yggdrasil adapt '{"name":"universal_ingest"}'
python -m yggdrasil dispatch '{"namespace":"yggdrasil.ingest"}'
pytest -q
# emit eval mapping locally (not committed):
PYTHONPATH=src python fixtures/seed/build_eval_mapping_v2.py
```

## Eval corpus

| Layer | Where | In git? |
|-------|-------|---------|
| Builder | `fixtures/seed/build_eval_mapping_v2.py` | Yes |
| Emit stub | `fixtures/seed/eval_mapping_v2.jsonl` | Yes (comments only) |
| Seed atoms | `fixtures/seed/atoms.jsonl` | Yes (tiny smoke) |
| Built mapping | same path after builder/pytest | Local rewrite only |

Gold `route_class` is Spec 012 only. v2.0 `node.lane` is never a class. `NAME_TO_LANE` comes from `yggdrasil.adapt`.

## Fail-closed gates

Do **not** without Danny/operator yes:

- Treat this repo as a drop-in replacement for Abraxas-v2.0 `core/yggdrasil/`
- Flip `name_gate` or open Hub for a learned router
- Commit large populated eval dumps as if they were training weights
- Forecast mint, promotion, or phenomenal claims

## Peers

Hyperlex (form / lexical) · Athanor (tradition structure) · Semion (sign relation) · **Yggdrasil (route topology)** · Abraxas-v2.0 (runtime spine)

## License

Code: MIT unless otherwise noted. See repo license files.
