# genesis-scope

**Semantic coordination system for human-LLM collaboration** — GenesisAeon Package 39.

[![CI](https://github.com/GenesisAeon/genesis-scope/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/genesis-scope/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17472834-blue)](https://doi.org/10.5281/zenodo.17472834)

---

## Mission

A human integrates **temporally** — meaning emerges from a continuous,
ordered stream of experience. An LLM navigates **atemporally** — it
collapses a probability space in a single step, with no continuous
experience stream of its own.

`genesis-scope` is the explicit, executable geometry of the shared space
between these two asynchronous processes. It models:

- **Semantic anchors** (Sigillin) — compressed state markers that reduce
  meaning drift between sessions (`semantic_anchor.py`).
- **Drift model** — `dD/dt = -kappa * (D - D*)`, the relaxation of shared
  semantic state toward a fixed point `D* = (lambda/kappa) * A_avg`
  set by the registered anchors (`drift_model.py`).
- **Coordination space** — the `(tau_A, tau_H, Sigma)` coordinate system:
  action time, human time, and semantic density (`coordination_space.py`).
- **Collaboration CREP** — `Gamma_collab = (C * R * E * P) ** 0.25`, the
  coherence metric for a collaboration session (`crep_collaboration.py`).
- **Q4 collaboration states** — 4-bit encoding of collaboration phases,
  following the GenesisAeon Q4 Runtime Contract (`q4_collaboration.py`).
- **Session tracking** — records sessions, computes Fisher-Rao velocity
  through coordination space, and warns if it exceeds `v_RIG`
  (Package 31, `session_tracker.py`).
- **Semantic cartography** — the navigable map of the GenesisAeon concept
  space: typed nodes and edges, explicit paths between concepts, attractor
  ranking, drift detection between map snapshots, and multi-agent
  perspective comparison (`cartography.py`).

All of these are tied together by `GenesisScope`, the Diamond-interface
implementation in `system.py`.

## Installation

```bash
pip install genesis-scope
```

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
print(result["utac_state"])        # Sigma(t) + Q4 state
```

## CLI

```bash
scope status                  # run a cycle and print the scope status
scope drift                   # simulate drift with/without anchors
scope benchmark                # evaluate against SCOPE_TARGETS
scope anchor                  # list registered semantic anchors (Sigillin)
scope map                     # print the semantic cartography (nodes + edges)
scope trace <start> <end>     # trace an explicit path through the map
scope attractors               # rank concepts by attractor strength
scope drift-map <old> <new>   # diff two semantic map snapshots
```

## Semantic cartography

`genesis-scope` is the translation layer that projects domain knowledge
(physics, governance, runtime, agents, entropy, mathematics) onto a
navigable topography: explicit **nodes** (concepts, states, agents,
metrics, models), typed **edges** (`influences`, `generates`,
`stabilizes`, `contradicts`, `extends`, `abstracts`), and traceable
**paths** between them.

```python
from genesis_scope import DEFAULT_MAP, compare_maps, compare_perspectives

# An explicit path through the concept space
DEFAULT_MAP.trace("crep", "agent_coordination")
# ["crep", "governance", "diamond", "claim_system", "agent_coordination"]

# Which concepts attract the most meaning?
DEFAULT_MAP.attractors(top_n=3)
# [("genesis_os", 1.65), ("scope", 1.5), ("unified_mandala", 1.4)]

# Drift between two snapshots of the map over time
report = compare_maps(previous_map, current_map)
report.added_nodes, report.reweighted_edges

# Where do different agents' maps of the same space agree or diverge?
compare_perspectives({"claude": claude_map, "gemini": gemini_map})
```

## Development

```bash
uv sync --dev
pre-commit install
uv run ruff check .
uv run mypy src
uv run pytest
```

## Falsifiable prediction

`Gamma_collab` for GenesisAeon sessions is hypothesised to lie in the
critical regime `[0.2, 0.5]` (see `benchmark.py` / `SCOPE_TARGETS`). If
real session data instead lands outside `[0.1, 0.8]`, the model needs
revision.

## Role in the GenesisAeon Ecosystem

`genesis-scope` is Package **P39** of the GenesisAeon ecosystem, in the
**meta-collaboration / semantic cartography** domain. It is the human-AI
navigation layer: the explicit, executable geometry that tracks
collaboration coherence (`Gamma_collab`), semantic drift, and the
navigable concept map shared across the other GenesisAeon packages.

## Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PLACEHOLDER.svg)](https://doi.org/10.5281/zenodo.PLACEHOLDER)

DOI will be assigned automatically on first GitHub Release once
Zenodo–GitHub integration is enabled for this repo. Until then, cite the
existing concept DOI:
[10.5281/zenodo.17472834](https://doi.org/10.5281/zenodo.17472834).

---

*GenesisAeon Package 39 · Johann Römer · MOR Research Collective · Mai 2026*
*Reference: [10.5281/zenodo.17472834](https://doi.org/10.5281/zenodo.17472834)*
