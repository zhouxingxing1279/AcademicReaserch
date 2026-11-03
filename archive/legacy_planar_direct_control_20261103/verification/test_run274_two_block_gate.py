"""Run274 isolated exact-rational regression checks."""
import unittest
from fractions import Fraction as F
from check_run274_two_block_gate import A,W,H,T,R,BOX,bound,safe,modes,certify

class TwoBlockGateTests(unittest.TestCase):
    def test_packet_modes(self):
        self.assertEqual(len(modes(3)),7)
        self.assertEqual(len(modes(6)),44)
        self.assertTrue(all('MMM' not in s for s in modes(6)))
    def test_old_tick75_exact(self):
        self.assertEqual(bound(15,BOX['SMM']['p'],BOX['SMM']['v'])['v'],F(22047167311,10000000000))
        self.assertEqual(bound(15,BOX['MMS']['p'],BOX['MMS']['v'])['p'],F(6643635767,10000000000))
    def test_all_two_blocks(self):
        for name, b in BOX.items():
            self.assertTrue(all(safe(bound(q,b['p'],b['v'])) for q in range(31)),name)
    def test_tick90_bounds(self):
        self.assertEqual(bound(30,BOX['SMM']['p'],BOX['SMM']['v'])['v'],F(7124766859,2500000000))
        self.assertEqual(bound(30,BOX['MMS']['p'],BOX['MMS']['v'])['phi'],F(7,500))
    def test_first_envelope_failure(self):
        for name,q in [('SMM',33),('MMS',44)]:
            b=BOX[name]
            self.assertTrue(safe(bound(q,b['p'],b['v'])))
            self.assertFalse(safe(bound(q+1,b['p'],b['v'])))
    def test_gate(self):
        a90=A+30*H*W
        extra=bound(15,F(0),F(0),a=a90)['v']
        self.assertEqual(F(3)-extra,F(187678479,80000000))
    def test_gate_sufficiency_and_failure_of_unconditional(self):
        data=certify()
        for name in BOX:
            b=data['branches'][name]
            self.assertFalse(b['unconditional_tick90_box_meets_gate'])
            self.assertLessEqual(F(b['tick105_bound_if_gate_met']['p']),5)
            self.assertEqual(F(b['tick105_bound_if_gate_met']['v']),3)
    def test_global_sine_bound_is_analytic(self):
        for name,b in BOX.items():
            self.assertEqual(bound(0,b['p'],b['v'])['p'],b['p'])
            self.assertTrue(all(bound(q+1,b['p'],b['v'])['v']>=bound(q,b['p'],b['v'])['v'] for q in range(45)))

if __name__=='__main__': unittest.main()
