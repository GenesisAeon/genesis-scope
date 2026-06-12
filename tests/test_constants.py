"""Tests for genesis_scope.constants."""

from __future__ import annotations

import math

from genesis_scope import constants


def test_phi_cuberoot():
    assert math.isclose(constants.PHI_CUBEROOT, constants.PHI ** (1 / 3), rel_tol=1e-12)
    assert math.isclose(constants.PHI_CUBEROOT, 1.174, abs_tol=1e-3)


def test_v_rig_value():
    assert math.isclose(constants.V_RIG_KM_S, 1352.12, abs_tol=0.5)


def test_v_rig_ratio_cmb():
    assert math.isclose(constants.V_RIG_RATIO_CMB, 3.66, abs_tol=0.05)


def test_sigma_phi():
    assert constants.SIGMA_PHI == 1 / 16


def test_q4_constants():
    assert constants.Q4_BITS == 4
    assert constants.Q4_STATES == 16
    assert len(constants.GRAY_ORDER) == 16
    assert sorted(constants.GRAY_ORDER) == list(range(16))
