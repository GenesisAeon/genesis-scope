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

---

## `scope map`

Print the semantic cartography: all nodes (concepts, states, agents,
metrics, models) and the typed, weighted edges between them.

```bash
scope map
```

---

## `scope trace`

Trace an explicit path between two nodes of the semantic map.

```
Usage: scope trace [OPTIONS] START END
```

```bash
scope trace crep agent_coordination
scope trace quasicrystals scope
```

---

## `scope attractors`

Rank semantic nodes by attractor strength (weighted in-degree) — which
concepts pull the most meaning toward them.

```
Usage: scope attractors [OPTIONS]

Options:
  --top-n INTEGER  Number of nodes to show [default: 5]
```

```bash
scope attractors
scope attractors --top-n 10
```

---

## `scope drift-map`

Compare two semantic map snapshots (JSON files produced by
`SemanticMap.to_dict`) and report added/removed nodes and edges, and
edges whose weight changed.

```
Usage: scope drift-map [OPTIONS] PREVIOUS CURRENT
```

```bash
scope drift-map map_v1.json map_v2.json
```
