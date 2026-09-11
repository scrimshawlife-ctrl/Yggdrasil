# Architecture

```
route_atom
    -> T0 classify (this repo)
    -> yggdrasil.route.v0
    -> Spec 009 router bind (operator sentence)
    -> Abraxas-v2.0 core/yggdrasil runtime (not this package)
```

T0 owns classification only. Runtime graph models stay in Abraxas-v2.0. Export is schema-shaped JSON. No hard import.
