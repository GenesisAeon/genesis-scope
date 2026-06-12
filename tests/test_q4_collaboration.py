"""Tests for genesis_scope.q4_collaboration."""

from __future__ import annotations

import pytest

from genesis_scope.crep_collaboration import CollaborationCREP
from genesis_scope.q4_collaboration import (
    crep_to_q4,
    gray_sequence,
    hamming_distance,
    is_gray_transition,
    q4_to_label,
)


def test_crep_to_q4_all_high():
    crep = CollaborationCREP(c=0.9, r=0.9, e=0.9, p=0.9)
    assert crep_to_q4(crep) == 0b1111


def test_crep_to_q4_all_low():
    crep = CollaborationCREP(c=0.1, r=0.1, e=0.1, p=0.1)
    assert crep_to_q4(crep) == 0b0000


def test_crep_to_q4_mixed():
    crep = CollaborationCREP(c=0.9, r=0.1, e=0.9, p=0.1)
    assert crep_to_q4(crep) == 0b1010


def test_q4_to_label():
    assert q4_to_label(0) == "0000"
    assert q4_to_label(15) == "1111"
    assert q4_to_label(10) == "1010"


def test_q4_to_label_invalid():
    with pytest.raises(ValueError):
        q4_to_label(16)


def test_hamming_distance():
    assert hamming_distance(0b0000, 0b0001) == 1
    assert hamming_distance(0b0000, 0b1111) == 4


def test_is_gray_transition():
    assert is_gray_transition(0b0000, 0b0001)
    assert not is_gray_transition(0b0000, 0b0011)


def test_gray_sequence():
    seq = gray_sequence()
    assert len(seq) == 16
    assert sorted(seq) == list(range(16))
    for a, b in zip(seq, seq[1:], strict=False):
        assert is_gray_transition(a, b)
