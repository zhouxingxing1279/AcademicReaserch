#!/usr/bin/env python3
"""Illustrate finite certificates; floating geometry is not proof verification."""

import argparse
from fractions import Fraction
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle


ROOT = Path(__file__).resolve().parents[1]


def kernel_curve(angle, rate, torque):
    h = J = .02
    step = h * torque / J
    positive_knots = np.r_[np.arange(0, rate, step), rate]
    rho = np.unique(np.r_[-positive_knots, positive_knots])
    n = np.arange(int(np.ceil(rate / step)) + 1)
    def stop(s):
        return np.max(h * s[:, None] * n - h * step * n * (n - 1) / 2, axis=1)
    return rho, -angle + stop(np.maximum(-rho, 0)), angle - stop(np.maximum(rho, 0))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads((ROOT / "results/theory_terminal_polytope_20260911/certificate.json").read_text())
    a, b = [float(Fraction(x)) for x in data["minimal_transformed_radii"]]
    plt.rcParams["svg.fonttype"] = "none"
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10.5, 4.5), layout="constrained")
    ax.add_patch(Rectangle((-.0225, -.12), .045, .24, fill=False, ls="--", color="#777777", label="Previous outer box (not RPI)"))
    vertices = [(-a, b + 4*a), (-a, -b + 4*a), (a, -b - 4*a), (a, b - 4*a)]
    ax.add_patch(Polygon(vertices, facecolor="#93bdb5", edgecolor="#28564d", alpha=.9, label="Finite RPI polytope"))
    ax.add_patch(Rectangle((-.005, -.01), .01, .02, color="#315b85", alpha=.8, label="Initial error set"))
    ax.set(xlim=(-.027, .027), ylim=(-.15, .15), xlabel="Angle error (rad)", ylabel="Rate error (rad/s)", title="Four faces preserve error correlation")
    ax.legend(loc="upper right", fontsize=7)
    new_limits = [float(Fraction(x)) for x in data["reference_limits_angle_rate_torque"]]
    for limits, color, label in [(new_limits, "#93bdb5", "New reference certificate"), ([.4275, 1.88, .0504], "#c0c7d4", "Previous reference certificate")]:
        rho, lower, upper = kernel_curve(*limits)
        bx.fill_betweenx(rho, lower, upper, color=color, alpha=.8, label=label)
    bx.scatter([.43], [0], color="#a94936", s=24, zorder=4)
    bx.annotate("Strict witness: (0.43, 0)", xy=(.43, 0), xytext=(.02, -.9), arrowprops={"arrowstyle":"->", "color":"#a94936"}, fontsize=8)
    bx.set(xlim=(-.48, .48), ylim=(-2.1, 2.1), xlabel="Reference angle (rad)", ylabel="Reference rate (rad/s)", title="Larger certified reference kernel")
    bx.legend(loc="upper right", fontsize=7)
    for axis in (ax, bx):
        axis.grid(alpha=.2)
        axis.axhline(0, color="grey", lw=.5)
        axis.axvline(0, color="grey", lw=.5)
    fig.suptitle("Same model, noise bounds and feedback gains", fontsize=13)
    fig.supxlabel("Certificate improvement only; full six-state terminal invariance remains unproved.", fontsize=9)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    plt.close(fig)


if __name__ == "__main__":
    main()
