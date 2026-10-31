"""Run208 exact-rational two-stage causal-backup regression tests."""
from fractions import Fraction as Q
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
import check_reachable_smf_backup_rollout as m
import check_two_stage_causal_backup as c

class TestTwoStageCausalBackup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.start=m.initial_box()
        cls.critical,cls.critical_t,cls.critical_truth=c.rollout_filter('alternating_high','two_stage',capture_tick=95)['capture']

    def test_initial_interval_and_exact_projection_counts(self):
        a=c.two_stage_audit(self.start,m.TMAX)
        self.assertTrue(a['feasible'])
        self.assertEqual((Q(a['lower']),Q(a['upper'])),(-m.UMAX,m.UMAX))
        self.assertEqual(len(a['endpoint_details']),2)
        for e in a['endpoint_details']:
            self.assertEqual(e['raw_signed_inequalities'],256)
            self.assertGreater(e['pairwise'],0)

    def test_initial_independent_four_tick_audit(self):
        a=c.two_stage_audit(self.start,m.TMAX)
        for u in (Q(a['lower']),Q(0),Q(a['upper'])):
            for t1 in (m.TMIN,Q(10),m.TMAX):
                self.assertTrue(c.verify_next_backup(self.start,m.TMAX,u,t1))

    def test_two_stage_contains_zero_bridge_interval(self):
        for box,t in ((self.start,m.TMIN),(self.start,m.TMAX),(self.critical,self.critical_t)):
            zero=c.zero_bridge_audit(box,t)
            new=c.two_stage_audit(box,t)
            if zero['feasible']:
                self.assertTrue(new['feasible'])
                self.assertLessEqual(Q(new['lower']),Q(zero['lower']))
                self.assertGreaterEqual(Q(new['upper']),Q(zero['upper']))

    def test_strict_reachable_expansion_at_tick95(self):
        zero=c.zero_bridge_audit(self.critical,self.critical_t)
        new=c.two_stage_audit(self.critical,self.critical_t)
        self.assertFalse(zero['feasible'])
        self.assertTrue(new['feasible'])
        self.assertTrue(all(lo<=v<=hi for (lo,hi),v in zip(self.critical,self.critical_truth)))

    def test_nonzero_contingent_backup_at_tick95(self):
        u,cert=c.two_stage_filter(self.critical,self.critical_t)
        self.assertIsNotNone(u)
        for t1 in (m.TMIN,Q(7),Q(10),m.TMAX):
            u1=c.contingent_u1(self.critical,self.critical_t,u,t1)
            self.assertNotEqual(u1,Q(0))
            self.assertTrue(-m.UMAX<=u1<=m.UMAX)
            self.assertTrue(c.verify_next_backup(self.critical,self.critical_t,u,t1))

    def test_posterior_measurement_monotonicity(self):
        u,_=c.two_stage_filter(self.critical,self.critical_t)
        predicted=m.predict(self.critical,self.critical_t,u)
        for t1 in (m.TMIN,Q(10),m.TMAX):
            u1=c.contingent_u1(self.critical,self.critical_t,u,t1)
            for success in (False,True):
                for truth in (tuple(m.mid(x) for x in predicted),tuple(x[0] for x in predicted)):
                    for noise in ((m.Z,)*4,(m.SIGMA[0],m.Z,m.SIGMA[2],-m.SIGMA[3])):
                        try:post=m.observe(predicted,truth,success,noise)
                        except ValueError:continue
                        self.assertTrue(all(a[0]<=b[0]<=b[1]<=a[1] for a,b in zip(predicted,post)))
                        cert=m.backup_audit(post,t1)
                        self.assertTrue(cert['feasible'])
                        self.assertLessEqual(Q(cert['lower']),u1)
                        self.assertGreaterEqual(Q(cert['upper']),u1)

    def test_rejects_bad_current_outer_box(self):
        bad=((Q(6),Q(7)),(-Q(1),Q(1)),(-Q(1,100),Q(1,100)),(-Q(1,100),Q(1,100)))
        self.assertFalse(c.two_stage_audit(bad,m.TMAX)['feasible'])

    def test_projector_handles_empty_conflicting_rows(self):
        interval,meta=c.project_u1([(Q(0),Q(1),Q(-1)),(Q(0),Q(-1),Q(-1))],(-m.UMAX,m.UMAX))
        self.assertGreater(interval[0],interval[1])

    def test_reachable_rollout_comparison(self):
        expected={'positive_high':(100,100),'alternating_high':(94,95),'switch_positive':(100,100)}
        for scenario,(old,new) in expected.items():
            self.assertEqual(c.rollout_filter(scenario,'zero_bridge')['accepted_ticks'],old)
            result=c.rollout_filter(scenario,'two_stage')
            self.assertEqual(result['accepted_ticks'],new)
            self.assertTrue(all(x['next_backup_verified'] for x in result['sampled_next_backup_checks']))

    def test_no_infinite_time_claim(self):
        r=c.rollout_filter('alternating_high','two_stage')
        self.assertEqual(r['first_refusal']['tick'],96)
        self.assertFalse(r['first_refusal']['zero_bridge_feasible'])

if __name__=='__main__':unittest.main()
