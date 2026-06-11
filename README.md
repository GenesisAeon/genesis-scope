# genesis-scope

**Semantic coordination system for human-LLM collaboration** — GenesisAeon Package 39.

[![CI](https://github.com/GenesisAeon/genesis-scope/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/genesis-scope/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

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

All of these are tied together by `GenesisScope`, the Diamond-interface
implementation in `system.py`.

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

---

*GenesisAeon Package 39 · Johann Römer · MOR Research Collective · Mai 2026*
*Reference: [10.5281/zenodo.17472834](https://doi.org/10.5281/zenodo.17472834)*
