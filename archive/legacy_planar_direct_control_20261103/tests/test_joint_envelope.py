import copy,json,sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from smf_mpc.affine_model import AffineResidualMLP
from smf_mpc.joint_envelope import joint_envelope,analytic_affine
from smf_mpc.local_envelope import LocalEnvelope
from smf_mpc.residual_envelope import true_acceleration_interval
from smf_mpc.local_filter import local_learned_prediction
from smf_mpc.sets import Zonotope
from smf_mpc.zonotope_filter import contains
from smf_mpc import plant

class JointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d=ROOT/'results/joint_model_a_20260909'
        cls.m=AffineResidualMLP.from_dict(json.loads((d/'model.json').read_text()))
        cls.c=json.loads((ROOT/'configs/planar_baseline.json').read_text())
        cls.cert=json.loads((d/'envelope.json').read_text());a=np.load(d/'envelope_leaves.npz')
        cls.lo,cls.hi,cls.b=[a[k] for k in ('lower','upper','acceleration_halfwidth')]
        cls.table=LocalEnvelope(cls.cert,cls.m,cls.c,cls.lo,cls.hi,cls.b)
    def test_regenerate_all_cells(self):
        cert,lo,hi,b=joint_envelope(self.m,self.c)
        for x,y in ((lo,self.lo),(hi,self.hi),(b,self.b)):np.testing.assert_array_equal(x,y)
        old=np.load(ROOT/'results/affine_model_a_20260909/envelope_leaves.npz')['acceleration_halfwidth']
        self.assertTrue(np.all(b<=old+1e-12))
    def test_joint_samples_and_analytic_affine(self):
        rng=np.random.default_rng(76001);idx=rng.integers(0,len(self.lo),5000)
        lo,hi=self.lo[idx],self.hi[idx];p=rng.uniform(lo,hi);mid=(lo+hi)/2;r=(hi-lo)/2
        truth,_=true_acceleration_interval(p,p)
        forms=analytic_affine(lo,hi)
        for j,f in enumerate(forms):
            v=f.c+np.einsum('ij,ij->i',f.g,(p-mid)/r)
            self.assertTrue(np.all(np.abs(truth[:,j]-v)<=f.e+1e-11))
        self.assertTrue(np.all(np.abs(truth-self.m.predict(p[:,:5]))<=self.b[idx]+1e-11))
    def test_reject_missing_tampered_and_mismatched(self):
        with self.assertRaises(ValueError):LocalEnvelope(self.cert,self.m,self.c,self.lo[:-1],self.hi[:-1],self.b[:-1])
        b=self.b.copy();b[0]*=.9
        with self.assertRaises(ValueError):LocalEnvelope(self.cert,self.m,self.c,self.lo,self.hi,b)
        c=copy.deepcopy(self.c);c['plant']['dt_s']*=2
        with self.assertRaises(ValueError):LocalEnvelope(self.cert,self.m,c,self.lo,self.hi,self.b)
    def test_boundary_query_and_prediction(self):
        z=Zonotope(np.array([0,2,0,0,0,0]),np.diag([.02,.02,.05,.05,.02,.01]));u=np.array([9.81,0])
        bound,count=self.table.query(z,u);self.assertGreater(count,16)
        pred,_=local_learned_prediction(z,u,self.c,self.m,self.cert,self.table)
        rng=np.random.default_rng(76002)
        for _ in range(100):
            x=z.center+z.generators@rng.uniform(-1,1,6)
            self.assertTrue(contains(pred,plant.step(x,u,rng.uniform(-.5,.5,2),self.c)))
        with self.assertRaises(ValueError):self.table.query(z,[100,0])
if __name__=='__main__':unittest.main()
