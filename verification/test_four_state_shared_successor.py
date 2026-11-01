"""Run237 exact support separation and scope regression."""
import unittest
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_shared_successor as m
import check_four_state_finite_rpi as rpi

class SharedSuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.c=m.certificate()
    def test_gap(self): self.assertEqual(self.c['strict_gap_lower'],'181/10000')
    def test_finite_generator_count(self): self.assertEqual(self.c['finite_generators'],4000)
    def test_common_observation(self):
        x=rpi.D*rpi.H
        self.assertGreater(x,0)
        self.assertLess(x,Q(1,10))
    def test_disturbance_is_legal(self): self.assertLess(rpi.R,rpi.D)
    def test_symmetric_fiber_contradiction(self): self.assertFalse(self.c['shared_torque_feasible'])
    def test_support_direction(self): self.assertEqual(tuple(map(Q,self.c['normal'])),m.ELL)
    def test_nonclaim(self): self.assertIn('not every SMF posterior',self.c['limitations'][0])
    def test_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertEqual(m.certificate(root),self.c)
        else: self.skipTest('requires full checkout; CI must verify')

if __name__=='__main__': unittest.main()
