# 55 Constant-residual equilibrium gate

For the chapter-35 lateral model under fixed thrust T and an admissible constant residual r, any stable static-feedback closed loop has equilibrium
[
v_*=0,quad omega_*=0,quad phi_*=r/T,quad
p_*=-(K_phi/K_p)r/T.
]
Hence any origin-containing robust invariant set satisfying (|p|le5) must obey
[
|K_phi/K_p|,d_x(T)/Tle5.
]
With the vertex-consistent contract (d_x(T)=1.880+T(0.45)^3/6), at (T=4.905),
[
d_x/T=6254383/15696000,qquad
|K_phi/K_p|le78480000/6254383approx12.54800034.
]
The chapter-35 best sampled gain has (|K_phi/K_p|approx18.57635), so its admissible constant-residual equilibrium has (|p_*|approx7.40211643>5). Thus its long-horizon position failure is structural, not a finite-sum artifact.

This is a necessary gate only; it does not certify common LPV stability, transient torque/state constraints, or RPI sufficiency. Next: enforce this gate in certificate-based joint controller/invariant synthesis.
