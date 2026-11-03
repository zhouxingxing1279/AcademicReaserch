import unittest
from fractions import Fraction as F
import check_run278_exact_slice as m

class ExactSliceTests(unittest.TestCase):
    def test_packet_automaton(self):
        self.assertEqual(m.verify()['packet_history_ticks_5_to_60'],'SSSMMSMMSMMS')
    def test_shared_nonzero_pulse_prefix(self):
        self.assertEqual(m.history_prefix()[45],(F(0),)*4)
    def test_fractional_residual_legal(self):
        self.assertTrue(-1<m.optimal_alpha()<1)
        self.assertEqual(len(m.controls(1)),15)
        self.assertTrue(all(abs(r)<=m.R for r in m.controls(1)))
    def test_true_histories(self):
        p,q=m.continuation(1),m.continuation(-1)
        self.assertEqual(p[60][0],m.EPS)
        self.assertEqual(q[60][0],-m.EPS)
        self.assertEqual(p[60][1],-q[60][1])
    def test_dual_sum(self):
        self.assertEqual(sum(abs(F(1)-F(w,11)) for w in range(14,-1,-1)),F(72,11))
    def test_primal_equals_dual(self):
        self.assertEqual(m.continuation(1)[60][1],m.dual_velocity_bound())
    def test_new_diameter_stronger(self):
        self.assertGreater(2*m.dual_velocity_bound(),F(22724681,40000000))
    def test_first_strict_obstruction(self):
        self.assertEqual(m.first_open_loop_obstruction(),66)
        self.assertLessEqual(m.velocity_diameter_after(65),6)
        self.assertGreater(m.velocity_diameter_after(66),6)
    def test_deterministic_certificate(self):
        self.assertEqual(m.verify(),m.verify())
    def test_final_exact_numbers(self):
        self.assertEqual(m.dual_velocity_bound(),F(39217447,110000000))
        self.assertEqual(m.optimal_alpha(),F(28057872,35710213))

if __name__=='__main__':unittest.main()
