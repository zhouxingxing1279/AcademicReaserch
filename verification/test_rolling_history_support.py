"""Run214 focused tests. Run against real repository modules when available."""
import unittest
from fractions import Fraction as Q
import check_rolling_history_support as r
import check_reachable_smf_backup_rollout as m
import check_nominal_short_mpc as base

class RollingHistorySupportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.box,cls.truth,cls.positions,cls.attitudes,cls.thrusts=r.replay_to_193()
        cls.last3,cls.meta3=r.rolling_support(cls.positions,cls.attitudes,cls.thrusts,192,3)
        cls.last6,cls.meta6=r.rolling_support(cls.positions,cls.attitudes,cls.thrusts,192,6)
        cls.refined=(cls.box[0],m.intersect(cls.box[1],cls.last6),cls.box[2],cls.box[3])

    def test_coefficients_and_exact_breakpoint_optimum(self):
        a,b,c=105,165,180
        self.assertIn(Q(50,9),r.breakpoints(a,b,c))
        for q in r.breakpoints(a,b,c):
            co=r.coefficients(a,b,c,q)
            self.assertEqual(sum(co),Q(0))
            self.assertEqual(m.H*((b-a)*co[1]+(c-a)*co[2]),Q(1))
        self.assertEqual(self.meta6['best_lower']['lower_q'],'50/9')

    def test_causal_history_only(self):
        self.assertEqual(self.meta6['triples'],20)
        self.assertEqual(self.meta6['newest_packet'],180)
        self.assertTrue(all(k<192 for k in self.attitudes if k<192))
        self.assertEqual(self.meta6['best_lower']['packets'],(105,165,180))

    def test_run213_prefix_and_truth_containment(self):
        self.assertEqual(self.last6[0]-self.box[1][0],Q(57617501,1440000000))
        self.assertEqual(self.last3[0],self.box[1][0])
        self.assertTrue(all(a<=v<=b for (a,b),v in zip(self.refined,self.truth)))
        self.assertTrue(all(abs(v)<=lim for v,lim in zip(self.truth,m.LIMITS)))

    def test_exact_refusal_survives_optimized_support(self):
        self.assertIsNone(base.interval(self.box,m.TMAX)[0])
        self.assertIsNone(base.interval(self.refined,m.TMAX)[0])
        self.assertLess(r.five_step_box_corner(self.refined)[-1],-m.LIMITS[1])

    def test_all_20_packet_triples_enclose_true_velocity(self):
        from itertools import combinations
        last=sorted(self.positions)[-6:]
        for tri in combinations(last,3):
            bound,_=r.three_packet_support(tuple((j,self.positions[j]) for j in tri),
                                            self.attitudes,self.thrusts,192)
            self.assertLessEqual(bound[0],self.truth[1])
            self.assertLessEqual(self.truth[1],bound[1])

if __name__=='__main__':unittest.main()
