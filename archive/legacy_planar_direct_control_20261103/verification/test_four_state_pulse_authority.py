"""Run244 exact arithmetic tests for an admissible pulse-family obstruction."""
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_pulse_authority as m

class PulseAuthorityTests(unittest.TestCase):
    def test_attitude_reset_and_sign(self):
        a=m.attitude_response()
        self.assertEqual(len(a),15)
        self.assertTrue(all(x>=0 for x in a))
        self.assertEqual(sum(a),F(27,25))
        self.assertEqual(max(a),F(9,50))

    def test_disturbance_is_exact_config_formula(self):
        self.assertEqual(m.R,F(3246383,1600000))

    def test_max_velocity_correction(self):
        self.assertEqual(m.per_pulse_correction_bound(),F(26487,1562500))

    def test_modes_are_selected_successes_on_valid_opportunities(self):
        for n in m.FREE_TICKS:
            self.assertEqual((15+n)%5,0)
            self.assertLessEqual(0,m.MAX_MISSES)

    def test_exact_cycle_bounds(self):
        self.assertEqual([m.per_cycle_lower_bound(n) for n in m.FREE_TICKS],
                         [F(79464407,100000000),F(399017203,400000000),F(240088389,200000000)])

    def test_first_certified_violation_cycle(self):
        self.assertEqual([m.first_certified_violation_cycles(n) for n in m.FREE_TICKS],[4,4,3])
        for n in m.FREE_TICKS:
            k=m.first_certified_violation_cycles(n);d=m.per_cycle_lower_bound(n)
            self.assertLessEqual((k-1)*d,m.V_MAX)
            self.assertGreater(k*d,m.V_MAX)

    def test_margins_positive(self):
        self.assertEqual([m.first_certified_violation_cycles(n)*m.per_cycle_lower_bound(n)-m.V_MAX
                          for n in m.FREE_TICKS],
                         [F(4464407,25000000),F(99017203,100000000),F(120265167,200000000)])

    def test_not_general_no_go(self):
        s=m.verify()
        self.assertFalse(s['general_output_feedback_infeasible'])
        self.assertFalse(s['smf_mpc_recursive_feasibility_proved'])
        self.assertFalse(s['all_legal_packet_patterns_robust_safety_for_this_pulse_family'])

    def test_numerical_sanity_matches_strict_lower_bound(self):
        for n in m.FREE_TICKS:
            sim=m.numerical_witness(n)
            self.assertIsNotNone(sim["first_velocity_violation_tick"])
            self.assertLessEqual(sim["first_velocity_violation_tick"],sim["ticks"])
            self.assertGreater(sim["final_v_m_s"],float(m.first_certified_violation_cycles(n)*m.per_cycle_lower_bound(n)))

    def test_reject_unsupported_mode(self):
        with self.assertRaises(ValueError):m.per_cycle_lower_bound(0)

    def test_real_repo_configuration(self):
        root=Path(__file__).resolve().parent.parent
        if not (root/'configs/planar_baseline.json').exists():
            self.skipTest('full repository configuration not present in isolated run')
        self.assertEqual(m.verify(root)['run'],244)

if __name__=='__main__':unittest.main()
