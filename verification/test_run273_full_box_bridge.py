import unittest
from fractions import Fraction as F
from check_run273_full_box_bridge import H, R, BOX, outer_abs, packet_patterns, certify

class Run273Tests(unittest.TestCase):
    def test_packet_modes(self):
        self.assertEqual(len(packet_patterns()), 7)
    def test_initial_bounds(self):
        for key in BOX:
            self.assertEqual(outer_abs(key, 0)['v'], BOX[key]['v'])
    def test_monotone_envelope(self):
        for key in BOX:
            for axis in ('p','v','phi'):
                seq=[outer_abs(key,q)[axis] for q in range(16)]
                self.assertTrue(all(a<=b for a,b in zip(seq,seq[1:])))
    def test_exact_smm_terminal(self):
        self.assertEqual(outer_abs('SMM',15)['v'], F(22047167311,10000000000))
        self.assertEqual(outer_abs('SMM',15)['p'], F(109170729653,100000000000))
    def test_exact_mms_terminal(self):
        self.assertEqual(outer_abs('MMS',15)['v'], F(216236297,125000000))
        self.assertEqual(outer_abs('MMS',15)['p'], F(6643635767,10000000000))
    def test_full_box_hard_safety(self):
        for key in BOX:
            for q in range(16):
                x=outer_abs(key,q)
                self.assertLess(x['v'],3)
                self.assertLess(x['p'],5)
                self.assertLess(x['phi'],F(9,20))
    def test_actual_zero_torque_failure(self):
        self.assertLess(73*H*R,3)
        self.assertGreater(74*H*R,3)
    def test_certificate(self):
        self.assertEqual(certify()['gate_A'],'blocked')
        self.assertTrue(certify()['branches']['SMM']['all_16_ticks_hard_safe'])

if __name__=='__main__':
    unittest.main()
