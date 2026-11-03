"""Regression tests for the Run-126 Scott-CZ baseline."""

from __future__ import annotations

import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

import numpy as np
from scipy.optimize import linprog


class TestRun126ScottCZBaseline(unittest.TestCase):
    def _module(self):
        try:
            from verification import check_run126_scott_cz_baseline
        except ImportError as exc:  # makes the pre-implementation RED explicit
            self.fail(f"Run-126 baseline module is missing: {exc}")
        return check_run126_scott_cz_baseline

    def test_strip_to_cz_preserves_run123_support(self) -> None:
        """Catches a wrong noise sign/radius in the strip-to-equality lift."""
        module = self._module()
        source, lifted = module.build_run123_posterior_cz()
        directions = module.controller_directions()

        for direction in directions:
            self.assertAlmostEqual(
                source.support(direction), lifted.support(direction), places=8
            )

    def test_precomputed_scaled_constraints_preserve_support(self) -> None:
        """Catches a timing shortcut that changes the reference polytope."""
        module = self._module()
        source, _ = module.build_run123_posterior_cz()
        scaled = module._scaled_source_constraints(source)
        for direction in module.controller_directions():
            self.assertAlmostEqual(
                module._scaled_source_support(source, direction),
                module._scaled_source_support(source, direction, scaled),
                places=12,
            )

    def test_scott_reduction_outer_contains_small_zonotope(self) -> None:
        """Catches an inward or incorrectly updated generator reduction."""
        module = self._module()
        generators = np.array(
            [
                [1.0, 0.0, 0.7, -0.2],
                [0.0, 1.0, 0.4, 0.8],
            ]
        )
        reduced = module.scott_reduce_zonotope(generators, target_generators=2)

        self.assertEqual(reduced.shape, (2, 2))
        for signs in itertools.product((-1.0, 1.0), repeat=generators.shape[1]):
            point = generators @ np.asarray(signs)
            membership = linprog(
                np.zeros(reduced.shape[1]),
                A_eq=reduced,
                b_eq=point,
                bounds=[(-1.0, 1.0)] * reduced.shape[1],
                method="highs",
            )
            self.assertTrue(membership.success, msg=f"missed corner {point}")

    def test_scott_basis_has_unit_bounded_coordinates(self) -> None:
        """Catches a pivot basis that violates Scott's |T^-1 V| <= 1 premise."""
        module = self._module()
        _, lifted = module.build_run123_posterior_cz()
        lifted_generators = np.vstack(
            [lifted.generators, lifted.constraints]
        )
        self.assertTrue(
            hasattr(module, "scott_basis_coordinates"),
            msg="Scott-compatible basis selection is missing",
        )
        _, coordinates = module.scott_basis_coordinates(lifted_generators)
        self.assertLessEqual(float(np.max(np.abs(coordinates))), 1.0 + 1e-12)

    def test_square_zonotope_needs_no_reduction(self) -> None:
        """Catches an empty-residual argmax for an already minimal zonotope."""
        module = self._module()
        generators = np.array([[2.0, 0.0], [0.0, 3.0]])
        reduced = module.scott_reduce_zonotope(generators, target_generators=2)
        self.assertEqual(reduced.shape, (2, 2))
        self.assertEqual(float(np.sum(np.abs(reduced[0]))), 2.0)
        self.assertEqual(float(np.sum(np.abs(reduced[1]))), 3.0)

    def test_full_baseline_is_fixed_complexity_and_outer(self) -> None:
        """Catches a wrong lift/recovery or an unsafe seven-generator result."""
        module = self._module()
        self.assertTrue(
            hasattr(module, "verify_scott_cz_baseline"),
            msg="full Run-126 comparison has not been implemented",
        )
        report = module.verify_scott_cz_baseline(repetitions=1)

        self.assertEqual(report["representation"]["source_latents"], 602)
        self.assertEqual(report["representation"]["lifted_generators"], 605)
        self.assertEqual(report["representation"]["reduced_generators"], 7)
        self.assertEqual(report["representation"]["equality_constraints"], 3)
        self.assertEqual(report["support_comparison"]["direction_count"], 300)
        self.assertLessEqual(
            report["support_comparison"]["max_underestimate"], 1e-8
        )
        threshold = report.get("admission_threshold")
        self.assertIsNotNone(
            threshold, msg="minimum admissible Scott complexity is unreported"
        )
        self.assertEqual(threshold["minimum_admissible_generators"], 539)
        self.assertEqual(threshold["predecessor_generators"], 538)
        self.assertEqual(threshold["admissible_violation_count_at_1e-8"], 0)
        self.assertGreater(
            threshold["predecessor_violation_count_at_1e-8"], 0
        )
        self.assertTrue(threshold["predecessor_within_one_solver_tolerance"])
        self.assertTrue(
            report["timing_seconds"][
                "reference_constraint_precomputation_excluded"
            ]
        )

    def test_exact_candidate_slack_subtracts_nominal_once(self) -> None:
        """Catches accidental double subtraction of the nominal state."""
        module = self._module()
        _, lifted = module.build_run123_posterior_cz()
        shifted_source, powers, inputs, states = module._shifted_candidate()
        exact_slacks, _ = module._constraint_slacks(
            shifted_source, lifted, powers, inputs, states
        )
        stage, state_index = np.unravel_index(
            np.argmax(np.abs(states[: module.HORIZON])),
            states[: module.HORIZON].shape,
        )
        self.assertGreater(abs(states[stage, state_index]), 1e-6)
        direction = np.eye(4)[state_index]
        expected = (
            module.STATE_LIMITS[state_index]
            - direction @ states[stage]
            - module._scaled_source_support(
                shifted_source, powers[stage].T @ direction
            )
            - module._disturbance_support(direction, stage, powers)
        )
        record_index = stage * 10 + state_index * 2
        self.assertAlmostEqual(
            exact_slacks[record_index], expected, places=12
        )

    def test_direct_script_entrypoint_emits_json(self) -> None:
        """Catches a script that imports only when launched with ``-m``."""
        root = Path(__file__).resolve().parents[1]
        environment = os.environ.copy()
        environment["ACADEMIC_RESEARCH_NO_WRITE"] = "1"
        environment["RUN126_REPETITIONS"] = "1"
        completed = subprocess.run(
            [sys.executable, str(root / "verification/check_run126_scott_cz_baseline.py")],
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, msg=completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["support_comparison"]["direction_count"], 300)


if __name__ == "__main__":
    unittest.main()
