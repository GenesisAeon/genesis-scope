"""GenesisScope — Diamond interface for the semantic coordination model (Package 39)."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from genesis_scope.constants import DEFAULT_KAPPA, DEFAULT_LAMBDA, PHI_CUBEROOT, SIGMA_PHI
from genesis_scope.coordination_space import CoordinationPoint
from genesis_scope.crep_collaboration import CollaborationCREP
from genesis_scope.drift_model import DriftModel
from genesis_scope.q4_collaboration import crep_to_q4, q4_to_label
from genesis_scope.semantic_anchor import SemanticAnchor
from genesis_scope.session_tracker import SessionTracker
from genesis_scope.temporal_integration import TemporalIntegrator

# The canonical Sigillin (semantic anchors) of the GenesisAeon ecosystem.
DEFAULT_ANCHORS: tuple[SemanticAnchor, ...] = (
    SemanticAnchor(name="CREP", state_bits=64.0, anchor_bits=4.0, strength=0.9),
    SemanticAnchor(name="v_RIG", state_bits=32.0, anchor_bits=4.0, strength=0.85),
    SemanticAnchor(name="Q4", state_bits=16.0, anchor_bits=4.0, strength=0.95),
    SemanticAnchor(name="sigma_Phi", state_bits=16.0, anchor_bits=2.0, strength=0.8),
)


def _synthetic_crep(index: int) -> CollaborationCREP:
    """Generates a deterministic, plausible CREP(C,R,E,P) for session `index`.

    Values oscillate gently around the critical Gamma_collab regime
    (~0.35-0.55), modelling a maturing but still-evolving collaboration.
    """
    phase = index * (2 * math.pi / PHI_CUBEROOT) / 10.0
    c = 0.55 + 0.10 * math.sin(phase)
    r = 0.55 + 0.10 * math.cos(phase * 0.9)
    e = 0.45 + 0.10 * math.sin(phase * 1.3 + 1.0)
    p = 0.45 + 0.10 * math.cos(phase * 0.7 + 0.5)
    return CollaborationCREP(
        c=min(max(c, 0.0), 1.0),
        r=min(max(r, 0.0), 1.0),
        e=min(max(e, 0.0), 1.0),
        p=min(max(p, 0.0), 1.0),
    )


@dataclass
class GenesisScope:
    """Diamond interface implementation for genesis-scope (Package 39).

    Tracks a history of collaboration sessions, computes the collaboration
    CREP tensor, the semantic drift model, and Q4 phase events.
    """

    anchors: list[SemanticAnchor] = field(default_factory=lambda: list(DEFAULT_ANCHORS))
    kappa: float = DEFAULT_KAPPA
    lambda_: float = DEFAULT_LAMBDA
    tracker: SessionTracker = field(default_factory=SessionTracker)
    _last_n_sessions: int = 0

    def run_cycle(self, n_sessions: int = 38) -> dict[str, Any]:
        """Runs a full collaboration history of `n_sessions` sessions.

        Returns a summary dict with the final CREP state, drift status,
        coherence score and phase events.
        """
        if n_sessions < 1:
            raise ValueError("n_sessions must be >= 1")

        self.tracker = SessionTracker()
        self._last_n_sessions = n_sessions

        for i in range(1, n_sessions + 1):
            crep = _synthetic_crep(i)
            integrator = TemporalIntegrator(r=0.5, k=1.0, gamma=crep.gamma(), sigma=SIGMA_PHI)
            sigma_value = integrator.integrate(sigma0=0.1, t_span=(0, i), n_steps=2)[-1][1]
            point = CoordinationPoint(tau_a=float(i), tau_h=float(i), sigma=sigma_value)
            self.tracker.record(point, crep)

        return {
            "n_sessions": n_sessions,
            "crep_state": self.get_crep_state(),
            "utac_state": self.get_utac_state(),
            "phase_events": self.get_phase_events(),
            "coherence_score": self.coherence_score(),
            "drift_status": self.drift_status(),
            "anchor_count": self.anchor_count(),
        }

    def get_crep_state(self) -> dict[str, Any]:
        """Returns the most recent CREP(C,R,E,P) measurement and Gamma_collab."""
        if not self.tracker.sessions:
            return {"C": None, "R": None, "E": None, "P": None, "gamma": None}
        return self.tracker.sessions[-1].crep.as_dict()

    def get_utac_state(self) -> dict[str, Any]:
        """Returns the current semantic density Sigma(t) state."""
        if not self.tracker.sessions:
            return {"sigma": None, "q4_state": None, "q4_label": None}
        last = self.tracker.sessions[-1]
        q4_state = crep_to_q4(last.crep)
        return {
            "sigma": last.point.sigma,
            "q4_state": q4_state,
            "q4_label": q4_to_label(q4_state),
        }

    def get_phase_events(self) -> list[int]:
        """Returns session indices where Gamma_collab crossed the critical threshold."""
        return self.tracker.phase_events()

    def coherence_score(self) -> float:
        """Returns Gamma_collab in [0, 1] — current collaboration coherence."""
        if not self.tracker.sessions:
            return 0.0
        return self.tracker.mean_gamma()

    def drift_status(self) -> str:
        """Returns 'stable' | 'drifting' | 'anchored' for the current session history."""
        model = self._drift_model()
        d = self.tracker.collaboration_velocity()
        return model.status(d)

    def anchor_count(self) -> int:
        """Returns the number of registered semantic anchors."""
        return len(self.anchors)

    def v_rig_warning(self) -> bool:
        """Returns True if collaboration velocity exceeds the v_RIG threshold."""
        return self.tracker.v_rig_warning()

    def to_zenodo_record(self) -> dict[str, Any]:
        """Returns a Zenodo-compatible metadata record for this run."""
        return {
            "package": 39,
            "name": "genesis-scope",
            "domain": "meta-collaboration",
            "scale": "session",
            "zenodo": "10.5281/zenodo.17472834",
            "reference": "Johann Roemer x MOR Research Collective x Mai 2026",
            "n_sessions": self._last_n_sessions,
            "coherence_score": self.coherence_score(),
            "drift_status": self.drift_status(),
            "anchor_count": self.anchor_count(),
            "v_rig_warning": self.v_rig_warning(),
        }

    def _drift_model(self) -> DriftModel:
        return DriftModel(kappa=self.kappa, lambda_=self.lambda_, anchors=self.anchors)
