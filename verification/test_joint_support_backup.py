"""Run216 focused exact-rational tests, no external optimizer needed."""
import unittest
from fractions import Fraction as Q
import check_joint_support_backup as j


class JointSupportBackupTests(unittest.TestCase):
    def test_polygon_exact_support_and_boundary(self):
        box=((Q(-1),Q(1)),(Q(-1),Q(1)))
        p=j.polygon(box,((Q(1),Q(1),Q(0)),(-Q(1),-Q(1),Q(0))))
        self.assertEqual(j.support(p,1,1),0)
        self.assertEqual(j.support(p,1,0),1)
        self.assertEqual(j.support(p,-1,0),1)
        self.assertTrue(all(x+y==0 for x,y in p))
        self.assertTrue(j.contains(p,(Q(1,2),Q(-1,2))))
        self.assertFalse(j.contains(p,(Q(1,2),Q(1,2))))

    def test_empty_intersection_is_not_silently_accepted(self):
        self.assertEqual(j.polygon(((Q(0),Q(1)),(Q(0),Q(1))),((1,0,-1),)),())
        with self.assertRaises(ValueError):j.support((),1,0)

    def test_degenerate_singleton(self):
        p=j.polygon(((Q(1),Q(1)),(Q(-2),Q(-2))),((1,0,1),))
        self.assertEqual(j.support(p,Q(3,7),Q(-4,9)),Q(3,7)+Q(8,9))
        self.assertTrue(j.contains(p,(Q(1),Q(-2))))
        self.assertFalse(j.contains(p,(Q(2),Q(-2))))
        p0=j.polygon(((Q(1),Q(1)),(Q(-2),Q(-2))))
        self.assertTrue(j.contains(p0,(Q(1),Q(-2))))
        self.assertFalse(j.contains(p0,(Q(1),Q(-1))))

    def test_box_vs_joint_strict_control_recovery(self):
        box=((Q(-5),Q(5)),(Q(-2),Q(2)),(Q(0),Q(0)),(Q(0),Q(0)))
        base=j.joint_backup(box,j.TMAX)
        pv=j.polygon(box[:2],((Q(1),Q(1),Q(0)),(-Q(1),-Q(1),Q(0))))
        joint=j.joint_backup(box,j.TMAX,pv,j.polygon(box[2:]))
        self.assertFalse(base['feasible'],base)
        self.assertTrue(joint['feasible'],joint)
        self.assertLessEqual(Q(joint['lower']),Q(joint['upper']))

    def test_reachable_tick193_obstruction_in_source_compatible_replay(self):
        d=j.integration_tick193()
        self.assertFalse(d['baseline']['feasible'])
        self.assertFalse(d['joint']['feasible'])
        self.assertTrue(d['truth_in_joint_outer'])
        w=d['obstruction']
        self.assertTrue(w['individually_impossible'])
        self.assertEqual((w['physical_step'],w['state_index'],w['constraint_sign']),(5,1,-1))
        self.assertLess(Q(w['best_case_slack_exact']),0)
        self.assertEqual(Q(d['critical_row_support_gain_exact']),Q(57617501,1440000000))

    def test_no_change_for_full_box(self):
        box=((Q(-1,50),Q(1,50)),(Q(-1,10),Q(1,10)),
             (Q(-1,200),Q(1,200)),(Q(-1,100),Q(1,100)))
        a=j.joint_backup(box,j.TMAX)
        b=j.joint_backup(box,j.TMAX,j.polygon(box[:2]),j.polygon(box[2:]))
        self.assertEqual((a['feasible'],a['lower'],a['upper']),
                         (b['feasible'],b['lower'],b['upper']))

    def test_history_polygons_causal_and_truth_support(self):
        # One transition from exact zero, no residual, zero torque.
        box=((Q(-1),Q(1)),(Q(-1),Q(1)),(Q(-1,10),Q(1,10)),(Q(-1,10),Q(1,10)))
        positions={0:Q(0)}; attitudes={0:Q(0)}
        thrusts={0:j.TMAX};torques={0:Q(0)}
        p,a=j.history_polygons(box,positions,attitudes,thrusts,torques,1)
        self.assertGreaterEqual(j.support(p,1,0),0)
        self.assertGreaterEqual(j.support(p,-1,0),0)
        self.assertGreaterEqual(j.support(a,1,0),0)
        self.assertGreaterEqual(j.support(a,-1,0),0)
        with self.assertRaises(ValueError):
            j.history_polygons(box,positions,{},thrusts,torques,1)

    def test_rows_are_robust_for_exact_vertex_trajectories(self):
        box=((Q(-1,10),Q(1,10)),(Q(-1,10),Q(1,10)),
             (Q(-1,100),Q(1,100)),(Q(-1,100),Q(1,100)))
        pv=j.polygon(box[:2]);ao=j.polygon(box[2:])
        thrusts=(j.TMAX,j.TMIN,j.TMAX,j.TMIN,j.TMAX)
        rows=j.rows_for_future(pv,ao,thrusts)
        self.assertEqual(len(rows),40)
        # Each row is an exact upper bound over the joint outer set and all
        # independent residuals.  For zero controls, sample extreme vertices.
        for x in ((a,b,c,d) for a,b in pv for c,d in ao):
            for signs in ((1,1,1,1,1),(-1,-1,-1,-1,-1)):
                state=x
                for k,(t,s) in enumerate(zip(thrusts,signs)):
                    state=j.step(state,t)
                    state=(state[0],state[1]+j.H*s*j.rad(t),state[2],state[3])
                    for i in range(4):
                        for sg in (-1,1):
                            row=rows[k*8+i*2+(sg+1)//2]
                            self.assertLessEqual(sg*state[i],j.LIMITS[i]-row[2])

if __name__=='__main__':unittest.main()
