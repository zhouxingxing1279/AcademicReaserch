import unittest
from fractions import Fraction as Q
from check_cross_block_history_support import (
    cross_block_packet_strip,strip_residual,one_strip_dual,
    multiple_strip_outer_support,product_support)

class CrossBlockTest(unittest.TestCase):
    def test_exact_identity_arbitrary_torques(self):
        h=Q(1,50); J=h
        x=(Q(2,3),Q(-3,5),Q(1,10),Q(-2,7))
        torques={i:Q(i-2,100) for i in range(5)}
        thrusts={i:Q(5+i,1) for i in range(5)}
        p0=x[0]
        for i in range(5):
            p,v,phi,omega=x
            x=(p+h*v,v-h*thrusts[i]*phi,phi+h*omega,
               omega+h/J*torques[i])
        strip=cross_block_packet_strip(0,p0,5,thrusts,torques,
                                       position_noise=Q(0),radius_fn=lambda t:Q(0))
        self.assertEqual(strip_residual(x,strip),0)
        self.assertNotEqual(strip[0][2],0)
        self.assertNotEqual(strip[0][3],0)

    def test_multiple_exact_histories(self):
        h=Q(1,50)
        for seed in range(1,15):
            x=(Q(seed,11),Q(seed-7,19),Q(seed-4,100),Q(3-seed,50))
            torques={i:Q((seed+3*i)%7-3,200) for i in range(2,7)}
            thrusts={i:Q(5+((seed+i)%4)) for i in range(2,7)}
            p2=x[0]
            for i in range(2,7):
                p,v,phi,omega=x
                x=(p+h*v,v-h*thrusts[i]*phi,phi+h*omega,omega+torques[i])
            strip=cross_block_packet_strip(2,p2,7,thrusts,torques,
                                           position_noise=Q(0),radius_fn=lambda t:Q(0))
            self.assertEqual(strip_residual(x,strip),0)

    def test_noise_and_disturbance_outer(self):
        h=Q(1,50)
        x=(Q(0),Q(1,4),Q(1,10),Q(1,5))
        torques={i:Q(-1,100) for i in range(4)}
        thrusts={i:Q(10) for i in range(4)}
        for i in range(4):
            p,v,phi,omega=x
            x=(p+h*v,v+h*(-10*phi+Q(1,3)),phi+h*omega,omega+torques[i])
        strip=cross_block_packet_strip(0,Q(1,100),4,thrusts,torques,
                                       position_noise=Q(1,50),
                                       radius_fn=lambda t:Q(1,2))
        self.assertLessEqual(strip_residual(x,strip),0)

    def test_dual_strict_gain_synthetic(self):
        square=((Q(-1),Q(-1)),(Q(1),Q(-1)),(Q(1),Q(1)),(Q(-1),Q(1)))
        q=(Q(0),Q(1),Q(1),Q(0))
        strip=((Q(0),Q(1),Q(1),Q(0)),Q(0),Q(1,5))
        r=one_strip_dual(square,square,q,strip)
        self.assertEqual(r['independent_upper'],2)
        self.assertEqual(r['upper'],Q(1,5))
        self.assertEqual(r['lambda'],1)

    def test_no_false_improvement_irrelevant_strip(self):
        square=((Q(-1),Q(-1)),(Q(1),Q(-1)),(Q(1),Q(1)),(Q(-1),Q(1)))
        q=(Q(0),Q(1),Q(1),Q(0))
        strip=((Q(1),Q(0),Q(0),Q(0)),Q(0),Q(0))
        r=multiple_strip_outer_support(square,square,q,(strip,))
        self.assertEqual(r['upper'],2)

    def test_history_rejects_missing_torque(self):
        with self.assertRaises(ValueError):
            cross_block_packet_strip(0,0,2,{0:Q(5),1:Q(5)},{0:Q(0)})

if __name__=='__main__':unittest.main()
