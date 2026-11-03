import itertools
import unittest
from fractions import Fraction as Q
from check_intermit_smf_mpc_closed_loop import (
    A, W, V, TERMINAL, GRID, HORIZON, X, U,
    contains, cost, feasible, optimize, predict, run, shift,
    terminal_invariant, update,
)


class IntermittentSMFMPCTests(unittest.TestCase):
    def test_terminal_is_robust_invariant(self):
        self.assertTrue(terminal_invariant())
        self.assertLessEqual(A * TERMINAL + W, TERMINAL)

    def test_measurement_intersection_and_missing(self):
        prior = (Q(-1, 2), Q(1, 2))
        self.assertEqual(update(prior, None), prior)
        self.assertEqual(update(prior, Q(1, 2)), (Q(2, 5), Q(1, 2)))
        with self.assertRaises(ValueError):
            update(prior, Q(2))

    def test_initial_feasible_and_optimizer_exact_grid_optimality(self):
        belief = (Q(-1), Q(1))
        fallback = (Q(0),) * HORIZON
        self.assertTrue(feasible(belief, fallback))
        plan, count = optimize(belief, fallback)
        self.assertTrue(feasible(belief, plan))
        self.assertGreater(count, 0)
        self.assertEqual(cost(belief, plan), min(
            cost(belief, p) for p in itertools.product(GRID, repeat=HORIZON)
            if feasible(belief, p)))

    def test_all_endpoint_observations_preserve_shift_feasibility(self):
        prior = (Q(-9, 10), Q(9, 10))
        plan, _ = optimize(prior, (Q(0),) * HORIZON)
        u = plan[0]
        for x in prior:
            for w in (-W, W):
                actual = A * x + u + w
                predicted = predict(prior, u)
                for y in (None, actual - V, actual + V):
                    post = update(predicted, y)
                    self.assertTrue(contains(post, actual))
                    self.assertTrue(feasible(post, shift(plan)))
                    self.assertLessEqual(abs(actual), X)
                    self.assertLessEqual(abs(u), U)

    def test_replay_includes_misses_and_actual_optimizations(self):
        result = run()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["episodes"], 16)
        self.assertEqual(result["steps"], 384)
        self.assertGreater(result["missed_packets"], 0)
        self.assertGreater(result["received_packets"], 0)
        self.assertGreater(result["optimizer_changes"], 0)
        self.assertEqual(result["violations"], 0)


if __name__ == "__main__":
    unittest.main()
