"""Run239 exact primal-dual noisy-position SMF regressions."""
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_posterior_strip as m

class PosteriorStripTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=m.verify()

    def test_source_run238_exact(self):
        self.assertEqual(len(m.two_dim_generators()),16)
        self.assertEqual(sum(p for p,v in m.two_dim_generators()),F(78628341,800000000))

    def test_branch_primal_dual_equality(self):
        for s in (-1,1):
            for y in (F(0),F(1,20),-F(1,20)):
                w=m.branch_upper(s,y,m.NOISE)
                self.assertIsNotNone(w)
                self.assertLessEqual(abs(w['position_witness']-y),m.NOISE)

    def test_exact_posterior_velocity(self):
        self.assertEqual(m.posterior_upper(F(0))['upper'],F(353411321,960000000))
        self.assertEqual(m.posterior_upper(F(0))['sign'],-1)

    def test_nonzero_noise_effect(self):
        self.assertEqual(m.posterior_upper(F(0),F(0))['upper'],F(281453,1000000))
        self.assertLess(m.posterior_upper(F(0),F(0))['upper'],m.posterior_upper(F(0))['upper'])

    def test_no_uniform_shrink(self):
        pmax=sum(p for p,v in m.two_dim_generators())
        self.assertEqual(m.posterior_upper(pmax)['upper'],F(52180511,80000000))

    def test_ambiguous_last_disturbance(self):
        self.assertEqual(m.two_dim_generators()[-1],(F(0),m.H*m.R))
        self.assertEqual(2*m.H*m.R,F(3246383,40000000))

    def test_conditional_next_gap_safety(self):
        self.assertTrue(self.c['conditional_additional_15_tick_state_and_input_safe'])
        self.assertLess(F(self.c['conditional_additional_15_tick_zero_torque_position_bound']),m.LIMITS[0])
        self.assertLess(F(self.c['conditional_additional_15_tick_zero_torque_velocity_bound']),m.LIMITS[1])

    def test_no_recursive_claim(self):
        self.assertFalse(self.c['posterior_valid_for_all_measurements'])
        self.assertFalse(self.c['recursive_invariance_certified'])
        self.assertFalse(self.c['smf_mpc_closed_loop_certified'])

    def test_empty_observation(self):
        self.assertIsNone(m.posterior_upper(F(1)))

    def test_config_contract(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertEqual(m.verify(root),self.c)
        else:self.skipTest('requires complete repository checkout')

if __name__=='__main__':unittest.main()
