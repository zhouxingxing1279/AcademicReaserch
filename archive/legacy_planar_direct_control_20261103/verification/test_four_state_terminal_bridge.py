"""Run227 exact rational terminal geometry tests."""
import unittest
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_terminal_bridge as m

class TerminalBridgeTests(unittest.TestCase):
    def test_candidate_nonempty_both_modes(self):
        self.assertTrue(m.in_two_mode_candidate((Q(0),m.VMAX,m.A,Q(0))))
        self.assertTrue(m.in_two_mode_candidate((Q(0),-m.VMAX,-m.A,Q(0))))

    def test_one_step_counterexample_all_controls(self):
        d=m.one_step_candidate_counterexample()
        self.assertLess(Q(d['all_legal_inputs_next_v_upper']),0)
        self.assertEqual(Q(d['all_legal_inputs_next_phi']),m.A)

    def test_angular_gap_and_exact_exit(self):
        d=m.exact_bridge_obstruction()
        self.assertTrue(d['proved'])
        self.assertGreater(Q(d['forbidden_mode_gap']),Q(d['max_one_step_angle_jump']))
        n=d['latest_strict_exit_tick'];drift=Q(d['adverse_velocity_drift_per_tick_lower'])
        self.assertLessEqual((n-1)*drift,2*m.VMAX)
        self.assertGreater(n*drift,2*m.VMAX)
        self.assertEqual(n,112)

    def test_threshold_is_strict(self):
        self.assertFalse(m.exact_bridge_obstruction(m.H*m.OMAX/2)['proved'])
        self.assertTrue(m.exact_bridge_obstruction(Q(21,1000))['proved'])

    def test_no_cartesian_box(self):
        d=m.cartesian_box_obstruction()
        self.assertTrue(d['proved'])
        self.assertGreater(Q(d['min_successor_velocity_separation']),0)

    def test_archive_contract(self):
        d=m.verify()
        self.assertEqual(d['gate_A'],'blocked')
        self.assertEqual(d['no_two_disconnected_tilt_bands']['latest_strict_exit_tick'],112)
        self.assertEqual(len(d['candidate_nonempty_witnesses']),2)

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(m.config_contract(root))
        else:
            self.skipTest('requires full checkout; GitHub Actions must verify')

if __name__=='__main__':unittest.main()
