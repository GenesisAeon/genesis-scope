"""Tests for genesis_scope.drift_model."""

from __future__ import annotations

import math

import pytest

from genesis_scope.drift_model import DriftModel
from genesis_scope.semantic_anchor import SemanticAnchor


def test_no_anchors_decay_to_zero():
    model = DriftModel(kappa=0.3, lambda_=0.8, anchors=[])
    assert model.fixed_point() == 0.0
    # D(t) = D0 * exp(-kappa * t) when D* == 0
    assert model.drift_at(t=1.0, d0=1.0) == pytest.approx(math.exp(-0.3))


def test_fixed_point_with_anchors():
    anchors = [SemanticAnchor(name="a", state_bits=16, anchor_bits=4, strength=1.0)]
    model = DriftModel(kappa=0.3, lambda_=0.8, anchors=anchors)
    assert model.fixed_point() == pytest.approx(0.8 / 0.3)


def test_drift_converges_to_fixed_point():
    anchors = [SemanticAnchor(name="a", state_bits=16, anchor_bits=4, strength=1.0)]
    model = DriftModel(kappa=0.3, lambda_=0.8, anchors=anchors)
    d_far = model.drift_at(t=1000.0, d0=10.0)
    assert d_far == pytest.approx(model.fixed_point(), abs=1e-6)


def test_trajectory_length():
    model = DriftModel(kappa=0.3, lambda_=0.8, anchors=[])
    traj = model.trajectory((0, 10), n_steps=11)
    assert len(traj) == 11
    assert traj[0][0] == 0
    assert traj[-1][0] == 10


def test_status_anchored():
    anchors = [SemanticAnchor(name="a", state_bits=16, anchor_bits=4, strength=1.0)]
    model = DriftModel(kappa=0.3, lambda_=0.8, anchors=anchors)
    assert model.status(d=0.0) == "anchored"


def test_status_drifting_without_anchors():
    model = DriftModel(kappa=0.3, lambda_=0.0, anchors=[])
    assert model.status(d=5.0) == "drifting"


def test_status_stable():
    model = DriftModel(kappa=0.3, lambda_=0.0, anchors=[])
    assert model.status(d=0.0) == "stable"


def test_invalid_kappa():
    with pytest.raises(ValueError):
        DriftModel(kappa=0.0, lambda_=0.8)


def test_invalid_lambda():
    with pytest.raises(ValueError):
        DriftModel(kappa=0.3, lambda_=-1.0)
