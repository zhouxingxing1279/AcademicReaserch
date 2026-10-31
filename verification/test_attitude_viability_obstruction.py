"""Run209 exact-rational viability regression tests."""
import itertools
import unittest
from fractions import Fraction as Q
import check_reachable_smf_backup_rollout as m
import check_two_stage_causal_backup as prior
import check_attitude_viability_obstruction as a

class TestAttitudeViabilityObstruction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.box,cls.t,cls.truth=prior.rollout_filter('alternating_high','two_stage',steps=100,capture_tick=96)['capture']
        cls.phi,cls.omega=cls.truth[2:4]

    def test_frozen_attitude_contract(self):
        self.assertEqual((m.H,m.J,m.UMAX,m.LIMITS[2]),(Q(1,50),Q(1,50),Q(2,25),Q(9,20)))

    def test_reachable_posterior_is_singleton_attitude(self):
        for i in (2,3):self.assertEqual(self.box[i],(self.truth[i],self.truth[i]))

    def test_closed_form_equals_all_negative_torque(self):
        for n in range(1,7):
            self.assertEqual(a.minimum_attitude(self.phi,self.omega,n),a.attitude_after(self.phi,self.omega,[-m.UMAX]*n))

    def test_all_five_tick_torque_vertices(self):
        vals=[a.attitude_after(self.phi,self.omega,u) for u in itertools.product((-m.UMAX,m.UMAX),repeat=5)]
        self.assertEqual(min(vals),a.minimum_attitude(self.phi,self.omega,5))
        self.assertEqual(len(vals),32)

    def test_four_tick_not_yet_forced_to_violate(self):
        self.assertLessEqual(a.minimum_attitude(self.phi,self.omega,4),m.LIMITS[2])

    def test_five_tick_inevitable_attitude_violation(self):
        self.assertGreater(a.minimum_attitude(self.phi,self.omega,5),m.LIMITS[2])
        self.assertGreater(a.minimum_attitude(self.phi,self.omega,5)-m.LIMITS[2],Q(27,1000))

    def test_no_new_attitude_information_at_tick97(self):
        self.assertNotEqual(97%5,0)
        for u in (-m.UMAX,Q(0),m.UMAX):
            pred=m.predict(self.box,self.t,u)
            for s1,s2 in itertools.product((-1,0,1),repeat=2):
                y=(m.mid(pred[0]),m.mid(pred[1]),m.mid(pred[2]),m.mid(pred[3]))
                post=m.observe(pred,y,False,(m.Z,m.Z,s1*m.SIGMA[2],s2*m.SIGMA[3]))
                self.assertEqual(post,pred)

    def test_existing_two_stage_refusal(self):
        self.assertFalse(prior.two_stage_audit(self.box,self.t)['feasible'])

    def test_summary_has_strict_scope(self):
        s=a.inspect_reachable_tick96()
        self.assertEqual(s['vertex_torque_sequences_checked'],32)
        self.assertEqual(s['accepted_prior_ticks'],95)
        self.assertFalse(s['next_attitude_measurement_adds_information'])
        self.assertEqual(s['gate_A'],'blocked')

if __name__=='__main__':unittest.main()
