import unittest
from fractions import Fraction as F
from check_run262_actuation_delay import H, J, T, U, R, certificate


class TestRun262(unittest.TestCase):
    def test_exact_constants(self):
        self.assertEqual(H, F(1, 50))
        self.assertEqual(J, H)
        self.assertEqual(U, F(2, 25))

    def test_torque_delay(self):
        for tau0 in (-U, F(0), U):
            phi = omega = F(0)
            for tau in (tau0, -U):
                phi, omega = phi + H * omega, omega + H * tau / J
            self.assertEqual(phi, H * H * tau0 / J)

    def test_velocity_first_two_steps(self):
        self.assertEqual(2 * H * R, F(3246383, 40000000))

    def test_velocity_lower_bound(self):
        self.assertEqual(3*H*R-H*T*(H*H*U/J), F(48570177, 400000000))

    def test_exceeds_narrow_terminal(self):
        self.assertGreater(F(certificate()['v3_universal_lower_under_plusR']), F(3,25))

    def test_witness_safe_position(self):
        self.assertLess(3*H*H*R, F(5))

    def test_symmetric_span(self):
        self.assertEqual(F(certificate()['v3_necessary_symmetric_velocity_span']), F(48570177, 200000000))

    def test_scope(self):
        c = certificate()
        self.assertFalse(c['closed_loop_controller_implemented'])
        self.assertFalse(c['terminal_information_RCI_certified'])
        self.assertEqual(c['gate_A'], 'blocked')


if __name__ == '__main__':
    unittest.main()
