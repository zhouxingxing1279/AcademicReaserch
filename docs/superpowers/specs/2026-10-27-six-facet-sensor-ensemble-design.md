# Six-Facet Sensor-Ensemble Gate Design

## Intent

Close the continuous-measurement-center gap left by Run186 at the smallest exact interface. Show
whether all position-measurement centers are represented by one linear meta coordinate for the
six-facet configuration, before selecting the remaining `Z/H/Omega` template or building another
large graph LP.

## Goals

- derive the measurement-compatible center interval for a general configured six-facet `P(y)`;
- prove exact equivalence between existence of a position measurement center and
  `Z_1 y <= a`, with `Z_1=(e_0+e_3)/2`;
- verify that `+p/-p` offsets are exact supports throughout the selected configuration cone;
- bind the claim, checker, tests, adapter, Run186 geometry checker, and design in a replayable
  exact artifact;
- preserve explicit negative flags for full meta-template, graph invariance, constraints, terminal
  ingredients, and recursive feasibility.

## Non-goals

- no arbitrary choice of the remaining `Z_2`, `H`, or `Omega`;
- no 15-mode/17-edge LP and no controller implementation;
- no enumeration of future measurement centers;
- no novelty claim for Houska's sensor-ensemble construction or CCTMPC support coordinates.

## Approaches considered

1. **Directly replace Run184 boxes in the full graph LP.** Rejected because `Z_2/H/Omega` is not yet
   justified; solver feasibility would describe an arbitrary discretization budget.
2. **Enumerate finitely many measurement centers.** Rejected because it cannot certify the continuous
   output domain and duplicates the problem that the information-ensemble construction already solves.
3. **Exact sensor-ensemble row first (selected).** Use the Run186 configuration triple to prove the
   width criterion algebraically, then leave only the remaining meta-template choice as the next blocker.

## Exact contract

For a nonempty six-facet polytope in the Run186 configuration cone,

```math
I(y,a)=[y_0-a,\,-y_3+a]
```

is precisely the set of measurement centers whose error strip contains the whole polytope. Hence

```math
I(y,a)\ne\varnothing
\iff (y_0+y_3)/2\le a
\iff Z_1y\le a.
```

The proof uses exact vertex maps to establish `max p=y_0` and `min p=-y_3`. Tests independently
enumerate configured rational offsets and must reject a width/diameter scaling error.

## Evidence boundary

Success yields evidence level `exact_six_facet_sensor_ensemble_measurement_row`. It removes continuous
measurement-center enumeration as a blocker, but does not certify a complete polytopic information
ensemble or any control theorem.
