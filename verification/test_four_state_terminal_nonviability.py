"""Run246 reachable nonviable terminal-state regression tests."""
import json
import math
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_terminal_nonviability as m

class TerminalNonviabilityTests(unittest.TestCase):
    def test_model_and_witness(self):
        self.assertEqual(m.R,F(3246383,1600000))
        self.assertEqual(len(m.prior.TORQUES),30)
        self.assertEqual(m.INIT,(F(-1,50),F(-1,10),F(-1,200),F(-1,100)))

    def test_exact_pitch_and_euler_indexing(self):
        rows=m.reachable_corner()
        self.assertEqual(rows[30][2:],(F(1097,5000),F(-1,100)))
        self.assertEqual(m.pitch_bounds(rows[30][2],rows[30][3],1),
                         (rows[30][2]+m.H*rows[30][3],)*2)

    def test_all_first30_states_safe(self):
        for p,v,phi,omega in m.reachable_corner():
            self.assertLess(max(map(abs,p)),m.prior.P_MAX)
            self.assertLess(max(map(abs,v)),m.prior.V_MAX)
            self.assertLess(abs(phi),m.prior.PHI_MAX)
            self.assertLess(abs(omega),m.prior.OMEGA_MAX)

    def test_future_pitch_positive_for_all_torques(self):
        _,_,phi,omega=m.reachable_corner()[30]
        for j in range(13):
            lo,hi=m.pitch_bounds(phi,omega,j)
            self.assertLess(0,lo)
            self.assertLessEqual(lo,hi)
            self.assertLess(hi,m.prior.PHI_MAX)

    def test_necessary_velocity_guard_excludes_witness(self):
        r=m.verify()
        self.assertLess(F(r['tick30_velocity_enclosure'][1]),
                        F(r['necessary_velocity_floor_at_tick30']))

    def test_any_future_torque_fails_by_tick43(self):
        r=m.verify()
        self.assertEqual(r['unavoidable_violation_tick'],43)
        self.assertLess(F(r['velocity_upper_bound_at_tick43']),-3)
        self.assertGreater(F(r['strict_velocity_violation_margin']),0)

    def test_float_full_brake_sanity_only(self):
        p,v,phi,omega=map(float,m.INIT)
        for u in m.prior.TORQUES:
            p,v,phi,omega=p+.02*v,v+.02*(-9.81*math.sin(phi)-float(m.R)),phi+.02*omega,omega+float(u)
        lo,hi=m.reachable_corner()[30][1]
        self.assertLessEqual(float(lo)-1e-12,v)
        self.assertGreaterEqual(float(hi)+1e-12,v)
        for _ in range(13):
            p,v,phi,omega=p+.02*v,v+.02*(-9.81*math.sin(phi)-float(m.R)),phi+.02*omega,omega-.08
        self.assertLess(v,-3)

    def test_no_unwarranted_global_claims(self):
        r=m.verify()
        self.assertFalse(r['all_terminal_states_nonviable'])
        self.assertFalse(r['general_smf_mpc_impossible'])
        self.assertFalse(r['recursive_feasibility_proved'])

    def test_archive_when_full_checkout(self):
        root=Path(__file__).resolve().parent.parent
        f=root/'results/four_state_terminal_nonviability_20261101/checks.json'
        if not f.exists():self.skipTest('archived certificate absent in isolation')
        self.assertEqual(json.loads(f.read_text()),m.verify())

    def test_real_config_when_full_checkout(self):
        root=Path(__file__).resolve().parent.parent
        if not (root/'configs/planar_baseline.json').exists():
            self.skipTest('full repo config absent in isolation')
        self.assertEqual(m.verify(root)['run'],246)

if __name__=='__main__':unittest.main()
