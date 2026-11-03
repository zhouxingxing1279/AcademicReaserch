"""Run220 exact focused tests; full-checkout integration is explicit opt-in."""
import os
import unittest
from fractions import Fraction as Q
import check_two_shared_rows as s


class TwoSharedRowsTests(unittest.TestCase):
    def setUp(self):
        self.pv=((Q(-1),Q(-1)),(Q(1),Q(-1)),(Q(1),Q(1)),(Q(-1),Q(1)))
        self.ao=((Q(0),Q(0)),)
        self.q=(Q(1),Q(0),Q(0),Q(0))
        self.rows=(((Q(1),Q(1),Q(0),Q(0)),Q(0)),
                   ((Q(1),Q(-1),Q(0),Q(0)),Q(0)))

    def test_two_rows_strictly_better_than_either(self):
        self.assertEqual(s.support(self.pv,self.ao,self.q),Q(1))
        for row in self.rows:
            self.assertEqual(s.propose_dual(self.pv,self.ao,self.q,(row,))['certified_upper'],Q(1))
        sol=s.propose_dual(self.pv,self.ao,self.q,self.rows)
        self.assertTrue(sol['solver_success'])
        self.assertEqual(sol['certified_upper'],Q(0))

    def test_fraction_upper_not_float_objective(self):
        self.assertEqual(s.exact_dual_upper(
            self.pv,self.ao,self.q,self.rows,(Q(499,1000),Q(501,1000))),Q(1,500))

    def test_reject_negative_dual(self):
        with self.assertRaises(ValueError):
            s.exact_dual_upper(self.pv,self.ao,self.q,self.rows,(Q(-1),Q(1)))

    def test_signed_strip_and_truth(self):
        rows=s.halfspaces(((Q(1),Q(0),Q(0),Q(0)),Q(1,2),Q(1,4)))
        self.assertEqual(tuple(b for _,b in rows),(Q(-1,4),Q(3,4)))
        x=(Q(-1,2),Q(0),Q(0),Q(0))
        self.assertTrue(all(s.dot(c,x)<=b for c,b in rows))

    @unittest.skipUnless(os.environ.get('RUN_TICK193_AUDIT')=='1',
                         'requires full repository checkout and explicit opt-in')
    def test_full_checkout_tick193(self):
        result=s.audit_tick193()
        self.assertGreaterEqual(Q(result['extra_certified_gain_exact']),0)
        self.assertTrue(result['truth_contained'])
        self.assertEqual(result['candidate_rows_checked'],12)
        self.assertEqual(result['solver_failures'],0)
        self.assertEqual(Q(result['original_support_exact'])-Q(result['one_row_support_upper_exact']),Q(5212367,450000000))


if __name__=='__main__':
    unittest.main()
