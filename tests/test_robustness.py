import unittest
from dataclasses import replace
from fractions import Fraction as F
import numpy as np
from experiments.robustness import exact_budget, radius_lines, stimulus, recovery, run_case
from src.outerloop.finite_memory import Contract
from src.outerloop.tube_mpc import TubeDesign


class RobustnessTests(unittest.TestCase):
    def test_rational_envelope_and_boundary_against_design(self):
        for M in range(4):
            for L in range(4):
                p, v = radius_lines(M, L)
                for a in [F(0), F(1, 50), F(1, 25), F(1, 10)]:
                    c = replace(Contract(), missing=M, delay=L, acceleration=float(a))
                    exact = [float(max(x+y*a for x, y in lines)) for lines in [p, v]]
                    np.testing.assert_allclose(exact, c.uniform_error(), atol=1e-12)
                upper = exact_budget(M, L)['strict_upper']
                c = replace(Contract(), missing=M, delay=L)
                if upper > 0:
                    self.assertGreater(TubeDesign(replace(c, acceleration=upper*(1-1e-6))).v_limit, 0)
                    with self.assertRaises(ValueError):
                        TubeDesign(replace(c, acceleration=upper*(1+1e-6)))

    def test_stimuli_are_paired_and_contract_legal(self):
        for delivery in ['fresh', 'max_gap', 'random']:
            s = stimulus(123, delivery, 'pulse', 1)
            self.assertEqual(s, stimulus(123, delivery, 'pulse', 1))
            w = np.array(s['disturbance'])
            self.assertTrue(np.all(w[:20] == 0) and np.all(w[30:] == 0))
            self.assertEqual(np.max(np.abs(w)), .02)
            gap = 0
            for event in s['events']:
                gap = gap+1 if event == -1 else 0
                self.assertLessEqual(gap, 1)
                self.assertIn(event, [-1, 0, 1])
            doubled = np.array(stimulus(123, delivery, 'pulse', 2)['disturbance'])
            np.testing.assert_array_equal(doubled, 2*w)

    def test_recovery_requires_complete_tail_and_uses_state_time(self):
        rows = [dict(k=k, next_p=.06 if k < 34 else .01, next_v=0.)
                for k in range(60) for _ in range(3)]
        self.assertEqual(recovery(rows, True), 2.5)
        self.assertIsNone(recovery(rows, False))
        rows[-1]['next_p'] = 1.
        self.assertIsNone(recovery(rows, True))

    def test_contract_failure_is_retained_without_fallback(self):
        s = stimulus(0, 'fresh', 'bias', 1, steps=8)
        s['events'] = [-1]*8
        summary, rows = run_case('deliberately_illegal', 'cz', s)
        self.assertEqual(summary['status'], 'estimator_contract_error')
        self.assertEqual(summary['failure_step'], Contract().span)
        self.assertEqual(len(rows), 3*Contract().span)
        self.assertFalse(summary['observed_safe_complete'])


if __name__ == '__main__':
    unittest.main()
