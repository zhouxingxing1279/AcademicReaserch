"""Audit existing frozen results and plot comparisons; never reruns control."""
from pathlib import Path
from collections import defaultdict
import csv
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments/results/cong_mpc_validation"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(name):
    with (OUT / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def key(row):
    return row["model"], int(row["case_id"]), int(row["period"])


def quant(values):
    return np.quantile(np.asarray(values, dtype=float), [0, .5, .95, 1]).tolist()


def main():
    summary = json.loads((OUT / "summary.json").read_text(encoding="utf-8"))
    for name, digest in summary["source_sha256"].items():
        assert sha(ROOT / name) == digest, name
    for name, digest in summary["artifact_sha256"].items():
        assert sha(OUT / name) == digest, name
    cases, steps, static = read("cases.csv"), read("steps.csv"), read("static.csv")
    assert len(cases) == 1056 and len(steps) == 31680 and len(static) == 2592
    reference = {key(r): r for r in cases if r["method"] == "exact"}
    assert len(reference) == 96
    by_run = defaultdict(list)
    for r in steps:
        by_run[(*key(r), r["method"], r["budget"])].append(r)
        assert float(r["state_violation"]) <= 2e-6
        assert float(r["input_violation"]) <= 2e-6
        if r["method"] in ("control", "geometry", "uniform"):
            assert int(r["anchor_faces"]) <= int(r["budget"])
    for r in cases:
        rs = by_run[(*key(r), r["method"], r["budget"])]
        assert len(rs) == 30 and {int(v["k"]) for v in rs} == set(range(30))
        assert abs(sum(float(v["cost"]) for v in rs) - float(r["cost"])) < 1e-10
        assert sum(int(v["fallback"]) for v in rs) == int(r["fallback_steps"])
    output = {
        "audit_date": "2026-11-05",
        "plan_date": "2026-11-04",
        "execution_date_note": "summary.date is the frozen plan date; run.log and result files were completed on 2026-11-05 Asia/Shanghai.",
        "hashes_verified": len(summary["source_sha256"]) + len(summary["artifact_sha256"]),
        "unique_paired_scenarios": 96,
        "counts": {"cases": len(cases), "steps": len(steps), "static": len(static)},
        "safety": {"max_state_residual": max(float(r["state_violation"]) for r in steps),
                   "max_input_residual": max(float(r["input_violation"]) for r in steps)},
        "timing_caveat": "Exact posterior prediction is outside its recorded online_ms. Do not compare exact online_ms with compressed-method end-to-end timings. The three bounded methods include prediction, conditioning, selection and QP, but exclude the common nominal observer update and independent audits. These are single-run measurements, not WCET.",
        "groups": [], "pairs": [], "observation": [], "by_model_period": []
    }
    for budget in (6, 8, 12):
        for method in ("uniform", "geometry", "control"):
            cs = [r for r in cases if r["method"] == method and int(r["budget"]) == budget]
            ss = [r for r in steps if r["method"] == method and int(r["budget"]) == budget and int(r["k"]) > 0]
            st = [r for r in static if r["method"] == method and int(r["budget"]) == budget]
            output["groups"].append({
                "method": method, "budget": budget, "cases": len(cs),
                "mean_cost": float(np.mean([float(r["cost"]) for r in cs])),
                "cost_change_vs_exact_pct_min_median_p95_max": quant([100 * (float(r["cost"])/float(reference[key(r)]["cost"])-1) for r in cs]),
                "fallback_steps": sum(int(r["fallback_steps"]) for r in cs),
                "shift_lost_steps": sum(int(r["shift_lost_steps"]) for r in cs),
                "static_count": len(st),
                "static_qp_feasible": sum(int(r["qp_feasible"]) for r in st),
                "static_shift_preserved": sum(int(r["shift_preserved"]) for r in st),
                "static_max_gap": max(float(r["max_direction_gap"]) for r in st),
                "online_ms_min_median_p95_max": quant([float(r["online_ms"]) for r in ss]),
                "queries_min_median_p95_max": quant([float(r["support_queries"]) for r in ss]),
                "stored_faces_max": max(int(r["anchor_faces"]) for r in ss),
                "working_vertices_max": max(int(r["working_vertices"]) for r in ss),
            })
        cc = {key(r): r for r in cases if r["method"] == "control" and int(r["budget"]) == budget}
        for base in ("geometry", "uniform"):
            bb = {key(r): r for r in cases if r["method"] == base and int(r["budget"]) == budget}
            delta = [100 * (float(cc[k]["cost"])/float(bb[k]["cost"])-1) for k in cc]
            output["pairs"].append({"budget": budget, "baseline": base, "n": len(delta),
                                    "cost_change_pct_min_median_p95_max": quant(delta),
                                    "lower_count_tol_1e_6_pct": sum(d < -1e-6 for d in delta),
                                    "higher_count_tol_1e_6_pct": sum(d > 1e-6 for d in delta)})
    for model in ("fast", "slow"):
        for period in (0, 1, 3):
            for method in ("exact", "full", "uniform", "geometry", "control"):
                for budget in ((0,) if method == "exact" else ((42 if model == "fast" else 66),) if method == "full" else (6, 8, 12)):
                    cs = [r for r in cases if r["model"] == model and int(r["period"]) == period and r["method"] == method and int(r["budget"]) == budget]
                    output["by_model_period"].append({"model": model, "period": period, "method": method, "budget": budget,
                        "cases": len(cs), "mean_cost": float(np.mean([float(r["cost"]) for r in cs])),
                        "fallback_steps": sum(int(r["fallback_steps"]) for r in cs),
                        "max_stored_faces": max(int(r["max_stored_faces"]) for r in cs)})
        for period in (0, 3):
            delta = [100*(float(reference[(model, i, period)]["cost"])/float(reference[(model, i, 1)]["cost"])-1) for i in range(16)]
            output["observation"].append({"model": model, "period_vs_every_step": period,
                                         "n": 16, "cost_change_pct_min_median_p95_max": quant(delta)})
    independent = json.loads((OUT / "independent_audit.json").read_text(encoding="utf-8"))
    output["independent_support_checks"] = sum(r["queries"] for r in independent)
    output["max_independent_support_disagreement"] = max(r["max_support_disagreement"] for r in independent)
    output["audit_script_sha256"] = sha(Path(__file__))
    (OUT / "audit.json").write_text(json.dumps(output, indent=2), encoding="utf-8")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.7), layout="constrained")
    colors = {"uniform": "#ad7d35", "geometry": "#527a8a", "control": "#a04c56"}
    for method, color in colors.items():
        gs = [r for r in output["groups"] if r["method"] == method]
        budgets = [r["budget"] for r in gs]
        axes[0].plot(budgets, [100*r["static_qp_feasible"]/r["static_count"] for r in gs], "-o", color=color, label=method)
        axes[1].plot(budgets, [r["online_ms_min_median_p95_max"][1] for r in gs], "-o", color=color, label=method)
        axes[1].plot(budgets, [r["online_ms_min_median_p95_max"][2] for r in gs], "--", color=color, alpha=.6)
    axes[0].set(title="Same-posterior QP feasibility", xlabel="Persistent facet cap", ylabel="Feasible snapshots (%)", ylim=(0, 102), xticks=[6,8,12])
    axes[0].legend(frameon=False)
    axes[1].set(title="Selection cost is included", xlabel="Persistent facet cap", ylabel="Online time (ms)", xticks=[6,8,12])
    axes[1].text(.02, .98, "solid: median; dashed: P95\nExact timing excluded (scope mismatch)", transform=axes[1].transAxes, va="top", fontsize=8)
    for j, budget in enumerate((6, 8, 12)):
        cc = {key(r): r for r in cases if r["method"] == "control" and int(r["budget"]) == budget}
        bb = {key(r): r for r in cases if r["method"] == "geometry" and int(r["budget"]) == budget}
        delta = np.array([100*(float(cc[k]["cost"])/float(bb[k]["cost"])-1) for k in cc])
        axes[2].scatter(j + np.linspace(-.15,.15,len(delta)), delta, s=9, alpha=.55, color=colors["control"])
        axes[2].plot([j-.22,j+.22], [np.median(delta)]*2, color="black")
    axes[2].axhline(0, color="gray", lw=1)
    axes[2].set(title="Control-aware vs geometry baseline", ylabel="Paired cost change (%)", xticks=[0,1,2], xticklabels=[6,8,12], xlabel="Persistent facet cap")
    fig.suptitle("Frozen 2-D validation: 96 scenarios per controller; lower cost is better", fontsize=12)
    fig.savefig(OUT / "validation_evidence.png", dpi=180)
    fig.savefig(OUT / "validation_evidence.pdf")
    print(json.dumps({k:v for k,v in output.items() if k != "by_model_period"}, indent=2))


if __name__ == "__main__":
    main()
