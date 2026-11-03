"""Run211 regression: finite-candidate optimization and exact box-reset obstruction."""
import itertools
import unittest
from fractions import Fraction as Q
import check_reachable_smf_backup_rollout as m
import check_two_stage_causal_backup as prior
import check_attitude_viability_guard as guard
import check_nominal_short_mpc as opt

class TestRun211(unittest.TestCase):
    def test_frozen_contract(self):
        self.assertEqual((m.H,m.J,m.UMAX,m.LIMITS),(Q(1,50),Q(1,50),Q(2,25),(Q(5),Q(3),Q(9,20),Q(2))))

    def test_initial_first_action_exactly_certified(self):
        box=m.initial_box();t=m.TMAX
        u,meta=opt.select(box,t)
        cert=prior.two_stage_audit(box,t)
        gl,gh=guard.guard_interval(box,8)
        self.assertTrue(cert['feasible'])
        self.assertLessEqual(max(Q(cert['lower']),gl),u)
        self.assertLessEqual(u,min(Q(cert['upper']),gh))
        self.assertGreaterEqual(meta['total_plans'],9)

    def test_nominal_prediction_is_not_a_safety_certificate(self):
        box=m.initial_box();u,meta=opt.select(box,m.TMAX)
        self.assertIn('nominal_cost',meta)
        self.assertTrue(opt.__doc__.find('NOT certified')>=0)

    def test_run210_baseline_reproduced(self):
        r=opt.rollout('positive_high',steps=200,optimized=False)
        self.assertEqual((r['accepted_ticks'],r['first_refusal']['tick']),(191,192))

    def test_finite_candidate_negative_result(self):
        r=opt.rollout('positive_high',steps=200,optimized=True)
        self.assertEqual((r['accepted_ticks'],r['first_refusal']['tick']),(133,134))
        self.assertGreater(r['interventions'],0)

    def test_other_reachable_traces(self):
        a=opt.rollout('alternating_high',steps=200,optimized=True)
        b=opt.rollout('switch_positive',steps=200,optimized=True)
        self.assertEqual((a['accepted_ticks'],b['accepted_ticks']),(200,81))

    def test_exact_outer_box_witness_and_extreme_torques(self):
        tick,box,truth,reason=opt.capture_baseline_refusal()
        self.assertEqual((tick,reason),(192,'two_stage_refusal'))
        self.assertTrue(all(lo<=v<=hi for (lo,hi),v in zip(box,truth)))
        corner=(box[0][0],box[1][0],box[2][1],box[3][1])
        vals=[]
        for seq in itertools.product((-m.UMAX,m.UMAX),repeat=5):
            s=corner
            for u in seq:s=m.step(s,m.TMAX,u,-m.rad(m.TMAX))
            vals.append(s[1])
        best=max(vals)
        witness=opt.refusal_box_witness()
        self.assertEqual(best,Q(witness['corner_velocity_5_steps_max_under_fixed_adverse_history']))
        self.assertLess(best,-m.LIMITS[1])
        self.assertAlmostEqual(float(best),-3.044998077967292)

    def test_no_recursive_feasibility_claim(self):
        data=opt.run(steps=2)
        self.assertEqual(data['gate_A'],'blocked')
        self.assertTrue(any('No terminal invariant' in s for s in data['limitations']))
        self.assertIn('NOT verified reachable',data['refusal_box_witness']['interpretation'])

if __name__=='__main__':unittest.main()
