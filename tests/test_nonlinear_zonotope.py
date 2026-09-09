import json
from pathlib import Path
import sys
import unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from smf_mpc import plant
from smf_mpc.sets import Box,Zonotope,EmptySet
from smf_mpc.filter import OutOfDomain
from smf_mpc.sensing import Observation,ContractViolation
from smf_mpc.zonotope_filter import nominal_step_and_jacobian,predict_zonotope,measurement_update,ZonotopeSMF,contains
CONFIG=json.loads((ROOT/'configs/planar_baseline.json').read_text())


class NonlinearZonotopeTests(unittest.TestCase):
    def test_lp_tolerance_regression(self):
        from smf_mpc.zonotope_filter import lp_witness
        case=json.loads((ROOT/'tests/fixtures/lp_tolerance_case.json').read_text())
        self.assertTrue(lp_witness(np.array(case['matrix']),np.array(case['rhs'])))

    def test_lp_row_scaling_regression(self):
        from smf_mpc.zonotope_filter import lp_witness
        case=json.loads((ROOT/'tests/fixtures/lp_row_scaling_case.json').read_text())
        self.assertTrue(lp_witness(np.array(case['matrix']),np.array(case['rhs'])))

    def test_nonhover_jacobian(self):
        x=np.array([.1,2,.2,-.2,.3,.1]);u=np.array([11.,.02])
        _,A=nominal_step_and_jacobian(x,u,CONFIG)
        eps=1e-6
        fd=np.column_stack([(nominal_step_and_jacobian(x+eps*d,u,CONFIG)[0]-nominal_step_and_jacobian(x-eps*d,u,CONFIG)[0])/(2*eps) for d in np.eye(6)])
        np.testing.assert_allclose(A,fd,atol=1e-9,rtol=0)

    def test_whole_interval_remainder_and_missing_remainder_counterexample(self):
        c=np.array([0,2,0,0,.15,0.]);G=np.diag([.1,.1,.1,.1,.2,.1]);u=np.array([12.,0])
        z=Zonotope(c,G);_,d=predict_zonotope(z,u,CONFIG)
        f,A=nominal_step_and_jacobian(c,u,CONFIG)
        max_error=0
        for phi in np.linspace(-.05,.35,101):
            x=c.copy();x[4]=phi
            residual=nominal_step_and_jacobian(x,u,CONFIG)[0]-f-A@(x-c)
            self.assertTrue(np.all(np.abs(residual)<=d['remainder_radius']+1e-14))
            max_error=max(max_error,np.max(np.abs(residual)))
        self.assertGreater(max_error,1e-3)

    def test_independent_nonlinear_truth_in_predicted_zonotope(self):
        rng=np.random.default_rng(73001)
        for _ in range(10):
            c=np.array([0,2,0,0,rng.uniform(-.2,.2),0.])
            G=np.diag([.1,.1,.2,.2,.15,.1]);z=Zonotope(c,G)
            u=np.array([rng.uniform(5,14),rng.uniform(-.07,.07)])
            prediction,_=predict_zonotope(z,u,CONFIG)
            for _ in range(10):
                x=c+G@rng.uniform(-1,1,6)
                truth=plant.step(x,u,rng.uniform(-.5,.5,2),CONFIG)
                self.assertTrue(contains(prediction,truth))

    def test_empty_strip_detected(self):
        z=Zonotope(np.array([0,2,0,0,0,0.]),np.eye(6)*.01)
        with self.assertRaises(EmptySet):
            measurement_update(z,Observation(0,(0,),[10],[.02]))

    def test_domain_rejection(self):
        z=Zonotope(np.array([0,2,0,0,0,0.]),np.diag([.1,.1,.1,.1,.5,.1]))
        with self.assertRaises(OutOfDomain):predict_zonotope(z,[9.81,0],CONFIG)

    def test_contract_and_atomic_failure(self):
        b=Box.from_center(CONFIG['initial_set']['center'],CONFIG['initial_set']['halfwidth'])
        f=ZonotopeSMF(b,plant.observe(b.center,0,(0,1,4,5),np.zeros(6),CONFIG),CONFIG)
        before=f.zonotope.generators.copy()
        with self.assertRaises(ContractViolation):f.advance([9.81,0],Observation(2,(4,5),[0,0],[.005,.01]))
        with self.assertRaises(EmptySet):f.advance([9.81,0],Observation(1,(4,5),[10,0],[.005,.01]))
        self.assertEqual(f.tick,0);np.testing.assert_array_equal(before,f.zonotope.generators)

    def test_budget_and_valid_measurement_update(self):
        b=Box.from_center(CONFIG['initial_set']['center'],CONFIG['initial_set']['halfwidth'])
        f=ZonotopeSMF(b,plant.observe(b.center,0,(0,1,4,5),np.zeros(6),CONFIG),CONFIG,12)
        for k in range(1,16):
            indices=(0,1,4,5) if k%5==0 else (4,5)
            f.advance([9.81,0],plant.observe(b.center,k,indices,np.zeros(6),CONFIG))
            self.assertLessEqual(f.zonotope.generators.shape[1],12)
            self.assertTrue(contains(f.zonotope,b.center))


if __name__=='__main__':unittest.main()
