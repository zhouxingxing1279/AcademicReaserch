"""Run238 exact-rational 15-tick shared-information backup regressions."""
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_fiber_recovery as m


class FiberRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert = m.verify()

    def test_initial_fiber(self):
        self.assertEqual(m.generators(0), [(F(0), m.H*m.D, F(0), F(0))])

    def test_one_step_exact(self):
        self.assertEqual(m.support(1, (F(1), F(0), F(0), F(0))), F(1742383, 2000000000))
        self.assertEqual(m.support(1, (F(0), F(1), F(0), F(0))), F(6731149, 80000000))

    def test_generator_shift(self):
        for n in range(15):
            self.assertEqual([m.advance_zero_torque(g) for g in m.generators(n)] +
                             [(F(0),m.H*m.R,F(0),F(0))], m.generators(n+1))

    def test_15_step_exact(self):
        self.assertEqual(m.support(15, (F(1),F(0),F(0),F(0))), F(78628341,800000000))
        self.assertEqual(m.support(15, (F(0),F(1),F(0),F(0))), F(52180511,80000000))

    def test_constraints_every_tick(self):
        self.assertTrue(self.cert['all_0_to_15_state_and_input_hard_constraints_certified'])
        for n in range(16):
            for j, limit in enumerate(m.STATE_LIMITS):
                direction = tuple(F(i == j) for i in range(4))
                self.assertLess(m.support(n, direction), limit)

    def test_causal_shared_control(self):
        self.assertEqual(self.cert['common_causal_policy'], 'T=981/100 N, tau=0 Nm; ignores all measurements')
        self.assertLessEqual(abs(F(0)), m.TAU_MAX)

    def test_negative_uncontrolled_long_horizon(self):
        self.assertEqual(self.cert['zero_torque_backup_first_speed_violation_tick_under_positive_adversary'], 73)
        self.assertGreater(m.H*m.D+73*m.H*m.R, m.STATE_LIMITS[1])

    def test_no_invariance_claim(self):
        self.assertFalse(self.cert['terminal_invariance_certified'])
        self.assertFalse(self.cert['smf_mpc_recursive_feasibility_certified'])
        self.assertFalse(self.cert['full_prior_certified'])

    def test_config_contract(self):
        root = Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertEqual(m.verify(root), self.cert)
        else:
            self.skipTest('requires full checkout; CI must verify')


if __name__ == '__main__':
    unittest.main()
