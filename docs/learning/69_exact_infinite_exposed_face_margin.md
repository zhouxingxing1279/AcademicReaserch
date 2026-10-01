# Run 106 — exact H15 infinite-mRPI exposed-face separation

## Core question

Run 104 observed numerically that all 160 signed Run-100 H15 directions have a finite-zonotope q-exposed vertex outside the horizontal position measurement strip |p_x|<=0.02. Run 105 proved the omitted Run-93 infinite tail is tiny, but deliberately left the finite exposed-face margin uncertified. This run closes that proof gap with exact rational arithmetic and, more strongly, avoids relying on the 1390-term numerical classification.

## Exact certificate

Freeze the Run-93 horizontal/reference closed loop, disturbance radius D0=3403343/1600000, Run-90 vertical input certificate used by the Run-99 q+/q- seeds, and the Run-100 five-seed H15 library.

For the mRPI
[
S=\bigoplus_{i=0}^{\infty} g_i[-1,1],\qquad g_i=D_0F^iG,
]
fix q. For the first N=600 generators, every nonzero q^T g_i fixes the maximizing sign of the q-exposed face; if q^T g_i=0, that generator remains free. Let c_q be the resulting exact p_x contribution and f_q the exact sum of absolute p_x contributions of those free generators.

For all generators after N, do not assume any maximizing sign. Using the Run-93 M=139 block contraction alpha=||F^M||_inf<1 gives the direction-independent reliable tail radius
[
r_p(N)\le {D_0\over1-\alpha}\sum_{j=0}^{M-1}|e_p^TF^{N+j}G|.
]
Hence every point x of the infinite q-exposed face satisfies
[
|e_p^Tx|\ge |c_q|-f_q-r_p(N).
]
All arithmetic used for the comparison is Python Fraction; decimals are display only.

For every one of the 80 unsigned H15 directions (therefore all 160 signed facets), the verifier proves
[
|c_q|-f_q-r_p(600)>139/500=0.278.
]
The minimum occurs in the depth-15 q+ / q- seed pair. Consequently every point of every infinite-mRPI H15 exposed face obeys
[
|p_x|>0.278,
]
and therefore its distance from the measurement strip |p_x|<=0.02 is strictly larger than
[
0.278-0.02=0.258.
]

Thus
[
F_S(q)\cap\{|p_x|\le0.02\}=\varnothing,\qquad \forall q\in H_{15}.
]
By the Run-104 exposed-face theorem,
[
h_{S\cap M}(q)<h_S(q),\qquad \forall q\in H_{15},
]
provided S intersect M is nonempty.

This upgrades the previous 160/160 numerical observation to a proof-quality statement for the frozen infinite Run-93 mRPI.

## Interpretation

The result is negative for a simple eager-template pruning strategy: under this frozen set and measurement contract there is no H15 facet that can be certified unchanged merely because a position measurement is 'unrelated' to its direction vector. Correlation makes every controller-predecessor exposed face incompatible with the fresh position strip.

It does not prove that every practical measurement packet yields the same numerical improvement, nor that eager 160-support materialization is slower than a CZ update. It only removes the structural shortcut 'skip directions whose support cannot tighten'.

## Literature boundary

Scott, Raimondo, Marseglia and Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection*, Automatica 69 (2016), DOI 10.1016/j.automatica.2016.02.036, already establishes constrained-zonotope set operations and conservative complexity reduction. Rego, Raffo, Scott and Raimondo, *Guaranteed nonlinear set-valued state estimation using constrained zonotopes*, Automatica 111 (2020), DOI 10.1016/j.automatica.2019.108614, already uses guaranteed prediction enclosures and bounded-error measurement intersections. Therefore neither measurement intersection nor CZ retention is an innovation claim.

The project-specific question remains whether retaining one joint measurement-updated object can preserve controller-relevant dependency at lower online cost than eagerly materializing all certified predecessor supports while respecting the shifted-cap recursive-feasibility contract.

## Reproduction

Run:

```bash
python verification/check_infinite_exposed_face_margin.py
```

The script recomputes Run-90 Uz, the five Run-100 seeds, H15, the first 600 generators, and the M=139 infinite tail. It asserts the strict rational threshold 0.278 for every unsigned direction.

## Status ledger

- **Proved:** all 160 signed H15 exposed faces of the frozen infinite Run-93 mRPI are disjoint from |p_x|<=0.02 by more than 0.258.
- **Proved previously and now closed:** therefore a nonempty fresh position-strip intersection strictly reduces every H15 directional support.
- **Rejected shortcut:** no H15 direction can be skipped on the structural claim that this position measurement cannot tighten it.
- **Not proved:** eager-H15 runtime relative to CZ/joint-object update.
- **Not proved:** full nonlinear six-state recursive feasibility.

## Next unique priority

Now perform the equal-information implementation comparison that Runs 103-106 were preparing: on the same machine and identical measurement/dropout record, compare (1) eager materialization of all 160 H15 supports at each fresh position packet with (2) one measurement-updated CZ/joint object followed by only the controller queries actually consumed before the next packet. Record wall time, fresh optimization count, v_x/psi/mu certified bounds, and preservation of the Run-99 strict witness. Do not reduce H15 or change K to make either method win.
