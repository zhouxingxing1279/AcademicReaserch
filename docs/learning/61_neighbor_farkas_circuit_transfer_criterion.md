# Chapter 61 — Exact transfer criterion for neighboring-cone Farkas circuits

For a neighboring configuration, after central-symmetry elimination write the feasibility system as
[
A^{(r)}z^{(r)}le b^{(r)}.
]
Orbit 5 has a repository-reproducible rational certificate on support (S_5):
[
y_5^TA^{(5)}_{S_5}=0,qquad y_5^Tb^{(5)}_{S_5}=-1,qquad y_5>0.
]

## Exact transfer proposition

Let (r) be another audited neighbor. Assume there are a row bijection (pi:S_5	o S_r), one column permutation matrix (P), and positive rational row scalings (lambda_i) such that
[
a^{(r)}_{pi(i)}=lambda_i a^{(5)}_iP,qquad
b^{(r)}_{pi(i)}=lambda_i b^{(5)}_i.
]
Then (	ilde y_{pi(i)}=y_{5,i}/lambda_i) is an exact certificate:
[
	ilde y^TA^{(r)}_{S_r}=0,qquad
	ilde y^Tb^{(r)}_{S_r}=-1.
]
The proof is direct substitution. Therefore exact row/column isomorphism is sufficient to transfer the orbit-5 obstruction.

## Required audit

Semantic labels are insufficient because changing active sets changes the exact vertex-affine maps. For each target orbit 0,1,3,4,6,7 the code must reconstruct exact active-set inverses, exact selected primal rows, pair-offset elimination, a globally consistent column permutation, positive row scalings, and finally recompute the two weighted identities.

Failure to find such an isomorphism does not establish primal feasibility; it only means the orbit-5 circuit cannot be transferred by that mapping. A new dual support must then be discovered and exactified independently.

## Evidence status

Proved: the transfer proposition, conditional on the exact rational identities above.

Repository-certified already: orbit 5 through `verification/check_orbit5_neighbor_farkas_exact.py`.

Open: whether any of orbits 0,1,3,4,6,7 satisfies the transfer hypotheses.

## Next unique priority

Implement the exact isomorphism audit for orbits 0,1,3,4,6,7. At the first failed transfer, discover and exactify a target-specific support rather than entering distance-two configuration search.
