# Gate T3 — two-timestamp causal velocity bound (2026-11-03)

Status: **conditional analytic bound and finite-word enumeration; not CZ, Equalized Recovery, or MPC safety theorem**. This note follows the checkpoint's six-state abstract outer-loop model and the previous fixed-gain SMM instability counterexample. No PX4/ArduPilot interface assumptions.

## Frozen minimal assumptions

For each axis, continuous-time `dot p=v, dot v=a(t)` with `|a(t)|<=a_bar` for every time, exact sampling interval `T>0`; every successful position measurement at timestamp `t_j` is `y_j=p(t_j)+nu_j`, `|nu_j|<=nu_bar`. Known input effects are removed from the position differences; remaining unknown acceleration is included in `a_bar`. At each control time `t`, only measurements already **received** may be used. Initially two distinct successful timestamps must be available. For this initial no-delay success/miss baseline, no more than `L=2` consecutive misses; timestamp and receipt time coincide. Delays require a separate timestamp-aware automaton.

Let the two most recently received distinct successful timestamps be `t_1<t_2<=t`, `h=t_2-t_1=dT`, `tau=t-t_2=age*T`. Define causal velocity estimate `vhat(t)=(y_2-y_1)/h` (without unknown-acceleration correction). Then for **every** admissible acceleration function and measurement noise realization,

`|v(t)-vhat(t)| <= 2 nu_bar/h + (h/2+tau) a_bar`.

Proof: `(p(t_2)-p(t_1))/h=(1/h)int_[t_1,t_2]v(s)ds`. Since `|v(t_1)-v(s)|<=a_bar(s-t_1)`, the difference between this average and `v(t_1)` is at most `h a_bar/2`; moving from `t_1` to `t` directly would yield `(h/2+tau)a_bar` only if we compare with `v(t_2)`, because `|v(t_2)-average v|<=h a_bar/2`. The two measurement noise contributions are at most `2nu_bar/h`. Triangle inequality proves the displayed result. Componentwise application gives a six-state model's three velocity bounds.

Under `L=2`, once the initial pair is available, `1<=d<=3` and `0<=age<=2`. Hence a uniform finite bound is the maximum of the nine displayed expressions; the bound does **not** require a fixed-gain switched observer. With `T=0.1s, nu_bar=0.02m, a_bar=0.3m/s^2`, maximum is **0.475m/s** at `(d,age)=(1,2)`; at age 2 and d 1/2/3, bounds are 0.475, 0.290, 0.238333...m/s. This is an analytic worst-case outer bound, not an empirical noise estimate.

## What this does and does not prove

* **Proved conditionally:** a common causal point velocity estimate exists with uniformly bounded error for every infinite admissible no-delay success/miss word, provided two historical distinct measurements already exist and all frozen physical bounds hold. The estimator uses two timestamps; it is not the previous fixed-gain `L=[1,1/T]^T` observer that is unstable under repeated SMM.
* **Not proved:** a strict contraction/equalized recovery relative to a target phase set, a tight joint position-velocity CZ posterior, a delayed-measurement bound, a feasible observer-gain family, an invariant output-feedback Tube, or terminal recursive feasibility. A uniform finite bound alone is weaker than Equalized Recovery.
* **Initialization caveat:** before two successful readings, velocity may be unbounded without an independent initial velocity set. The measurement language must specify startup.
* **Delay caveat:** use acquisition timestamps and receipt times separately; a delayed old measurement may arrive out of order, so simply keeping the latest two *received* values does not guarantee increasing timestamps or age<=2. Reprocessing historical constraints is necessary.
* **Model caveat:** a generic `x+=Ax+Bu+Gw` does not automatically satisfy the continuous double-integrator bound. The physical residual must be mapped to a justified acceleration bound or the inequality re-derived for the discrete model.

## Reproducibility and bounded-word check

The following independently executed Python 3 / NumPy-free finite-word enumeration was run locally on 2026-11-03; it enumerated every length 1–12 success/miss word without `MMM`, initialized with successes at stamps -1 and 0. Length 3,6,9,12 counts: 7,44,274,1705. Maximum computed bound over all prefixes was 0.475m/s. These are finite enumeration cross-checks of the analytic bound, not infinite-word proof by simulation.

```python
import itertools
T,nu,acc=0.1,0.02,0.3
for n in range(1,13):
    worst=0
    for word in itertools.product('SM',repeat=n):
        if 'MMM' in ''.join(word): continue
        stamps=[-1,0]
        for k,s in enumerate(word,1):
            if s=='S': stamps.append(k)
            d=stamps[-1]-stamps[-2]; age=k-stamps[-1]
            worst=max(worst,2*nu/(d*T)+(d*T/2+age*T)*acc)
    assert worst <= 0.475+1e-12
print('all finite words checked')
```

## Literature relation and next gate

This is a self-contained elementary set-membership bound, **not attributed** to Scott (2016), Rego (2020), Hassaan (2021/22) or other papers without theorem-level reinspection. The existing literature ledger remains unchanged; no new paper was read this round. The next single priority is a **timestamp-aware joint position-velocity CZ set update and phase-wise recovery certificate**, with explicit startup and bounded delay, compared against the two-timestamp baseline and SMM counterexample. End-to-end theoretical closed loop remains pending.
