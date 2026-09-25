# 57 Symmetric neighboring-configuration audit

Date: 2026-09-26. Parent: Chapter 56.

## Result

For each of the eight center-symmetric exposed boundary orbits, use the Chapter-56 exact crossing rule with d=r_t and epsilon equal to one half of the smallest exact row/positivity margin. The selected restricted class becomes positive, every other old-cone class stays strictly negative, and all pair offsets stay positive.

After lifting to 38 paired offsets and globally re-enumerating H/V incidence, the audit is:

| orbit | vertices | active facets | simple |
|---|---:|---:|---|
| 0 | 160 | 38 | yes |
| 1 | 160 | 38 | yes |
| 2 | 152 | 36 | yes |
| 3 | 160 | 38 | yes |
| 4 | 160 | 38 | yes |
| 5 | 162 | 38 | yes |
| 6 | 160 | 38 | yes |
| 7 | 160 | 38 | yes |

Thus seven crossings are bounded, 38-active and entirely simple candidate neighbors. Orbit 2 loses two active facets and is rejected as a 38-facet CC candidate. Orbit 5 changes the vertex count from 160 to 162 while retaining the required geometry.

Rebuilding the endpoint-exact CC-RCI LP for orbits 0,1,3,4,5,6,7 gives HiGHS infeasible for all seven under the frozen disturbance, hard-state and |tau|<=0.08 contract.

## Evidence level

The one-class crossing and rational step construction are exact consequences of Chapters 55-56. Global H/V enumeration and the seven LP infeasibility results are numerical NumPy/HiGHS audits, not exact Farkas certificates. Therefore this excludes no neighboring cone exactly yet, and says nothing about more distant configurations or other orientation families.

## Literature boundary

Mejari, Mulagaleti and Bemporad, IEEE Control Systems Letters 7 (2023), DOI 10.1109/LCSYS.2023.3346128, already provides fixed-orientation/variable-offset CC-RCI synthesis with vertex controls. Badalamenti et al., arXiv:2505.14440 (2025), studies CCTMPC template refinement and complexity/conservatism trade-offs. Neighbor-template search is baseline machinery, not the intended SMF/MPC innovation.

## Next single priority

Extract and rationalize a dual/Farkas certificate for one representative infeasible neighbor, preferably orbit 5 because it changes the vertex count while remaining 38-active and simple. Then test whether the exact obstruction transfers to the other six neighbors before attempting distance-two crossings.
