# Yggdrasil

SHADOW topology specialist for the Abraxas model stack. Route atoms in. `yggdrasil.route.v0` out.

Named for the world tree: namespaces, edges, and gates. This repo classifies topology. It does not become the runtime spine in Abraxas-v2.0.

| | |
|---|---|
| **Owns** | route_class · scan_class · integrity · unknown-node gate |
| **Honesty** | `OBSERVED` / `INFERRED` / `SPECULATIVE` / `NOT_COMPUTABLE` |
| **Shape** | T0 rules now. Encoder name-gated. Not a chatbot. |
| **Anti** | promotion · forecast mint · chat trunk · Hyperlex form · Athanor family · Semion triad · settled Brier |
| **Lane** | SHADOW — classify live · train/Hub gated |

Live spine code stays in `scrimshawlife-ctrl/Abraxas-v2.0` `core/yggdrasil/`. This specialist does not hard-import that tree.

## Quick links

| Doc | Path |
|-----|------|
| Status | [`STATUS.md`](STATUS.md) |
| Constitution | [`.specify/memory/constitution.md`](.specify/memory/constitution.md) |
| Spec 000 spine | [`specs/000-yggdrasil-spine/spec.md`](specs/000-yggdrasil-spine/spec.md) |
| Spec 001 classifier | [`specs/001-route-classifier/spec.md`](specs/001-route-classifier/spec.md) |
| Model card | [`MODEL_CARD.md`](MODEL_CARD.md) |

## Install and classify

```bash
pip install -e ".[dev]"
python -m yggdrasil --version
python -m yggdrasil classify '{"namespace":"yggdrasil.ingest","rune_id":"RUNE.INGEST.HANDOFF_BUILD"}'
pytest -q
```
