import importlib
import unittest


class RollingControlNormalLedgerTests(unittest.TestCase):
    def test_checker_imports_and_runs_a_minimal_audit(self):
        """An unmatched delimiter hidden outside test discovery must fail."""
        subject = importlib.import_module("check_rolling_control_normal_ledger")
        result = subject.run(horizon=1, ticks=1)

        self.assertEqual(
            result["status"],
            "rolling_control_normal_ledger_audit_not_full_mpc_proof",
        )
        self.assertEqual(result["horizon"], 1)
        self.assertEqual(result["ticks"], 1)


if __name__ == "__main__":
    unittest.main()
