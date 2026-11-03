import unittest
from fractions import Fraction as Q
from check_compression_performance import (case, sweep, interpolation_factor, witness,
                                           cz_support_certificate, quadratic_dual, stopping_probe)


class CompressionPerformanceTests(unittest.TestCase):
    def test_partial_measurement_strict_control_gap(self):
        r = witness()
        self.assertEqual(r['full']['u'][0], Q(63,500))
        self.assertEqual(r['box']['u'][0], Q(9,100))
        self.assertFalse(r['box_retains_candidate'])
        self.assertEqual(r['missing']['u'][0], Q(3,25))
        self.assertEqual(r['queried']['u'][0], Q(123,1000))

    def test_cost_certificate_and_dual_sign(self):
        r = witness()['queried']
        self.assertEqual(r['cost_gap'], Q(333,1000000))
        self.assertEqual(r['interpolation_bound'], Q(342,1000000))
        self.assertEqual(r['quadratic_interpolation_bound'], r['cost_gap'])
        self.assertLess(r['old_dual_linear_term'], r['cost_gap'])
        self.assertGreaterEqual(r['new_dual_bound'], r['cost_gap'])

    def test_zero_margin_requires_zero_inflation(self):
        r=case(Q(1,50),Q(0),None)
        self.assertEqual(r['cost_gap'],0)
        self.assertEqual(interpolation_factor([Q(0)],[Q(0)]),0)
        with self.assertRaises(ValueError):
            interpolation_factor([Q(1,1000)],[Q(0)])

    def test_direction_scaling_does_not_change_factor(self):
        self.assertEqual(interpolation_factor([Q(1,10),Q(1,5)],[Q(1,2),Q(1,4)]),
                         interpolation_factor([Q(7,10),Q(3,5)],[Q(7,2),Q(3,4)]))

    def test_parameter_sweep(self):
        r=sweep()
        self.assertEqual(r['cases'],216)
        self.assertEqual(r['failures'],0)
        self.assertGreater(r['box_candidate_losses'],0)

    def test_cz_primal_and_dual_match_exactly(self):
        lower,upper,lam,vertex=cz_support_certificate(Q(1,50),(Q(4,5),Q(1,5)))
        self.assertEqual(lower,Q(8,125))
        self.assertEqual(lower,upper)
        self.assertEqual(lam,Q(1,5))
        self.assertEqual(vertex,(Q(1,10),-Q(2,25)))

    def test_dual_bound_works_without_optimal_multiplier(self):
        for lam in (Q(0),Q(1,10),Q(1,5),Q(1)):
            lower=quadratic_dual((Q(9,50),Q(0)),(Q(1),Q(1)),
                                 [(Q(1),Q(0))],[Q(63,500)],[lam])
            self.assertLessEqual(lower,Q(729,250000))
        with self.assertRaises(ValueError):
            quadratic_dual((Q(0),),(Q(1),),[(Q(1),)],[Q(0)],[-Q(1)])

    def test_stopping_distinguishes_accuracy_from_budget(self):
        converged=stopping_probe()
        interrupted=stopping_probe(budget=0)
        self.assertTrue(converged['tolerance_met'])
        self.assertEqual(converged['trace'][-1]['query_rounds'],2)
        self.assertFalse(interrupted['tolerance_met'])
        self.assertEqual(interrupted['trace'][0]['u'],(Q(3,25),Q(0)))


if __name__=='__main__': unittest.main()
