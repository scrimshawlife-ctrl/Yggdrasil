# Yggdrasil

<p align="center">
  <img src="assets/hero.png" alt="Yggdrasil hero — bronze world-tree topology graph" width="100%" />
</p>

SHADOW topology specialist for the Abraxas model stack. Route atoms in. `yggdrasil.route.v0` out.

Named for the world tree: namespaces, edges, and gates. This repo classifies topology. It does not become the runtime spine in Abraxas-v2.0.

| | |
|---|---|
| **Owns** | route_class · scan_class · integrity · unknown-node gate |
| **Honesty** | `OBSERVED` / `INFERRED` / `SPECULATIVE` / `NOT_COMPUTABLE` |
| **Shape** | T0 rules now. Encoder name-gated. Not a chatbot. |
| **Anti** | promotion · forecast mint · chat trunk · Hyperlex form · Athanor family · Semion triad · settled Brier |
| **Lane** | SHADOW — classify live · train/Hub gated |
| **Router** | Spec 009 R009 / R010. Forecast stays R004 `NOT_COMPUTABLE`. |

Live spine code stays in `scrimshawlife-ctrl/Abraxas-v2.0` `core/yggdrasil/`. This specialist does not hard-import that tree.
Bind record on v2.0 main: `specs/012-yggdrasil-topology/BIND.md` (PR #1139).

## Social preview

Raster card for GitHub Settings → Social preview: [`assets/og-social.jpg`](assets/og-social.jpg) (1280×640). Also [`assets/og-social.png`](assets/og-social.png).
Custom Settings social preview is **not** writable via API/MCP. Paste after merge if desired (private repos may block first custom OG).

## Quick links

| Doc | Path |
|-----|------|
| Status | [`STATUS.md`](STATUS.md) |
| Bind receipt | [`BIND_RECEIPT.md`](BIND_RECEIPT.md) |
| Constitution | [`constitution.md`](constitution.md) |
| Spec 000 spine | [`specs/000-yggdrasil-spine/spec.md`](specs/000-yggdrasil-spine/spec.md) |
| Spec 001 classifier | [`specs/001-route-classifier/spec.md`](specs/001-route-classifier/spec.md) |
| Spec 002 adapt | [`specs/002-spine-adapt/spec.md`](specs/002-spine-adapt/spec.md) |
| Spec 004 dispatch | [`specs/004-shadow-dispatch/spec.md`](specs/004-shadow-dispatch/spec.md) |
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
```
