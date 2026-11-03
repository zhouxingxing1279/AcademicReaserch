import unittest
from fractions import Fraction as F
from check_run265_terminal_velocity_guard import H, J, T, U, R, V, certificate


class TestRun265(unittest.TestCase):
    def test_three_step_bound(self):
        self.assertEqual(3*H*R-H*T*H*H*U/J, F(48570177, 400000000))

    def test_positive_start_cap(self):
        c=certificate()
        self.assertEqual(F(c['necessary_v0_interval_at_zero_attitude_m_s'][1]), F(1151429823, 400000000))

    def test_negative_start_floor(self):
        c=certificate()
        self.assertEqual(F(c['necessary_v0_interval_at_zero_attitude_m_s'][0]), -F(1151429823, 400000000))

    def test_first_two_ticks_safe(self):
        c=certificate()
        self.assertLess(F(c['positive_adversarial_v2_m_s']), V)
        self.assertGreater(F(c['positive_adversarial_v1_m_s']), -V)

    def test_third_tick_unsafe_for_all_torques(self):
        c=certificate()
        self.assertGreater(F(c['positive_adversarial_v3_strict_lower_m_s']), V)

    def test_position_and_attitude_legal(self):
        c=certificate()
        self.assertLess(F(c['positive_adversarial_p3_m']), 5)
        self.assertLess(3*H*H*U/J, F(9,20))
        self.assertLess(3*H*U/J, 2)

    def test_width_only_counterexample(self):
        # Singleton information fiber width zero but physically unviable.
        self.assertEqual(F(29,10)-F(29,10), 0)
        self.assertGreater(F(29,10), F(certificate()['necessary_v0_interval_at_zero_attitude_m_s'][1]))

    def test_scope(self):
        c=certificate()
        self.assertEqual(c['gate_A'], 'blocked')
        self.assertIn('these states occur in Run260 tick60 posterior', c['does_not_assert'])


if __name__ == '__main__':
    unittest.main()
