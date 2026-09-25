# Run 62 PWA ancillary interface

Base revision: 1c49659c762dcb96dadeb8fe7a6216570951b774.

Question: is a static linear ancillary gain actually required before a polytopic RCI certificate can be used by Tube MPC?

Conclusion: no. Robustly admissible controls assigned to polytope vertices induce a PWA ancillary controller by barycentric interpolation. Convexity proves invariance transfer and input admissibility. Input tightening can be represented by the finite control-support ledger max_i c_u^T u_i rather than by K-transformed state directions.

Exact check: verification/check_pwa_ancillary_interface.py uses rational arithmetic and a vertex-control assignment that is not globally affine.

Literature boundary: predefined-complexity RCI with extreme-point controls and PWA realization already exists in Gupta, Koroglu and Falcone (2021), DOI 10.1002/rnc.5378; PWA tube-MPC laws also pre-exist. This is baseline closure, not an innovation claim.

Limitation: no feasible RCI for the frozen quadrotor benchmark is obtained here; terminal decrease is still open.

Next priority: synthesize one correlated shape/offset plus free-vertex-control RCI certificate for the frozen lateral benchmark and export its state/control support ledgers.
