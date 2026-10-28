# Scheduling-visible 19-pair Farkas audit design

## Scope

Audit the existing 19-pair four-state configuration cone under the corrected information pattern:
current thrust is known before torque is chosen. Preserve the old parameter-independent offsets and
geometry, but assign independent low/high-thrust torque variables to every state vertex.

## Construction

- Reuse the audited 19-pair normals and 160 simple vertices from
  `check_19pair_cc_seed_cone.py`.
- Use 38 nonnegative offsets and 320 endpoint-specific torque variables, for 358 decisions.
- Check configuration containment, endpoint-wise one-step invariance, state hard bounds and endpoint
  torque bounds. Also solve the same LP without torque bounds to distinguish actuator shortage from
  geometric/configuration obstruction.
- Assert that the hard-coded reduced contract matches `configs/planar_baseline.json` before solving.
- Reconstruct a sparse rational Farkas circuit directly from normals, active sets and `Fraction`
  arithmetic. Do not depend on SymPy. The exact acceptance conditions are: 24 selected rows,
  coefficient rank 23, every multiplier positive, all 358 weighted coefficients exactly zero, and
  weighted right-hand side `-3069803/88290`.

Endpoint checks are sufficient for the present affine-in-thrust dynamics and affine interpolation of
the two endpoint torques. This audit does not introduce parameter-dependent offsets and does not cover
future-thrust preview, the six-state nonlinear model, output feedback, terminal conditions or recursive
feasibility.

## Outputs and evidence

`verification/check_scheduling_visible_19pair_farkas.py` emits a JSON record containing contract and
source hashes, full-LP dimensions/status, exact circuit checks, multiplier list and scope exclusions.
The exact certificate is `COUNTEREXAMPLE`; the full LP solver status is only `NUMERIC_CHECK`.
Tests pin the dimensions, both numerical infeasibility results, exact zero residual, exact negative
right-hand side, absence of torque-bound rows and archived artifact reproducibility.

## Failure interpretation

Failure of this candidate means only that the fixed 19-pair parameter-independent configuration cone
cannot be made RCI by scheduling-visible vertex torques. It must not be reported as physical
infeasibility, failure of all fixed-normal sets, or failure of the six-state project.

