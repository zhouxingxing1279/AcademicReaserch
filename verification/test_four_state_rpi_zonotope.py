"""Run234: rational nonlinear four-state RCI proof regression."""
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_rpi_zonotope as m


class ExactZonotopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert = m.certificate()

    def test_frozen_linearization(self):
        self.assertEqual(m.A[1][2], -m.H*m.T)
        self.assertEqual(m.A[3], tuple(-k if i < 3 else 1-k for i,k in enumerate(m.K)))
        self.assertEqual(m.B, (0, m.H, 0, 0))

    def test_adversarial_acceleration_bound(self):
        self.assertEqual(m.R, F(47,25)+F(243,16000)*m.T)
        self.assertEqual(m.D-m.R, m.T*m.PHI_LIMIT**3/6)

    def test_power_contracts(self):
        self.assertLess(F(self.cert['power_infinity_norm_upper']), F(1))
        self.assertEqual(self.cert['block_length'], 800)

    def test_strict_state_and_input_slacks(self):
        for x,lim in zip(self.cert['state_abs_upper_rounded_outward'],m.LIMITS):
            self.assertLess(F(x), lim)
        self.assertLess(F(self.cert['torque_abs_upper_rounded_outward']),m.TAU_MAX)

    def test_proof_scope_explicit(self):
        self.assertEqual(self.cert['gate_A'], 'blocked_for_output_feedback_MPC')
        self.assertIn('full-state',self.cert['quantifiers']+' '+' '.join(self.cert['limitations']))

    def test_rounding_is_outward(self):
        self.assertEqual(m.round_up(F(1,3)), '0.333334')
        self.assertEqual(m.round_up(F(1,2)), '0.500000')

    def test_reject_zero_block(self):
        with self.assertRaises(ValueError):m.certificate(0)

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertEqual(m.verify(root),self.cert)
        else:self.skipTest('requires complete checkout; CI must verify')

if __name__=='__main__':unittest.main()
