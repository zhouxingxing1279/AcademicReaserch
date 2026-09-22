import unittest
from fractions import Fraction as Q
import numpy as np
from unittest.mock import patch
from types import SimpleNamespace
from check_certified_multistep_qp import build, query, exact_support, execute, dual_value


class CertifiedMultistepTests(unittest.TestCase):
    def test_lp_proposals_have_exact_certificates(self):
        for p in [(Q(4,5),Q(1,5)),(Q(-1),Q(2)),(Q(1),Q(1))]:
            lower,upper,point=query(p)
            self.assertLessEqual(lower,exact_support(p))
            self.assertGreaterEqual(upper,exact_support(p))
            self.assertLessEqual(abs(sum(point)),Q(1,50))
            self.assertTrue(all(abs(v)<=Q(1,10) for v in point))

    def test_dense_quadratic_matches_original_cost(self):
        import check_multidim_tube_qp as base
        data=build((Q(4,5),-Q(2,5)))
        v=np.array([Q(j-4,100) for j in range(8)],dtype=object)
        self.assertEqual(data['c']+data['f']@v+v@data['H']@v/2,
                         base.objective(data['z'],v.reshape(4,2)))

    def test_full_queries_certify_target_accuracy(self):
        r=execute('all_at_once')
        self.assertTrue(r['tolerance_met'])
        self.assertGreater(r['objective_improvement'],0)
        self.assertGreaterEqual(r['minimum_robust_margin'],0)

    def test_zero_budget_does_not_claim_precision(self):
        r=execute('priority',budget=0,initial_bounds='caps_only')
        self.assertFalse(r['tolerance_met'])
        self.assertEqual(r['support_lp_calls'],0)
        self.assertGreaterEqual(r['minimum_robust_margin'],0)

    def test_negative_multiplier_is_rejected(self):
        d=build((Q(4,5),-Q(2,5)))
        lam=np.full(len(d['b']),Q(0),dtype=object)
        lam[0]=-Q(1)
        with self.assertRaises(ValueError): dual_value(d,d['b'],lam)

    def test_condensed_constraints_match_direct_tube(self):
        import check_multidim_tube_qp as base
        d=build((Q(4,5),-Q(2,5)))
        v=np.array([Q(j-4,100) for j in range(8)],dtype=object)
        oracle=SimpleNamespace(support=exact_support)
        direct=np.array(base.margins(d['z'],np.array([Q(0),Q(0)],dtype=object),oracle,v.reshape(4,2)))
        self.assertTrue(np.array_equal(direct,d['b']-d['D']@v-d['true_support']))

    def test_dual_value_is_exact_lagrangian_minimum(self):
        d=build((Q(4,5),-Q(2,5)))
        lam=np.array([Q(j%3,10) for j in range(len(d['b']))],dtype=object)
        bound=d['b']-d['true_support']
        stationary=-d['Hinv']@(d['f']+d['D'].T@lam)
        lag=d['c']+d['f']@stationary+stationary@d['H']@stationary/2+lam@(d['D']@stationary-bound)
        self.assertEqual(lag,dual_value(d,bound,lam))

    def test_lp_failure_keeps_valid_upper_and_member(self):
        p=(Q(4,5),Q(1,5))
        with patch('check_certified_multistep_qp.linprog',return_value=SimpleNamespace(success=False)):
            lower,upper,point=query(p)
        self.assertEqual(lower,0)
        self.assertGreaterEqual(upper,exact_support(p))
        self.assertEqual(tuple(point),(Q(0),Q(0)))

    def test_free_box_bound_avoids_unnecessary_queries(self):
        r=execute('priority',budget=0,initial_bounds='box')
        self.assertTrue(r['tolerance_met'])
        self.assertEqual(r['support_lp_calls'],0)

    def test_active_maneuver_requires_geometry_refinement(self):
        coarse=execute('priority',(Q(1,5),Q(1,5)),budget=0,scenario='active_maneuver')
        refined=execute('all_at_once',(Q(1,5),Q(1,5)),scenario='active_maneuver')
        self.assertFalse(coarse['tolerance_met'])
        self.assertTrue(refined['tolerance_met'])
        self.assertGreater(refined['objective_improvement'],coarse['objective_improvement'])

    def test_maneuver_cost_and_terminal_contract(self):
        import check_multidim_tube_qp as base
        d=build((Q(1,5),Q(1,5)),scenario='active_maneuver')
        v=d['fallback']
        self.assertEqual(d['c']+d['f']@v+v@d['H']@v/2,
                         base.objective(d['z'],v.reshape(4,2))+100*(v[0]-Q(2,5))**2)
        self.assertTrue(all(Q(1,5)+np.abs(base.TX)@base.RR<=Q(1,2)))


if __name__=='__main__': unittest.main()
