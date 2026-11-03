import importlib
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))


def _subject():
    return importlib.import_module("check_vertical_future_residual_decomposition")


class VerticalFutureResidualDecompositionTest(unittest.TestCase):
    def test_current_contract_has_only_aerodynamic_and_attitude_thrust_terms(self):
        result = _subject().future_residual_decomposition_certificate()
        source = result["current_contract"]
        self.assertEqual(source["truth_semantics"], "defined_discrete_euler")
        self.assertEqual(source["external_process_halfwidth_z"], F(0))
        self.assertEqual(source["aerodynamic_core"], F(1043, 500))
        self.assertEqual(source["attitude_thrust_term_at_tmax"], F(238383, 160000))
        self.assertEqual(source["total_halfwidth"], F(572143, 160000))

    def test_run166_scale_implies_exact_absolute_target(self):
        result = _subject().future_residual_decomposition_certificate()
        target = result["run166_target"]
        self.assertEqual(target["scale_max"], F(16254878, 42598647))
        self.assertEqual(target["absolute_halfwidth_max"], F(89401829, 65520000))

    def test_eliminating_entire_attitude_term_is_still_insufficient(self):
        result = _subject().future_residual_decomposition_certificate()
        obstruction = result["attitude_only_obstruction"]
        self.assertEqual(obstruction["best_halfwidth"], F(1043, 500))
        self.assertEqual(obstruction["strict_excess"], F(47272891, 65520000))
        self.assertEqual(obstruction["best_scale"], F(333760, 572143))
        self.assertGreater(obstruction["best_scale"], F(16254878, 42598647))

    def test_aerodynamic_core_requires_a_future_tube_certificate(self):
        result = _subject().future_residual_decomposition_certificate()
        necessary = result["necessary_aerodynamic_contract"]
        self.assertEqual(necessary["core_scale_max_if_attitude_zero"], F(89401829, 136674720))
        self.assertEqual(necessary["core_reduction_min"], F(47272891, 136674720))
        self.assertEqual(necessary["quantifier"], "all_15_future_ticks_and_all_information_consistent_trajectories")

    def test_claim_is_deliberately_limited(self):
        result = _subject().run()
        self.assertTrue(result["attitude_only_route_impossible"])
        self.assertFalse(result["local_aerodynamic_route_ruled_out"])
        self.assertFalse(result["is_recursive_feasibility_proof"])
        self.assertFalse(result["is_full_six_state_guarantee"])


if __name__ == "__main__":
    unittest.main()
