import json,sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from smf_mpc.affine_model import AffineResidualMLP
from smf_mpc.neural_model import ResidualMLP
from smf_mpc.affine_filter import affine_learned_prediction
from smf_mpc.sets import Zonotope
from smf_mpc.zonotope_filter import contains
from smf_mpc import plant

class AffineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model=AffineResidualMLP.from_dict(json.loads((ROOT/'results/model_a_20260909/model.json').read_text()))
        cls.config=json.loads((ROOT/'configs/planar_baseline.json').read_text())
    def test_trained_taylor_enclosure_and_interval(self):
        m=self.model;rng=np.random.default_rng(75001)
        for _ in range(80):
            c=rng.uniform(-.8,.8,5);r=rng.uniform(0,.4,5)
            r[4]=0
            center,G,error=m.affine_box(c-r,c+r)
            np.testing.assert_allclose(G,m.jacobian(c)*r,atol=1e-12)
            lo,hi=m.interval(c-r,c+r)
            oldlo,oldhi=ResidualMLP.interval(m,c-r,c+r)
            self.assertTrue(np.all(lo>=oldlo) and np.all(hi<=oldhi))
            for d in rng.uniform(-1,1,(30,5))*r:
                value=m.predict(c+d)
                self.assertTrue(np.all(value>=lo-1e-11) and np.all(value<=hi+1e-11))
                self.assertTrue(np.all(np.abs(value-center-m.jacobian(c)@d)<=error+1e-11))
    def test_batch_and_zero_width(self):
        m=self.model;c=np.array([[0,.1,-.5,0,0],[.9,-.9,.2,0,0]])
        a=m.affine_box(c-.1,c+.1)
        for i in range(2):
            b=m.affine_box(c[i]-.1,c[i]+.1)
            for x,y in zip(a,b):np.testing.assert_allclose(x[i],y,atol=1e-12)
        lo,hi=m.interval(c,c);np.testing.assert_allclose(lo,m.predict(c),atol=1e-12);np.testing.assert_allclose(hi,m.predict(c),atol=1e-12)
    def test_prediction_membership(self):
        cert=json.loads((ROOT/'results/affine_model_a_20260909/envelope.json').read_text())
        z=Zonotope(np.array([0,2,.1,-.2,.1,0]),np.diag([.02,.02,.1,.1,.03,.01]));u=np.array([10.,.01])
        pred,_=affine_learned_prediction(z,u,self.config,self.model,cert)
        rng=np.random.default_rng(75002)
        for _ in range(100):
            x=z.center+z.generators@rng.uniform(-1,1,6)
            self.assertTrue(contains(pred,plant.step(x,u,rng.uniform(-.5,.5,2),self.config)))
if __name__=='__main__':unittest.main()
