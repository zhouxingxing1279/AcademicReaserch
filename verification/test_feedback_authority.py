import unittest
from fractions import Fraction as Q
import numpy as np
from check_feedback_authority import authority_certificate, InputTransport, input_path_check
from check_transport_template import Transport

class FeedbackAuthorityContracts(unittest.TestCase):
    def test_every_feedback_obstruction_exact_boundary(self):
        r = authority_certificate()
        self.assertEqual(r['first_position_failure'], 209)
        self.assertLessEqual(Q(r['p208']), 5)
        self.assertEqual(Q(r['p209']), Q(5013796793, 1000000000))
        self.assertEqual(Q(r['necessary_D_at_356']), Q(2657458367,631900000))

    def test_known_thrust_is_kept_in_matrix_and_affine_offset(self):
        t = InputTransport(Q('14.715'))
        x = np.array([Q(0)]*6, dtype=object)
        x[4] = Q('.1')
        xp = t.f @ x+t.offset
        self.assertEqual(xp[2], -Q('14.715')*Q('.1')/50)
        self.assertEqual(xp[3], Q('4.905')/50)
        self.assertLess(t.dx, Transport().dx)
        for i, terms in enumerate(t.terms):
            lhs = sum((w*t.h[j] for j,w in terms), np.array([Q(0)]*6))
            self.assertTrue(np.array_equal(lhs, t.h[i] @ t.f))
            self.assertEqual(t.q[i], sum(abs(v) for v in t.h[i] @ t.w)+t.h[i] @ t.offset)

    def test_invalid_thrust_is_rejected(self):
        for value in (Q(0), Q(15), 9.81):
            with self.assertRaises((ValueError, TypeError)):
                InputTransport(value)

    def test_variable_input_shift_and_membership(self):
        r=input_path_check(30)
        self.assertEqual(r['shift_rows'], 30*25*72)
        self.assertEqual(r['posterior_memberships'],31)

if __name__=='__main__':
    unittest.main()
