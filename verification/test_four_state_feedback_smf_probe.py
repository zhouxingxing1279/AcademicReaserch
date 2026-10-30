import unittest
from check_four_state_feedback_smf_probe import (load,rad,add,scale,intersect,plant_step,initial,predict,observe,v_from_two_packets,feedback,simulate,run)

class FeedbackSMFProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.c=load()
    def test_bounds_and_legal_thrust(self):
        c=self.c
        self.assertAlmostEqual(rad(c['tmax']),2.1034840625)
        self.assertAlmostEqual(c['taumax'],0.08)
    def test_interval_operations(self):
        self.assertEqual(scale((-1,2),-2),(-4,2))
        self.assertEqual(intersect((-2,2),(-1,1)),(-1,1))
        with self.assertRaises(ValueError):intersect((1,2),(3,4))
    def test_two_packet_identity_for_constant_acceleration(self):
        h=self.c['h'];n=15;acc=[(2.,2.)]*n
        p0=(0.,0.);pn=(h*h*2*n*(n-1)/2,)*2
        vn=v_from_two_packets(p0,pn,acc,h)
        self.assertAlmostEqual(vn[0],h*2*n)
        self.assertAlmostEqual(vn[1],h*2*n)
    def test_prediction_contains_exact_plant_for_extreme_residual(self):
        c=self.c;box=initial(c)
        for t in (c['tmin'],c['tmax']):
            for u in (-c['taumax'],c['taumax']):
                b,_=predict(box,t,u,c)
                for r in (-rad(t),rad(t)):
                    x=plant_step((0.,0.,0.,0.),t,u,r,c)
                    self.assertTrue(all(lo-1e-10<=z<=hi+1e-10 for z,(lo,hi) in zip(x,b)))
    def test_zero_torque_72_tick_counterexample_replayed(self):
        d=simulate(self.c,'zero','positive_high',150)
        self.assertEqual(d['first_violation'][0],72)
        self.assertEqual(d['first_violation'][1],1)
    def test_nonzero_smf_feedback_is_causal_but_not_robust(self):
        d=simulate(self.c,'feedback','positive_high',150)
        self.assertGreater(d['nonzero_torque_ticks'],100)
        self.assertEqual(d['first_violation'][1],3)
        self.assertEqual(d['smf_coverage'],150)
        self.assertLessEqual(d['max_abs_torque'],self.c['taumax']+1e-12)
    def test_fullstate_is_diagnostic_only(self):
        d=simulate(self.c,'fullstate','positive_high',150)
        self.assertIsNone(d['first_violation'])
        self.assertEqual(d['smf_coverage'],150)
    def test_all_cases_covered_but_not_all_safe(self):
        d=run()
        self.assertEqual(len(d['scenarios']),9)
        self.assertTrue(all(r['smf_coverage']==150 for r in d['scenarios']))
        self.assertTrue(any(r['first_violation'] is not None for r in d['scenarios']))
        self.assertEqual(d['gate_A'],'blocked')

if __name__=='__main__':unittest.main()
