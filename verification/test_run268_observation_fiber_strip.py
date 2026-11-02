import math
import unittest
from fractions import Fraction as F
from check_run268_observation_fiber_strip import (
    H, T, R, EP, futures, latest_pair, weights, strip, certificate
)

class TestRun268(unittest.TestCase):
    def test_packet_automaton(self):
        self.assertEqual((len(list(futures('SMM'))), len(list(futures('MMS')))), (4, 7))
        for mode in ('SMM', 'MMS'):
            for seq in futures(mode):
                s, t = latest_pair(mode, seq)
                self.assertIn(t-s, (5, 10, 15))

    def test_euler_telescoping_exact_linear_acceleration(self):
        for s, t in [(35, 50), (45, 50), (45, 60), (50, 60), (55, 60)]:
            p, v = F(1, 9), F(2, 7)
            ps = p
            aa = {i: F(i-47, 71) for i in range(s, 60)}
            pt = None
            for i in range(s, 60):
                p, v = p + H*v, v + H*aa[i]
                if i+1 == t:
                    pt = p
            predicted = (pt-ps)/((t-s)*H) + H*sum((c*aa[i] for i,c in weights(s,t)),F(0))
            self.assertEqual(v, predicted)

    def test_exact_affine_residual_with_rational_linear_sine(self):
        for s,t in [(35,50),(45,60),(50,55),(55,60)]:
            z = strip(s,t)
            phi, omega = F(1,200), F(1,200)
            p, v = F(0), F(1,5)
            ps = p
            pt = None
            for i in range(s,60):
                a = -T*(phi-(60-i)*H*omega)+R/3
                p, v = p+H*v, v+H*a
                if i+1==t: pt=p
            dy = pt-ps
            residual = v + z['phi_coefficient']*phi + z['omega_coefficient']*omega - dy/((t-s)*H)
            self.assertLessEqual(abs(residual), z['E'])

    def test_analytic_remainder(self):
        for mode in ('SMM','MMS'):
            for seq in futures(mode):
                s,t=latest_pair(mode,seq)
                z=strip(s,t)
                self.assertLess(z['Q'], F(1,100000))
                self.assertGreater(z['radius'],z['E'])
                self.assertGreater(z['E'],0)
                self.assertLess(z['E'],F(1))

    def test_sampled_nonlinear_truth_inside_strip(self):
        # Empirical cross-check only; proof uses analytic Taylor remainder.
        for s,t in [(35,50),(45,60),(50,55),(55,60)]:
            z=strip(s,t)
            for sign in (-1,1):
                phi,omega=sign*0.007,sign*0.009
                p,v=0.01,0.1
                ps=p
                for i in range(s,60):
                    r=sign*float(R)*0.8
                    angle=phi-(60-i)*float(H)*omega
                    p,v=p+float(H)*v,v+float(H)*(-float(T)*math.sin(angle)+r)
                    if i+1==t: pt=p
                ys=ps+sign*float(EP)*0.9
                yt=pt-sign*float(EP)*0.9
                lhs=v+float(z['phi_coefficient'])*phi+float(z['omega_coefficient'])*omega-(yt-ys)/((t-s)*float(H))
                self.assertLessEqual(abs(lhs),float(z['radius'])+1e-12)

    def test_certificate(self):
        c=certificate()
        self.assertEqual(c['gate_A'],'blocked')
        self.assertEqual(sum(map(len,c['branches'].values())),11)

if __name__=='__main__': unittest.main()
