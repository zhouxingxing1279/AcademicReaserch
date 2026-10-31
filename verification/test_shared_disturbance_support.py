"""Run219 focused exact tests; full-repo integration explicitly opt-in."""
import os
import unittest
from fractions import Fraction as Q
import check_shared_disturbance_support as s


class SharedResidualTests(unittest.TestCase):
    def test_two_packet_shared_residual_form(self):
        # Three Euler transitions with known zero torque and T=1, h=J=1/50.
        # x3 from x0=(0,0,0,0), r=(1,1,1) is (3h²,3h,0,0).
        h = Q(1, 50)
        pos = {1: Q(0), 2: h*h}
        ts = {1: Q(1), 2: Q(1)}
        us = {1: Q(0), 2: Q(0)}
        form = s.shared_packet_form({1: Q(1), 2: Q(-1)}, pos, ts, us, 3,
                                    radius=lambda t: Q(1))
        # No noise; the model's true r=1 remains feasible.
        c, C, B = form
        x = (3*h*h, 3*h, Q(0), Q(0))
        self.assertLessEqual(abs(C + s.dot(c, x)), B)

    def test_product_clip_exact(self):
        square = ((Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1)))
        point = ((Q(0), Q(0)),)
        q = (Q(1), Q(0), Q(0), Q(0))
        upper, _ = s.clipped_product_support(square, point, q,
                                              (Q(1), Q(0), Q(0), Q(0)), Q(1, 2))
        self.assertEqual(upper, Q(1, 2))

    def test_exclusion_not_equivalent_to_recovery(self):
        pv = ((Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1)))
        ao = ((Q(0), Q(0)),)
        out = s.certify_direction(pv, ao, (Q(1), Q(0), Q(0), Q(0)),
                                  ((Q(1), Q(0), Q(0), Q(0)), Q(0), Q(1, 2)),
                                  (Q(0), Q(0), Q(0), Q(0)))
        self.assertTrue(out['all_maximizers_excluded'])
        self.assertEqual(out['gain_lower'], Q(1, 2))

    def test_missing_causal_history_rejected(self):
        with self.assertRaises(ValueError):
            s.shared_packet_form({2: Q(1)}, {2: Q(0)}, {}, {}, 3)

    @unittest.skipUnless(os.environ.get('RUN_TICK193_AUDIT') == '1',
                         'requires full repository checkout and explicit opt-in')
    def test_full_checkout_tick193(self):
        out = s.audit_tick193()
        self.assertEqual(out['critical_support_gain_exact'], '5212367/450000000')
        self.assertLess(out['remaining_single_row_slack_approx'], 0)


if __name__ == '__main__':
    unittest.main()
