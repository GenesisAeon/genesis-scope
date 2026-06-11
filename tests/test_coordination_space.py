"""Tests for genesis_scope.coordination_space."""

from __future__ import annotations

import math

import pytest

from genesis_scope.coordination_space import (
    CoordinationPoint,
    CoordinationSpace,
    fisher_rao_velocity,
)


def test_fisher_rao_velocity_simple():
    p1 = CoordinationPoint(tau_a=0, tau_h=0, sigma=0)
    p2 = CoordinationPoint(tau_a=0, tau_h=1, sigma=0)
    assert fisher_rao_velocity(p1, p2) == pytest.approx(1.0)


def test_fisher_rao_velocity_diagonal():
    p1 = CoordinationPoint(tau_a=0, tau_h=0, sigma=0)
    p2 = CoordinationPoint(tau_a=3, tau_h=1, sigma=4)
    assert fisher_rao_velocity(p1, p2) == pytest.approx(math.sqrt(3**2 + 1**2 + 4**2))


def test_fisher_rao_velocity_requires_distinct_tau_h():
    p1 = CoordinationPoint(tau_a=0, tau_h=1, sigma=0)
    p2 = CoordinationPoint(tau_a=1, tau_h=1, sigma=1)
    with pytest.raises(ValueError):
        fisher_rao_velocity(p1, p2)


def test_coordination_space_velocities_and_mean():
    points = [
        CoordinationPoint(tau_a=0, tau_h=0, sigma=0),
        CoordinationPoint(tau_a=0, tau_h=1, sigma=0),
        CoordinationPoint(tau_a=0, tau_h=2, sigma=0),
    ]
    space = CoordinationSpace(points=points)
    assert space.velocities() == [pytest.approx(1.0), pytest.approx(1.0)]
    assert space.mean_velocity() == pytest.approx(1.0)


def test_coordination_space_empty_mean_velocity():
    space = CoordinationSpace(points=[])
    assert space.mean_velocity() == 0.0


def test_coordination_space_add():
    space = CoordinationSpace(points=[])
    space.add(CoordinationPoint(tau_a=0, tau_h=0, sigma=0))
    assert len(space.points) == 1
