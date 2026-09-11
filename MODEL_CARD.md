# Model card — Yggdrasil T0

| Field | Value |
|---|---|
| Name | Yggdrasil |
| Artifact | `yggdrasil-topology-t0` (rules, not weights) |
| Task | Map route atoms to namespace class + scan class + integrity |
| Input | route atom (`namespace`, `rune_id`, `claimed_lane`, `packet_type`) |
| Output | `yggdrasil.route.v0` |
| Forecast | never |
| Promotion | never |
| Phenomenal | never |
| Training data | none at T0 |
| Eval | `tests/test_yggdrasil_e_r0.py` |
| Intended use | Abraxas RUNTIME_GATE specialist |
| Out of scope | chat, mind claims, replacing `core/yggdrasil/`, slang form parse, tradition gold, settled Brier |
