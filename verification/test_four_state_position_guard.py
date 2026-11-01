"""Run230 exact rational necessary boundary guard tests."""
import unittest
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_position_guard as m
import check_four_state_bridge_graph as prior

class PositionGuardTests(unittest.TestCase):
    def test_tilt_envelope_and_sine_domain(self):
        self.assertEqual(m.tilt_upper(0),0)
        self.assertEqual(m.tilt_upper(1),0)
        self.assertEqual(m.tilt_upper(24),Q(276,625))
        self.assertLess(m.tilt_upper(24),prior.PHIMAX)
        with self.assertRaises(ValueError):m.adversarial_acceleration_lower(25)

    def test_minimizing_thrust_switches_endpoint(self):
        self.assertEqual(m.adversarial_acceleration_lower(0)[1],prior.TMIN)
        self.assertEqual(m.adversarial_acceleration_lower(5)[1],prior.TMAX)
        for k in range(25):
            a,t=m.adversarial_acceleration_lower(k)
            s5=prior.sine_bounds(m.tilt_upper(k))[1]
            self.assertEqual(a,min(prior.R0+T*(prior.RT-s5) for T in (prior.TMIN,prior.TMAX)))

    def test_exact_displacement_and_strict_boundary(self):
        d=m.position_guard()
        self.assertEqual(d['minimum_outward_displacement'],Q(98296135986106564467,762939453125000000000))
        self.assertGreater(Q(49,10)+d['minimum_outward_displacement'],prior.PMAX)
        self.assertLess(d['positive_position_threshold'],Q(49,10))

    def test_two_step_and_monotone_first_velocity(self):
        self.assertEqual(m.position_guard(2)['minimum_outward_displacement'],prior.H**2*(prior.R0+prior.RT*prior.TMIN))
        self.assertGreater(m.position_guard(3)['minimum_outward_displacement'],m.position_guard(2)['minimum_outward_displacement'])

    def test_output_claim_not_invariance(self):
        d=m.verify()
        self.assertEqual(d['gate_A'],'blocked')
        self.assertEqual(len(d['rows']),25)
        self.assertIn('not an RCI',d['limitations'][0])
        self.assertTrue(d['negative_witness_is_sign_mirror'])

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(prior.config_contract(root))
        else: self.skipTest('requires full checkout; CI must verify')
if __name__=='__main__':unittest.main()
