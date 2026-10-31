"""Run225: two-step exact rational inclusion and strict exclusion checks."""
import unittest
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_two_step_predecessor as m

class TwoStepPredecessorTests(unittest.TestCase):
    def test_positive_and_negative_two_step_inclusions(self):
        for sign in (1,-1):
            cert=m.signed_box(sign)
            self.assertTrue(cert['in_Pre2_X_sufficient'])
            self.assertTrue(-m.VMAX <= Q(cert['second_velocity'][0]) <= Q(cert['second_velocity'][1]) <= m.VMAX)
            self.assertTrue(-m.PMAX <= Q(cert['second_position'][0]) <= Q(cert['second_position'][1]) <= m.PMAX)

    def test_bad_states_are_in_one_step_predecessor(self):
        for sign in (1,-1):
            x=(Q(0),sign*m.VMAX,sign*m.PHI,-sign*m.OMAX)
            self.assertTrue(m.certified_predecessor(x,m.TMAX,sign*m.TAUMAX))

    def test_bad_states_excluded_from_two_step_predecessor(self):
        self.assertEqual(m.PHI_NEXT_BAD,Q(11,100))
        self.assertEqual(m.bad_boundary_gap(),Q(15703932131047,2000000000000000))
        self.assertGreater(m.bad_boundary_gap(),0)

    def test_causal_torque_cannot_change_first_successor_angle(self):
        x=(Q(0),m.VMAX,m.PHI,-m.OMAX)
        for tau in (-m.TAUMAX,Q(0),m.TAUMAX):
            self.assertEqual(m.next_bounds(x,m.TMAX,tau)['phi'],(Q(11,100),)*2)

    def test_archive_contract(self):
        d=m.verify()
        self.assertEqual(len(d['two_step_inclusions']),2)
        self.assertEqual(len(d['one_step_but_not_two_step']),2)
        self.assertEqual(d['gate_A'],'blocked')

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(m.config_contract(root))
        else:
            self.skipTest('requires full checkout; verified by GitHub Actions')

if __name__=='__main__':unittest.main()
