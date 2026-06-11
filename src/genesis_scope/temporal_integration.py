"""Human-time integration of semantic density Sigma(t).

Mirrors the UTAC logistic ODE dH/dt = r*H*(1-H/K)*tanh(sigma*Gamma), with
H reinterpreted as Sigma — the semantic density of the shared context that
accumulates as the human collaborator integrates experience over tau_H.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from genesis_scope.constants import SIGMA_PHI


@dataclass
class TemporalIntegrator:
    """Integrates semantic density Sigma(t) using the UTAC logistic form.

    dSigma/dt = r * Sigma * (1 - Sigma/K) * tanh(sigma * gamma)

    Attributes:
        r: Growth rate of semantic density.
        k: Carrying capacity (maximum semantic density).
        gamma: CREP coherence value driving the tanh coupling.
        sigma: Coupling constant (defaults to the Frame Principle sigma_Phi).
    """

    r: float
    k: float
    gamma: float
    sigma: float = SIGMA_PHI

    def __post_init__(self) -> None:
        if self.r <= 0:
            raise ValueError("r must be positive")
        if self.k <= 0:
            raise ValueError("k must be positive")

    def rate(self, sigma_value: float) -> float:
        """Returns dSigma/dt at the given semantic density."""
        return self.r * sigma_value * (1 - sigma_value / self.k) * math.tanh(
            self.sigma * self.gamma
        )

    def integrate(self, sigma0: float, t_span: tuple[float, float], n_steps: int = 100) -> list[
        tuple[float, float]
    ]:
        """Integrates Sigma(t) over t_span using forward Euler.

        Returns a list of (t, Sigma(t)) samples.
        """
        t_start, t_end = t_span
        if n_steps < 2:
            raise ValueError("n_steps must be >= 2")
        dt = (t_end - t_start) / (n_steps - 1)
        result = [(t_start, sigma0)]
        sigma_value = sigma0
        for i in range(1, n_steps):
            sigma_value = sigma_value + self.rate(sigma_value) * dt
            result.append((t_start + i * dt, sigma_value))
        return result
