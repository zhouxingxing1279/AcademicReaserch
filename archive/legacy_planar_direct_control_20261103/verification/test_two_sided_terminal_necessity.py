"""Run223 exact-rational necessary-condition tests; no RCI sufficiency claim."""
import math
import unittest
from fractions import Fraction as Q
from pathlib import Path

import check_two_sided_terminal_necessity as m

class TwoSidedTerminalTests(unittest.TestCase):
    def test_sine_upper_sanity_and_domain(self):
        for r in (Q(0),Q(3,50),Q(7,50),Q(717,5000),Q(9,20)):
            self.assertGreaterEqual(float(m.sin_upper(r))+1e-14, math.sin(float(r)))
        with self.assertRaises(ValueError):m.sin_upper(Q(1,2))

    def test_run222_extension_and_wider_radius(self):
        self.assertGreater(m.drift_acceleration_lower(Q(3,50)),0)
        self.assertGreater(m.drift_acceleration_lower(Q(7,50)),0)
        self.assertGreater(m.drift_acceleration_lower(Q(717,5000)),0)
        self.assertLess(m.drift_acceleration_lower(Q(3,20)),0)

    def test_exact_finite_exit_witness(self):
        for r in (Q(3,50),Q(7,50),Q(717,5000)):
            step=m.H*m.drift_acceleration_lower(r)
            n=m.first_strict_crossing_from_minus_limit(step)
            self.assertLessEqual((n-1)*step,2*m.V_LIMIT)
            self.assertGreater(n*step,2*m.V_LIMIT)
        self.assertEqual(m.first_strict_crossing_from_minus_limit(m.H*m.drift_acceleration_lower(Q(7,50))),5988)
        self.assertEqual(m.first_strict_crossing_from_minus_limit(m.H*m.drift_acceleration_lower(Q(717,5000))),519396)

    def test_two_sided_projection_and_reversal_kinematics(self):
        self.assertEqual(m.minimum_tilt_reversal_ticks(Q(717,5000)),8)
        r=m.verify()
        self.assertEqual(len(r['rows']),4)
        self.assertEqual(r['gate_A'],'blocked')
        self.assertIn('sup_C(phi)',r['necessary_projection'])

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(m.config_contract(root))
        else:
            self.skipTest('full repository checkout required; GitHub CI must run this')

if __name__=='__main__':unittest.main()
