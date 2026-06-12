"""Semantic drift model: dD/dt = kappa * D - lambda * sum(A_i).

Models how meaning diverges between an asynchronous human/LLM collaboration
over time, and how semantic anchors (Sigillin) damp that divergence.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from genesis_scope.constants import DEFAULT_KAPPA, DEFAULT_LAMBDA
from genesis_scope.semantic_anchor import SemanticAnchor


@dataclass
class DriftModel:
    """ODE model of semantic drift, optionally damped by anchors.

    dD/dt = -kappa * (D(t) - D*),  where D* = (lambda / kappa) * A_avg

    Without anchors (A_avg == 0): D* = 0 and D(t) = D0 * exp(-kappa * t)
    decays to zero — no anchors means no persistent shared state, but
    also no runaway divergence.

    With anchors: D(t) relaxes toward the fixed point
    D* = (lambda / kappa) * A_avg, the stable amount of shared semantic
    state maintained by the anchors.
    """

    kappa: float = DEFAULT_KAPPA
    lambda_: float = DEFAULT_LAMBDA
    anchors: list[SemanticAnchor] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.kappa <= 0:
            raise ValueError("kappa must be positive")
        if self.lambda_ < 0:
            raise ValueError("lambda_ must be non-negative")

    def anchor_average(self) -> float:
        """Returns A_avg, the mean strength of all registered anchors."""
        if not self.anchors:
            return 0.0
        return sum(a.strength for a in self.anchors) / len(self.anchors)

    def fixed_point(self) -> float:
        """Returns D* = (lambda_ / kappa) * A_avg, the stable drift level."""
        return (self.lambda_ / self.kappa) * self.anchor_average()

    def drift_at(self, t: float, d0: float = 1.0) -> float:
        """Returns D(t), the closed-form solution of the drift ODE.

        D(t) = D* + (D0 - D*) * exp(-kappa * t)

        This solves dD/dt = -kappa * (D - D*), the linear relaxation form
        equivalent to dD/dt = kappa*D - lambda*sum(A_i) with
        D* = (lambda_/kappa) * A_avg.
        """
        d_star = self.fixed_point()
        return d_star + (d0 - d_star) * math.exp(-self.kappa * t)

    def trajectory(self, t_span: tuple[float, float], n_steps: int = 100, d0: float = 1.0) -> list[
        tuple[float, float]
    ]:
        """Returns [(t, D(t)), ...] sampled over t_span."""
        t_start, t_end = t_span
        if n_steps < 2:
            raise ValueError("n_steps must be >= 2")
        step = (t_end - t_start) / (n_steps - 1)
        return [
            (t_start + i * step, self.drift_at(t_start + i * step, d0=d0)) for i in range(n_steps)
        ]

    def status(self, d: float, threshold: float = 0.1) -> str:
        """Classifies a drift value D relative to the fixed point D*.

        Returns:
            "anchored" if D is at/below the anchored fixed point and anchors exist.
            "stable" if |D - D*| <= threshold.
            "drifting" otherwise.
        """
        d_star = self.fixed_point()
        if self.anchors and d <= d_star + threshold:
            return "anchored"
        if abs(d - d_star) <= threshold:
            return "stable"
        return "drifting"
