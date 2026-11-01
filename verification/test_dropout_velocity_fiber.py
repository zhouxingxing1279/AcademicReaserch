#!/usr/bin/env python3
"""Run252 exact rational two-miss information-state necessary bound tests."""
import unittest
from fractions import Fraction as F
from check_dropout_velocity_fiber import H, R, U, envelope, velocity_gap, verify
from check_velocity_indistinguishability import lateral_witness


class TwoMissVelocityFiberTests(unittest.TestCase):
    def test_run251_witness_has_common_readings(self):
        w = lateral_witness(15)
        self.assertEqual(w['records'][-1][1:3], (F(0), F(0)))
        self.assertTrue(all(v <= F(1, 50) for v in w['observed_half_separation'].values()))

    def test_exact_diameter_at_20(self):
        self.assertEqual(velocity_gap(5), F(74666809, 80000000))

    def test_exact_diameter_at_25(self):
        self.assertEqual(velocity_gap(10), F(107130639, 80000000))

    def test_growth_per_tick_is_control_independent(self):
        for j in range(10):
            self.assertEqual(velocity_gap(j + 1) - velocity_gap(j), 2 * H * R)

    def test_every_intermediate_state_has_strict_safety_margin(self):
        for j in range(11):
            e = envelope(j)
            for k, limit in [('p', F(5)), ('v', F(3)), ('phi', F(9,20)), ('omega', F(2))]:
                self.assertLess(e[k], limit, (j, k))

    def test_angular_envelope_includes_all_legal_nonzero_torques(self):
        self.assertEqual(envelope(10)['omega'], 10 * U)
        self.assertEqual(envelope(10)['phi'], F(9,125))
        self.assertEqual(envelope(10)['v'], F(113157903,160000000))

    def test_scope_not_overstated(self):
        obj = verify()
        self.assertEqual(obj['dropout_word_at_position_opportunities'], 'SSSMM')
        self.assertFalse(obj['terminal_invariant_set_proved'])
        self.assertFalse(obj['recursive_feasibility_proved'])
        self.assertIn('continuation', obj['quantifiers'])
        self.assertEqual(obj['gate_A'], 'blocked')

    def test_run249_constants_agree_when_available(self):
        try:
            import check_four_state_shielded_smf_mpc as prior
        except ImportError:
            self.skipTest('Run249 module unavailable outside full repository checkout')
        self.assertEqual((prior.H, prior.R, prior.U), (H, R, U))
        self.assertEqual(prior.NOISE['p'], F(1, 50))


if __name__ == '__main__':
    unittest.main()
