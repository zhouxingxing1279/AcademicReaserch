import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from check_gate_a_control_baseline_audit import audit


class GateAControlBaselineAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit(ROOT)

    def test_gate_a_remains_blocked_without_sufficient_rci_certificate(self):
        self.assertEqual(self.result["gate"], "A")
        self.assertEqual(self.result["gate_status"], "blocked")
        self.assertFalse(self.result["sufficient_ancillary_rci_certificate_present"])

    def test_evidence_classes_prevent_plant_level_overclaim(self):
        by_id = {item["id"]: item for item in self.result["evidence"]}
        self.assertEqual(by_id["common_quadratic_static_K"]["level"], "DERIVED")
        self.assertEqual(by_id["specific_K_torque_obstruction"]["level"], "COUNTEREXAMPLE")
        self.assertEqual(by_id["static_K_search"]["level"], "NUMERIC_CHECK")
        self.assertEqual(by_id["axis_aligned_box_obstruction"]["level"], "COUNTEREXAMPLE")
        self.assertEqual(by_id["one_configuration_cone_farkas"]["level"], "COUNTEREXAMPLE")
        serialized = json.dumps(self.result).lower()
        for forbidden in (
            "all static gains are infeasible",
            "the plant is infeasible",
            "the orientation family is infeasible",
            "recursive feasibility is certified",
        ):
            self.assertNotIn(forbidden, serialized)

    def test_contract_is_scheduled_current_and_arbitrary_future_jump(self):
        contract = self.result["contract"]
        self.assertTrue(contract["current_thrust_measured"])
        self.assertEqual(contract["future_thrust"], "arbitrary_jump_in_interval")
        self.assertEqual(contract["smallest_universal_rate_bound_N_per_tick"], "9.810")
        self.assertTrue(contract["endpoint_reduction_exact_for_current_affine_contract"])

    def test_every_archived_evidence_has_matching_source_hash(self):
        for item in self.result["evidence"]:
            source = ROOT / item["source"]
            expected = hashlib.sha256(source.read_bytes()).hexdigest()
            self.assertEqual(item["source_sha256"], expected)

    def test_audit_binds_all_direct_dependencies(self):
        required = {
            "verification/check_gate_a_control_baseline_audit.py",
            "verification/test_gate_a_control_baseline_audit.py",
            "configs/planar_baseline.json",
            "results/lpv_common_quadratic_20260924/checks.json",
            "results/lpv_torque_rpi_obstruction_20260924/checks.json",
            "results/vertex_consistent_ancillary_20260924/checks.json",
            "results/actuator_authority_scheduled_residual_20260924/checks.json",
            "results/axis_aligned_rci_obstruction_20260924/checks.json",
            "results/thrust_scheduling_contract_20260924/checks.json",
            "results/endpoint_predecessor_reduction_20260924/checks.json",
            "results/cc_19pair_exact_farkas_20260924/checks.json",
        }
        hashes = self.result["audit_dependencies_sha256"]
        self.assertEqual(set(hashes), required)
        for relative, digest in hashes.items():
            self.assertEqual(
                digest, hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            )

    def test_checker_reproduces_archived_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checks.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(HERE / "check_gate_a_control_baseline_audit.py"),
                    "--root",
                    str(ROOT),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads(
                (ROOT / "results/gate_a_control_baseline_audit_20261027/checks.json").read_text()
            )
            self.assertEqual(generated, archived)

    def test_next_problem_is_a_sufficient_controller_rci_certificate(self):
        self.assertIn("sufficient", self.result["next_problem"].lower())
        self.assertIn("state", self.result["next_problem"].lower())
        self.assertIn("torque", self.result["next_problem"].lower())


if __name__ == "__main__":
    unittest.main()
