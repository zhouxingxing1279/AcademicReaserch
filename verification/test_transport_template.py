import unittest
from fractions import Fraction as Q
import numpy as np
from check_transport_template import Transport, analytical_bounds, obstruction
from check_constrained_zonotope import eye


class TransportContracts(unittest.TestCase):
    def test_every_transport_identity_and_noise_support(self):
        t = Transport()
        for row, terms in enumerate(t.terms):
            actual = sum((weight*t.h[col] for col, weight in terms), np.array([Q(0)]*6))
            self.assertTrue(np.array_equal(actual, t.h[row] @ t.f))
            self.assertEqual(t.q[row], sum(abs(x) for x in t.h[row] @ t.w))
            self.assertTrue(all(weight >= 0 for _, weight in terms))

    def test_velocity_is_recovered_from_two_position_strips(self):
        t = Transport()
        b = [Q(100)]*len(t.h)
        b[0], b[6] = Q(2), Q(-2)
        j = t.strip(0, 10, 1)
        b[j], b[j+1] = Q(1), Q(-1)
        result = t.close(b)
        self.assertEqual(result[2], Q(5))
        self.assertEqual(result[8], Q(-5))

    def test_monotone_transport_preserves_shift_without_cap(self):
        t = Transport()
        wide = t.initial()
        narrow = [x-Q(1, 1000) for x in wide]
        for _ in range(25):
            wide, narrow = t.predict(wide), t.predict(narrow)
            self.assertTrue(all(a <= b for a, b in zip(narrow, wide)))

    def test_no_position_packet_still_uses_angle_measurements(self):
        t = Transport()
        b = [Q(100)]*len(t.h)
        result = t.update(b, [4, 5], [Q(1, 1000), Q(0)])
        self.assertEqual(result[0], 100)
        self.assertEqual(result[4], Q(6, 1000))
        self.assertEqual(result[10], Q(4, 1000))

    def test_all_gap_age_bounds_and_exact_obstruction(self):
        bounds = analytical_bounds(Transport())
        self.assertEqual(len(bounds['cases']), 45)
        self.assertLess(Q(bounds['max_velocity_halfwidth'][0]), 3)
        self.assertLess(Q(bounds['max_velocity_halfwidth'][1]), 3)
        proof = obstruction(Transport())
        self.assertGreater(Q(proof['terminal_velocity_half_span']), 3)
        self.assertEqual(proof['elapsed_ticks'], 39)


if __name__ == '__main__':
    unittest.main()
