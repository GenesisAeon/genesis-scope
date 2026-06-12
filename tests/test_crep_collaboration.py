"""Tests for genesis_scope.crep_collaboration."""

from __future__ import annotations

import pytest

from genesis_scope.crep_collaboration import CollaborationCREP


def test_gamma_calculation():
    crep = CollaborationCREP(c=1.0, r=1.0, e=1.0, p=1.0)
    assert crep.gamma() == 1.0


def test_gamma_zero():
    crep = CollaborationCREP(c=0.0, r=1.0, e=1.0, p=1.0)
    assert crep.gamma() == 0.0


def test_is_critical():
    crep = CollaborationCREP(c=0.4, r=0.4, e=0.4, p=0.4)
    assert crep.is_critical()


def test_is_not_critical():
    crep = CollaborationCREP(c=1.0, r=1.0, e=1.0, p=1.0)
    assert not crep.is_critical()


def test_as_dict():
    crep = CollaborationCREP(c=0.5, r=0.5, e=0.5, p=0.5)
    d = crep.as_dict()
    assert set(d.keys()) == {"C", "R", "E", "P", "gamma"}
    assert d["gamma"] == pytest.approx(0.5)


@pytest.mark.parametrize("bad", [-0.1, 1.1])
def test_invalid_values(bad):
    with pytest.raises(ValueError):
        CollaborationCREP(c=bad, r=0.5, e=0.5, p=0.5)
