import unittest
from fractions import Fraction as F
from check_run258_delayed_anchor import (
    branch_at_35, branch_at_40, predict_35_to_40,
    velocity_from_position_anchor, uniform_anchor_width,
    physical_zero_witness, verify,
)
from check_run255_posterior_bridge import NOISE, posterior30

class TestRun258DelayedAnchor(unittest.TestCase):
    def test_start_is_run254(self):
        self.assertEqual(posterior30()['v'],(-F(269364701,200000000),F(269364701,200000000)))

    def test_success35_shrinks(self):
        _,s35,_=branch_at_35(True)
        _,miss35,_=branch_at_35(False)
        self.assertLess(s35['v'][1]-s35['v'][0],miss35['v'][1]-miss35['v'][0])

    def test_two_branches_have_five_acceleration_bounds(self):
        for b in (True,False):
            _,s35,_=branch_at_35(b)
            rows,a=predict_35_to_40(s35)
            self.assertEqual((len(rows),len(a)),(6,5))
            self.assertTrue(all(lo<=hi for lo,hi in a))

    def test_ten_step_identity_zero_acceleration(self):
        y=F(0);p=(-F(1,50),F(1,50));a=[(F(0),F(0))]*10
        lo,hi=velocity_from_position_anchor(y,p,a)
        self.assertEqual((lo,hi),(-F(1,5),F(1,5)))
        self.assertEqual(uniform_anchor_width(p,a),F(2,5))

    def test_miss35_success40_recovers_velocity(self):
        ms,_=branch_at_40(False,True)
        mm,_=branch_at_40(False,False)
        self.assertLess(ms['v'][1]-ms['v'][0],F(9,10))
        self.assertGreater(mm['v'][1]-mm['v'][0],F(7,2))

    def test_all_four_packet_branches(self):
        c=verify()['branches']
        self.assertEqual(set(c),{'SS','SM','MS','MM'})
        self.assertEqual(c['SS']['tick40_velocity_width'],c['MS']['tick40_velocity_width'])
        self.assertNotEqual(c['SM']['tick40_velocity_width'],c['MM']['tick40_velocity_width'])

    def test_uniform_bound_is_independent_of_reading(self):
        _,s35,a30=branch_at_35(False)
        _,a35=predict_35_to_40(s35)
        anchor=posterior30()['p'];acc=a30+a35
        for y in (-F(1,10),F(0),F(1,10)):
            lo,hi=velocity_from_position_anchor(y,anchor,acc)
            self.assertEqual(hi-lo,uniform_anchor_width(anchor,acc))

    def test_physical_witness_both_successes(self):
        w=physical_zero_witness()
        self.assertEqual(set(w),{'35','40'})
        for v in w.values():
            self.assertEqual(v['phi'],'0')
            self.assertEqual(v['omega'],'0')
            self.assertLessEqual(abs(F(v['p'][0])),NOISE['p'])
            self.assertLessEqual(abs(F(v['p'][1])),NOISE['p'])

    def test_no_false_invariance(self):
        c=verify()
        self.assertFalse(c['full_posterior_recursive_filter'])
        self.assertFalse(c['terminal_information_invariance_proved'])
        self.assertFalse(c['recursive_feasibility_proved'])

if __name__=='__main__':unittest.main()
