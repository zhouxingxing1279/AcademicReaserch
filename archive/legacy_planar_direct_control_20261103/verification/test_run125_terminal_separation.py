import unittest
from fractions import Fraction as Q

import numpy as np

from verification.check_run125_terminal_separation import (
    _exact_contract_posterior,
    exact_block_tail_support_upper,
    exact_terminal_direction,
    replay_archived_certificate,
    verify_terminal_separation,
)
from verification.check_run124_recenter_compression import _shifted_candidate


class Run125TerminalSeparationTest(unittest.TestCase):
    def test_block_tail_upper_is_exact_on_scalar_geometric_series(self):
        bound = exact_block_tail_support_upper(
            [[Q(1, 2)]], [Q(1)], Q(1), [Q(1)], head_length=1, block_length=1
        )
        self.assertEqual(bound, Q(2))

    def test_block_tail_upper_bounds_signed_nonnormal_partial_sum(self):
        matrix = [[Q(1, 2), Q(1, 4)], [Q(0), Q(1, 3)]]
        state = [Q(1), Q(-1)]
        direction = [Q(2), Q(-3)]
        partial = Q(0)
        for _ in range(200):
            partial += abs(sum(a * b for a, b in zip(direction, state)))
            state = [
                matrix[0][0] * state[0] + matrix[0][1] * state[1],
                matrix[1][1] * state[1],
            ]
        bound = exact_block_tail_support_upper(
            matrix,
            [Q(1), Q(-1)],
            Q(1),
            direction,
            head_length=3,
            block_length=4,
        )
        self.assertGreaterEqual(bound, partial)

    def test_rational_contract_preserves_run123_latent_order(self):
        generator_rows, inequalities, bounds = _exact_contract_posterior()
        posterior, *_ = _shifted_candidate()
        actual_inequalities, actual_bounds = posterior._inequalities()
        self.assertTrue(
            np.allclose(
                np.asarray(generator_rows, dtype=float),
                posterior.generators,
                rtol=0.0,
                atol=1e-14,
            )
        )
        self.assertTrue(
            np.allclose(
                np.asarray(inequalities, dtype=float),
                actual_inequalities,
                rtol=0.0,
                atol=1e-14,
            )
        )
        self.assertTrue(
            np.allclose(
                np.asarray(bounds, dtype=float), actual_bounds, rtol=0.0, atol=1e-15
            )
        )

    def test_run124_nonzero_recenter_has_strict_certified_separator(self):
        result = verify_terminal_separation()
        certificate = result["separation_certificate"]
        self.assertTrue(certificate["certified_noncontainment"])
        self.assertGreater(certificate["exact_gap"], 0.002)
        self.assertLessEqual(certificate["exact_witness_max_inequality_excess"], 0.0)
        self.assertLessEqual(certificate["exact_witness_max_box_excess"], 0.0)
        self.assertNotEqual(
            result["terminal_implication"]["exact_closed_loop_determinant"], 0.0
        )
        self.assertGreater(result["terminal_implication"]["exact_support_gap"], 0.0)

    def test_terminal_direction_exactly_cancels_finite_reachable_prefix(self):
        direction, terminal_direction, identity_residual = exact_terminal_direction()
        self.assertEqual(identity_residual, [Q(0), Q(0), Q(0), Q(0)])

        # Hand-check the support decomposition S_(N+L)=R_N (+) F^N S_L.
        from verification.check_run125_terminal_separation import (
            _dot,
            _exact_model,
            _matrix_power,
            _mv,
        )
        from verification.check_run122_run119_reproduction import HORIZON

        matrix, generator, radius = _exact_model()
        state = generator[:]
        direct = Q(0)
        prefix = Q(0)
        for index in range(HORIZON + 11):
            term = radius * abs(_dot(terminal_direction, state))
            direct += term
            if index < HORIZON:
                prefix += term
            state = _mv(matrix, state)
        state = generator[:]
        shifted = Q(0)
        for _ in range(11):
            shifted += radius * abs(_dot(direction, state))
            state = _mv(matrix, state)
        self.assertEqual(direct, prefix + shifted)
        power = _matrix_power(matrix, HORIZON)
        self.assertNotEqual(power, [])

    def test_archived_witness_replays_without_solver(self):
        replay = replay_archived_certificate()
        self.assertTrue(replay["certified_noncontainment"])
        self.assertTrue(replay["certified_terminal_noncontainment"])
        self.assertGreater(replay["exact_gap"], 0.002)


if __name__ == "__main__":
    unittest.main()
