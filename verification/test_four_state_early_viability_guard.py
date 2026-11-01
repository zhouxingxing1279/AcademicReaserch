"""Run247: two-sided necessary viability guard and early intervention tests."""
import json
import math
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_early_viability_guard as m

class EarlyViabilityGuardTests(unittest.TestCase):
    def test_parameters(self):
        self.assertEqual(m.R, F(3246383, 1600000))
        self.assertEqual(len(m.TORQUES), 30)
        self.assertEqual(m.INITIAL, (F(-1,50),F(-1,10),F(-1,200),F(-1,100)))

    def test_euler_timing(self):
        self.assertEqual(m.pitch_envelope(F(1,10),F(1,20),1), (F(101,1000),)*2)
        lo, hi = m.pitch_envelope(F(0),F(0),2)
        self.assertEqual((lo,hi),(-m.H*m.U,m.H*m.U))

    def test_sine_enclosure_sanity_not_proof(self):
        for i in range(-45,46):
            x = F(i,100)
            lo,hi = m.sin_bounds(x)
            self.assertLessEqual(float(lo)-1e-15, math.sin(float(x)))
            self.assertGreaterEqual(float(hi)+1e-15, math.sin(float(x)))

    def test_prefix_safety(self):
        for p,v,phi,omega in m.reachable_corner():
            self.assertLess(max(map(abs,p)),m.P_MAX)
            self.assertLess(max(map(abs,v)),m.V_MAX)
            self.assertLess(abs(phi),m.PHI_MAX)
            self.assertLess(abs(omega),m.OMEGA_MAX)

    def test_two_sided_hover_guard(self):
        lo,hi = m.necessary_velocity_guard(F(0),F(0),13)
        self.assertLess(lo,0)
        self.assertGreater(hi,0)
        self.assertEqual(lo,-hi)

    def test_first_strict_rejection_at_tick26(self):
        self.assertEqual(m.first_rejection(m.reachable_corner())[:3],(26,20,'negative'))
        for k in range(26):
            self.assertIsNone(m.first_rejection(m.reachable_corner()[:k+1]))

    def test_strict_unavoidable_negative_violation(self):
        a = m.verify()
        self.assertLess(F(a['strict_velocity_upper_bound_at_tick46']),-3)
        self.assertGreater(F(a['strict_negative_violation_margin_m_s']),0)
        self.assertLess(F(a['tick26_velocity_enclosure'][1]),F(a['necessary_velocity_floor_at_tick26']))

    def test_symmetric_guard_formula(self):
        lo,hi=m.necessary_velocity_guard(F(0),F(0),7)
        self.assertEqual(lo,-hi)
        self.assertLess(lo,hi)

    def test_scope_and_non_claims(self):
        a=m.verify()
        self.assertFalse(a['guard_is_sufficient_for_viability'])
        self.assertFalse(a['guard_on_outer_SMF_can_prove_true_posterior_infeasible'])
        self.assertFalse(a['shared_causal_feedback_synthesized'])
        self.assertFalse(a['recursive_feasibility_proved'])

    def test_archive_in_full_checkout(self):
        root=Path(__file__).resolve().parent.parent
        f=root/'results/four_state_early_viability_guard_20261101/checks.json'
        if not f.exists(): self.skipTest('archive unavailable in isolation')
        self.assertEqual(json.loads(f.read_text()),m.verify())

    def test_config_in_full_checkout(self):
        root=Path(__file__).resolve().parent.parent
        if not (root/'configs/planar_baseline.json').exists():
            self.skipTest('full checkout unavailable')
        self.assertEqual(m.verify(root)['run'],247)

if __name__=='__main__':unittest.main()
