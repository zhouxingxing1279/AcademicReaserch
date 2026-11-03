import unittest
from fractions import Fraction as F
from check_run259_rolling_anchor import (
    roll, reset_width_cap, physical_zero_witness, verify,
)
from check_run258_delayed_anchor import branch_at_40


class TestRun259RollingAnchor(unittest.TestCase):
    def test_seven_legal_patterns(self):
        self.assertEqual(set(verify()['position_packet_patterns']),
                         {'SSS','SSM','SMS','SMM','MSS','MSM','MMS'})

    def test_three_misses_rejected(self):
        with self.assertRaises(ValueError): roll('MMM')

    def test_forced_success_45(self):
        rec, mem = roll('MMS')
        self.assertEqual(rec['45']['packet'], 'S')
        self.assertEqual(rec['45']['anchor_age_steps'], 15)
        self.assertEqual(mem, 15)
        self.assertLess(F(rec['45']['velocity_width']), 1)

    def test_age_five_ten_fifteen(self):
        for pat, n in [('SSS',5),('SMS',10),('MMS',15)]:
            self.assertEqual(roll(pat)[0]['45']['anchor_age_steps'], n)

    def test_uniform_reset_caps(self):
        for n in (5,10,15):
            self.assertLess(reset_width_cap(n), F(11,10))
        self.assertLess(reset_width_cap(10), reset_width_cap(15))
        self.assertLess(reset_width_cap(15), reset_width_cap(5))

    def test_all_post_pulse_resets_below_cap(self):
        for pat in ('SSS','SSM','SMS','SMM','MSS','MSM','MMS'):
            for item in roll(pat)[0].values():
                if item['packet']=='S' and item['previous_anchor_tick']>=35:
                    self.assertLessEqual(F(item['velocity_width']),
                                         reset_width_cap(item['anchor_age_steps']))

    def test_forgetting_old_anchor_is_conservative(self):
        s40,_=branch_at_40(True,True)
        self.assertGreater(F(roll('SSS')[0]['40']['velocity_width']),
                           s40['v'][1]-s40['v'][0])

    def test_zero_witness_all_three_ticks(self):
        witness=physical_zero_witness()
        self.assertEqual(set(witness),{'35','40','45'})
        for pat in ('SSS','SSM','SMS','SMM','MSS','MSM','MMS'):
            rec,_=roll(pat)
            for tick in witness:
                lo,hi=(F(x) for x in rec[tick]['velocity'])
                wlo,whi=(F(x) for x in witness[tick]['velocity_outer'])
                self.assertLessEqual(lo,wlo)
                self.assertLessEqual(whi,hi)

    def test_nonzero_position_readings(self):
        for pat in ('SSS','SSM','SMS','SMM','MSS','MSM','MMS'):
            for y in (-F(1,100),F(1,100)):
                rec,_=roll(pat,{35:y,40:y,45:y})
                self.assertEqual(len(rec),3)

    def test_scope_flags(self):
        r=verify()
        self.assertFalse(r['complete_cz_or_hrep_filter'])
        self.assertFalse(r['terminal_information_invariance_proved'])
        self.assertFalse(r['recursive_feasibility_proved'])
        self.assertEqual(r['gate_A'],'blocked')


if __name__=='__main__':unittest.main()
