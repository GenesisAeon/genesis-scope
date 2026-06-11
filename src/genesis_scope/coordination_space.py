"""The (tau_A, tau_H, Sigma) coordination space for human-LLM collaboration.

tau_A: action time   — discrete, atemporal LLM operation steps.
tau_H: human time    — continuous, integrating wall-clock time.
Sigma: semantic density — information content of the shared context.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class CoordinationPoint:
    """A single point P_i = (tau_A, tau_H, Sigma) in the coordination space."""

    tau_a: float
    tau_h: float
    sigma: float

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.tau_a, self.tau_h, self.sigma)


def fisher_rao_velocity(p1: CoordinationPoint, p2: CoordinationPoint) -> float:
    """Returns the Fisher-Rao-style velocity between two coordination points.

    Approximated as the Euclidean distance between the two points in
    (tau_A, tau_H, Sigma) space, normalised by the tau_H interval —
    a discrete analogue of the Fisher information metric speed
    v = sqrt(g_ij * dtheta^i * dtheta^j) / dt.
    """
    d_tau_h = p2.tau_h - p1.tau_h
    if d_tau_h == 0:
        raise ValueError("p1 and p2 must differ in tau_h")
    d_tau_a = p2.tau_a - p1.tau_a
    d_sigma = p2.sigma - p1.sigma
    distance = math.sqrt(d_tau_a**2 + d_tau_h**2 + d_sigma**2)
    return distance / abs(d_tau_h)


@dataclass
class CoordinationSpace:
    """A trajectory of coordination points P_1, ..., P_n."""

    points: list[CoordinationPoint]

    def velocities(self) -> list[float]:
        """Returns Fisher-Rao velocities between consecutive points."""
        return [
            fisher_rao_velocity(self.points[i], self.points[i + 1])
            for i in range(len(self.points) - 1)
        ]

    def mean_velocity(self) -> float:
        """Returns the mean Fisher-Rao velocity across the trajectory."""
        velocities = self.velocities()
        if not velocities:
            return 0.0
        return sum(velocities) / len(velocities)

    def add(self, point: CoordinationPoint) -> None:
        self.points.append(point)
