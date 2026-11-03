# Run 44 — S2 configuration-constrained RCI Farkas obstruction

- Repository start: `4224482bd92dc5448d962d64cb083be7e4f7cb2a`.
- Core question: with the 28 S2 normals fixed, can 14 independent symmetric offsets plus vertex torques produce an endpoint-exact RCI while preserving the audited S2 vertex incidence?
- Literature checked: Mejari–Mulagaleti–Bemporad (2024, arXiv:2309.06998) for configuration-constrained fixed-orientation/variable-offset RCI LP; Gupta–Köroğlu–Falcone (2021, DOI 10.1002/rnc.5378) for predefined-complexity uncertain-system RCI and unrestricted extreme-point controls.
- Proven result: no. Four exact endpoint-robust vertex inequalities plus the torque lower bound form a Farkas infeasibility certificate. Multipliers are `[5/11, 6/11, 2943/550000, 1]`; after adding the torque-bound row, all variables cancel and yield `0 <= -370024843/4400000000`.
- Interpretation: unlike Run 43, actuator authority is explicitly part of this obstruction. However, the proof excludes only the configuration cone preserving S2 incidence, not every polytope with the same normals.
- Verification: `verification/check_s2_configuration_farkas.py`; archived exact output in `results/s2_configuration_farkas_20260924/checks.json`.
- Failed/avoided approach: do not report a floating HiGHS `infeasible` status as the proof. The exact reduced Farkas certificate is the auditable result.
- Remaining proof gap: whether another S2-normal combinatorial configuration is feasible; whether selected S3 normals can remove the offending vertex chains.
- Next unique priority: select the minimal S3 normals that cut the Farkas-certificate offending vertices/chains, then solve and certify the expanded configuration LP before considering the full S3/S4 template.
