# CLI Reference

## `scope status`

Run a collaboration cycle and print the resulting scope status as JSON.

```
Usage: scope status [OPTIONS]

Options:
  --n-sessions INTEGER  Number of sessions to simulate [default: 38]
```

```bash
scope status
scope status --n-sessions 10
```

---

## `scope drift`

Simulate the semantic drift model with and without anchors.

```
Usage: scope drift [OPTIONS]

Options:
  --n-steps INTEGER  Number of time steps to simulate [default: 10]
  --kappa FLOAT      Drift rate [default: 0.3]
  --lambda- FLOAT    Anchor damping [default: 0.8]
```

```bash
scope drift --n-steps 20
```

---

## `scope benchmark`

Evaluate the current model against `SCOPE_TARGETS`.

```bash
scope benchmark
```

---

## `scope anchor`

List the registered semantic anchors (Sigillin) with their compression
ratio and strength.

```bash
scope anchor
```
