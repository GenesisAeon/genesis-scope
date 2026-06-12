"""Tracks collaboration sessions as a trajectory in coordination space.

Each session is a point P_i = (tau_A, tau_H, Sigma) plus a CREP(C,R,E,P)
measurement. The trajectory's Fisher-Rao velocity is compared against the
v_RIG threshold (Package 31): if the collaboration drifts through the
coordination space faster than v_RIG, semantic anchors are recommended.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from genesis_scope.constants import V_RIG_RATIO_CMB
from genesis_scope.coordination_space import CoordinationPoint, CoordinationSpace
from genesis_scope.crep_collaboration import CollaborationCREP


@dataclass
class Session:
    """A single recorded collaboration session."""

    point: CoordinationPoint
    crep: CollaborationCREP


@dataclass
class SessionTracker:
    """Records sessions and evaluates collaboration coherence over time."""

    sessions: list[Session] = field(default_factory=list)
    v_rig_threshold: float = V_RIG_RATIO_CMB

    def record(self, point: CoordinationPoint, crep: CollaborationCREP) -> Session:
        """Records a new session and returns it."""
        session = Session(point=point, crep=crep)
        self.sessions.append(session)
        return session

    def coordination_space(self) -> CoordinationSpace:
        """Returns the CoordinationSpace built from all recorded sessions."""
        return CoordinationSpace(points=[s.point for s in self.sessions])

    def mean_gamma(self) -> float:
        """Returns the mean Gamma_collab over all sessions."""
        if not self.sessions:
            return 0.0
        return sum(s.crep.gamma() for s in self.sessions) / len(self.sessions)

    def collaboration_velocity(self) -> float:
        """Returns the mean Fisher-Rao velocity across recorded sessions."""
        return self.coordination_space().mean_velocity()

    def v_rig_warning(self) -> bool:
        """Returns True if the collaboration velocity exceeds v_RIG.

        A warning means the shared semantic state is drifting faster than
        the v_RIG threshold and additional semantic anchors are recommended.
        """
        if len(self.sessions) < 2:
            return False
        return self.collaboration_velocity() > self.v_rig_threshold

    def phase_events(self) -> list[int]:
        """Returns indices of sessions where the Q4-relevant Gamma jumped.

        A phase event is a session where Gamma_collab crosses 0.5 relative
        to the previous session.
        """
        events: list[int] = []
        for i in range(1, len(self.sessions)):
            prev = self.sessions[i - 1].crep.gamma()
            curr = self.sessions[i].crep.gamma()
            if (prev < 0.5) != (curr < 0.5):
                events.append(i)
        return events
