"""Run241 exact-rational shared-information recovery tests."""
import unittest
import math
from fractions import Fraction as F
from pathlib import Path
import check_four_state_observation_pulse as m

class ObservationPulseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=m.verify()

    def test_profile_restarts_attitude(self):
        p,w=m.angle_coefficients()
        self.assertEqual((p[-1],w[-1]),(0,0))
        self.assertEqual(max(p),F(3,25))
        self.assertEqual(max(w),F(2))

    def test_exact_model_contract(self):
        self.assertEqual(m.H/m.J,1)
        self.assertEqual(m.R,F(3246383,1600000))
        self.assertEqual(m.D,F(1742383,800000))

    def test_modes_and_noisy_observation_bounds(self):
        self.assertEqual([x['packet_after_ticks'] for x in self.result['modes']],[5,10,15])
        for n in m.MODES:
            gs=m.prior_generators(n)
            self.assertEqual(m.bounds(n,15)['y_abs'],sum(p for p,v in gs)+m.NOISE)

    def test_exact_all_tick_safety(self):
        for n in m.MODES:
            for t in range(16):
                a=m.bounds(n,t)
                self.assertLess(a['safe_p'],m.LIMITS[0])
                self.assertLess(a['safe_v'],m.LIMITS[1])
                self.assertLess(a['phi'],m.LIMITS[2])
                self.assertLess(a['omega'],m.LIMITS[3])
                self.assertLessEqual(a['torque'],m.TAU_MAX)

    def test_strict_terminal_improvement_only_10_15(self):
        for n in m.MODES:
            a=m.bounds(n,15)
            self.assertEqual(a['pulse_p']<a['baseline_p'],n in (10,15))
            self.assertEqual(a['pulse_v']<a['baseline_v'],n in (10,15))

    def test_noise_5_tick_negative_result(self):
        a=m.bounds(5,15)
        self.assertGreater(a['pulse_p'],a['baseline_p'])
        self.assertGreater(a['pulse_v'],a['baseline_v'])

    def test_remainder_is_nonnegative_and_small(self):
        for n in m.MODES:
            a=m.bounds(n,15)
            self.assertGreaterEqual(a['taylor_p'],0)
            self.assertGreaterEqual(a['taylor_v'],0)
            self.assertLess(a['taylor_v'],F(1,1000000))

    def test_causality_and_nonzero_torque(self):
        self.assertNotEqual(m.SHAPE[0],0)
        self.assertEqual(sum(m.SHAPE),0)
        self.assertLess(m.GAIN*m.bounds(15,15)['y_abs'],m.TAU_MAX)
        self.assertFalse(self.result['recursive_invariance_certified'])
        self.assertFalse(self.result['smf_mpc_closed_loop_certified'])

    def test_invalid_modes_and_horizons(self):
        with self.assertRaises(ValueError):m.prior_generators(7)
        with self.assertRaises(ValueError):m.bounds(15,16)

    def test_independent_euler_extreme_trajectories(self):
        # Floating-point sanity check independent of support/Taylor derivation;
        # NOT used as a mathematical proof.
        for n in m.MODES:
            for initial_sign in (-1,1):
                p,v,phi,omega=0.0,float(initial_sign*m.H*m.D),0.0,0.0
                for _ in range(n):
                    p,v=p+float(m.H)*v,v+float(m.H)*float(initial_sign*m.R)
                y=p+float(initial_sign*m.NOISE)
                for future_sign in (-1,1):
                    x=(p,v,phi,omega)
                    for t,a in enumerate(m.SHAPE):
                        p0,v0,ph0,om0=x
                        torque=float(m.GAIN)*y*a
                        x=(p0+float(m.H)*v0,
                           v0+float(m.H)*(-float(m.T)*math.sin(ph0)+future_sign*float(m.R)),
                           ph0+float(m.H)*om0,
                           om0+float(m.H/m.J)*torque)
                        bound=m.bounds(n,t+1)
                        self.assertLessEqual(abs(x[0]),float(bound['pulse_p'])+1e-10)
                        self.assertLessEqual(abs(x[1]),float(bound['pulse_v'])+1e-10)
                        self.assertLessEqual(abs(x[2]),float(bound['phi'])+1e-10)
                        self.assertLessEqual(abs(x[3]),float(bound['omega'])+1e-10)

    def test_full_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertEqual(m.verify(root),self.result)
        else:self.skipTest('requires complete repository checkout')

if __name__=='__main__':unittest.main()
