# Bind receipt — Spec 009

**Date**: 2026-09-11
**Operator sentence**: Bind yggdrasil.topology on Spec 009. Packet yggdrasil.route.v0. Home RUNTIME_GATE. Rules R009 route_atom and R010 unknown_namespace. Forecast stays R004 NOT_COMPUTABLE. Do not train. Do not Hub.

| field | value |
|---|---|
| specialist | yggdrasil.topology |
| packet | yggdrasil.route.v0 |
| home | RUNTIME_GATE / yggdrasil.runtime_gate |
| R009 | route_atom → yggdrasil.topology |
| R010 | unknown_namespace → NOT_COMPUTABLE / UNKNOWN_NODE_GATE |
| R004 | forecast_request → NOT_COMPUTABLE |
| train | false |
| Hub | closed |
| v2.0 main | PR #1139 squash `541b5c1` + index `242eda3` |
| replaces core/yggdrasil | false |
