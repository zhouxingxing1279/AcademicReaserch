import unittest
from fractions import Fraction as F
from check_run271_mms_history_membership import certificate, angular_history, H, T, R, SUCCESS, MISS

class Run271Tests(unittest.TestCase):
    def test_certificate(self):
        self.assertEqual(certificate()['gate_A'],'blocked')
    def test_pulse_zero_net(self):
        a=angular_history()
        self.assertEqual(a[35],(F(0),F(0)))
    def test_nonzero_angular_readings_not_assumed_zero(self):
        a=angular_history()
        self.assertEqual(a[31][1],F(1,25))
        self.assertEqual(a[33][1],-F(1,25))
    def test_exact_cancel_bound(self):
        self.assertLess(T*F(1,1250),R)
    def test_history(self):
        self.assertEqual(tuple(k for k in (35,40,45) if k in SUCCESS),(45,))
        self.assertEqual(tuple(k for k in (50,55) if k in MISS),(50,55))
    def test_lower_bound(self):
        self.assertEqual(F(certificate()['post_success_velocity_diameter_lower_bound_m_s']),F(22724681,40000000))
    def test_not_smm(self):
        self.assertIn('not SMM',certificate()['claim'])
    def test_exact_displacement(self):
        self.assertEqual(H*H*R*F(7*6,2),F(68174043,4000000000))

if __name__=='__main__':unittest.main()
