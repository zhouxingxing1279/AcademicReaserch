"""Exact standalone tests plus deterministic full-repository replay."""
import unittest
from fractions import Fraction as Q
import check_three_packet_velocity_support as s

class TestThreePacketSupport(unittest.TestCase):
    def test_identity(self):
        c,w=s.identity_weights()
        self.assertEqual(len(w),41)
        p0=Q(7,13);v0=Q(-3,7)
        a=[Q((i%9)-4,11) for i in range(41)]
        p=[p0];v=[v0]
        for ai in a:
            p.append(p[-1]+s.H*v[-1]);v.append(v[-1]+s.H*ai)
        self.assertEqual(v[41],sum((x*y for x,y in zip(c,(p[0],p[15],p[30]))),Q(0))+sum((x*y for x,y in zip(w,a)),Q(0)))

    def test_contains_feasible_truth(self):
        p=Q(1,4);v=Q(-1,5);phi=Q(1,20);t=s.TMAX
        obs=[];positions={0:p}
        for k in range(41):
            obs.append(phi)
            p=p+s.H*v
            v=v+s.H*(-t*phi+s.rad(t))
            if k+1 in (15,30):positions[k+1]=p
        lo,hi=s.measurement_support([positions[k] for k in (0,15,30)],obs,[t]*41)
        self.assertLessEqual(lo,v);self.assertLessEqual(v,hi)

    def test_exact_lower_relative_to_max_residual(self):
        c,w=s.identity_weights();t=s.TMAX
        # Zero-noise observations and actual residual at +rad: exact
        # displacement-independent gap between the support and true velocity.
        delta=-s.SIGMA_P*sum(map(abs,c),Q(0))
        delta-=sum((abs(wi)*(t*s.SIGMA_PHI+s.rad(t))+wi*s.rad(t) for wi in w),Q(0))
        self.assertEqual(delta,Q(-809569631,480000000))
        self.assertAlmostEqual(float(delta),-1.6866033979166667,places=12)
        # Historical JSON float values are only a diagnostic, not an exact replay.
        prior_truth=Q('-0.7331640043621591')
        prior_box=Q('-2.4931037251954926')
        self.assertGreater(prior_truth+delta-prior_box,Q(7,100))

    def test_full_run210_replay(self):
        r=s.replay_positive_high()
        self.assertEqual(r['tick'],192)
        self.assertEqual(Q(r['strict_lower_improvement']),Q(7040287,96000000))

if __name__=='__main__':unittest.main()
