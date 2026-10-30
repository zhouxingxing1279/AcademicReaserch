import itertools
import unittest
from fractions import Fraction as Q
from check_mode_indexed_backup_admission import (
    ROOT, contract, load_rows, packet_branches, initial_box, dynamics,
    residual_radius, propagate, support_abs, reachable_bounds, admitted,
    closed_form_v3, zero_torque_counterexample, run,
)


class ModeIndexedBackupAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=ROOT
        cls.c=contract()
        cls.rows=load_rows()

    def test_frozen_mode_graph_and_contract(self):
        c=self.c
        self.assertEqual((c['h'],c['j']),(Q(1,50),Q(1,50)))
        self.assertEqual((c['tmin'],c['tmax']),(Q(981,200),Q(2943,200)))
        self.assertEqual(c['limits'],(Q(5),Q(3),Q(9,20),Q(2)))
        self.assertEqual(packet_branches(5,c),[('success',0),('miss',5)])
        self.assertEqual(packet_branches(10,c),[('success',0),('miss',10)])
        self.assertEqual(packet_branches(15,c),[('success',0)])

    def test_rational_run202_inputs_are_conservative(self):
        c=self.c
        for n in (5,10,15):
            for name in ('low','high'):
                row=self.rows[(n,name)]
                success=initial_box(row,'success',c)
                self.assertEqual(success[0],Q(1,50))
                self.assertLessEqual(success[1],Q(row['certified_box_velocity_outer_halfwidth']))
                if n<15:
                    miss=initial_box(row,'miss',c)
                    self.assertGreaterEqual(miss[0],success[0])
                    self.assertGreaterEqual(miss[1],success[1])

    def test_exact_v3_formula_for_all_torque_and_future_endpoints(self):
        c=self.c
        rad=initial_box(self.rows[(10,'high')],'success',c)
        for tau in (Q(-2,25),Q(0),Q(1,25),Q(2,25)):
            for t1,t2 in itertools.product((c['tmin'],c['tmax']),repeat=2):
                z=((Q(0),)*4,tuple(tuple(rad[i] if i==j else Q(0) for j in range(4)) for i in range(4)))
                for t,u in ((c['tmax'],tau),(t1,Q(0)),(t2,Q(0))):
                    z=propagate(z,t,u,c)
                self.assertEqual(support_abs(z)[1],closed_form_v3(rad,c['tmax'],t1,t2,tau,c))

    def test_generator_support_matches_independent_corner_witnesses(self):
        c=self.c
        rad=initial_box(self.rows[(10,'high')],'success',c)
        t0,t1,t2=c['tmax'],c['tmin'],c['tmax']
        tau=Q(1,25)
        z=((Q(0),)*4,tuple(tuple(rad[i] if i==j else Q(0) for j in range(4)) for i in range(4)))
        for t,u in ((t0,tau),(t1,Q(0)),(t2,Q(0))):z=propagate(z,t,u,c)
        expected=support_abs(z)
        corners=[Q(-1),Q(1)]
        observed=[Q(0)]*4
        for signs in itertools.product(corners,repeat=7):
            x=tuple(rad[i]*signs[i] for i in range(4))
            for k,t in enumerate((t0,t1,t2)):
                x=dynamics(x,t,tau if k==0 else Q(0),c)
                x=(x[0],x[1]+c['h']*residual_radius(t)*signs[4+k],x[2],x[3])
            observed=[max(observed[i],abs(x[i])) for i in range(4)]
        self.assertEqual(tuple(observed),expected)

    def test_future_interior_thrusts_contained_in_endpoint_envelope(self):
        c=self.c
        rad=initial_box(self.rows[(10,'high')],'miss',c)
        tau=Q(-1,25)
        worst=reachable_bounds(rad,c['tmin'],tau,c)
        for t1,t2 in itertools.product((c['tmin'],(c['tmin']+c['tmax'])/2,c['tmax']),repeat=2):
            z=((Q(0),)*4,tuple(tuple(rad[i] if i==j else Q(0) for j in range(4)) for i in range(4)))
            for k,(t,u) in enumerate(((c['tmin'],tau),(t1,Q(0)),(t2,Q(0)))):
                z=propagate(z,t,u,c)
                self.assertTrue(all(a<=b for a,b in zip(support_abs(z),worst[k])))

    def test_all_branches_have_finite_horizon_hard_backup(self):
        d=run()
        self.assertEqual(len(d['rows']),10)
        self.assertTrue(all(r['zero_torque_hard_admissible'] for r in d['rows']))
        self.assertTrue(all(r['admissible_torque_candidates']==5 for r in d['rows']))
        self.assertEqual(d['gate_A'],'blocked')
        self.assertEqual(d['evidence'],'EXACT_RATIONAL_THREE_TICK_OUTER_REACHABILITY')

    def test_branch_specific_diagnostic_only(self):
        d=run()
        selected={(r['gap_ticks'],r['thrust'],r['packet']):r for r in d['rows']}
        self.assertTrue(selected[(10,'high','success')]['zero_torque_v065_admissible'])
        self.assertFalse(selected[(10,'high','miss')]['zero_torque_v065_admissible'])
        self.assertNotIn((15,'high','miss'),selected)
        self.assertIn('not an original hard',d['diagnostic_velocity_limit'])

    def test_perpetual_zero_torque_is_not_invariant(self):
        witness=zero_torque_counterexample(self.c)
        self.assertEqual(witness['first_violation_tick'],72)
        self.assertEqual(witness['violated_coordinates'],[1])
        self.assertGreater(Q(witness['state'][1]),Q(3))
        self.assertLess(Q(witness['state'][0]),Q(5))

    def test_zero_torque_minimizes_symmetric_velocity_envelope(self):
        c=self.c
        rad=initial_box(self.rows[(15,'high')],'success',c)
        base=reachable_bounds(rad,c['tmax'],Q(0),c)[2][1]
        for tau in (Q(-2,25),Q(-1,25),Q(1,25),Q(2,25)):
            self.assertGreater(reachable_bounds(rad,c['tmax'],tau,c)[2][1],base)


if __name__=='__main__':unittest.main()
