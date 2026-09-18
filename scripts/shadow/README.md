# scripts/shadow

SHADOW / advisory only. No Abraxas import. No train. No Hub.

`yggdrasil` is Spec 012. Router rules R009 / R010 / R004 / R011 live in `src/yggdrasil/dispatch.py`.

```
PYTHONPATH=src python3 -m yggdrasil dispatch '{"namespace":"yggdrasil.ingest"}'
```

Spec 009 named path `scripts/shadow/abx_router/` is not in scrimshawlife-ctrl/Abraxas or Abraxas-v2.0.
This folder is the specialist-local copy of that named path.
