import unittest
from fractions import Fraction as F
from check_run275_two_packet_velocity_gate import H,R,EPS,G,patterns,pair,radius,threshold,witness,certificate
class TestGate(unittest.TestCase):
    def test_44(self): self.assertEqual(len(patterns()),44)
    def test_last_two_successes(self):
        for s in patterns():
            a,b=pair(s);self.assertIn(b-a,(5,10,15));self.assertLessEqual(90-b,10)
    def test_positive_gates(self):
        for s in patterns():
            a,b=pair(s);self.assertGreater(threshold(a,b),0)
    def test_euler_identity(self):
        for n in (1,5,10,15):
            p,v=F(7,100),F(1,4);p0=p
            for _ in range(n):p,v=p+H*v,v+H*R
            self.assertEqual(v,(p-p0)/(n*H)+H*(n+1)*R/2)
    def test_true_trajectories_44_patterns(self):
        for v0,sign in ((F(0),1),(F(3,2),1),(F(0),-1)):
            p,v=F(0),v0; pos={60:p}
            for k in range(60,90):
                r=sign*R if k%3 else -sign*R
                p,v=p+H*v,v+H*r;pos[k+1]=p
            for s in patterns():
                a,b=pair(s);delta=abs((pos[b]-EPS)-(pos[a]+EPS))
                self.assertLessEqual(abs(v),delta/((b-a)*H)+radius(a,b))
                if delta<=threshold(a,b):self.assertLessEqual(abs(v),G)
    def test_zero_readings_pass(self):
        for s in patterns():
            a,b=pair(s);self.assertGreaterEqual(threshold(a,b),0)
    def test_outer_box_negative(self):
        w=witness();self.assertGreater(F(w['v90']),G)
        self.assertGreater(F(w['displacement']),F(w['gate']))
        self.assertIn('unproved',w['scope'])
    def test_certificate(self):
        c=certificate();self.assertEqual(c['count'],44)
        self.assertEqual(sum(c['counts'].values()),44)
if __name__=='__main__':unittest.main()
