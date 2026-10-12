import importlib
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))


def _subject():
    return importlib.import_module("check_vertical_local_aerodynamic_counterexample")


class VerticalLocalAerodynamicCounterexampleTest(unittest.TestCase):
    def test_return_velocity_endpoints_are_jointly_admitted_by_abstract_contract(self):
        result = _subject().local_aerodynamic_counterexample_certificate()
        seed = result["j14_return_velocity_seed"]
        self.assertEqual(seed["horizontal_halfwidth"], F(113619923, 40000000))
        self.assertEqual(seed["vertical_halfwidth"], F(152955031, 72000000))
        self.assertTrue(seed["source_generator_supports_disjoint"])
        self.assertTrue(seed["opposite_vertical_and_horizontal_endpoints_jointly_admitted"])

    def test_witness_respects_nominal_physical_and_wind_domains(self):
        result = _subject().local_aerodynamic_counterexample_certificate()
        witness = result["admissible_first_edge_witness"]
        self.assertEqual(witness["nominal_velocity"], (F(6380077, 40000000), F(-1, 4)))
        self.assertEqual(witness["physical_velocity"], (F(3), F(-170955031, 72000000)))
        self.assertEqual(witness["wind"], (F(-1, 2), F(1, 2)))
        self.assertEqual(witness["relative_velocity"], (F(7, 2), F(-206955031, 72000000)))
        self.assertEqual(witness["pitch"], F(0))
        self.assertTrue(witness["all_configured_domains_satisfied"])

    def test_rational_aerodynamic_lower_bound_breaks_run168_target(self):
        result = _subject().local_aerodynamic_counterexample_certificate()
        obstruction = result["first_edge_obstruction"]
        self.assertEqual(obstruction["rational_lower_bound"], F(51297584856210961, 34560000000000000))
        self.assertEqual(obstruction["run168_target"], F(89401829, 65520000))
        self.assertEqual(obstruction["strict_excess"], F(376792429915197451, 3144960000000000000))
        self.assertTrue(obstruction["strictly_exceeds_target"])

    def test_counterexample_rejects_only_the_independent_residual_outer_contract(self):
        result = _subject().run()
        self.assertTrue(result["abstract_independent_residual_contract_breaks_target"])
        self.assertFalse(result["nonlinear_benchmark_trajectory_witness_proved"])
        self.assertFalse(result["frozen_j14_local_residual_route_impossible"])
        self.assertTrue(result["joint_physical_reachability_route_open"])
        self.assertFalse(result["all_alternative_seed_or_model_contracts_ruled_out"])
        self.assertFalse(result["is_recursive_feasibility_proof"])
        self.assertFalse(result["is_full_six_state_guarantee"])


if __name__ == "__main__":
    unittest.main()
