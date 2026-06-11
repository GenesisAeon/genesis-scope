"""Tests for genesis_scope.system."""

from __future__ import annotations

import pytest

from genesis_scope.system import GenesisScope


def test_run_cycle_default():
    scope = GenesisScope()
    result = scope.run_cycle()
    assert result["n_sessions"] == 38
    assert 0.0 <= result["coherence_score"] <= 1.0
    assert result["drift_status"] in {"stable", "drifting", "anchored"}
    assert result["anchor_count"] == 4


def test_run_cycle_custom_n():
    scope = GenesisScope()
    result = scope.run_cycle(n_sessions=5)
    assert result["n_sessions"] == 5


def test_run_cycle_invalid_n():
    scope = GenesisScope()
    with pytest.raises(ValueError):
        scope.run_cycle(n_sessions=0)


def test_get_crep_state_before_run():
    scope = GenesisScope()
    state = scope.get_crep_state()
    assert state["gamma"] is None


def test_get_utac_state_after_run():
    scope = GenesisScope()
    scope.run_cycle(n_sessions=5)
    state = scope.get_utac_state()
    assert state["sigma"] is not None
    assert state["q4_label"] is not None
    assert len(state["q4_label"]) == 4


def test_get_phase_events_is_list():
    scope = GenesisScope()
    scope.run_cycle(n_sessions=10)
    assert isinstance(scope.get_phase_events(), list)


def test_to_zenodo_record():
    scope = GenesisScope()
    scope.run_cycle(n_sessions=5)
    record = scope.to_zenodo_record()
    assert record["package"] == 39
    assert record["name"] == "genesis-scope"
    assert record["n_sessions"] == 5
