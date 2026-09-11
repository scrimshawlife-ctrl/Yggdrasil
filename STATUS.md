# STATUS

**Lane**: SHADOW
**Date**: 2026-09-11
**Version**: 0.1.0

| Gate | State |
|---|---|
| Spec 000 spine | specified |
| Spec 001 route classifier T0 | specified + code |
| Spec 002 spine adapt | specified + `adapt.py` |
| Spec 003 export | specified + `compat.py` |
| Spec 004 shadow dispatch | specified + `dispatch.py` |
| scripts/shadow | specialist-local (Hyperlex pattern) |
| Encoder | name_gate **false** |
| Hub | closed |
| Spec 009 router bind | flipped (R009 / R010) |
| Replaces Abraxas-v2.0 `core/yggdrasil/` | false |
| Legacy Abraxas `scripts/shadow/abx_router` | absent |
| Hero / OG rasters | `assets/hero.{png,jpg}` · `assets/og-social.{png,jpg}` |
| Settings Social preview | manual paste of `og-social.jpg` (no API/MCP) |
| Eval mapping v2 | builder + tests live; committed `eval_mapping_v2.jsonl` is emit stub — run builder/pytest to populate |
| Eval mapping v2 tests | green after classify YGGDRASIL bare-vs-pipeline lane fix |
