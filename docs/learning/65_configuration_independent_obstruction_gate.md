# Chapter 65 — Existing first-layer certificates do not yet imply a configuration-independent obstruction

## Core question

The audited immediate-neighbor layer is closed, but can its exact Farkas certificates already be promoted to an obstruction that is independent of the local configuration cone?

## Certificate-support audit

A configuration-independent Farkas obstruction must be supported only on inequalities that remain valid when the local configuration-cone inequalities are removed. If a stored certificate uses a configuration row with a positive multiplier, that particular certificate proves infeasibility only for the constrained local cone.

The current exact-certificate ledger gives:

| orbit | support size | configuration rows in the stored support |
|---|---:|---:|
| 0 | 14 | 1 |
| 1 | 13 | 2 |
| 3 | 9 | 0 |
| 4 | 13 | 2 |
| 5 | 13 | 2 |
| 6 | 28 | 0 |
| 7 | 13 | 2 |

Orbits 1, 4, and 7 inherit the orbit-5 support-local circuit, hence the same two configuration rows.

Therefore the existing certificates do **not** establish a configuration-independent obstruction for the 19-pair orientation family. This is a logical insufficiency result, not a feasibility result: an alternative certificate without configuration rows may still exist for orbits 0/1/4/5/7.

## Why this matters

It would be invalid to infer a family-wide impossibility theorem merely because all audited immediate neighbors are infeasible. Five of the seven stored certificates explicitly use inequalities defining their local configuration cones. Removing those inequalities enlarges the primal feasible set, and the current positive Farkas combinations no longer certify that enlarged system.

The correct next discriminator is therefore not distance-two enumeration. For a representative configuration-dependent case, first orbit 0 and then orbit 5, solve the relaxed CC-RCI problem after deleting all configuration inequalities while keeping the same frozen incidence, endpoint disturbance contract, hard-state constraints, and pair-offset parameterization.

If the relaxed problem is feasible, that feasible point is a counterexample to the claim that the currently frozen vertex-map subsystem alone is impossible. If it remains infeasible, extract and rationally exactify a dual support that contains no configuration rows.

## Literature boundary

Gupta, Köroğlu, and Falcone (2021), DOI 10.1002/rnc.5378, already compute predefined-complexity symmetric RCI sets for rationally parameter-dependent uncertain systems with additive disturbances and do not impose a fixed feedback form; controls are assigned at extreme points and can induce a PWA controller. Their paper also notes dependence on the initial polytope choice. The present result is therefore a proof-status audit for our fixed-orientation benchmark, not a new RCI synthesis principle.

## Evidence status and next unique priority

Proved here: the *existing stored certificates* are insufficient to establish a configuration-independent obstruction, because orbits 0, 1, 4, 5, and 7 use positive multipliers on configuration inequalities.

Not proved: existence or nonexistence of an alternative configuration-free certificate.

Next unique priority: run the orbit-0 relaxed problem with all configuration inequalities removed. Do not enter distance-two search until this discriminator is resolved.
