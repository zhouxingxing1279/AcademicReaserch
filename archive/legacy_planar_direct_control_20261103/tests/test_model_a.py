import copy,json,sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from smf_mpc.neural_model import ResidualMLP,features
from smf_mpc.residual_envelope import envelope,validate_envelope,true_acceleration_interval
from smf_mpc.learned_filter import learned_prediction
from smf_mpc.sets import Zonotope
from smf_mpc.zonotope_filter import contains
from smf_mpc import plant
C=json.loads((ROOT/'configs/planar_baseline.json').read_text())


class ModelATests(unittest.TestCase):
    def test_training_gradient_directions(self):
        rng=np.random.default_rng(74001);m=ResidualMLP.initialize();v=m.vector()
        x=rng.uniform(-1,1,(8,5));y=rng.normal(size=(8,2));_,g=m.loss_gradient(x,y)
        for _ in range(8):
            d=rng.normal(size=v.shape);d/=np.linalg.norm(d);eps=1e-6
            fd=(ResidualMLP.from_vector(v+eps*d).loss_gradient(x,y)[0]-ResidualMLP.from_vector(v-eps*d).loss_gradient(x,y)[0])/(2*eps)
            self.assertAlmostEqual(fd,g@d,places=7)

    def test_input_jacobian(self):
        m=ResidualMLP.initialize();x=np.array([.2,-.3,.5,.1,-.4]);eps=1e-6
        fd=np.column_stack([(m.predict(x+eps*d)-m.predict(x-eps*d))/(2*eps) for d in np.eye(5)])
        np.testing.assert_allclose(m.jacobian(x),fd,atol=1e-9)

    def test_interval_and_whole_box_remainder(self):
        rng=np.random.default_rng(74002);m=ResidualMLP.initialize();c=np.array([.2,-.1,.3,0,0]);r=np.array([.1,.2,.1,0,0])
        lo,hi=m.interval(c-r,c+r);bound=.5*m.directional_second_bound(c-r,c+r,r)
        for _ in range(100):
            d=rng.uniform(-1,1,5)*r;value=m.predict(c+d)
            self.assertTrue(np.all(value>=lo-1e-12) and np.all(value<=hi+1e-12))
            self.assertTrue(np.all(np.abs(value-m.predict(c)-m.jacobian(c)@d)<=bound+1e-12))

    def test_partition_cover_and_true_difference(self):
        m=ResidualMLP.initialize();cert,lo,hi,bound=envelope(m,C,7)
        self.assertEqual(len(lo),128)
        self.assertAlmostEqual(np.prod(hi-lo,axis=1).sum(),np.prod(np.array(cert['domain_upper'])-cert['domain_lower']))
        rng=np.random.default_rng(74003)
        for _ in range(200):
            point=rng.uniform(cert['domain_lower'],cert['domain_upper'])
            membership=np.all(point>=lo,axis=1)&np.all(point<=hi,axis=1)
            self.assertEqual(membership.sum(),1)
            j=np.flatnonzero(membership)[0]
            state=np.array([0,2,3*point[0],3*point[1],.45*point[2],0]);u=np.array([9.81*(point[3]+1),.08*point[4]])
            a=plant.aerodynamic_acceleration(state,u,point[5:])
            tl,th=true_acceleration_interval(lo[j:j+1],hi[j:j+1])
            self.assertTrue(np.all(a>=tl[0]-1e-12) and np.all(a<=th[0]+1e-12))
            self.assertTrue(np.all(np.abs(a-m.predict(point[:5]))<=bound[j]))

    def test_model_and_config_binding(self):
        m=ResidualMLP.initialize();cert,*_=envelope(m,C,2)
        with self.assertRaises(ValueError):validate_envelope(cert,ResidualMLP.initialize(1),C)
        changed=copy.deepcopy(C);changed['plant']['dt_s']=.1
        with self.assertRaises(ValueError):validate_envelope(cert,m,changed)
        np.testing.assert_array_equal(ResidualMLP.from_dict(m.to_dict()).vector(),m.vector())
        data=m.to_dict();data['arrays'][0][0][0]+=.01
        with self.assertRaises(ValueError):ResidualMLP.from_dict(data)

    def test_learned_prediction_contains_truth(self):
        m=ResidualMLP.initialize();cert,*_=envelope(m,C,5)
        z=Zonotope(np.array([0,2,.1,-.2,.1,0]),np.diag([.02,.02,.1,.1,.03,.01]));u=np.array([10.,.01])
        predicted,_=learned_prediction(z,u,C,m,cert);rng=np.random.default_rng(74004)
        for _ in range(30):
            x=z.center+z.generators@rng.uniform(-1,1,6)
            self.assertTrue(contains(predicted,plant.step(x,u,rng.uniform(-.5,.5,2),C)))


if __name__=='__main__':unittest.main()
