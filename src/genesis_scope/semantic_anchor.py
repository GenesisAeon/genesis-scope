"""Semantic anchors — the Sigillin as information-theoretic state compressors.

A semantic anchor is a compressed representation of a state that reduces
the entropy of recalling that state for an asynchronous collaborator.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticAnchor:
    """A named semantic anchor (Sigillin) compressing a state to fewer bits.

    Attributes:
        name: Human-readable identifier (e.g. "CREP", "v_RIG", "Q4").
        state_bits: Size of the full, uncompressed state representation in bits.
        anchor_bits: Size of the compressed anchor representation in bits.
        strength: Anchor strength A_i in [0, 1], how reliably the anchor
            triggers correct recall of the full state.
    """

    name: str
    state_bits: float
    anchor_bits: float
    strength: float = 1.0

    def __post_init__(self) -> None:
        if self.state_bits <= 0:
            raise ValueError("state_bits must be positive")
        if self.anchor_bits <= 0:
            raise ValueError("anchor_bits must be positive")
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("strength must be in [0, 1]")

    def compression_ratio(self) -> float:
        """Returns |State| / |Anchor| — how much the anchor compresses the state."""
        return self.state_bits / self.anchor_bits

    def recall_entropy(self) -> float:
        """Returns H(State | Anchor) in bits.

        A perfect anchor (strength = 1) drives recall entropy to zero.
        A useless anchor (strength = 0) leaves the full state entropy.
        """
        return self.state_bits * (1.0 - self.strength)

    def drift_reduction(self, kappa: float, lambda_: float) -> float:
        """Returns the drift fixed point D* = (lambda_ / kappa) * strength.

        This is the contribution of a single anchor to the stable
        deviation D* in the drift model (see drift_model.py).
        """
        if kappa <= 0:
            raise ValueError("kappa must be positive")
        return (lambda_ / kappa) * self.strength

    def information_density(self) -> float:
        """Returns bits of information preserved per anchor bit.

        log2(compression_ratio) scaled by strength — a measure of how
        densely the anchor packs recoverable information.
        """
        return math.log2(self.compression_ratio()) * self.strength
