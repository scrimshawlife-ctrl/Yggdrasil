# Spec 003 — Export without import

**Status**: SHADOW specified + `compat.py`
**Module**: `src/yggdrasil/compat.py`

`frame_to_route_packet` turns a T0 frame into an Abraxas-routable packet.

- specialist id `yggdrasil.topology`
- packet `yggdrasil.route.v0`
- `forecast_eligible` forced false
- incoming `forecast_eligible: true` becomes `SPECIALIST_LANE_VIOLATION`
- no `import abraxas`
- no rune registry write
