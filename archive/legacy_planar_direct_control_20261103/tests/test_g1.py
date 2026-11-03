"""Invariant and counterexample checks for the G1 numerical prototype."""
import ast
import itertools
import json
from pathlib import Path
import sys
import unittest
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from smf_mpc import plant
from smf_mpc.data import split_for,rng_for,windows
from smf_mpc.filter import predict,update,residual_halfwidth,BoxSMF,OutOfDomain
from smf_mpc.sensing import Observation,PacketSchedule,ContractViolation,enumerate_masks
from smf_mpc.sets import Box,EmptySet,Zonotope,trig_range
C=json.loads((ROOT/'configs/planar_baseline.json').read_text())


class G1Tests(unittest.TestCase):
    def test_truth_hover_and_torque_sign(self):
        x=np.array([0,2,0,0,0,0.])
        np.testing.assert_array_equal(plant.step(x,[9.81,0],[0,0],C),x)
        self.assertGreater(plant.step(x,[9.81,.01],[0,0],C)[5],0)
        x[4]=.2
        self.assertLess(plant.step(x,[9.81,0],[0,0],C)[2],0)

    def test_affine_box_extreme_corners(self):
        b=Box([-1,-2],[2,3]);A=np.array([[1,-3],[-2,4.]])
        corners=np.array(list(itertools.product(*zip(b.lower,b.upper))))
        expected=corners@A.T
        result=b.affine(A)
        np.testing.assert_allclose(result.lower,expected.min(axis=0))
        np.testing.assert_allclose(result.upper,expected.max(axis=0))

    def test_sin_cos_interior_extrema(self):
        self.assertEqual(trig_range(0,np.pi,'sin')[1],1)
        self.assertEqual(trig_range(-.2,.2,'cos')[1],1)
        self.assertEqual(trig_range(0,4*np.pi,'cos'),(-1,1))

    def test_box_empty_and_immutability(self):
        b=Box([0],[1])
        with self.assertRaises(EmptySet):b.intersect(Box([2],[3]))
        with self.assertRaises(ValueError):b.lower[0]=9
        with self.assertRaises(ValueError):Box([np.nan],[1])

    def test_component_update_no_velocity_contraction(self):
        b=Box.from_center([0,2,0,0,0,0],[1,1,.5,.5,.1,.1])
        obs=Observation(0,(0,1,4,5),np.array([0,2,0,0]),np.array([.02,.02,.005,.01]))
        out=update(b,obs)
        self.assertTrue(b.encloses(out))
        np.testing.assert_array_equal(out.radius[2:4],b.radius[2:4])
        with self.assertRaises(EmptySet):update(b,Observation(0,(0,),[9],[.02]))

    def test_residual_bound_global_random_and_boundary(self):
        rng=rng_for(70001,'bound_check');d=C['domain'];p=C['plant']
        bound=residual_halfwidth(C)[2:4]/p['dt_s']
        # Boundary combinations are independent of analytic bounding expressions.
        points=list(itertools.product([-3,3],[-3,3],[-.45,.45],[4.905,14.715],[-.5,.5],[-.5,.5]))
        for vx,vz,phi,T,bx,bz in points:
            a=plant.aerodynamic_acceleration(np.array([0,2,vx,vz,phi,0.]),[T,0],[bx,bz])
            self.assertTrue(np.all(np.abs(a)<=bound))
        for _ in range(1000):
            x=rng.uniform(d['state_lower'],d['state_upper']);u=rng.uniform(d['input_lower'],d['input_upper'])
            a=plant.aerodynamic_acceleration(x,u,rng.uniform(-.5,.5,2))
            self.assertTrue(np.all(np.abs(a)<=bound))

    def test_planar_prediction_contains_independent_truth_steps(self):
        rng=rng_for(70002,'one_step');d=C['domain']
        for _ in range(100):
            c=rng.uniform(np.array(d['state_lower'])+.15,np.array(d['state_upper'])-.15)
            b=Box.from_center(c,[.05,.05,.1,.1,.05,.1])
            u=rng.uniform(d['input_lower'],d['input_upper']);outer=predict(b,u,C)
            for _ in range(10):
                x=rng.uniform(b.lower,b.upper)
                self.assertTrue(outer.contains(plant.step(x,u,rng.uniform(-.5,.5,2),C)))

    def test_domain_failure_does_not_clip(self):
        b=Box.from_center([0,2,0,0,0,0],[.1,.1,3.1,.1,.01,.01])
        with self.assertRaises(OutOfDomain):predict(b,[9.81,0],C)
        b=Box.from_center([0,2,0,0,0,0],[.1]*6)
        with self.assertRaises(OutOfDomain):predict(b,[20,0],C)

    def test_schedule_packet_vs_tick(self):
        schedule=PacketSchedule();received=[]
        for k in range(16):
            indices=schedule.step(k,k in (5,10))
            self.assertTrue({4,5}<=set(indices))
            if 0 in indices:received.append(k)
        self.assertEqual(received,[0,15])
        self.assertEqual(received[1]-received[0]-1,14)

    def test_schedule_rejects_third_drop_and_wrong_tick(self):
        s=PacketSchedule()
        for k in range(15):s.step(k,k in (5,10))
        with self.assertRaises(ContractViolation):s.step(15,True)
        self.assertEqual(s.last_tick,14)
        s.step(15,False)
        with self.assertRaises(ContractViolation):s.step(17)
        with self.assertRaises(ContractViolation):s.step(16,True)

    def test_mask_enumeration_matches_brute_force_all_phases(self):
        for start in range(5):
            for missed in range(3):
                opportunities=[k for k in range(start+1,start+26) if k%5==0]
                valid=[]
                for bits in itertools.product((0,1),repeat=len(opportunities)):
                    count=missed;arrivals=[];ok=True
                    for t,arrived in zip(opportunities,bits):
                        count=0 if arrived else count+1
                        ok &= count<=2
                        if arrived:arrivals.append(t)
                    if ok:valid.append(tuple(arrivals))
                self.assertEqual(set(enumerate_masks(start,missed,25)),set(valid))

    def test_filter_rejects_future_values_and_unexpected_channels(self):
        b=Box.from_center(C['initial_set']['center'],C['initial_set']['halfwidth'])
        obs=plant.observe(b.center,0,(0,1,4,5),np.zeros(6),C)
        f=BoxSMF(b,obs,C)
        with self.assertRaises(ContractViolation):f.advance([9.81,0],Observation(2,(4,5),[0,0],[.005,.01]))
        with self.assertRaises(ContractViolation):f.advance([9.81,0],Observation(1,(2,4,5),[0,0,0],[.01,.005,.01]))
        self.assertEqual(f.tick,0)

    def test_filter_enforces_packet_contract_without_schedule(self):
        b=Box.from_center(C['initial_set']['center'],C['initial_set']['halfwidth'])
        f=BoxSMF(b,plant.observe(b.center,0,(0,1,4,5),np.zeros(6),C),C)
        for k in range(1,15):f.advance([9.81,0],Observation(k,(4,5),[0,0],[.005,.01]))
        with self.assertRaises(ContractViolation):f.advance([9.81,0],Observation(15,(4,5),[0,0],[.005,.01]))
        self.assertEqual(f.tick,14)

    def test_filter_has_no_truth_import(self):
        tree=ast.parse((ROOT/'src/smf_mpc/filter.py').read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom):self.assertNotIn('plant',node.module or '')
            if isinstance(node,(ast.Import,ast.ImportFrom)):
                for name in node.names:self.assertNotIn('plant',name.name)

    def test_zonotope_strip_membership_via_lp(self):
        rng=rng_for(70001,'strip_lp');z=Zonotope(np.zeros(2),np.array([[.2,.3],[.1,-.2]]))
        Cmat=np.array([[1.,0.]])
        for _ in range(30):
            x=z.center+z.generators@rng.uniform(-1,1,2)
            obs=Cmat@x+np.array([rng.uniform(-.02,.02)])
            out=z.strip(Cmat,obs,[.02])
            lp=linprog(np.zeros(out.generators.shape[1]),A_eq=out.generators,b_eq=x-out.center,
                       bounds=[(-1,1)]*out.generators.shape[1],method='highs')
            self.assertTrue(lp.success)
            self.assertLess(np.max(np.abs(out.generators@lp.x-(x-out.center))),1e-8)

    def test_generator_reduction_outer_support(self):
        rng=rng_for(70002,'reduction');z=Zonotope(np.zeros(3),rng.normal(size=(3,20)))
        out=z.reduce(8)
        self.assertEqual(out.generators.shape,(3,8))
        for a in rng.normal(size=(100,3)):
            self.assertLessEqual(np.abs(z.generators.T@a).sum(),np.abs(out.generators.T@a).sum()+1e-10)

    def test_episode_split_and_window_isolation(self):
        self.assertEqual(split_for(70001),'g1_pilot')
        self.assertEqual(split_for(40000),'test')
        a=windows('episode-a',10000,101,25);b=windows('episode-b',20000,101,25)
        self.assertEqual({r['split'] for r in a},{'train'})
        self.assertEqual({r['split'] for r in b},{'validation'})
        self.assertTrue(all(r['stop_exclusive']<=101 for r in a))
        with self.assertRaises(ValueError):split_for(12000)
        np.testing.assert_array_equal(rng_for(70001,'a').normal(size=10),rng_for(70001,'a').normal(size=10))
        self.assertNotEqual(rng_for(70001,'a').normal(),rng_for(70001,'b').normal())


if __name__=='__main__':unittest.main()
