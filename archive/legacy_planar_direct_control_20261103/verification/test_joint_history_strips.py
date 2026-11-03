"""Focused exact-rational tests; repository integration test is conditional."""
import unittest
from fractions import Fraction as Q
from check_joint_history_strips import (position_velocity_strip, attitude_rate_strip,
                                        residual, audit_corner, position_support_three_packets)

H=Q(1,50)


class JointHistoryStripsTests(unittest.TestCase):
    def test_exact_euler_position_velocity_identity_with_uncertainty(self):
        p,v=Q(1,3),Q(-2,5)
        positions={0:p}
        attitudes={i:Q(i-2,100) for i in range(5)}
        thrusts={i:Q(5+i,1) for i in range(5)}
        for i in range(5):
            a=-thrusts[i]*attitudes[i]+Q(i-2,10)
            p,v=p+H*v,v+H*a
        strip=position_velocity_strip(0,positions[0],5,attitudes,thrusts)
        self.assertLessEqual(residual(p-5*H*v,strip),0)

    def test_attitude_rate_exact_and_noisy(self):
        phi,omega,u=Q(3,10),Q(-1,2),Q(1,25)
        phi_next=phi+H*omega
        omega_next=omega+u
        strip=attitude_rate_strip(phi,u)
        self.assertLessEqual(residual(phi_next-H*omega_next,strip),0)
        self.assertGreater(residual(phi_next-H*omega_next+Q(1,10),strip),0)

    def test_joint_box_corner_can_be_excluded(self):
        # True trajectory is zero; a wide independent box includes a false corner.
        box=((Q(-1),Q(1)),(Q(-1),Q(1)),(Q(-1),Q(1)),(Q(-1),Q(1)))
        positions={0:Q(0)}
        attitudes={0:Q(0)}
        thrusts={0:Q(5)}
        torques={0:Q(0)}
        result=audit_corner(box,positions,attitudes,thrusts,torques,1)
        self.assertTrue(result['excluded'])
        self.assertEqual(result['status'],'excluded_by_necessary_history_strip')

    def test_consistent_singleton_is_not_excluded(self):
        box=((Q(0),Q(0)),)*4
        result=audit_corner(box,{0:Q(0)},{0:Q(0)},{0:Q(5)},{0:Q(0)},1)
        self.assertFalse(result['excluded'])

    def test_three_packet_position_support_contains_true_state(self):
        p,v=Q(1,3),Q(-2,5)
        positions={0:p}
        attitudes={i:Q(i-2,100) for i in range(5)}
        thrusts={i:Q(5+i,1) for i in range(5)}
        for i in range(5):
            if i==2:positions[2]=p
            if i==4:positions[4]=p
            a=-thrusts[i]*attitudes[i]+Q(i-2,10)
            p,v=p+H*v,v+H*a
        lo,hi=position_support_three_packets(((0,positions[0]),(2,positions[2]),
            (4,positions[4])),attitudes,thrusts,5,Q(7,3))
        self.assertLessEqual(lo,p)
        self.assertLessEqual(p,hi)

    def test_three_packet_rejects_missing_history(self):
        with self.assertRaises(ValueError):
            position_support_three_packets(((0,Q(0)),(2,Q(0)),(4,Q(0))),
                {0:Q(0)},{0:Q(5)},5,Q(7,3))

    def test_run214_reachable_corner_excluded_but_backup_refused(self):
        from check_joint_history_strips import audit_reachable_run214
        result=audit_reachable_run214()
        self.assertEqual(result['position_lower_improvement_exact'],
                         '205895263/8000000000')
        self.assertTrue(result['original_corner_excluded_by_position_support'])
        self.assertFalse(result['refined_backup_feasible'])
        self.assertTrue(result['truth_contained'])

    def test_causality_rejects_missing_data(self):
        with self.assertRaises(ValueError):
            position_velocity_strip(1,Q(0),2,{}, {})
        with self.assertRaises(ValueError):
            audit_corner(((Q(0),Q(0)),)*4,{0:Q(0)},{0:Q(0)},{0:Q(5)}, {},1)


if __name__ == '__main__':unittest.main()
