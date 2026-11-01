"""Run235: finite-generator robust invariance rational regression."""
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_finite_rpi as m

class FiniteRpiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert=m.certificate()

    def test_contract_parameters(self):
        self.assertEqual(m.A[1][2],-m.H*m.T)
        self.assertEqual(m.B,(0,m.H,0,0))
        self.assertEqual(m.D,F(1742383,800000))

    def test_exact_block_contraction(self):
        self.assertLess(F(self.cert['rho_upper']),1)
        self.assertEqual(self.cert['block_length'],800)

    def test_finite_membership_dimensions(self):
        self.assertEqual(self.cert['generator_count'],4000)
        self.assertIn('LP feasibility',self.cert['membership'])

    def test_state_and_torque_strict_slack(self):
        for bound,limit in zip(self.cert['state_abs_upper'],m.LIMITS):
            self.assertLess(F(bound),limit)
        self.assertLess(F(self.cert['torque_abs_upper']),m.TAU_MAX)

    def test_nonzero_box_and_scope(self):
        self.assertGreater(F(self.cert['tail_box_halfwidth_upper']),0)
        self.assertEqual(self.cert['gate_A'],'blocked_for_output_feedback_SMF_MPC')

    def test_generator_support_matches_certified_bounds(self):
        support=[F(0)]*4
        torque=F(0)
        generators=0
        for g in m.finite_generators():
            generators+=1
            for i in range(4): support[i]+=abs(g[i])
            torque+=abs(m.dot(m.K,g))
        self.assertEqual(generators,4000)
        for value,bound in zip(support,self.cert['state_abs_upper']):
            self.assertLessEqual(value,F(bound))
        self.assertLessEqual(torque,F(self.cert['torque_abs_upper']))

    def test_400_step_construction_rejected_by_constraints(self):
        with self.assertRaises(AssertionError): m.certificate(400)

    def test_zero_block_rejected(self):
        with self.assertRaises(ValueError): m.certificate(0)

    def test_real_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertEqual(m.verify(root),self.cert)
        else:self.skipTest('requires full checkout; GitHub CI must verify')

if __name__=='__main__': unittest.main()
