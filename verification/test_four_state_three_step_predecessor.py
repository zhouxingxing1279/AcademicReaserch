"""Run226: exact three-step robust predecessor tests."""
import unittest
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_three_step_predecessor as m

class ThreeStepPredecessorTests(unittest.TestCase):
    def test_three_step_positive_and_negative_witnesses(self):
        for sign in (1,-1):
            d=m.positive_three_step(sign)
            self.assertEqual(len(d['enclosures']),3)
            self.assertTrue(d['in_Pre3_X_sufficient'])
            self.assertTrue(all(-m.VMAX<=Q(b['v'][0])<=Q(b['v'][1])<=m.VMAX for b in d['enclosures']))

    def test_two_step_positive_and_negative_witnesses(self):
        for sign in (1,-1):
            d=m.two_step_but_not_three(sign)
            self.assertEqual(len(d['two_step_enclosures']),2)
            self.assertTrue(d['in_Pre2_X_sufficient'])

    def test_three_step_strict_exclusion_gap(self):
        d=m.third_step_gap()
        self.assertGreater(Q(d['lower_bound_on_adversarial_v3_minus_3']),0)
        self.assertEqual(Q(d['phi1']),Q(71,500))
        self.assertEqual(Q(d['phi2_max']),Q(339,2500))

    def test_any_first_torque_has_angle_bounded(self):
        d=m.third_step_gap()
        for tau in (-m.TAUMAX,Q(0),m.TAUMAX):
            phi2=m.PHI+2*m.H*m.BAD_OMEGA+m.H*m.H*tau/m.INERTIA
            self.assertLessEqual(phi2,Q(d['phi2_max']))
            self.assertGreaterEqual(phi2,Q(d['phi2_min']))

    def test_adversarial_thrust_monotonicity(self):
        # Every possible third-step angle is strictly above the thrust-dependent residual slope.
        d=m.third_step_gap()
        for phi in (Q(d['phi0']),Q(d['phi1']),Q(d['phi2_min'])):
            self.assertGreater(m.sine_bounds(phi)[0],m.RT)

    def test_archive_contract(self):
        d=m.verify()
        self.assertEqual(len(d['three_step_inclusions']),2)
        self.assertEqual(len(d['two_step_but_not_three_step']),2)
        self.assertEqual(d['gate_A'],'blocked')

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(m.config_contract(root))
        else:
            self.skipTest('requires full checkout; GitHub Actions must verify')

if __name__=='__main__': unittest.main()
