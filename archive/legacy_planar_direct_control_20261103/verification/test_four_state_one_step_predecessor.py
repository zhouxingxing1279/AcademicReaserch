"""Run224 one-step robust predecessor tests; no RCI claim."""
import math
import unittest
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_one_step_predecessor as m

class PredecessorTests(unittest.TestCase):
    def test_sine_enclosure(self):
        for i in range(-45,46):
            p=Q(i,100)
            lo,hi=m.sine_bounds(p)
            self.assertLessEqual(float(lo)-1e-14,math.sin(float(p)))
            self.assertGreaterEqual(float(hi)+1e-14,math.sin(float(p)))
        with self.assertRaises(ValueError):m.sine_bounds(Q(1,2))

    def test_boundary_strict_exclusion(self):
        self.assertTrue(m.boundary_obstruction(Q(717,5000)))
        self.assertFalse(m.boundary_obstruction(Q(3,20)))
        self.assertGreater(m.RT+m.R0/m.TMAX-m.sine_bounds(Q(717,5000))[1],0)

    def test_both_boundary_witnesses(self):
        for s in (-1,1):
            x=(Q(0),s*m.VMAX,s*Q(3,20),Q(0))
            self.assertTrue(m.certified_predecessor(x,m.TMAX,Q(0)))
            b=m.next_bounds(x,m.TMAX,Q(0))
            self.assertGreaterEqual(b['v'][0],-m.VMAX)
            self.assertLessEqual(b['v'][1],m.VMAX)
            self.assertEqual(b['p'][0],s*Q(3,50))

    def test_false_boundary_and_bad_input(self):
        self.assertFalse(m.certified_predecessor((Q(0),m.VMAX,Q(0),Q(0)),m.TMAX,Q(0)))
        with self.assertRaises(ValueError):m.next_bounds((Q(0),)*4,m.TMAX+1,Q(0))

    def test_archived_result(self):
        data=m.verify()
        self.assertEqual(len(data['boundary_witnesses']),2)
        self.assertEqual(data['gate_A'],'blocked')

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():self.assertTrue(m.config_contract(root))
        else:self.skipTest('requires full repository checkout; run in GitHub Actions')

if __name__=='__main__':unittest.main()
