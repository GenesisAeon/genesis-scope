"""Benchmark targets for genesis-scope (Package 39).

These targets are hypotheses to be validated against real session history,
following the falsifiable-prediction style used across the GenesisAeon
package series (P17-P38).
"""

from __future__ import annotations

from typing import Any

from genesis_scope.constants import DEFAULT_KAPPA, DEFAULT_LAMBDA
from genesis_scope.system import GenesisScope

# (target_value, tolerance) — tolerance of None means an exact boolean check.
SCOPE_TARGETS: dict[str, tuple[float | bool | int, float | None]] = {
    "gamma_collab_min": (0.35, 0.10),
    "gamma_collab_max": (0.55, 0.10),
    "drift_fixpoint_ratio": (0.37, 0.10),
    "anchor_compression": (10.0, 5.0),
    "session_coherence_p38": (True, None),
    "v_rig_warning_triggered": (False, None),
}


def evaluate(scope: GenesisScope | None = None, n_sessions: int = 38) -> dict[str, dict[str, Any]]:
    """Runs a GenesisScope cycle and checks the result against SCOPE_TARGETS.

    Returns a dict mapping each target name to
    {"value": measured, "target": target, "tolerance": tol, "passed": bool}.
    """
    scope = scope or GenesisScope()
    scope.run_cycle(n_sessions=n_sessions)

    gamma = scope.coherence_score()
    drift_ratio = scope.lambda_ / scope.kappa
    anchor_compressions = [a.compression_ratio() for a in scope.anchors]
    mean_compression = sum(anchor_compressions) / len(anchor_compressions)

    measured = {
        "gamma_collab_min": gamma,
        "gamma_collab_max": gamma,
        "drift_fixpoint_ratio": drift_ratio,
        "anchor_compression": mean_compression,
        "session_coherence_p38": gamma > 0.0,
        "v_rig_warning_triggered": scope.v_rig_warning(),
    }

    results: dict[str, dict[str, Any]] = {}
    for name, (target, tol) in SCOPE_TARGETS.items():
        value = measured[name]
        if tol is None:
            passed = bool(value) == bool(target)
        elif name == "gamma_collab_min":
            passed = value >= target - tol
        elif name == "gamma_collab_max":
            passed = value <= target + tol
        else:
            passed = abs(value - target) <= tol
        results[name] = {"value": value, "target": target, "tolerance": tol, "passed": passed}

    return results


def default_kappa_lambda() -> tuple[float, float]:
    """Returns the default (kappa, lambda_) drift parameters."""
    return DEFAULT_KAPPA, DEFAULT_LAMBDA
