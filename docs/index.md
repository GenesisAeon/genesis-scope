# genesis-scope

**Semantic coordination system for human-LLM collaboration** — GenesisAeon Package 39.

A human integrates **temporally** — meaning emerges from a continuous,
ordered stream of experience. An LLM navigates **atemporally** — it
collapses a probability space in a single step. `genesis-scope` is the
explicit, executable geometry of the shared space between these two
asynchronous processes.

## Quickstart

```bash
uv sync --dev
uv run pytest
```

```python
from genesis_scope import GenesisScope

scope = GenesisScope()
result = scope.run_cycle(n_sessions=38)

print(result["coherence_score"])   # Gamma_collab
print(result["drift_status"])      # "stable" | "drifting" | "anchored"
```

## Core concepts

| Module | Concept |
|--------|---------|
| `semantic_anchor.py` | Sigillin as information-theoretic state compressors |
| `drift_model.py` | `dD/dt = -kappa * (D - D*)` semantic drift relaxation |
| `coordination_space.py` | `(tau_A, tau_H, Sigma)` coordinate system |
| `crep_collaboration.py` | `Gamma_collab = (C * R * E * P) ** 0.25` |
| `q4_collaboration.py` | 4-bit Q4 state encoding for collaboration phases |
| `session_tracker.py` | Session history, Fisher-Rao velocity, `v_RIG` warning |
| `cartography.py` | Semantic map: nodes, typed edges, paths, attractors, drift, pheromone trails |
| `system.py` | `GenesisScope` — Diamond interface |

## Commands

| Command | Description |
|---------|-------------|
| `scope status` | Run a collaboration cycle and print the status |
| `scope drift` | Simulate semantic drift with/without anchors |
| `scope benchmark` | Evaluate against `SCOPE_TARGETS` |
| `scope anchor` | List registered semantic anchors (Sigillin) |
| `scope map` | Print the semantic cartography (nodes + edges) |
| `scope trace <start> <end>` | Trace an explicit path through the map |
| `scope attractors` | Rank concepts by attractor strength |
| `scope drift-map <old> <new>` | Diff two semantic map snapshots |
| `scope walk <map.json> <actor> <nodes...>` | Lay a pheromone trail along a path |
| `scope evaporate <map.json>` | Decay all edge weights (pheromone evaporation) |
| `scope trail <map.json>` | Show the recorded pheromone trail and footprints |
