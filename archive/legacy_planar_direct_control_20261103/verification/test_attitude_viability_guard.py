"""Run210 exact-rational necessary viability guard tests; historical dependencies required."""
import itertools
import unittest
from fractions import Fraction as Q
import check_reachable_smf_backup_rollout as m
import check_two_stage_causal_backup as prior
import check_attitude_viability_guard as g

class TestAttitudeViabilityGuard(unittest.TestCase):
    def test_frozen_contract(self):
        self.assertEqual((m.H,m.J,m.UMAX,m.LIMITS[2]),(Q(1,50),Q(1,50),Q(2,25),Q(9,20)))

    def test_closed_form_all_torque_vertices(self):
        phi,omega=Q(3,10),Q(19,10)
        for n in (1,2,4,6):
            vals=[]
            for seq in itertools.product((-m.UMAX,m.UMAX),repeat=n):
                p,w=phi,omega
                for u in seq:p,w=p+m.H*w,w+m.H*u/m.J
                vals.append(p)
            self.assertEqual(min(vals),g.attitude_min(phi,omega,n))
            self.assertEqual(max(vals),g.attitude_max(phi,omega,n))

    def test_guard_interval_matches_one_step_necessary_checks(self):
        box=tuple((Q(0),Q(0)) for _ in range(2))+((Q(1,5),Q(1,5)),(Q(7,5),Q(7,5)))
        lo,hi=g.guard_interval(box,8)
        for u in (-m.UMAX,Q(-1,20),Q(0),Q(1,20),m.UMAX):
            nxt=m.predict(box,m.TMAX,u)
            ok,_,_=g.necessary_at_state(nxt,7)
            self.assertEqual(lo<=u<=hi,ok)

    def test_exact_reachable_early_warning(self):
        r=g.replay('alternating_high',steps=100,horizon=8)
        self.assertEqual(r['accepted_ticks'],95)
        self.assertEqual(r['first_refusal']['tick'],96)
        self.assertEqual(r['first_state_nonviability_warning']['tick'],94)
        self.assertEqual(r['first_baseline_next_state_warning']['tick'],93)

    def test_necessary_guard_alone_refuses_earlier(self):
        r=g.replay('alternating_high',steps=100,horizon=8,guarded=True)
        self.assertEqual(r['accepted_ticks'],93)
        self.assertEqual(r['first_refusal']['cause'],'necessary_viability_guard_refusal')

    def test_early_braking_improves_reachable_prefix(self):
        r=g.replay('alternating_high',steps=150,horizon=8,guarded=True,brake_gain=Q(1,5))
        self.assertEqual(r['accepted_ticks'],150)
        self.assertIsNone(r['first_refusal'])
        self.assertGreater(r['guard_interventions'],0)

    def test_negative_long_horizon_persists(self):
        r=g.replay('positive_high',steps=200,horizon=8,guarded=True,brake_gain=Q(1,5))
        self.assertEqual(r['accepted_ticks'],191)
        self.assertEqual(r['first_refusal']['tick'],192)

    def test_no_safety_claim_in_scope(self):
        self.assertIn('necessary',g.__doc__.lower())
        self.assertNotEqual(g.guard_interval(m.initial_box(),8),(Q(1),Q(0)))

if __name__=='__main__':unittest.main()
