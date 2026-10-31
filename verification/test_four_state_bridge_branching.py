"""Run229 exact two-step robust branching graph tests."""
import unittest
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_bridge_graph as old
import check_four_state_bridge_branching as m

class BranchingTests(unittest.TestCase):
    def test_three_certified_edges(self):
        nodes,edges,u=m.build_graph()
        self.assertEqual(len(edges),3)
        for src,dsts in edges:
            self.assertTrue(old.union_covers(old.outer_successor(nodes[src],*u),[nodes[x] for x in dsts])[0])

    def test_both_sign_branches_necessary_for_outer_coverage(self):
        nodes,_,u=m.build_graph()
        s=old.outer_successor(nodes['seed'],*u)
        self.assertFalse(old.union_covers(s,[nodes['velocity_negative']])[0])
        self.assertFalse(old.union_covers(s,[nodes['velocity_positive']])[0])

    def test_exact_center_two_sided_disturbance(self):
        self.assertEqual(old.H*(old.R0+old.RT*old.TMIN),Q(6254383,160000000))
        d=m.verify()
        self.assertGreater(Q(d['two_step_branching']['seed_successor_velocity_halfwidth']),Q(1,20)*Q(4,5))

    def test_position_velocity_coupling_and_domain(self):
        nodes,_,_=m.build_graph()
        self.assertLess(nodes['next_negative'][0][0],nodes['next_positive'][0][0])
        self.assertLess(nodes['next_negative'][0][1],nodes['next_positive'][0][1])
        self.assertTrue(all(old.within_domain(c) for c in nodes.values()))

    def test_finite_dag_not_rci(self):
        d=m.verify()
        self.assertEqual(d['gate_A'],'blocked')
        self.assertEqual(len(d['certified_edges']),3)
        self.assertTrue(all(x['robust_covered'] for x in d['certified_edges']))
        self.assertIn('no terminal RCI',d['limitations'][0])

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(old.config_contract(root))
        else:self.skipTest('requires full checkout; GitHub Actions must verify')
if __name__=='__main__':unittest.main()
