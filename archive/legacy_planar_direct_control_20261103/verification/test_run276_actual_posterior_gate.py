import unittest
from fractions import Fraction as F
import check_run276_actual_posterior_gate as m

class Run276Tests(unittest.TestCase):
    def test_pulse_and_legality(self):
        x=m.states()
        self.assertEqual(x[30],(F(0),)*4)
        self.assertEqual(x[35][2:],(F(0),F(0)))
        self.assertLess(F(4,5)*m.R+m.T/F(1250),m.R)
        self.assertEqual(x[35][0],8*m.R*m.H*m.H)
    def test_independent_kinematics(self):
        x=m.states()
        self.assertEqual(x[90][1],m.H*m.R*59)
        self.assertEqual(x[90][0],m.H*m.H*m.R*(F(4,5)*sum(89-k for k in range(30,35))+sum(89-k for k in range(35,90))))
    def test_actual_run260_membership(self):
        c=m.verify();self.assertTrue(c['all_packet_streaks_legal'])
        self.assertTrue(c['all_measurement_noises_within_bounds'])
        self.assertTrue(c['all_hard_state_constraints_satisfied'])
        self.assertEqual(c['packet_history_5_to_90'][:9],'SSSMMSSMM')
    def test_smm_outer(self):
        x=m.states()
        self.assertLess(abs(x[45][0]),F(406119767,2500000000))
        self.assertLess(abs(x[45][1]),F(9408238409,10000000000))
        self.assertLess(abs(x[60][0]),F(665412229,1250000000))
        self.assertLess(abs(x[60][1]),F(7841778593,5000000000))
    def test_gate_refutation(self):
        c=m.verify()
        self.assertGreater(F(c['speed_at_90']),F(c['speed_gate_G']))
        self.assertGreater(F(c['actual_displacement_85_90']),F(c['run275_gate_85_90']))
        self.assertLess(F(c['speed_at_90']),3)
    def test_noise_at_35(self):
        self.assertEqual(F(m.verify()['position_noise_tick35']),-F(3246383,500000000))
        self.assertLess(abs(F(m.verify()['position_noise_tick35'])),m.EPS)

if __name__=='__main__': unittest.main()
