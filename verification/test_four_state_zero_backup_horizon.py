"""Run250 focused proof regression; no numerical replay is used as a proof."""
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_zero_backup_horizon as m

class TestZeroBackupHorizon(unittest.TestCase):
    def test_taylor_sign_symmetry(self):
        for a in (F(0),F(1,100),F(1,5),m.PHI_MAX):
            lo,hi=m.sin_bounds(a)
            self.assertEqual(m.sin_bounds(-a),(-hi,-lo))
    def test_outward_rounding(self):
        for a in (F(-1,3),F(1,3),F(-11,100)):
            self.assertLessEqual(m.down(a),a)
            self.assertGreaterEqual(m.up(a),a)
    def test_zero_55_safe(self):
        rows=m.uniform_zero_prefix(55)
        self.assertEqual(len(rows),56)
        self.assertTrue(all(map(m.safe,rows)))
    def test_uniform_67_safe(self):
        rows=m.uniform_zero_prefix(67)
        self.assertTrue(all(map(m.safe,rows)))
        self.assertLess(rows[-1]['v'][1],m.V_MAX)
    def test_uniform_68_fails(self):
        b=m.uniform_zero_prefix(68)[-1]
        self.assertFalse(m.safe(b))
        self.assertLess(b['v'][0],-m.V_MAX)
    def test_physical_corner_true_not_box_artifact(self):
        rows=m.physical_corner_negative(68)
        self.assertTrue(all(-m.PHI_MAX<phi<m.PHI_MAX for _,_,phi,_ in rows))
        self.assertTrue(all(-m.OMEGA_MAX<omega<m.OMEGA_MAX for _,_,_,omega in rows))
        self.assertTrue(all(max(map(abs,v))<m.V_MAX for _,v,_,_ in rows[:68]))
        self.assertLess(rows[68][1][1],-m.V_MAX)
    def test_strict_margin_and_claim_scope(self):
        obj=m.verify()
        self.assertGreater(F(obj['strict_velocity_violation_margin_lower_bound_m_s']),0)
        self.assertTrue(obj['full_information_viability_of_tick55_corner_unknown'])
        self.assertFalse(obj['general_recursive_feasibility_proved'])
    def test_config_and_run249_if_full_checkout(self):
        root=Path(__file__).resolve().parents[1]
        if not (root/'configs/planar_baseline.json').exists():
            self.skipTest('requires complete checkout')
        self.assertEqual(m.verify(root)['run'],250)
    def test_archive_if_full_checkout(self):
        root=Path(__file__).resolve().parents[1]
        archive=root/'results/four_state_zero_backup_horizon_20261101/checks.json'
        if not archive.exists():self.skipTest('requires complete checkout')
        self.assertEqual(json.loads(archive.read_text()),m.verify(root))

if __name__=='__main__':unittest.main()
