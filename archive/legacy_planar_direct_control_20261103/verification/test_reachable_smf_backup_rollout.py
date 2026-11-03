"""Run206 regression tests, no external dependencies."""
import unittest
import sys
from pathlib import Path
from fractions import Fraction as Q
sys.path.insert(0,str(Path(__file__).resolve().parent))
import check_reachable_smf_backup_rollout as m

class TestReachableSMFBackup(unittest.TestCase):
    def test_contract_mirror(self):
        self.assertTrue(m.verify_contract())
    def test_interval_contains_true_step_extremes(self):
        box=m.initial_box()
        for t in (m.TMIN,m.TMAX,Q(10)):
            for u in (-m.UMAX,m.Z,m.UMAX):
                p=m.predict(box,t,u)
                for i in range(16):
                    x=tuple(box[j][(i>>j)&1] for j in range(4))
                    for sign in (-1,1):
                        nxt=m.step(x,t,u,sign*m.rad(t))
                        self.assertTrue(all(lo<=val<=hi for val,(lo,hi) in zip(nxt,p)))
    def test_measurement_updates_contain_truth(self):
        box=m.initial_box();x=(m.Z,)*4
        for s in (False,True):
            for noise in ((m.Z,)*4,(m.SIGMA[0],m.Z,-m.SIGMA[2],m.SIGMA[3])):
                post=m.observe(box,x,s,noise)
                self.assertTrue(all(lo<=val<=hi for val,(lo,hi) in zip(x,post)))
    def test_packet_velocity_identity(self):
        n=15;accels=[];x=(m.Z,)*4;old=x[0]
        for k in range(n):
            t=m.TMAX if k%2 else m.TMIN
            a=-t*x[2]+m.rad(t)
            accels.append((a,a))
            x=m.step(x,t,m.UMAX,m.rad(t))
        out=m.velocity_from_packets((old,old),(x[0],x[0]),accels)
        self.assertEqual(out,(x[1],x[1]))
    def test_packet_refinement_sound_and_tightens(self):
        b=m.initial_box();p0=b[0];acc=[];x=(m.Z,)*4
        for k in range(15):
            t=m.TMAX
            acc.append(m.add(m.scale(b[2],-t),(-m.rad(t),m.rad(t))))
            x=m.step(x,t,m.Z,m.rad(t))
            b=m.predict(b,t,m.Z)
            b=m.observe(b,x,k==14)
        v2=m.intersect(b[1],m.velocity_from_packets(p0,b[0],acc))
        self.assertLessEqual(v2[1]-v2[0],b[1][1]-b[1][0])
        self.assertLessEqual(v2[0],x[1]);self.assertGreaterEqual(v2[1],x[1])
    def test_four_tick_certificate_contains_vertex_trajectories(self):
        box=m.initial_box();t=m.TMAX
        cert=m.backup_audit(box,t)
        self.assertTrue(cert['feasible']);self.assertEqual(cert['inequalities'],128)
        for u in (Q(cert['lower']),Q(cert['upper']),m.Z):
            for future in ((m.TMIN,)*3,(m.TMAX,)*3,(m.TMIN,m.TMAX,m.TMIN)):
                for corner in range(16):
                    for rs in range(16):
                        x=tuple(box[i][(corner>>i)&1] for i in range(4))
                        for k,tk in enumerate((t,)+future):
                            x=m.step(x,tk,u if k==0 else m.Z,(1 if (rs>>k)&1 else -1)*m.rad(tk))
                            self.assertTrue(all(abs(v)<=lim for v,lim in zip(x,m.LIMITS)))
    def test_reachable_rollout_interval_refuses_without_violation(self):
        r=m.rollout('positive_high',100,'interval')
        self.assertEqual(r['accepted_ticks'],54)
        self.assertEqual(r['first_refusal']['tick'],55)
        self.assertEqual(r['first_refusal']['reason'],'empty_four_tick_backup_interval')
    def test_packet_refinement_delays_refusal(self):
        for scenario in ('positive_high','alternating_high','switch_positive'):
            a=m.rollout(scenario,100,'interval')
            b=m.rollout(scenario,100,'packet_velocity')
            self.assertGreater(b['accepted_ticks'],a['accepted_ticks'])
            self.assertGreaterEqual(b['packet_refinements'],1)
    def test_policy_rejects_invalid_current_box(self):
        bad=((Q(6),Q(7)),(-Q(1),Q(1)),(-Q(1,100),Q(1,100)),(-Q(1,100),Q(1,100)))
        cert=m.backup_audit(bad,m.TMAX)
        self.assertFalse(cert['feasible']);self.assertEqual(cert['reason'],'current_outer_box_outside_hard_limits')
    def test_invalid_noise_rejected(self):
        with self.assertRaises(AssertionError):
            m.observe(m.initial_box(),(m.Z,)*4,True,(Q(1),m.Z,m.Z,m.Z))

if __name__=='__main__':unittest.main()
