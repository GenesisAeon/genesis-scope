"""Fundamental constants for the genesis-scope semantic coordination model."""

from __future__ import annotations

import math

# ── Golden ratio family ──────────────────────────────────────────────────────
PHI: float = (1 + math.sqrt(5)) / 2
PHI_CUBEROOT: float = PHI ** (1 / 3)
PHI_SQUAREROOT: float = math.sqrt(PHI)

# ── Frame Principle ───────────────────────────────────────────────────────────
SIGMA_PHI: float = 1 / 16

# ── v_RIG cosmological velocity (Package 31) ─────────────────────────────────
C_KM_S: float = 299792.458
ALPHA_INV: float = 137.035999084
V_RIG_KM_S: float = C_KM_S / (ALPHA_INV * PHI)
V_CMB_DIPOLE_KM_S: float = 369.82
V_RIG_RATIO_CMB: float = V_RIG_KM_S / V_CMB_DIPOLE_KM_S

# ── Q4 / CREP defaults (contracts/runtime.schema.yaml) ───────────────────────
Q4_BITS: int = 4
Q4_STATES: int = 16
CREP_THRESHOLDS: dict[str, float] = {"C": 0.5, "R": 0.6, "E": 0.7, "P": 0.8}
GRAY_ORDER: list[int] = [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8]

# ── Drift model defaults (empirical estimates, P39) ──────────────────────────
DEFAULT_KAPPA: float = 0.3  # Drift rate per session
DEFAULT_LAMBDA: float = 0.8  # Anchor damping per anchor
