import unittest
from check_run269_unobserved_gap import (H, R, MAX_GAP, certificate, difference, zero_torque_witness)

class Run269Tests(unittest.TestCase):
    def test_gap14_exact(self):
        self.assertEqual(difference(14)['velocity'], 28 * H * R)
        self.assertEqual(difference(14)['position'], 182 * H * H * R)

    def test_gap1_position_unaffected(self):
        self.assertEqual(difference(1)['position'], 0)
        self.assertEqual(difference(1)['velocity'], 2 * H * R)

    def test_endpoint_pair(self):
        a = zero_torque_witness(14, 1)[-1]
        b = zero_torque_witness(14, -1)[-1]
        self.assertEqual(a[0] - b[0], difference(14)['position'])
        self.assertEqual(a[1] - b[1], difference(14)['velocity'])

    def test_full_trajectory_safe(self):
        for sign in (-1, 1):
            for p, v, phi, omega in zero_torque_witness(MAX_GAP, sign):
                self.assertLessEqual(abs(p), 5)
                self.assertLessEqual(abs(v), 3)
                self.assertEqual(phi, 0)
                self.assertEqual(omega, 0)

    def test_formula_each_tick(self):
        for q in range(MAX_GAP + 1):
            a = zero_torque_witness(q, 1)[-1]
            b = zero_torque_witness(q, -1)[-1]
            self.assertEqual(a[0]-b[0], difference(q)['position'])
            self.assertEqual(a[1]-b[1], difference(q)['velocity'])

    def test_no_future_success_claim(self):
        with self.assertRaises(ValueError):
            difference(15)

    def test_certificate_metadata(self):
        c = certificate()
        self.assertEqual(c['gate_A'], 'blocked')
        self.assertIn('not a bound after tick60', c['scope'])
        self.assertEqual(len(c['gaps']), 6)

if __name__ == '__main__':
    unittest.main()
