#!/usr/bin/env python3
"""Plot the proved finite-horizon bounds; no plant trajectories are simulated."""

import argparse
from fractions import Fraction
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "results/theory_coupling_20260910/exact_checks.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    if data["status"] != "EXACT_FINITE_HORIZON_SIX_STATE_ARITHMETIC_PASSED":
        raise ValueError("Expected the finite-horizon arithmetic result")
    rows = data["per_tick_enclosures"]
    times = [float(Fraction(row["time_s"])) for row in rows]
    limits = [5, 1.5, 3, 3, .45, 2]
    values = [[float(Fraction(row["absolute_bounds_relative_to_hover"][i])) / limits[i] for row in rows] for i in range(6)]
    labels = [r"$|p_x|/5$", r"$|p_z-2|/1.5$", r"$|v_x|/3$", r"$|v_z|/3$", r"$|\phi|/0.45$", r"$|\omega|/2$"]
    plt.rcParams["svg.fonttype"] = "none"
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), layout="constrained", sharey=True)
    for ax, title, indices in zip(axes, ["Position", "Velocity", "Attitude"], [(0, 1), (2, 3), (4, 5)]):
        for index, color in zip(indices, ["#245a81", "#ad6034"]):
            ax.plot(times, values[index], color=color, lw=2, label=labels[index])
        ax.axhline(1, color="#777777", ls="--", lw=1, label="Original limit")
        ax.set(title=title, xlabel="Time (s)", xlim=(0, .8), ylim=(0, 1.08))
        ax.grid(alpha=.2)
        ax.legend(loc="upper left", fontsize=8)
    axes[0].set_ylabel("Proved absolute bound / constraint limit")
    fig.suptitle("Six-state analytic enclosure under all allowed disturbances", fontsize=13)
    fig.supxlabel("Finite horizon only: 0.8 s. Curves are set bounds, not simulated states.", fontsize=9)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    plt.close(fig)


if __name__ == "__main__":
    main()
