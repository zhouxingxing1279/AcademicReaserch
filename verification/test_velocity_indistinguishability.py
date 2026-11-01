#!/usr/bin/env python3
"""Run251 exact certificate unit tests, no third-party dependencies."""
import unittest
from pathlib import Path
from fractions import Fraction as F
from check_velocity_indistinguishability import (
    H, R, POSITION_NOISE, lateral_witness, optimum_deltas, verify)


class IndistinguishableVelocityTest(unittest.TestCase):
    def test_primal_dual_equality(self):
        for n in (5, 10, 15):
            pivot, d, primal, dual = optimum_deltas(n)
            self.assertEqual(primal, dual)
            self.assertEqual(sum(w * v for w, v in d.items()), 0)
            self.assertTrue(all(abs(v) <= 1 for v in d.values()))
            self.assertEqual(dual, sum(abs(1-F(w, pivot)) for w in range(n)))

    def test_fifteen_tick_optimum(self):
        pivot, d, primal, dual = optimum_deltas(15)
        self.assertEqual((pivot, primal, dual), (10, F(13, 2), F(13, 2)))
        self.assertEqual(d[10], F(1, 2))
        self.assertEqual([d[w] for w in range(11, 15)], [F(-1)] * 4)

    def test_indistinguishable_all_packets_success(self):
        for n in (5, 10, 15):
            case = lateral_witness(n)
            self.assertTrue(all(v <= POSITION_NOISE for v in case['observed_half_separation'].values()))
            self.assertEqual(case['records'][-1][1:3], (F(0), F(0)))
            self.assertTrue(all(abs(rec[1]) <= 5 and abs(rec[3]) <= 3 for rec in case['records']))

    def test_velocity_gap_and_halfwidth(self):
        case = lateral_witness(15)
        self.assertEqual(case['terminal_velocity_gap'], 13*H*R)
        self.assertEqual(case['terminal_velocity_gap'], F(42202979, 80000000))
        self.assertEqual(case['necessary_posterior_halfwidth'], F(42202979, 160000000))

    def test_causal_angle_independence(self):
        # Lateral residual does not enter phi/omega, so any shared legal torque
        # sequence gives identical angular histories. With fixed T the common
        # lateral -T*sin(phi) cancels from differences in p and v.
        case = lateral_witness(15)
        for _, pp, pm, vp, vm in case['records']:
            self.assertEqual(pp, -pm)
            self.assertEqual(vp, -vm)

    def test_run249_interval_smf_contains_both_histories(self):
        # Full-repository integration: actual Run249 SMF under one shared
        # observation word (all position packets succeed, readings zero).
        try:
            import check_four_state_shielded_smf_mpc as prior
        except ImportError:
            self.skipTest('Run249 source unavailable in isolated local checkout')
        self.assertEqual((prior.H, prior.R, prior.T), (H, R, F(981, 100)))
        s = dict(prior.INIT)
        for tick in range(1, 16):
            s = prior.step(s, F(0))
            obs = {'phi': F(0), 'omega': F(0)}
            if tick % 5 == 0:
                obs['p'] = F(0)
            s = prior.strip(s, obs)
            self.assertIsNotNone(s)
        half = lateral_witness(15)['necessary_posterior_halfwidth']
        self.assertLessEqual(s['v'][0], -half)
        self.assertGreaterEqual(s['v'][1], half)
        self.assertTrue(prior.safe(s))

    def test_json_claim_scope(self):
        obj = verify()
        self.assertEqual(obj['run'], 251)
        self.assertFalse(obj['recursive_feasibility_proved'])
        self.assertFalse(obj['terminal_invariant_set_proved'])
        self.assertEqual(obj['gate_A'], 'blocked')
        self.assertEqual(len(obj['certificates']), 3)


if __name__ == '__main__':
    unittest.main()
