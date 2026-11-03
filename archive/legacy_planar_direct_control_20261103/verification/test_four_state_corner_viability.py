"""Run248: independent full-information no-return witness regression."""
import json
import math
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_corner_viability as m


class CornerViabilityTests(unittest.TestCase):
    def test_initial_corner_is_valid(self):
        self.assertEqual(m.INITIAL, (F(-1,50),F(-1,10),F(1,200),F(1,100)))
        self.assertEqual(m.R,F(3246383,1600000))

    def test_prefix_matches_run245(self):
        self.assertEqual(len(m.PREFIX),30)
        self.assertEqual(m.PREFIX[:12],(m.U,)*12)
        self.assertEqual(m.PREFIX[12:24],(-m.U,)*12)

    def test_euler_causal_index(self):
        self.assertEqual(m.extremal_pitch(F(0),F(0),0),0)
        self.assertEqual(m.extremal_pitch(F(0),F(0),1),0)
        self.assertEqual(m.extremal_pitch(F(0),F(0),2),-m.H*m.U)

    def test_exact_prefix_state_safety(self):
        for p,v,phi,omega in m.reachable_corner():
            self.assertLess(max(map(abs,p)),m.prior.P_MAX)
            self.assertLess(max(map(abs,v)),m.V_MAX)
            self.assertLess(abs(phi),m.PHI_MAX)
            self.assertLess(abs(omega),m.prior.OMEGA_MAX)

    def test_first_rejection_in_bounded_scan(self):
        rows=m.reachable_corner()
        self.assertEqual(m.first_rejection(rows)[:2],(14,30))
        self.assertIsNone(m.first_rejection(rows[:14]))

    def test_optimistic_full_state_extremal_path(self):
        rows=m.reachable_corner()
        bound,lo,hi=m.full_information_negative_witness(rows,14,30)
        self.assertGreater(lo,-m.PHI_MAX)
        self.assertLess(hi,m.PHI_MAX)
        self.assertLess(bound,-m.V_MAX)

    def test_guard_matches_direct_extremal_sum(self):
        rows=m.reachable_corner()
        _,v,phi,omega=rows[14]
        bound,_,_=m.full_information_negative_witness(rows,14,30)
        floor,_=m.prior.necessary_velocity_guard(phi,omega,30)
        self.assertEqual(bound,v[1]-floor-m.V_MAX)

    def test_sine_bounds_numerical_sanity_only(self):
        for i in range(-45,46):
            x=F(i,100)
            lo,hi=m.prior.sin_bounds(x)
            self.assertLessEqual(float(lo)-1e-15,math.sin(float(x)))
            self.assertGreaterEqual(float(hi)+1e-15,math.sin(float(x)))

    def test_certificate_and_scope(self):
        result=m.verify()
        self.assertEqual(result['unavoidable_velocity_violation_by_tick'],44)
        self.assertGreater(F(result['strict_negative_violation_margin_m_s']),0)
        self.assertFalse(result['earliest_true_nonviability_time_proved'])
        self.assertFalse(result['smf_posterior_tested'])
        self.assertFalse(result['recursive_feasibility_proved'])

    def test_archive_in_full_checkout(self):
        root=Path(__file__).resolve().parent.parent
        file=root/'results/four_state_corner_viability_20261101/checks.json'
        if not file.exists(): self.skipTest('full checkout archive unavailable')
        self.assertEqual(json.loads(file.read_text()),m.verify())

    def test_config_in_full_checkout(self):
        root=Path(__file__).resolve().parent.parent
        if not (root/'configs/planar_baseline.json').exists():
            self.skipTest('full checkout config unavailable')
        self.assertEqual(m.verify(root)['run'],248)

if __name__=='__main__': unittest.main()
