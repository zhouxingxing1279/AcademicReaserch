"""Run243 exact rational Schur + two-packet SMF radius regressions."""
import math
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_posterior_damping as m


class PosteriorDampingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=m.verify()

    def test_attitude_reset_and_shape(self):
        a,w=m.response_per_unit()
        self.assertEqual(len(a),15)
        self.assertEqual(max(map(abs,a)),F(9,50))
        self.assertEqual(max(map(abs,w)),F(3))
        self.assertEqual(sum(m.SHAPE),0)

    def test_pulse_coefficients_independently(self):
        al,be=m.response_coefficients()
        self.assertEqual(al,F(26487,125000))
        self.assertEqual(be,F(79461,2500000))
        self.assertEqual(15*m.H*al,2*be)

    def test_exact_jury_margins_all_modes(self):
        for n in m.MODES:
            a,b,c=m.jury(n)
            self.assertGreater(a,0)
            self.assertGreater(b,0)
            self.assertGreater(c,0)
            self.assertEqual(m.det2(m.macro_jacobian(n)),F(4549721,5000000))

    def test_old_no_velocity_feedback_is_not_schur(self):
        al,be=m.response_coefficients()
        old_gain=F(2,3)
        det=1+be*old_gain # velocity gain b=0
        self.assertGreater(det,1)

    def test_exact_velocity_radius_modes(self):
        self.assertEqual([m.velocity_radius(n+15) for n in m.MODES],
            [F(84174043,160000000),F(48602979,80000000),F(333913619,480000000)])
        self.assertLess(m.velocity_radius(20),m.velocity_radius(25))
        self.assertLess(m.velocity_radius(25),m.velocity_radius(30))

    def test_two_packet_interval_sharp_extremal(self):
        for N in (20,25,30):
            p=F(1,100);v=F(1,20)
            old=p+m.NOISE
            acc=[F(0)]*N
            for j in range(N):
                p,v=p+m.H*v,v+m.H*m.R
            new=p-m.NOISE
            est=m.reconstruct_velocity(old,new,acc)
            self.assertEqual(v-est,m.velocity_radius(N))

    def test_alternating_disturbance_and_noise_contains(self):
        for N in (20,25,30):
            p=F(1,100);v=F(1,20)
            old=p-m.NOISE
            acc=[F(0)]*N
            for j in range(N):
                r=m.R if j%2 else -m.R
                p,v=p+m.H*v,v+m.H*r
            new=p+m.NOISE
            est=m.reconstruct_velocity(old,new,acc)
            self.assertLessEqual(abs(v-est),m.velocity_radius(N))

    def test_known_attitude_acceleration_is_causal(self):
        for n in m.MODES:
            acc=m.known_accelerations(F(1,100),n)
            self.assertEqual(len(acc),15+n)
            self.assertTrue(all(math.isfinite(x) for x in acc))
            self.assertAlmostEqual(acc[0],0.0)

    def test_local_input_and_state_one_macro(self):
        x=self.result
        self.assertEqual(F(x['local_unsaturated_torque_bound_Nm']),F(3,40))
        self.assertLess(F(x['local_unsaturated_torque_bound_Nm']),m.TAU_MAX)
        s=x['local_one_macro_state_bounds']
        self.assertLess(F(s['p_m']),5)
        self.assertLess(F(s['v_m_s']),3)
        self.assertLess(F(s['phi_rad']),F(9,20))
        self.assertLess(F(s['omega_rad_s']),2)

    def test_deterministic_causal_closed_loop(self):
        sim=m.simulate_zero_noise()
        self.assertEqual(sim['cycles'],75)
        self.assertLess(sim['max_velocity_reconstruction_error'],1e-10)
        self.assertLess(sim['max_torque'],float(m.TAU_MAX))
        self.assertLess(abs(sim['final_p']),0.01)
        self.assertLess(abs(sim['final_v']),0.01)
        self.assertLess(sim['max_p'],5)
        self.assertLess(sim['max_v'],3)

    def test_scope_flags(self):
        x=self.result
        self.assertTrue(x['fixed_mode_local_schur_certified'])
        self.assertFalse(x['arbitrary_switching_schur_certified'])
        self.assertFalse(x['robust_input_and_state_invariance_certified'])
        self.assertFalse(x['full_smf_mpc_closed_loop_certified'])

    def test_invalid_gap_and_mode(self):
        with self.assertRaises(ValueError):m.velocity_radius(0)
        with self.assertRaises(ValueError):m.velocity_radius(3.5)
        with self.assertRaises(ValueError):m.macro_jacobian(7)
        with self.assertRaises(ValueError):m.reconstruct_velocity(0,1,[])

    def test_full_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertEqual(m.verify(root),self.result)
        else:self.skipTest('requires complete repository checkout')

if __name__=='__main__':unittest.main()
