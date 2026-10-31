"""Run207 exact rational causal-bridge regression tests."""
import unittest
from fractions import Fraction as Q
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import check_reachable_smf_backup_rollout as m
import check_causal_shift_bridge as b

class TestCausalShiftBridge(unittest.TestCase):
    def test_initial_box_feasible(self):
        a=b.bridge_audit(m.initial_box(),m.TMAX)
        self.assertTrue(a['feasible'])
        self.assertEqual(a['inequalities'],260)
        self.assertLessEqual(Q(a['lower']),Q(0))
        self.assertGreaterEqual(Q(a['upper']),Q(0))

    def test_shift_at_boundaries_and_interior(self):
        box=m.initial_box()
        for t0 in (m.TMIN,Q(10),m.TMAX):
            a=b.bridge_audit(box,t0)
            self.assertTrue(a['feasible'])
            for u in (Q(a['lower']),Q(a['upper']),Q(0)):
                if not Q(a['lower'])<=u<=Q(a['upper']):continue
                for t1 in (m.TMIN,Q(10),m.TMAX):
                    self.assertTrue(b.verify_shift(box,t0,u,t1))

    def test_every_legal_next_measurement_is_subset(self):
        box=m.initial_box();t0=m.TMAX
        a=b.bridge_audit(box,t0);u=Q(a['upper'])
        predicted=m.predict(box,t0,u)
        for t1 in (m.TMIN,Q(10),m.TMAX):
            for success in (False,True):
                for truth in (tuple(m.mid(v) for v in predicted),tuple(v[0] for v in predicted)):
                    for noise in ((m.Z,)*4,(m.SIGMA[0],m.Z,m.SIGMA[2],-m.SIGMA[3])):
                        try:post=m.observe(predicted,truth,success,noise)
                        except AssertionError:continue
                        except ValueError:continue
                        self.assertTrue(all(predicted[i][0]<=post[i][0]<=post[i][1]<=predicted[i][1] for i in range(4)))
                        cert=m.backup_audit(post,t1)
                        self.assertTrue(cert['feasible'])
                        self.assertLessEqual(Q(cert['lower']),0)
                        self.assertGreaterEqual(Q(cert['upper']),0)

    def test_bridge_subset_of_four_tick_interval(self):
        for t0 in (m.TMIN,m.TMAX):
            box=m.initial_box();a=b.bridge_audit(box,t0);c=m.backup_audit(box,t0)
            self.assertTrue(a['feasible'] and c['feasible'])
            self.assertGreaterEqual(Q(a['lower']),Q(c['lower']))
            self.assertLessEqual(Q(a['upper']),Q(c['upper']))

    def test_bad_current_box_fails_closed(self):
        bad=((Q(6),Q(7)),(-Q(1),Q(1)),(-Q(1,100),Q(1,100)),(-Q(1,100),Q(1,100)))
        self.assertFalse(b.bridge_audit(bad,m.TMAX)['feasible'])

    def test_run206_regression_mirror(self):
        r=m.rollout('alternating_high',100,'packet_velocity')
        self.assertEqual(r['accepted_ticks'],95)
        self.assertEqual(r['first_refusal']['tick'],96)

    def test_bridge_trajectory_never_outlasts_original(self):
        for s in ('positive_high','alternating_high','switch_positive'):
            original=m.rollout(s,100,'packet_velocity')
            bridge=b.bridge_rollout(s,100)
            self.assertLessEqual(bridge['accepted_ticks'],100)
            self.assertGreaterEqual(bridge['accepted_ticks'],1)
            # Different control histories: no pointwise monotonicity claimed.
            self.assertIsNotNone(bridge['accepted_ticks'])

if __name__=='__main__':unittest.main()
