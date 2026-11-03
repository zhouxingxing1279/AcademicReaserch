import unittest
from fractions import Fraction as F
from check_run270_recovered_packet_fiber import (H, R, EPS_P, START, END, family, trajectory, check_legal, certificate)

class Run270Tests(unittest.TestCase):
    def test_exact_last_seven(self):
        a,b=family(7)
        self.assertEqual(a[60][0], H*H*R*21)
        self.assertEqual(a[60][1], 7*H*R)
        self.assertEqual(a[60][0]-b[60][0], 42*H*H*R)
        self.assertEqual(a[60][1]-b[60][1], 14*H*R)

    def test_common_success_measurement(self):
        a,b=family(7)
        self.assertLessEqual(abs(a[60][0]), EPS_P)
        self.assertLessEqual(abs(b[60][0]), EPS_P)
        self.assertEqual(a[60][0]+(-a[60][0]), F(0))
        self.assertEqual(b[60][0]+(-b[60][0]), F(0))

    def test_full_extreme_is_discriminated(self):
        a,b=family(15)
        self.assertGreater(a[60][0]-b[60][0], 2*EPS_P)

    def test_seven_not_eight_for_this_family(self):
        a,_=family(7)
        b,_=family(8)
        self.assertLessEqual(abs(a[60][0]), EPS_P)
        self.assertGreater(abs(b[60][0]), EPS_P)

    def test_all_hard_boxes_each_tick(self):
        for j in (1,7,8,15):
            for sign in (-1,1):
                self.assertTrue(check_legal(trajectory(sign,60-j)))

    def test_angular_outputs_indistinguishable(self):
        a,b=family(7)
        self.assertTrue(all(a[k][2:]==b[k][2:]==(F(0),F(0)) for k in range(45,61)))

    def test_no_position_observation_at_misses(self):
        c=certificate()
        self.assertIn('tick50/55 miss',c['packets'])
        self.assertEqual(c['last_seven_disturbance_ticks'],list(range(53,60)))

    def test_certification_limits(self):
        c=certificate()
        self.assertEqual(c['gate_A'],'blocked')
        self.assertIn('actual Run260 tick45 posterior',' '.join(c['not_certified']))
        self.assertEqual(c['post_success_velocity_diameter_floor'],str(14*H*R))

if __name__ == '__main__':
    unittest.main()
