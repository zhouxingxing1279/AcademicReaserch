# Run 2026-09-25 — constant-residual equilibrium gate

- Base: main @ 1c49659c762dcb96dadeb8fe7a6216570951b774.
- Core question: can the chapter-35 joint ancillary search be pruned by an analytic necessary condition before RPI synthesis?
- Result: yes. For constant admissible residual, equilibrium implies v*=omega*=0, phi*=r/T and p*=-(Kphi/Kp)r/T. At T=4.905, vertex-consistent d_x gives |Kphi/Kp| <= 12.54800034 as a necessary position-feasibility gate.
- Counterexample/audit: chapter-35 best sample has ratio 18.57635 and exact implied |p*|=7.40211643>5, explaining its long-horizon p failure.
- Evidence: algebraic necessary condition; exact rational checker in verification/check_constant_residual_equilibrium_gate.py.
- Literature: Kothare, Balakrishnan, Morari, Automatica 1996, DOI 10.1016/0005-1098(96)00063-5; Tahir & Jaimoukha, IFAC 2012, DOI 10.3182/20120823-5-NL-3013.00032. Both cover constrained robust/controller-invariant synthesis; the gate is not claimed as a generic synthesis innovation.
- Limitation: necessary only; it does not certify common LPV stability, transients, torque feasibility, or RPI sufficiency.
- Next unique priority: certificate-based joint synthesis with this equilibrium ratio gate enforced, followed by finite-reachable falsification and safe-tail/RPI certification.
