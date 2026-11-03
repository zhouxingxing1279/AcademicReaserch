import hashlib
import importlib
import json
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def _subject():
    try:
        return importlib.import_module("check_houska_vertical_adapter")
    except ModuleNotFoundError:
        return None


class HouskaVerticalAdapterTests(unittest.TestCase):
    def test_fixed_lti_and_global_residual_envelope_are_exact(self):
        """Using hover rather than maximum thrust would underbound process noise."""
        subject = _subject()
        adapter = getattr(subject, "adapter_contract", None)
        self.assertTrue(callable(adapter))
        config = json.loads((ROOT / "configs/planar_baseline.json").read_text(), parse_float=F)
        result = adapter(config)
        self.assertEqual(result["A"], [[F(1), F(1, 50)], [F(0), F(1)]])
        self.assertEqual(result["B"], [[F(0)], [F(1, 50)]])
        self.assertEqual(result["C"], [[F(1), F(0)]])
        self.assertEqual(result["continuous_residual_halfwidth"], F(572143, 160000))
        self.assertEqual(result["discrete_W_velocity_halfwidth"], F(572143, 8000000))

        drifted = deepcopy(config)
        drifted["mpc"]["ancillary_rci_contract"]["disturbance_graph"][
            "physical_residual_halfwidth"
        ]["r_z"] = "1043/500 + (1/10) * actual_thrust"
        with self.assertRaisesRegex(ValueError, "vertical residual formula"):
            adapter(drifted)

    def test_measurement_edges_and_branch_controls_preserve_packet_causality(self):
        """Giving miss edges a measurement or branch-specific current controls is noncausal."""
        subject = _subject()
        run = getattr(subject, "run", None)
        self.assertTrue(callable(run))
        result = run()
        self.assertEqual(result["mode_count"], 15)
        self.assertEqual(result["edge_count"], 17)
        self.assertEqual(result["measurement_operators"], {
            "miss": {"intersection": "identity", "noise_halfwidth": None},
            "success": {"intersection": "position_strip", "noise_halfwidth": F(1, 50)},
        })
        self.assertEqual(result["shared_control_branch_modes"], [4, 9])
        self.assertTrue(result["control_precedes_packet_outcome"])

        config = json.loads((ROOT / "configs/planar_baseline.json").read_text(), parse_float=F)
        drifted = deepcopy(config)
        drifted["mpc"]["ancillary_rci_contract"]["mode_graph"]["edges"][-1][2] = "miss"
        adapter_run = getattr(subject, "run_from_config", None)
        self.assertTrue(callable(adapter_run))
        with self.assertRaisesRegex(ValueError, "15-mode packet graph"):
            adapter_run(drifted)

        drifted = deepcopy(config)
        drifted["sensing"]["position_period_ticks"] = 4
        with self.assertRaisesRegex(ValueError, "position sensing schedule"):
            adapter_run(drifted)

    def test_hard_margins_are_derived_from_nominal_and_physical_boxes(self):
        """Using the physical box directly would omit nominal-state tightening."""
        subject = _subject()
        run = getattr(subject, "run", None)
        self.assertTrue(callable(run))
        result = run()
        self.assertEqual(result["tracking_error_box"], {
            "position_halfwidth": F(1),
            "velocity_halfwidth": F(11, 4),
        })
        self.assertEqual(result["correction_input_halfwidth"], F(572143, 160000))

        config = json.loads((ROOT / "configs/planar_baseline.json").read_text(), parse_float=F)
        drifted = deepcopy(config)
        drifted["mpc"]["nominal_input_upper"][0] -= F(1, 10)
        adapter = getattr(subject, "adapter_contract", None)
        with self.assertRaisesRegex(ValueError, "symmetric nominal input allocation"):
            adapter(drifted)

    def test_scope_and_hash_bound_artifact_are_reproducible(self):
        subject = _subject()
        run = getattr(subject, "run", None)
        self.assertTrue(callable(run))
        result = run()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["evidence_level"], "exact_houska_vertical_adapter_contract")
        self.assertFalse(result["invariant_information_ensemble_certified"])
        self.assertFalse(result["recursive_feasibility_certified"])
        self.assertFalse(result["full_six_state_guarantee"])
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "verification/check_houska_vertical_adapter.py"),
                 "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads((
                ROOT / "results/theory_houska_vertical_adapter_20261026/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(digest, hashlib.sha256((ROOT / name).read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
