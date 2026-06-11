"""Tests for genesis_scope.benchmark."""

from __future__ import annotations

from genesis_scope.benchmark import SCOPE_TARGETS, evaluate


def test_evaluate_returns_all_targets():
    results = evaluate(n_sessions=38)
    assert set(results.keys()) == set(SCOPE_TARGETS.keys())


def test_evaluate_result_shape():
    results = evaluate(n_sessions=38)
    for result in results.values():
        assert {"value", "target", "tolerance", "passed"} <= set(result.keys())
        assert isinstance(result["passed"], bool)


def test_session_coherence_passes():
    results = evaluate(n_sessions=38)
    assert results["session_coherence_p38"]["passed"]


def test_v_rig_warning_not_triggered():
    results = evaluate(n_sessions=38)
    assert results["v_rig_warning_triggered"]["passed"]
