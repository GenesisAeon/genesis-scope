"""genesis-scope — semantic coordination system for human-LLM collaboration (Package 39)."""

from genesis_scope.coordination_space import CoordinationPoint, CoordinationSpace
from genesis_scope.crep_collaboration import CollaborationCREP
from genesis_scope.drift_model import DriftModel
from genesis_scope.semantic_anchor import SemanticAnchor
from genesis_scope.session_tracker import Session, SessionTracker
from genesis_scope.system import GenesisScope

__version__ = "0.1.0"
__author__ = "GenesisAeon"

__all__ = [
    "CollaborationCREP",
    "CoordinationPoint",
    "CoordinationSpace",
    "DriftModel",
    "GenesisScope",
    "SemanticAnchor",
    "Session",
    "SessionTracker",
    "__author__",
    "__version__",
]
