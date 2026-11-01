"""Run245 finite-horizon shared tilt/SMF gate; exact arithmetic checks."""
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_tilt_authority as m

class TiltAuthorityTests(unittest.TestCase):
    def test_configured_disturbance(self):
        self.assertEqual(m.R,F(3246383,1600000))

    def test_sine_bounds_and_symmetry(self):
        for x in [F(0),F(1,100),F(1,5),F(45,100)]:
            lo,hi=m.sin_bounds(x)
            self.assertLessEqual(lo,hi)
            self.assertLessEqual(float(lo)-1e-15,__import__('math').sin(float(x)))
            self.assertGreaterEqual(float(hi)+1e-15,__import__('math').sin(float(x)))
            self.assertEqual(m.sin_bounds(-x),(-hi,-lo))

    def test_ramp_and_hold_schedule(self):
        self.assertEqual(len(m.TORQUES),30)
        self.assertEqual(m.TORQUES[:12],(m.TAU_MAX,)*12)
        self.assertEqual(m.TORQUES[12:24],(-m.TAU_MAX,)*12)
        self.assertEqual(m.TORQUES[24:],(F(0),)*6)

    def test_initial_full_prior_and_angle_endpoint(self):
        rows=m.envelope()
        self.assertEqual(rows[0]['bounds'],m.INIT)
        self.assertEqual(rows[24]['bounds']['phi'],(F(1103,5000),F(1201,5000)))
        self.assertEqual(rows[24]['bounds']['omega'],(F(-1,100),F(1,100)))

    def test_all_intermediate_constraints(self):
        for row in m.envelope():
            b=row['bounds']
            for key,lim in [('p',m.P_MAX),('v',m.V_MAX),('phi',m.PHI_MAX),('omega',m.OMEGA_MAX)]:
                self.assertLess(max(abs(x) for x in b[key]),lim)

    def test_adverse_positive_acceleration_reversed(self):
        rows=m.envelope()
        for row in rows[24:]:
            self.assertGreater(m.T*m.sin_bounds(row['bounds']['phi'][0])[0],m.R)

    def test_negative_residual_tradeoff_preserved(self):
        result=m.verify()
        self.assertGreater(F(result['positive_velocity_upper_improvement_vs_zero_torque_at_tick30_m_s']),0)
        self.assertGreater(F(result['worst_absolute_velocity_tilt_at_tick30_m_s']),F(result['worst_absolute_velocity_zero_torque_at_tick30_m_s']))

    def test_legal_packet_words(self):
        words=m.packet_paths()
        self.assertEqual(len(words),44)
        self.assertIn('SMMSSS',words)
        self.assertIn('SSSSSS',words)
        self.assertNotIn('MMMMMM',words)
        self.assertTrue(all('MMM' not in w for w in words))

    def test_measurement_intersection_and_miss(self):
        prior={'p':(F(-1),F(1)),'v':(F(-2),F(2))}
        self.assertEqual(m.measurement_update(prior,{}),prior)
        post=m.measurement_update(prior,{'p':(F(0),F(1,50))})
        self.assertEqual(post['p'],(F(-1,50),F(1,50)))
        self.assertEqual(post['v'],prior['v'])
        self.assertIsNone(m.measurement_update(prior,{'p':(F(2),F(1,50))}))

    def test_float_sanity_not_proof(self):
        for word in ['SSSSSS','SMMSSS','MSMSSM']:
            s=m.float_sanity(word)
            self.assertEqual(s['pattern'],word)

    def test_evidence_flags(self):
        s=m.verify()
        self.assertTrue(s['finite_horizon_robust_state_and_input_constraints'])
        self.assertFalse(s['robust_recursive_feasibility_proved'])
        self.assertFalse(s['mpc_optimization_implemented'])
        self.assertFalse(s['six_state_safety_proved'])

    def test_real_repository_config(self):
        root=Path(__file__).resolve().parent.parent
        if not (root/'configs/planar_baseline.json').exists():
            self.skipTest('full repository config unavailable in isolated execution')
        self.assertEqual(m.verify(root)['run'],245)

if __name__=='__main__':unittest.main()
