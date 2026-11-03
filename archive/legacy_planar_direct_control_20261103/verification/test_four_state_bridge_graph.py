"""Run228 rational bridge-graph certificate tests."""
import unittest
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_bridge_graph as m

class BridgeGraphTests(unittest.TestCase):
    def test_radius_and_center_strict_obstruction(self):
        d=m.center_obstruction(Q(3,100))
        self.assertEqual(Q(d['minimum_adversarial_next_speed']),Q(6254383,160000000))
        self.assertTrue(d['certified_noninvariant'])
        self.assertGreater(Q(d['strict_gap_if_positive']),0)

    def test_expanded_center_not_refuted(self):
        self.assertFalse(m.center_obstruction(Q(1,20))['certified_noninvariant'])

    def test_union_coverage_crosses_adjacent_cells(self):
        a=m.make_box((0,1),(0,1),(0,1),(0,1))
        b=m.make_box((1,2),(0,1),(0,1),(0,1))
        target=m.make_box((Q(1,2),Q(3,2)),(0,1),(0,1),(0,1))
        self.assertTrue(m.union_covers(target,[a,b])[0])
        self.assertFalse(m.union_covers(target,[a])[0])

    def test_union_detects_gap_and_boundary(self):
        a=m.make_box((0,Q(9,10)),(0,1),(0,1),(0,1))
        b=m.make_box((Q(11,10),2),(0,1),(0,1),(0,1))
        target=m.make_box((0,2),(0,1),(0,1),(0,1))
        ok,point=m.union_covers(target,[a,b]);self.assertFalse(ok)
        self.assertTrue(Q(9,10)<point[0]<Q(11,10))

    def test_outward_successor_covers_center_extremes(self):
        box=m.make_box((0,0),(0,0),(0,0),(0,0))
        for t in (m.TMIN,m.TMAX):
            s=m.outer_successor(box,t,Q(0))
            r=m.R0+m.RT*t
            self.assertEqual(s[1],(-m.H*r,m.H*r))
            self.assertEqual(s[2],(Q(0),Q(0)))

    def test_candidate_cells_in_domain(self):
        for b in (Q(3,100),Q(1,20)):
            self.assertEqual(set(m.candidate_cells(b)),{'bridge','positive','negative'})
            self.assertTrue(all(m.within_domain(c) for c in m.candidate_cells(b).values()))

    def test_archive_and_nonclaim(self):
        d=m.verify()
        self.assertEqual(d['gate_A'],'blocked')
        self.assertTrue(d['cases']['narrow']['center_obstruction']['certified_noninvariant'])
        self.assertFalse(d['cases']['expanded']['center_obstruction']['certified_noninvariant'])
        self.assertEqual(d['cases']['narrow']['cell_policy_scan']['bridge']['menu_actions_tested'],9)

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(m.config_contract(root))
        else:self.skipTest('requires full checkout; GitHub Actions must verify')

if __name__=='__main__':unittest.main()
