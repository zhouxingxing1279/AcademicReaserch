"""Run213 focused exact-rational integration tests (repository imports)."""
import unittest
from fractions import Fraction as Q
import check_history_tightened_backup as r
import check_reachable_smf_backup_rollout as m
import check_nominal_short_mpc as base

class HistoryTightenedBackupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.box,cls.truth,cls.history=r.replay_snapshot()
        cls.refined=(cls.box[0],m.intersect(cls.box[1],cls.history),cls.box[2],cls.box[3])

    def test_history_exact_improvement(self):
        self.assertEqual(self.refined[1][0]-self.box[1][0],Q(7040287,96000000))
        self.assertLessEqual(self.history[0],self.truth[1]);self.assertLessEqual(self.truth[1],self.history[1])

    def test_original_refusal_refined_admission(self):
        self.assertIsNone(base.interval(self.box,m.TMAX)[0])
        allowed,reason=base.interval(self.refined,m.TMAX)
        self.assertIsNone(reason)
        self.assertEqual(allowed,(-m.UMAX,m.UMAX))

    def test_true_state_and_current_hard_limits(self):
        self.assertTrue(all(a<=v<=b for (a,b),v in zip(self.refined,self.truth)))
        self.assertTrue(all(abs(v)<=lim for v,lim in zip(self.truth,m.LIMITS)))

    def test_independent_next_backup_endpoint_and_midpoint(self):
        for u0 in (-m.UMAX,Q(0),m.UMAX):
            next_box=m.predict(self.refined,m.TMAX,u0)
            for t1 in (m.TMIN,(m.TMIN+m.TMAX)/2,m.TMAX):
                cert=m.backup_audit(next_box,t1)
                self.assertTrue(cert['feasible'],(u0,t1,cert))
                self.assertLessEqual(Q(cert['lower']),Q(0))
                self.assertGreaterEqual(Q(cert['upper']),Q(0))

    def test_counterfactual_same_policy_one_tick_gain(self):
        old=r.rollout_from_snapshot(steps=200,refine=False)
        new=r.rollout_from_snapshot(steps=200,refine=True)
        self.assertEqual(old['accepted_ticks'],191)
        self.assertEqual(new['accepted_ticks'],192)
        self.assertEqual(new['first_refusal']['tick'],193)
        self.assertEqual(new['observed_hard_violations'],0)
        self.assertLessEqual(abs(Q(new['selected_torque_tick192'])),m.UMAX)

if __name__=='__main__':unittest.main()
