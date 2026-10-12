import importlib
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))


def _subject():
    return importlib.import_module("check_vertical_shared_factor_graph")


class VerticalSharedFactorGraphTests(unittest.TestCase):
    def test_run169_point_satisfies_shared_relative_velocity_graph(self):
        graph = _subject().shared_factor_graph_certificate()["shared_factor_graph"]
        self.assertEqual(graph["relative_velocity"], (F(7, 2), F(-206955031, 72000000)))
        self.assertTrue(graph["all_affine_factor_equalities_hold"])
        self.assertTrue(graph["state_wind_pitch_and_thrust_domains_hold"])

    def test_exact_sqrt_brackets_certify_the_true_vertical_aerodynamic_image(self):
        aero = _subject().shared_factor_graph_certificate()["vertical_aerodynamic_image"]
        self.assertTrue(aero["sqrt_brackets_are_exact"])
        self.assertLess(aero["lower"], aero["upper"])
        self.assertGreater(aero["lower"], F(89401829, 65520000))

    def test_single_step_sound_outer_graph_cannot_exclude_the_witness(self):
        result = _subject().run()
        self.assertTrue(result["exact_nonlinear_graph_point_exists"])
        self.assertTrue(result["every_sound_single_step_graph_outer_approximation_must_include_its_image"])
        self.assertFalse(result["nonlinear_history_from_initial_set_proved"])
        self.assertTrue(result["cross_time_joint_reachability_remains_required"])
        self.assertFalse(result["is_recursive_feasibility_proof"])


if __name__ == "__main__":
    unittest.main()
