"""Regression tests for the Run-127 terminal-containment audit."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock


class TestRun127TerminalCZAudit(unittest.TestCase):
    def _module(self):
        try:
            from verification import check_run127_terminal_cz_audit
        except ImportError as exc:  # keeps the TDD RED state explicit
            self.fail(f"Run-127 audit module is missing: {exc}")
        return check_run127_terminal_cz_audit

    def test_exact_terminal_direction_mapping_has_zero_residual(self) -> None:
        module = self._module()
        _, _, residual = module.exact_terminal_direction()
        self.assertTrue(all(value == 0 for value in residual))

    def test_frozen_539_cz_has_exactly_feasible_separator_witness(self) -> None:
        module = self._module()
        certificate = module.exact_separator_certificate()
        self.assertEqual(certificate["target_generators"], 539)
        self.assertTrue(certificate["exact_equalities_hold"])
        self.assertLessEqual(certificate["exact_box_excess"], 0.0)
        self.assertGreater(certificate["exact_support_gap"], 5e-8)
        self.assertGreater(
            certificate["exact_mrpi_upper"] - certificate["finite_head_support"],
            0.0,
        )

    def test_report_does_not_overclaim_general_scott_failure(self) -> None:
        module = self._module()
        report = module.verify_terminal_cz_audit()
        self.assertEqual(report["evidence_level"], "implementation_counterexample")
        self.assertFalse(report["claims_general_scott_failure"])
        self.assertFalse(report["claims_full_nonlinear_quadrotor_guarantee"])
        self.assertTrue(report["terminal_containment_refuted"])

    def test_saved_exact_artifact_replays_without_linprog(self) -> None:
        module = self._module()
        report = json.loads(module.RESULT_PATH.read_text(encoding="utf-8"))
        with mock.patch.object(
            module,
            "linprog",
            side_effect=AssertionError("artifact replay must be solver-free"),
        ):
            replay = module.replay_artifact_certificate(report)
        self.assertTrue(replay["exact_equalities_hold"])
        self.assertTrue(replay["stored_exact_values_match"])
        self.assertGreater(replay["exact_support_gap"], 5e-8)

    def test_direct_script_entrypoint_emits_json(self) -> None:
        root = Path(__file__).resolve().parents[1]
        environment = os.environ.copy()
        environment["ACADEMIC_RESEARCH_NO_WRITE"] = "1"
        completed = subprocess.run(
            [sys.executable, str(root / "verification/check_run127_terminal_cz_audit.py")],
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, msg=completed.stderr)
        report = json.loads(completed.stdout)
        self.assertTrue(report["terminal_containment_refuted"])


if __name__ == "__main__":
    unittest.main()
