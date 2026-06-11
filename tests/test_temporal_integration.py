"""Tests for genesis_scope.temporal_integration."""

from __future__ import annotations

import pytest

from genesis_scope.temporal_integration import TemporalIntegrator


def test_integrate_returns_correct_length():
    integrator = TemporalIntegrator(r=0.5, k=1.0, gamma=0.5)
    result = integrator.integrate(sigma0=0.1, t_span=(0, 10), n_steps=11)
    assert len(result) == 11
    assert result[0] == (0, 0.1)


def test_growth_toward_capacity():
    integrator = TemporalIntegrator(r=0.5, k=1.0, gamma=10.0, sigma=1.0)
    result = integrator.integrate(sigma0=0.1, t_span=(0, 50), n_steps=200)
    final_sigma = result[-1][1]
    assert final_sigma == pytest.approx(1.0, abs=0.05)


def test_zero_gamma_no_growth():
    integrator = TemporalIntegrator(r=0.5, k=1.0, gamma=0.0)
    result = integrator.integrate(sigma0=0.1, t_span=(0, 10), n_steps=11)
    assert result[-1][1] == pytest.approx(0.1)


def test_invalid_r():
    with pytest.raises(ValueError):
        TemporalIntegrator(r=0.0, k=1.0, gamma=0.5)


def test_invalid_k():
    with pytest.raises(ValueError):
        TemporalIntegrator(r=0.5, k=0.0, gamma=0.5)


def test_invalid_n_steps():
    integrator = TemporalIntegrator(r=0.5, k=1.0, gamma=0.5)
    with pytest.raises(ValueError):
        integrator.integrate(sigma0=0.1, t_span=(0, 10), n_steps=1)
