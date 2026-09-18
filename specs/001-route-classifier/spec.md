# Spec 001 — Route classifier T0

**Status**: SHADOW specified + code
**Artifact**: `yggdrasil-topology-t0`
**Packet**: `yggdrasil.route.v0`

R1 Forecast payload or forecast_eligible true → NOT_COMPUTABLE / SPECIALIST_LANE_VIOLATION.
R2 Promotion payload or can_promote true → REJECT_OR_SHADOW.
R3 Namespace yggdrasil.<lane> maps when lane is frozen.
R4 RUNE family tokens map lane. `RUNE.YGGDRASIL.*` tokens set scan_class only. A bare YGGDRASIL atom (no namespace, no claimed lane) maps to `runtime_gate`.
R5 claimed_lane mismatch → lane_boundary / SHIFTING.
R6 Unknown namespace → unknown_node / NOT_COMPUTABLE.
R7 Empty atom → NOT_COMPUTABLE.
