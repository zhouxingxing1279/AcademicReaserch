import itertools
import unittest
from fractions import Fraction as Q
from check_four_tick_affine_backup import (load_contract,read_rows,radii_from_run202,
                                           propagate_affine,initial,constrain,audit,run,radius,step,filter_torque)

class FourTickAffineBackupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=load_contract();cls.row=read_rows()[(10,'high')]
    def test_contract(self):
        self.assertEqual((self.c['h'],self.c['J']),(Q(1,50),Q(1,50)))
        self.assertEqual(self.c['limits'],(Q(5),Q(3),Q(9,20),Q(2)))
    def test_residual(self):
        self.assertEqual(radius(self.c['tmax']),Q(6731149,3200000))
    def test_interval_exact(self):
        self.assertEqual(constrain((Q(-1),Q(1)),Q(1,2),Q(1),Q(3,4)),(Q(-1),Q(1,4)))
        self.assertEqual(constrain((Q(-1),Q(1)),Q(1,2),Q(-1),Q(3,4)),(Q(-1,4),Q(1)))
    def test_run202_success_tighter(self):
        a=radii_from_run202(self.row,'success',self.c)
        b=radii_from_run202(self.row,'miss',self.c)
        self.assertTrue(all(x<=y for x,y in zip(a,b)))
    def test_origin_all_torques_safe_four_ticks(self):
        a=audit((Q(0),)*4,radii_from_run202(self.row,'success',self.c),self.c['tmax'],self.c)
        self.assertEqual((a['lower'],a['upper']),('-2/25','2/25'))
    def test_shifted_velocity_packet_changes_hard_admission(self):
        center=(Q(0),Q(47,20),Q(0),Q(0))
        yes=audit(center,radii_from_run202(self.row,'success',self.c),self.c['tmax'],self.c)
        no=audit(center,radii_from_run202(self.row,'miss',self.c),self.c['tmax'],self.c)
        self.assertTrue(yes['feasible']);self.assertFalse(no['feasible'])
    def test_shifted_attitude_rejects_positive_torque(self):
        center=(Q(0),Q(0),Q(19,50),Q(4,5))
        a=audit(center,radii_from_run202(self.row,'success',self.c),self.c['tmax'],self.c)
        self.assertTrue(a['feasible']);self.assertLess(Q(a['upper']),Q(1,100))
        self.assertGreaterEqual(Q(a['upper']),Q(0))
    def test_all_vertices_checked(self):
        a=audit((Q(0),)*4,radii_from_run202(self.row,'success',self.c),self.c['tmax'],self.c)
        self.assertEqual(a['inequalities'],4*4*8)
    def test_multiaffine_interior_thrust_by_corner_convex_combination(self):
        # For each signed coordinate and fixed tau, multi-affine interpolation
        # between the 2^3 endpoint outcomes encloses every interior T triple.
        c=self.c;rad=radii_from_run202(self.row,'success',c)
        tmid=(c['tmin']+c['tmax'])/2
        def endpoint(tseq,tau):
            state=(*initial((Q(0),)*4,rad)[:1],(Q(0),)*4,initial((Q(0),)*4,rad)[1])
            for k,t in enumerate(tseq):state=propagate_affine(state,t,k,c)
            center,coef,gens=state
            return tuple((center[i]+coef[i]*tau,sum(abs(g[i]) for g in gens)) for i in range(4))
        for tau in (-c['umax'],Q(0),c['umax']):
            corners=[endpoint((c['tmax'],)+f,tau) for f in itertools.product((c['tmin'],c['tmax']),repeat=3)]
            interior=endpoint((c['tmax'],tmid,tmid,tmid),tau)
            for i in range(4):
                low=min(a[i][0]-a[i][1] for a in corners)
                high=max(a[i][0]+a[i][1] for a in corners)
                self.assertGreaterEqual(interior[i][0]-interior[i][1],low)
                self.assertLessEqual(interior[i][0]+interior[i][1],high)
    def test_affine_support_matches_all_state_and_residual_corners(self):
        c=self.c
        rad=radii_from_run202(self.row,'success',c)
        center=(Q(0),Q(47,20),Q(0),Q(0))
        thrusts=(c['tmax'],c['tmin'],c['tmax'],c['tmin'])
        for tau in (Q(-2,25),Q(0),Q(2,25)):
            state=(center,(Q(0),)*4,initial(center,rad)[1])
            for k,t in enumerate(thrusts):state=propagate_affine(state,t,k,c)
            x,b,gens=state
            exact=tuple(abs(x[i]+b[i]*tau)+sum(abs(g[i]) for g in gens) for i in range(4))
            observed=[Q(0)]*4
            for signs in itertools.product((-1,1),repeat=8):
                actual=tuple(center[i]+rad[i]*signs[i] for i in range(4))
                for k,t in enumerate(thrusts):
                    actual=step(actual,t,tau if k==0 else Q(0),c)
                    actual=(actual[0],actual[1]+c['h']*radius(t)*signs[4+k],actual[2],actual[3])
                for i in range(4):observed[i]=max(observed[i],abs(actual[i]))
            self.assertEqual(tuple(observed),exact)

    def test_fourth_tick_torque_affects_position_but_not_first_three(self):
        c=self.c;state=((Q(0),)*4,(Q(0),)*4,())
        for k in range(4):
            state=propagate_affine(state,c['tmax'],k,c)
            self.assertEqual(state[1][0]==0,k<3)
        self.assertNotEqual(state[1][0],0)

    def test_shifted_velocity_miss_has_explicit_hard_violation_witness(self):
        c=self.c;rad=radii_from_run202(self.row,'miss',c)
        # At tau=0 and T0=T1=T2=T3=Tmax, the positive-velocity
        # box vertex with the worst residual signs breaches |v|<=3.
        x=(rad[0],Q(47,20)+rad[1],-rad[2],-rad[3])
        for _ in range(4):
            x=step(x,c['tmax'],Q(0),c)
            x=(x[0],x[1]+c['h']*radius(c['tmax']),x[2],x[3])
        self.assertGreater(x[1],c['limits'][1])

    def test_projection_safety_filter(self):
        c=self.c;center=(Q(0),Q(0),Q(19,50),Q(4,5))
        a=audit(center,radii_from_run202(self.row,'success',c),c['tmax'],c)
        self.assertEqual(filter_torque(Q(1,25),a),Q(1,300))
        self.assertEqual(filter_torque(Q(-1,25),a),Q(-1,25))
        b=audit((Q(0),Q(47,20),Q(0),Q(0)),radii_from_run202(self.row,'miss',c),c['tmax'],c)
        self.assertIsNone(filter_torque(Q(0),b))

    def test_run_shape(self):
        d=run();self.assertEqual(len(d['rows']),6);self.assertEqual(d['gate_A'],'blocked')

if __name__=='__main__':unittest.main()
