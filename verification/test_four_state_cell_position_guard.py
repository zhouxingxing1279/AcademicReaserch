"""Run231 rational whole-cell necessary safety guard tests."""
import unittest
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_cell_position_guard as m
import check_four_state_bridge_graph as plant

class CellPositionGuardTests(unittest.TestCase):
    def test_positive_volume_and_sign_symmetry(self):
        b=m.witness_box()
        self.assertTrue(all(lo<hi for lo,hi in b))
        self.assertEqual(m.mirror_box(m.mirror_box(b)),b)
        self.assertTrue(plant.within_domain(m.mirror_box(b)))

    def test_strict_whole_cell_exclusion(self):
        d=m.positive_position_guard(m.witness_box())
        self.assertTrue(d['strict_exclusion'])
        self.assertEqual(d['position_lower']-5,Q(461731712952866342887537,25000000000000000000000000))
        self.assertEqual(len(d['rows']),25)

    def test_recovers_run230_zero_slice(self):
        b=plant.make_box((Q(49,10),Q(49,10)),(0,0),(0,0),(0,0))
        d=m.positive_position_guard(b)
        self.assertEqual(d['position_lower']-Q(49,10),Q(98296135986106564467,762939453125000000000))

    def test_inconclusive_center_not_claimed_safe(self):
        b=plant.make_box((0,0),(0,0),(0,0),(0,0))
        self.assertFalse(m.positive_position_guard(b)['strict_exclusion'])

    def test_reject_uncertified_tilt_and_invalid_horizon(self):
        b=plant.make_box((0,0),(0,0),(Q(1,100),Q(1,100)),(Q(1,100),Q(1,100)))
        with self.assertRaises(ValueError):m.positive_position_guard(b)
        with self.assertRaises(ValueError):m.positive_position_guard(m.witness_box(),26)

    def test_output_contract(self):
        d=m.verify()
        self.assertEqual(d['gate_A'],'blocked')
        self.assertTrue(d['both_full_cells_excluded'])
        self.assertTrue(d['run230_zero_slice_reproduced'])

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(plant.config_contract(root))
        else:self.skipTest('requires complete checkout; GitHub CI must verify')

if __name__=='__main__':unittest.main()
