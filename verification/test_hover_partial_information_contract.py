import json
import unittest
from fractions import Fraction as F
from pathlib import Path


class HoverPartialInformationContractTests(unittest.TestCase):
    def _step(self, success):
        try:
            from check_hover_partial_information_contract import split_successor
        except ImportError as exc:
            self.fail(f"hover partial-information checker is missing: {exc}")
        zeros = [F(0)] * 6
        return split_successor(
            success=success,
            eta=zeros,
            d=zeros,
            z=zeros,
            nominal_input=[F(981, 100), F(0)],
            correction=[F(0), F(0)],
            primitives={
                "rho_x": F(1),
                "rho_z": F(1),
                "n_px_next": F(1, 2),
                "n_pz_next": F(-1, 2),
                "n_phi_next": F(1),
                "n_omega_next": F(-1),
            },
        )

    def test_miss_edge_splits_shared_physical_residual_without_duplication(self):
        result = self._step(False)
        self.assertEqual(result["eta_next"], result["eta_next_oracle"])
        self.assertTrue(result["run136_bounds_ok"])
        self.assertEqual(result["d_next"][4:], [F(1, 200), F(-1, 100)])

    def test_success_edge_splits_one_residual_and_one_measurement_primitive(self):
        result = self._step(True)
        self.assertEqual(result["eta_next"], result["eta_next_oracle"])
        self.assertTrue(result["run136_bounds_ok"])
        self.assertEqual(
            [a + b for a, b in zip(result["eta_next"], result["d_next"])],
            result["tracking_error_next"],
        )

    def test_residual_scaling_and_run136_bridge_hold_at_source_domain_boundaries(self):
        from check_hover_partial_information_contract import split_successor

        for thrust in (F(981, 200), F(2943, 200)):
            for phi in (F(-9, 20), F(9, 20)):
                for rho_x, rho_z in ((F(-1), F(-1)), (F(1), F(1))):
                    with self.subTest(thrust=thrust, phi=phi, rho_x=rho_x):
                        zeros = [F(0)] * 6
                        z = zeros.copy()
                        z[4] = phi
                        result = split_successor(
                            success=False,
                            eta=zeros,
                            d=zeros,
                            z=z,
                            nominal_input=[F(981, 100), F(0)],
                            correction=[thrust - F(981, 100), F(0)],
                            primitives={
                                "rho_x": rho_x, "rho_z": rho_z,
                                "n_px_next": F(0), "n_pz_next": F(0),
                                "n_phi_next": F(0), "n_omega_next": F(0),
                            },
                        )
                        self.assertEqual(result["eta_next"], result["eta_next_oracle"])
                        self.assertTrue(result["run136_bounds_ok"])

    def test_constants_must_agree_with_configuration(self):
        from check_hover_partial_information_contract import audit_config_constants

        config = json.loads((Path(__file__).resolve().parents[1] / "configs/planar_baseline.json").read_text())
        config["plant"]["dt_s"] = 0.03
        with self.assertRaises(AssertionError):
            audit_config_constants(config)

    def test_repository_contract_covers_all_17_edges_exactly(self):
        try:
            from check_hover_partial_information_contract import run
        except ImportError as exc:
            self.fail(f"hover partial-information checker is missing: {exc}")
        result = run()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(len(result["edge_contract_checks"]), 17)
        self.assertTrue(all(row["pass"] for row in result["edge_contract_checks"]))
        self.assertEqual(
            result["evidence_level"],
            "problem_contract_ready_not_an_invariant_set_certificate",
        )


if __name__ == "__main__":
    unittest.main()
