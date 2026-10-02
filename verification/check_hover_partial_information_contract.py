#!/usr/bin/env python3
"""Exact algebra audit for the frozen hover partial-information contract.

This checker instantiates one physical, observer, and nominal successor from
the same primitive realization.  It does not synthesize a policy or an
invariant set.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_augmented_rci_contract import audit_contract


ROOT = Path(__file__).resolve().parents[1]
H = F(1, 50)
GRAVITY = F(981, 100)
INERTIA = F(1, 50)
ELL_X = F(5)
ELL_Z = F(9, 2)
PHI_MAX = F(9, 20)
THRUST_MIN = F(981, 200)
THRUST_MAX = F(2943, 200)
NOISE_WIDTHS = {
    "n_px_next": F(1, 50),
    "n_pz_next": F(1, 50),
    "n_phi_next": F(1, 200),
    "n_omega_next": F(1, 100),
}
RUN136_WX_WIDTH = F(47, 25) + (THRUST_MAX - GRAVITY) * PHI_MAX + F(243, 16000) * THRUST_MAX
RUN136_WZ_WIDTH = F(1043, 500) + F(81, 800) * THRUST_MAX


def audit_config_constants(config):
    """Fail if this independent exact oracle drifts from the frozen config."""
    assert config["plant"]["dt_s"] == H
    assert config["plant"]["gravity_m_s2"] == GRAVITY
    assert config["plant"]["inertia_kg_m2"] == INERTIA
    assert config["domain"]["state_upper"][4] == PHI_MAX
    assert config["domain"]["state_lower"][4] == -PHI_MAX
    assert config["domain"]["input_lower"][0] == THRUST_MIN
    assert config["domain"]["input_upper"][0] == THRUST_MAX
    noise = config["sensing"]["observed_noise_halfwidth"]
    assert noise == {"px": F(1, 50), "pz": F(1, 50), "phi": F(1, 200), "omega": F(1, 100)}


def _add(a, b):
    return [x + y for x, y in zip(a, b)]


def _sub(a, b):
    return [x - y for x, y in zip(a, b)]


def _physical_successor(x, actual_input, primitives):
    px, pz, vx, vz, phi, omega = x
    thrust, torque = actual_input
    return [
        px + H * vx,
        pz + H * vz,
        vx - H * thrust * phi + H * primitives["r_x"],
        vz + H * (thrust - GRAVITY) + H * primitives["r_z"],
        phi + H * omega,
        omega + H * torque / INERTIA,
    ]


def _nominal_successor(z, nominal_input):
    px, pz, vx, vz, phi, omega = z
    thrust, torque = nominal_input
    return [
        px + H * vx,
        pz + H * vz,
        vx - H * thrust * phi,
        vz + H * (thrust - GRAVITY),
        phi + H * omega,
        omega + H * torque / INERTIA,
    ]


def _observer_successor(success, x_next, hat, actual_input, primitives):
    px, pz, vx, vz, phi, omega = hat
    thrust, torque = actual_input
    predicted = [
        px + H * vx,
        pz + H * vz,
        vx - H * GRAVITY * phi,
        vz + H * (thrust - GRAVITY),
        phi + H * omega,
        omega + H * torque / INERTIA,
    ]
    if success:
        measured_px = x_next[0] + primitives["n_px_next"]
        measured_pz = x_next[1] + primitives["n_pz_next"]
        innovation_x = measured_px - predicted[0]
        innovation_z = measured_pz - predicted[1]
        predicted[0] = measured_px
        predicted[1] = measured_pz
        predicted[2] += ELL_X * innovation_x
        predicted[3] += ELL_Z * innovation_z
    predicted[4] = x_next[4] + primitives["n_phi_next"]
    predicted[5] = x_next[5] + primitives["n_omega_next"]
    return predicted


def _realize_primitives(actual_thrust, normalized):
    required = {"rho_x", "rho_z", *NOISE_WIDTHS}
    if set(normalized) != required:
        raise ValueError("normalized primitive vector does not match the frozen graph")
    if any(abs(value) > 1 for value in normalized.values()):
        raise ValueError("normalized primitive lies outside the unit box")
    return {
        "r_x": (F(47, 25) + F(243, 16000) * actual_thrust) * normalized["rho_x"],
        "r_z": (F(1043, 500) + F(81, 800) * actual_thrust) * normalized["rho_z"],
        **{name: width * normalized[name] for name, width in NOISE_WIDTHS.items()},
    }


def _run136_eta_oracle(success, eta, x_phi, actual_thrust, realized):
    """Independent Run136 edge-map form, including w_x transformation."""
    n_phi_current = -eta[4]
    w_x = realized["r_x"] + (GRAVITY - actual_thrust) * x_phi
    w_z = realized["r_z"]
    eta_px = eta[0] + H * eta[2]
    eta_pz = eta[1] + H * eta[3]
    eta_vx = eta[2] + H * (w_x + GRAVITY * n_phi_current)
    eta_vz = eta[3] + H * w_z
    if success:
        eta_vx -= ELL_X * (eta_px + realized["n_px_next"])
        eta_vz -= ELL_Z * (eta_pz + realized["n_pz_next"])
        eta_px = -realized["n_px_next"]
        eta_pz = -realized["n_pz_next"]
    expected = [
        eta_px, eta_pz, eta_vx, eta_vz,
        -realized["n_phi_next"], -realized["n_omega_next"],
    ]
    return expected, w_x, w_z, n_phi_current


def split_successor(*, success, eta, d, z, nominal_input, correction, primitives):
    """Return exact eta/d/e successors under one shared primitive realization."""
    if not all(len(v) == 6 for v in (eta, d, z)):
        raise ValueError("eta, d, and z must follow the six-state ordering")
    actual_input = _add(nominal_input, correction)
    realized = _realize_primitives(actual_input[0], primitives)
    tracking_error = _add(eta, d)
    x = _add(z, tracking_error)
    hat = _add(z, d)
    x_next = _physical_successor(x, actual_input, realized)
    z_next = _nominal_successor(z, nominal_input)
    hat_next = _observer_successor(success, x_next, hat, actual_input, realized)
    eta_next = _sub(x_next, hat_next)
    d_next = _sub(hat_next, z_next)
    tracking_error_next = _sub(x_next, z_next)
    if _add(eta_next, d_next) != tracking_error_next:
        raise AssertionError("shared-primitives split identity failed")
    eta_oracle, w_x, w_z, n_phi_current = _run136_eta_oracle(
        success, eta, x[4], actual_input[0], realized
    )
    if eta_next != eta_oracle:
        raise AssertionError("observer successor disagrees with independent Run136 edge-map oracle")
    source_domain = (
        THRUST_MIN <= actual_input[0] <= THRUST_MAX
        and abs(x[4]) <= PHI_MAX
        and abs(n_phi_current) <= NOISE_WIDTHS["n_phi_next"]
    )
    bounds_ok = source_domain and abs(w_x) <= RUN136_WX_WIDTH and abs(w_z) <= RUN136_WZ_WIDTH
    return {
        "eta_next": eta_next,
        "eta_next_oracle": eta_oracle,
        "d_next": d_next,
        "tracking_error_next": tracking_error_next,
        "realized_primitives": realized,
        "run136_disturbance": {"w_x": w_x, "w_z": w_z, "n_phi_current": n_phi_current},
        "run136_bounds_ok": bounds_ok,
    }


def run():
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text(), parse_float=F)
    audit_config_constants(config)
    audit = audit_contract(config, root=ROOT)
    assert audit["status"] == "ready"
    contract = config["mpc"]["ancillary_rci_contract"]
    edges = contract["mode_graph"]["edges"]
    probe = {
        "eta": [F(1, 100), F(-1, 100), F(1, 20), F(-1, 20), F(1, 1000), F(-1, 500)],
        "d": [F(-1, 50), F(1, 50), F(-1, 25), F(1, 25), F(-1, 500), F(1, 250)],
        "z": [F(1, 10), F(2), F(1, 20), F(-1, 20), F(1, 100), F(-1, 100)],
        "nominal_input": [GRAVITY, F(0)],
        "correction": [F(1, 10), F(1, 100)],
        "primitives": {
            "rho_x": F(1, 5),
            "rho_z": F(-1, 4),
            "n_px_next": F(1, 2),
            "n_pz_next": F(-1, 2),
            "n_phi_next": F(1, 5),
            "n_omega_next": F(-1, 5),
        },
    }
    checks = []
    for source, target, label in edges:
        result = split_successor(success=label == "success", **probe)
        checks.append({
            "from": source,
            "to": target,
            "label": label,
            "pass": (
                result["eta_next"] == result["eta_next_oracle"]
                and _add(result["eta_next"], result["d_next"])
                == result["tracking_error_next"]
                and result["run136_bounds_ok"]
            ),
        })
    assert len(checks) == 17 and all(row["pass"] for row in checks)

    nominal = contract["nominal_state_domain"]
    hover = [F(0), F(2), F(0), F(0), F(0), F(0)]
    assert all(lo < x < hi for lo, x, hi in zip(nominal["lower"], hover, nominal["upper"]))
    return {
        "status": "pass",
        "claim": "hover_partial_information_problem_contract_is_executable",
        "edge_contract_checks": checks,
        "run136_bridge": {
            "transformation": "w_x = r_x + (gravity - actual_thrust) * true_phi",
            "certified_halfwidth": {"w_x": RUN136_WX_WIDTH, "w_z": RUN136_WZ_WIDTH},
            "boundary_checks": "covered_by_unit_tests_at_thrust_and_phi_extrema",
        },
        "hover_is_strictly_interior": True,
        "policy_class": contract["policy"]["class"],
        "evidence_level": "problem_contract_ready_not_an_invariant_set_certificate",
        "limitations": [
            "no policy coefficients or invariant set have been synthesized",
            "the nominal box is an existence-probe domain, not a maneuvering MPC domain",
            "exact split algebra does not prove source-domain closure or recursive feasibility",
        ],
    }


def _encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, list):
        return [_encode(v) for v in value]
    if isinstance(value, dict):
        return {k: _encode(v) for k, v in value.items()}
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = run()
    sources = [
        "verification/check_hover_partial_information_contract.py",
        "verification/test_hover_partial_information_contract.py",
        "verification/check_augmented_rci_contract.py",
        "configs/planar_baseline.json",
        "docs/research/run140_literature_gate.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(_encode(result), indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(_encode(result), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
