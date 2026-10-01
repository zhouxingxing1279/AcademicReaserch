"""Regression tests for the Run-129 certificate-carrying Scott audit."""

from __future__ import annotations

import unittest
from fractions import Fraction
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np


class TestRun129CertificateCarryingScott(unittest.TestCase):
    def _module(self):
        try:
            from verification import check_run129_certificate_carrying_scott
        except ImportError as exc:
            self.fail(f"Run-129 certificate module is missing: {exc}")
        return check_run129_certificate_carrying_scott

    def test_equality_adjustment_recovers_hidden_box_budget(self) -> None:
        """Catches a certificate that ignores equality-slice freedom."""
        module = self._module()
        certificate = module.equality_adjusted_row_certificate(
            coefficients=np.array([1.2]),
            constraints=np.array([[1.0]]),
            rhs=np.array([0.5]),
        )

        self.assertTrue(certificate.success)
        self.assertLessEqual(certificate.budget, 0.6 + 1e-10)
        np.testing.assert_allclose(
            certificate.adjusted_coefficients,
            np.array([0.0]),
            atol=1e-9,
        )
        self.assertAlmostEqual(abs(certificate.offset), 0.6, places=9)

    def test_any_strict_budget_excess_requires_a_row_audit(self) -> None:
        """Catches unsafe admission of an over-budget row via a tolerance."""
        module = self._module()
        rows = module.strictly_over_budget_rows(
            np.array([1.0, 1.0 + 5e-13, 0.999999999999])
        )
        self.assertEqual(rows, (1,))

    def test_scott_lineage_reconstructs_one_step_reduction(self) -> None:
        """Catches a column-order or scaling error in the carried map."""
        module = self._module()
        from verification.check_run126_scott_cz_baseline import (
            build_run123_posterior_cz,
            scott_lift_then_reduce,
        )

        source, lifted = build_run123_posterior_cz()
        candidate = module.scott_lineage_candidate(target_generators=604)
        reference = scott_lift_then_reduce(lifted, target_generators=604)

        np.testing.assert_allclose(
            candidate.reduced.generators,
            reference.generators,
            rtol=2e-13,
            atol=2e-15,
        )
        np.testing.assert_allclose(
            candidate.reduced.constraints,
            reference.constraints,
            rtol=2e-13,
            atol=2e-15,
        )
        np.testing.assert_allclose(
            source.generators @ candidate.coefficients,
            candidate.reduced.generators,
            rtol=2e-13,
            atol=2e-15,
        )

    def test_first_elimination_has_exact_dual_budget_obstruction(self) -> None:
        """Catches false admission caused by a tolerant floating row LP."""
        module = self._module()
        audit = module.audit_terminal_certificate(target_generators=604)

        self.assertFalse(audit.certified)
        self.assertEqual(audit.violating_rows, (4, 27, 78, 601))
        self.assertGreater(audit.minimum_exact_dual_margin, 1.2e-8)
        for row in audit.row_audits:
            self.assertTrue(row.exact_dual_feasible)
            self.assertEqual(row.exact_equality_residual, 0)
            self.assertLessEqual(row.exact_box_excess, 0)
            self.assertGreater(row.exact_dual_margin, 0)

    def test_direct_script_archives_first_step_obstruction(self) -> None:
        """Catches an entrypoint that omits the exact witness checks."""
        root = Path(__file__).resolve().parents[1]
        environment = os.environ.copy()
        environment["ACADEMIC_RESEARCH_NO_WRITE"] = "1"
        completed = subprocess.run(
            [
                sys.executable,
                str(
                    root
                    / "verification/check_run129_certificate_carrying_scott.py"
                ),
            ],
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, msg=completed.stderr)
        report = json.loads(completed.stdout)
        first = report["first_elimination"]
        self.assertEqual(first["target_generators"], 604)
        self.assertFalse(first["certificate_feasible"])
        self.assertEqual(first["violating_rows"], [4, 27, 78, 601])
        self.assertTrue(first["all_exact_dual_witnesses_feasible"])
        for row in first["rows"]:
            self.assertGreater(Fraction(row["exact_dual_margin_fraction"]), 0)


if __name__ == "__main__":
    unittest.main()
