"""Tests for genesis_scope.semantic_anchor."""

from __future__ import annotations

import math

import pytest

from genesis_scope.semantic_anchor import SemanticAnchor


def test_compression_ratio():
    anchor = SemanticAnchor(name="CREP", state_bits=64.0, anchor_bits=4.0, strength=1.0)
    assert anchor.compression_ratio() == 16.0


def test_recall_entropy_perfect_anchor():
    anchor = SemanticAnchor(name="CREP", state_bits=64.0, anchor_bits=4.0, strength=1.0)
    assert anchor.recall_entropy() == 0.0


def test_recall_entropy_useless_anchor():
    anchor = SemanticAnchor(name="CREP", state_bits=64.0, anchor_bits=4.0, strength=0.0)
    assert anchor.recall_entropy() == 64.0


def test_drift_reduction():
    anchor = SemanticAnchor(name="CREP", state_bits=64.0, anchor_bits=4.0, strength=0.5)
    assert anchor.drift_reduction(kappa=0.3, lambda_=0.8) == pytest.approx((0.8 / 0.3) * 0.5)


def test_drift_reduction_invalid_kappa():
    anchor = SemanticAnchor(name="CREP", state_bits=64.0, anchor_bits=4.0)
    with pytest.raises(ValueError):
        anchor.drift_reduction(kappa=0.0, lambda_=0.8)


def test_information_density():
    anchor = SemanticAnchor(name="Q4", state_bits=16.0, anchor_bits=4.0, strength=1.0)
    assert anchor.information_density() == pytest.approx(math.log2(4.0))


@pytest.mark.parametrize(
    ("state_bits", "anchor_bits", "strength"),
    [(0.0, 4.0, 1.0), (16.0, 0.0, 1.0), (16.0, 4.0, 1.5), (16.0, 4.0, -0.1)],
)
def test_invalid_construction(state_bits, anchor_bits, strength):
    with pytest.raises(ValueError):
        SemanticAnchor(name="x", state_bits=state_bits, anchor_bits=anchor_bits, strength=strength)
