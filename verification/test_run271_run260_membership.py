import unittest
from fractions import Fraction as F
from check_run271_run260_membership import (
    T,R,EPS,packet_automaton,shared_prefix,continuation,check_state_box,verify
)


class Run271Membership(unittest.TestCase):
    def test_packet_automaton(self):
        self.assertEqual(packet_automaton(),'SSSMMSMMSMMS')

    def test_prefix_pulse_returns_exact_zero(self):
        states,_=shared_prefix()
        self.assertEqual(states[45],(F(0),)*4)

    def test_pre45_disturbance_bound(self):
        _,a=shared_prefix()
        self.assertLessEqual(T*max(abs(x[0]) for x in a.values()),R)

    def test_two_trajectories_legal(self):
        check_state_box(continuation(1))
        check_state_box(continuation(-1))

    def test_tick60_common_measurement(self):
        a,b=continuation(1),continuation(-1)
        self.assertEqual(a[60][0],-b[60][0])
        self.assertLessEqual(abs(a[60][0]),EPS)

    def test_tick60_velocity_diameter(self):
        a,b=continuation(1),continuation(-1)
        self.assertEqual(a[60][1]-b[60][1],F(22724681,40000000))

    def test_same_angular_readings(self):
        a,b=continuation(1),continuation(-1)
        self.assertTrue(all(a[k][2:]==b[k][2:] for k in range(61)))

    def test_certificate(self):
        self.assertEqual(verify()['gate_A'],'blocked')


if __name__=='__main__':
    unittest.main()
