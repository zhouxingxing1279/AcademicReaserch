"""Run232: exact rational all-control bridge obstruction regression tests."""
import unittest
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_bridge_multistep_obstruction as m
import check_four_state_bridge_graph as plant

class MultiStepBridgeTests(unittest.TestCase):
    def test_tilt_envelope_exact_and_mode_gap(self):
        self.assertEqual(m.tilt_envelope(0),0)
        self.assertEqual(m.tilt_envelope(1),0)
        self.assertEqual(m.tilt_envelope(2),Q(1,625))
        self.assertEqual(m.tilt_envelope(14),Q(91,625))
        self.assertLess(m.tilt_envelope(14),Q(3,20))

    def test_two_step_unavoidable_residual(self):
        d=m.adversarial_velocity_envelope(2)
        self.assertEqual(d['velocity_lower'],2*plant.H*(plant.R0+plant.RT*plant.TMIN))
        self.assertEqual(d['velocity_lower'],Q(6254383,80000000))

    def test_fourteen_step_all_control_lower_bound(self):
        d=m.adversarial_velocity_envelope()
        self.assertEqual(len(d['rows']),14)
        self.assertTrue(all(Q(r['acceleration_lower'])>0 for r in d['rows']))
        self.assertGreater(d['velocity_lower'],Q(2,5))
        self.assertLess(d['velocity_lower'],Q(41,100))

    def test_run228_expanded_bridge_strictly_excluded(self):
        d=m.bridge_obstruction(Q(1,20))
        self.assertTrue(d['strict_noninvariance'])
        self.assertEqual(d['first_forced_velocity_exit_tick'],2)

    def test_bridge_threshold_is_only_necessary(self):
        self.assertEqual(m.bridge_obstruction(Q(2,5))['first_forced_velocity_exit_tick'],13)
        self.assertFalse(m.bridge_obstruction(Q(41,100))['strict_noninvariance'])

    def test_invalid_inputs(self):
        for value in [0,Q(31,10)]:
            with self.assertRaises(ValueError):m.bridge_obstruction(value)
        for n in [0,15,1.5]:
            with self.assertRaises(ValueError):m.adversarial_velocity_envelope(n)

    def test_output_contract(self):
        d=m.verify()
        self.assertEqual(d['gate_A'],'blocked')
        self.assertEqual(d['horizon'],14)
        self.assertEqual(d['cases']['run228_narrow']['first_forced_velocity_exit_tick'],1)

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(plant.config_contract(root))
        else:self.skipTest('requires full checkout; GitHub Actions must verify')

if __name__=='__main__':unittest.main()
