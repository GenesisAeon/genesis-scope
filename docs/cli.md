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

---

## `scope walk`

Lay a pheromone trail along a path through a saved semantic map: every
edge connecting consecutive nodes gets its weight increased by `gain`
(clamped to 1.0), and the traversal is recorded in the map's trail.
The updated map is written back to `map_file`.

```
Usage: scope walk [OPTIONS] MAP_FILE ACTOR NODES...

Options:
  --gain FLOAT  Reinforcement applied to each edge on the path [default: 0.05]
```

```bash
scope walk map.json human crep governance diamond
scope walk map.json claude crep scope --gain 0.1
```

---

## `scope evaporate`

Evaporate pheromones: decay every edge weight in a saved semantic map
by `rate`, never dropping below `floor`, and write the map back.
Routes that aren't reinforced by `scope walk` fade toward `floor` over
repeated calls.

```
Usage: scope evaporate [OPTIONS] MAP_FILE

Options:
  --rate FLOAT   Multiplicative decay applied to every edge [default: 0.95]
  --floor FLOAT  Minimum edge weight after decay [default: 0.01]
```

```bash
scope evaporate map.json
scope evaporate map.json --rate 0.9 --floor 0.05
```

---

## `scope trail`

Print the pheromone trail recorded in a saved semantic map: every
traversal (who walked which path) and a per-actor footprint count.

```
Usage: scope trail [OPTIONS] MAP_FILE
```

```bash
scope trail map.json
```
