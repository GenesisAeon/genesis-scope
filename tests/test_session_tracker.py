"""Tests for genesis_scope.session_tracker."""

from __future__ import annotations

from genesis_scope.coordination_space import CoordinationPoint
from genesis_scope.crep_collaboration import CollaborationCREP
from genesis_scope.session_tracker import SessionTracker


def test_record_and_mean_gamma():
    tracker = SessionTracker()
    tracker.record(
        CoordinationPoint(tau_a=0, tau_h=0, sigma=0.1), CollaborationCREP(0.5, 0.5, 0.5, 0.5)
    )
    tracker.record(
        CoordinationPoint(tau_a=1, tau_h=1, sigma=0.2), CollaborationCREP(0.6, 0.6, 0.6, 0.6)
    )
    assert tracker.mean_gamma() > 0


def test_empty_tracker():
    tracker = SessionTracker()
    assert tracker.mean_gamma() == 0.0
    assert tracker.collaboration_velocity() == 0.0
    assert not tracker.v_rig_warning()
    assert tracker.phase_events() == []


def test_v_rig_warning_not_triggered_for_small_steps():
    tracker = SessionTracker()
    for i in range(5):
        tracker.record(
            CoordinationPoint(tau_a=float(i), tau_h=float(i), sigma=0.1 * i),
            CollaborationCREP(0.5, 0.5, 0.5, 0.5),
        )
    assert not tracker.v_rig_warning()


def test_phase_events_detected():
    tracker = SessionTracker()
    crep_low = CollaborationCREP(0.3, 0.3, 0.3, 0.3)  # gamma = 0.3 < 0.5
    crep_high = CollaborationCREP(0.9, 0.9, 0.9, 0.9)  # gamma = 0.9 >= 0.5
    tracker.record(CoordinationPoint(tau_a=0, tau_h=0, sigma=0), crep_low)
    tracker.record(CoordinationPoint(tau_a=1, tau_h=1, sigma=1), crep_high)
    tracker.record(CoordinationPoint(tau_a=2, tau_h=2, sigma=2), crep_high)
    assert tracker.phase_events() == [1]
