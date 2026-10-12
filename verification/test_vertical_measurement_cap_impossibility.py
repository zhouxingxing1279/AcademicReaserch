import importlib
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))


def _subject():
    return importlib.import_module("check_vertical_measurement_cap_impossibility")


class VerticalMeasurementCapImpossibilityTest(unittest.TestCase):
    def test_forced_return_visible_coordinate_is_exact_minkowski_sum(self):
        result = _subject().measurement_cap_certificate()
        support = result["forced_return_support"]
        self.assertEqual(support["identity"], "d_p_plus=q+n_p")
        self.assertEqual(support["mode14_q_halfwidth"], F(23312147, 48000000))
        self.assertEqual(support["measurement_noise_halfwidth"], F(1, 50))
        self.assertEqual(support["visible_halfwidth"], F(24272147, 48000000))

    def test_zero_noise_witness_already_breaks_required_global_cap(self):
        result = _subject().measurement_cap_certificate()
        witness = result["noiseless_counterexample"]
        self.assertEqual(witness["q"], F(23312147, 48000000))
        self.assertEqual(witness["n_p"], F(0))
        self.assertEqual(witness["d_p_plus"], F(23312147, 48000000))
        self.assertEqual(witness["required_cap"], F(58684997, 145000000))
        self.assertEqual(witness["strict_excess"], F(563381459, 6960000000))
        self.assertTrue(witness["admissible_under_current_contract"])

    def test_current_noise_requires_smaller_pre_return_support(self):
        result = _subject().measurement_cap_certificate()
        requirement = result["necessary_source_contract"]
        self.assertEqual(requirement["q_halfwidth_max"], F(55784997, 145000000))
        self.assertEqual(requirement["absolute_reduction"], F(702581459, 6960000000))
        self.assertEqual(requirement["scale_max"], F(2677679856, 3380261315))
        self.assertLess(requirement["scale_max"], 1)

    def test_measurement_only_route_is_rejected_with_limited_claim(self):
        result = _subject().run()
        self.assertEqual(result["status"], "pass")
        self.assertTrue(result["measurement_only_global_cap_impossible"])
        self.assertTrue(result["seed_measurement_branch_terminated"])
        self.assertFalse(result["is_recursive_feasibility_proof"])
        self.assertFalse(result["is_full_six_state_guarantee"])


if __name__ == "__main__":
    unittest.main()
