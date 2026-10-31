import unittest
import os
from fractions import Fraction as Q
from check_cross_block_saturation import support_saturation, dot

class SaturationTest(unittest.TestCase):
    def setUp(self):
        self.sq = ((Q(-1), Q(-1)), (Q(1), Q(-1)),
                   (Q(1), Q(1)), (Q(-1), Q(1)))
        self.q = (Q(0), Q(-1), Q(1), Q(0))

    def test_exact_saturation_for_valid_strip(self):
        strip = ((Q(1), Q(0), Q(0), Q(0)), Q(1), Q(1))
        r = support_saturation(self.sq, self.sq, self.q, (strip,))
        self.assertTrue(r['saturated'])
        self.assertEqual(r['joint_support'], Q(2))
        self.assertEqual(r['strip_margins'], (Q(1),))

    def test_excluded_maximizer_is_inconclusive(self):
        strip = ((Q(0), Q(1), Q(-1), Q(0)), Q(0), Q(1,5))
        r = support_saturation(self.sq, self.sq, self.q, (strip,))
        self.assertFalse(r['saturated'])
        self.assertIsNone(r['joint_support'])

    def test_multiple_strips_with_joint_witness(self):
        strips = (((Q(1), Q(0), Q(0), Q(0)), Q(0), Q(1)),
                  ((Q(0), Q(1), Q(1), Q(0)), Q(0), Q(2)))
        r = support_saturation(self.sq, self.sq, self.q, strips)
        self.assertTrue(r['saturated'])
        self.assertEqual(r['joint_support'], Q(2))
        self.assertTrue(all(m >= 0 for m in r['strip_margins']))
        self.assertEqual(dot(self.q, r['witness']), Q(2))

    @unittest.skipUnless(os.environ.get('RUN_TICK193_AUDIT') == '1',
                         'requires complete repository replay dependencies')
    def test_reachable_tick193_saturation(self):
        from check_cross_block_saturation import audit_tick193
        r = audit_tick193()
        self.assertEqual(r['support_gain_exact'], '0')
        self.assertLess(r['old_best_case_slack_approx'], 0)

    def test_invalid_negative_radius_rejected(self):
        with self.assertRaises(ValueError):
            support_saturation(self.sq, self.sq, self.q,
                               (((Q(1),Q(0),Q(0),Q(0)),Q(0),Q(-1)),))

if __name__ == '__main__': unittest.main()
