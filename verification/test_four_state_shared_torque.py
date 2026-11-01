"""Run236 exact observation-fiber and information-permission regression."""
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_shared_torque as m
import check_four_state_finite_rpi as rpi

class SharedTorqueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=m.certificate()

    def test_generator_witness_in_F(self):
        self.assertEqual(tuple(map(F,self.c['state_plus'])),tuple(rpi.D*b for b in rpi.B))
        self.assertEqual(tuple(map(F,self.c['state_minus'])),tuple(-rpi.D*b for b in rpi.B))

    def test_same_output_even_at_position_packet(self):
        a=list(map(F,self.c['state_plus']));b=list(map(F,self.c['state_minus']))
        for i in (0,2,3):self.assertEqual(a[i],b[i])
        self.assertNotEqual(a[1],b[1])

    def test_both_states_inside_initial_prior(self):
        for s in ('state_plus','state_minus'):
            x=list(map(F,self.c[s]))
            self.assertLessEqual(abs(x[1]),F(1,10))
            self.assertEqual(x[0],0)

    def test_exact_minimax_lower_bound(self):
        a=F(self.c['torque_fullstate_plus']);b=F(self.c['torque_fullstate_minus'])
        d=F(self.c['minimax_common_torque_error_lower'])
        self.assertEqual(d,abs(a-b)/2)
        self.assertEqual(d,F(430368601,20000000000))
        for u in (F(-1,25),F(0),F(1,25),a,b):
            self.assertGreaterEqual(max(abs(u-a),abs(u-b)),d)

    def test_both_fullstate_torques_legal(self):
        self.assertLess(abs(F(self.c['torque_fullstate_plus'])),rpi.TAU_MAX)
        self.assertLess(abs(F(self.c['torque_fullstate_minus'])),rpi.TAU_MAX)

    def test_global_triangle_tightening_rejected(self):
        self.assertGreater(F(self.c['terminal_torque_support_lower'])+F(self.c['minimax_common_torque_error_lower']),rpi.TAU_MAX)
        self.assertEqual(self.c['prefix_terms'],100)

    def test_scope_and_nonclaim(self):
        self.assertIn('Does not show that no shared torque',self.c['limitations'][0])
        self.assertEqual(self.c['gate_A'],'blocked_for_output_feedback_SMF_MPC')

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertEqual(m.certificate(root),self.c)
        else:self.skipTest('requires full checkout; CI verifies actual config')

if __name__=='__main__':unittest.main()
