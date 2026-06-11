"""CREP tensor reinterpreted for human-LLM collaboration sessions.

C = Context continuity   (0 = fully new context, 1 = full context retained)
R = Reproducibility      (0 = not reproducible, 1 = exact)
E = Entropy              (0 = fully determined, 1 = maximally open)
P = Productivity         (normalised meaning-units produced per session)

Gamma_collab = (C * R * E * P) ** (1/4)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CollaborationCREP:
    """A single CREP(C, R, E, P) measurement for a collaboration session."""

    c: float
    r: float
    e: float
    p: float

    def __post_init__(self) -> None:
        for name, value in (("c", self.c), ("r", self.r), ("e", self.e), ("p", self.p)):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1], got {value}")

    def gamma(self) -> float:
        """Returns Gamma_collab = (C * R * E * P) ** (1/4)."""
        return float((self.c * self.r * self.e * self.p) ** 0.25)

    def is_critical(self, low: float = 0.2, high: float = 0.5) -> bool:
        """Returns True if Gamma_collab lies in the critical regime [low, high]."""
        return low <= self.gamma() <= high

    def as_dict(self) -> dict[str, float]:
        return {"C": self.c, "R": self.r, "E": self.e, "P": self.p, "gamma": self.gamma()}
