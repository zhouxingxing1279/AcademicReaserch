import importlib
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def _matmul(left, right):
    return [[
        sum(left[row][inner] * right[inner][column] for inner in range(len(right)))
        for column in range(len(right[0]))
    ] for row in range(len(left))]


def _subject():
    try:
        return importlib.import_module("check_single_slant_shape_gate")
    except ModuleNotFoundError:
        return None


class SingleSlantShapeGateTests(unittest.TestCase):
    def test_transformed_dynamics_keep_the_required_minus_sign_and_noise(self):
        """Changing q=p-kappa*v to the opposite slant must change this recurrence."""
        subject = _subject()
        build = getattr(subject, "shape_recurrence", None)
        self.assertTrue(callable(build))
        recurrence = build()
        adapter = importlib.import_module("check_houska_vertical_adapter").run()
        kappa = F(1, 10)
        transform = [[F(1), F(0)], [F(1), -kappa]]
        inverse = [[F(1), F(0)], [F(1) / kappa, -F(1) / kappa]]
        independently_derived_state = _matmul(_matmul(transform, adapter["A"]), inverse)
        independently_derived_input = _matmul(transform, adapter["B"])
        self.assertEqual(recurrence["kappa"], F(1, 10))
        self.assertEqual(recurrence["signed_state_matrix"], independently_derived_state)
        self.assertEqual(recurrence["signed_input_matrix"], independently_derived_input)
        self.assertEqual(recurrence["signed_state_matrix"], [[F(6, 5), F(-1, 5)],
                                                              [F(1, 5), F(4, 5)]])
        self.assertEqual(recurrence["signed_input_matrix"], [[F(0)], [F(-1, 500)]])
        self.assertEqual(recurrence["radius_matrix"], [[F(6, 5), F(1, 5)],
                                                        [F(1, 5), F(4, 5)]])
        self.assertEqual(recurrence["radius_matrix"], [
            [abs(value) for value in row] for row in independently_derived_state
        ])
        self.assertEqual(recurrence["radius_disturbance"],
                         [F(0), F(572143, 80000000)])

    def test_fifteen_step_q_gain_proves_no_nonnegative_return_radius(self):
        """A q-to-q gain above one rules out the unchanged-q success return."""
        subject = _subject()
        obstruction = subject.return_obstruction()
        self.assertEqual(obstruction["fifteen_step_radius_matrix_q_q"],
                         F(187604137722, 30517578125))
        self.assertGreater(obstruction["fifteen_step_radius_matrix_q_q"], F(1))
        self.assertEqual(obstruction["coefficient_excess"],
                         F(157086559597, 30517578125))
        self.assertTrue(obstruction["no_nonnegative_return_radius"])

    def test_all_success_gaps_are_checked_and_long_returns_fail(self):
        """Checking only the five-step return would miss the legal 10/15-step obstruction."""
        subject = _subject()
        result = subject.run()
        success = result["success_return_checks"]
        self.assertEqual([edge["prediction_age"] for edge in success], [5, 10, 15])
        self.assertEqual([edge["q_q_gain"] for edge in success], [
            F(2096, 3125), F(17562857, 9765625),
            F(187604137722, 30517578125),
        ])
        self.assertEqual([edge["nonnegative_fixed_radius_possible"] for edge in success],
                         [True, False, False])
        self.assertFalse(result["periodic_shape_cycle_certified"])

    def test_rejected_candidate_fails_first_miss_and_velocity_capacity(self):
        """The old candidate must expose its first-edge underbound and later capacity failure."""
        subject = _subject()
        result = subject.run()
        rejected = result["rejected_run185_candidate"]
        self.assertEqual(rejected["first_miss_position_underbound"], F(1, 125))
        self.assertEqual(rejected["first_failed_success_age"], 5)
        self.assertGreater(rejected["derived_velocity_radius_at_age_5"], F(11, 4))
        self.assertFalse(rejected["all_shape_radius_capacity_checks_pass"])

    def test_evidence_flags_do_not_upgrade_a_shape_gate_to_a_controller(self):
        """A feasible radius schedule is not a center, input, or terminal certificate."""
        subject = _subject()
        result = subject.run()
        self.assertEqual(result["evidence_level"],
                         "exact_fixed_slant_parallelogram_shape_obstruction")
        self.assertFalse(result["full_information_ensemble_certified"])
        self.assertFalse(result["center_dynamics_certified"])
        self.assertFalse(result["input_feasibility_certified"])
        self.assertFalse(result["mpc_recursive_feasibility_certified"])

    def test_cli_artifact_is_hash_bound_and_reproducible(self):
        """A stale archive must not survive a checker, test, config, or design edit."""
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "verification/check_single_slant_shape_gate.py"),
                 "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads((
                ROOT / "results/theory_single_slant_shape_gate_20261026/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(digest, hashlib.sha256((ROOT / name).read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
