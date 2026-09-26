# 59 Exact Farkas obstruction for the orbit-5 immediate neighbor

Date: 2026-09-26. Parent: Chapters 57-58.

## Core question

Chapter 57 found seven numerically infeasible immediate symmetric neighbors. Chapter 58 showed how a floating-point dual support can be exactified. This run applies that procedure to orbit 5, the 162-vertex neighbor, before any distance-two search.

## Deterministic reconstruction

The orbit-5 restricted exposed facet is represented by the Chapter-55 symmetry pair ((89,29)), ((78,28)). Starting from its exact rational relative-interior witness, use the Chapter-56 rule (d=r_t) and
[
arepsilon=rac12min{mu_ell,
u_k}.
]
The resulting exact crossing has
[
arepsilon=rac{1424999829}{625000001924722}>0.
]
Every non-target restricted class remains strictly negative and every pair offset remains positive. Lifting to 38 paired offsets and re-enumerating gives the Chapter-57 orbit-5 incidence: 162 vertices, 38 active facets, and four active facets per vertex.

## Exact certificate

For this frozen neighboring incidence, rebuild the CC-RCI rows with rational arithmetic. A numerical dual feasibility solve was used only to discover a sparse support. The support contains 13 rows: 2 configuration rows, 10 endpoint-robust invariance rows, and 1 hard-state row. It contains **no torque-bound row**, no pair-offset equality row, and no offset-nonnegativity row.

The positive rational multipliers are
[
egin{aligned}
&(981000,981000,29430,15000000,5886000,10000000,10000000,5000000,78480,\
&qquad 40000000/3,470880,80000000/3,88290)/3069803,
end{aligned}
]
where the two entries written with /3 are equivalently (40000000/9209409) and (80000000/9209409).

Using Fraction/SymPy reconstruction of the selected primal rows gives exactly
[
yge0,qquad y^	op A=0,qquad y^	op b=-1.
]
Hence Farkas' lemma yields a contradiction (0le-1). Therefore:

[
oxed{	ext{the audited orbit-5 immediate neighboring CC-RCI cone is exactly infeasible even with unbounded vertex torque.}}
]

This is strictly stronger than Chapter 57's bounded-torque HiGHS observation. The obstruction is not caused by the (|	au|le0.08) actuator bound.

## Support metadata

The 13 selected rows are:

- config: ((v,j)=(15,5),(17,5));
- (T=4.905) invariance: ((2,7),(2,21),(3,5),(20,11),(34,11),(35,11),(56,6),(102,6));
- (T=14.715) invariance: ((56,24),(102,34));
- hard state: vertex 0, positive fourth-state bound.

The certificate is exact **conditional on the audited neighboring incidence**. Numerical H/V enumeration is still used to identify the 162 vertex active sets, exactly as Chapter 49 used numerical geometry to label its audited seed cone. Once those active sets are frozen, every selected row and the final Farkas identity are rational.

## What this changes

Orbit 5 was chosen because its 162 vertices differ from the seed cone's 160, so a seed certificate could not be transferred merely by vertex index. Nevertheless, an unbounded-torque obstruction survives in the changed combinatorics. This is evidence that the Chapter-49 obstruction is not merely an artifact of the original 160-vertex incidence.

It is **not yet** a theorem covering the other six valid immediate neighbors. Support transfer must be checked explicitly under their own active-set maps.

## Literature boundary

Gupta, Köroğlu and Falcone, *Computation of Robust Control Invariant Sets with Predefined Complexity for Uncertain Systems*, IJRNLC 31 (2021), 1674-1688, DOI 10.1002/rnc.5378, directly computes symmetric predefined-complexity RCI sets for rationally parameter-dependent systems with additive disturbances and assigns independent controls to extreme points, enabling a PWA controller. Their paper also notes that the initial polytope choice affects the result. The present Farkas certificate is a benchmark-specific exclusion result, not a new predefined-complexity synthesis method.

The configuration-constrained RCI literature remains the baseline for fixed-orientation/variable-offset synthesis. The intended contribution still has to come from the certified SMF/CZ uncertainty interface to recursive-feasible Tube MPC and a strict conservatism comparison, not from configuration search itself.

## Evidence status

**Proved for the audited orbit-5 incidence:** exact infeasibility under the endpoint disturbance contract and hard-state constraints, even when vertex torque is unbounded.

**Numerical/combinatorial only:** the global H/V enumeration that identifies the 162-vertex neighboring incidence.

**Still numerical only:** infeasibility of the other six valid immediate neighbors from Chapter 57.

## Next single priority

Test whether the 13-row orbit-5 support pattern, after mapping through each neighbor's active sets and symmetry, exactifies for orbits 0,1,3,4,6,7. If a common rational circuit exists, formulate a layer-wide obstruction theorem. If not, exactify the six neighbors separately before any distance-two configuration search.
