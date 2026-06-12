"""Q4 4-bit state encoding for collaboration phases.

Each CREP(C, R, E, P) measurement is mapped onto a 4-bit Q4 state by
thresholding each dimension, following the Q4 Runtime Contract
(contracts/runtime.schema.yaml). Bit order is C-R-E-P, MSB first.
"""

from __future__ import annotations

from genesis_scope.constants import CREP_THRESHOLDS, GRAY_ORDER, Q4_STATES
from genesis_scope.crep_collaboration import CollaborationCREP


def crep_to_q4(
    crep: CollaborationCREP, thresholds: dict[str, float] | None = None
) -> int:
    """Maps a CollaborationCREP measurement to a Q4 state in [0, 15].

    Each dimension contributes one bit: 1 if the value is >= its threshold,
    else 0. Bits are ordered C (MSB) R E P (LSB).
    """
    th = thresholds or CREP_THRESHOLDS
    bits = (
        (crep.c >= th["C"]) << 3
        | (crep.r >= th["R"]) << 2
        | (crep.e >= th["E"]) << 1
        | (crep.p >= th["P"])
    )
    return int(bits)


def q4_to_label(state: int) -> str:
    """Returns a 4-character binary label (e.g. "1010") for a Q4 state."""
    if not 0 <= state < Q4_STATES:
        raise ValueError(f"state must be in [0, {Q4_STATES - 1}]")
    return format(state, "04b")


def hamming_distance(a: int, b: int) -> int:
    """Returns the Hamming distance between two Q4 states."""
    return bin(a ^ b).count("1")


def is_gray_transition(a: int, b: int) -> bool:
    """Returns True if the transition a -> b has Hamming distance 1.

    The Gray-code policy (contracts/runtime.schema.yaml) requires all
    state transitions to differ in exactly one bit.
    """
    return hamming_distance(a, b) == 1


def gray_sequence() -> list[int]:
    """Returns the canonical Gray-code ordering of all 16 Q4 states."""
    return list(GRAY_ORDER)
