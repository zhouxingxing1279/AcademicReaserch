import unittest
import numpy as np
from unittest.mock import patch
from types import SimpleNamespace
from fractions import Fraction as Q
from check_multidim_tube_qp import (initial, terminal_check, margins,
                                    optimize, objective, replay, shifted, nominal,
                                    F, G, TX, RR, RAD)


class MultidimTubeTests(unittest.TestCase):
    def test_terminal_invariance_and_initial_candidate(self):
        self.assertTrue(terminal_check())
        z, d, estimator, plan = initial()
        self.assertGreaterEqual(min(margins(z, d, estimator, plan)), 0)

    def test_optimizer_improves_and_bad_proposal_fails(self):
        z, d, estimator, plan = initial()
        optimized, accepted = optimize(z, d, estimator, plan)
        self.assertTrue(accepted)
        self.assertLess(objective(z, optimized), objective(z, plan))
        self.assertGreaterEqual(min(margins(z, d, estimator, optimized)), 0)
        self.assertLess(min(margins(z, d, estimator,
                                    np.full((4, 2), Q(2), dtype=object))), 0)

    def test_missing_support_queries_preserve_shifted_plan(self):
        result = replay('template_missing', steps=5)
        self.assertEqual(result['violations'], 0)
        self.assertEqual(result['shift_rejections'], 0)

    def test_solver_failure_uses_certified_fallback(self):
        z,d,est,plan=initial()
        for proposal in (np.full(8,np.nan),np.full(8,2.0)):
            with patch('check_multidim_tube_qp.minimize',return_value=SimpleNamespace(x=proposal)):
                chosen,accepted=optimize(z,d,est,plan)
                self.assertFalse(accepted)
                self.assertTrue(np.array_equal(chosen,plan))

    def test_cost_shift_decreases_without_optimizer(self):
        z,d,est,plan=initial()
        next_z=nominal(z,plan)[1]
        self.assertGreaterEqual(objective(z,plan)-objective(next_z,shifted(z,plan)),
                                10*(z@z)+plan[0]@plan[0])

    def test_shared_noise_and_global_iss_bound(self):
        self.assertTrue(np.array_equal(TX@G,np.hstack((np.eye(2,dtype=int),np.zeros((2,2),dtype=int)))))
        self.assertTrue(all(np.abs(F)@RR <= Q(3,4)*RR))
        self.assertTrue(all(np.abs(G)@RAD <= Q(3,20)*RR))

    def test_qp_constraint_map_is_affine_including_terminal(self):
        z,d,est,plan=initial()
        zero=np.full((4,2),Q(0),dtype=object)
        constant=np.array(margins(z,d,est,zero),dtype=object)
        proposal=np.array([[Q(i-3,7),Q(5-i,9)] for i in range(4)],dtype=object)
        reconstructed=constant.copy()
        for j in range(8):
            unit=zero.copy()
            unit.flat[j]=Q(1)
            reconstructed+=(np.array(margins(z,d,est,unit),dtype=object)-constant)*proposal.flat[j]
        self.assertTrue(np.array_equal(reconstructed,np.array(margins(z,d,est,proposal),dtype=object)))


if __name__ == '__main__':
    unittest.main()
